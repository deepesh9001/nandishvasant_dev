import cv2
import joblib
import numpy as np

im = cv2.imread("images/3.png")
im = (255 - im)
im = cv2.resize(im, (700, 700))

im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

ret, thresh = cv2.threshold(im_gray, 130, 255, 0)
contours, _ = cv2.findContours(thresh, 1, 2)

im_gray = cv2.cvtColor(im_gray, cv2.COLOR_GRAY2BGR)
cv2.drawContours(im_gray, contours, -1, (0, 255, 0), 1)

cv2.imshow("Window", im_gray)
cv2.waitKey(0)
cv2.destroyAllWindows()

model = joblib.load("MalariaClassifier")

area = []

for i in range(5):
    try:
        area.append(cv2.contourArea(contours[i]))
    except:
        area.append(0.0)

if area[0] == 0:
    area[0] = 15000
area = np.asarray(area).reshape(1, -1)

print(area)

result = model.predict(area)
print(result)
