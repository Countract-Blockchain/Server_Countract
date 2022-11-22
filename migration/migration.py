import mysql.connector
import bcrypt

dbconfig = {
    "host":"localhost",
    "port":"3306",
    "username":"root",
    "password":"",
    "database":"countract_db"
}

class migration():
    def __init__(self):
        self.con = mysql.connector.connect(host=dbconfig['host'],user=dbconfig['username'],password=dbconfig['password'],database=dbconfig['database'])
        self.con.autocommit=True
        self.cur = self.con.cursor(dictionary=True)
    
    def users(self):
        self.cur.execute("DROP TABLE IF EXISTS users;")
        salt = bcrypt.gensalt()

        data1 = {
            "name":"boggie",
            "email" : "boggie@gmail.com",
            "password": bcrypt.hashpw(bytes("tes123", encoding="utf-8"), salt).decode()
        }
        data2 = {
            "name":"wisnu",
            "email" : "wispram@gmail.com",
            "password": bcrypt.hashpw(bytes("tes123", encoding="utf-8"), salt).decode()
        }
        data3 = {
            "name":"ivan",
            "email" : "ivan@gmail.com",
            "password": bcrypt.hashpw(bytes("tes123", encoding="utf-8"), salt).decode()
        }
        data4 = {
            "name":"iqbal",
            "email" : "iqbalabd@gmail.com",
            "password": bcrypt.hashpw(bytes("tes123", encoding="utf-8"), salt).decode()
        }

        self.cur.execute("CREATE TABLE users (ID int NOT NULL AUTO_INCREMENT, name varchar(255), email varchar(255), password varchar(255), PRIMARY KEY (ID));")
        self.cur.execute(f"INSERT INTO users(name, email, password) VALUES('{data1['name']}', '{data1['email']}', '{data1['password']}')")
        self.cur.execute(f"INSERT INTO users(name, email, password) VALUES('{data2['name']}', '{data2['email']}', '{data2['password']}')")
        self.cur.execute(f"INSERT INTO users(name, email, password) VALUES('{data3['name']}', '{data3['email']}', '{data3['password']}')")
        self.cur.execute(f"INSERT INTO users(name, email, password) VALUES('{data4['name']}', '{data4['email']}', '{data4['password']}')")

    def dokumens(self):
        self.cur.execute("DROP TABLE IF EXISTS dokumens;")

        data1 = {
            "jenis":"Kartu Tanda Penduduk",
            "path" : "path_ktp_usr1",
            "user_id": 1
        }
        data2 = {
            "jenis":"Kartu Keluarga",
            "path" : "path_kk_usr1",
            "user_id": 1
        }
        self.cur.execute("CREATE TABLE dokumens (ID int NOT NULL AUTO_INCREMENT, jenis varchar(255), path varchar(255), user_id varchar(255), PRIMARY KEY (ID));")
        self.cur.execute(f"INSERT INTO dokumens(jenis, path, user_id) VALUES('{data1['jenis']}', '{data1['path']}', '{data1['user_id']}')")
        self.cur.execute(f"INSERT INTO dokumens(jenis, path, user_id) VALUES('{data2['jenis']}', '{data2['path']}', '{data2['user_id']}')")

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