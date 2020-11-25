from flask import render_template, redirect, url_for, request
from login import find_all_for_one, find_one
from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, SelectField
from wtforms.validators import DataRequired
import sys

class LoginForm(FlaskForm):
    login       =   StringField(     'Login', validators=[DataRequired()])
    password    =   StringField(  'Password', validators=[DataRequired()])