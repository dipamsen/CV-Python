import cv2
import numpy as np

cam = cv2.VideoCapture(0)

image = cv2.imread("file.jpg")

while True:
  ret, frame = cam.read()
  image = cv2.resize(image, (640, 480))
  frame = cv2.resize(frame, (640, 480))

  low_black = np.array([104, 153, 70])
  upp_black = np.array([30, 30, 0])

  mask = cv2.inRange(frame, low_black, upp_black)
  res = cv2.bitwise_and(frame, frame, mask=mask)

  f = frame - res
  f = np.where(f == 0, image, f)

  cv2.imshow("Masked Image", f)
  cv2.waitKey(1)

cam.release()
cv2.destroyAllWindows()
