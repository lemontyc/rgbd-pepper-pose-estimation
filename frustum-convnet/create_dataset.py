#%%
from pathlib import Path
import shutil
import os
import math

#%%
OUTPUT_DATASET_PATH     =    r"G:\datasets\dataset_620_red_yellow_cart_only\ply"
INPUT_DATASET_PATH      =    r"G:\datasets\dataset_620_red_yellow_cart_only\images"
INPUT_IMG_PATHs         =   [r"G:\Bags\red\cart_1_red\ply\ply", 
                             r"G:\Bags\red\cart_2_red\ply\ply", 
                             r"G:\Bags\red\cart_3_red\ply\ply",
                             r"G:\Bags\yellow\cart_1_yellow\ply\ply",
                             r"G:\Bags\yellow\cart_2_yellow\ply\ply",
                             r"G:\Bags\yellow\cart_3_red_yellow\ply\ply",
                             r"G:\Bags\yellow\cart_4_yellow_red\ply\ply"]    

# %%
pc_paths = []
intput_dataset_list = os.listdir(INPUT_DATASET_PATH)
intput_dataset_list_fixed = []

#%%
for img in intput_dataset_list:
    intput_dataset_list_fixed.append(img.split(".")[0].split("_")[2])

#%%
for pc_path in INPUT_IMG_PATHs:
    pc_list = os.listdir(pc_path)
    pc_list_fixed = []
    for pc in pc_list:
        pc_list_fixed.append(pc.split(".")[0].split("_")[1])
    for img in intput_dataset_list_fixed:
        try:
            index = pc_list_fixed.index(img)
            print("found {} at {}".format(img, pc_path + "\\" + pc_list[index]))
            shutil.copy(pc_path + "\\" + pc_list[index], OUTPUT_DATASET_PATH)
        except:
            pass

# %%
print(len(pc_list))
# %%
