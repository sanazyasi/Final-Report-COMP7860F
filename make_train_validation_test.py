# -*- coding: utf-8 -*-
"""
Created on Fri Oct  6 22:22:26 2023

@author: AsusIran
"""

import os
import shutil
import random

main_directory = 'data/'

class_folders = os.listdir(main_directory)

subfolders = ['train', 'validation', 'test']

for subfolder in subfolders:
    subfolder_path = os.path.join(main_directory, subfolder)
    os.makedirs(subfolder_path, exist_ok=True)

train_ratio = 0.7  # 70% for training
validation_ratio = 0.15  # 15% for validation
test_ratio = 0.15  # 15% for testing

for class_folder in class_folders:
    class_path = os.path.join(main_directory, class_folder)
    
    if not os.path.isdir(class_path):
        continue
    
    for subfolder in subfolders:
        subfolder_path = os.path.join(main_directory, subfolder, class_folder)
        os.makedirs(subfolder_path, exist_ok=True)
    
    images = os.listdir(class_path)
    
    random.shuffle(images)
    
    num_images = len(images)
    num_train = int(train_ratio * num_images)
    num_validation = int(validation_ratio * num_images)
    
    train_images = images[:num_train]
    validation_images = images[num_train:num_train + num_validation]
    test_images = images[num_train + num_validation:]
    
    for image in train_images:
        src = os.path.join(class_path, image)
        dst = os.path.join(main_directory, 'train', class_folder, image)
        shutil.move(src, dst)
    
    for image in validation_images:
        src = os.path.join(class_path, image)
        dst = os.path.join(main_directory, 'validation', class_folder, image)
        shutil.move(src, dst)
    
    for image in test_images:
        src = os.path.join(class_path, image)
        dst = os.path.join(main_directory, 'test', class_folder, image)
        shutil.move(src, dst)

print("Completed")
