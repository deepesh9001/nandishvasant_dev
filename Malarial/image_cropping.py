import cv2
import joblib
import numpy as np

im = cv2.imread("images1/2.jpg")
im = cv2.resize(im, (900, 720))

width = 300
height = 240

imCropped = []

for i in range(3):
    for j in range(3):
        imCropped.append(im[height * i:height * (i + 1), width * j:width * (j + 1)])

model = joblib.load("MalariaClassifier")

count = 0

for i in range(9):
    imCropped[i] = cv2.resize(imCropped[i], (400, 400))
    imCropped[i] = (255 - imCropped[i])

    im_gray = cv2.cvtColor(imCropped[i], cv2.COLOR_BGR2GRAY)

    ret, thresh = cv2.threshold(im_gray, 130, 255, 0)
    contours, _ = cv2.findContours(thresh, 1, 2)

    area = []

    for j in range(5):
        try:
            area.append(cv2.contourArea(contours[j]))
        except:
            area.append(0.0)

    if area[0] == 0:
        area[0] = 15000
    area = np.asarray(area).reshape(1, -1)

    result = model.predict(area)

    if result == 'Parasitized':
        count += 1

if count > 0:
    print("Malaria detected")
else:
    print("No Malaria Detected")
