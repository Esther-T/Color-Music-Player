# Captures images using a Windows' laptop camera and uploads the image to AWS S3 bucket

import cv2
import time
import boto3
# some code is from Evan Grim on stackoverflow.com
s3 = boto3.client('s3', aws_access_key_id=key_id, aws_secret_access_key=secret_key)

cv2.namedWindow("preview")
vc = cv2.VideoCapture(0)

if vc.isOpened():  # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False

while rval:
    time.sleep(3)
    cv2.imwrite("color_test.png", frame)
    s3.upload_file("color_test.png", "iot-project-color-music-player", "color_test.png")
    cv2.imshow("preview", frame)
    rval, frame = vc.read()
    key = cv2.waitKey(20)
    if key == 27:  # exit on ESC
        break
cv2.destroyWindow("preview")
