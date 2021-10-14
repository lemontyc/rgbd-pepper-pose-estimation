import glob
from PIL import Image
import os
import shutil

def delete_all(m_rcnn_path, path):
   #%% Delete all files at path
    files = glob.glob(m_rcnn_path +'/' + path + '/*')
    for f in files:
        os.remove(f) 

def save_image(image, name, m_rcnn_path, save_path):
    im = Image.fromarray(image)
    # Create image first, and then copy to start inference process
    im.save(os.path.join( m_rcnn_path + '/' + name + '.png'))
    shutil.move(m_rcnn_path + '/' + name + '.png', m_rcnn_path + '/' + save_path + '/' + name + '.png')
