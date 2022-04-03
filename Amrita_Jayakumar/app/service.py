from datetime import date
import sqlite3, os, json
from flask import g, jsonify
from app import app
from external_api import countries

import logging
log = logging.getLogger(__name__)

DATABASE = app.config.get("DATABASE_URI","")

THIS_FOLDER = os.path.realpath(os.path.dirname(__file__))

DB_URL = os.path.join(THIS_FOLDER, "../", DATABASE)

class Employee:
  def __init__(self, id,created, firstName, lastName, jobTitle, company, country, dateOfBirth, countryInfo, region, uid):
    self.firstName = firstName
    self.lastName = lastName
    self.dateOfBirth = dateOfBirth
    self.jobTitle= jobTitle
    self.company = company
    self.country = country
    self.created = created
    self.id = id


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
                query = 'SELECT * FROM users' #to fetch all users
                if limit and offset:
                    query += f" limit {str(int(limit))} offset {str(int(offset))}" #for pagination
                users = curr.execute(query).fetchall()
                log.error(json.dumps(users))
                close_connection()
                # users_final = [Employee(id=user["id"], firstName=user["firstName"], created=user["created"], lastName=user["lastName"], jobTitle=user["jobTitle"], company=user["company"], country=user["country"], dateOfBirth=user["dateOfBirth"]) for user in users]
                return {"error": False, "message":"Users Fetched Successfully","users":users}
        else:
            return {"error": True, "message":"DB Connection could not be established.","users":users}

    except Exception as e:
        return {"error": True, "message":str(e),"users":[]}


def sanitize_user_list(users_list, refresh_country_data=False):
    users_final=[]
    if len(users_list)>0:
        #fetch all countries at once
        countries_l = countries.get_all_countries(refresh_country_data) 
        if countries_l.get("error", True) is False and len(countries_l)>0:
            g._countries_list = countries_l.get("countries_list",[])
        
        empCountryList = map(addCountryInfo, users_list)
        users_final = [ user for user in empCountryList]
    return users_final

def addCountryInfo(emp):
    employee = Employee(id=emp["id"], firstName=emp["firstName"], created=emp["created"], lastName=emp["lastName"], jobTitle=emp["jobTitle"], company=emp["company"], country=emp["country"], dateOfBirth=emp["dateOfBirth"], countryInfo=None, region=None, uid=None)
    # Get the item from the dictionary/ iterable that is with matching predicate
    countries_list = getattr(g,"_countries_list")
    countryInfo = next(filter(lambda c: employee.country in [c.cioc, c.cca2], countries_list), None)
    
    cInfo = countryInfo.__dict__
    
    # Take only necessary data from the above item and add it to the employee
    emp.update(cInfo)
    if emp.get("region","") in app.config.get("REGIONS",[]):
        firstName = emp.get("firstName","")
        lastName = emp.get("lastName","")
        dateOfBirth = emp.get("dateOfBirth","")
        dateOfBirth = dateOfBirth.replace("/","")
        uid = ""
        if firstName and lastName and dateOfBirth:
            uid = f"{firstName.lower()}{lastName.lower()}{dateOfBirth}"
        emp["uid"] = uid
        
    # Return the employee
    return emp


