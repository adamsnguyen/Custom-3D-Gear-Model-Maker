# =============================================================================
# File Name     : routes.py
# Description   : This module handles the web application routing
# =============================================================================

import sys
from app.Backend_FreeCAD.gear import BevelGear, InvoluteGear, WormGear
sys.path.append("app/Backend_FreeCAD/")
from flask import render_template, flash, send_from_directory, abort, request, redirect, url_for
from app import app
from app import forms
from shutil import copyfile
from flask_socketio import SocketIO, emit
import subprocess
import os
import time
from decimal import Decimal
from flask_login import current_user, login_user, logout_user
from app.models import User, Gear
from flask_sqlalchemy import SQLAlchemy
import json
from datetime import datetime
from pprint import pprint


db = SQLAlchemy(app)
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

# Web App Socket IO Communication

socketio = SocketIO(app)

# This function prints loading on successful to console window on successful connection
@socketio.on('success')
def success():
    print("success")
    socketio.emit('loading')

# This function prints a message to console window when generate button is clicked
@socketio.on('generate')
def generate(message):
    print("generating models")
    generate_model(message['data'])
    socketio.emit('done')
    
socketio.run(app)
# ---------------------------------------------------------------------------------

#   Routing
# This function renders the first page on opening website
# Returns the spur gear form on first opening the page 
@app.route('/', methods=['GET', 'POST'])
def base_index():
    return index(form_type = "spur_form")
    
# This function renders the Engineering page of website
# form_type: Intakes the type of form chosen by the user (type: string)
# Returns the renderended template of the page according to calc.html
# with the form chosen, ID and gear name
@app.route('/calculate/<form_type>', methods=['GET', 'POST'])
def calculate(form_type = "spur_form"):
    form = forms.SpurFormCalc()
    gear_name = None
    my_gear = None
    other_gear = None 
    
    # Choosing and parsing Gear Form according to method
    if form_type == "spur_form":
        form = forms.SpurFormCalc(request.form)
        gear_name = "Spur Gear"
    elif form_type == "helix_form":
        form = forms.HelixFormCalc(request.form)
        gear_name = "Helix Gear"
    elif form_type == "double_helix_form":
        form = forms.DoubleHelixFormCalc(request.form)
        gear_name = "Double Helix Gear"
    elif form_type == "worm_form":
        form = forms.WormForm(request.form)
        gear_name = "Worm Gear"
    elif form_type == "bevel_form":
        form = forms.BevelFormCalc(request.form)
        gear_name = "Bevel Gear"
        
     # Form Validation
    if form.validate_on_submit():
        

        if gear_name == "Spur Gear" or gear_name == "Helix Gear" or gear_name == "Double Helix Gear":

            my_gear = InvoluteGear(teeth_number = form.num_teeth.data, \
                pressure_angle = form.pressure_angle.data,
                pitch_diameter = form.pitch_dia.data,
                clearance = form.clearance.data,
                hole_diameter = form.hole_dia.data,
                gear_type = gear_name)
            
            other_teeth = float(form.pitch_dia2.data)/my_gear.get_module()
            
            other_gear = InvoluteGear(
                teeth_number = other_teeth, 
                pressure_angle = form.pressure_angle.data,
                pitch_diameter = form.pitch_dia2.data,
                clearance = form.clearance.data,
                hole_diameter = form.hole_dia.data,
                gear_type = gear_name)
            
            pprint(vars(my_gear))
            pprint(vars(other_gear))
            
        elif gear_name == "Worm Gear":

            my_gear = WormGear(teeth_number = form.num_teeth.data, \
                pressure_angle = form.pressure_angle.data,
                pitch_diameter = form.pitch_dia.data,
                clearance = form.clearance.data,
                hole_diameter = form.hole_dia.data,
                gear_type = gear_name,
                )
            
        elif gear_name == "Bevel Gear":
    
            my_gear = BevelGear(teeth_number = form.num_teeth.data, 
                pressure_angle = form.pressure_angle.data,
                pitch_diameter = form.pitch_dia.data,
                clearance = form.clearance.data,
                hole_diameter = form.hole_dia.data,
                gear_type = gear_name,
                )
            
            other_teeth = float(form.pitch_dia2.data/my_gear.get_module())
            
            other_gear = BevelGear(
                teeth_number = other_teeth, 
                pressure_angle = form.pressure_angle.data,
                pitch_diameter = form.pitch_dia2.data,
                clearance = form.clearance.data,
                hole_diameter = form.hole_dia.data,
                gear_type = gear_name)
                    
    return render_template("calc.html", title = "Engineering Calculation", gear_form = form, my_gear = my_gear, other_gear = other_gear, gear_name = gear_name)

# This function renders the index page of website with different types of gears
# form_type: Intakes the type of form chosen by the user (type: string)
# Returns the renderended template of the page with the form chosen, ID and gear name
@app.route('/index/<form_type>', methods=['GET', 'POST'])
def index(form_type = "spur_form", login=False):
    
    ID =''
    # Checking for Gear Form
    id_flags = ['s','h','d','r','w','b']
    id_flag = None
    form = forms.SpurForm()
    gear_name = None

    # Choosing and parsing Gear Form according to method
    if form_type == "spur_form":
        form = forms.SpurForm(request.form)
        id_flag = id_flags[0]
        gear_name = "Spur Gear"
    elif form_type == "helix_form":
        form = forms.HelixForm(request.form)
        id_flag = id_flags[1]
        gear_name = "Helix Gear"
    elif form_type == "double_helix_form":
        form = forms.DoubleHelixForm(request.form)
        id_flag = id_flags[2]
        gear_name = "Double Helix Gear"
    elif form_type == "rack_form":
        form = forms.RackForm(request.form)
        id_flag = id_flags[3]
        gear_name = "Rack"
    elif form_type == "worm_form":
        form = forms.WormForm(request.form)
        id_flag = id_flags[4]
        gear_name = "Worm Gear"
    elif form_type == "bevel_form":
        form = forms.BevelForm(request.form)
        id_flag = id_flags[5]
        gear_name = "Bevel Gear"
    
    # Form Validation
    if form.validate_on_submit() and login == False:
        
        # Generating json from form for sending to FreeCAD
        json_data = {"gear_type": form_type.split("_")[0] if not form_type == "double_helix_form" else "double_helix",}
        
        for key, value in form.data.items():
            if isinstance(value, Decimal):
                value = float(value)
            json_data[key] = value
        
        # Generating unique ID
        ID = f"id{int(json_data.get('pitch_dia'))}{json_data.get('num_teeth')}{int(json_data.get('hole_dia'))}{int(json_data.get('height'))}{int(json_data.get('pressure_angle'))}"+id_flag    
        
        json_gear_id = {"ID": ID}
        json_data.update(json_gear_id)
        
        # Add to Database
        if current_user.is_authenticated:
            gear = Gear(id=ID, time_created = datetime.now(), 
                    username=current_user.username, \
                    gear_type = gear_name, height = json_data.get('height'), \
                    num_teeth = json_data.get('num_teeth'), \
                    pitch_dia = json_data.get('pitch_dia'), \
                    hole_dia = json_data.get('hole_dia'), \
                    angle_teeth = json_data.get('angle_teeth'), \
                    pressure_angle = json_data.get('pressure_angle'), \
                    clearance = json_data.get('clearance'), \
                    double_helix = json_data.get('double_helix'))
            db.session.add(gear)
            db.session.commit()
        
        # Unique name of the Generated Gear
        flash({"data": ID})

        # Running the Backend and Generating gears
        from app.Backend_FreeCAD.Running import main
        main(json_data)

    # Display User history form sql database
    result = None
    if current_user.is_authenticated:
        result = Gear.query.filter_by(username=current_user.username)
        print(result)
    
    return render_template('index.html' , title = "Home", gear_form = form, gear_id = ID, gears = result, gear_name = gear_name)

# This function gets the file from a directory and allows the user to download the .stl file generated
# ID: Intakes the ID of the file generated (type: string)
# Returns nothing
# Raises error if file not found
@app.route("/download/<ID>")
def download(ID):
    file = f"{ID}.stl"
    dirname =os.path.join(os.path.dirname(__file__), r"Backend_FreeCAD\Part_files\\") 
    try:
        return send_from_directory(dirname, file, as_attachment=True)
    except FileNotFoundError:
        print('path', dirname)
        abort(404)

# This function allows user to sign in the website when login button is clicked
# Returns a rendered template according to login.html     
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index', form_type = "spur_form"))
    
    login_form = forms.LoginForm()
    
    if login_form.validate_on_submit() :
        user = User.query.filter_by(username=login_form.username.data).first()
        if user is None or not user.check_password(login_form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=login_form.remember_me.data)
        return index(form_type = "spur_form", login = True)
    if current_user.is_authenticated:
        return index(form_type = "spur_form", login = True)
  
    return render_template('login.html', title='Sign In', login_form=login_form)

# This function allows user to register in the website when register button is clicked
# Returns a rendered template according to register.html
@app.route('/register', methods=['GET', 'POST'])
def register():
    
    if current_user.is_authenticated:

        return redirect(url_for('index', form_type = "spur_form", login = True))
    
    

    register_form = forms.RegistrationForm()
    if register_form.validate_on_submit():
        user = User(username=register_form.username.data, email=register_form.email.data)
        user.set_password(register_form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', title='Sign In', register_form=register_form)

# This function allows user to logout off the website when logout button is clicked
# Returns a rendered template according to index.html with spur form as the form
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index', form_type = "spur_form"))

# This function allows user to check the database made by the user
# Returns a rendered template according to gear_all.html with a SQL database
@app.route('/gear-database')
def show_all():
   return render_template('gear_all.html', gears = Gear.query.all() )

# This function allows user to get the design history of the user
# Returns a rendered template according to gear_all.html with a SQL database
@app.route('/design-history')
def user_history():
    result = Gear.query.filter_by(username=current_user.username)
    return render_template('gear_all.html', gears = result)


# ---------------------------------------------------------------------------------
                
# Converting .stl to .gif 
# This function generates .gif of the .stl model generated from three different angles
# IT stores these .gifs in a folder
# ID: Intake is the ID generated for the gear
# Returns nothing
def generate_model(ID):
    dirname = os.path.dirname(__file__)
    stl2gif = os.path.join(dirname, "stl_to_gif.py")
    stl = os.path.join("Backend_FreeCAD", "Part_files", f"{ID}.stl")
    gif = os.path.join("Backend_FreeCAD", "Part_files", ID)
    gif_side_1 = os.path.join("Backend_FreeCAD", "Part_files", ID+"_side_1")
    gif_side_2 = os.path.join("Backend_FreeCAD", "Part_files", ID+"_side_2")
    
    input_flag = "-i"
    output_flag = "-o"
    stl_input = os.path.join(dirname, stl)
    output = os.path.join(dirname, gif)
    output_side_1 = os.path.join(dirname, gif_side_1)
    output_side_2 = os.path.join(dirname, gif_side_2)
    side_flags_1 = '-e 90 -n 1 --mesh_color "silver" --line_color "red" --line_width 0.1 -t 0.2"'
    side_flags_2 = '-e 30 -n 1 --mesh_color "silver" --line_color "red" --line_width 0.1 -t 0.25"'
    side_flags_3 = '-e 60 -n 1 --mesh_color "silver" --line_color "red" --line_width 0.1 -t 0.25"'
    
    subprocess.run( rf'python "{stl2gif}"  "{input_flag}" "{stl_input}" "{output_flag}" "{output}" {side_flags_1}')
    subprocess.run( rf'python "{stl2gif}"  "{input_flag}" "{stl_input}" "{output_flag}"  "{output_side_1}" {side_flags_2}')
    subprocess.run( rf'python "{stl2gif}"  "{input_flag}" "{stl_input}" "{output_flag}"  "{output_side_2}" {side_flags_3}') 
    copyfile(os.path.join(dirname, f"{gif}.gif"), os.path.join(dirname, "static", "gear_output_gifs", f"{ID}.gif"))
    copyfile(os.path.join(dirname, f"{gif_side_1}.gif"), os.path.join(dirname, "static", "gear_output_gifs", f"{ID}_side_1.gif"))
    copyfile(os.path.join(dirname, f"{gif_side_2}.gif"), os.path.join(dirname, "static", "gear_output_gifs", f"{ID}_side_2.gif"))