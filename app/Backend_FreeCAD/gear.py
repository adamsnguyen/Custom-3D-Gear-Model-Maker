# =============================================================================
# File Name     : gear.py
# Description   : This module describes the gears in object oriented fashion and
#                 handles gear calculations
# =============================================================================

import math

# This class contains the parameters and functions of Base Gear
class Gear:

    # Gear Attributes
    teeth_number = None
    pressure_angle = None
    pitch_diameter = None
    clearance = None
    hole_diameter = None
    gear_type = None

    # Constructor of the Base Gear which initalises/stores parameters of Base Gear
    # kwargs: Dictionary with elements containg numbers (real and integer) and string
    def __init__(self, **kwargs):
        self.teeth_number = float(kwargs.get('teeth_number'))
        self.pressure_angle = float(kwargs.get('pressure_angle'))
        self.pitch_diameter = float(kwargs.get('pitch_diameter'))
        self.clearance = float(kwargs.get('clearance'))
        self.hole_diameter = float(kwargs.get('hole_diameter'))
        self.gear_type = kwargs.get('gear_type')
    
    # This function computes and gets the module of Base Gear
    # Returns module using pitch diameter and teeth number of gear as float
    # Raises Exception if error encountered and returns 0
    def get_module(self):
        try:
            return float(self.pitch_diameter / self.teeth_number)
        except Exception as e:
            print(f"Unexpected {e=}, {type(e)}")
            return 0
        
        
    # This function gets addendum of Base gear
    # Returns module of the gear   
    def get_addendum(self):
        return self.get_module()

# Different types of Gears
# This inherited class contains parameters and functions of Spur Gear
class InvoluteGear(Gear):

    # Constructor of the Spur Gear which initalises/stores parameters of Spur Gear
    # Inherits from base class Gear
    # kwargs: Dictionary with elements containg numbers (real and integer) and String
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    # This function gets dedendum of spur gear
    # Returns module*1.25 of the gear
    # Raises Error if error encountered and returns 0
    def get_dedendum(self):
        try:
            return self.get_module() * 1.25
        except Exception as e:
            print(f"Unexpected {e=}, {type(e)}")
            return 0
    
    # This function gets tool depth of spur gear
    # Returns module*2.25 of the gear
    # Raises Error if error encountered and returns 0
    def get_tooth_depth(self):
        try:
            return self.get_module() * 2.25 
        except Exception as e:
            print(f"Unexpected {e=}, {type(e)}")
            return 0

    # This function gets tip diameter of spur gear
    # Returns calculated tip diameter (float) of the gear
    # Raises Error if error encountered and returns 0       
    def get_tip_diameter(self):
        try:
            return (float(self.teeth_number) + 2) * self.get_module()
        except Exception as e:
            print(f"Unexpected {e=}, {type(e)}")
            return 0
    
    # This function gets root diameter of spur gear
    # Returns root diameter of the gear
    # Raises Error if error encountered and returns 0
    def get_root_diameter(self):
        try:
            return (self.teeth_number - 2.25) * self.get_module()
        except Exception as e:
            print(f"Unexpected {e=}, {type(e)}")
            return 0

    # This function gets get_centre_distance diameter of spur gear using other gear
    # other_gear: Other gears root diameter
    # Returns the calculated root diameter 
    # Raises Error if error encountered and returns 0    
    def get_centre_distance(self, other_gear):
        try:
            return (self.pitch_diameter + other_gear.pitch_diameter) / 2
        except Exception as e:
            print(f"Unexpected {e=}, {type(e)}")
            return 0
        
    # This function gets tip clearance of spur gear
    # Returns module*0.25 (float) of the gear
    # Raises Error if error encountered and returns 0    
    def get_tip_clearance(self):
        try:
            return (float(self.get_module()) * 0.25)
        except Exception as e:
            print(f"Unexpected {e=}, {type(e)}")
            return 0

    # This function gets properties previously calculated of spur gear
    # and stores in a dictionary
    # Returns nothing  
    def get_properties(self):
        properties = { \
            "addendum": self.get_addendum,
            "dedendum": self.get_dedendum,
            "tooth_depth": self.get_tooth_depth,
            "tip_diameter": self.get_tip_diameter,
            "tip_clearance":self.get_tip_diameter,
            "module": self.get_module
            }

# This inherited class contains parameters and functions of Bevel Gear
class BevelGear(Gear):

    # Constructor of the Bevel Gear which initalises/stores parameters of Bevel Gear
    # Inherits from base class Gear
    # kwargs: Dictionary with elements containg numbers (real and integer) and String
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    # This function gets refernece cone angle of bevel gear using other gear
    # other_gear: Other gears teeth number
    # Returns the calculated refernece cone angle 
    # Raises Error if error encountered and returns 0  
    def get_my_reference_cone_angle(self, other_gear):
        try:
            return (self.teeth_number / other_gear.teeth_number)
        except Exception as e:
            print(f"Unexpected {e=}, {type(e)}")
            return 0
    
    # This function gets reference cole angle of other bevel gear
    # other_gear: Other gears teeth number
    # Returns the other gears calculated reference cone angle 
    # Raises Error if error encountered and returns 0  
    def get_other_reference_cone_angle(self, other_gear):
        try:
            return (other_gear.teeth_number / self.teeth_number)
        except Exception as e:
            print(f"Unexpected {e=}, {type(e)}")
            return 0
    
    # This function gets total angle value using other gear
    # other_gear: Other gears cone angle
    # Returns the calculated total angle between gears 
    # Raises Error if error encountered and returns 0  
    def get_axis_single_total(self,other_gear):
        try:
            return self.get_my_reference_cone_angle() + other_gear.get_my_reference_cone_angle()
        except Exception as e:
            print(f"Unexpected {e=}, {type(e)}")
            return 0
        
    # This function gets addendum of gear
    # Returns the calculated addendum
    # Raises Error if error encountered and returns 0   
    def get_addendum(self):
        return self.pitch_diameter + (2 * self.get_module()* math.cos(self.get_my_reference_cone_angle))

# This inherited class contains parameters and functions of Worm Gear
class WormGear(Gear):

    # Constructor of the Worm Gear which initalises/stores parameters of Worm Gear
    # Inherits from base class Gear
    # kwargs: Dictionary with elements containg numbers (real and integer) and String
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    # This function gets lead angle of worm gear
    # Returns module*0.25 (float) of the gear
    # Raises Error if error encountered and returns 0 
    def get_lead_angle(self):
        try:
            return math.atan(self.get_module()*self.teeth_number / self.pitch_diameter)
        except Exception as e:
            print(f"Unexpected {e=}, {type(e)}")
            return 0
        
    # This function gets axial pitch of worm gear
    # Returns module*0.25 (float) of the gear
    # Raises Error if error encountered and returns 0 
    def get_axial_pitch(self):
        try:
            return math.pi * self.get_module() * self.teeth_number
        except Exception as e:
            print(f"Unexpected {e=}, {type(e)}")
            return 0

# This class contains utility function of gear     
class Gear_Utility:
    
    # This function gets teeth number of a gear
    # Returns float(pitch_diameter / module) of the gear
    # Raises Error if error encountered and returns 0 
    def get_teeth_number(module, pitch_diameter):
        try:
            return float(pitch_diameter / module)
        except Exception as e:
            print(f"Unexpected {e=}, {type(e)}")
            return 0