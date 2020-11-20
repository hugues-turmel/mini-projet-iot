from flask import Flask, jsonify, url_for,request,abort
from flask_restx import Resource, Api, fields
import sqlite3
import os

db_name = "user.db"

def createDB(table_name):
    print("Create User DB")
    conn = sqlite3.connect(db_name)
    conn.execute("CREATE TABLE {table_name} (user_id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, description TEXT NOT NULL, log_id INTEGER)".format(table_name=table_name))
    conn.execute("INSERT INTO {table_name} (name,description) VALUES ('Laura', 'Elève ingénieur à Polytech Orleans')".format(table_name=table_name))
    conn.commit()
    conn.close()

if os.path.exists(db_name):
    os.remove(db_name)

createDB("user")