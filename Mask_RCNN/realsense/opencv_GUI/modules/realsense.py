from modules.utils import *
import pyrealsense2 as rs 
import os
import numpy as np
import time

class Realsense:
    def __init__(self, recording_path, m_rcnn_path):
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
        self.pipeline.start(self.config)

        # Create colorizer object
        self.colorizer = rs.colorizer()

        self.frames = []
        self.depth_frame_aligned = []
        self.depth_image_aligned_color = []
        self.color_image = []
        self.saved_depth_image = []
        self.start_time = 0

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

    def save_depth(self):
        self.saved_depth_image = np.asanyarray(self.depth_frame_aligned.get_data())