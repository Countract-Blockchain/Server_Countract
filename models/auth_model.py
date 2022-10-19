from datetime import datetime, timedelta
from logging import exception
import mysql.connector
import jwt
from flask import make_response, request, json
import re
from configs.config import dbconfig, key_jwt
from functools import wraps

class auth_model():
    
    def __init__(self):
        self.con = mysql.connector.connect(host=dbconfig['host'],user=dbconfig['username'],password=dbconfig['password'],database=dbconfig['database'])
        self.con.autocommit=True
        self.cur = self.con.cursor(dictionary=True)
        
    def token_auth(self, endpoint=""):
        def inner1(func):
            @wraps(func)
            def inner2(*args):
                endpoint = request.url_rule
                try:
                    authorization = request.headers.get("authorization")
                    if re.match("^Bearer *([^ ]+) *$", authorization, flags=0):
                        token = authorization.split(" ")[1]
                        try:
                            tokendata = jwt.decode(token, key_jwt["key"], algorithms="HS256")
                        except Exception as e:
                            return make_response({"ERROR":str(e)}, 401)
                        current_user = tokendata['payload']

                        if len(current_user) > 0:
                            self.cur.execute(f"SELECT email FROM users WHERE email='{current_user}'")
                            result = self.cur.fetchall()
                            if len(result) > 0:
                                return func(*args)
                            else:
                                return make_response({"ERROR":"INVALID_TOKEN"}, 401)
                        # if len(result)>0:
                        #     roles_allowed = json.loads(result[0]['roles_allowed'])
                        #     if current_role in roles_allowed:
                        # return func(*args)
                        #     else:
                        #         return make_response({"ERROR":"INVALID_ROLE"}, 422)
                        else:
                            return make_response({"ERROR":"INVALID_TOKEN"}, 401)
                    else:
                        return make_response({"ERROR":"INVALID_TOKEN"}, 401)
                except Exception as e:
                    return make_response({"ERROR":str(e)}, 401)
            return inner2
        return inner1