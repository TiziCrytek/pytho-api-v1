from flask import Flask, request, jsonify
from flask_cors import CORS
from tradingview_ta import TA_Handler, Interval
from os.path import join
import json, pyrebase


server_access = True
password_db = 'jd7euw82kd84th7dje'


app = Flask(__name__)
cors = CORS(app, origins = '*')

config = {
    "apiKey": "AIzaSyDuqSii-UZqJ5VcbyegVwKUzphvtlId-Yg",
    "authDomain": "userdb-fb9e9.firebaseapp.com",
    "projectId": "userdb-fb9e9",
    "storageBucket": "userdb-fb9e9.appspot.com",
    "messagingSenderId": "865993321814",
    "appId": "1:865993321814:web:9385e30878bae0b5ecfaf7",
    "databaseURL": "https://userdb-fb9e9-default-rtdb.firebaseio.com",
}
firebase = pyrebase.initialize_app(config)
db = firebase.database()

@app.route('/vb')
def save_db():
    

    data = {"321": "mac"}
    key = '321'
    keys = db.child('keys').get()
    for i in keys.each():
        if key == i.key():
            
            return str(i.val()['device'])


@app.route('/', methods=['POST'])
def root():
    return '', 200

@app.route('/test')
def test():
    li = []
    for key in db.child("keys").get().each():
        li.append(key.key(), key.val())
    return li, 200

@app.route('/get-skins', methods=['POST'])
def get_skins():
    try:
        with open(join('data', 'skins.json'), 'r') as file:
            skins = json.load(file)
            file.close()
            
        data = request.json
        if data['code'] == 15142:
            return skins
        else:
            return 'Error', 400
    except Exception as e:
        return str(e)

@app.route('/get-common', methods=['POST'])
def get_common():
    try:
        with open(join('data', 'common.json'), 'r') as file:
            skins = json.load(file)
            file.close()
            
        data = request.json
        if data['code'] == 15142:
            return skins
        else:
            return 'Error', 400
    except Exception as e:
        return str(e)

@app.route('/version', methods=['POST'])
def version():
    data = request.json
    if data['code'] == 15142:
        if data['version'] == 'v0.1':
            return '', 200
        else:
            return '', 404

@app.route('/connect', methods=['POST'])
def connect():
    data = request.json
    if data['code'] == 15142:
        if server_access:
            return '', 200
        else:
            return '', 404
    else:
        return '', 404

@app.route('/save', methods=['POST'])
def save():
    data = request.json
    if data['code'] == 15142:
        key = data['key']
        for k in db.child('keys').get():
            if key == k.key():
                if k.val()['device'] == '':
                    db.child('keys').child(k.key()).update({"device": data['mac']})
                    return '', 200
                else:
                    return jsonify({"error": "Key already used"}), 400
            else:
                return jsonify({"error": "Invalid key"}), 400
        else:
            return jsonify({"error": "Invalid code"}), 400

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    if data['code'] == 15142:
        key = data['key']
        li = []
        db = firebase.database()
        for k in db.child("keys").get().each():
            li.append(k.key())
            if k.key() == key:
                if k.val()['device'] == data['mac']:
                    with open(join('data', 'app.py'), 'r') as file:
                        app = file.read()
                        file.close()
                    res = {
                        "key": {
                            "status": "ok",
                            "device": k.val()['device']
                        },
                        
                        "app": app
                    }
                elif k.val()['device'] != data['mac']:
                    if k.val()['device'] == '':
                        res = {
                            "key": {
                                "status": "ok",
                                "device": ""
                            },
                            
                            "app": ""
                        }
                    else:
                        res = {
                            "key": {
                                "status": "ok",
                                "device": "error"
                            },
                            
                            "app": ""
                        }
            else:
                res = {
                        "key": {
                            "status": "no_key",
                            "device": li
                        },
                        
                        "app": ""
                    } 
            return res
    else:
        return jsonify({"error": "Invalid code"}), 400

@app.route('/get')
def get():
    bank = TA_Handler(
        symbol = 'EURUSD',
        exchange = "FX_IDC", 
        screener = "forex", 
        interval = Interval.INTERVAL_1_MINUTE, 
        timeout=None,
    )
    res = {
        'summary': bank.get_analysis().summary["RECOMMENDATION"],
        'oscillators': bank.get_analysis().oscillators["RECOMMENDATION"],
        'moving_averages': bank.get_analysis().moving_averages["RECOMMENDATION"]
    }

    return res


if __name__ == '__main__':
    app.run(debug=True)
    