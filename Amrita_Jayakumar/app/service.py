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
        return {"error": True, "message":str(e),"conn":None}

def close_connection():
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def fetch_users(params = {}):
    try:
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

def sanitize_user_list(users_list, refresh_country_data=False):
    users_final=[]
    if len(users_list)>0:
        countries_list = countries.get_all_countries(refresh_country_data)
        if countries_list.get("error", True) is False and len(countries_list)>0:
            countries_list = countries_list.get("countries_list",{})
        country_keys = list(countries_list.keys())

        for user in users_list:
            cioc = user.get("country","")
            if countries_list and len(countries_list)>0:
                country_specific_data = None
                if cioc in country_keys:
                    country_specific_data = countries_list.get(cioc,{})
                
                if country_specific_data is None or len(country_specific_data)<=0:
                    country_specific_data = {}
                    country_specific_data = countries.get_single_country(user)
                    
                    if country_specific_data.get("error", True) is False and len(country_specific_data)>0:
                        country_specific_data = country_specific_data.get("country_data",{})

                if country_specific_data is not None and len(country_specific_data)>0:

                    region = country_specific_data.get("region","")
                    
                    if region in app.config.get("REGIONS",[]):
                        firstName = user.get("firstName","")
                        lastName = user.get("lastName","")
                        dateOfBirth = user.get("dateOfBirth","")
                        dateOfBirth = dateOfBirth.replace("/","")
                        uid = ""
                        if firstName and lastName and dateOfBirth:
                            uid = f"{firstName.lower()}{lastName.lower()}{dateOfBirth}"
                        country_specific_data["uid"] = uid

                
            user.update(country_specific_data)
            users_final.append(user)
    return users_final
    
def add_user(params={}):
    try:
        users = params.get("users",[])
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