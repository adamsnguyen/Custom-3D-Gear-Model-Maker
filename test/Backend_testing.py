# =============================================================================
# File Name     : Backend_testing.py
# Description   : Unit Test of script generator for FreeCAD
# =============================================================================

import sys
sys.path.append("../app/Backend_FreeCAD")
import os
import unittest
#from app import app
from Running import main
# ---------------------------------------------------------------------------------
# This little script will look for freecad so we don't have to manually code
# in the path
for root, dir, files in os.walk(r"C:\Program Files"):
      if "FreeCADCmd.exe" in files:
         freecad = os.path.join(root, "FreeCADCmd.exe")
         break
         
if freecad:
    print(f"Found FreeCadCmd.exe at {freecad}")
    
else:
    raise OSError("Can't find FreeCADCmd.exe")
# ---------------------------------------------------------------------------------

# This class contains a function which tests the spur gear generation against a reference file
class TestspurGear(unittest.TestCase):

    # This function compares file sizes of a generated spur gear and reference spur gear
    # If they are not equal that implies it passed the test
    # Returns nothing   
    def test_spur(self):
        # Gear Attributes
        dic = {
            'num_teeth': 10,
            'pressure_angle': 20,
            'pitch_dia': 60,
            'clearance': 0.12,
            'hole_dia': 10,
            'height': 10,
            'gear_type': "spur"
        }
        # Reference File
        Reference_file = os.path.getsize(os.path.join(os.path.dirname(__file__), "..", "app", "Backend_FreeCAD", "Reference\Spur.stl"))
        
        # ID generation and storing in dictionary
        file = f"id{int(dic.get('pitch_dia'))}{dic.get('num_teeth')}{int(dic.get('hole_dia'))}{int(dic.get('height'))}{int(dic.get('pressure_angle'))}"+'b'   
        ID_name = {'ID': file}
        dic.update(ID_name)

        # Running the Backend and generating gear
        main(dic)
        Compiled_file = os.path.getsize(os.path.join(os.path.dirname(__file__), "..", "app", "Backend_FreeCAD", "Part_files\\" + file + ".stl"))
        
        # Comparing the file size
        self.assertNotAlmostEqual(Compiled_file, Reference_file)

# This class contains a function which tests the helix gear generation against a reference file
class TesthelixGear(unittest.TestCase):
    
    # This function compares file sizes of a generated helix gear and reference helix gear
    # If they are not equal that implies it passed the test
    # Returns nothing
    def test_helix(self):
        # Gear Attributes
        dic = {
            'num_teeth': 10,
            'pressure_angle': 20,
            'pitch_dia': 20,
            'clearance': 0.12,
            'hole_dia': 10,
            'angle_teeth': 20,
            'height': 10,
            'gear_type': "helix"
        }
        # Reference File
        Reference_file = os.path.getsize(os.path.join(os.path.dirname(__file__), "..", "app", "Backend_FreeCAD", "Reference\Helix.stl"))
        
        # ID generation and storing in dictionary
        file = f"id{int(dic.get('pitch_dia'))}{dic.get('num_teeth')}{int(dic.get('hole_dia'))}{int(dic.get('height'))}{int(dic.get('pressure_angle'))}"+'h'   
        ID_name = {'ID': file}
        dic.update(ID_name)
        
        # Running the Backend and generating gear
        main(dic)
        Compiled_file = os.path.getsize(os.path.join(os.path.dirname(__file__), "..", "app", "Backend_FreeCAD", "Part_files\\" + file + ".stl"))
        
        # Comparing the file size
        self.assertNotAlmostEqual(Compiled_file, Reference_file)

# This class contains a function which tests the double helix gear generation against a reference file
class TestDoublehelixGear(unittest.TestCase):
    
    # This function compares file sizes of a generated double helix gear and reference double helix gear
    # If they are not equal that implies it passed the test
    # Returns nothing
    def test_doublehelix(self):
        # Gear Attributes
        dic = {
            'num_teeth': 10,
            'pressure_angle': 20,
            'pitch_dia': 20,
            'clearance': 0.12,
            'hole_dia': 10,
            'angle_teeth': 20,
            'height': 10,
            'gear_type': "double_helix"
        }
        # Reference File
        Reference_file = os.path.getsize(os.path.join(os.path.dirname(__file__), "..", "app", "Backend_FreeCAD", "Reference\Double_Helix.stl"))

        # ID generation and storing in dictionary
        file = f"id{int(dic.get('pitch_dia'))}{dic.get('num_teeth')}{int(dic.get('hole_dia'))}{int(dic.get('height'))}{int(dic.get('pressure_angle'))}"+'d'   
        ID_name = {'ID': file}
        dic.update(ID_name)

        # Running the Backend and generating gear
        main(dic)
        Compiled_file = os.path.getsize(os.path.join(os.path.dirname(__file__), "..", "app", "Backend_FreeCAD", "Part_files\\" + file + ".stl"))
        
        # Comparing the file size
        self.assertNotAlmostEqual(Compiled_file, Reference_file)

# This class contains a function which tests the bevel gear generation against a reference file
class TestBevelGear(unittest.TestCase):
    
    # This function compares file sizes of a generated bevel gear and reference bevel gear
    # If they are not equal that implies it passed the test
    # Returns nothing
    def test_bevel(self):
        # Gear Attributes
        dic = {
            'num_teeth': 10,
            'pressure_angle': 20,
            'pitch_dia': 20,
            'clearance': 0.12,
            'hole_dia': 10,
            'angle_teeth': 20,
            'height': 10,
            'gear_type': "bevel"
        }
        # Reference File
        Reference_file = os.path.getsize(os.path.join(os.path.dirname(__file__), "..", "app", "Backend_FreeCAD", "Reference\Bevel.stl"))
        
        # ID generation and storing in dictionary
        file = f"id{int(dic.get('pitch_dia'))}{dic.get('num_teeth')}{int(dic.get('hole_dia'))}{int(dic.get('height'))}{int(dic.get('pressure_angle'))}"+'b'   
        ID_name = {'ID': file}
        dic.update(ID_name)
        
        # Running the Backend and generating gear
        main(dic)
        Compiled_file = os.path.getsize(os.path.join(os.path.dirname(__file__), "..", "app", "Backend_FreeCAD", "Part_files\\" + file + ".stl"))
        
        # Comparing the file size
        self.assertNotAlmostEqual(Compiled_file, Reference_file)

# This class contains a function which tests the worm gear generation against a reference file
class TestWormGear(unittest.TestCase):
    
    # This function compares file sizes of a generated worm gear and reference worm gear
    # If they are not equal that implies it passed the test
    # Returns nothing
    def test_worm(self):
        # Gear Attributes
        dic = {
            'num_teeth': 10,
            'pressure_angle': 20,
            'pitch_dia': 20,
            'clearance': 0.12,
            'hole_dia': 10,
            'angle_teeth': 20,
            'height': 60,
            'gear_type': "worm"
        }
        # Reference File
        Reference_file = os.path.getsize(os.path.join(os.path.dirname(__file__), "..", "app", "Backend_FreeCAD", "Reference\Worm.stl"))
        
        # ID generation and storing in dictionary
        file = f"id{int(dic.get('pitch_dia'))}{dic.get('num_teeth')}{int(dic.get('hole_dia'))}{int(dic.get('height'))}{int(dic.get('pressure_angle'))}"+'w'   
        ID_name = {'ID': file}
        dic.update(ID_name)
        
        # Running the Backend and generating gear
        main(dic)
        Compiled_file = os.path.getsize(os.path.join(os.path.dirname(__file__), "..", "app", "Backend_FreeCAD", "Part_files\\" + file + ".stl"))
        
        # Comparing the file size
        self.assertNotAlmostEqual(Compiled_file, Reference_file)

# Runs the main unittest function
if __name__ == '__main__':
    unittest.main()