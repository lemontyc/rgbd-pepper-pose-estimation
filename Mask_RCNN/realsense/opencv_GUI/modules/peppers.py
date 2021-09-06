import os
import json
import sys
import math
import time


class Peppers:
    def __init__(self, m_rcnn_path, m_rcnn_json_path):
        self.m_rcnn_path = m_rcnn_path
        self.m_rcnn_json_path = m_rcnn_json_path


        self.final_pepper_list = {}
        self.complete_pepper_list = {}
        self.json_file = []
        self.start_time = 0
        # def read_JSON():

    def start_timer(self):
        self.start_time = time.time()

    def read_JSON(self):
        self.json_file = next(os.walk(self.m_rcnn_path + '/' + self.m_rcnn_json_path))[2]
        
    def get_JSON_name(self):
        self.read_JSON()
        while not self.json_file:
            self.read_JSON()

    def validate_size(x_coords, y_coords, threshold):
        if (x_coords[1] - x_coords[0]) * (y_coords[1] - y_coords[0]) > (threshold**2):
            return True
        else:
            return False

    def get_orientation(pepper_center, peduncle_center):
        pepper_x = pepper_center[0]
        pepper_y = pepper_center[1]
        peduncle_x = peduncle_center[0]
        peduncle_y = peduncle_center[1]
        radians = math.atan2(peduncle_y - pepper_y, peduncle_x - pepper_x)
        return math.degrees(radians)
