from flask import Flask, jsonify, url_for,request,abort
from flask_restx import Resource, Api, fields

app = Flask(__name__)
api = Api(app)

@api.route('/login')
class Login(Ressource):
    def get(self):
        return(jsonify())
    
    
if __name__ == '__main__':
    app.run(debug=True)