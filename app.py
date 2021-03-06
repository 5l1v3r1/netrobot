from flask import Flask, current_app, request, render_template, Response
import time
import json
import subprocess
import os

app = Flask(__name__)
subprocess.call(['sudo', 'bash', './stream.sh'])
host_ip = subprocess.check_output(['hostname', '-I']).strip().decode('utf-8')
print("IP: " + str(host_ip))

@app.route('/')
def index():
	return render_template('index.html', stream_ip="http://" + host_ip + ":8081")

@app.route('/move')
def move():
	speed = request.args.get('speed')
	rotation = request.args.get('rotation')

	speed = float(speed) / 100
	rotation = float(rotation)

	speed_a = speed_b = speed
	if(rotation > 1):
	  speed_a = speed;
	  speed_b = -speed * abs(rotation) / 100
	elif(rotation < -1):
	  speed_b = speed;
	  speed_a = -speed * abs(rotation) / 100

	motor_a = motor_b = []

	if speed_a > 0:
		motor_a = [18, 17]
	else:
		motor_a = [17, 18]
	if speed_b > 0:
		motor_b = [23, 22]
	else:
		motor_b = [22, 23]

	print((on_pin, off_pin))
	os.system('echo "4=1" > /dev/pi-blaster')
	os.system(f'echo "{motor_a[0]}={abs(speed_a)}" > /dev/pi-blaster')
	os.system(f'echo "{motor_a[1]}=0" > /dev/pi-blaster')

	os.system(f'echo "{motor_b[0]}={abs(speed_b)}" > /dev/pi-blaster')
	os.system(f'echo "{motor_b[1]}=0" > /dev/pi-blaster')

	return Response(json.dumps((speed_a, speed_b)), status=200, mimetype="application/json")

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

if(__name__ == '__main__'):
	app.run(debug=True, host='0.0.0.0')
