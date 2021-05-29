import face_recognition
from fer import FER
import cv2
import time
import pprint

cap = cv2.VideoCapture(0)
detector = FER(mtcnn=True)

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

face_encodings = []

while True:
    ret, frame = cap.read()
    frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
    
    try:
        det_emotion = detector.detect_emotions(frame)
        top_emotions = [ max(e["emotions"], key=lambda key: e["emotions"][key]) for e in det_emotion ]
    
        i = 0
        for top_emotion in top_emotions:
            score = det_emotion[i]["emotions"][top_emotion]
            bounding_box = det_emotion[i]["box"]
            name = "Unknown"
            face_frame = frame[(bounding_box[1]):(bounding_box[1] + bounding_box[3]),(bounding_box[0]):(bounding_box[0] + bounding_box[2]),::-1]
            #face_frame = frame[:, :, ::-1]
            current_encoding = face_recognition.face_encodings(face_frame)[0]
            
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, current_encoding)
            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]

            cv2.rectangle(frame,(bounding_box[0], bounding_box[1]),
            (bounding_box[0] + bounding_box[2], bounding_box[1] + bounding_box[3]),(0, 155, 255), 2,)
            print(name,"\t",top_emotion,"\t",score,"\t",bounding_box)
            i=i+1
        
            cv2.imshow('CAMERA', frame)
    
    except:
    	print("Face not detected")
    c = cv2.waitKey(1)
    if c == 27:
        break

cap.release()
cv2.destroyAllWindows()