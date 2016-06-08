'''
This script defines the Mechanical setup.

It only uses the new ACT Application Program Interface (API) to define the mechanical setup 
(no jscript core are used).

More advanced techniques could be used to define the mechanical setup, such as:
* Use legacy APDL snippets mixed with python to perform advanced operations
* Use python to call an external application or solver
* Implements a completely new boundary condition or load with python

Created on 27/05/2016

@author: vinicius@esss.com.br
'''
import os
import exportImage
    
def AssignMaterial():
    '''
    Assigns the material
    
    :param materialName: str
        The material name
    
    '''
    ExtAPI.Log.WriteMessage("--------> DS:AssignMaterial")
    
    ExtAPI.ExtensionManager.CurrentExtension.UpdateAttributes()
    mechData = ExtAPI.ExtensionManager.CurrentExtension.Attributes["mechData"]
    materialName = mechData["Material"]
    
    model = ExtAPI.DataModel.Project.Model
    model.Geometry.Children[0].Children[0].Assignment = materialName
    
    
def CreateMeshControls():
    '''
    Defines the mesh controls
    
    :param elementSize:
    '''
    ExtAPI.Log.WriteMessage("--------> DS:CreateMeshControls")
    ExtAPI.ExtensionManager.CurrentExtension.UpdateAttributes()
    mechData = ExtAPI.ExtensionManager.CurrentExtension.Attributes["mechData"]
    elementSize = mechData["ElementSize"]
    
    model = ExtAPI.DataModel.Project.Model
    mesh = model.Mesh

    # defines the meshing method
    sizing = mesh.AddSizing()
    
    # selects the geometry (in this case, all parts)
    ids = []
    for part in ExtAPI.DataModel.GeoData.Assemblies[0].Parts:
        for body in part.Bodies:
            ids.Add(body.Id)
    sel = ExtAPI.SelectionManager.CreateSelectionInfo(SelectionTypeEnum.GeometryEntities)
    sel.Ids = ids
    sizing.Location = sel
    
    # applies the sizing
    ExtAPI.Log.WriteMessage("--------> elementSize: %s" % elementSize)
    sizing.ElementSize = Quantity(elementSize.replace(',','.'))
    
    # generates the mesh
    mesh.GenerateMesh()
    
    
def CreateLoads():
    '''
    Creates the Loads
    '''
    ExtAPI.Log.WriteMessage("--------> DS:CreateLoads:")
    ExtAPI.ExtensionManager.CurrentExtension.UpdateAttributes()
    mechData = ExtAPI.ExtensionManager.CurrentExtension.Attributes["mechData"]
    forceValue = mechData["ForceValue"]
    
    model = ExtAPI.DataModel.Project.Model
    analysis = model.Analyses[0]    

    # defines a fixed support (analysis has a plenty of different types of BCs that can be used)
    support = analysis.AddFixedSupport()
    
    # selects the appropriate face to apply the fixed support
    fixedFaceId = ExtAPI.DataModel.GeoData.Assemblies[0].Parts[0].Bodies[0].Faces[0].Id
    sel = ExtAPI.SelectionManager.CreateSelectionInfo(SelectionTypeEnum.GeometryEntities)
    sel.Ids = [fixedFaceId]
    support.Location = sel # applies the fixed support BC
    
    # clears the selection
    ExtAPI.SelectionManager.ClearSelection()
    
    # defines a force load
    force = analysis.AddForce()
    
    # selects the appropriate face to apply the load
    appliedFaceId = ExtAPI.DataModel.GeoData.Assemblies[0].Parts[0].Bodies[0].Faces[4].Id
    sel.Ids = [appliedFaceId]
    force.Location = sel # applies the load BC
    
    # defines the load, according with the user inputs
    ExtAPI.Log.WriteMessage("--------> forceValue: %s" % forceValue)
    force.DefineBy = LoadDefineBy.Components
    force.XComponent.Output.DiscreteValues = [Quantity('0 [N]')]
    force.YComponent.Output.DiscreteValues = [Quantity(forceValue.replace(',','.'))]
    force.ZComponent.Output.DiscreteValues = [Quantity('0 [N]')]
    
    # solves the simulation
    analysis.Solve(True)
    
    # creates the results
    _CreateResults()
        

def _CreateResults():
    '''
    Internal method, used only to create some results
    '''
    # adds a total deformation result
    dataModel = ExtAPI.DataModel
    solution = dataModel.Project.Model.Analyses[0].Solution
    workdir = os.path.normpath(os.path.join(solution.WorkingDir, '..\\..\..\\user_files'))
    totalDeformation = solution.AddTotalDeformation()
    
    # defines the image filename
    fileName = os.path.join(workdir, totalDeformation.Name.replace(' ', '_') + '.png')
    
    # updates the results
    solution.EvaluateAllResults()
    
    totalDeformation.Activate()

    # JScript to generate the export the image
    contents = exportImage.jscriptContents.replace(
        '{$fileName}', fileName.replace('\\', '/')).replace(
            '{$target}', 'Total Deformation')
    
    # writes the JS Script that captures the image
    scriptDebugFilename = 'scriptDebug.js'
    oss = open(os.path.join(workdir, scriptDebugFilename), 'w')
    oss.write(contents)
    oss.close()
   
    # Export the image (executes the script)
    ExtAPI.Application.ScriptByName("jscript").ExecuteCommand(contents)
    
    # Adds a figure below the result
    totalDeformationFigure = totalDeformation.AddFigure()
    



    