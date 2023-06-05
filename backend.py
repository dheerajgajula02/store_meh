from flask import Flask, jsonify, request
import pyrebase
import json

firebase_config = {
    "apiKey": "AIzaSyDqa0cnCF_jMO7bnkOBoHDUVd4w-zarZqM",
    "authDomain": "fir-course-72a1f.firebaseapp.com",
    "projectId": "fir-course-72a1f",
    "storageBucket": "fir-course-72a1f.appspot.com",
    "messagingSenderId": "713176253381",
    "appId": "1:713176253381:web:b25bca43ea8043680f41ac",
    "measurementId": "G-435F9VKV90",
    "databaseURL": "https://fir-course-72a1f-default-rtdb.firebaseio.com/"
}

firebase = pyrebase.initialize_app(firebase_config)

auth = firebase.auth()

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



        

@app.route('/hello', methods=['GET'])
def home():
    return jsonify({
        "first value":"name"
    })

if __name__=="__main__":
    app.run(port=5050, debug=True)
