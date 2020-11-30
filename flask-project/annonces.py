from flask import Flask, jsonify, url_for,request,abort
import sqlite3
import os


db_file_name = "annonces.db"
db_name      = "annonces"

def createDB(table_name):
    print("Create {} DB".format(table_name))
    if os.path.exists(db_file_name):
        os.remove(db_file_name)
    conn = sqlite3.connect(db_file_name)
    conn.execute("CREATE TABLE {table_name} (id INTEGER PRIMARY KEY AUTOINCREMENT, titre TEXT NOT NULL, entreprise TEXT NOT NULL, categorie TEXT NOT NULL, date_depot TEXT NOT NULL, date_limite TEXT NOT NULL, description TEXT NOT NULL, contact TEXT NOT NULL, mots_cles TEXT NOT NULL)".format(table_name=table_name))
    conn.execute("INSERT INTO  {table_name} (login,password) VALUES ('Laura367', 'Polytech45')".format(table_name=table_name))
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

def find_all_for_one(log_id):
    conn = sqlite3.connect(db_file_name)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM {table_name} WHERE log_id={id}".format(id = log_id, table_name = db_name))
    result = cursor.fetchall()
    conn.commit()
    conn.close()
    return(result)

def find_one(login):
    conn = sqlite3.connect(db_file_name)
    cursor = conn.cursor()
    cursor.execute("SELECT login,password FROM {table_name} WHERE  login = '{login}'".format(login = login, table_name = db_name))
    result = cursor.fetchall()
    conn.commit()
    conn.close()
    return(result)

def save(login, password):
    conn = sqlite3.connect(db_file_name)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO {table_name} (login,password) VALUES ('{login}', '{password}')".format(login = login, password = password, table_name = db_name))
    conn.commit()
    conn.close()

def delete(log_id):
    conn = sqlite3.connect(db_file_name)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM {table_name} WHERE log_id={id}".format(id = log_id, table_name = db_name))
    conn.commit()
    conn.close()

def update(log_id, login, password):
    conn = sqlite3.connect(db_file_name)
    cursor = conn.cursor()
    cursor.execute("UPDATE {table_name} SET login='{login}', password='{password}' WHERE log_id={id}".format(login = login, password = password, id = log_id, table_name = db_name))
    conn.commit()
    conn.close()

