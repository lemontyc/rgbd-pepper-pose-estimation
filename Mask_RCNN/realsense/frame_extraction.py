#%%
# Import realsense python wrapper
import os
import glob
import cv2
import json
import shutil
import sys
import numpy as np
import math
from PIL import Image
import matplotlib.pyplot as plt
import pyrealsense2 as rs 
import argparse
import time
print("Environment Ready")


#%%
RECORDING_PATH = '../dataset/bags/cart_3_red_yellow.bag'
MASK_PATH = '../src/Mask_RCNN/datasets/process'

#%% Delete all files at [..]/boxes
files = glob.glob(MASK_PATH +'/boxes/*')
for f in files:
    os.remove(f)

#%%
def validate_size(x_coords, y_coords, threshold):
    if (x_coords[1] - x_coords[0]) * (y_coords[1] - y_coords[0]) > (threshold**2):
        return True
    else:
        return False

#%%
def get_orientation(pepper_center, peduncle_center):
    pepper_x = pepper_center[0]
    pepper_y = pepper_center[1]
    peduncle_x = peduncle_center[0]
    peduncle_y = peduncle_center[1]
    radians = math.atan2(peduncle_y - pepper_y, peduncle_x - pepper_x)
    # radians = math.atan2(pepper_y - peduncle_y, pepper_x - peduncle_x)
    return math.degrees(radians)

#%%

def nothing(x):
    pass

try:
    # Create pipeline
    pipeline = rs.pipeline()

    # Create a config object
    config = rs.config()

    # Tell config that we will use a recorded device from file to be used by the pipeline through playback.
    config.enable_device_from_file(RECORDING_PATH)

    # Start streaming from file
    pipeline.start(config)

    # Create opencv window to render images in
    cv2.namedWindow("Color Stream", cv2.WINDOW_AUTOSIZE)
    cv2.namedWindow("Depth Stream", cv2.WINDOW_AUTOSIZE)
    cv2.namedWindow("Detection", cv2.WINDOW_AUTOSIZE)

    # Add trackbars to modify detection settings
    cv2.createTrackbar('ON/OFF','Detection', 1, 1, nothing)
    cv2.createTrackbar('Seconds','Detection', 3, 10,nothing)
    cv2.createTrackbar('Min BBOX Size','Detection', 100, 200,nothing)
    
    # Set window position
    cv2.moveWindow("Color Stream", 0,10)
    cv2.moveWindow("Depth Stream", 0,480)
    
    cv2.moveWindow("Detection", 690, 10)

    # Create colorizer object
    colorizer = rs.colorizer()

    first_run = False

    start_time = 0
    detection_image                 = []
    # Streaming loop
    while True:
        if not first_run:
            # Skip 5 first frames to give the Auto-Exposure time to adjust
            for x in range(5):
                frames = pipeline.wait_for_frames()
            # Get test color_frame
            color_frame = frames.get_color_frame()
            color_image = np.asanyarray(color_frame.get_data())
            detection_image = color_image.copy()
            # Save test image as a file
            im = Image.fromarray(color_image)
            im.save(os.path.join(MASK_PATH + '/test.png'))
            shutil.move(MASK_PATH + '/test.png', MASK_PATH + '/input/test.png')

            # Read bbox JSON of test file. While it is not present, Mask RCNN has not
            # initialized yet
            file_names = next(os.walk(MASK_PATH + '/boxes'))[2]
            print("Waiting for Mask R-CNN intialization")
            while not file_names:
                file_names = next(os.walk(MASK_PATH + '/boxes'))[2]
            print("Mask R-CNN initialized")

            #%% Delete all files at [..]/boxes
            files = glob.glob(MASK_PATH +'/boxes/*')
            for f in files:
                os.remove(f)
            first_run = True
            # Start timer
            start_time = time.time()
        
        # Get frameset of depth
        frames = pipeline.wait_for_frames()

        # Get color and depth frames
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()

        # Align depth image with color
        # Create alignment primitive with color as its target stream
        align = rs.align(rs.stream.color)
        frames = align.process(frames)

        # Update color and depth frames
        depth_frame_aligned = frames.get_depth_frame()


        # Colorize depth frame to jet colormap
        depth_frame_aligned_color = colorizer.colorize(depth_frame_aligned)


        depth_image_aligned_color       = np.asanyarray(depth_frame_aligned_color.get_data())
        color_image                     = np.asanyarray(color_frame.get_data())
        
        
        # Resize images for display
        small_color_image                   = cv2.resize(color_image, (640, 320))
        medium_color_image                  = cv2.resize(color_image, (1056, 528))
        small_depth_image_aligned_color     = cv2.resize(depth_image_aligned_color, (640, 320))

        # Render image in opencv window
        cv2.imshow("Color Stream", cv2.cvtColor(small_color_image, cv2.COLOR_RGB2BGR))
        cv2.imshow("Depth Stream", cv2.cvtColor(small_depth_image_aligned_color, cv2.COLOR_RGB2BGR))

        # Get current trackbar values
        detection               = cv2.getTrackbarPos('ON/OFF','Detection')
        capture_delay           = cv2.getTrackbarPos('Seconds','Detection')
        BBOX_SIZE_THRESHOLD     = cv2.getTrackbarPos('Min BBOX Size','Detection')

        # Save image and send to model every capture_delay seconds
        if (time.time() - start_time) > capture_delay:
            print("Copied image")
            detection_image = color_image.copy()
            im = Image.fromarray(color_image)
            im.save(os.path.join(MASK_PATH + '/frame.png'))
            shutil.move(MASK_PATH + '/frame.png', MASK_PATH + '/input/frame.png')
            start_time = time.time()
        
        # Try to read bbox JSON
        file_names = next(os.walk(MASK_PATH + '/boxes'))[2]
        if file_names:
            file_name = file_names[0]
            data = []
            with open(os.path.join(MASK_PATH + '/boxes/', file_name)) as json_file:
                data = json.load(json_file)
                data = np.array(data, dtype=object)

            # Filter peppers
            pepper_data = []
            peduncle_data = []
            
            expected = 1 # Scale multiplier, in this case the coordinates are already alligned
            for box in data:
                box = box.tolist()
                xmin = box[0][1]
                xmax = box[0][3]
                ymin = box[0][0]
                ymax = box[0][2]

                bbox_center = [
                    int((xmax - xmin)/2 + xmin),
                    int((ymax - ymin)/2 + ymin)
                ]

                if(validate_size([xmin, xmax], [ymin, ymax], BBOX_SIZE_THRESHOLD)):
                    box.append(bbox_center)
                    pepper_data.append(box)
                
                # Append data from peduncles
                if(box[1] == 2):
                    bbox_center = [
                        int((xmax - xmin)/2 + xmin),
                        int((ymax - ymin)/2 + ymin)
                    ]
                    
                    box.append(bbox_center)
                    peduncle_data.append(box)

            # Find peduncle
            final_pepper_list = {}
            for count, pepper in enumerate(pepper_data):
                xmin = pepper[0][1]
                xmax = pepper[0][3]
                ymin = pepper[0][0]
                ymax = pepper[0][2]

                # Currently using the average size of the bbox to find peduncles near the center of the pepper
                avg_size = int(((xmax - xmin) + (ymax -ymin))/2)

                pepper_center_x = pepper[2][0]
                pepper_center_y = pepper[2][1]

                # Add pepper information to the final list
                final_pepper_list[count] = {}
                final_pepper_list[count]["pepper"] = pepper
                
                # Traverse peduncles to find one that corresponds to a pepper
                for peduncle in peduncle_data:
                    peduncle_center_x = peduncle[2][0]
                    peduncle_center_y = peduncle[2][1]
                    
                    if(pepper_center_x + avg_size >  peduncle_center_x and pepper_center_x - avg_size   < peduncle_center_x):
                        if(pepper_center_y + avg_size >  peduncle_center_y and pepper_center_y - avg_size   < peduncle_center_y):
                            # print("Found pepper {} with peduncle {}".format(pepper[2], peduncle[2]))
                            final_pepper_list[count]["peduncle"]    = peduncle
                            final_pepper_list[count]["angle"]       = get_orientation(pepper[2], peduncle[2])

            # Draw infered objects
            infered_image = detection_image.copy()
            for key, value in final_pepper_list.items():
                xmin = value["pepper"][0][1]
                xmax = value["pepper"][0][3]
                ymin = value["pepper"][0][0]
                ymax = value["pepper"][0][2]
                cv2.rectangle(infered_image, (int(xmin * expected), int(ymin * expected)), (int(xmax * expected), int(ymax * expected)), (0, 255, 0), 5)

                if "peduncle" in value:
                    xmin = value["peduncle"][0][1]
                    xmax = value["peduncle"][0][3]
                    ymin = value["peduncle"][0][0]
                    ymax = value["peduncle"][0][2]

                    # Draw peduncle
                    cv2.rectangle(infered_image, (int(xmin * expected), int(ymin * expected)), (int(xmax * expected), int(ymax * expected)), (0, 0, 255), 5)

                    # Draw line with computed angle
                    angle = value["angle"]
                    length = 80

                    p1 = value["pepper"][2]
                    p2_x = int(p1[0] + length * math.cos(angle * math.pi /180))
                    p2_y = int(p1[1] + length * math.sin(angle * math.pi /180))

                    cv2.line(detection_image, p1, (p2_x, p2_y), (255, 0, 0), 3)
            final_pepper_list = {}
            cv2.imshow("Detection", cv2.cvtColor(infered_image, cv2.COLOR_RGB2BGR))

        key = cv2.waitKey(1)
        # if pressed escape exit program
        if key == 27:
            cv2.destroyAllWindows()
            break

finally:
    print("Stopping depth and image processing")
    pass
