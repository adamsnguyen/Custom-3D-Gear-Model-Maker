from flask import current_app
import pandas as pd
import os

#   Gear data from user is fetched and stored in database
def add_gear(gear_json: dict, ID: str):

    all_gears = current_app.config.get("all_gears", [])
    gear_data = {
        "ID": ID,
        "Gear Type": gear_json.get("gear_type"),
        "Pitch Diameter": gear_json.get("pitch_dia"),
        "Hole Diameter": gear_json.get("hole_dia"),
        "Number of Teeth": gear_json.get("num_teeth"),
        "Angle of Teeth": gear_json.get("angle_teeth"),
    }
    all_gears.append(gear_data)
    current_app.config["all_gears"] = all_gears
    get_dump()

#   Generating the table for data input from user
def get_gear_html():

    all_gears = current_app.config.get("all_gears", [])

    html_temp = "<table style=\"width:100%;text-align:center;background-color:white;\">"
    for idx, gear in enumerate(all_gears):

        if idx == 0:
            html_temp += "<tr style=\"background-color:white;color:black;\">"
            for key in gear.keys():
                html_temp += "<th>{}</th>".format(key)
            html_temp += "</tr>"
        html_temp += "<tr style=\"background-color:white;color:black;\">>"
        for value in gear.values():
            html_temp += "<td>{}</td>".format(value)
        html_temp += "</tr>"
    html_temp += "</table>"
    return html_temp            

#   Generating a .csv file and saving in root
def get_dump():
    all_gears = current_app.config.get("all_gears", [])
    if all_gears:
        df = pd.DataFrame(all_gears)
        path = os.path.join(os.path.dirname(__file__), "all_gears.csv")
        df.to_csv(path, index = False)