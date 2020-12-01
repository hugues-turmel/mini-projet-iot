from flask import Flask, jsonify, url_for,request,abort
from flask_restx import Resource, Api, fields
import datetime
from threading import Timer
import time
import json
from collections    import defaultdict
from offreurs       import createOffreursDB,    find_all_offreurs,      find_one_offreur,       save_offreur,       delete_offreur,     update_offreur
from categories     import createCategoriesDB,  find_all_categories,    find_one_categorie,     save_categorie,     delete_categorie,   update_categorie
from entreprises    import createEntreprisesDB, find_all_entreprises,   find_one_entreprise,    save_entreprise,    delete_categorie,   update_entreprise

app = Flask(__name__)
api = Api(app)

createOffreursDB()
createCategoriesDB()
createEntreprisesDB()


annonces = {
    1 : {'id':1, 'titre':'Stage Ingénieur R&D', 'entreprise':'Orange',  'categorie':'Ingénieur',            'date depot':'28/11/2020', 'date limite':'28/11/2020', 'description':'Stage de 6 mois', 'contact':'hugues.turmel@orange.fr', 'mots clés':'#stage#ingénieur#r&d'},
    2 : {'id':2, 'titre':'Ingénieur Qualite',   'entreprise':'Renault', 'categorie':'Ingénieur',            'date depot':'20/11/2020', 'date limite':'10/01/2021', 'description':'CDI',             'contact':'hugues.turmel@orange.fr', 'mots clés':'#cdd#ingénieur#qualite'},
    3 : {'id':1, 'titre':'DRH',                 'entreprise':'SAP',     'categorie':'Ressources Humaines',  'date depot':'10/11/2020', 'date limite':'20/12/2020', 'description':'CDI',             'contact':'hugues.turmel@orange.fr', 'mots clés':'#drh#cdi'}
}

offreurs = {
    1 : {'id':1, 'login':'Laura367', 'password':'Polytech45'},
    2 : {'id':2, 'login':'Hugues98', 'password':'Polytech45'}
}

demandeurs = {
    1 : {'id':1, 'login':'Laura367', 'password':'Polytech45'},
    2 : {'id':2, 'login':'Hugues98', 'password':'Polytech45'}
}

genid_annonce = 4

modele_annonce_input=api.model('annonce_input',
                        {'titre':fields.String,
                         'entreprise':fields.String,
                         'categorie':fields.String,
                         'date limite':fields.String,
                         'description':fields.String,
                         'contact':fields.String,
                         'mots clés':fields.String})

modele_delete_input=api.model('delete_input',
                        {'login':fields.String,
                         'password':fields.String})

modele_mc_annonce_input=api.model('annonce_input_mc',
                        {'login':fields.String,
                         'password':fields.String,
                         'titre':fields.String,
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

modele_offreur_output=api.model('offreur_output',
                        {'id':fields.Integer,
                         'login':fields.String,
                         'password':fields.String,
                         'entreprise':fields.String,
                         'contact':fields.String})

modele_offreur_input=api.model('offreur_input',
                        {'login':fields.String,
                         'password':fields.String,
                         'entreprise':fields.String,
                         'contact':fields.String})

@api.route('/offreurs')
class Offreurs(Resource):
    
    def get(self):
        Liste_Offreurs = find_all_offreurs()
        if(Liste_Offreurs != ""):
            reponse                     = jsonify(Liste_Offreurs)
            reponse.status_code         = 201
            return(reponse)
        else:
            reponse                     = jsonify("Erreur lors de la lecture de la table Offreurs")
            reponse.status_code         = 404
            return(reponse)
    
    @api.doc(model=modele_offreur_output, body=modele_offreur_input)
    def post(self):

        entreprise  = request.json['entreprise']
        contact     = request.json['contact']
        login       = request.json['login']
        password    = request.json['password']

        verification_state = self.isFull(login, password, entreprise, contact)

        if(verification_state):
            save_offreur(login, password, entreprise, contact)
            reponse                     = jsonify("ok")
            reponse.status_code         = 201
            return(reponse)
        else:
            reponse                     = jsonify("Tout les champs ne sont pas remplis")
            reponse.status_code         = 400
            return(reponse)
    
    def isFull(self, login, password, entreprise, contact):
        if((entreprise != "") and (contact != "") and (login != "") and (password != "")):
            return(True)
        else:
            return(False)

@api.route('/offreurs/<int:offid>')
class Offreur(Resource):

    def get(self, offid):
        offreur = find_one_offreur(offid)
        if(offreur != ""):
            reponse                     = jsonify(offreur)
            reponse.status_code         = 201
            return(reponse)
        else:
            reponse                     = jsonify("Aucun offreur trouvé")
            reponse.status_code         = 404
            return(reponse)

    @api.doc(model = modele_offreur_output, body = modele_mc_annonce_input) 
    def put(self,offid):
        offreur     = find_one_offreur(offid)
        login       = request.json['login']
        password    = request.json['password']
        entreprise  = request.json['entreprise']
        contact     = request.json['contact']
        if((offreur[0][1] == login) and (offreur[0][2] == password)):
            update_offreur(offid, login, password, entreprise, contact)
            reponse                     = jsonify("ok")
            reponse.status_code         = 201

            return(reponse)
        else:
            reponse                     = jsonify("Vous n'êtes pas autorisé à modifier ce compte")
            reponse.status_code         = 401
            return(reponse)

    @api.doc(body=modele_delete_input) 
    def delete(self, offid):
        offreur     = find_one_offreur(offid)
        login       = request.json['login']
        password    = request.json['password']
        if((offreur[0][1] == login) and (offreur[0][2] == password)):
            delete_offreur(offid)
            reponse                     = jsonify("ok")
            reponse.status_code         = 201
            return(reponse)
        else:
            reponse                     = jsonify("Vous n'êtes pas autorisé à supprimer ce compte")
            reponse.status_code         = 401
            return(reponse)

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
            'date depot':   str(datetime.date.today()),
            'date limite':  request.json['date limite'],
            'description':  request.json['description'],
            'contact':      request.json['contact'],
            'mots clés':    request.json['mots clés']
        }
        
        verification_state = self.isFull(nouvelle_annonce)

        if(verification_state):
            nouvelle_annonce['id']      = genid_annonce
            annonces.update({genid_annonce : nouvelle_annonce})
            genid_annonce               = genid_annonce + 1
            reponse                     = jsonify(nouvelle_annonce)
            reponse.status_code         = 201
            reponse.headers['location'] = url_for('annonces') + '/' + str(genid_annonce - 1)
            return(reponse)
        else:
            reponse                     = jsonify("Tout les champs ne sont pas remplis")
            reponse.status_code         = 400
            return(reponse)
    
    def isFull(self, Annonce):
        if((Annonce['titre'] != "") and (Annonce['entreprise'] != "") and (Annonce['categorie'] != "") and (Annonce['date depot'] != "") and (Annonce['date limite'] != "") and (Annonce['description'] != "") and (Annonce["contact"] != "")):
            return(True)
        else:
            return(False)

@api.route('/annonces/<int:anid>')
class Annonce(Resource):
    
    def get(self, anid):
        return(jsonify({ 'annonce':annonces[int(anid)]}))
    
    @api.doc(body=modele_delete_input) 
    def delete(self, anid):

        authentication_state = False

        user = {
            'login':        request.json['login'],
            'password':     request.json['password'],
        }

        id = annonces[anid]['id']
        for i in range(1,len(offreurs) + 1):
            if(offreurs[i].get('id')  == id):
                if(offreurs[i].get('login') == user.get('login')):
                    if(offreurs[i].get('password') == user.get('password')):
                        authentication_state = True
                        break
        
        if(authentication_state == True):
            annonces.pop(i)
            reponse                     = jsonify("Ok")
            reponse.status_code         = 200
            return(reponse)
        else:
            reponse                     = jsonify("Vous n'êtes pas autorisé à supprimer cette annonce")
            reponse.status_code         = 401
            return(reponse)


    @api.doc(model=modele_annonce_output, body=modele_mc_annonce_input)
    def put(self, anid):
        
        authentication_state = False

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

        user = {
            'login':        request.json['login'],
            'password':     request.json['password'],
        }
        
        id = annonces[anid]['id']
        for i in range(1,len(offreurs) + 1):
            if(offreurs[i].get('id')  == id):
                if(offreurs[i].get('login') == user.get('login')):
                    if(offreurs[i].get('password') == user.get('password')):
                        authentication_state = True
                        break
        
        verification_state = self.isFull(nouvelle_annonce)

        if((verification_state == True) and (authentication_state == True)):
            annonces[int(anid)]['titre']        = nouvelle_annonce.get('titre')
            annonces[int(anid)]['entreprise']   = nouvelle_annonce.get('entreprise')
            annonces[int(anid)]['categorie']    = nouvelle_annonce.get('categorie')
            annonces[int(anid)]['date depot']   = nouvelle_annonce.get('date depot')
            annonces[int(anid)]['date limite']  = nouvelle_annonce.get('date limite')
            annonces[int(anid)]['description']  = nouvelle_annonce.get('description')
            annonces[int(anid)]['contact']      = nouvelle_annonce.get('contact')
            annonces[int(anid)]['mots clés']    = nouvelle_annonce.get('mots clés')
            reponse                     = jsonify("Ok")
            reponse.status_code         = 200
            reponse.headers['location'] = url_for('annonces') + '/' + str(genid_annonce - 1)
            return(reponse)
        else:
            reponse                     = jsonify("Vous n'êtes pas autorisé à modifier cette annonce")
            reponse.status_code         = 401
            return(reponse)

    def isFull(self, Annonce):
        if((Annonce['titre'] != "") and (Annonce['entreprise'] != "") and (Annonce['categorie'] != "") and (Annonce['date depot'] != "") and (Annonce['date limite'] != "") and (Annonce['description'] != "") and (Annonce["contact"] != "")):
            return(True)
        else:
            return(False)
        

def  checkEndDate():
    """ This function allows to see if all advertisements still relevant """
    t = Timer(10.0, checkEndDate)
    t.start()
    # Read and store of the current day
    current_date    = str(datetime.date.today()).split('-')
    current_year    = int(current_date[0])
    current_month   = int(current_date[1])
    current_day     = int(current_date[2])
    # Store the "annonces" indexes in L
    L = []
    for elem in annonces:
        L.append(elem)
    # Verification is every advertisement is up to date
    for i in L:
        # Read and store the advertisement end date
        date    = annonces[i]['date limite'].split('/')
        year    = int(date[2])
        month   = int(date[1])
        day     = int(date[0])
        # Verification
        if(year < current_year):
            annonces.pop(i)
            print("remove advertisement {}".format(i))
        if(year >= current_year):
            if(year == current_year):
                if(month < current_month):
                    annonces.pop(i)
                    print("remove advertisement {}".format(i))
                else:
                    if(month == current_month):
                        if(day < current_day):
                            annonces.pop(i)
                            print("remove advertisement {}".format(i))
    print("checkEndDate")

        
   
if __name__ == '__main__':
    checkEndDate()
    app.run(debug=True)
    