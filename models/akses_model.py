import mysql.connector
from configs.config import dbconfig
from flask import make_response

class akses_model():
    def __init__(self):
        self.con = mysql.connector.connect(host=dbconfig['host'],user=dbconfig['username'],password=dbconfig['password'],database=dbconfig['database'])
        self.con.autocommit=True
        self.cur = self.con.cursor(dictionary=True)

    def add_akses_model(self,data):
        try:
            self.cur.execute(f"INSERT INTO aksess(user_id, dokumen_id, owner_id) VALUES('{data['user_id']}', '{data['dokumen_id']}', '{data['dokumen_id']}')")
        except Exception as e:
            return make_response({"message":"More Than 1 PK Detected"},400)
        return make_response({"message":"CREATED_SUCCESSFULLY"},201)

    def check_akses_model(self,data):
        self.cur.execute(f"SELECT * FROM aksess WHERE user_id='{data['user_id']}' AND dokumen_id='{data['dokumen_id']}'")
        result = self.cur.fetchall()
        if len(result) > 0:
            return True
        else:
            False