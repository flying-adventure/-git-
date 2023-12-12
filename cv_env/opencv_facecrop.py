import cv2

face_cascade = cv2.CascadeClassifier('../haarcascades/haarcascade_frontalface_default.xml')
eye_casecade = cv2.CascadeClassifier('../haarcascades/haarcascade_eye.xml')

img = cv2.imread('이길여.jpg"')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
faces = face_cascade.detectMultiScale(gray, 1.3,5)
imgNum = 0

for (x,y,w,h) in faces:
    cropped = img[y - int(h / 4):y + h + int(h / 4), x - int(w / 4):x + w + int(w / 4)]
    cv2.imwrite("thumbnail" + str(imgNum) + ".png", cropped)
    imgNum += 1

cv2.imshow('Image view', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
