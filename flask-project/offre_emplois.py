from flask import Flask, jsonify, url_for,request,abort
from flask_restx import Resource, Api, fields

app = Flask(__name__)
api = Api(app)

annonces = {
    1 : {'id':1, 'titre':'Stage Ingénieur R&D', 'entreprise':'Orange',  'categorie':'Ingénieur',            'date depot':'25/11/2020', 'date limite':'25/12/2020', 'description':'Stage de 6 mois', 'contact':'hugues.turmel@orange.fr', 'mots clés':'#stage#ingénieur#r&d'},
    2 : {'id':2, 'titre':'Ingénieur Qualite',   'entreprise':'Renault', 'categorie':'Ingénieur',            'date depot':'20/11/2020', 'date limite':'10/01/2020', 'description':'CDI',             'contact':'hugues.turmel@orange.fr', 'mots clés':'#cdd#ingénieur#qualite'},
    3 : {'id':3, 'titre':'DRH',                 'entreprise':'SAP',     'categorie':'Ressources Humaines',  'date depot':'10/11/2020', 'date limite':'20/12/2020', 'description':'CDI',             'contact':'hugues.turmel@orange.fr', 'mots clés':'#drh#cdi'}
}



genid_annonce = 4

modele_annonce_input=api.model('annonce_input',
                        {'titre':fields.String,
                         'entreprise':fields.String,
                         'categorie':fields.String,
                         'date depot':fields.String,
                         'date limite':fields.String,
                         'description':fields.String,
                         'contact':fields.String,
                         'mots clés':fields.String})

modele_annonce_output=api.model('annonce_output',
                        {'id':fields.Integer,
                         'titre':fields.String,
                         'entreprise':fields.String,
                         'categorie':fields.String,
                         'date depot':fields.String,
                         'date limite':fields.String,
                         'description':fields.String,
                         'contact':fields.String,
                         'mots clés':fields.String})



@api.route('/annonces')
class Annonces(Resource):
    def get(self):
        return(jsonify(annonces))
    
    @api.doc(model=modele_annonce_output, body=modele_annonce_input)
    def post(self):
        global genid_annonce
        nouvelle_annonce = {
            'titre':        request.json['titre'],
            'entreprise':   request.json['entreprise'],
            'categorie':    request.json['categorie'],
            'date depot':   request.json['date depot'],
            'date limite':  request.json['date limite'],
            'description':  request.json['description'],
            'contact':      request.json['contact'],
            'mots clés':    request.json['mots clés']
        }
        verification_state = self.isFull(nouvelle_annonce)
        if(verification_state):
            nouvelle_annonce['id']      = genid_annonce
            genid_annonce               = genid_annonce + 1
            reponse                     = jsonify(nouvelle_annonce)
            reponse.status_code         = 201
            reponse.headers['location'] = url_for('annonces') + '/' + str(genid_annonce-1)
            return(reponse)
        else:
            reponse = jsonify("Tout les champs ne sont pas remplis")
            reponse.status_code = 404
            return(reponse)
    
    def isFull(self,Annonce):
        if((Annonce['titre'] != "") and (Annonce['entreprise'] != "") and (Annonce['categorie'] != "") and (Annonce['date depot'] != "") and (Annonce['date limite'] != "") and (Annonce['description'] != "") and (Annonce["contact"] != "")):
            return(True)
        else:
            return(False)


@api.route('/annonces/<int:abid>',endpoint='annonce')
class Annonce(Resource) :
    def get(self,abid):
        return(jsonify(annonces))
    def put(self,abid):
        title=annonces[int(abid)]
        try:
            titre=request.json['titre']
            category=request.json['categorie']
            entreprise=request.json['entreprise']
        except (KeyError, TypeError, ValueError):
            response=jsonify('Champs obligatoires manquants')
            response.status_code=400
            return response
        title['nom']=titre
        try:
            title['avere']=bool(request.json['avere']=='True')
        except (KeyError, TypeError, ValueError):
            title['avere']=False
        response=jsonify(title)
        response.status_code=200
        response.headers['location'] = url_for('annonce',abid=abid)
        return response


    
if __name__ == '__main__':
    app.run(debug=True)