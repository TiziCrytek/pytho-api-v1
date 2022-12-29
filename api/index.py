from flask import Flask

app = Flask(__name__)

# bank = TA_Handler(
#     symbol = 'EURUSD',
#     exchange = "FX_IDC", 
#     screener = "forex", 
#     interval = Interval.INTERVAL_1_MINUTE, 
#     timeout=None,
# )
# res = {
#     'summary': bank.get_analysis().summary["RECOMMENDATION"],
#     'oscillators': bank.get_analysis().oscillators["RECOMMENDATION"],
#     'moving_averages': bank.get_analysis().moving_averages["RECOMMENDATION"]
# }


@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/about')
def about():
    return 'About'