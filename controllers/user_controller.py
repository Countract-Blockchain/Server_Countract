from flask import request, send_file, jsonify
from app import app
from models.user_model import user_model
import bcrypt
from models.auth_model import auth_model

obj = user_model()
auth = auth_model()

@app.route("/user/all")
# The endpoint for token_auth() is automatically getting calculated in the auth_model.token_auth() method
# @auth.token_auth()
def all_users():
    return obj.all_user_model()

@app.route("/user/add", methods=["POST"])
def add_user():
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(bytes(f"{request.form['password']}", encoding="utf-8"), salt)
    # print(hashed.decode())
    hasshed_dict = {
        "name": request.form['name'],
        "email": request.form['email'],
        "password": hashed.decode()
    }

    # if bcrypt.checkpw(b"tes123", bytes(f"{hasshed_dict['password']}", encoding="utf-8")):
    #     print("Match")

    return obj.add_user_model(hasshed_dict)

@app.route("/user/login", methods=["POST"])
def user_login():
    email = request.form.get('email')
    password = request.form.get('password')
    
    return obj.user_login_model(email, password)