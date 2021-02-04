import cv2
import time
import numpy as np

fourcc = cv2.VideoWriter_fourcc(*'XVID')

output_file = cv2.VideoWriter("output.avi", fourcc, 20.0, (640,  480))

cap = cv2.VideoCapture(0)

time.sleep(2)

bg = 0

for i in range(60):
    ret, bg = cap.read()

bg = np.flip(bg, axis=1)

while (cap.isOpened()):
    ret, img = cap.read()
    if not ret:
        break
    img = np.flip(img, axis=1)

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    lower_red = np.array([0, 120, 50])
    upper_red = np.array([10, 255, 255])
    mask_one = cv2.inRange(hsv, lower_red, upper_red)

    lower_red = np.array([170, 120, 70])
    upper_red = np.array([180, 255, 255])
    mask_two = cv2.inRange(hsv, lower_red, upper_red)

    mask_one = mask_one + mask_two

    mask_one = cv2.morphologyEx(
        mask_one, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    mask_one = cv2.morphologyEx(
        mask_one, cv2.MORPH_DILATE, np.ones((3, 3), np.uint8))

    mask_two = cv2.bitwise_not(mask_one)

    result_one = cv2.bitwise_and(img, img, mask=mask_two)

    result_two = cv2.bitwise_and(bg, bg, mask=mask_one)

    final_output = cv2.addWeighted(result_one, 1, result_two, 1, 0)

    output_file.write(final_output)

    cv2.imshow("MAGIC", final_output)

    cv2.waitKey(1)

cap.release()
output_file.release()
cv2.destroyAllWindows()
