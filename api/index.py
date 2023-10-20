from flask import Flask, request
from flask_cors import CORS
from tradingview_ta import TA_Handler, Interval
from os.path import join

app = Flask(__name__)
CORS(app)
cors = CORS(app, origins = '*')

@app.route('/test', methods=['POST'])
def handle_post_request():
    if request.method == 'POST':
        data = request.json  # Получаем данные POST-запроса в формате JSON
        # Обрабатываем данные...
        return 'POST request received successfully'  # Отправляем ответ на POST-запрос
    else:
        return 'Invalid request method'

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
