# =============================================================================
# File Name     : models.py
# Description   : This module describes the database model
# =============================================================================

from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

# This class contains the parameters and functions for setting user account
# UserMixin:    Default method for user
# db.Model:     Variable of SQLAlchemy
# Returns nothing
class User(UserMixin, db.Model):

    # User Attributes
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    # This function converts password to a hash
    # password: Password from the user (type: String)
    # Returns nothing
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # This function checks a password against a hashed password value
    # password: Password from the user (type: String)
    # Returns True if the password is matched else False
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # This function formats the username as a string
    # Returns username as String
    def __repr__(self):
        return '<User {}>'.format(self.username)

# This function loads the user details from SQL
# id:   ID of the user
# Returns an id from the SQL
@login.user_loader
def load_user(id):
    return User.query.get(int(id))

# This class contains the gear parameters stored in SQL database
# db.Model: Variable of SQLAlchemy
# Returns nothing
class Gear(db.Model):
    id = db.Column(db.String(16))
    username = db.Column(db.String(16))
    time_created = db.Column(db.DateTime, primary_key=True)
    gear_type = db.Column(db.String(16))
    height = db.Column(db.Float)
    num_teeth = db.Column(db.Integer)
    pitch_dia = db.Column(db.Float)
    hole_dia = db.Column(db.Float)
    angle_teeth = db.Column(db.Float)
    pressure_angle = db.Column(db.Float)
    clearance = db.Column(db.Float)
    double_helix = db.Column(db.Boolean)