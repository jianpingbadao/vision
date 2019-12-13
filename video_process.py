import cv2
import numpy as np
import vehicles
import time
import os
from typing import List

from utils import Hexagon, Point

debug = True

def video_process(video_file: str, result_file: str, lines: List) -> None:
    """
    Process video and count the number of vehicles passing by

    Parameters
    ----------
    video_file : str,
        The abosulte path of the video file to be processed.
    result_file : str,
        The result file
    lines : List,
        The lines that are used to determine the moving direction of the vehicles in the video.
        Each element of the list is a dictionary, of which,
        Key is the moving direction, i.e., up or down;
        Values are three lines, and each line consists of 4 numbers (relative to width or height, range is [0, 1]),
        i.e., x_left, y_left, x_right, y_right
    """
    if debug:
        if lines:
            for direction_and_line in lines:
                print(direction_and_line['direction'])
                for line in direction_and_line['lines']:
                    print(line)

    cap = cv2.VideoCapture(video_file)

    # Find OpenCV version
    major_ver, _, _ = (cv2.__version__).split('.')
    if int(major_ver) < 3:
        fps = cap.get(cv2.cv.CV_CAP_PROP_FPS)
        if debug:
            print("Frames per second using video.get(cv2.cv.CV_CAP_PROP_FPS): {0}".format(fps))
    else:
        fps = cap.get(cv2.CAP_PROP_FPS)
        if debug:
            print("Frames per second using video.get(cv2.CAP_PROP_FPS) : {0}".format(fps))

    # Get width and height of video
    width = cap.get(3)
    height = cap.get(4)
    frame_area = height * width
    area_threshold = frame_area / 450  # the area threshold (minimum) for each single vehicle in the video;
    # TODO: should be adjustable for different camera
    # one option is to get the width of the lane
    # then use that as the baseline

    fast_play = 1.0  # TODO: adjust the process speed

    # construct Hexagon area using the passed/picked up lines
    hexagons = []
    for direction_and_line in lines:
        direction = direction_and_line['direction']
        one_group_lines = direction_and_line['lines']

        # change the number in lines from ratio to actual values
        # based on the width and height of the window
        new_group_lines = []
        for line in one_group_lines:
            new_line = [int(num * width) if idx % 2 == 0 else int(num * height) for idx, num in enumerate(line)]
            new_group_lines.append(new_line)
        hexagon = Hexagon(new_group_lines, direction)
        hexagons.append(hexagon)
    all_counts = [0] * len(lines)
    all_cars = [[] for _ in range(len(lines))]  # the Car in each hexagon

    # Background Subtractor (contains binary image of moving objects)
    background_subtractor = cv2.createBackgroundSubtractorMOG2(detectShadows=True)

    # Kernals
    kernalOp = np.ones((3, 3))
    kernalCl = np.ones((11, 11))

    font = cv2.FONT_HERSHEY_SIMPLEX
    max_car_age = 6
    car_id = 1

    while cap.isOpened():
        read_success, frame = cap.read()
        last_frame_time = time.time()

        for cars in all_cars:
            for car in cars:
                car.age_one()

        all_cars = [[car for car in cars if not car.timedOut()] for cars in all_cars]

        masked_frame = background_subtractor.apply(frame)

        if read_success == True:

            # Binarization
            _, imBin = cv2.threshold(masked_frame, 200, 255, cv2.THRESH_BINARY)

            # Opening i.e First Erode the dilate
            mask = cv2.morphologyEx(imBin, cv2.MORPH_OPEN, kernalOp)

            # Closing i.e First Dilate then Erode
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernalCl)

            # Find Contours
            # Creates rectangles around each vehicle
            countours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            for countour in countours:
                countour_area = cv2.contourArea(countour)
                # print(f"Detected area size: {countour_area}")
                if countour_area > area_threshold:
                    ####Tracking######
                    m = cv2.moments(countour)
                    if m['m00'] == 0:
                        # normally this should not happen since the area is already larger than threshold.
                        # Just in case of a bad threshold
                        continue
                    cx = int(m['m10'] / m['m00'])  # Centroid, https://www.learnopencv.com/find-center-of-blob-centroid-using-opencv-cpp-python/
                    cy = int(m['m01'] / m['m00'])
                    x, y, w, h = cv2.boundingRect(countour)

                    existing_car = False
                    car_area_id = -1
                    in_interested_area = False
                    centroid_point = Point(cx, cy)
                    for idx, hexagon in enumerate(hexagons):
                        if not hexagon.inside(centroid_point):
                            continue

                        in_interested_area = True
                        for car in all_cars[idx]:
                            # the countour has match with an existing/previous car
                            # TODO: this may not hold for all cases
                            # e.g. if the frame rate is too low,
                            # then the same car in consecutive frames will be far away from each other
                            if abs(cx - car.getX()) <= w and abs(cy - car.getY()) <= h:
                                existing_car = True
                                car.updateCoords(cx, cy)

                                mid_line = (hexagon.lines[1].point1.y + hexagon.lines[1].point2.y) / 2

                                count_it = False
                                if hexagon.direction == 'up' and car.going_UP(mid_line):
                                    count_it = True
                                elif hexagon.direction == 'down' and car.going_DOWN(mid_line):
                                    count_it = True

                                if count_it:
                                    all_counts[idx] += 1

                                break

                        car_area_id = idx
                        # always break here, since one point can only be in one area
                        break

                    if in_interested_area:
                        if not existing_car:
                            new_car = vehicles.Car(car_id, cx, cy, max_car_age)
                            all_cars[car_area_id].append(new_car)
                            car_id += 1

                        cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    else:
                        cv2.circle(frame, (cx, cy), 5, (0, 255, 255), -1)
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)
                else:
                    # countours with smaller area
                    pass
            ## The end of processing countours in current frame

            for cars in all_cars:
                for car in cars:
                    cv2.putText(frame, str(car.getId()), (car.getX(), car.getY()),
                            font, 0.3, car.getRGB(), 1, cv2.LINE_AA)

            start_y = 40
            delta_y = 50
            for idx, hexagon in enumerate(hexagons):
                for line in hexagon.lines:
                    _line = np.array(line.as_list_of_points(), dtype=np.int32).reshape((-1, 1, 2))
                    # pdb.set_trace()
                    frame = cv2.polylines(frame, [_line], False, (255, 255, 255), 1)

                count_str = hexagon.direction + ": " + str(all_counts[idx])
                cv2.putText(frame, count_str, (10, start_y + delta_y * idx), font, 0.5, (255, 0, 0), 2, cv2.LINE_AA)

            cv2.imshow('Vehicle Counting In Progress (Press q to quit)', frame)

            if cv2.waitKey(1) & 0xff == ord('q'):
                break

            cur_time = time.time()
            while cur_time - last_frame_time < fast_play / fps:
                time.sleep(0.001)
                cur_time = time.time()
        else:
            # video open failed
            # print(f"ERROR: cannot open video {video_file}")
            break

    cap.release()
    cv2.destroyAllWindows()
