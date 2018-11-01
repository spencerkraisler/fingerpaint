import cv2

def getContours(mask):
	_, contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	return contours

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
# buggy shit

THRESH_RECT_AREA = 4000

def getRectangles(contours):
	rectangles = []
	for cnt in contours:
		x, y, w, h = cv2.boundingRect(cnt)
		if w * h > THRESH_RECT_AREA:
			rectangles.append((x, y, w, h))
	# rectangles = handleRectangles(rectangles)
	return rectangles
"""
def handleRectangles(rectangles):
	output = []
	for rct1 in rectangles:
		for rct2 in rectangles:
			if rct1 != rct2:
				if (rct1[0] not in range(rct2[0], rct2[0] + rct2[2])) or (rct1[1] not in range(rct2[1], rct2[1] + rct2[3])):
					output.append(rct1)
	return output
"""

def drawRectangles(img, rectangles):
	for rct in rectangles:
		x, y, w, h = rct
		cv2.rectangle(img,(x,y),(x+w,y+h),(255,255,255), 2)


def getHullDefects(contours):
	defects = []
	for cnt in contours:
		hull = cv2.convexHull(cnt, returnPoints=False)
		defects.append(cv2.convexityDefects(cnt, hull))
	return defects


def drawConvexHulls(img, contours, hulls):
	for i in range(len(contours)):
		cnt = contours[i]
		hull = hulls[i]
		for i in range(hull.shape[0]):
			s,e,f,d = hull[i,0]
			start = tuple(cnt[s][0])
			end = tuple(cnt[e][0])
			far = tuple(cnt[f][0])
			cv2.line(img, start,end,[0,255,0],2)
			cv2.circle(img,far,5,[0,0,255],-1)
