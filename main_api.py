from flask import Flask, request

from led_control import led_gradually_turn_on, led_turn_off, led_rainbow

app = Flask(__name__)


@app.route('/turn_on', methods=['POST'])
def turn_on():
    timespan_sec1 = 500
    timespan_sec2 = 100
    if 'timespan_sec1' in request.args:
        timespan_sec1 = int(request.args.get('timespan_sec1'))
    if 'timespan_sec2' in request.args:
        timespan_sec2 = int(request.args.get('timespan_sec2'))

    led_gradually_turn_on(timespan_sec1, timespan_sec2)
    return 'Turned on!'


@app.route('/turn_off', methods=['POST'])
def turn_off():
    led_turn_off()
    return 'Turned off!'


@app.route('/rainbow', methods=['POST'])
def rainbow():
    led_rainbow()
    return 'Rainbow!'


@app.route('/hello')
def hello():
    return "Hello"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
