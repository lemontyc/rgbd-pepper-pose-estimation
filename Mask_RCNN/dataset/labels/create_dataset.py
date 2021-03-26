#!/usr/bin/python

import sys
import os, random
import shutil

#print ('Number of arguments:', len(sys.argv), 'arguments.')
#print ('Argument List:', str(sys.argv))

#percentage  = sys.argv[1]
#json_path   = sys.argv[2]
#images_path = sys.argv[3]
#output_path = sys.argv[4]


src_dir   = r'C:\Github\rgbd-pepper-pose-estimation\Mask_RCNN\dataset\labels\Dataset\\'
val_dir   = r'C:\Github\rgbd-pepper-pose-estimation\\Mask_RCNN\dataset\labels\output\val'
train_dir = r'C:\Github\rgbd-pepper-pose-estimation\\Mask_RCNN\dataset\labels\output\train'

#Put all images in a list
file_list = os.listdir(src_dir)



#Create \val\ directory
os.makedirs(val_dir)
#Create \train\ directory
os.makedirs(train_dir)

percentage=20
#Calculate percentage of images to be moved to val
percentage_val=round(len(file_list)*(percentage/100))

#Choose random percentage of images
a = random.sample(file_list, percentage_val)

#Move chosen images to \val\      
for i in range(percentage_val):
    file_list.remove(a[i])
    shutil.move(src_dir + a[i], val_dir + "\\" + a[i])
    

#Move remain images to \train\
for i in range(len(file_list)):
    shutil.move(src_dir + file_list[i], train_dir + "\\" + file_list[i])




#print(random.choices(json_path, k = 5))
#print(percentage, json_path, images_path, output_path)
