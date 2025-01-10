from flask import Flask
app = Flask(__name__)#플라스크 애플리케이션을 생성하는 코드

@app.route('/')
def hello_pybo():
    return 'Hello, Pybo!'