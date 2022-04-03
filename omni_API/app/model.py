from datetime import date
import sqlite3, os, json
from flask import g, jsonify

from app import app

from external_api import countries

import logging
log = logging.getLogger(__name__)

DATABASE = app.config.get("DATABASE_URI","")

# DATABASE = 'database.db'
THIS_FOLDER = os.path.realpath(os.path.dirname(__file__))

DB_URL = os.path.join(THIS_FOLDER, "../", DATABASE)


def row_to_dict(cursor: sqlite3.Cursor, row: sqlite3.Row) -> dict:
    data = {}
    for idx, col in enumerate(cursor.description):
        data[col[0]] = row[idx]
    return data

    

def get_db( rowbased_access=False):
    try:
        db = getattr(g, '_database', None)
        if db is None:
            db = g._database = sqlite3.connect(DB_URL)
            if rowbased_access is True:
                db.row_factory = row_to_dict #sqlite3.Row
        return {"error": False, "message":"Connection Established Successfully","conn":db}
    except Exception as e:
        log.error("get_db = "+str(e))
        return {"error": True, "message":str(e),"conn":None}

def close_connection():
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Function version
def row2dict(row):
    return json.dumps(tuple(row))

def fetch_users(params = {}):
    try:
        log.error("params "+json.dumps(params))
        limit = params.get("limit","")
        offset = params.get("offset","")
        conn_response = get_db(True)
        users = []
        if conn_response.get("error",True) is False:
            conn = conn_response.get("conn", None)
            if conn:
                curr = conn.cursor()
                query = 'SELECT * FROM users'
                if limit and offset:
                    query += f" limit {str(int(limit))} offset {str(int(offset))}" 
                users = curr.execute(query).fetchall()
                

                close_connection()
                # users_final = [row2dict(user) for user in users]
                return {"error": False, "message":"Users Fetched Successfully","users":users}
        else:
            return {"error": True, "message":"DB Connection could not be established.","users":users}

    except Exception as e:
        return {"error": True, "message":str(e),"users":[]}

def add_user(params={}):
    try:
        users = params.get("users",[])
        log.error(json.dumps(users))
        conn_response = get_db()
        resp=None
        if conn_response.get("error",False):
            conn = conn_response.get("conn", None)
            if conn and len(users)>0:
                if len(users)==1:
                    user = users[0]
                    firstName = user.get("firstName","")
                    lastName = user.get("lastName","")
                    dateOfBirth = user.get("dateOfBirth","")
                    jobTitle = user.get("jobTitle","")
                    company = user.get("company","")
                    country = user.get("country","")
                    if firstName and lastName and dateOfBirth and jobTitle and company and country:
                        resp = conn.execute("INSERT INTO users (firstName, lastName, dateOfBirth, jobTitle, company, country) VALUES (?, ?, ?, ?, ?, ?)",
                            (firstName, lastName, dateOfBirth, jobTitle, company, country)
                        )
                        return {"error": False, "message":"User Inserted Successfully","resp":resp}
                    else:
                        return {"error": True, "message":"User Insertion Failed. Check for mandatory input fields.","resp":resp}
                else:
                    users_list = []
                    for user in  users:
                        users_list.append(tuple(user.values()))
                    resp = conn.executemany("INSERT INTO users (firstName, lastName, dateOfBirth, jobTitle, company, country) VALUES (?, ?, ?, ?, ?, ?)",
                            users_list
                        )
                    return {"error": False, "message":"User Inserted Successfully","resp":resp}
                    

        return {"error": True, "message":"DB Connection could not be obtained.","resp":resp}

    except Exception as e:
        return {"error": True, "message":str(e),"resp":None}