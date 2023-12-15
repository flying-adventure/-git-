import cv2
import os



face_cascade = cv2.CascadeClassifier('../haarcascade_frontalface_default.xml')
eye_casecade = cv2.CascadeClassifier('../haarcascade_eye.xml')

img = cv2.imread("image/person.jpg")
if img is None:
    print("Can't read image file.")
else:
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3,5)


    for (x,y,w,h) in faces:
        cropped = img[y - int(h / 4):y + h + int(h / 4), x - int(w / 4):x + w + int(w / 4)]
        output_path = os.path.join("image", "cropped_by_OpenCV.png")
        cv2.imwrite(output_path, cropped)
      

   
    cv2.waitKey(0)
    cv2.destroyAllWindows()
