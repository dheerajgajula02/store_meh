from flask import Flask, jsonify, request
import pyrebase
import json
import werkzeug
import os
import shutil


firebase_config = {
    "apiKey": "AIzaSyBGzjwvhJoq3kz9tgkvFGd10p2bg-ZX_hI",
    "authDomain": "storemeh-7ff88.firebaseapp.com",
    "projectId": "storemeh-7ff88",
    "storageBucket": "storemeh-7ff88.appspot.com",
    "messagingSenderId": "229911645323",
    "appId": "1:229911645323:web:901cf0acdfb6c9dead188e",
    "measurementId": "G-NYK67LP1N2",
    "databaseURL":"gs://storemeh-7ff88.appspot.com"
}

firebase = pyrebase.initialize_app(firebase_config)

auth = firebase.auth()
storage = firebase.storage()

app = Flask(__name__)

@app.route('/login', methods=['POST'])
def login():
    body = request.get_json(force=True)
    mail = body['email']
    password = body['password']
    message = ""
    try:
        auth.sign_in_with_email_and_password(email=mail, password=password)
        message= "CORRECT_CREDENTILS"
    except Exception as e:
        arguments = e.args[1]
        json_object = json.loads(arguments)
        if json_object['error']['message']=="INVALID_EMAIL":
            message = "INVALID_EMAIL"
        elif json_object['error']['message']=="EMAIL_NOT_FOUND":
            message="EMAIL_NOT_FOUND"
        elif json_object['error']['message']=="INVALID_PASSWORD":
            message = "INVALID_PASSWORD"
        else:
            message= json_object['error']['message']
    
    
    return jsonify({
        "message":message
    })

@app.route("/new_user", methods=['POST'])
def autheticate():
    body = request.get_json(force=True)
    mail = body['email']
    password = body['password']
    confirm_password= body['confirm_password']
    message =""
    if password==confirm_password:
        try:
            auth.create_user_with_email_and_password(email=mail, password=password)
            message="USER_CREATED"
        except Exception as e:
            arguments= e.args[1]
            json_object = json.loads(arguments)
            if json_object['error']['message']=="WEAK_PASSWORD":
                message = "WEAK_PASSWORD"
            elif json_object['error']['message']=="INVALID_EMAIL":
                message="INVALID_EMAIL"
            elif json_object['error']['message']=="EMAIL_EXISTS":
                message = "EMAIL_EXISTS"
            else:
                message= json_object['error']['message']

    else:
        message="passwords doesnt match"
    
    return jsonify({
        "message":message
    })

@app.route("/download", methods=["GET"])
def downlaod():
    body = request.get_json(force=True)
    email = body['email']
    document = body['document']
    cloud_name = email+"/"+document
    storage.child(cloud_name).download(path="test_folder/download", filename="test_folder/download/download_x.jpg")

    return jsonify({
        "message":"downloaded_successfully"
    })
    

@app.route('/upload', methods=['POST','UPLOAD'])
def upload():
    filename=""
    cloud_name =""
    user_name=""
    if request.method=="UPLOAD":
        document = request.files['document']
        filename = werkzeug.utils.secure_filename(document.filename)
        document.save("./uploaded_files/"+filename)
    if request.method=="POST":
        body = request.get_json(force=True)
        cloud_name= body['file_name']
        user_name = body['email']
    storage.child(user_name+'/'+cloud_name).put("./uploaded_files/"+filename)     
    

    print(filename)
    return jsonify({
        "message":"saving successful",
        "file_name":str(filename),
        "docuemtn":str(document),
        "form_data":body['first_name']
    })

@app.route("/upload_file", methods=['POST'])
def upload_file():
    document = request.files['document']
    document_name = werkzeug.utils.secure_filename(document.filename)
    print(document_name)
    document.save("./uploaded_files/"+document_name)
    return jsonify({
        "message":"document uploaded successfully"
    })

@app.route("/file_name", methods=['POST'])
def file_name():
    body= request.get_json(force=True)
    email = body['email']
    cloud_file_name = body['file_name']
    cloud_name= email+"/"+cloud_file_name
    lst = os.listdir("uploaded_files/")
    file_name = lst[0]
    local_filename = "uploaded_files/"+file_name
    storage.child(cloud_name).put(local_filename)
    shutil.rmtree("uploaded_files/")
    os.mkdir("uploaded_files/")

    return jsonify({
        "message":"uploaded successfully"
    })


    


@app.route('/hello', methods=['GET'])
def home():
    return jsonify({
        "first value":"name"
    })

if __name__=="__main__":
    app.run(port=5050, debug=True)
