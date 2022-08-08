#!/usr/bin/env python
# license removed for brevity
import rospy 
from std_msgs.msg import Int16

import cv2
import numpy as np 

cap = cv2.VideoCapture(0)     # open camera 


lHue = 30
UHue = 40
lSat = 120
USat = 255
lVal = 40
UVal = 255
lThresh = 100
uThresh = 200


def get_contour_center(contour):
	M = cv2.moments(contour)
	cx = -1
	cy = -1
	if (M['m00']!=0):
		cx = int(M['m10']/M['m00'])
		cy = int(M['m01']/M['m00'])
        # rospy.loginfo(cx)
        # pub.publish(cx)
        print cx," ",cy
	return cx,cy

def talker():
    pub = rospy.Publisher('chatter',Int16, queue_size=10)
    pub2 = rospy.Publisher('chatter2',Int16, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10) #10hz
    i = 0
    print("Hello1")
	
    while not rospy.is_shutdown():
        # print("Hello2")
        
        _, frame = cap.read()
        frame = cv2.flip(frame, 1)
        if cv2.waitKey(1) & 0xFF == ord('q'):         # wait for the q to be pressed 
            cap.release()
            cv2.destroyAllWindows()
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)                        # convert to hsv
        lower = np.array([lHue, lSat, lVal])
        upper = np.array([UHue, USat, UVal])
        mask2 = cv2.inRange(hsv, lower, upper)                     # doing the mask to on hsv not the frame
        kernel = np.ones((15,15),np.uint8)                                   # 15 15 kernal 
        openMask = cv2.morphologyEx(mask2, cv2.MORPH_OPEN, kernel)            # here doing openning like the slides 
        cv2.imshow('mask2',openMask)
        _, contours, hierarchy = cv2.findContours(openMask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)   # find countors and draw them next line 
        cv2.drawContours(frame, contours, -1, (0,255,0), 3)
        black = np.zeros([frame.shape[0], frame.shape[1], 3], 'uint8')
        maxLength = 5
        minArea = 3500
        cx = 0
        cy = 0

        for c in contours:
			area = cv2.contourArea(c)
			if area > minArea:                        # check area then draw contour 
				areaRatio = area/minArea 
				perimeter = cv2.arcLength(c, True)
				((x,y),radius) = cv2.minEnclosingCircle(c)
				cv2.drawContours(frame, [c], -1, (150,250,150), 1)
				x = (int)(x)
				y = (int)(y)
				cx,cy = get_contour_center(c)
				cv2.circle(frame, (x,y), (int)(radius), (0,0,255), 3)
				cv2.line(black, (x,(int)(y-(maxLength*areaRatio))), (x,(int)(y+(maxLength*areaRatio))), (0, 255, 0), 1)
				cv2.line(black, ((int)(x-(maxLength*areaRatio)),y), ((int)(x+(maxLength*areaRatio)),y), (0, 255, 0), 1)
        can = cv2.Canny(openMask, lThresh, uThresh)                       # doing the canny on openmask
        lower_white = np.array([30,120,40], dtype=np.uint8) #25   35  89
        upper_white = np.array([40,255,255], dtype=np.uint8) #80   180   130
        mask = cv2.inRange(hsv, lower_white, upper_white)
        res = cv2.bitwise_and(frame,frame, mask= mask)
        cv2.imshow('frame',frame)
        cv2.imshow("black", black)         #######
        # cv2.imshow('mask',mask)
        # cv2.imshow('res',res)
        cv2.imshow("Canny", can)
        def on_trackbar(val):
			print val
        cv2.createTrackbar("hazem","mask", 0, 255,on_trackbar)
        k = cv2.waitKey(1) & 0xFF
        if k == 27:
			break


        i += 1

        # hello_str = "x = %d y = %d " % cx % cy
        rospy.loginfo(cx)
        pub.publish(cx)
        rospy.loginfo(cy)
        pub2.publish(cy)
        
        rate.sleep()

    cv2.destroyAllWindows()

if __name__=='__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass

