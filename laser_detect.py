import cv2
import numpy as np
import argparse
import imutils
from collections import deque
import pdb
import time
current_milli_time = lambda: int(round(time.time() * 1000))



cap = cv2.VideoCapture(0)

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
	help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=256,
	help="max buffer size")
args = vars(ap.parse_args())

pts = deque(maxlen=args["buffer"])

lower_red = np.array([0, 0, 255])
upper_red = np.array([50, 255, 255])

lastInsertedTime = None

#CONSTANTS
TIME_THRESHOLD = 1000

while (1):
	pdb.set_trace()
	# Take each frame
	ret, frame = cap.read()
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	mask = cv2.inRange(hsv, lower_red, upper_red)

	(minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(mask)

	#This is to show the video window and draws a circle around the current position
	print('why not work')
	cv2.circle(frame, maxLoc, 20, (0, 0, 255), 2, cv2.LINE_AA)
	cv2.imshow('Track Laser', frame)

	if(maxLoc is not None):
		#print(frame[maxLoc[1], maxLoc[0]])
		#print('maxLoc', maxLoc[0], maxLoc[1])

		if(maxLoc == (0,0)):
			if lastInsertedTime is None:
				print('here1')
				continue
			elif(current_milli_time() - lastInsertedTime < TIME_THRESHOLD):
				print('here2')
				continue
			elif(len(pts) > 0):
				#logic
				print('here3')
				xIncreasing = 0
				yIncreasing = 0
				xDecreasing = 0
				yDecreasing = 0
				offset = 2
				threshold = 0.6
				for k in range(1, len(pts) - 2):
					print('ptsss', pts[k])
					# print(str(pts[k-1]) + ' -- ' + str(pts[k+1]))
					#print(pts[k-1], '---------------- ', pts[k + 1])
					if pts[k-offset] is None or pts[k + offset] is None:
						print('continue')
						continue
					xOld = pts[k-offset][0]
					xNew = pts[k + offset][0]
					yOld = pts[k-offset][1]
					yNew = pts[k + offset][1]

					if xOld > xNew:
						xIncreasing += 1
					elif xOld < xNew:
						xDecreasing += 1
					if yOld > yNew:
						yIncreasing += 1
					elif yOld < yNew:
						yDecreasing += 1

				print('here5')
				horizontal = max(xIncreasing, xDecreasing)
				vertical = max(yIncreasing, yDecreasing)


				if horizontal > vertical:
					print('xIncreasing'+'-----'+str(xIncreasing/len(pts)))
					print('xDecreasing'+'-----'+str(xDecreasing/len(pts)))
					# horizontal gesture1
					if(xIncreasing/len(pts) > threshold):
						print("Left")
					elif(xDecreasing/len(pts) > threshold):
						print("Right")
				elif vertical > horizontal:
					print('yIncreasing'+'-----'+str(yIncreasing/len(pts)))
					print('yDecreasing'+'-----'+str(yDecreasing/len(pts)))
					if(yIncreasing/len(pts) > threshold):
						print("Down")
					elif(yDecreasing/len(pts) > threshold):
						print("UP")

				pts.clear()
				continue
			else:
				continue

		pts.appendleft(maxLoc)
		lastInsertedTime = current_milli_time()
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

cap.release()
cv2.destroyAllWindows()
