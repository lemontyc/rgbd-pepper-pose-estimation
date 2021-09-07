import cv2
import numpy as np
import time
import math


def nothing(x):
    pass

class Windows():
    def __init__(self, expected):
        # Create opencv windows to render images in
        cv2.namedWindow("Color/Depth Stream", cv2.WINDOW_AUTOSIZE)
        cv2.namedWindow("Detection", cv2.WINDOW_AUTOSIZE)
        
        # Set default values for trackbars
        self.detection = 1
        self.capture_delay = 4
        self.BBOX_SIZE_THRESHOLD = 100
        self.expected = expected

        # Add trackbars to modify detection settings
        cv2.createTrackbar('ON/OFF','Detection', self.detection , 1, nothing)
        cv2.createTrackbar('Seconds','Detection', self.capture_delay, 10,nothing)
        cv2.createTrackbar('Min BBOX Size','Detection', self.BBOX_SIZE_THRESHOLD, 200,nothing)

        # Set window position
        cv2.moveWindow("Color/Depth Stream", 0,10)
        cv2.moveWindow("Detection", 690, 10)

    def user_exited(self):
        key = cv2.waitKey(1)
        # if pressed escape exit program
        if key == 27:
            cv2.destroyAllWindows()
            return True
        
    def user_paused(self):
        pass

    def display_clean_stream(self, color_image, depth_image_aligned_color):
        small_color_image                   = cv2.resize(color_image, (640, 320))
        small_depth_image_aligned_color     = cv2.resize(depth_image_aligned_color, (640, 320))
        stacked_depth_and_color_images      = np.concatenate((small_color_image, small_depth_image_aligned_color), axis=0)
        # Render image in opencv window
        cv2.imshow("Color/Depth Stream", cv2.cvtColor(stacked_depth_and_color_images, cv2.COLOR_RGB2BGR))

    def read_trackbars(self):
        self.detection               = cv2.getTrackbarPos('ON/OFF','Detection')
        self.capture_delay           = cv2.getTrackbarPos('Seconds','Detection')
        self.BBOX_SIZE_THRESHOLD     = cv2.getTrackbarPos('Min BBOX Size','Detection')

    def display_inference_stream(self, saved_color_image):
        cv2.imshow("Detection", cv2.cvtColor(saved_color_image, cv2.COLOR_RGB2BGR))

    def draw_all_objects_bbox(self, saved_color_image, objects, pepper_color, peduncle_color, size):
        for key, value in objects.items():
            
            for bbox_number, bbox in value.items():
                info_2d = bbox['2d_info']
                if key == 'peppers':
                    # This validation is necessary as final_pepper_list has different structure
                    # than comple_pepper_list
                    if 'fruit' in bbox['2d_info']:
                        info_2d = bbox['2d_info']['fruit']
                    cv2.rectangle(saved_color_image,    (int(info_2d["x_min"] * self.expected), int(info_2d["y_min"] * self.expected)), 
                                                        (int(info_2d["x_max"] * self.expected), int(info_2d["y_max"] * self.expected)), 
                                                        pepper_color, size)
                    if 'peduncle' in bbox['2d_info']:
                        info_2d = bbox['2d_info']['peduncle']
                        cv2.rectangle(saved_color_image,    (int(info_2d["x_min"] * self.expected), int(info_2d["y_min"] * self.expected)), 
                                                            (int(info_2d["x_max"] * self.expected), int(info_2d["y_max"] * self.expected)), 
                                                            peduncle_color, size)
                if key == 'peduncles':
                    cv2.rectangle(saved_color_image,    (int(info_2d["x_min"] * self.expected), int(info_2d["y_min"] * self.expected)), 
                                                        (int(info_2d["x_max"] * self.expected), int(info_2d["y_max"] * self.expected)), 
                                                        peduncle_color, size)

    def draw_angles(self, saved_color_image, final_pepper_list):
        for pepper, pepper_data in final_pepper_list["peppers"].items():
            if "angle" in pepper_data["2d_info"]:
                angle = pepper_data["2d_info"]["angle"]
                line_end        = []
                pepper_center      = [pepper_data["2d_info"]["fruit"]["center"]["x"], pepper_data["2d_info"]["fruit"]["center"]["y"]]
                peduncle_center    = [pepper_data["2d_info"]["peduncle"]["center"]["x"], pepper_data["2d_info"]["peduncle"]["center"]["y"]]
                
                length = math.sqrt( ((pepper_center[0] - peduncle_center[0]) ** 2 )+((pepper_center[1] - peduncle_center[1]) ** 2) )

                line_end.append(int(pepper_center[0] + length * math.cos(angle * math.pi / 180)))
                line_end.append(int(pepper_center[1] + length * math.sin(angle * math.pi / 180)))

                cv2.line(saved_color_image, pepper_center, line_end, (255, 0, 0), 2)
    