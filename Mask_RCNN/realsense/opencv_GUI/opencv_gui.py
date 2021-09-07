#%%
from modules.realsense import Realsense
from modules.peppers import Peppers
from modules.gui import Windows
from modules.utils import *
import pprint

RECORDING_PATH = '../../dataset/bags/cart_3_red_yellow.bag'
M_RCNN_PATH = '../../src/Mask_RCNN/datasets/process'
M_RCNN_JSON_PATH = 'boxes'


def extract_frames(recording_path, m_rcnn_path, m_rcnn_json_path):
    try:
        peppers = Peppers(m_rcnn_path, m_rcnn_json_path)
        camera = Realsense(recording_path, m_rcnn_path, peppers.expected)
        gui = Windows(peppers.expected)
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
                print("Saved frame #{} for inference".format(camera.frames.get_frame_number()))
                save_image(camera.color_image, str(camera.frames.get_frame_number()), m_rcnn_path, 'input')
                camera.save_color()
                camera.save_depth()
                camera.start_capture_timer()

            # Try to read bbox JSON
            peppers.read_JSON()
            # If JSON was succesfully read, continue
            if peppers.json_file:
                # Only parse data if read file matches saved frame
                # Prevents desynch
                if peppers.read_json_data(camera):
                    # Delete json file
                    delete_all(m_rcnn_path, M_RCNN_JSON_PATH)
                    peppers.parse_json_data()
                    gui.draw_all_objects_bbox(camera.saved_color_image, peppers.complete_pepper_list, (199, 240, 218), (129, 176, 247), 1)
                    peppers.filter_peppers(gui.BBOX_SIZE_THRESHOLD)
                    gui.draw_all_objects_bbox(camera.saved_color_image, peppers.final_pepper_list, (57, 219, 98), (10, 88, 204),2)
                    peppers.find_peduncles()
                    gui.draw_all_objects_bbox(camera.saved_color_image, peppers.final_pepper_list, (57, 219, 98), (10, 88, 204),2)
                    peppers.compute_angle()
                    gui.draw_angles(camera.saved_color_image, peppers.final_pepper_list)
                    camera.obtain_coordinates(peppers.final_pepper_list)

                    pprint.pprint(peppers.final_pepper_list)
                    
                    gui.display_inference_stream(camera.saved_color_image)

                    
            



            gui.user_paused()
            if(gui.user_exited()):
                break
            

    finally:
        print("Stopping depth and image processing")
        pass




if __name__ == "__main__":
       extract_frames(RECORDING_PATH, M_RCNN_PATH, M_RCNN_JSON_PATH)
# %%
