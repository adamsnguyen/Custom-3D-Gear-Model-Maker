# =============================================================================
# File Name     : forms.py
# Description   : This module contains forms of the web application
# =============================================================================

from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SubmitField, IntegerField, SelectField, PasswordField
from wtforms import validators
from wtforms.fields.simple import BooleanField
from wtforms.validators import DataRequired, NumberRange, ValidationError, EqualTo, Email
from app.models import User
import decimal

# This class contains erros, parameters and validation of a Base Gear Form
class GearForm(FlaskForm):
    name = None

    # Attribute Error
    pitch_dia_error = "Invalid Input. Input can only be between 5 and 500"
    teeth_num_error = "Invalid Input. Input can only be between 2 and 100"
    hole_dia_error = "Invalid Input. Input can only be between 1 and 450"
    height_error = "Invalid Input. Input can only be between 2 and 500"
    pressure_ang_error = "Invalid Input. Input can only be between 0 and 30"
    angle_teeth_error = "Invalid Input. Input can only be between 0 and 50"
    reverse_pitch_error = "Invalid Input. Can only be True or False"

    # Defining range and type of Gear Attributes
    pitch_dia = DecimalField('Pitch Diameter [mm]', validators=[NumberRange(min=5, max=500, message=pitch_dia_error), DataRequired()]  , default=60)
    num_teeth = IntegerField('Number of Teeth', validators=[NumberRange(min=2, max=100, message=teeth_num_error), DataRequired()], default=20)
    hole_dia = DecimalField('Hole Diameter [mm]', validators=[NumberRange(min=1, max=450, message=hole_dia_error)], default=5)
    height = DecimalField('Gear Height/Thickness [mm]', validators=[NumberRange(min=2, max=500, message=height_error), DataRequired()], default=10)
    pressure_angle = IntegerField('Pressure Angle [degrees]', validators=[NumberRange(min=0, max=30, message=pressure_ang_error), DataRequired()], default=20)
    clearance = DecimalField("Clearance", validators = [DataRequired()], default=0.12)

    # This function performs validation of pitch diameter
    # form: Intake is form data
    # Raises a Validation Error when hole diameter is greater than pitch diameter
    def validate_pitch_dia(form, field):

        hole_dia = float(form.data.get("hole_dia"))
        pitch_dia = float(form.data.get("pitch_dia"))
        if hole_dia >= pitch_dia * 0.8:
            raise ValidationError("Invalid Pitch Diameter")

    # This function performs validation of clearance
    # form: Intake is form data
    # Raises a Validation Error when clearance is greater than 0.25*pitch diameter
    def validate_clearance(form, field):
        clearance = float(form.data.get("clearance"))
        pitch_dia = float(form.data.get("pitch_dia", 1))
        if clearance > (0.250 * pitch_dia):
            raise ValidationError("Invalid Clearance. It should 25% of Pitch Diameter") 

# This inherited class contains erros, parameters and validation specific to Spur Gear Form
class SpurForm(GearForm):
    name = "Spur Gear"

    # Defining range and type of Gear Attributes and Submit button
    GearType = StringField(default = "spur_gear")
    submit = SubmitField('Generate')

# This class contains erros, parameters and validation specific to Angle Gear Form
class AngleForm(GearForm):
    name = "Angle Gear"

    # Attribute Error
    angle_teeth_error = "Invalid Input. Input can only be between 0 and 45"

    # Defining range and type of Angle Gear Attributes
    GearType = StringField(default="angle_gear")    
    angle_teeth = IntegerField('Angle Teeth [degrees]', validators=[NumberRange(min=0, max=45, message=angle_teeth_error), DataRequired()], default=20)

# This inherited class contains erros, parameters and validation specific to Helix Gear Form
class HelixForm(AngleForm):
    name = "Helix Gear"

    # Defining type of Helix Gear Attribute and Submit button
    GearType = StringField(default="helix_gear")    
    submit = SubmitField('Generate')  

    # This function performs validation of angle of teeth
    # form: Intake is form data
    # Raises a Validation Error when angle teeth is not between 5 and 45 degrees
    def validate_angle_teeth(form, field):
        angle_teeth = form.data.get("angle_teeth")
        if not isinstance(angle_teeth, int):
            angle_teeth = int(angle_teeth)
        
        if not (5 <= angle_teeth <= 45):
            raise ValidationError("Invalid Teeth angle. It should be between 5 to 45") 


# This inherited class contains erros, parameters and validation specific to Double Helix Form
class DoubleHelixForm(AngleForm):
    name = "Double Helix Gear"

    # Definingtype of Double Helix Gear Attributes and Submit button
    GearType = StringField(default = "double_helix_gear")
    submit = SubmitField('Generate')

    # This function performs validation of angle of teeth
    # form: Intake is form data
    # Raises a Validation Error when angle teeth is not between 20 and 45 degrees
    def validate_angle_teeth(form, field):
        angle_teeth = form.data.get("angle_teeth")
        if not isinstance(angle_teeth, int):
            angle_teeth = int(angle_teeth)
        
        if not (20 <= angle_teeth <= 45):
            raise ValidationError("Invalid Teeth angle. It should be between 20 to 45")

# This inherited class contains erros, parameters and validation specific to Bevel Gear Form
class BevelForm(AngleForm):
    name = "Bevel Gear"

    # Attribute Error
    backlash_error = "Invalid Input. Input can only be between 0 and 30"
    reset_origin_error = "Invalid Input. Input can only be True or False"
    pitch_angle_error = "Invalid Input. Input can only be between 5 and 50"

    # Defining range and type of Bevel Gear Attributes and Submit button
    backlash = DecimalField('Backlash [mm]', validators=[NumberRange(min=0, max=30, message=backlash_error)], default=0)
    reset_origin = BooleanField('Reset Origin', validators=[], default=False)
    pitch_angle = IntegerField('Pitch Angle [degrees]',  validators=[NumberRange(min=5, max=50, message=pitch_angle_error), DataRequired()], default=45)
    submit = SubmitField('Generate')

# This inherited class contains erros, parameters and validation specific to Worm Gear Form
class WormForm(GearForm):
    name = "Worm Gear"

    # Attribute Error
    height_error = "Invalid Input. Input can only be between 1 and 500"

    # Defining range and type of Worm Gear Attributes and Submit button
    height = DecimalField('Gear Height/Thickness [mm]', validators=[NumberRange(min=1, max=500, message=height_error), DataRequired()], default=50)
    reverse_pitch = BooleanField('Reverse Pitch', validators=[], default=False)
    submit = SubmitField('Generate')

    # This function performs validation of worm gear height
    # form: Intake is form data
    # Raises a Validation Error when angle teeth is not between 5 and 45 degrees
    def validate_height(form, field):
        height = form.data.get("height")
        pitch = form.data.get("pitch_dia")
        teeth = form.data.get("num_teeth")
        if height < (decimal.Decimal(4.5)*pitch*decimal.Decimal(3.14)/teeth):
            raise ValidationError("Invalid Height and should be greater than 4.5*pitch diameter*number of teeth*pi")   

# This class contains erros, parameters and validation specific to Rack Gear Form
class RackForm(AngleForm):
    name = "Rack Gear"

    # Attribute Error
    add_ending_error = "Invalid Input. Input can only be True or False"
    simp_error = "Invalid Input. Input can only be True or False"
    double_helix_error = "Invalid Input. Input can only be True or False"
    thickness_error = "Invalid Input. Input can only be between 0 and 30"
    head_error = "Invalid Input. Input can only be between 0 and 30"

    # Defining range and type of Rack Gear Attributes and Submit button
    GearType = StringField(default = "rack_gear")
    add_ending = BooleanField('Add Ending', validators=[], default =False)
    simp = BooleanField('Simp', validators=[], default=False)
    double_helix = BooleanField('Double Helix', validators=[], default=False)
    thickness = DecimalField('Thickness [mm]', validators=[NumberRange(min=0, max=30, message=thickness_error)], default=10)
    head = DecimalField('Head [mm]', validators=[NumberRange(min=0, max=30, message=head_error)], default=10)
    submit = SubmitField('Generate')

    # This function performs validation of height
    # form: Intake is form data
    # Raises a Validation Error when height is not between 5 and 100
    def validate_height(form, field):
        height = float(form.data.get("height"))
        if not (5 <= height <= 100):
            raise ValidationError("Invalid thickness. It should be between 5 to 100")

# This class defines type of login details required and Submit button
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')
    
# This class defines type of login detials on sign-up required and Submit button
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    # This function performs validation of username
    # username: Intake is username defined by user
    # Raises a Validation Error when username is already taken
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    # This function performs validation of email
    # username: Intake is email defined by user
    # Raises a Validation Error when email address is already used
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')
        
# This inherited class contains erros, parameters and validation specific to Bevel Gear Calculation
class BevelFormCalc(BevelForm):
    # Error
    pitch_dia_error = "Invalid Input. Input can only be between 0 and 500"

    # Defining range and type of Bevel Gear Attributes and Submit button
    submit = None
    pitch_dia2 = DecimalField('Pitch Diameter of Mating Gear [mm]', validators=[NumberRange(min=0, max=500, message=pitch_dia_error), DataRequired()]  , default=60)
    submit2 = SubmitField('Calculate')

# This inherited class contains erros, parameters and validation specific to Spur Gear Calculation
class SpurFormCalc(SpurForm):
    # Error
    pitch_dia_error = "Oops1"

    # Defining range and type of Bevel Gear Attributes and Submit button
    pitch_dia2 = DecimalField('Pitch Diameter of Mating Gear [mm]', validators=[NumberRange(min=0, max=500, message=pitch_dia_error), DataRequired()]  , default=60)
    submit = None
    submit2 = SubmitField('Calculate')

# This inherited class contains erros, parameters and validation specific to Helix Gear Form
class HelixFormCalc(HelixForm):
    # Error
    pitch_dia_error = "Oops1"

    # Defining range and type of Bevel Gear Attributes and Submit button
    submit = None
    pitch_dia2 = DecimalField('Pitch Diameter of Mating Gear [mm]', validators=[NumberRange(min=0, max=500, message=pitch_dia_error), DataRequired()]  , default=60)
    submit2 = SubmitField('Calculate')

# This inherited class contains erros, parameters and validation specific to Double Helix Form
class DoubleHelixFormCalc(DoubleHelixForm):
    # Error
    pitch_dia_error = "Oops1"

    # Defining range and type of Bevel Gear Attributes and Submit button
    submit = None
    pitch_dia2 = DecimalField('Pitch Diameter of Mating Gear [mm]', validators=[NumberRange(min=0, max=500, message=pitch_dia_error), DataRequired()]  , default=60)
    submit2 = SubmitField('Calculate')