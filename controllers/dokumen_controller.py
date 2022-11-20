from models.dokumen_model import dokumen_model
from models.auth_model import auth_model
from models.akses_model import akses_model
from models.user_model import user_model
import jwt
from flask import request, send_file, jsonify, make_response
from modules.encode import encode_image
from modules.decode import decode_image
from PIL import Image
from configs.config import key_jwt
from app import app
import os
from modules.Encrypter import Encrypter
from modules.Decrypter import Decrypter

import io
import numpy as np
import cv2
from Crypto.Cipher import AES

config = {}
config['key_jwt'] = os.getenv('key_jwt')

if config['key_jwt'] == None:
    config['key_jwt'] = key_jwt['key']

obj = dokumen_model()
auth = auth_model()
aks_model = akses_model() 
usr_model = user_model()

savepath = 'F:/Project/Countract/images/'

from Crypto.Cipher import AES

def enc_image(input_data,key,iv,filepath):
	cfb_cipher = AES.new(key, AES.MODE_CFB, iv)
	enc_data = cfb_cipher.encrypt(input_data)

	enc_file = open(filepath+"/encrypted.enc", "wb")
	enc_file.write(enc_data)
	enc_file.close()

	
def dec_image(input_data,key,iv,filepath):
	cfb_decipher = AES.new(key, AES.MODE_CFB, iv)
	plain_data = cfb_decipher.decrypt(input_data)

	output_file = open(filepath+"/output.png", "wb")
	output_file.write(plain_data)
	output_file.close()

@app.route("/dokumen/upload", methods=["POST"])
# @auth.token_auth()
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

    # img_visible = img_visible.resize((img_hidden.size[0], img_hidden.size[1]))

    # convert PIL into numpy array
    np_img = np.array(img_hidden.getdata()).reshape(img_hidden.size[1], img_hidden.size[0], 3)

    # convert numpy array into byte
    byte_img = np_img.tobytes()
  

    #Encrypt
    key = b'gavecrtqogavecrtqogavecrtqo23fde' # 32 bytes key
    nonce = b'H\x82\x1dM\xc4\xdaT\x0f\x17\x0e\xa9\xad\x94\x89\x81v'

    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce) #MODE_EAX => is about "how" to encript
    
    # we need to convert to bytes - we encrypt bytes - not strings
    encryptedContent, messageDigest = cipher.encrypt_and_digest(byte_img)
    
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)

    
    img_enc = np.frombuffer(encryptedContent, dtype=np_img.dtype)
    img_enc = img_enc.reshape(img_hidden.size[1], img_hidden.size[0], 3)
    # print(img_enc.shape)
    img_enc = img_enc
    img_enc = img_enc.astype(np.uint8)
    img_enc = Image.fromarray(img_enc)
    print("enc_size")
    print(img_enc.size)
    img_enc.save(savepath + '/encrypted_image.png')


    # decryptContent = cipher.decrypt(encryptedContent)

    # print(len(decryptContent))

    # img_dec = np.frombuffer(decryptContent, dtype=np_img.dtype)
    # img_dec = img_dec.reshape(img_hidden.size[1], img_hidden.size[0], 3)
    # print(img_dec.shape)
    # img_dec = img_dec
    # img_dec = img_dec.astype(np.uint8)
    # img_dec = Image.fromarray(img_dec)
    # img_dec.save(savepath + '/decrypted_image.png')

    # return jsonify(savepath), 200   

    encoded_image = encode_image(img_visible, img_enc)
    print("masuk encoded")
    print(encoded_image.size)
    encoded_image.save(savepath + '/encoded_image_new.png')
    data = {
        "user_id":tokendata["ID"],
        "path":savepath,
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
    print("masuk decoded")
    print(image.size)

    decoded_image = decode_image(image)
    print("dec_imgsize")
    print(decoded_image.size)
    decoded_image.save(savepath + '/decoded_image_new.png')

    # convert PIL into numpy array
    np_img = np.array(decoded_image.getdata()).reshape(decoded_image.size[1], decoded_image.size[0], 3)

    # convert numpy array into byte
    byte_img = np_img.tobytes()
  

    #Encrypt
    key = b'gavecrtqogavecrtqogavecrtqo23fde' # 32 bytes key
    nonce = b'H\x82\x1dM\xc4\xdaT\x0f\x17\x0e\xa9\xad\x94\x89\x81v'

    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce) #MODE_EAX => is about "how" to encript

    decryptContent = cipher.decrypt(byte_img)

    print(len(decryptContent))

    img_dec = np.frombuffer(decryptContent, dtype=np_img.dtype)
    img_dec = img_dec.reshape(decoded_image.size[1], decoded_image.size[0], 3)
    img_dec = img_dec
    img_dec = img_dec.astype(np.uint8)
    img_dec = Image.fromarray(img_dec)
    img_dec.save(savepath + '/decrypted_image_new.png')

    # return jsonify(savepath), 200

    return jsonify({
            "status": "OK",
            "path":savepath
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
