from flask import Flask, request, jsonify
from flask_cors import CORS
from tradingview_ta import TA_Handler, Interval
from os.path import join
import json

server_access = True

app = Flask(__name__)
cors = CORS(app, origins = '*')

@app.route('/', methods=['POST'])
def root():
    return '', 200

@app.route('/get-skins', methods=['POST'])
def get_skins():
    with open(join('data', 'skins.json'), 'r') as file:
        skins = json.load(file)
        file.close()
        
    data = request.json
    if data['code'] == 15142:
        return skins

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
    with open(join('data', 'keys.json'), 'r') as file:
            keys = json.load(file)
            file.close()

    data = request.json
    if data['code'] == 15142:
        key = data['key']
        if key in keys:
            if keys[key]['device'] == '':
                keys[key]['device'] = data['mac']
                with open(join('data', 'keys.json'), 'w') as file:
                    json.dump(keys, file)
                    file.close()
                return jsonify({"key": key}), 200
            else:
                return jsonify({"error": "Key already used"}), 400
        else:
            return jsonify({"error": "Invalid key"}), 400
    else:
        return jsonify({"error": "Invalid code"}), 400

@app.route('/login', methods=['POST'])
def login():
    with open(join('data', 'keys.json'), 'r') as file:
        keys = json.load(file)
        file.close()
    data = request.json
    if data['code'] == 15142:
        key = data['key']
        if key in keys:
            if keys[key]['device'] == data['mac']:
                with open(join('data', 'app.py'), 'r') as file:
                    app = file.read()
                    file.close()
                res = {
                    "key": {
                        "status": "ok",
                        "device": keys[key]['device']
                    },
                    
                    "app": app
                }
            elif keys[key]['device'] != data['mac']:
                if keys[key]['device'] == '':
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
                        "status": "",
                        "device": ""
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
    