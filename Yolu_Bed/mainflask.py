import logging
import os
import json
from flask import Flask
from flask_ask import Ask, request, session, question, statement
import RPi.GPIO as GPIO
import serial
import time as t

app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger('flask_ask').setLevel(logging.DEBUG)
 
ser = serial.Serial('/dev/ttyS0', 9600, timeout=1)
ser.flush()

DIRECTIONUP = ["up","upward","forward"]
DIRECTIONDOWN = ["down","downward","backward"]
DIRECTIONSTOP = ["stop"]

@ask.launch
def launch():
    speech_text = 'Welcome to your Alexa enabled Smart bed.'
    return question(speech_text).reprompt(speech_text).simple_card(speech_text)
 
@ask.intent('DirectionIntent', mapping = {'direction':'direction'})
def DirectionIntent(direction,room):
    # print(direction)
    if direction in DIRECTIONSTOP:
        directionmsg = '{"direction" : "stop"}'
        msg = json.loads(directionmsg)
        ser.write(msg)
        return statement('Stopping the bed')

    elif direction in DIRECTIONUP:
        directionmsg = '{"direction" : "up"}'
        msg = json.loads(directionmsg)
        ser.write(msg)
        return statement('Moving the bed upward')

    elif direction in DIRECTIONDOWN:
        directionmsg = '{"direction" : "down"}'
        msg = json.loads(directionmsg)
        ser.write(msg)
        return statement('Moving the bed downward')

    else:
        return statement('Direction unclear')

@ask.intent('AngleIntent', mapping = {'angle':'angle'})
def AngleIntent(angle,room):
    # print(angle)
    try:
        angleInt = angle.toInt()
        if angleInt in range(minAngle,maxAngle):
            anglemsg = '{"angle" : %d }' % (angleInt)
            msg = json.loads(anglemsg)
            ser.write(msg)
            return statement('Setting the bed to %s degrees' % (angle))
        else:
            return statement('Please limit the angle value between %d degrees and %d degrees' % (minAngle,maxAngle))
    except:
        return statement('That is an invalid angle')

@ask.intent('PulseIntent', mapping = {'pulse':'pulse'})
def PulseIntent(pulse,room):
    msg = json.loads('{"pulse" : true}')
    ser.write(msg)
    startTime = t.time()
    while ser.in_waiting != 0:
        elapsedTime = t.time() - startTime
        if elapsedTime > 2:
            break;
    try:
        pulseValue = ser.readline().decode('utf-8').rstrip()
        return statement('Your current pulse rate is %d' % (pulseValue.toInt()))
    except:
        return statement('Sorry, Could not fetch your current pulse rate')

@ask.intent('AMAZON.HelpIntent')
def help():
    speech_text = 'You can say hello to me!'
    return question(speech_text).reprompt(speech_text).simple_card('HelloWorld', speech_text)
 
 
@ask.session_ended
def session_ended():
    return "{}", 200
 
 
if __name__ == '__main__':
    if 'ASK_VERIFY_REQUESTS' in os.environ:
        verify = str(os.environ.get('ASK_VERIFY_REQUESTS', '')).lower()
        if verify == 'false':
            app.config['ASK_VERIFY_REQUESTS'] = False
    app.run(debug=True)