import mysql.connector
from configs.config import dbconfig
from flask import make_response

class dokumen_model():
    def __init__(self):
        self.con = mysql.connector.connect(host=dbconfig['host'],user=dbconfig['username'],password=dbconfig['password'],database=dbconfig['database'])
        self.con.autocommit=True
        self.cur = self.con.cursor(dictionary=True)

    def add_dokumen_model(self,data):
        self.cur.execute(f"INSERT INTO dokumens(jenis, path, user_id) VALUES('{data['jenis']}', '{data['path']}', '{data['user_id']}')")
        return make_response({"message":"CREATED_SUCCESSFULLY"},201)

    def get_dokumen_model(self,data):
        self.cur.execute(f"SELECT ID, path FROM dokumens WHERE user_id='{data['user_id']}' AND jenis='{data['jenis']}'")
        result = self.cur.fetchall()
        return result

    # def get_dokumen_model_by_email(self,data):
    #     self.cur.execute(f"SELECT ID, path FROM dokumens WHERE user_id='{data['email']}' AND jenis='{data['jenis']}'")
    #     result = self.cur.fetchall()
    #     return result