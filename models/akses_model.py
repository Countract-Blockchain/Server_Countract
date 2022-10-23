import mysql.connector
from configs.config import dbconfig
from flask import make_response
import os

config = {}
config['host'] = os.getenv('db_host')
config['username'] = os.getenv('db_username')
config['password'] = os.getenv('db_hpassword')
config['database'] = os.getenv('db_database')

if config['host'] == None:
    config['host'] = dbconfig['host']

if config['username'] == None:
    config['username'] = dbconfig['username']

if config['password'] == None:
    config['password'] = dbconfig['password']

if config['database'] == None:
    config['database'] = dbconfig['database']

class akses_model():
    def __init__(self):
        self.con = mysql.connector.connect(host=config['host'],user=config['username'],password=config['password'],database=config['database'])
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