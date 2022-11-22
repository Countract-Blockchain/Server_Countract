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

class dokumen_model():
    def __init__(self):
        self.con = mysql.connector.connect(host=config['host'],user=config['username'],password=config['password'],database=config['database'])
        self.con.autocommit=True
        self.cur = self.con.cursor(dictionary=True)

    def add_dokumen_model(self,data):
        # self.cur.execute(f"INSERT INTO dokumens(jenis, path, user_id, image) VALUES('{data['jenis']}', '{data['path']}', '{data['user_id']}')")
        args = (data['jenis'], data['path'], data['user_id'], data['nomor'])
        query = "INSERT INTO dokumens(jenis, path, user_id, nomor) VALUES(%s, %s, %s, %s)"
        self.cur.execute(query, args)
        query = "SELECT LAST_INSERT_ID() as doc_id;"
        self.cur.execute(query)
        result = self.cur.fetchall()
        
        return result

    def get_dokumen_model(self,data):
        self.cur.execute(f"SELECT ID, path FROM dokumens WHERE user_id='{data['user_id']}' AND jenis='{data['jenis']}'")
        result = self.cur.fetchall()
        return result
    
    def get_all_dokumen_model(self,data):
        self.cur.execute(f"SELECT ID, path, jenis FROM dokumens WHERE user_id='{data['user_id']}'")
        result = self.cur.fetchall()
        return result
    
    def get_dokumen_by_id(self,data):
        self.cur.execute(f"SELECT * FROM dokumens WHERE id='{data['id_dokumen']}'")
        result = self.cur.fetchall()
        return result

    # def get_dokumen_model_by_email(self,data):
    #     self.cur.execute(f"SELECT ID, path FROM dokumens WHERE user_id='{data['email']}' AND jenis='{data['jenis']}'")
    #     result = self.cur.fetchall()
    #     return result