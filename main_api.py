from flask import Flask, request
import multiprocessing
import os

from led_control import led_gradually_turn_on, led_turn_off, led_rainbow, led_set_brightness, led_real_time

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
    if 'brightness' not in request.form:
        return "No brightness supplied.", 400

    # set new brightness
    brightness = int(request.form['brightness'])
    current_process.terminate()
    led_set_brightness(brightness)

    # restart the running process

    current_process = multiprocessing.Process(target=current_target)
    current_process.start()
    return "Brightness correctly set."


@app.route('/log', methods=['POST'])
def log():
    if 'value' not in request.form:
        return "No value supplied.", 400

    value = request.form['value']

    with open('values.txt', 'a') as values_file:
        values_file.write(value + '\n')


@app.route('/real_time', methods=['POST'])
def real_time():
    if 'values' not in request.form:
        return "No values supplied.", 400
    if 'sudden_change' not in request.form:
        return "No sudden_change supplied.", 400

    values = request.form['values']
    parsed_values = values.split(';')

    # handle empty array
    if values == '':
        parsed_values = []

    # don't run looping animation while this function is executed
    if current_process.is_alive():
        current_process.terminate()

    sudden_change = True if request.form['sudden_change'] == 'True' else False

    led_real_time(parsed_values, sudden_change)
    return "Successfully displayed values."


@app.route('/hello')
def hello():
    return "Hello"


if __name__ == '__main__':
    # remove log file
    try:
        os.remove('values.txt')
    except:
        pass

    current_target = led_rainbow
    current_process = multiprocessing.Process(target=led_rainbow)
    current_process.start()

    app.run(host='0.0.0.0', port=5000)
