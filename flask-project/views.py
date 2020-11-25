from app import app, db
from flask import render_template, redirect, url_for, request
from login import find_all_for_onen, find_one
from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, SelectField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    login       =   StringField(     'Login', validators=[DataRequired()])
    password    =   StringField(  'Password', validators=[DataRequired()])

@app.route("/login/", methods=("POST"))
def login():
    f = LoginForm()
    if f.validate_on_submit():
        login       = str(f.login.data)
        password    = str(f.password.data)
        user = find_one(login)
        if(password == user[0][0]):
            return(render_template(
                "home.html"
            ))
        return render_template(
            "login.html",
            form=f
        )