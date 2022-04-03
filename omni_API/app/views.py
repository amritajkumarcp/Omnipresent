# import the Flask class from the flask module
from app import app, model
from flask import render_template, request, jsonify
from external_api import countries
import json

import logging

log = logging.getLogger(__name__)

# use decorators to link the function to a url
@app.route('/')
def home():
   return  "<b>There has been a change</b>"
#    return render_template('index.html')  # return a string

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')  # render a template

users = []

def _find_next_id():
    return max(user["id"] for user in users) + 1

@app.route("/users",methods = ['GET','POST'])
def manage_users():
    user_params = {}
    if request.args:
        user_params = request.args.to_dict()
    
    if request.method == 'GET':
        users =  model.fetch_users(user_params)
        log.error("users "+ json.dumps(users))
        if users.get("error", True) is False and len(users.get("users",[]))>0:
            refresh_country_data = user_params.get("refresh_countries",False)
            log.error("users "+ json.dumps(users["users"]))

            users_sanitized = sanitize_user_list(users["users"], refresh_country_data)
            if len(users_sanitized)>0:
                users["users"] = users_sanitized
        return users, 201
    elif request.method == 'POST':
        return model.add_user(user_params), 201
    else:
        return {"error":True, "message":"HTTP method not defined"}, 415

def sanitize_user_list(users_list, refresh_country_data=False):
    users_final=[]
    if len(users_list)>0:
        countries_list = countries.get_all_countries(refresh_country_data)
        if countries_list.get("error", True) is False and len(countries_list)>0:
            countries_list = countries_list.get("countries_list",{})
        country_keys = list(countries_list.keys())
        log.error("country_specific_data "+ ", ".join(country_keys))

        for user in users_list:
            log.error("user "+ json.dumps(user))
            cioc = user.get("country","")
            if countries_list and len(countries_list)>0:
                country_specific_data = None
                if cioc in country_keys:
                    country_specific_data = countries_list.get(cioc,{})
                
                if country_specific_data is None or len(country_specific_data)<=0:
                    country_specific_data = countries.get_single_country(user)
                    if country_specific_data is not None and len(country_specific_data)>0:
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

@app.route("/countries",methods = ['GET'])
def get_countries():
    user_params = {}
    if request.args:
        user_params = request.args.to_dict()
    if request.method == 'GET':
        return countries.get_all_countries(), 201
    else:
        return {"error":True, "message":"HTTP method not defined"}, 415

