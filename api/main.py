from flask import Flask

app = Flask(__name__)

@app.get('/users')
def root():
    return 'Hello'

if __name__ == '__main':
    app.run()