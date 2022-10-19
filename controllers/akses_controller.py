from flask import request, send_file, jsonify
from app import app
from models.akses_model import akses_model
from models.auth_model import auth_model
import jwt
from configs.config import key_jwt

obj = akses_model()
auth = auth_model()

@app.route("/akses/add", methods=["POST"])
def add_akses():
    authorization = request.headers.get("authorization")
    token = authorization.split(" ")[1]
    tokendata = jwt.decode(token, key_jwt["key"], algorithms="HS256")

    data = {
        "user_id": request.form['user_id'],
        "dokumen_id": request.form['dokumen_id'],
        "owner_id": tokendata["ID"]
    }

    # if bcrypt.checkpw(b"tes123", bytes(f"{data['password']}", encoding="utf-8")):
    #     print("Match")

    return obj.add_akses_model(data)