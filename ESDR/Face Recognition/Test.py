import face_recognition
from fer import FER
import cv2
import numpy as np

cap = cv2.VideoCapture(0)
detector = FER(mtcnn=True)
font = cv2.FONT_HERSHEY_DUPLEX

# Check if the webcam is opened correctly
if not cap.isOpened():
    raise IOError("Cannot open webcam")

navaneeth_image = face_recognition.load_image_file("navaneeth.jpg")
navaneeth_face_encoding = face_recognition.face_encodings(navaneeth_image)[0]

# Load a second sample picture and learn how to recognize it.
arjun_image = face_recognition.load_image_file("arjun.jpg")
arjun_face_encoding = face_recognition.face_encodings(arjun_image)[0]

known_face_encodings = [
    navaneeth_face_encoding,
    arjun_face_encoding
]
known_face_names = [
    "navaneeth",
    "arjun"
]

face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

while True:
	ret, frame = cap.read()
	# small_frame = cv2.resize(frame, None, fx=0.25, fy=0.25, interpolation=cv2.INTER_AREA)
	small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
	# Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
	rgb_frame = small_frame[:, :, ::-1]
	
	if process_this_frame:
		# Find all the faces and face encodings in the current frame of video
		face_locations = face_recognition.face_locations(rgb_frame)
		face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

		face_names = []
		for face_encoding in face_encodings:
			# See if the face is a match for the known face(s)
			matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
			name = "Unknown"

			# Or instead, use the known face with the smallest distance to the new face
			face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
			best_match_index = np.argmin(face_distances)
			if matches[best_match_index]:
				name = known_face_names[best_match_index]

			face_names.append(name)

	process_this_frame = not process_this_frame

	# Display the results
	for (top, right, bottom, left), name in zip(face_locations, face_names):
		
		# face_frame = frame[(bottom*4)+35:(top*4)-45,(left*4)-25:(right*4)+35]
		# Scale back up face locations since the frame we detected in was scaled to 1/4 size
		top *= 4
		right *= 4
		bottom *= 4
		left *= 4

		# Draw a box around the face
		cv2.rectangle(frame, (left-25, top-45), (right+35, bottom+35), (0, 0, 255), 2)

		try:
			face_frame = frame[top-45:bottom+35,left-25:right+35]
			face = cv2.resize(face_frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
			emotion, score = detector.top_emotion(face)
			print(emotion,"\t",score)
			cv2.putText(frame, name+":"+emotion, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
		except:
			# print("No Face")
			cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

	# Display the resulting image
	cv2.imshow('Video', frame)

	# Hit 'q' on the keyboard to quit!
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

# Release handle to the webcam
cap.release()
cv2.destroyAllWindows()