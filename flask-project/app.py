from flask import Flask, jsonify, url_for,request,abort
from flask_restx import Resource, Api, fields
import datetime
from threading import Timer
import time
import json
from collections    import defaultdict
from databases.offreurs       import createOffreursDB,    find_all_offreurs,      find_one_offreur,       save_offreur,       delete_offreur,     update_offreur,     find_this_offreur
from databases.categories     import createCategoriesDB,  find_all_categories,    find_one_categorie,     save_categorie,     delete_categorie,   update_categorie,   find_this_categorie        
from databases.entreprises    import createEntreprisesDB, find_all_entreprises,   find_one_entreprise,    save_entreprise,    delete_categorie,   update_entreprise,  find_this_entreprise
from databases.titres         import createTitresDB,      find_all_titres,        find_one_titre,         save_titre,         delete_titre,       update_titre              
from databases.annonces       import createAnnoncesDB,    find_all_annonces,      find_one_annonce,       save_annonces,      delete_annonces,    update_annonces, find_annonce_by_enteprise, find_annonce_by_categorie      

app = Flask(__name__)
api = Api(app)

createOffreursDB()
createCategoriesDB()
createEntreprisesDB()
createTitresDB()
createAnnoncesDB()

genid_annonce = 4

modele_annonce_input=api.model('annonce_input',
                        {'titre':fields.String,
                         'entreprise':fields.String,
                         'categorie':fields.String,
                         'date_limite':fields.String,
                         'description':fields.String,
                         'contact':fields.String,
                         'mots_clés':fields.String,
                         'login':fields.String,
                         'password':fields.String})

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

    @api.doc(model = modele_offreur_output, body = modele_offreur_input) 
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
        return(jsonify(find_all_annonces()))
    
    @api.doc(model=modele_annonce_output, body=modele_annonce_input)
    def post(self):
        global genid_annonce
        off_login           = request.json['login']
        off_password        = request.json['password']
        titre_annonce       = request.json['titre']
        entreprise_annonce  = request.json['entreprise']
        categorie_annonce   = request.json['categorie']
        date_depot_annonce  = str(datetime.date.today())
        date_limite_annonce = request.json['date_limite']
        description_annonce = request.json['description']
        contact_annonce     = request.json['contact']
        mots_cles_annonce   = request.json['mots_clés']
        offreur_id_annonce  = 0
        categorie_verification_state = False

        nouvelle_annonce = {
            'titre':        titre_annonce,
            'entreprise':   entreprise_annonce,
            'categorie':    categorie_annonce,
            'date_depot':   date_depot_annonce,
            'date_limite':  date_limite_annonce,
            'description':  description_annonce,
            'contact':      contact_annonce,
            'mots_clés':    mots_cles_annonce
        }

        id_off = find_this_offreur(off_login, off_password)
        if(id_off != None):
            nouvelle_annonce['offreur_id']  = id_off
            offreur_id_annonce              = id_off
            offreur_verification_state = True
        else:
            offreur_verification_state = False

        id_cat = find_this_categorie(categorie_annonce)
        if(id_cat != None):
            categorie_verification_state = True
        else:
            categorie_verification_state = False

        id_ent = find_this_entreprise(entreprise_annonce)
        if(id_ent == None):
            save_entreprise(entreprise_annonce)

        verification_state = self.isFull(nouvelle_annonce)

        if(verification_state & offreur_verification_state & categorie_verification_state):
            nouvelle_annonce['id']      = genid_annonce
            genid_annonce               = genid_annonce + 1
            save_annonces(titre_annonce, offreur_id_annonce, id_ent, id_cat, date_depot_annonce, date_limite_annonce, description_annonce, contact_annonce, mots_cles_annonce)
            reponse                     = jsonify(nouvelle_annonce)
            reponse.status_code         = 201
            reponse.headers['location'] = url_for('annonces') + '/' + str(genid_annonce - 1)
            return(reponse)
        else:
            reponse                     = jsonify("Tout les champs ne sont pas remplis")
            reponse.status_code         = 400
            return(reponse)
    
    def isFull(self, Annonce):
        if((Annonce['titre'] != "") and (Annonce['entreprise'] != "") and (Annonce['categorie'] != "") and (Annonce['date_depot'] != "") and (Annonce['date_limite'] != "") and (Annonce['description'] != "") and (Annonce["contact"] != "")):
            return(True)
        else:
            return(False)

@api.route('/annonces/<int:anid>')
class Annonce(Resource):
    
    def get(self, anid):
        return(jsonify(find_one_annonce(anid)))
    
    @api.doc(body=modele_delete_input) 
    def delete(self, anid):
        off_login               = request.json['login']
        off_password            = request.json['password']
        authentication_state    = False
        id_off_annonce          = find_one_annonce(anid)[1]
        print(id_off_annonce)
        id_off = find_this_offreur(off_login, off_password)[0]
        print(id_off)
        if(id_off != None):
            if(id_off == id_off_annonce):
                authentication_state = True
            else:
                authentication_state = False
        else:
            authentication_state = False
        
        
        if(authentication_state == True):
            delete_annonces(anid)
            reponse                     = jsonify("Ok")
            reponse.status_code         = 200
            return(reponse)
        else:
            reponse                     = jsonify("Vous n'êtes pas autorisé à supprimer cette annonce")
            reponse.status_code         = 401
            return(reponse)


    @api.doc(model=modele_annonce_output, body=modele_mc_annonce_input)
    def put(self, anid):
        
        annonces = find_all_annonces()

        off_login               = request.json['login']
        off_password            = request.json['password']
        authentication_state    = False
        id_off_annonce          = find_one_annonce(anid)[1]
        id = annonces[anid-1][0]
        off = find_this_offreur(off_login, off_password)
        
        if(off != None):
            id_off = find_this_offreur(off_login, off_password)[0]
            if(id_off == id_off_annonce):
                authentication_state = True
            else:
                authentication_state = False
        else:
            authentication_state = False

        id_cat = find_this_categorie(request.json['categorie'])[0]
        if(id_cat != None):
            categorie_verification_state = True
        else:
            categorie_verification_state = False

        if((authentication_state == True) and (categorie_verification_state==True)):
            titre = request.json['titre']
            entreprise = request.json['entreprise']
            offreur_id = id_off
            categorie = id_cat
            date_depot = request.json['date depot']
            date_limite = request.json['date limite']
            description = request.json['description']
            contact = request.json['contact']
            mots_cles = request.json['mots clés']
            update_annonces(id,titre,offreur_id,entreprise,categorie,date_depot,date_limite,description,contact,mots_cles)
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
        
@api.route('/annonces/categories', endpoint='categories')
class Categories(Resource):
    def get(self):
        cates = find_all_categories()
        if(cates != ""):
            reponse                     = jsonify(cates)
            reponse.status_code         = 201
            return(reponse)
        else:
            reponse                     = jsonify("Aucune catégories répertoriée")
            reponse.status_code         = 404
            return(reponse)



@api.route('/annonces/<string:catg>/categorie', endpoint='categorie')
class Categorie(Resource):
    def get(self, catg):
        categorie_verification_state = False
        category = find_this_categorie(catg)
        print(category)
        if (category != None):
            categorie_verification_state = True
            catego = find_annonce_by_categorie(catg)
            print(catego)
        else:
            categorie_verification_state = False

        if(categorie_verification_state == True):
            reponse                     = jsonify(catego)
            reponse.status_code         = 201
            return(reponse)
        else:
            reponse                     = jsonify("Aucune catégorie répertoriée")
            reponse.status_code         = 404
            return(reponse)



@api.route('/annonces/entreprises', endpoint='entreprises')
class Entreprises(Resource):
    def get(self):
        enterprises = find_all_entreprises()
        if(enterprises != ""):
            reponse                     = jsonify(enterprises)
            reponse.status_code         = 201
            return(reponse)
        else:
            reponse                     = jsonify("Aucune entreprises répertoriée")
            reponse.status_code         = 404
            return(reponse)


@api.route('/annonces/<string:entre>/entreprise', endpoint='entreprise')
class Entreprise(Resource):
    def get(self, entre):
        entreprise_verification_state = False
        ent = find_this_entreprise(entre)
       

        if (ent != None):
            entreprise_verification_state = True
            entreprise = find_annonce_by_enteprise(entre)


        else:
            entreprise_verification_state = False

        if(entreprise_verification_state == True):
            reponse                     = jsonify(entreprise)
            reponse.status_code         = 201
            return(reponse)
        else:
            reponse                     = jsonify("Aucune entreprise répertoriée")
            reponse.status_code         = 404
            return(reponse)





         

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
    annonces = find_all_annonces()
    for elem in annonces:
        L.append(elem)
    # Verification is every advertisement is up to date
    for i in range(len(L)):
        # Read and store the advertisement end date
        print(L[i][6])
        date    = L[i][6].split('/')
        year    = int(date[2])
        month   = int(date[1])
        day     = int(date[0])
        # Verification
        if(year < current_year):
            delete_annonces(i+1)
            print("remove advertisement {}".format(i+1))
            print("year")
        if(year >= current_year):
            if(year == current_year):
                if(month < current_month):
                    delete_annonces(i+1)
                    print("remove advertisement {}".format(i+1))
                    print("month")
                else:
                    if(month == current_month):
                        if(day < current_day):
                            delete_annonces(i+1)
                            print("remove advertisement {}".format(i+1))
                            print("day")
    print("checkEndDate")

        
   
if __name__ == '__main__':
    checkEndDate()
    app.run(debug=True)
    
