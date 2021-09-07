import cv2
import numpy as np
import time


def nothing(x):
    pass

class Windows():
    def __init__(self, expected):
        # Create opencv windows to render images in
        cv2.namedWindow("Color/Depth Stream", cv2.WINDOW_AUTOSIZE)
        cv2.namedWindow("Detection", cv2.WINDOW_AUTOSIZE)
        
        # Set default values for trackbars
        self.detection = 1
        self.capture_delay = 3
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
                if key == 'peppers':
                    cv2.rectangle(saved_color_image,    (int(bbox["x_min"] * self.expected), int(bbox["y_min"] * self.expected)), 
                                                        (int(bbox["x_max"] * self.expected), int(bbox["y_max"] * self.expected)), 
                                                        pepper_color, size)
                if key == 'peduncles':
                    cv2.rectangle(saved_color_image,    (int(bbox["x_min"] * self.expected), int(bbox["y_min"] * self.expected)), 
                                                        (int(bbox["x_max"] * self.expected), int(bbox["y_max"] * self.expected)), 
                                                        peduncle_color, size)



    