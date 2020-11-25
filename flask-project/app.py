from flask import Flask, render_template
from flask_restx import Resource, Api, fields, reqparse
from login import find_all, find_all_for_one, save, delete, update


app = Flask(__name__)


@app.route("/", methods=["GET"])
def get():
    return(render_template("login.html"))

print(find_all())
print(find_all_for_one(1))
save("Hugues98","PoPO1234")
print(find_all())
delete(2)
print(find_all())
update(1,"Laura367","Polytech49")
print(find_all())

if __name__ == "__main__":
    app.run(host='0.0.0.0')