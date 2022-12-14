import mysql.connector
import bcrypt
from configs.config import dbconfig

# dbconfig = {
#     "host":"localhost",
#     "port":"3306",
#     "username":"root",
#     "password":"",
#     "database":"countract_db"
# }

import os

config = {}
config['host'] = os.getenv('db_host')
config['username'] = os.getenv('db_username')
config['password'] = os.getenv('db_hpassword')
config['database'] = os.getenv('db_database')

config['key_jwt'] = os.getenv('key_jwt')

if config['host'] == None:
    config['host'] = dbconfig['host']

if config['username'] == None:
    config['username'] = dbconfig['username']

if config['password'] == None:
    config['password'] = dbconfig['password']

if config['database'] == None:
    config['database'] = dbconfig['database']

if config['key_jwt'] == None:
    config['key_jwt'] = key_jwt['key']


class migration():
    def __init__(self):
        self.con = mysql.connector.connect(host=config['host'],user=config['username'],password=config['password'],database=config['database'])
        self.con.autocommit=True
        self.cur = self.con.cursor(dictionary=True)

    def users(self):
        self.cur.execute("DROP TABLE IF EXISTS users;")
        salt = bcrypt.gensalt()

        data1 = {
            "email" : "boggie@gmail.com",
            "password": bcrypt.hashpw(bytes("tes123", encoding="utf-8"), salt).decode()
        }
        self.cur.execute("CREATE TABLE users (ID int NOT NULL AUTO_INCREMENT, email varchar(255), password varchar(255), PRIMARY KEY (ID));")
        self.cur.execute(f"INSERT INTO users(email, password) VALUES('{data1['email']}', '{data1['password']}')")

    def dokumens(self):
        self.cur.execute("DROP TABLE IF EXISTS dokumens;")
        self.cur.execute("CREATE TABLE dokumens (ID int NOT NULL AUTO_INCREMENT, jenis varchar(255), path varchar(255), user_id varchar(255), PRIMARY KEY (ID));")

    def aksess(self):
        self.cur.execute("DROP TABLE IF EXISTS aksess;")
        self.cur.execute("CREATE TABLE aksess (user_id int NOT NULL, dokumen_id int NOT NULL, owner_id int, PRIMARY KEY (user_id, dokumen_id));")

# Migration
try:
    print("migrate")
    migrate = migration()
    migrate.users()
    migrate.dokumens()
    migrate.aksess()
except Exception as e:
    print(e)