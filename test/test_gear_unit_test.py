import os
import sys
sys.path.append('../app/Backend_FreeCAD')
import gear
import unittest

#This class contains unittest case for different types of gears
class test_GearFuncs(unittest.TestCase):
    
    # Involute Gear Parameters
    involute_gear =gear.InvoluteGear(
            teeth_number = 20, 
            pressure_angle = 20,
            pitch_diameter = 60,
            clearance = 0.12,
            hole_diameter = 5,
            gear_type = "Spur Gear")
    
    # Worm Gear Parameters
    worm_gear =gear.WormGear(
            teeth_number = 20, 
            pressure_angle = 20,
            pitch_diameter = 60,
            clearance = 0.12,
            hole_diameter = 5,
            gear_type = "Worm Gear")
    
    # This function checks for module of the involute gear
    # Returns nothing
    def test_involute_module(self):
        module = self.involute_gear.get_module()
        self.assertAlmostEqual(module, 3)
    
    # This function checks for addendum of the involute gear
    # Returns nothing
    def test_involute_addendum(self):
        addendum = self.involute_gear.get_addendum()
        self.assertAlmostEqual(addendum, 3)
    
    # This function checks for dedendum of the involute gear
    # Returns nothing
    def test_involute_dedendum(self):
        dedendum = self.involute_gear.get_dedendum()
        self.assertAlmostEqual(dedendum, 3.75)
    
    # This function checks for tooth depth of the involute gear
    # Returns nothing
    def test_involute_tooth_depth(self):
        tooth_depth = self.involute_gear.get_tooth_depth()
        self.assertAlmostEqual(tooth_depth, 6.75)

    # This function checks for tip diameter of the involute gear
    # Returns nothing 
    def test_involute_tip_diameter(self):
        tip_diameter = self.involute_gear.get_tip_diameter()
        self.assertAlmostEqual(tip_diameter, 66)
    
    # This function checks for tip clearance of the involute gear
    # Returns nothing
    def test_involute_tip_clearance(self):
        tip_clearance = self.involute_gear.get_tip_clearance()
        self.assertAlmostEqual(tip_clearance, 0.75)
    
    # This function checks for tip clearance of the involute gear
    # Returns nothing
    def test_involute_tip_clearance(self):
        root_diameter = self.involute_gear.get_root_diameter()
        self.assertAlmostEqual(root_diameter, 53.25)

    # This function checks for centre distance of the involute gear
    # Returns nothing 
    def test_involute_centre_distance(self):
        centre_distance = self.involute_gear.get_centre_distance(self.involute_gear)
        self.assertAlmostEqual(centre_distance, 60)

    # This function checks for lead angle of the worm gear
    # Returns nothing 
    def test_worm_lead_angle(self):
        lead_angle = self.worm_gear.get_lead_angle()
        self.assertAlmostEqual(lead_angle, 0.7853981633974483)

    # This function checks for axial pitch of the worm gear
    # Returns nothing   
    def test_axial_pitch(self):
        axial_pitch = self.worm_gear.get_axial_pitch()
        self.assertAlmostEqual(axial_pitch, 188.49555921538757)
    
    # Runs the unittest main function
    if __name__ == '__main__':
        unittest.main()