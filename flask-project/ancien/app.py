from flask import Flask, render_template
from login import find_all, find_all_for_one, save, delete, update, find_one, createDB
from views import LoginForm
import sys


app = Flask(__name__)

createDB("login")

@app.route("/", methods=["GET"])
def get():
    return(render_template("login.html"))

@app.route("/login/", methods=("GET","POST"))
def login():
    print("Login")
    f = LoginForm()
    if f.validate_on_submit():
        login       = str(f.login.data)
        password    = str(f.password.data)
        print(login)
        print(password)
        user = find_one(login)
        if(password == user[0][0]):
            
            return(render_template(
                "home.html"
            ))
        return render_template(
            "login.html",
            form=f
        )


if __name__ == "__main__":
    app.run(host='0.0.0.0')