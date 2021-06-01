from flask import Flask, request, render_template, redirect, url_for, Response
import datetime as dt

app = Flask(__name__)

def getframe(start):
	print('getframe called')
	import cv2
	cap = cv2.VideoCapture(0)
	while True:
		ret, rawframe = cap.read()
		ret, jpeg = cv2.imencode('.jpg', rawframe)
		frame = jpeg.tobytes()
		yield (b'--frame\r\n'
			b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/')
def index():
	return render_template('index.html')

@app.route('/dynamic', methods = ['GET'])
def dynamic():
	timestamp =dt.datetime.now()
	return render_template('dynamic.html', timestamp = timestamp)

@app.route('/videofeed')
def videofeed():
	return Response(getframe(True), mimetype = 'multipart/x-mixed-replace; boundary=frame')
app.run(debug = True)
