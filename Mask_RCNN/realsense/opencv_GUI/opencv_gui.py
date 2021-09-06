#%%
from modules.realsense import Realsense
from modules.peppers import Peppers
from modules.utils import *

RECORDING_PATH = '../../dataset/bags/cart_3_red_yellow.bag'
M_RCNN_PATH = '../../src/Mask_RCNN/datasets/process'
M_RCNN_JSON_PATH = 'boxes'


def extract_frames(recording_path, m_rcnn_path, m_rcnn_json_path):
    try:
        camera = Realsense(recording_path, m_rcnn_path)
        peppers = Peppers(m_rcnn_path, m_rcnn_json_path)
        first_run = False
        
        # while True:

        if not first_run:
            # Delete al JSONs at [...]/boxes
            delete_all(m_rcnn_path, M_RCNN_JSON_PATH)
            camera.first_run()

            print("Waiting for Mask R-CNN intialization")
            peppers.get_JSON_name()
            print("Mask R-CNN initialized")
            
            # Discard test image detection json
            delete_all(m_rcnn_path, M_RCNN_JSON_PATH)

            first_run = True
            # Start timer
            peppers.start_timer()

        camera.next_frame()
    finally:
        print("Stopping depth and image processing")
        pass




if __name__ == "__main__":
       extract_frames(RECORDING_PATH, M_RCNN_PATH, M_RCNN_JSON_PATH)
# %%
