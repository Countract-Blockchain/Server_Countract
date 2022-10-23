from models.dokumen_model import dokumen_model
from models.auth_model import auth_model
from models.akses_model import akses_model
from models.user_model import user_model
import jwt
from flask import request, send_file, jsonify, make_response
from modules.encode import encode_image
from modules.decode import decode_image
from PIL import Image
# from configs.config import key_jwt
from app import app
import os

config = {}
config['key_jwt'] = os.getenv('key_jwt')

# if config['key_jwt'] == None:
#     config['key_jwt'] = key_jwt['key']

obj = dokumen_model()
auth = auth_model()
aks_model = akses_model()
usr_model = user_model()

@app.route("/dokumen/upload", methods=["POST"])
@auth.token_auth()
def upload_encode():
    authorization = request.headers.get("authorization")
    token = authorization.split(" ")[1]
    tokendata = jwt.decode(token, config['key_jwt'], algorithms="HS256")
    jenis = request.form['jenis']

    if "img_visible" not in request.files:
        return jsonify({
            "status": "Bad Request",
            "message": "No file part."
        }), 400

    if "img_hidden" not in request.files:
        return jsonify({
            "status": "Bad Request",
            "message": "No file part."
        }), 400

    source_img_visible = request.files.get("img_visible")
    source_img_hidden = request.files.get("img_hidden")

    if source_img_visible.filename == "":
        return jsonify({
            "status": "Bad Request",
            "message": "No selected file."
        }), 400

    if source_img_hidden.filename == "":
        return jsonify({
            "status": "Bad Request",
            "message": "No selected file."
        }), 400

    img_visible = Image.open(source_img_visible)
    img_hidden = Image.open(source_img_hidden)

    path = encode_image(img_visible, img_hidden)
    data = {
        "user_id":tokendata["ID"],
        "path":path,
        "jenis":jenis
    }
    # print(data)
    obj.add_dokumen_model(data)

    return jsonify({
            "status": "OK",
            "message": "Success"
        }), 200

@app.route("/dokumen/decode", methods=["POST"])
def dokumen_decode():
    if "image" not in request.files:
        return jsonify({
            "status": "Bad Request",
            "message": "No file part."
        }), 400

    source_image = request.files.get("image")

    if source_image.filename == "":
        return jsonify({
            "status": "Bad Request",
            "message": "No selected file."
        }), 400

    image = Image.open(source_image)

    path = decode_image(image)

    return jsonify({
            "status": "OK",
            "path":path
        }), 200

@app.route("/dokumen", methods=["GET"])
def get_dokumen():
    authorization = request.headers.get("authorization")
    token = authorization.split(" ")[1]
    tokendata = jwt.decode(token, config['key_jwt'], algorithms="HS256")

    data = {
        "user_id":tokendata["ID"],
        "jenis":request.form['jenis']
    }
    result = obj.get_dokumen_model(data)

    return make_response({"data":result})

@app.route("/dokumen/akses", methods=["GET"])
def check_dokumen_akses():
    authorization = request.headers.get("authorization")
    token = authorization.split(" ")[1]
    tokendata = jwt.decode(token, config['key_jwt'], algorithms="HS256")

    email = {
        "email":request.form['email_owner']
    }

    id_user = usr_model.get_id_user_by_email(email)

    data = {
        "user_id":id_user[0]["ID"],
        "jenis":request.form['jenis']
    }

    dokumen_data = obj.get_dokumen_model(data)

    isAkses = False
    if len(dokumen_data) == 1:
        check_data = {
            "user_id":tokendata["ID"],
            "dokumen_id":dokumen_data[0]["ID"]
        }
        isAkses = aks_model.check_akses_model(check_data)

    if isAkses:
        return make_response({"data":dokumen_data})
    else:
        return make_response({"Message":"Sorry You Didn't have Access to this Document"}, 400)
