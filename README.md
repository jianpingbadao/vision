# vision
This is a simple vehile detection project using Computer Vision

Here I used background subtractions methods of OpenCV Library of Python and some morphological transformation for accuracy.
But this is for only static cameras. 

At the corner of the video you can see the count of the vehicles which gets recorded
when they cross a predefined limit. For the calculation of the object coordinates and object ids I defined a class called vehicles.py

For running it, just download all files and run the main.py
Thank you.


## Demo
A simple demo to show how the `VideoCapture()` works with the webcam:
> `python video_capture_demo.py`


## Set up
1. (Optional) It is highly recommended to set up and run this in a separate [conda](https://conda.io/en/latest/) environment.
2. Install required packages:
    > `python install -r requirements.txt`
3. You need to follow this step only if you want to try out the functionality that captures and processes video from a given URL of a traffic camera.
   - Install Chrome Web Browser (Other web browsers could also work. But corresponding changes are needed in the code.), and find out its version by going to `Menu` on the top right -> `Help` -> `About`. https://www.howtogeek.com/299243/which-version-of-chrome-do-i-have/
   - Find and download the matching [Chrome driver](https://sites.google.com/a/chromium.org/chromedriver/). I believe as long as the major versions (the number before the first `.` in version number) of the driver and browser are the same, it should work fine.
   - Unzip the Chrome Driver and put it onto the `Desktop` (Of course you can put it wherever you want, but then you need to make some changes in the coding so that the program knows where to find the Driver.)

## To Run

1. To process video stream from URL, run:
   > `python WebsiteVidCapture.py [web-cam-URL]`
   
   where [`web-cam-URL`] can be found at [New York City Department of Transportation](https://webcams.nyctmc.org/), e.g. <https://webcams.nyctmc.org/google_popup.php?cid=738> for **Northern Blvd @ Honeywell Bridge**.

2. To launch with GUI, follow
   
3. To process multiple video streams from URL, go to the terminal and edit runMany

   You can edit on terminal by typing [nano runMany] and inside you will see an array in which you can populate with multiple URL's as a string. Save the file and run chmod +x runMany. From terminal run the command [./runMany]

4. To process a sample video, run command [python original.py]
   **TO Be Continued**
