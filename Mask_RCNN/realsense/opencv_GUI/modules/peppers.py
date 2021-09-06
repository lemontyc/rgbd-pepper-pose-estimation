import os
import json
import sys
import math
import numpy as np

class Peppers:
    def __init__(self, m_rcnn_path, m_rcnn_json_path):
        self.m_rcnn_path = m_rcnn_path
        self.m_rcnn_json_path = m_rcnn_json_path


        self.final_pepper_list = {}
        self.complete_pepper_list = {}
        self.json_file = []
        self.json_data = []
        self.expected = 1 # Scale multiplier, in this case the coordinates are already alligned

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

    def read_json_data(self):
        file_name = self.json_file[0]
        print("Processing bboxes of {}".format(file_name))
        with open(os.path.join(self.m_rcnn_path + '/' + self.m_rcnn_json_path + '/', file_name)) as json_file:
            self.json_data = json.load(json_file)
            self.json_data = np.array(self.json_data, dtype=object)
        
            
    def parse_json_data(self):
        complete_pepper_list = {}
        complete_pepper_list["peppers"] = {}
        complete_pepper_list["peduncles"] = {}
        pepper_counter = 0
        peduncle_counter = 0
        for count, detected_object in enumerate(self.json_data):
            # If object is a pepper
            if(detected_object[1] == 1):
                complete_pepper_list["peppers"][pepper_counter] = {}
                complete_pepper_list["peppers"][pepper_counter]["x_min"] = detected_object[0][1]
                complete_pepper_list["peppers"][pepper_counter]["x_max"] = detected_object[0][3]
                complete_pepper_list["peppers"][pepper_counter]["y_min"] = detected_object[0][0]
                complete_pepper_list["peppers"][pepper_counter]["y_max"] = detected_object[0][2]

                bbox_center = [
                    int((complete_pepper_list["peppers"][pepper_counter]["x_max"] - complete_pepper_list["peppers"][pepper_counter]["x_min"] )/2 + complete_pepper_list["peppers"][pepper_counter]["x_min"]),
                    int((complete_pepper_list["peppers"][pepper_counter]["y_max"] - complete_pepper_list["peppers"][pepper_counter]["y_min"])/2 + complete_pepper_list["peppers"][pepper_counter]["y_min"])
                ]
                complete_pepper_list["peppers"][pepper_counter]["center"] = {}
                complete_pepper_list["peppers"][pepper_counter]["center"]["x"] = bbox_center[0]
                complete_pepper_list["peppers"][pepper_counter]["center"]["y"] = bbox_center[1]
                
                pepper_counter = pepper_counter + 1

            # Is peduncle
            if(detected_object[1] == 2):
                complete_pepper_list["peduncles"][peduncle_counter] = {}
                complete_pepper_list["peduncles"][peduncle_counter]["x_min"] = detected_object[0][1]
                complete_pepper_list["peduncles"][peduncle_counter]["x_max"] = detected_object[0][3]
                complete_pepper_list["peduncles"][peduncle_counter]["y_min"] = detected_object[0][0]
                complete_pepper_list["peduncles"][peduncle_counter]["y_max"] = detected_object[0][2]

                bbox_center = [
                    int((complete_pepper_list["peduncles"][peduncle_counter]["x_max"] - complete_pepper_list["peduncles"][peduncle_counter]["x_min"])/2 + complete_pepper_list["peduncles"][peduncle_counter]["x_min"]),
                    int((complete_pepper_list["peduncles"][peduncle_counter]["y_max"] - complete_pepper_list["peduncles"][peduncle_counter]["y_min"])/2 + complete_pepper_list["peduncles"][peduncle_counter]["y_min"])
                ]
                complete_pepper_list["peduncles"][peduncle_counter]["center"] = {}
                complete_pepper_list["peduncles"][peduncle_counter]["center"]["x"] = bbox_center[0]
                complete_pepper_list["peduncles"][peduncle_counter]["center"]["y"] = bbox_center[1]

                peduncle_counter = peduncle_counter + 1
        print(complete_pepper_list)

            


    def process_pepper_data(self):
        self.read_json_data()
        self.parse_json_data()
        pass