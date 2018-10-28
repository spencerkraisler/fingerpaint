import cv2
import matplotlib
import matplotlib.pyplot as plt 
import numpy as np 
from contours import handleContours


def getHistogram(img):
	lab_img = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
	hist = cv2.calcHist([lab_img], [1, 2], None, 
		 				[15, 15], [0, 255, 0, 255])
	cv2.normalize(hist, hist, 0, 255, cv2.NORM_MINMAX)
	#hist = dilate(hist, DILATION_KERNEL_SIZE)
	return hist

def mask(hist, img):
	img = cv2.blur(img, (5, 5))
	mask = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
	mask = cv2.calcBackProject([mask], [1, 2], hist, [0, 255, 0, 255], 1)
	#mask = denoise(mask)
	#mask = cv2.blur(mask, (5,5))
	return mask

def getContours(mask):
	_, contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	return contours

def getHullDefects(contours):
	defects = []
	for cnt in contours:
		hull = cv2.convexHull(cnt, returnPoints=False)
		defects.append(cv2.convexityDefects(cnt, hull))
	return defects

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
		for cnt in contours:
			hull = cv2.convexHull(cnt,returnPoints = False)
			defects = cv2.convexityDefects(cnt,hull)
			for i in range(defects.shape[0]):
				s,e,f,d = defects[i,0]
				start = tuple(cnt[s][0])
				end = tuple(cnt[e][0])
				far = tuple(cnt[f][0])
				cv2.line(frame, start,end,[0,255,0],2)
				cv2.circle(frame,far,5,[0,0,255],-1)
		#cv2.drawContours(frame, contours, -1, (0,255,0), 2)


		cv2.imshow('frame', frame)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
	cap.release()
	cv2.destroyAllWindows()


roi_img = cv2.imread('./images/hand2_roi.jpg', 3)
roi_hist = getHistogram(roi_img)

startVideoFeed(0)
