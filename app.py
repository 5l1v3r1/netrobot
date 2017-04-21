from flask import Flask, current_app, request, render_template, Response
import RPi.GPIO as GPIO
import subprocess
import time

GPIO.setmode(GPIO.BCM)

motors = {
  'front_left': (4, 17, 18)
  #'front_right': -1,
  #'back_left': -1,
  #'back_right': -1
}

# setup
for motor in motors:
	for port in motors[motor]:
		GPIO.setup(port, GPIO.OUT)

app = Flask(__name__)
host_ip = subprocess.check_output(['hostname', '-I']).strip().decode('utf-8')
print("IP: " + str(host_ip))

@app.route('/')
def index():
	return render_template('index.html', stream_ip='http://' + host_ip + ':8081')

@app.route('/move')
def move():
	speed = request.args.get('speed')
	rotation = request.args.get('rotation')
	GPIO.output(4, GPIO.HIGH)
	GPIO.output(17, GPIO.LOW)
	GPIO.output(18, GPIO.HIGH)

@app.route('/stop')
def stop():
	GPIO.output(18, GPIO.LOW)

if(__name__ == '__main__'):
	app.run(debug=True, host='0.0.0.0')
	
