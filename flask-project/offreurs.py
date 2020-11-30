from flask import Flask, jsonify, url_for,request,abort
import sqlite3
import os

db_file_name = "offreurs.db"
db_name      = "offreurs"

def createOffreursDB(table_name):
    print("Create {} DB".format(table_name))
    if os.path.exists(db_file_name):
        os.remove(db_file_name)
    conn = sqlite3.connect(db_file_name)
    conn.execute("CREATE TABLE {table_name} (id INTEGER PRIMARY KEY AUTOINCREMENT, login TEXT NOT NULL, password TEXT NOT NULL, entreprise TEXT NOT NULL, contact TEXT NOT NULL)".format(table_name=table_name))
    conn.execute("INSERT INTO  {table_name} (login,password,entreprise,contact) VALUES ('Laura367', 'Polytech45', 'Polytech Orleans', 'laura.vb@monmail.com')".format(table_name=table_name))
    conn.execute("INSERT INTO  {table_name} (login,password,entreprise,contact) VALUES ('Hugues98', 'Polytech45', 'Polytech Orleans', 'hugues.turmel@monmail.com')".format(table_name=table_name))    
    conn.commit()
    conn.close()

def find_all():
    conn = sqlite3.connect(db_file_name)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM {table_name}".format(table_name = db_name))
    result = cursor.fetchall()
    conn.commit()
    conn.close()
    return(result)


def find_one(id):
    conn = sqlite3.connect(db_file_name)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM {table_name} WHERE  id = '{id}'".format(id = id, table_name = db_name))
    result = cursor.fetchall()
    conn.commit()
    conn.close()
    return(result)

def save(login, password, entreprise, contact):
    conn = sqlite3.connect(db_file_name)
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(id) FROM {table_name}".format(table_name = db_name))
    conn.commit()
    id = cursor.fetchone()[0] + 1
    print(id)
    cursor.execute("INSERT INTO {table_name} (id, login, password, entreprise, contact) VALUES ('{id}', '{login}', '{password}', '{entreprise}', '{contact}')".format(id = id, login = login, password = password, entreprise = entreprise, contact = contact, table_name = db_name))
    conn.commit()
    conn.close()

def delete(id):
    conn = sqlite3.connect(db_file_name)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM {table_name} WHERE id={id}".format(id = id, table_name = db_name))
    conn.commit()
    conn.close()

def update(log_id, login, password, entreprise, contact):
    conn = sqlite3.connect(db_file_name)
    cursor = conn.cursor()
    cursor.execute("UPDATE {table_name} SET login='{login}', password='{password}', entreprise='{entreprise}', contact='{contact}' WHERE id={id}".format(login = login, password = password, entreprise=entreprise, contact = contact, id = log_id, table_name = db_name))
    conn.commit()
    conn.close()

