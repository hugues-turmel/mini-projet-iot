# Mini Projet IoT
  
Comment créer un Flask Project ? 
Dans un terminal : 
* mkdir flask-project && cd flask-project 
* python3 -m venv env (if necessary : sudo apt-get install python3-venv)
* source env/bin/activate 
  
Comment lancer le projet flask ?  
Ourvrir un terminal dnas le dossier /flask-project  
Dans ce terminal :  
* pip3 install -i requirements.txt  
* python3 app.py  
* cliquer sur le lien inscrit dans le terminal (ex : 127.0.0.1)  
  
** Détails des fonctions **  
  
* ---- **POST** ----   
Permet de poster une annonces avec les paramètres titre, entreprise, catégorie, date limite de l'annonce, description, contact, mots clés, login et mot de passe  
  
Pour cela il faut faire partie d'un des deux offreurs.  
L'offreur enregistrer est Laura367 (mdp : Polytech45).  
Vous pouvez tester Hugues98 (mdp : Polytech45) pour vérifier que l'accès est bien refuser.  
  
Un nouvel identifiant sera attribuer à la nouvelle annonce lors de sa création.  
  
* ---- **GET /annonces** ----   
Toutes les personnes peuvent accéder à toutes les annonces répertoriée (ici il n'y en a qu'une s'il n'y a pas eu de post de nouvelle annonce)  
  

* ---- **GET /annonces/categories** ----   
Toutes les personnes peuvent accéder à toutes les catégories des annonces.  
  
* ---- **GET /annonces/entreprise** ----   
Toutes les personnes peuvent accéder à toutes les entreprises des annonces.  
  

* ---- **PUT /annonces/{anid}** ----   
Les offreurs (l'autorisé est Laura367) peut modifier une annonce existante par son titre, entreprise, catégorie, date de dépôt, date limite, description, contact ou mots clés.  
L'offreur modifiera l'annonce par son identifiant.  
  

* ---- **DELETE /annonces/{anid}** ----   
Les offreurs (l'autorisé est Laura367) peut supprimer une annonce existante.  
L'offreur supprimera l'annonce par son identifiant.  
  

* ---- **GET /annonces/{catg}/categorie** ----   
Toutes les personnes peuvent faire une recherche d'une annonce par catégorie.  
  

* ---- **GET /annonces/{entre}/entreprise** ----   
Toutes les personnes peuvent faire une recherche d'une annonce par entreprise.  
Par exemple si vous mettez l'entreprise Renault alors vous aurez la première annonce.  
Si vous mettez une entreprise ne faisant partie d'aucune annonce alors vous aurez un message d'erreur : "Aucune entreprise répertoriée".  
  

* ---- **POST /offreurs** ----   
Il est possible de créer un nouvel offreur caractérisé par un login, password, une entreprise et son contact (courriel).  
A sa création l'offreur aura un identifiant d'attribuer.  
  

* ---- **GET /offreurs** ----   
Il est possible de connaître les offreurs par cette méthode GET. S'il n'y a pas eu de post de nouvel offreur alors les actuels sont Laura367 et Hugues98.  
  

* ---- **PUT /offreurs/{offid}** ----   
Il est possible de modifier par identifiant les données des offreurs: login, password, entreprise, contact.  
  
* ---- **DELETE /offreurs/{offid}** ----   
Il est possible de supprimer un offreur, par identifiant.  
  
* ---- **GET /offreurs/{offid}** ----   
Il est possible de chercher un offreur par identifiant.  
  
* ---- **checkEndDate** ----   
Cette fonction permet de supprimer les annonces dont la date limite est dépassée. Cette fonction est appelée à interval régulier.  
  
Projet réalisé par Laura Valier-Brasier et Hugues Turmel  
