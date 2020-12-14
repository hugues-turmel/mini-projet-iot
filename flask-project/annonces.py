from flask import Flask, jsonify, url_for,request,abort
import sqlite3
import os


db_file_name = "annonces.db"
db_name      = "annonces"

def createAnnoncesDB():
    print("Create {} DB".format(db_name))
    if os.path.exists(db_file_name):
        os.remove(db_file_name)
    conn = sqlite3.connect(db_file_name)
    conn.execute("CREATE TABLE {table_name} (id INTEGER PRIMARY KEY AUTOINCREMENT,offreur_id INTEGER NOT NULL, titre TEXT NOT NULL, entreprise TEXT NOT NULL, categorie INTEGER NOT NULL, date_depot TEXT NOT NULL, date_limite TEXT NOT NULL, description TEXT NOT NULL, contact TEXT NOT NULL, mots_cles TEXT NOT NULL, FOREIGN KEY(categorie) REFERENCES categories(id))".format(table_name=db_name))
    conn.execute("INSERT INTO  {table_name} (titre,offreur_id,entreprise,categorie,date_depot,date_limite,description,contact,mots_cles) VALUES ('Ingénieur Qualite',1,'Renault',1,'20/11/2020','10/01/2020','CDI','hugues.turmel@orange.fr','#ingénieur')".format(table_name=db_name))
    conn.commit()
    conn.close()

def find_all_annonces():
    conn = sqlite3.connect(db_file_name)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM {table_name}".format(table_name = db_name))
    result = cursor.fetchall()
    conn.commit()
    conn.close()
    return(result)

def find_all_for_one_annonces(log_id):
    conn = sqlite3.connect(db_file_name)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM {table_name} WHERE log_id={id}".format(id = log_id, table_name = db_name))
    result = cursor.fetchall()
    conn.commit()
    conn.close()
    return(result)

def find_one_annonce(id):
    conn = sqlite3.connect(db_file_name)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM {table_name} WHERE  id = '{id}'".format(id = id, table_name = db_name))
    result = cursor.fetchone()
    conn.commit()
    conn.close()
    return(result)

def save_annonces(titre,offreur_id,entreprise,categorie,date_depot,date_limite,description,contact,mots_cles):
    conn = sqlite3.connect(db_file_name)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO {table_name} (titre,offreur_id,entreprise,categorie,date_depot,date_limite,description,contact,mots_cles) VALUES ('{titre}', '{offreur_id}', '{entreprise}', '{categorie}', '{date_depot}', '{date_limite}', '{description}', '{contact}', '{mots_cles}')".format(titre = titre,offreur_id = offreur_id,entreprise = entreprise,categorie = categorie,date_depot = date_depot,date_limite = date_limite,description = description,contact = contact,mots_cles = mots_cles, table_name = db_name))
    conn.commit()
    conn.close()

def delete_annonces(log_id):
    conn = sqlite3.connect(db_file_name)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM {table_name} WHERE id={id}".format(id = log_id, table_name = db_name))
    conn.commit()
    conn.close()

def update_annonces(log_id, login, password):
    conn = sqlite3.connect(db_file_name)
    cursor = conn.cursor()
    cursor.execute("UPDATE {table_name} SET login='{login}', password='{password}' WHERE log_id={id}".format(login = login, password = password, id = log_id, table_name = db_name))
    conn.commit()
    conn.close()

