from flask import Flask

app = Flask(__name__)

@app.route('/users')
def root():
    return 'Hello'

if __name__ == '__main':
    app.run()
