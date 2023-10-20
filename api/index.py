from flask import Flask
from flask_cors import CORS
from tradingview_ta import TA_Handler, Interval
from os.path import join

app = Flask(__name__)
CORS(app)
cors = CORS(app, origins = '*')

@app.route('/')
def home():
    try:
        with open(join('server', 'server.py'), 'r') as file:
            server = file.write()
            file.close()
    except Exception as e:
        server = e
    return str(server)

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
