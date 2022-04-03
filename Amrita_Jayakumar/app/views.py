# import the Flask class from the flask module
from app import app, service
from flask import render_template, request, jsonify
import json

import logging

log = logging.getLogger(__name__)

# use decorators to link the function to a url
@app.route('/', methods = ['GET'])
def home():
    if request.method == 'GET':
        return  "<b>Omni API</b>", 200
    else:
        return "Method not allowed!", 405

# specify HTTPS methods to differentiate between various HTTP methods.
@app.route("/users",methods = ['GET'])
def manage_users():
    try:
        user_params = {}
        if request.args:
            user_params = request.args.to_dict()
        
        if request.method == 'GET':
            users =  service.fetch_users(user_params)
            if users.get("error", True) is False and len(users.get("users",[]))>0:
                refresh_country_data = user_params.get("refresh",False)
                users_sanitized = service.sanitize_user_list(users["users"], refresh_country_data)
                if len(users_sanitized)>0:
                    users["users"] = users_sanitized
            return users, 201
        else:
            return {"error":True, "message":"HTTP method not defined"}, 415
    except Exception as e:
        return {"error":True, "message":str(e)}, 500


