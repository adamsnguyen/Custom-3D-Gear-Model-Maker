# =============================================================================
# File Name     : Running.py
# Description   : This script validates user inputs before further processed
# =============================================================================

import sys, json
import subprocess
import os, decimal
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
# This function performs check of pitch diameter
# my_kwargs:   Dictionary with elements containg numbers (real and integer) and boolean value
# Raises a Value Error when hole diameter is greater than pitch diameter
def check_pitch_dia(**my_kwargs):
    hole_dia = float(my_kwargs.get("hole_dia"))
    pitch_dia = float(my_kwargs.get("pitch_dia"))
    if hole_dia >= pitch_dia * 0.8:
        raise ValueError("Invalid Pitch Diameter")

# This function performs check of clearance
# my_kwargs:   Dictionary with elements containg numbers (real and integer) and boolean value
# Raises a Value Error when clearance is greater than 0.25*pitch diameter
def check_clearance(**my_kwargs):
    clearance = float(my_kwargs.get("clearance"))
    pitch_dia = float(my_kwargs.get("pitch_dia", 1))
    if clearance > (0.250 * pitch_dia):
        raise ValueError("Invalid Clearance. It should 25% of Pitch Diameter")

# This function performs check of angle of teeth
# my_kwargs:   Dictionary with elements containg numbers (real and integer) and boolean value
# Raises a Value Error when angle teeth is not between 5 and 45 degrees
def check_angle_teeth(**my_kwargs):
    angle_teeth = my_kwargs.get("angle_teeth")
    if not isinstance(angle_teeth, int):
        angle_teeth = int(angle_teeth)
    if not (5 <= angle_teeth <= 45):
        raise ValueError("Invalid Teeth angle. It should be between 5 to 45") 

# This function performs a check of height
# my_kwargs:   Dictionary with elements containg numbers (real and integer) and boolean value
# Raises a Value Error when height is not between 5 and 100
def check_height(**my_kwargs):
    height = float(my_kwargs.get("height"))
    if not (5 <= height <= 100):
        raise ValueError("Invalid thickness. It should be between 5 to 100")

# This function performs check of number of teeth
# my_kwargs:   Dictionary with elements containg numbers (real and integer) and boolean value
# Raises a Value Error when angle teeth is not between 5 and 45 degrees
def check_num_teeth(**my_kwargs):
    num_teeth = my_kwargs.get("num_teeth")
    if not isinstance(num_teeth, int):
        num_teeth = int(num_teeth)
    if not (2 <= num_teeth <= 100):
        raise ValueError("Invalid Number of Teeth. It should be between 2 to 100")

# This function performs check of worm gear height
# my_kwargs:   Dictionary with elements containg numbers (real and integer) and boolean value
# Raises a Value Error when angle teeth is not between 5 and 45 degrees
def check_wormheight(**my_kwargs):
    height = my_kwargs.get("height")
    if height < decimal.Decimal(4.5)*decimal.Decimal(my_kwargs.get("pitch_dia"))*decimal.Decimal(3.14)/decimal.Decimal(my_kwargs.get("num_teeth")):
        raise ValueError("Invalid Height")

# This function selects Gear Types and calling their respective Gear Generation method
# Returns nothing
# Raises ValueError when Gear type is not defined
def main(my_kwargs):

    # Json values are loaded and gear type is chosen
    gear_type = my_kwargs.get("gear_type")

    # Gear generation method is selected according to method chosen by user
    if not gear_type:
        raise ValueError(f"Gear Type not defined. {my_kwargs}")
    check_num_teeth(**my_kwargs)
    check_pitch_dia(**my_kwargs)
    check_clearance(**my_kwargs)
    check_height(**my_kwargs)
    if gear_type == "helix": 
        check_angle_teeth(**my_kwargs)
    elif gear_type == "double_helix":
        check_angle_teeth(**my_kwargs)
    elif gear_type == "bevel":
        check_angle_teeth(**my_kwargs)
    elif gear_type == "worm":
        check_wormheight(**my_kwargs)

    sys.path.append(os.path.dirname(__file__))
    main_python_file = os.path.join(os.path.dirname(__file__), "Main.py")
    subprocess.run(rf'"{freecad}" "{main_python_file}"', input=json.dumps(my_kwargs).encode("utf-8") )