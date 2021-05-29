import speech_recognition as sr
import time

lang = "en-US"
wakeword = "hello bed"

rec = sr.Recognizer()
mic = sr.Microphone()

with mic as source:
	rec.adjust_for_ambient_noise(source)

def trigger_bed():
	time.sleep(2)
	print("Start Talking")
	with mic as source:
		print("..")
		audio_data = rec.record(source, duration=5)
		print("Recognizing")
		try:
			text = rec.recognize_google(audio_data, language=lang)
			return text
		except:
			print("Sorry didn't get you")
			return "null"

while True:
	word = trigger_bed()
	
	print(word)

	if word == wakeword:
		print("Wake word detected")
		
		command = trigger_bed()
		
		if "up" in command:
			print("Moving the bed up...")
		elif "down" in command:
			print("Moving the bed down...")
		elif "wake word" in command:
			print("Changing the wake word")
			wakeword = trigger_bed()
			print("New wake word : ", wakeword)
	else:
		pass