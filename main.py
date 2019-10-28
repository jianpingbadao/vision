import cv2
import numpy as np
import vehicles
import time
import tkinter as tk, threading
from tkinter import filedialog
import imageio
from PIL import Image, ImageTk
""" # import os  # OS Module for Operating System

##############################################################
win = tk.Tk()
# win.geometry("1000x600")
win.title("New GUI")
win.withdraw()

# Select File
file_path = filedialog.askopenfilename()

print(file_path)

input('press any key to start')

# Placing video in window
# Reference https://stackoverflow.com/questions/36635567/tkinter-inserting-video-into-window
video = imageio.get_reader(file_path)

def stream(label):
    for image in video.iter_data():
        frame_image = ImageTk.PhotoImage(Image.fromarray(image))
        label.config(image = frame_image)
        label.image = frame_image


if( __name__ == "__main__"):
    my_label = tk.Label(win)
    my_label.pack()
    thread = threading.Thread(target = stream, args = (my_label))
    thread.faemon = 1
    thread.start()













word = 'hiu'
def nothing(x):
    global word
    word = x
    print("Track Slider Value: ", x)

cv2.namedWindow('Window')
cv2.createTrackbar('B', 'Window', 0, 255, nothing)
# label_1 = cv2.Label('Window', text = "hioh").pack()

# frame = tk.Frame(win).pack()
# frame_1Area=h*w
# areaTH=frame_1Area/400
##############################################################


#cnt_up is how many cars are going up relative to the highway
#cnt_down is how many cars are going down relative to the highway
cnt_up=0
cnt_down=0

#cap is a variable set to capture whatever video file you set it to(can also be used to capture video from webcam)
#cap=cv2.VideoCapture("surveillance.m4v")
# cap=cv2.VideoCapture("Freewa.mp4")
cap=cv2.VideoCapture(file_path)
print(file_path)

# Save video
# fourcc = cv2.VideoWriter_fourcc(*'XVID')
# out = cv2.VideoWriter('output.avi', fourcc, 20.0, (500x300))





#Get width and height of video
w=cap.get(3)
h=cap.get(4)
frameArea=h*w
areaTH=frameArea/400

#Lines
#Create Lines for video 
line_up=int(3.25*(h/5))
#line_down=int(3*(h/5))
line_down=int(3*(h/5))

#up_limit=int(1*(h/5))
#down_limit=int(4*(h/5))
up_limit=int(2*(h/5))
down_limit=int(4.5*(h/5))

print("Red line y:",str(line_down))
print("Blue line y:",str(line_up))
#Sets line_down_color to red
line_down_color=(255,0,0)
#Sets line_up_color to purple
line_up_color=(255,0,255)

pt1 =  [0, line_down]
pt2 =  [w, line_down]
pts_L1 = np.array([pt1,pt2], np.int32)
pts_L1 = pts_L1.reshape((-1,1,2))
pt3 =  [0, line_up]
pt4 =  [w, line_up]
pts_L2 = np.array([pt3,pt4], np.int32)
pts_L2 = pts_L2.reshape((-1,1,2))

pt5 =  [0, up_limit]
pt6 =  [w, up_limit]
pts_L3 = np.array([pt5,pt6], np.int32)
pts_L3 = pts_L3.reshape((-1,1,2))
pt7 =  [0, down_limit]
pt8 =  [w, down_limit]
pts_L4 = np.array([pt7,pt8], np.int32)
pts_L4 = pts_L4.reshape((-1,1,2))

#Background Subtractor (contains binary image of moving objects)
fgbg=cv2.createBackgroundSubtractorMOG2(detectShadows=True)

#Kernals
kernalOp = np.ones((3,3),np.uint8)
kernalOp2 = np.ones((5,5),np.uint8)
kernalCl = np.ones((11,11),np.uint8)


font = cv2.FONT_HERSHEY_SIMPLEX
cars = []
max_p_age = 5
pid = 1
speed_up = 0.0
speed_down = 0.0
distance = .3
t2 = 0
t1 = 0

# frame = tk.Frame(win)
# label_9 = tk.Label(win, text = "This is a label")
# label_9.place(x =100, y = 100, width = 300)

while(cap.isOpened()):
    ret,frame=cap.read()
    for i in cars:
        i.age_one()
    fgmask=fgbg.apply(frame)
    fgmask2=fgbg.apply(frame)

    if ret==True:

        #Binarization
        ret,imBin=cv2.threshold(fgmask,200,255,cv2.THRESH_BINARY)
        ret,imBin2=cv2.threshold(fgmask2,200,255,cv2.THRESH_BINARY)
        #Opening i.e First Erode the dilate
        mask=cv2.morphologyEx(imBin,cv2.MORPH_OPEN,kernalOp)
        mask2=cv2.morphologyEx(imBin2,cv2.MORPH_CLOSE,kernalOp)

        #Closing i.e First Dilate then Erode
        mask=cv2.morphologyEx(mask,cv2.MORPH_CLOSE,kernalCl)
        mask2=cv2.morphologyEx(mask2,cv2.MORPH_CLOSE,kernalCl)


        #Find Contours
        #Creates rectangles around each vehicle
        _, countours0,hierarchy=cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
        for cnt in countours0:
            area=cv2.contourArea(cnt)
            print(area)
            if area>areaTH:
                ####Tracking######
                m=cv2.moments(cnt)
                cx=int(m['m10']/m['m00'])
                cy=int(m['m01']/m['m00'])
                x,y,w,h=cv2.boundingRect(cnt)

                new=True
                #detect cars in between up_limit down_limit
                if cy in range(up_limit,down_limit):
                    for i in cars:
                        if abs(x - i.getX()) <= w and abs(y - i.getY()) <= h:
                            new = False
                            i.updateCoords(cx, cy)

                            if i.going_UP(line_down,line_up)==True:
                                cnt_up+=1
                                print("ID:",i.getId(),'crossed going up at', time.strftime("%c"))
                                t1 = time.time()
                                # if(distance / abs(t1-t2)*10 < 80):
                                  #  speed_up = distance / abs(t1-t2)*10
                                
                            elif i.going_DOWN(line_down,line_up)==True:
                                cnt_down+=1
                                print("ID:", i.getId(), 'crossed going up at', time.strftime("%c"))
                                t1 = time.time()
                                if(distance / abs(t1-t2)*10 < 80):
                                    speed_down = distance / abs(t1-t2)*10
                                
                            break
                        if i.getState()=='1':
                            if i.getDir()=='down'and i.getY()>down_limit:
                                i.setDone()
                            elif i.getDir()=='up'and i.getY()<up_limit:
                                i.setDone()
                        if i.timedOut():
                            index=cars.index(i)
                            cars.pop(index)
                            del i
                            
                            

                    if new==True: #If nothing is detected,create new
                        p=vehicles.Car(pid,cx,cy,max_p_age)
                        cars.append(p)
                        pid+=1
                        t2 = time.time()


                cv2.circle(frame,(cx,cy),5,(0,0,255),-1)
                # cv2.circle(win,(cx,cy),5,(0,0,255),-1)
                img=cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
                # img=cv2.rectangle(win,(x,y),(x+w,y+h),(0,255,0),2)


        for i in cars:
            cv2.putText(frame, str(i.getId()), (i.getX(), i.getY()), font, 0.3, i.getRGB(), 1, cv2.LINE_AA)



        ############ Frame being built
        str_up='UP: '+str(cnt_up)
        str_down='DOWN: '+str(cnt_down)

        str_al = 'Press q to stop and quit'
        cv2.putText(frame, str_al, (200, 40), font, 0.5, (0, 0, 255), 1, cv2.LINE_AA)


        frame=cv2.polylines(frame,[pts_L1],False,line_down_color,thickness=2)
        frame=cv2.polylines(frame,[pts_L2],False,line_up_color,thickness=2)
        frame=cv2.polylines(frame,[pts_L3],False,(255,255,255),thickness=1)
        frame=cv2.polylines(frame,[pts_L4],False,(255,255,255),thickness=1)
        cv2.putText(frame, str_up, (10, 40), font, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, str_up, (10, 40), font, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
        cv2.putText(frame, str_down, (10, 90), font, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, str_down, (10, 90), font, 0.5, (255, 0, 0), 1, cv2.LINE_AA)
        cv2.putText(frame, 'SPEED_UP: ' + str(speed_up), (100 , 40), font, 0.5, (255,255,255), 2, cv2.LINE_AA)
        cv2.putText(frame, 'SPEED_UP: ' + str(speed_up), (100 , 40), font, 0.5, (0,0,255), 1, cv2.LINE_AA)
        cv2.putText(frame, 'SPEED_DOWN: ' + str(speed_down), (100 , 90), font, 0.5, (255,255,255), 2, cv2.LINE_AA)
        cv2.putText(frame, 'SPEED_DOWN: ' + str(speed_down), (100 , 90), font, 0.5, (255,0,0), 1, cv2.LINE_AA)
        cv2.imshow('Frame',frame)    # Name of frame
        #cv2.namedWindow(win)
        # cv2.imshow(win, frame)
        # frame = tk.Frame(win).pack()

        if cv2.waitKey(1)&0xff==ord('q'): # Press q to quit/ stop 
            break

    else:
        break


cap.release()
win.mainloop()
# out.release()
cv2.destroyAllWindows()
 """

#Set up GUI
window = tk.Tk()  #Makes main window
window.wm_title("Digital Microscope")
window.config(background="#FFFFFF")
window.geometry("800x600")

#Graphics window
imageFrame = tk.Frame(window, width=600, height=500)
imageFrame.grid(row=0, column=0, padx=10, pady=2)

#Capture video frames
lmain = tk.Label(imageFrame)
lmain.grid(row=0, column=0)

# Select File
file_path = filedialog.askopenfilename()

print(file_path)

input('press any key to start')
cap = cv2.VideoCapture(file_path)
# cap = cv2.VideoCapture(0)

def show_frame():
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)

    copy_of_image = img.copy() #
    img = copy_of_image.resize((400,300)) #
    imgtk = ImageTk.PhotoImage(image=img)
    
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(10, show_frame) 




Label_1 = tk.Label(window, text = "where am i", width = 100, height = 50)
Label_1.grid(row = 0, column=600)


#Slider window (slider controls stage position)
# sliderFrame = tk.Frame(window, width=600, height=100)
# sliderFrame.grid(row = 600, column=0, padx=10, pady=2)


show_frame()  #Display 2
window.mainloop()  #Starts GUI






