from flask import Flask, jsonify, url_for,request,abort
import sqlite3
import os

db_file_name = "entreprises.db"
db_name      = "entreprises"

def createEntreprisesDB():
    table_name = db_name
    print("Create {} DB".format(table_name))
    if os.path.exists(db_file_name):
        os.remove(db_file_name)
    conn = sqlite3.connect(db_file_name)
    conn.execute("CREATE TABLE {table_name} (id INTEGER PRIMARY KEY AUTOINCREMENT, nom TEXT NOT NULL)".format(table_name=table_name))
    conn.execute("INSERT INTO  {table_name} (nom) VALUES ('SAP')".format(table_name=table_name))
    conn.execute("INSERT INTO  {table_name} (nom) VALUES ('Inteva Porducts')".format(table_name=table_name))
    conn.execute("INSERT INTO  {table_name} (nom) VALUES ('MSL Circuits')".format(table_name=table_name))  
    conn.commit()
    conn.close()

def find_all_entreprises():
    conn = sqlite3.connect(db_file_name)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM {table_name}".format(table_name = db_name))
    result = cursor.fetchall()
    conn.commit()
    conn.close()
    return(result)


def find_one_entreprise(id):
    conn = sqlite3.connect(db_file_name)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM {table_name} WHERE  id = '{id}'".format(id = id, table_name = db_name))
    result = cursor.fetchall()
    conn.commit()
    conn.close()
    return(result)

def save_entreprise(nom):
    conn = sqlite3.connect(db_file_name)
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(id) FROM {table_name}".format(table_name = db_name))
    conn.commit()
    id = cursor.fetchone()[0] + 1
    cursor.execute("INSERT INTO {table_name} (id, nom) VALUES ('{id}', '{name}')".format(id = id, nom = nom))
    conn.commit()
    conn.close()

def delete_categorie(id):
    conn = sqlite3.connect(db_file_name)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM {table_name} WHERE id={id}".format(id = id, table_name = db_name))
    conn.commit()
    conn.close()

def update_entreprise(id, nom):
    conn = sqlite3.connect(db_file_name)
    cursor = conn.cursor()
    cursor.execute("UPDATE {table_name} SET nom='{nom}' WHERE id={id}".format(nom = nom, id = id))
    conn.commit()
    conn.close()

