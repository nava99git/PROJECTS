import speech_recognition as sr
import time

lang = "en-US"
wakeword = "hello bed"

rec_comm = sr.Recognizer()
mic_comm = sr.Microphone()

triggered = False

def trigger_bed():
	print("Wake word detected")
	time.sleep(2)
	print("Start Talking")
	with mic_comm as source:
		print("..")
		audio_data = rec_comm.record(source, duration=5)
		print("Recognizing")
		try:
			text = rec_comm.recognize_google(audio_data, language=lang)
			print(text)
		except:
			print("Sorry didn't get you")

def callback(recognizer, audio):
	try:
		det_word = recognizer.recognize_google(audio, language=lang)
		print(det_word)
		if det_word == wakeword:
			trigger_bed()
	except:
		print("...")

rec = sr.Recognizer()
mic = sr.Microphone()

with mic as source:
	rec.adjust_for_ambient_noise(source)

stop_listening = rec.listen_in_background(mic, callback)
# stop_listening(wait_for_stop=False)
while True:
	pass