
# coding: utf-8

# In[15]:


import cv2   
import numpy as np

def main():
    cap=cv2.VideoCapture(0)
    
    filename = 'C:\\Users\\Francis Xavier\\AppData\\Local\\Programs\\Python\\Python36-32\\Scripts\\Internship work\\Week 2\\Output\\Output.mp4'
    codec = cv2.VideoWriter_fourcc('X', 'V', 'I', 'D') #Fourcc: Four character code eg DIVX,XVID,H264
    framerate = 20
    resolution = (640, 480)
    
    VideoFileOutput = cv2.VideoWriter(filename, codec, framerate, resolution)
    
    if cap.isOpened():
        ret, frame = cap.read()
    else:
        ret = False
    
    ret, frame = cap.read()

    while(ret):
        ret, frame = cap.read()
        
        #For removing noise values
        blur = cv2.GaussianBlur(frame, (5, 5), -2)
        ret, th = cv2.threshold( blur, 20, 255, cv2.THRESH_BINARY)
        dilated = cv2.dilate(th, np.ones((3, 3), np.uint8), iterations=1 )
        eroded = cv2.erode(dilated, np.ones((3, 3), np.uint8), iterations=2 )
        
        hsv=cv2.cvtColor(blur,cv2.COLOR_BGR2HSV) #converting frame img(BGR) to HSV (hue-saturation-value)
        
        #defining the range of red color
        red_lower=np.array([140, 150, 0],np.uint8)
        red_upper=np.array([180,255,255],np.uint8)

        #defining the Range of Blue color
        blue_lower=np.array([100, 50, 50],np.uint8)
        blue_upper=np.array([140, 255,255],np.uint8)

        #defining the Range of yellow color
        yellow_lower=np.array([22,60,200],np.uint8)
        yellow_upper=np.array([60,255,255],np.uint8)

        #finding the range of red,blue and yellow color in the image
        red=cv2.inRange(hsv, red_lower, red_upper)
        blue=cv2.inRange(hsv,blue_lower,blue_upper)
        yellow=cv2.inRange(hsv,yellow_lower,yellow_upper)
        
        red=cv2.dilate(red, np.ones((5,5), "uint8"),iterations=1)
        res=cv2.bitwise_and(frame,frame, mask = red)

        blue=cv2.dilate(blue,np.ones((5,5), "uint8"),iterations=1)
        res1=cv2.bitwise_and(frame,frame, mask = blue)

        yellow=cv2.dilate(yellow,np.ones((5,5), "uint8"),iterations=1)
        res2=cv2.bitwise_and(frame,frame, mask = yellow)    
        
        #Tracking the Red Color
        (_,contours,hierarchy)=cv2.findContours(red,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        for  pic,contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if(area>5000): 
                (x,y),radius = cv2.minEnclosingCircle(contour)
                center = (int(x),int(y))
                radius = int(radius)
                #cv2.drawContours(frame,contours, -1, (0, 0, 255),2) #Gives outline over shape of object (records noise too)
                cv2.circle(frame,center,radius,(0,0,255),2)
                cv2.putText(frame,"RED color",center,cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,0,255))

        #Tracking the Blue Color
        (_,contours,hierarchy)=cv2.findContours(blue,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if(area>10000):
                (x,y),radius = cv2.minEnclosingCircle(contour)
                center = (int(x),int(y))
                radius = int(radius)
                #cv2.drawContours(frame, contours, -1, (255,0,0), 2)
                cv2.circle(frame,center,radius,(255,0,0),2)
                cv2.putText(frame,"Blue color",center,cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,0,0))

        #Tracking the yellow Color
        (_,contours,hierarchy)=cv2.findContours(yellow,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if(area>500):
                (x,y),radius = cv2.minEnclosingCircle(contour)
                center = (int(x),int(y))
                radius = int(radius)
                #cv2.drawContours(frame,contours, -1, (48, 225, 240), 2)
                cv2.circle(frame,center,radius,(48,225,240),2)
                cv2.putText(frame,"Yellow  color",center,cv2.FONT_HERSHEY_SIMPLEX, 1.0, (48,225,240))  

        VideoFileOutput.write(frame) #Writing current frame to a file
        cv2.imshow("Color Tracking",frame)
        if cv2.waitKey(1) ==27: #Esc key pressed
            cap.release()
            cv2.destroyAllWindows()
            break  
if __name__ == "__main__":
    main()

