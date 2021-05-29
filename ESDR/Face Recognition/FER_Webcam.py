from fer import FER
import cv2
import time
import pprint

cap = cv2.VideoCapture(0)
detector = FER(mtcnn=True)

# Check if the webcam is opened correctly
if not cap.isOpened():
    raise IOError("Cannot open webcam")

while True:
    ret, frame = cap.read()
    frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
    cv2.imshow('Input', frame)
    try:
    	emotion, score = detector.top_emotion(frame)
    	print(emotion,"\t",score)
    except:
    	print("Face not detected")
    c = cv2.waitKey(1)
    if c == 27:
        break

cap.release()
cv2.destroyAllWindows()