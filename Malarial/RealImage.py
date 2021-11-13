import cv2
import joblib
import numpy as np

image = cv2.imread("images/3.webp",0)

image=cv2.resize(image,(500,500))

image = cv2.bitwise_not(image)

ret, thresh = cv2.threshold(image, 127, 255, 0)
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

area=(cv2.contourArea(contours[0]),cv2.contourArea(contours[1]),cv2.contourArea(contours[2]),cv2.contourArea(contours[3]),cv2.contourArea(contours[4]))
area=np.asarray(area).reshape(1, -1)

model=joblib.load("MalariaClassifier")

result=model.predict(area)

if result[0]=='Parasitized':
    print("Malaria Infected")
else:
    print("No Malaria")