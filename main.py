from flask import Flask, render_template, request, jsonify
import time
import threading

app = Flask(__name__)

class DigitalClock:
    def __init__(self):
        self.format_12hr = True
        self.alarm_time = None
        self.alarm_set = False

    def get_time(self):
        return time.strftime('%I:%M:%S %p' if self.format_12hr else '%H:%M:%S')

    def get_date(self):
        return time.strftime('%A, %B %d, %Y')

    def set_alarm(self, alarm_time):
        self.alarm_time = alarm_time
        self.alarm_set = True
        threading.Thread(target=self.check_alarm).start()

    def check_alarm(self):
        while self.alarm_set:
            current_time = self.get_time()
            if current_time.startswith(self.alarm_time):
                self.alarm_set = False
                return "Alarm Ringing!"
            time.sleep(1)

clock = DigitalClock()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_time')
def get_time():
    return jsonify(time=clock.get_time(), date=clock.get_date())

@app.route('/switch_format')
def switch_format():
    clock.format_12hr = not clock.format_12hr
    return jsonify(success=True)

@app.route('/set_alarm', methods=['POST'])
def set_alarm():
    alarm_time = request.form['alarm_time']
    clock.set_alarm(alarm_time)
    return jsonify(success=True)

@app.route('/change_theme', methods=['POST'])
def change_theme():
    theme = request.form['theme']
    return jsonify(success=True, theme=theme)

if __name__ == "__main__":
    app.run(debug=True)
