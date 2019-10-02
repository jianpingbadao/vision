'''
Demo about how to use the VideoCapture

Tested in Python 3.6 and OpenCV 3.4
'''
import cv2
import time
import os

def demo():
    # cap = cv2.VideoCapture('https://www.weatherbug.com/traffic-cam/?latlng=42.931844,-78.763161')
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print('Fail to capture')
        exit()

    start_time = time.time()

    video_cod = cv2.VideoWriter_fourcc(*'mp4v')
    temp_video_folder = 'temp_videos'
    if not os.path.isdir(temp_video_folder):
        os.mkdir(temp_video_folder)
    output = cv2.VideoWriter(os.path.join(temp_video_folder, 'cam_video.mp4'),\
             video_cod, 20.0, (1280, 720))  # the last one is the resolution of the captured video

    while True:
        now = time.time()
        if now - start_time > 5:
            break

        got, frame = cap.read()

        if got:
            output.write(frame)
            # print(frame.shape)  # get the resolution here
            cv2.imshow("Webcam video", frame)
            if cv2.waitKey(20) == 27:
                break
        else:
            print('nothing captured')

    cap.release()
    output.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    demo()
