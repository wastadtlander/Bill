"""
Detect white rectangle
    Read in the image
    Convert to B/W
    Edge detection
    Thresholding
    Find contours
    Find the largest contour
    Draw a rectangle around it
    Resize the image
    Crop the image
    Skew the image to rectangle
    Save the new image
    
Detect the orders on the receipt
    Read the image
    Segment the image sections - Header, Order list, Footer
    For every element in the Order List
        OCR
        Create an order entry
    Return order entries and segments
"""

from fourcorners import four_point_transform
from skimage.filters import threshold_local
import numpy as np
import argparse
import cv2
import imutils
from random import randrange

import pytesseract
from pytesseract import Output

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True,
    help = "Path to the image to be scanned")
args = vars(ap.parse_args())

# load the image and compute the ratio of the old height
# to the new height, clone it, and resize it
image = cv2.imread(args["image"])
ratio = image.shape[0] / 500.0
orig = image.copy()
image = imutils.resize(image, height = 500)
# convert the image to grayscale, blur it, and find edges
# in the image
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (5, 5), 0)
edged = cv2.Canny(gray, 75, 200)
# show the original image and the edge detected image
# find the contours in the edged image, keeping only the
# largest ones, and initialize the screen contour
cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:5]
# loop over the contours

for c in cnts:
    # approximate the contour
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.02 * peri, True)
    # if our approximated contour has four points, then we
    # can assume that we have found our screen
    if len(approx) == 4:
        screenCnt = approx
        break
    else:
        print("No rectangle found")
        exit()
        
# show the contour (outline) of the piece of paper
# apply the four point transform to obtain a top-down
# view of the original image
warped = four_point_transform(orig, screenCnt.reshape(4, 2) * ratio)
# convert the warped image to grayscale, then threshold it
# to give it that 'black and white' paper effect
warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
T = threshold_local(warped, 11, offset = 10, method = "gaussian")
warped = (warped > T).astype("uint8") * 255
# increase the contrast of warped
warped = cv2.adaptiveThreshold(warped, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

# find the order list in the receipt through tessaract
conf = "--psm 4"
d = pytesseract.image_to_data(warped, output_type=Output.DICT, config=conf)
n_boxes = len(d['level'])
for i in range(n_boxes):
    (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])   
    # warped = cv2.rectangle(warped, (x, y), (x + w, y + h), (randrange(0, 255), randrange(0, 255), randrange(0, 255)), 2)
text = pytesseract.image_to_string(warped, timeout=8, lang="eng", config=conf)
print(text)

cv2.imshow("Original", imutils.resize(orig, height = 650))

# show the warp with the segmented sections as rectangles on the warped image


cv2.imshow("Warped", imutils.resize(warped, height = 650))
cv2.waitKey(0)
