from flask import Flask, request
from datetime import datetime
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello world!'


@app.route('/date')
def date():
    today = datetime.now().strftime('%Y-%m-%d')
    return today


@app.route('/square')
def square():
    x1 = request.args.get('x')
    result = '.' in x1
    if result:
        x = float(x1)
        num = pow(x, 2)
        return '%.2f' % num
    else:
        x = int(x1)
        num = pow(x, 2)
        return '%d' % num


@app.route('/divide')
def divide():
    x1 = request.args.get('x')
    y1 = request.args.get('y')
    x = float(x1)
    y = float(y1)
    result = x/y
    return '%.1f' % result


app.run(host='0.0.0.0',
        port=8080,
        debug=True)
