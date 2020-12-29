from flask import Flask

from led_control import led_gradually_turn_on, led_turn_off

app = Flask(__name__)


@app.route('/turn_on')
def turn_on():
    led_gradually_turn_on(500)
    return 'Turned on!'


@app.route('/turn_off')
def turn_off():
    led_turn_off()
    return 'Turned off!'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
