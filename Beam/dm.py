'''
This script is intended to generate the Beam geometry.

It only uses the new ACT Application Program Interface (API) to define the geometry 
(no jscript core are used).

More advanced techniques could be used to generate the geometry, such as:
* Import a pre-built geometry from a different CAD (Creo, NX, SolidWorks) and do some modifications 
  or cleaning operations in Design Modeller
* Use the math library to create complex geometries like Conical, hourglass and barrel-shaped springs.

Created on 27/05/2016

@author: vinicius@esss.com.br
'''
import units
import math

def CreateBeam(ag):
    '''
    Create the Beam object in the tree.
    
    The Beam object is created in the tree and allow the user define the beam dimensions.
    After this, he/she needs to click on the Generate Button to effectively create the beam.
    (this will call the method 'GenerateBeam')
    
    :param ag: 
        The Analysis object
    '''
    ExtAPI.Log.WriteMessage("--------> DM:CreateBeam")
    ExtAPI.ExtensionManager.CurrentExtension.UpdateAttributes()
    
    geoData = ExtAPI.ExtensionManager.CurrentExtension.Attributes["geoData"]
    feature = ExtAPI.CreateFeature("Beam")
    
def OnGenerateBeam(feature, function):
    '''
    Generates the Beam in the graphical window
    
    :param feature: 
    :param function: 
    '''
    ExtAPI.Log.WriteMessage("--------> DM:OnGenerateBeam")
    
    geoData = ExtAPI.ExtensionManager.CurrentExtension.Attributes["geoData"]
    length = geoData["Length"]
    height = geoData["Height"]
    width = geoData["Width"]
    
    ExtAPI.Log.WriteMessage("--------> DM:OnGenerateBeam: %s %s %s " % (length,height,width))
    
    # First point
    point1 = [0.,0.,0.]
    
    # Constructs the second point and also replaces the comma by dot, if needed
    point2 = [
        Quantity(width.replace(',','.')).Value,
        Quantity(height.replace(',','.')).Value,
        Quantity(length.replace(',','.')).Value
    ]
    
    # this list holds the solids that will be created (in this case only one)
    solidBodies = []

    # creates the solid
    primitives = ExtAPI.DataModel.GeometryBuilder.Primitives
    beam = primitives.Solid.CreateBox(point1, point2)
    beamGenerated = beam.Generate()
    solidBodies.Add(beamGenerated)

    # adds the new solid to the feature object
    feature.Bodies = solidBodies
    feature.MaterialType = MaterialTypeEnum.Add

    return True