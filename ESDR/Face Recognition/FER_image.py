from fer import FER
import cv2
import time
import pprint
from timer import timer

path = 'fear.jpg'

img = cv2.imread(path)
detector = FER(mtcnn=True)
result = detector.detect_emotions(img)
pprint.pprint(result)
time.sleep(10)
