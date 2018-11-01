import cv2
import numpy as np 
from backproj import mask, getHistogram
from shapeDetection import getContours, handleContours, getRectangles, drawRectangles

def startVideoFeed(cam_index, hist=None):

	# Args:
		# cam_index (int): 0 for webcam; 1 for USB camera
		# hist (numpy array): histogram for masking
	cap = cv2.VideoCapture(cam_index)
	while(True):
		ret, frame = cap.read()
		thresh_frame = mask(roi_hist, frame)
		contours = getContours(thresh_frame)
		contours = handleContours(contours)
		rects = getRectangles(contours)
		drawRectangles(thresh_frame, rects)
		cv2.imshow('frame', thresh_frame)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
	cap.release()
	cv2.destroyAllWindows()


roi_img = cv2.imread('./images/hand_roi.jpg', 3)
roi_hist = getHistogram(roi_img)

startVideoFeed(0)
