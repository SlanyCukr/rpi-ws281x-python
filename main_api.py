from flask import Flask, request
import multiprocessing

from led_control import led_gradually_turn_on, led_turn_off, led_rainbow, led_set_brightness

app = Flask(__name__)
current_process = None
current_target = None


@app.route('/turn_on', methods=['POST'])
def turn_on():
    timespan_sec1 = 500
    timespan_sec2 = 100
    if 'timespan_sec1' in request.args:
        timespan_sec1 = int(request.args.get('timespan_sec1'))
    if 'timespan_sec2' in request.args:
        timespan_sec2 = int(request.args.get('timespan_sec2'))

    # terminate old process, start a new one
    global current_process, current_target
    current_process.terminate()
    current_target = led_gradually_turn_on
    current_process = multiprocessing.Process(target=led_gradually_turn_on, args=(timespan_sec1, timespan_sec2))
    current_process.start()

    return 'Turning on!'


@app.route('/turn_off', methods=['POST'])
def turn_off():
    # terminate old process, start a new one
    global current_process, current_target
    current_process.terminate()
    current_target = led_turn_off
    current_process = multiprocessing.Process(target=led_turn_off)
    current_process.start()

    return 'Turning off!'


@app.route('/rainbow', methods=['POST'])
def rainbow():
    # terminate old process, start a new one
    global current_process, current_target
    current_process.terminate()
    current_target = led_rainbow
    current_process = multiprocessing.Process(target=led_rainbow)
    current_process.start()

    return 'Running rainbow program!'


@app.route('/set_brightness', methods=['POST'])
def set_brightness():
    global current_process
    if 'brightness' not in request.args:
        return "No brightness supplied.", 400

    # set new brightness
    brightness = int(request.args['brightness'])
    current_process.terminate()
    led_set_brightness(brightness)

    # restart the running process

    current_process = multiprocessing.Process(target=current_target)
    current_process.start()
    return "Brightness correctly set."


@app.route('/hello')
def hello():
    return "Hello"


if __name__ == '__main__':
    current_target = led_rainbow
    current_process = multiprocessing.Process(target=led_rainbow)
    current_process.start()

    app.run(host='0.0.0.0', port=5000)
