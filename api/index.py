from flask import Flask
from flask_cors import cross_origin
from tradingview_ta import TA_Handler, Interval

app = Flask(__name__)


@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/get')
@cross_origin(origins = ['https://api-v1.vercel.app/get'])
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