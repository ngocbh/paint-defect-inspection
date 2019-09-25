import cv2

img = cv2.imread('data/defect2.jpg')
cv2.rectangle(img, (2010, 1127), (2198, 1271), (255,0,0), 2)
cv2.imwrite("test.png", img)