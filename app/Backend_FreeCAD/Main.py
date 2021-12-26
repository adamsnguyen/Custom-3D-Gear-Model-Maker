# =============================================================================
# File Name     : Main.py
# Description   : This script prepares user data inputs before they are processed
# =============================================================================

import os
import sys
sys.path.append(os.path.dirname(__file__))
import Gear_types
import json

# This function selects Gear Types and calling their respective Gear Generation method
# Returns nothing
# Raises ValueError when Gear type is not defined
def main():

    # Json values are loaded and gear type is chosen
    inp = sys.stdin.read()
    my_kwargs = json.loads(inp)
    gear_type = my_kwargs.get("gear_type")

    # Gear generation method is selected according to method chosen by user
    if not gear_type:
        raise ValueError(f"Gear Type not defined. {my_kwargs}")
    elif gear_type == "spur":
        Gear_types.Gear_involute(**my_kwargs)
    elif gear_type == "helix": 
        Gear_types.Gear_angle(**my_kwargs)
    elif gear_type == "double_helix":
        Gear_types.Gear_double_helix(**my_kwargs)
    elif gear_type == "bevel":
        Gear_types.Gear_bevel(**my_kwargs)
    elif gear_type == "worm":
        Gear_types.Gear_worm(**my_kwargs)
    elif gear_type == "rack":
        Gear_types.Gear_rack(**my_kwargs)  

# This line runs the main function
main()