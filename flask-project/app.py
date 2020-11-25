from flask import Flask, render_template
from flask_restx import Resource, Api, fields, reqparse
from login import find_all, find_all_for_one, save, delete, update, find_one


app = Flask(__name__)


@app.route("/", methods=["GET"])
def get():
    return(render_template("login.html"))

print(find_one("Laura367")[0][0])

if __name__ == "__main__":
    app.run(host='0.0.0.0')