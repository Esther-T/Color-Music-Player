"""
Runs on the Raspberry Pi
pi_music_player.py
Date: 2/28/2020
Group: #7
"""
import cv2  # remember to 'pip install cv2'
import numpy
import math
import time
import colorsys as csys
from pygame import mixer
import boto3
import logging
import botocore
#from botocore.exceptions import ClientError
from boto3.s3.transfer import create_transfer_manager
from boto3.s3.transfer import TransferConfig, S3Transfer
from boto3.s3.transfer import ProgressCallbackInvoker
from boto3 import utils
s3_client = boto3.resource('s3', aws_access_key_id=key_id, aws_secret_access_key=secret_key)
client = boto3.client('s3', 'us-west-2')
transfer = S3Transfer(client)

cv2.namedWindow("preview")

mixer.init()

current_color = 0

while True:
    time.sleep(3)  # process color every 3 seconds
    transfer.download_file('iot-project-color-music-player', 'color_test.png', 'color_test.png')
    img = cv2.imread('color_test.png')
    
    img_height, image_width, a = img.shape
    
    img2 = cv2.getRectSubPix(img, (img_height/2, image_width/2), (img_height/2, image_width/2))  # cropping the image into the center of the img
    cv2.imwrite('color_test2.png', img2)
    b, g, r = cv2.split(img2)  # divide image into blue, green, and red arrays

    bheight, bwidth = b.shape
    gheight, gwidth = g.shape
    rheight, rwidth = r.shape

    tb = 0
    tg = 0
    tr = 0
    long(tb)
    long(tg)
    long(tr)
#  averaging the color of the whole image
    for i in b:
        for j in i:
            tb += j**2
    for i in g:
        for j in i:
            tg += j**2
    for i in r:
        for j in i:
            tr += j**2

    ab = math.floor(math.sqrt(tb / b.size))
    ag = math.floor(math.sqrt(tg / g.size))
    ar = math.floor(math.sqrt(tr / r.size))
    print("---------------")
    print("red:")
    print(ar)
    print("green:")
    print(ag)
    print("blue:")
    print(ab)
    

    img3 = numpy.zeros((300, 300, 3), numpy.uint8)  # filling img3 with the average color
    img3[:] = (ab, ag, ar)

    hls_h, hls_l, hls_s = csys.rgb_to_hls(ar / 255, ag / 255, ab / 255)  # converting from rgb to hls for easier color detection
    
    x = ("\nhue:", hls_h * 360, "\nlight:", hls_l * 100, "\nsat:", hls_s * 100)
    print("hue:")
    print(hls_h * 360)
    print("light:")
    print(hls_l * 100)
    print("sat:")
    print(hls_s * 100)
    
    if (hls_h <= (15.0/360) or hls_h >= (330.0/360)) and (hls_l > (35.0/100) and hls_l < (65.0/100)) and (hls_s > (70.0/100)) and current_color != 1:
        current_color = 1
        print("red")  # replace with play music
        mixer.music.load('/home/pi/Downloads/Pocahontas Colors of the Wind Disney Sing-Along.mp3')
        mixer.music.play()
    elif (hls_h < 140.0/360 and hls_h > 90.0/360) and (hls_l > 25.0/100 and hls_l < 60.0/100) and (hls_s > 65.0/100) and current_color != 2:
        current_color = 2
        print("green")  # replace with play music
        mixer.music.load('/home/pi/Downloads/Pocahontas Colors of the Wind Disney Sing-Along.mp3')
        mixer.music.play()
    elif (hls_h < 250.0/360 and hls_h > 190.0/360) and (hls_l > 35.0/100 and hls_l < 70.0/100) and (hls_s > 55.0/100) and current_color != 3:
        current_color = 3
        print("blue")  # replace with play music
        mixer.music.load('/home/pi/Downloads/01Track1.mp3')
        mixer.music.play()  
    else:
        print("no color")
    cv2.imshow("preview", img3)
    key = cv2.waitKey(20)
    if key == 27:  # exit on ESC
        break
