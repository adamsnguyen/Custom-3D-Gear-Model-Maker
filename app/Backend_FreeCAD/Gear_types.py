# =============================================================================
# File Name     : Gear_types.py
# Description   : This module integrates the web application with FreeCAD
# =============================================================================

import math
import FreeCAD
import Sketcher
import Mesh
import PartDesign
import Part
import os

# This class contains parameters and functions to generate and export a Base Gear
class Gear_initial():

    # Constructor of the Base Gear which initalises/stores parameters of Base Gear
    # kwargs: Dictionary with elements containg numbers (real and integer) and boolean value 
    def __init__(self, **kwargs):
        self.height = kwargs.get('height')
        self.num_teeth = kwargs.get("num_teeth")
        self.pitch_dia = kwargs.get("pitch_dia")
        self.hole_dia = kwargs.get("hole_dia")
        self.angle_teeth = kwargs.get("angle_teeth", 0)
        self.pressure_angle = kwargs.get("pressure_angle", 20)
        self.clearance = kwargs.get("clearance", 0.12)
        self.double_helix = kwargs.get("double_helix", False)
        self.ID = kwargs.get("ID")
    
    # This function performs and computes Model modification of Base Gear
    # filedoc:  Name of the Gear File (type: string) 
    # fileobj:  Name of Gear Part in FreeCAD (type: string)
    # kwargs:   Dictionary with elements containg numbers (real and integer) and boolean value
    # Returns nothing  
    def Model_Modification(self, filedoc, fileobj, **kwargs):
        FreeCAD.getDocument(filedoc).getObject(fileobj).height = '{} mm'.format(self.height)
        FreeCAD.getDocument(filedoc).getObject(fileobj).teeth = self.num_teeth
        FreeCAD.getDocument(filedoc).getObject(fileobj).beta = '{} deg'.format(self.angle_teeth)
        FreeCAD.getDocument(filedoc).getObject(fileobj).module  = '{} mm'.format(self.pitch_dia / self.num_teeth)
        FreeCAD.getDocument(filedoc).getObject('Cylinder').Radius = '{} mm'.format(self.hole_dia /2)
        FreeCAD.getDocument(filedoc).getObject('Cylinder').Height = '{} mm'.format(self.height + 1)
        FreeCAD.getDocument(filedoc).getObject(fileobj).clearance = self.clearance 
        FreeCAD.ActiveDocument.recompute()

    # This function finds the gears that are to be edited according to  
    # the method chosen and executes the model modification function
    # gear_mod: Type of gear modification method (type: string)
    # kwargs:   Dictionary with elements containg numbers (real and integer) and boolean value
    # Returns nothing
    # Raises a Value Error if gear type is not chosen correctly
    def GearMod(self, gear_mod: str, **kwargs):
        directory = os.path.join(os.path.dirname(__file__), 'Part_files\\')
        if gear_mod == "rack":
            partname = 'Rack_Gear' + '.FCStd'
            filedoc = "Rack_Gear"
            fileobj = "involuterack"

        elif gear_mod == "worm": 
            partname = 'Worm_Gear' + '.FCStd'
            filedoc = "Worm_Gear"
            fileobj = "wormgear"

        elif gear_mod == "bevel":
            partname =   'Bevel_Gear' + '.FCStd'
            filedoc, fileobj = 'Bevel_Gear', 'bevelgear'

        elif gear_mod in ["spur", "helix", "double_helix"]:
            partname = 'Involute_Gear' + '.FCStd'
            filedoc, fileobj = 'Involute_Gear', 'involutegear'

        else:
            raise ValueError("Invalid gear type")
            
        file = os.path.join(directory, partname)

        # Opening the gear file and modifying it
        FreeCAD.openDocument(file)
        self.Model_Modification(filedoc, fileobj, **kwargs)

    # This function exports the Gear file that was generated as an .stl
    # filedoc:      Name of the Gear File (type: string) 
    # nameoffile:   Name of the saved generated .stl file (type:string)
    # Returns nothing
    def Export_Gear(self, filedoc, nameoffile):
        Gear=[]
        Gear.append(FreeCAD.getDocument(filedoc).getObject("Cut"))
        direcetory = os.path.dirname(__file__)
        filedir = os.path.join(direcetory, 'Part_files\\')
        Mesh.export(Gear, filedir + nameoffile + ".stl")
        del Gear
   
   # This function contains general paramters of base gear in dictionary
   # Returns a dictionary with the attributes of base gear, which are numbers or bool
    def getParameters(self):
        gear_params = {'height' : self.height, 'num_teeth' : self.num_teeth, 'pitch_dia' : self.pitch_dia, 'hole_dia' : self.hole_dia, 
        'pressure_angle' : self.pressure_angle, 'angle_teeth' : self.angle_teeth, 'double_helix' : self.double_helix,  'clearance' : self.clearance }
        return gear_params

# Different types of Gears
# This inherited class contains parameters and functions to generate and export a Spur Gear
class Gear_involute(Gear_initial):

    # Constructor of the Spur Gear which initalises/stores parameters of Spur Gear
    # Inherits from base class Gear_initial and Calls the gear modification method
    # Exports the generated gear with name as ID
    # kwargs: Dictionary with elements containg numbers (real and integer) and boolean value
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Spur Gear Attributes
        self.angle_teeth = 0
        self.double_helix = False

        self.GearMod(gear_mod="spur", **self.getParameters())
        super().Export_Gear( 'Involute_Gear', self.ID)

# This class contains parameters and functions to generate and export a Helix/Angle Gear
class Gear_angle(Gear_initial):

    # Constructor of the Helix Gear which initalises/stores parameters of Helix Gear
    # Inherits from base class Gear_initial and Calls the gear modification method
    # Exports the generated gear with name as ID
    # kwargs: Dictionary with elements containg numbers (real and integer) and boolean value
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Helix Gear Attributes
        self.double_helix = False

        self.GearMod(gear_mod="helix", **self.getParameters())
        super().Export_Gear('Involute_Gear', self.ID)

# This class contains parameters and functions to generate and export a Double Helix Gear
class Gear_double_helix(Gear_initial):
    
    # Constructor of the Double Helix Gear which initalises/stores parameters of Double Helix Gear
    # Inherits from base class Gear_initial and Calls the gear modification method
    # kwargs: Dictionary with elements containg numbers (real and integer) and boolean value
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Double Helix Gear Attributes
        self.double_helix = True

        self.Gear_Mod_(**self.getParameters())

    # This function calls the Gear modification method from base class and applies changes
    # then applies double helix gear specific changes and exports the generated gear with name as ID
    # kwargs: Dictionary with elements containg numbers (real and integer) and boolean value
    # Returns nothing
    def Gear_Mod_(self, **kwargs):
        self.GearMod(gear_mod="double_helix", **kwargs)
        FreeCAD.getDocument('Involute_Gear').getObject('involutegear').double_helix = kwargs.get("double_helix")
        FreeCAD.ActiveDocument.recompute()
        super().Export_Gear('Involute_Gear', self.ID)

# This class contains parameters and functions to generate and export a Bevel Gear
class Gear_bevel(Gear_initial):

    # Constructor of the Bevel Gear which initalises/stores parameters of Bevel Gear
    # Inherits from base class Gear_initial and defines bevel gear specific parameters
    # Calls the gear modification method
    # kwargs: Dictionary with elements containg numbers (real and integer) and boolean value
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Bevel Gear Attributes
        self.reset_origin = True
        self.double_helix = False
        self.pitch_angle = kwargs.get("pitch_angle", 45)
        self.backlash = kwargs.get("backlash",0)

        self.Gear_Mod_(**self.getParameters())
    
    # This function contains specific parameters of the bevel gear in dictionary  
    # which are inherited from base class
    # Returns a dictionary with the attributes of bevel gear, which are numbers or bool
    def getParameters(self):
        gear_params = Gear_initial.getParameters(self)
        ind_params = {'backlash' : self.backlash, 'reset_origin' : self.reset_origin, 'pitch_angle' : self.pitch_angle}
        gear_params.update(ind_params)
        return gear_params

    # This function calls the Gear modification method from base class and applies changes
    # then applies bevel gear specific changes and exports the generated gear with name as ID
    # kwargs: Dictionary with elements containg numbers (real and integer) and boolean value
    # Returns nothing
    def Gear_Mod_(self, **kwargs):
        self.GearMod(gear_mod="bevel",**kwargs)
        FreeCAD.getDocument('Bevel_Gear').getObject('bevelgear').backlash = '{} mm'.format(kwargs.get("backlash"))
        FreeCAD.getDocument('Bevel_Gear').getObject('bevelgear').reset_origin = kwargs.get("reset_origin")
        FreeCAD.getDocument('Bevel_Gear').getObject('bevelgear').pitch_angle = '{} deg'.format(kwargs.get("pitch_angle"))
        FreeCAD.ActiveDocument.recompute()
        super().Export_Gear('Bevel_Gear', self.ID)

# This class contains parameters and functions to generate and export a Worm Gear
class Gear_worm(Gear_initial):

    # Constructor of the Worm Gear which initalises/stores parameters of Worm Gear
    # Inherits from base class Gear_initial and defines worm gear specific parameters
    # Calls the gear modification method
    # kwargs: Dictionary with elements containg numbers (real and integer) and boolean value
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Worm Gear Attributes
        self.reverse_pitch = kwargs.get("reverse_pitch", False)
        self.double_helix = False

        self.Gear_Mod_(**self.getParameters())
    
    # This function contains specific parameters of the worm gear in dictionary  
    # which are inherited from base class
    # Returns a dictionary with the attributes of worm gear, which are numbers or bool
    def getParameters(self):
        gear_params = Gear_initial.getParameters(self)
        ind_params = {'reverse_pitch' : self.reverse_pitch, 'clearance' : self.clearance }
        gear_params.update(ind_params)
        return gear_params
    
    # This function calls the Gear modification method from base class and applies changes
    # then applies worm gear specific changes and exports the generated gear with name as ID
    # kwargs: Dictionary with elements containg numbers (real and integer) and boolean value
    # Returns nothing
    def Gear_Mod_(self, **kwargs):
        self.GearMod(gear_mod="worm", **kwargs)
        FreeCAD.getDocument('Worm_Gear').getObject('wormgear').reverse_pitch = kwargs.get("reverse_pitch")
        FreeCAD.getDocument('Worm_Gear').getObject('wormgear').diameter = '{} mm'.format(kwargs.get("pitch_dia"))
        FreeCAD.ActiveDocument.recompute()
        super().Export_Gear('Worm_Gear', self.ID)

# This class contains parameters and functions to generate and export a Rack Gear
class Gear_rack(Gear_initial):
    
    # Constructor of the Rack Gear which initalises/stores parameters of Rack Gear
    # Inherits from base class Gear_initial and defines rack gear specific parameters
    # Calls the gear modification method
    # kwargs: Dictionary with elements containg numbers (real and integer) and boolean value
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        #   Rack Gear Attributes
        self.add_ending = kwargs.get("add_endings", False)
        self.simp = kwargs.get("simplified", False)
        self.double_helix = kwargs.get("double_helix", False)
        self.thickness = kwargs.get("thickness", 5)
        self.head = kwargs.get("head", 0)

        self.Gear_Mod_(**self.getParameters())
    
    # This function contains specific parameters of the rack gear in dictionary  
    # which are inherited from base class
    # Returns a dictionary with the attributes of rack gear, which are numbers or bool
    def getParameters(self):
        gear_params = Gear_initial.getParameters(self)
        ind_params = {'thickness' : self.thickness, 'simplified' : self.simp, 'add_endings' : self.add_ending, 'head' : self.head}
        gear_params.update(ind_params)
        return gear_params
    
    # Because this gear has no Cylinder object therefore, the Model_Modification is overridden here
    # This function performs and computes Model modification of Rack Gear
    # filedoc:  Name of the Gear File (type: string) 
    # fileobj:  Name of Gear Part in FreeCAD (type: string)
    # kwargs:   Dictionary with elements containg numbers (real and integer) and boolean value
    # Returns nothing 
    def Model_Modification(self, filedoc, fileobj, **kwargs):
        directory = os.path.join(os.path.dirname(__file__), 'Part_files\\')
        partname = 'Rack_Gear' + '.FCStd'
        file = os.path.join(directory, partname)

        #   Getting the file
        FreeCAD.openDocument(file)
        FreeCAD.getDocument(filedoc).getObject(fileobj).height = '{} mm'.format(kwargs.get("height"))
        FreeCAD.getDocument(filedoc).getObject(fileobj).teeth = kwargs.get("num_teeth")
        FreeCAD.getDocument(filedoc).getObject(fileobj).beta = '{} deg'.format(kwargs.get("angle_teeth"))
        FreeCAD.getDocument(filedoc).getObject(fileobj).module  = '{} mm'.format(kwargs.get('pitch_dia') / kwargs.get("num_teeth"))#* math.cos(kwargs.get('angle_teeth')))
        FreeCAD.getDocument(filedoc).getObject(fileobj).clearance = kwargs.get("clearance")
        FreeCAD.ActiveDocument.recompute()
    
    # This function calls the Gear modification method from base class and applies changes
    # then applies Rack gear specific changes and exports the generated gear with name as ID
    # kwargs: Dictionary with elements containg numbers (real and integer) and boolean value
    # Returns nothing
    def Gear_Mod_(self, **kwargs):
        self.Model_Modification("Rack_Gear", 'involuterack', **kwargs)
        FreeCAD.getDocument('Rack_Gear').getObject('involuterack').head = kwargs.get("head")
        FreeCAD.getDocument('Rack_Gear').getObject('involuterack').thickness = '{} mm'.format(kwargs.get("thickness"))
        FreeCAD.getDocument('Rack_Gear').getObject('involuterack').add_endings = kwargs.get("add_endings")
        FreeCAD.getDocument('Rack_Gear').getObject('involuterack').double_helix = kwargs.get("double_helix")
        FreeCAD.getDocument('Rack_Gear').getObject('involuterack').simplified = kwargs.get("simplified")
        FreeCAD.ActiveDocument.recompute()
        self.Export_Gear('Rack_Gear', "Rack", self.ID)

    # As this model does not have any hole
    # This function exports the Rack Gear file that was generated as an .stl
    # filedoc:      Name of the Gear File (type: string) 
    # nameoffile:   Name of the saved generated .stl file (type:string)
    # Returns nothing
    def Export_Gear(self, filedoc, nameoffile):
        Gear=[]
        Gear.append(FreeCAD.getDocument(filedoc).getObject("Body"))
        directory = os.path.dirname(__file__)
        filedir = os.path.join(directory, 'Part_files\\')
        Mesh.export(Gear, filedir + nameoffile + ".stl")
        del Gear