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

    def validate_size(self, x_coords, y_coords, threshold):
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

    def read_json_data(self, camera):
        file_name = self.json_file[0]

        if file_name.split('.')[0] == str(camera.frame_number):
            print("Processing bboxes of {}".format(file_name))
            with open(os.path.join(self.m_rcnn_path + '/' + self.m_rcnn_json_path + '/', file_name)) as json_file:
                self.json_data = json.load(json_file)
                self.json_data = np.array(self.json_data, dtype=object)
            return True
        else:
            return False
        
            
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
                complete_pepper_list["peppers"][pepper_counter]["2d_info"] ={}
                complete_pepper_list["peppers"][pepper_counter]["2d_info"]["x_min"] = detected_object[0][1]
                complete_pepper_list["peppers"][pepper_counter]["2d_info"]["x_max"] = detected_object[0][3]
                complete_pepper_list["peppers"][pepper_counter]["2d_info"]["y_min"] = detected_object[0][0]
                complete_pepper_list["peppers"][pepper_counter]["2d_info"]["y_max"] = detected_object[0][2]

                bbox_center = [
                    int((complete_pepper_list["peppers"][pepper_counter]["2d_info"]["x_max"] - complete_pepper_list["peppers"][pepper_counter]["2d_info"]["x_min"])/2 + complete_pepper_list["peppers"][pepper_counter]["2d_info"]["x_min"]),
                    int((complete_pepper_list["peppers"][pepper_counter]["2d_info"]["y_max"] - complete_pepper_list["peppers"][pepper_counter]["2d_info"]["y_min"])/2 + complete_pepper_list["peppers"][pepper_counter]["2d_info"]["y_min"])
                ]
                complete_pepper_list["peppers"][pepper_counter]["2d_info"]["center"] = {}
                complete_pepper_list["peppers"][pepper_counter]["2d_info"]["center"]["x"] = bbox_center[0]
                complete_pepper_list["peppers"][pepper_counter]["2d_info"]["center"]["y"] = bbox_center[1]
                
                pepper_counter = pepper_counter + 1

            # Is peduncle
            if(detected_object[1] == 2):
                complete_pepper_list["peduncles"][peduncle_counter] = {}
                complete_pepper_list["peduncles"][peduncle_counter]["2d_info"] = {}
                complete_pepper_list["peduncles"][peduncle_counter]["2d_info"]["x_min"] = detected_object[0][1]
                complete_pepper_list["peduncles"][peduncle_counter]["2d_info"]["x_max"] = detected_object[0][3]
                complete_pepper_list["peduncles"][peduncle_counter]["2d_info"]["y_min"] = detected_object[0][0]
                complete_pepper_list["peduncles"][peduncle_counter]["2d_info"]["y_max"] = detected_object[0][2]

                bbox_center = [
                    int((complete_pepper_list["peduncles"][peduncle_counter]["2d_info"]["x_max"] - complete_pepper_list["peduncles"][peduncle_counter]["2d_info"]["x_min"])/2 + complete_pepper_list["peduncles"][peduncle_counter]["2d_info"]["x_min"]),
                    int((complete_pepper_list["peduncles"][peduncle_counter]["2d_info"]["y_max"] - complete_pepper_list["peduncles"][peduncle_counter]["2d_info"]["y_min"])/2 + complete_pepper_list["peduncles"][peduncle_counter]["2d_info"]["y_min"])
                ]
                complete_pepper_list["peduncles"][peduncle_counter]["2d_info"]["center"] = {}
                complete_pepper_list["peduncles"][peduncle_counter]["2d_info"]["center"]["x"] = bbox_center[0]
                complete_pepper_list["peduncles"][peduncle_counter]["2d_info"]["center"]["y"] = bbox_center[1]

                peduncle_counter = peduncle_counter + 1
        # print(complete_pepper_list)
        self.complete_pepper_list = complete_pepper_list

    def filter_peppers(self, BBOX_SIZE_THRESHOLD):
        pepper_counter = 0
        final_pepper_list = {}
        final_pepper_list["peppers"] = {}
        for key, pepper in self.complete_pepper_list["peppers"].items():
            pepper = pepper["2d_info"]
            if(self.validate_size([ pepper["x_min"], pepper["x_max"] ], [ pepper["y_min"], pepper["y_max"] ], BBOX_SIZE_THRESHOLD)):
                final_pepper_list["peppers"][pepper_counter] = {}
                final_pepper_list["peppers"][pepper_counter]["2d_info"] = {}
                final_pepper_list["peppers"][pepper_counter]["2d_info"]["fruit"] = {}
                final_pepper_list["peppers"][pepper_counter]["2d_info"]["fruit"] = pepper
                pepper_counter = pepper_counter + 1

        self.final_pepper_list = final_pepper_list
        
    def find_peduncles(self):
        for pepper, pepper_data in self.final_pepper_list["peppers"].items():
            pepper_2d_info = pepper_data["2d_info"]["fruit"]

            pepper_center_x = pepper_2d_info["center"]["x"]
            pepper_center_y = pepper_2d_info["center"]["y"]

            # Currently using the average size of the bbox to find peduncles near the center of the pepper
            avg_size = int(((pepper_2d_info["x_max"] - pepper_2d_info["x_min"]) + (pepper_2d_info["y_max"] - pepper_2d_info["y_min"]))/2)
            
            # Traverse peduncles to find one that corresponds to a pepper
            for peduncle, peduncle_data in self.complete_pepper_list["peduncles"].items():
                peduncle_2d_info = peduncle_data["2d_info"]
                
                peduncle_center_x = peduncle_2d_info["center"]["x"]
                peduncle_center_y = peduncle_2d_info["center"]["y"]

                # Search algorithm
                if( pepper_center_x + avg_size/2 > peduncle_center_x and 
                    pepper_center_x - avg_size/2 < peduncle_center_x):
                    if( pepper_center_y  > peduncle_center_y and 
                        pepper_center_y - avg_size   < peduncle_center_y):
                        print("Found pepper {} with peduncle {}".format(pepper_2d_info, peduncle_2d_info))
                        self.final_pepper_list["peppers"][pepper]["2d_info"]["peduncle"] = {}
                        self.final_pepper_list["peppers"][pepper]["2d_info"]["peduncle"] = peduncle_2d_info
                        
        

    def process_pepper_data(self):
        self.read_json_data()
        self.parse_json_data()

    
