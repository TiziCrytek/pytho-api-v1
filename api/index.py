from flask import Flask, request
from flask_cors import CORS
from tradingview_ta import TA_Handler, Interval
from os.path import join
import json

connect = True

app = Flask(__name__)
cors = CORS(app, origins = '*')

@app.route('/', methods=['POST'])
def root():
    if connect:
        return '', 200
    else:
        return '', 404

@app.route('/connect', methods=['POST'])
def connect():
    if connect:
        return '', 200
    else:
        return '', 404

@app.route('/system', methods=['POST'])
def system():
    data = request.json
    return data['version']


@app.route('/login', methods=['POST'])
def login():
    pass

@app.route('/gg')
def gg():
    keys = 'NO NO NO'
    with open(join('data', 'keys.json'), 'r') as file:
        keys = json.load(file)
        file.close()
    return keys

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
