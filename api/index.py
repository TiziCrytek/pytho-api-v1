from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from tradingview_ta import TA_Handler, Interval
from os.path import join
from datetime import datetime, timedelta    
import json, pyrebase, random, string, hashlib, pytz


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
    
    k = request.args.get('key')
    found = False
    for key in db.child("keys").get().each():
        if k == key.key():
            found = True
            break
    
    # Проверьте значение found после завершения цикла
    if found:
        return 'OK'
    else:
        return 'Error'


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
            return '', 400

@app.route('/connect', methods=['POST'])
def connect():
    data = request.json
    if data['code'] == 15142:
        server = db.child('server').child('access').get().val()
        if server:
            return '', 200
        else:
            return '', 400
    else:
        return '', 400

@app.route('/save', methods=['POST'])
def save():
    data = request.json
    if data['code'] == 15142:
        key = data['key']
        key = hashlib.sha256(key.encode()).hexdigest()
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
    found = False
    data = request.json
    current_time = datetime.now()

    if data['code'] == 15142:
        key = data['key']
        key = hashlib.sha256(key.encode()).hexdigest()
        for k in db.child("keys").get().each():
            if key == k.key():
                found = True
                key = k
                break

        if found:
            if datetime.strptime(key.val()['date'], '%Y-%m-%d %H:%M:%S') > current_time:
                if key.val()['device'] == data['mac']:
                    with open(join('data', 'app.py'), 'r') as file:
                        app = file.read()
                        file.close()
                    res = {
                        "key": {
                            "status": "ok",
                            "device": key.val()['device']
                        },
                        
                        "app": app
                    }
                elif key.val()['device'] != data['mac']:
                    if key.val()['device'] == '':
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
                        "status": "date",
                        "device": ""
                    },
                    
                    "app": ""
                }

        else:
            res = {
                    "key": {
                        "status": "no_key",
                        "device": ""
                    },
                    
                    "app": ""
                } 
        return res
    else:
        return jsonify({"error": "Invalid code"}), 400

def generate_random_string(length):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def generate_key():
    part1_length = random.randint(1, 9)
    part2_length = random.randint(1, 9)
    part3_length = 27 - part1_length - part2_length

    part1 = generate_random_string(part1_length)
    part2 = generate_random_string(part2_length)
    part3 = generate_random_string(part3_length)

    generated_key = part1 + '.' + part2 + '.' + part3
    hashed_key = hashlib.sha256(generated_key.encode()).hexdigest()
    return generated_key, hashed_key

@app.route('/create_key', methods=['POST'])
def create_key():
    data = request.json
    kiev_tz = pytz.timezone('Europe/Kiev')

    if data['code'] == 'a2edr45tf5':
        original_key, hashed_key = generate_key()
        current_time = datetime.now(kiev_tz)
        date = current_time + timedelta(seconds=int(data['date']))
        date = date.strftime('%Y-%m-%d %H:%M:%S')

        db.child('keys').child(hashed_key).set({"device": '', "date": date})
        return original_key
    else:
        return 'no', 400

@app.route('/admins', methods=['GET'])
def admins():
    if request.remote_addr == '176.105.166.7':
        return render_template('index.html')  
    else:
        return 'Error'

@app.route('/api', methods=['POST'])
def api():
    data = request.json

    res = jsonify({"message": "No command"})
    server = db.child('server').child('access').get().val()

    if data['command'] == 'lock':
        if server != False:
            db.child('server').update({"access": False})
            res = jsonify({"message": "Server is closed"})
        else:
            res = jsonify({"message": "The server is already closed"})

    elif data['command'] == 'open':
        if server != True:
            db.child('server').update({"access": True})
            res = jsonify({"message": "Server is open"})
        else:
            res = jsonify({"message": "The server is already open"})

    return res

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
    