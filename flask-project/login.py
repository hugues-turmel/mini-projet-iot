from flask import Flask, jsonify, url_for,request,abort
from flask_restx import Resource, Api, fields
import sqlite3
import os

db_file_name = "login.db"
db_name      = "login"

def createDB(table_name):
    print("Create Login DB")
    conn = sqlite3.connect(db_file_name)
    conn.execute("CREATE TABLE {table_name} (log_id INTEGER PRIMARY KEY AUTOINCREMENT, login TEXT NOT NULL, password TEXT NOT NULL, FOREIGN KEY (log_id) REFERENCES user(log_id))".format(table_name=table_name))
    conn.execute("INSERT INTO {table_name} (login,password) VALUES ('Laura367', 'Polytech45')".format(table_name=table_name))
    conn.commit()
    conn.close()

if os.path.exists(db_file_name):
    os.remove(db_file_name)

createDB(db_name)


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

