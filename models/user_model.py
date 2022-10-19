from datetime import datetime, timedelta
import mysql.connector
import json
from flask import make_response, jsonify
import jwt
from configs.config import dbconfig, key_jwt
import bcrypt

class user_model():
    def __init__(self):
        self.con = mysql.connector.connect(host=dbconfig['host'],user=dbconfig['username'],password=dbconfig['password'],database=dbconfig['database'])
        self.con.autocommit=True
        self.cur = self.con.cursor(dictionary=True)

    def all_user_model(self):
        self.cur.execute("SELECT * FROM users")
        result = self.cur.fetchall()
        if len(result)>0:
            return {"data":result}
            # return make_response({"payload":result},200)
        else:
            return "No Data Found"
    
    def get_id_user_by_email(self, data):
        self.cur.execute(f"SELECT ID FROM users WHERE email='{data['email']}'")
        result = self.cur.fetchall()
        if len(result)>0:
            return result
        else:
            return None

    def add_user_model(self,data):
        self.cur.execute(f"INSERT INTO users(email, password) VALUES('{data['email']}', '{data['password']}')")
        return make_response({"message":"CREATED_SUCCESSFULLY"},201)

    def user_login_model(self, username, password):
        self.cur.execute(f"SELECT ID, email, password from users WHERE email='{username}'")
        result = self.cur.fetchall()
        print(result[0]['password'])
        
        if len(result)==1:
            if bcrypt.checkpw(bytes(f"{password}", encoding="utf-8"), bytes(f"{result[0]['password']}", encoding="utf-8")):
                exptime = datetime.now() + timedelta(minutes=30)
                exp_epoc_time = exptime.timestamp()
                data = {
                    "ID": result[0]['ID'],
                    "payload":result[0]['email'],
                    "exp":int(exp_epoc_time)
                }
                # print(int(exp_epoc_time))
                jwt_token = jwt.encode(data, key_jwt["key"], algorithm="HS256")
                return make_response({"token":jwt_token}, 200)
            else:
                return make_response({"message":"Please Check Your Email or Password"}, 204)
        else:
            return make_response({"message":"Please Check Your Email or Password"}, 204)