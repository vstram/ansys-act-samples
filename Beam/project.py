'''
This script defines the Beam Wizard.

In fact, it defines how the user advances towards the end of the wizard, by guiding the user through
different steps

Created on 27/05/2016

@author: vinicius@esss.com.br
'''
geometrySystem = None
mechanicalSystem = None

def CreateGeometry(step):
    '''
    Creates the Geometry
    
    This method is called at the first step.
    Actually, gathers the beam dimensions and forwards this information to the 'dm.py' module
    
    :param step:
    '''
    ExtAPI.Log.WriteMessage("--------> Project:CreateGeometry")
    
    global geometrySystem

    # gathers the beam properties
    length = step.Properties["GeometryProperties/Length"]
    height = step.Properties["GeometryProperties/Height"]
    width = step.Properties["GeometryProperties/Width"]
    
    # creates the Design Modeller system
    geometryTemplate = GetTemplate(TemplateName="Geometry")
    geometrySystem = geometryTemplate.CreateSystem()
    geometryContainer = geometrySystem.GetContainer(ComponentName="Geometry")

    # stores the beam information in the ACT
    ExtAPI.ExtensionManager.CurrentExtension.Attributes["geoData"] = {
        "Length": length.DisplayString, 
        "Height": height.DisplayString, 
        "Width": width.DisplayString
    }
        
    ExtAPI.Log.WriteMessage("--------> Project:CreateGeometry - Properties %s %s %s: " % (length, height, width))
    
    # executes Design Modeller 
    string = """load = ExtAPI.ExtensionManager.GetExtensionByName("Beam").GetModule().CreateBeam(None)"""
    geometryContainer.Edit(Interactive=False)
    geometryContainer.SendCommand(Language = "Python", Command = string)
    geometryContainer.Update()
    geometryContainer.Exit()

def DeleteGeometry(step):
    '''
    Deletes the Design Modeller system.
    
    :param step:
    '''
    global geometrySystem
    geometrySystem.Delete()

def CreateSetup(step):
    '''
    Creates/Defines the Mechanical setup
    '''
    ExtAPI.Log.WriteMessage("--------> Project:CreateSetup")
    global mechanicalSystem, geometrySystem    

    material = step.Properties["Properties/Material"].Value
    elementSize = step.Properties["Meshing/ElementSize"]

    mechanicalTemplate = GetTemplate(TemplateName="Static Structural", Solver="ANSYS")
    geometryComponent = geometrySystem.GetComponent(Name="Geometry")
    mechanicalSystem = mechanicalTemplate.CreateSystem(
        ComponentsToShare=[geometryComponent], 
        Position="Right",  
        RelativeTo=geometrySystem
    )   
     
    materialName = CreateMaterial(mechanicalSystem, material)    
    
    ExtAPI.ExtensionManager.CurrentExtension.Attributes["mechData"] = {
        "Material": materialName, 
        "ElementSize": elementSize.DisplayString, 
    }
    
    modelComponent = mechanicalSystem.GetComponent(Name="Model")
    modelComponent.Refresh()

    model = mechanicalSystem.GetContainer(ComponentName="Model")
    model.Edit(Interactive=False)
    model.SendCommand(
        Language = "Python", 
        Command = """
module = ExtAPI.ExtensionManager.GetExtensionByName("Beam").GetModule()
module.AssignMaterial()
module.CreateMeshControls()
"""
    )
    #mechanicalSystem.Update()
    model.Exit()


def DeleteSetup(step):
    '''
    Deletes the Mechanical setup system.
    
    :param step:
    '''
    global mechanicalSystem
    mechanicalSystem.Delete()

    
def DefineLoadSetup(step):
    '''
    Creates/Defines the Mechanical setup
    '''
    ExtAPI.Log.WriteMessage("--------> Project:DefineLoadSetup")
    global mechanicalSystem 

    forceValue = step.Properties["Loading/Force"] 
    
    ExtAPI.ExtensionManager.CurrentExtension.Attributes["mechData"] = {
        "ForceValue": forceValue.DisplayString, 
    }

    model = mechanicalSystem.GetContainer(ComponentName="Model")
    model.Edit(Interactive=True)
    model.SendCommand(
        Language = "Python", 
        Command = """
module = ExtAPI.ExtensionManager.GetExtensionByName("Beam").GetModule()
module.CreateLoads()
"""
    )
    #mechanicalSystem.Update()
    model.Exit()

    
def isPositive(step, prop):
    '''
    Auxiliar method used to check if the property's value is positive
    
    :param step:
    :param prop:
    '''
    return prop.Value > 0
    
def CreateMaterial(system, material):
    '''
    Creates the material
    
    :param system:
    :param system: str
        The material name
    '''
    ExtAPI.Log.WriteMessage("--------> Project:CreateMaterial")
    engineeringData = system.GetContainer(ComponentName="Engineering Data")
    newMaterial = engineeringData.ImportMaterial( 
        Name=material, Source="General_Materials.xml")
    
    return newMaterial.DisplayName

    

