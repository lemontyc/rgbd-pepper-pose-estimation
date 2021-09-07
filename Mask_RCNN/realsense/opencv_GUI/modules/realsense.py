from modules.utils import *
import pyrealsense2 as rs 
import os
import numpy as np
import time
import cv2

class Realsense:
    def __init__(self, recording_path, m_rcnn_path, expected):
        # Save paths
        self.recording_path = recording_path
        self.m_rcnn_path = m_rcnn_path

        # Create pipeline
        self.pipeline = rs.pipeline()

        # Create a config object
        self.config = rs.config()

        # Tell config that we will use a recorded device from file to be used by the pipeline through playback.
        self.config.enable_device_from_file(self.recording_path)

        # Start streaming from file
        self.profile = self.pipeline.start(self.config)

        # Create colorizer object
        self.colorizer = rs.colorizer()

        self.frames = []
        self.depth_frame_aligned = []
        self.depth_image_aligned_color = []
        self.color_image = []
        self.saved_aligned_depth_frame = []
        self.saved_color_image = []
        self.start_time = 0
        self.frame_number = 0
        self.expected = expected

    def start_capture_timer(self):
        self.start_time = time.time()
    
    def capture_delay_ready(self, capture_delay):
        if (time.time() - self.start_time) > capture_delay:
            return True
        else:
            return False

    def first_run(self):
         # Skip 5 first frames to give the Auto-Exposure time to adjust
        for x in range(5):
            self.frames = self.pipeline.wait_for_frames()
        
        # Get test color_frame
        self.color_frame = self.frames.get_color_frame()
        self.color_image = np.asanyarray(self.color_frame.get_data())
        # Save test image as a file
        save_image(self.color_image, 'test', self.m_rcnn_path, 'input')

    def next_frame(self):
        # Advance to next frame
        self.frames = self.pipeline.wait_for_frames()

        # Get color and depth frames
        depth_frame = self.frames.get_depth_frame()
        color_frame = self.frames.get_color_frame()

        # Align depth image with color
        # Create alignment primitive with color as its target stream
        align = rs.align(rs.stream.color)
        self.frames = align.process(self.frames)

        # Update color and depth frames
        self.depth_frame_aligned = self.frames.get_depth_frame()

        # Colorize depth frame to jet colormap
        depth_frame_aligned_color = self.colorizer.colorize(self.depth_frame_aligned)

        # Save aligned colorized depth and color images
        self.depth_image_aligned_color       = np.asanyarray(depth_frame_aligned_color.get_data())
        self.color_image                     = np.asanyarray(color_frame.get_data())

    def save_color(self):
        self.saved_color_image = self.color_image

    def save_depth(self):
        self.saved_aligned_depth_frame = self.depth_frame_aligned
        self.frame_number       = self.frames.get_frame_number()

    def obtain_coordinates(self, final_pepper_list):
        # Get Depth data from the sensor 
        depth           = np.asanyarray(self.saved_aligned_depth_frame.get_data())
        # Get data scale from the device and convert to meters
        depth_scale     = self.profile.get_device().first_depth_sensor().get_depth_scale()
        # Get intinsic values od alligned depth frame
        depth_intrin    = self.saved_aligned_depth_frame.profile.as_video_stream_profile().intrinsics
        
        # Get pepper depth coordinates at pepper bbox center
        for pepper, pepper_data in final_pepper_list["peppers"].items():
            pepper_2d_data  = pepper_data["2d_info"]["fruit"]

            xmin_depth = int((pepper_2d_data["x_min"] * self.expected))
            ymin_depth = int((pepper_2d_data["y_min"] * self.expected))
            xmax_depth = int((pepper_2d_data["x_max"] * self.expected))
            ymax_depth = int((pepper_2d_data["y_max"] * self.expected))

            # Get depth values at the bbox location
            bbox_area_depth = depth[ymin_depth:ymax_depth,  xmin_depth:xmax_depth]
            # Obtain average depth value, this will be used to obtain the centroid coordinates
            bbox_centroid_pixel_depth_value,_,_,_ = cv2.mean(bbox_area_depth)
            
            # Get the centroid of the bbox
            pepper_center      = [pepper_data["2d_info"]["fruit"]["center"]["x"], pepper_data["2d_info"]["fruit"]["center"]["y"]]

            coordinates = rs.rs2_deproject_pixel_to_point(depth_intrin, pepper_center, bbox_centroid_pixel_depth_value * depth_scale)

            final_pepper_list["peppers"][pepper]["3d_info"] = {}
            final_pepper_list["peppers"][pepper]["3d_info"]["fruit"] = {}
            final_pepper_list["peppers"][pepper]["3d_info"]["fruit"]["Pose"] = {}
            final_pepper_list["peppers"][pepper]["3d_info"]["fruit"]["Pose"]["Point"] = {}
            final_pepper_list["peppers"][pepper]["3d_info"]["fruit"]["Pose"]["Quaternion"] = {}
            

            final_pepper_list["peppers"][pepper]["3d_info"]["fruit"]["Pose"]["Point"]["x"] = coordinates[0]
            final_pepper_list["peppers"][pepper]["3d_info"]["fruit"]["Pose"]["Point"]["y"] = coordinates[1]
            final_pepper_list["peppers"][pepper]["3d_info"]["fruit"]["Pose"]["Point"]["z"] = coordinates[2]
            
            # If peduncle exist, get depth coordinates at peduncle bbox center
            if "peduncle" in pepper_data["2d_info"]:
                peduncle_2d_data  = pepper_data["2d_info"]["peduncle"]

                xmin_depth = int((peduncle_2d_data["x_min"] * self.expected))
                ymin_depth = int((peduncle_2d_data["y_min"] * self.expected))
                xmax_depth = int((peduncle_2d_data["x_max"] * self.expected))
                ymax_depth = int((peduncle_2d_data["y_max"] * self.expected))

                # Get depth values at the bbox location
                bbox_area_depth = depth[ymin_depth:ymax_depth,  xmin_depth:xmax_depth]
                # Obtain average depth value, this will be used to obtain the centroid coordinates
                bbox_centroid_pixel_depth_value,_,_,_ = cv2.mean(bbox_area_depth)
                
                # Get the centroid of the bbox
                peduncle_center    = [pepper_data["2d_info"]["peduncle"]["center"]["x"], pepper_data["2d_info"]["peduncle"]["center"]["y"]]

                coordinates = rs.rs2_deproject_pixel_to_point(depth_intrin, pepper_center, bbox_centroid_pixel_depth_value * depth_scale)

                final_pepper_list["peppers"][pepper]["3d_info"]["peduncle"] = {}
                final_pepper_list["peppers"][pepper]["3d_info"]["peduncle"]["Pose"] = {}
                final_pepper_list["peppers"][pepper]["3d_info"]["peduncle"]["Pose"]["Point"] = {}
                final_pepper_list["peppers"][pepper]["3d_info"]["peduncle"]["Pose"]["Quaternion"] = {}
                

                final_pepper_list["peppers"][pepper]["3d_info"]["peduncle"]["Pose"]["Point"]["x"] = coordinates[0]
                final_pepper_list["peppers"][pepper]["3d_info"]["peduncle"]["Pose"]["Point"]["y"] = coordinates[1]
                final_pepper_list["peppers"][pepper]["3d_info"]["peduncle"]["Pose"]["Point"]["z"] = coordinates[2]
