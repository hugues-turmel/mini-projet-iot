from flask import Flask, jsonify, url_for,request,abort
from flask_restx import Resource, Api, fields
import sqlite3
import os

db_name = "login.db"

def createDB(table_name):
    print("Create Login DB")
    conn = sqlite3.connect(db_name)
    conn.execute("CREATE TABLE {table_name} (log_id INTEGER PRIMARY KEY AUTOINCREMENT, login TEXT NOT NULL, password TEXT NOT NULL, FOREIGN KEY (log_id) REFERENCES user(log_id))".format(table_name=table_name))
    conn.execute("INSERT INTO {table_name} (login,password) VALUES ('Laura367', 'Polytech45')".format(table_name=table_name))
    conn.commit()
    conn.close()

if os.path.exists(db_name):
    os.remove(db_name)

createDB("login")