import cv2
import numpy as np 

cap = cv2.VideoCapture(0)     # open camera 

lHue = 75                     # basic values 
UHue = 90 
lSat = 60
USat = 180
lVal = 0
UVal = 255
lThresh = 100
uThresh = 200


def set_tiffany_blue_tracker():          # these are the valus for the cup 
	global lHue                     # this means that there is this global var that i want not to just call but also edit
	global UHue
	global lSat
	global USat
	global lVal
	global UVal
	lHue = 75
	UHue = 90 
	lSat = 60
	USat = 180
	lVal = 0
	UVal = 255
	lThresh = 100
	uThresh = 200
	
def set_canary_yellow_tracker():
	global lHue
	global UHue
	global lSat
	global USat
	global lVal
	global UVal
	lHue = 30
	UHue = 40
	lSat = 120
	USat = 255
	lVal = 40
	UVal = 255
	lThresh = 100
	uThresh = 200

def hsvThresh(val):
	global lHue
	global UHue
	global lSat
	global USat
	global lVal
	global UVal
	lHue = cv2.getTrackbarPos('lHue','Original')
	UHue = cv2.getTrackbarPos('UHue','Original')
	lSat = cv2.getTrackbarPos('LSat','Original')
	USat = cv2.getTrackbarPos('USat','Original')
	lVal = cv2.getTrackbarPos('LVal','Original')
	UVal = cv2.getTrackbarPos('UVal','Original')

def cannyThresh(val):
	global lThresh
	global uThresh
	lThresh = cv2.getTrackbarPos('lThresh','Canny')
	uThresh = cv2.getTrackbarPos('uThresh','Canny')

def perform_threshold(frame):                         # perform threshold function. setting lower and upper bounds 
	lower = np.array([lHue, lSat, lVal])
	upper = np.array([UHue, USat, UVal])
	f = cv2.inRange(frame, lower, upper)
	return f                                          # return final mask 

def perform_canny(frame):
	global lThresh
	global uThresh
	f = cv2.Canny(frame, lThresh, uThresh)
	return f

def read_frame():                         # read frame function 
	ret, frame = cap.read()
	frame = cv2.flip(frame, 1)
	return frame

def setColor(val):
	if (val == 0):
		set_canary_yellow_tracker()
	else:
		set_tiffany_blue_tracker()

def create_trackbars(isTrackbarCreated, isTestingPhase):
	if (isTrackbarCreated):
		return
	else:
		if (isTestingPhase):
			cv2.isTrackbarCreated('LHue','Original',0,360,hsvThresh)
			cv2.isTrackbarCreated('UHue','Original',0,360,hsvThresh)
			cv2.isTrackbarCreated('LSat','Original',0,255,hsvThresh)
			cv2.isTrackbarCreated('USat','Original',0,255,hsvThresh)
			cv2.isTrackbarCreated('LVal','Original',0,255,hsvThresh)
			cv2.isTrackbarCreated('UVal','Original',0,255,hsvThresh)
			cv2.isTrackbarCreated('lThresh','Canny',0,255,cannyThresh)
			cv2.isTrackbarCreated('UThresh','Canny',0,255,cannyThresh)
		else:
			cv2.createTrackbar('Canary Yellow (0) or Tiffany Blue (1)','Original',0,1,setColor)
		isTrackbarCreated = True

def show_frame(name, frame):
	f = cv2.imshow(name,frame)
	return f

def nothing(x):
	pass

def get_contour_center(contour):
	M = cv2.moments(contour)
	cx = -1
	cy = -1
	if (M['m00']!=0):
		cx = int(M['m10']/M['m00'])
		cy = int(M['m01']/M['m00'])
	return cx,cy

if __name__=="__main__":                  # start from the main here 
	print("Hello")
	isTrackbarCreated = False
	#set_tiffany_blue_tracker()
	#set_canary_yellow_tracker()
	while(True):
		img = read_frame()                            # read the frame 
		if cv2.waitKey(1) & 0xFF == ord('q'):         # wait for the q to be pressed 
			cap.release()
			cv2.destroyAllWindows()
		hsvFrame = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)                       # convert to hsv 
		hsvFrame = cv2.GaussianBlur(hsvFrame, (15,15),cv2.BORDER_DEFAULT)    # do guissan blur here make it softer
		# show_frame("Blurred",hsvFrame)                                       # blur the same hsv frame we working on
		mask = perform_threshold(hsvFrame)                                   # make mask , do perform threshold function 
		kernel = np.ones((15,15),np.uint8)                                   # 15 15 kernal 
		openMask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)            # here doing openning like the slides 
		show_frame("Mask", openMask)
		_, contours, hierarchy = cv2.findContours(openMask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)   # find countors and draw them next line 
		cv2.drawContours(img, contours, -1, (0,255,0), 3)
		black = np.zeros([img.shape[0], img.shape[1], 3], 'uint8')
		maxLength = 5
		minArea = 3500
		for c in contours:
			area = cv2.contourArea(c)
			if area > minArea:                        # check area then draw contour 
				areaRatio = area/minArea 
				perimeter = cv2.arcLength(c, True)
				((x,y),radius) = cv2.minEnclosingCircle(c)
				cv2.drawContours(img, [c], -1, (150,250,150), 1)
				x = (int)(x)
				y = (int)(y)
				cx,cy = get_contour_center(c)
				cv2.circle(img, (x,y), (int)(radius), (0,0,255), 3)
				cv2.line(black, (x,(int)(y-(maxLength*areaRatio))), (x,(int)(y+(maxLength*areaRatio))), (0, 255, 0), 1)
				cv2.line(black, ((int)(x-(maxLength*areaRatio)),y), ((int)(x+(maxLength*areaRatio)),y), (0, 255, 0), 1)
		can = perform_canny(openMask)
		#band = cv2.bitwise_and(img, img, mask = openMask)
		frame = show_frame("Original",img)
		show_frame("black", black)
		canf = show_frame("Canny", can)
		isTestingPhase = False                                      # change here from false 
		create_trackbars(isTrackbarCreated, isTestingPhase)
		isTrackbarCreated = True

		# perfect code working
		# For testing color does not work
