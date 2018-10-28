import cv2
import numpy as np 

THRESH_CONTOUR_AREA = 2000

def threshold_area(contours):
	out_contours = []
	for cnt in contours:
		if cv2.contourArea(cnt) >= THRESH_CONTOUR_AREA:
			out_contours.append(cnt)
	return out_contours

def handleContours(contours):
	contours = threshold_area(contours)
	return contours