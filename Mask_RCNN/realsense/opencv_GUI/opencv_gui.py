#%%
from modules.realsense import Realsense
from modules.peppers import Peppers
from modules.gui import Windows
from modules.utils import *

RECORDING_PATH = '../../dataset/bags/cart_3_red_yellow.bag'
M_RCNN_PATH = '../../src/Mask_RCNN/datasets/process'
M_RCNN_JSON_PATH = 'boxes'


def extract_frames(recording_path, m_rcnn_path, m_rcnn_json_path):
    try:
        camera = Realsense(recording_path, m_rcnn_path)
        peppers = Peppers(m_rcnn_path, m_rcnn_json_path)
        gui = Windows()
        first_run = False
        
        while True:

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
                camera.start_capture_timer()

            camera.next_frame()
            gui.display_clean_stream(camera.color_image, camera.depth_image_aligned_color)
            gui.read_trackbars()
            
            # Capture image from clean stream and copy to M-RCNN container for inferance
            # This process makes the stream slow down
            if(camera.capture_delay_ready(gui.capture_delay)):
                print("Running inferance at image #{}".format(camera.frames.get_frame_number()))
                save_image(camera.color_image, str(camera.frames.get_frame_number()), m_rcnn_path, 'input')
                camera.save_depth()
                camera.start_capture_timer()

            # Try to read bbox JSON
            peppers.read_JSON()
            if peppers.json_file:
                peppers.read_json_data()
                peppers.parse_json_data()
            




            if(gui.user_exited()):
                break


    finally:
        print("Stopping depth and image processing")
        pass




if __name__ == "__main__":
       extract_frames(RECORDING_PATH, M_RCNN_PATH, M_RCNN_JSON_PATH)
# %%
