import cv2
import numpy as np
import vehicles
import time
import os

debug = True

#variables to create color histograms
h_bins = 50
s_bins = 60
histSize = [h_bins, s_bins]

h_ranges = [0, 180]
s_ranges = [0, 256]
ranges = h_ranges + s_ranges

channels = [0, 1]

def execute(directory, file_n, result_n, up_dwn, lines=None):
    """ 
        purpose: it counts cars going up
        and down based on parameters. When it is run it analyzes the video,
        and produces a txt file in the end showing what times the cars 
        passed the intersection. It also includes information about the total
        cars going up and down.

        parameters
        ----------
        directory: string,
            The directory that contains the video and the result

        file_n: type = String, optimal: must be a video type that cv2.VideoCaputure accepts

        result_n: type = String, optimal: file should not exist, otherwise it overwrites the file

        up_dwn: type = Integer, optimal: 0 = count cars going down, 1 = count cars going up, 2 = count cars going both up and down

        lines : list,
                The lines that are used to determine the moving direction of the vehicles in the video.
                Each element of the list is a dictionary, of which,
                Key is the moving direction, i.e., up or down;
                Values are three lines, and each line consists of 4 numbers (relative, range is [0, 1]), i.e., x_left, y_left, x_right, y_right

        returns
        ----------
        none
    """
    if debug:
        if lines:
            for direction_and_line in lines:
                print(direction_and_line['direction'])
                for line in direction_and_line['lines']:
                    print(line)

    os.chdir(directory)
    file_name = file_n
    result_name = result_n
    up_down = up_dwn

    # cnt_up is how many cars are going up relative to the highway
    # cnt_down is how many cars are going down relative to the highway
    cnt_up = 0
    cnt_down = 0

    #store contours
    contour_image = []

    cap = cv2.VideoCapture(file_name)

    # Find OpenCV version
    major_ver, minor_ver, subminor_ver = (cv2.__version__).split('.')
    if int(major_ver) < 3:
        fps = cap.get(cv2.cv.CV_CAP_PROP_FPS)
        print("Frames per second using video.get(cv2.cv.CV_CAP_PROP_FPS): {0}".format(fps))
    else :
        fps = cap.get(cv2.CAP_PROP_FPS)
        print("Frames per second using video.get(cv2.CAP_PROP_FPS) : {0}".format(fps))

    # Get width and height of video
    w = cap.get(3)
    h = cap.get(4)
    frameArea = h * w
    areaTH = frameArea / 400  # the area threshold (minimum) for each single vehicle in the video;
    # TODO: should be adjustable for different camera

    if lines:
        line_downs = []
        line_ups = []
        for direction_and_line in lines:
            all_lines = direction_and_line['lines']
            if direction_and_line['direction'] == 'down':
                line_downs.append(all_lines)
            else:
                line_ups.append(all_lines)

        # TODO: For now just take the first one
        if line_ups:
            line_up = int(line_ups[0][1][1] * h)
        else:
            line_up = int(line_downs[0][1][1] * h)
        line_down = int(line_downs[0][1][1] * h)

        up_limit = int(line_downs[0][0][1] * h)
        down_limit = int(line_downs[0][2][1] * h)

        pts_L1 = np.array([[int(line_downs[0][1][0] * w), int(line_downs[0][1][1] * h)],
                        [int(line_downs[0][1][2] * w), int(line_downs[0][1][3] * h)]]).reshape((-1, 1, 2)) # line down
        pts_L2 = pts_L1 # line up # TODO
        pts_L3 = np.array([[int(line_downs[0][0][0] * w), int(line_downs[0][0][1] * h)],
                        [int(line_downs[0][0][2] * w), int(line_downs[0][0][3] * h)]]).reshape((-1, 1, 2)) # up limit
        pts_L4 = np.array([[int(line_downs[0][2][0] * w), int(line_downs[0][2][1] * h)],
                        [int(line_downs[0][2][2] * w), int(line_downs[0][2][3] * h)]]).reshape((-1, 1, 2)) # down limit
    else:
        # Lines
        # Create Lines for video
        if file_name == "test.mov":
            line_up = int(2.5 * (h / 5))
            line_down = int(4 * (h / 5))
        elif file_name == "test2.mov":
            line_up = int(2.5 * (h / 5))
            line_down = int(4 * (h / 5))
        elif file_name == "test3.mov":
            line_up = int(2.5 * (h / 5))
            line_down = int(4 * (h / 5))
        elif file_name == "surveillance.m4v":
            line_up = int(2.5 * (h / 5))
            line_down = int(3 * (h / 5))
        else:
            line_up = int(3.25 * (h / 5))
            line_down = int(3 * (h / 5))

        up_limit = int(2 * (h / 5))
        down_limit = int(4.5 * (h / 5))

        pt1 = [0, line_down]
        pt2 = [w, line_down]
        pts_L1 = np.array([pt1, pt2], np.int32)
        pts_L1 = pts_L1.reshape((-1, 1, 2))
        pt3 = [0, line_up]
        pt4 = [w, line_up]
        pts_L2 = np.array([pt3, pt4], np.int32)
        pts_L2 = pts_L2.reshape((-1, 1, 2))

        pt5 = [0, up_limit]
        pt6 = [w, up_limit]
        pts_L3 = np.array([pt5, pt6], np.int32)
        pts_L3 = pts_L3.reshape((-1, 1, 2))
        pt7 = [0, down_limit]
        pt8 = [w, down_limit]
        pts_L4 = np.array([pt7, pt8], np.int32)
        pts_L4 = pts_L4.reshape((-1, 1, 2))

    print("Red line y: ", str(line_down))
    print("Blue line y: ", str(line_up))
    # Sets line_down_color to red
    line_down_color = (255, 0, 0)
    # Sets line_up_color to purple
    line_up_color = (255, 0, 255)

    # Background Subtractor (contains binary image of moving objects)
    fgbg = cv2.createBackgroundSubtractorMOG2(detectShadows=True)

    # Kernals
    kernalOp = np.ones((3, 3), np.uint8)
    kernalCl = np.ones((11, 11), np.uint8)

    font = cv2.FONT_HERSHEY_SIMPLEX
    cars = []
    max_p_age = 5
    car_id = 1
    speed_up = 0.0
    speed_down = 0.0
    distance = .5
    t2 = 0
    t1 = 0
    contents = []

    while cap.isOpened():
        read_success, frame = cap.read()
        last_frame_time = time.time()

        for i in cars:
            i.age_one()
        fgmask = fgbg.apply(frame)

        if read_success == True:

            # Binarization
            _, imBin = cv2.threshold(fgmask, 200, 255, cv2.THRESH_BINARY)

            # Opening i.e First Erode the dilate
            mask = cv2.morphologyEx(imBin, cv2.MORPH_OPEN, kernalOp)

            # Closing i.e First Dilate then Erode
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernalCl)

            # Find Contours
            # Creates rectangles around each vehicle
            countours0, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            for cnt in countours0:
                area = cv2.contourArea(cnt)
                # print(f"Detected area size: {area}")
                if area > areaTH:
                    ####Tracking######
                    m = cv2.moments(cnt)
                    if m['m00'] == 0:
                        # generally this should not happen since the area is already larger than threshold.
                        # Just in case of a bad threshold
                        continue
                    cx = int(m['m10'] / m['m00'])  # Centroid, https://www.learnopencv.com/find-center-of-blob-centroid-using-opencv-cpp-python/
                    cy = int(m['m01'] / m['m00'])
                    x, y, w, h = cv2.boundingRect(cnt)

                    new = True
                    # detect cars in between up_limit and down_limit
                    if cy in range(up_limit, down_limit):
                        for i in cars:
                            # TODO: this may not hold for all cases
                            # e.g. if the frame rate is too low,
                            # then the same car in consecutive frames will be far away from each other
                            if abs(x - i.getX()) <= w and abs(y - i.getY()) <= h:
                                new = False
                                i.updateCoords(cx, cy)

                                if i.going_UP(line_up):
                                    cnt_up += 1
                                    content = "ID: " + str(i.getId()) + ' crossed going up at ' + time.strftime("%c")
                                    contents.append(content)
                                    print(content)
                                    t1 = time.time()
                                    if distance / abs(t1 - t2) * 10 < 80:
                                        speed_up = distance / abs(t1 - t2) * 10

                                elif i.going_DOWN(line_down):
                                    cnt_down += 1
                                    content = "ID: " + str(i.getId()) + ' crossed going down at ' + time.strftime("%c")
                                    contents.append(content)
                                    print(content)
                                    t1 = time.time()
                                    if distance / abs(t1 - t2) * 10 < 80:
                                        speed_down = distance / abs(t1 - t2) * 10

                                break
                            if i.getState() == '1':
                                if i.getDir() == 'down' and i.getY() > down_limit:
                                    i.setDone()
                                elif i.getDir() == 'up' and i.getY() < up_limit:
                                    i.setDone()
                            if i.timedOut():
                                index = cars.index(i)
                                cars.pop(index)
                                del i

                        if new:  # If nothing is detected, create new
                            p = vehicles.Car(car_id, cx, cy, max_p_age)
                            cars.append(p)
                            car_id += 1
                            t2 = time.time()

                    cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
                    img = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    contour_image.append(createHistogram(img))

            for i in cars:
                cv2.putText(frame, str(i.getId()), (i.getX(), i.getY()), font, 0.3, i.getRGB(), 1, cv2.LINE_AA)

            str_up = 'UP: ' + str(cnt_up)
            str_down = 'DOWN: ' + str(cnt_down)

            frame = cv2.polylines(frame, [pts_L3], False, (255, 255, 255), thickness=1)
            frame = cv2.polylines(frame, [pts_L4], False, (255, 255, 255), thickness=1)

            if up_down == 0:
                frame = cv2.polylines(frame, [pts_L1], False, line_down_color, thickness=2)
                cv2.putText(frame, 'SPEED_DOWN: ' + str(speed_down), (100, 40), font, 0.5, (255, 255, 255), 2,
                            cv2.LINE_AA)
                cv2.putText(frame, 'SPEED_DOWN: ' + str(speed_down), (100, 40), font, 0.5, (255, 0, 0), 1, cv2.LINE_AA)
                cv2.putText(frame, str_down, (10, 40), font, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
                cv2.putText(frame, str_down, (10, 40), font, 0.5, (255, 0, 0), 1, cv2.LINE_AA)
            elif up_down == 1:
                frame = cv2.polylines(frame, [pts_L2], False, line_up_color, thickness=2)
                cv2.putText(frame, str_up, (10, 40), font, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
                cv2.putText(frame, str_up, (10, 40), font, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
                cv2.putText(frame, 'SPEED_UP: ' + str(speed_up), (100, 40), font, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
                cv2.putText(frame, 'SPEED_UP: ' + str(speed_up), (100, 40), font, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
            elif up_down == 2:
                frame = cv2.polylines(frame, [pts_L2], False, line_up_color, thickness=2)
                frame = cv2.polylines(frame, [pts_L1], False, line_down_color, thickness=2)
                cv2.putText(frame, str_up, (10, 40), font, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
                cv2.putText(frame, str_up, (10, 40), font, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
                cv2.putText(frame, 'SPEED_UP: ' + str(speed_up), (100, 40), font, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
                cv2.putText(frame, 'SPEED_UP: ' + str(speed_up), (100, 40), font, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
                cv2.putText(frame, 'SPEED_DOWN: ' + str(speed_down), (100, 90), font, 0.5, (255, 255, 255), 2,
                            cv2.LINE_AA)
                cv2.putText(frame, 'SPEED_DOWN: ' + str(speed_down), (100, 90), font, 0.5, (255, 0, 0), 1, cv2.LINE_AA)
                cv2.putText(frame, str_down, (10, 90), font, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
                cv2.putText(frame, str_down, (10, 90), font, 0.5, (255, 0, 0), 1, cv2.LINE_AA)

            cv2.imshow('Frame', frame)

            if cv2.waitKey(1) & 0xff == ord('q'):
                break

            cur_time = time.time()
            while cur_time - last_frame_time < 1 / fps:
                time.sleep(0.001)
                cur_time = time.time()
        else:
            # video/stream open failed
            break

    with open(result_name, 'w') as f:
        for item in contents:
            f.write(item + '\n')
        f.write("Count going up: " + str_up + "\n")
        f.write("Count going down: " + str_down + "\n")

    open(result_name)
    cap.release()
    cv2.destroyAllWindows()

    return cnt_up, cnt_down

#make sure img is imread, create color histogram
def createHistogram(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hist_test1 = cv2.calcHist([hsv], channels, None, histSize, ranges, accumulate=False)
    cv2.normalize(hist_test1, hist_test1, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)
    
def compareHist(hist1, hist2):
    cv2.compareHist(hist1, hist2, 0)