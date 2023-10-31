from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import os
from PIL import Image
import numpy as np
import re


def CollectImages(queries, n):

    # Creating a webdriver instance
    driver = webdriver.Firefox()

    # Maximize the screen
    driver.maximize_window()

    # Open Google Images in the browser
    driver.get('https://images.google.com/')
    first = True
    # get current directory
    current_dir = os.getcwd()
    # create a new directory
    path = os.path.join(current_dir, 'images')
    # check if the directory exists
    if not os.path.isdir(path):
        os.mkdir(path)

    for query in queries:
        # Finding the search box
        if first == True:
            box = driver.find_element(By.XPATH, '//*[@id="APjFqb"]')
        else:
            box = driver.find_element(By.XPATH, '//*[@id="REsRA"]')
            # Clearing the search box
            box.clear()
        # Type the search query in the search box
        name, number = query.split(' [')
       
        search_query='multiple '+ name +'s'
        box.send_keys(search_query)

        # Pressing enter
        box.send_keys(Keys.ENTER)

        # Function for scrolling to the bottom of Google
        # Images results
        def scroll_to_bottom():

            last_height = driver.execute_script('\
            return document.body.scrollHeight')

            while True:
                driver.execute_script('\
                window.scrollTo(0,document.body.scrollHeight)')

                # waiting for the results to load
                # Increase the sleep time if your internet is slow
                time.sleep(3)

                new_height = driver.execute_script('\
                return document.body.scrollHeight')

                # click on "Show more results" (if exists)
                
                try:
                    driver.find_element(by=By.CLASS_NAME,value="LZ4I").click()
                    # waiting for the results to load
                    # Increase the sleep time if your internet is slow
                    time.sleep(3)

                except:
                    pass

                # checking if we have reached the bottom of the page
                if new_height == last_height:
                    break

                last_height = new_height


        # Calling the function
        scroll_to_bottom()

        # create a new directory for each query
        q_dir = os.path.join(path, query)
        # check if the directory exists
        if not os.path.isdir(q_dir):
            os.mkdir(q_dir)

        # Loop to capture and save each image
        for i in range(1, n):

            # range(1, 50) will capture images 1 to 49 of the search results
            # You can change the range as per your need.
            try:
                # XPath of each image
                str_i = str(i)
                val = f'/html/body/div[2]/c-wiz/div[3]/div[1]/div/div/div/div/div[1]/div[1]/span/div[1]/div[1]/div[{str_i}]/a[1]/div[1]/img'
                img = driver.find_element(by=By.XPATH, value=val)

                # Enter the location of folder in which
                # the images will be saved in q_dir.
                img.screenshot(f'{q_dir}/{str_i}.png')
            
                # Just to avoid unwanted errors
                time.sleep(0.2)

            except:
        
                # if we can't find the XPath of an image,
                # we skip to the next image
                continue
    
        first = False
    # Finally, we close the driver
    driver.close()
    # closes the current tab
    driver.quit()

def CreateBackup():
    # get current directory
    current_dir = os.getcwd()
    # check if the 'images_backup' directory exists
    if not os.path.isdir(os.path.join(current_dir, 'backup')):
        # create a new directory
        #os.mkdir(os.path.join(current_dir, 'backup'))
        # copy the 'images' directory to 'images_backup'
        os.system('cp -r images backup')


def resizeImages(width, height):
    # get current directory
    current_dir = os.getcwd()
    # create a new directory
    path = os.path.join(current_dir, 'images')
    # get all the subdirectories
    subdirs = os.listdir(path)
    for subdir in subdirs:
        # get the path of the subdirectory
        subdir_path = os.path.join(path, subdir)
        # get all the images in the subdirectory
        images = os.listdir(subdir_path)
        for image in images:
            # get the path of the image
            image_path = os.path.join(subdir_path, image)
            # open the image
            img = Image.open(image_path)
            # resize the image
            img = img.resize((width, height))
            # save the image
            img.save(image_path)


def list_of_original_images():
    images_per_dir = {}
    # get current directory
    current_dir = os.getcwd()
    # create a new directory
    path = os.path.join(current_dir, 'images')
    # get all the subdirectories
    subdirs = os.listdir(path)
    for subdir in subdirs:
        # get the path of the subdirectory
        subdir_path = os.path.join(path, subdir)
        # get all the images in the subdirectory
        images = os.listdir(subdir_path)
        images_per_dir[subdir] = images
        
    return images_per_dir
def resizeOneImage(path, width, height):
    # open the image
    img = Image.open(path)
    # resize the image
    img = img.resize((width, height))
    # save the image
    img.save(path)

def CropImage(list_of_images_per_dir):
    # get current directory
    current_dir = os.getcwd()
    # create a new directory
    path = os.path.join(current_dir, 'images')
    # get all the subdirectories
    subdirs = os.listdir(path)
    for subdir in subdirs:
        # get the path of the subdirectory
        subdir_path = os.path.join(path, subdir)
        # get all the images in the subdirectory
        images = list_of_images_per_dir[subdir]
        numbers = [int(file.split('.')[0]) for file in images if file.endswith('.png') and file.split('.')[0].isdigit()]
        max_number = max(numbers) if numbers else 0
        for i, image in enumerate(images):
            # get the path of the image
            image_path = os.path.join(subdir_path, image)
            # open the image
            img = Image.open(image_path)
            # crop the image
            img_croped = img.crop((10,10, 120, 120))
            # save the image
            image_name = f"{max_number + i + 1 }.png"
            img_path = os.path.join(subdir_path, image_name)
            img_croped.save(img_path)
            resizeOneImage(img_path, 224, 224)

def RotateImage(list_of_images_per_dir, alpha):
    # get current directory
    current_dir = os.getcwd()
    # create a new directory
    path = os.path.join(current_dir, 'images')
    # get all the subdirectories
    subdirs = os.listdir(path)
    for subdir in subdirs:
        # get the path of the subdirectory
        subdir_path = os.path.join(path, subdir)
        # get all the images in the subdirectory
        images = list_of_images_per_dir[subdir]
        files = os.listdir(subdir_path)
        numbers = [int(file.split('.')[0]) for file in files if file.endswith('.png') and file.split('.')[0].isdigit()]
        max_number = max(numbers) if numbers else 0
        for i, image in enumerate(images):
            # get the path of the image
            image_path = os.path.join(subdir_path, image)
            # open the image
            img = Image.open(image_path)
            # rotate the image alpha
            img_rotated = img.rotate(alpha)
            image_name = f"{max_number + i + 1 }.png"
            img_path = os.path.join(subdir_path, image_name)
            img_rotated.save(img_path)

def AddNoise(list_of_images_per_dir):
    # get current directory
    current_dir = os.getcwd()
    # create a new directory
    path = os.path.join(current_dir, 'images')
    # get all the subdirectories
    subdirs = os.listdir(path)
    for subdir in subdirs:
        # get the path of the subdirectory
        subdir_path = os.path.join(path, subdir)
        # get all the images in the subdirectory
        images = list_of_images_per_dir[subdir]
        files = os.listdir(subdir_path)
        numbers = [int(file.split('.')[0]) for file in files if file.endswith('.png') and file.split('.')[0].isdigit()]
        max_number = max(numbers) if numbers else 0
        for i, image in enumerate(images):
            # get the path of the image
            image_path = os.path.join(subdir_path, image)
            # open the image
            img = Image.open(image_path)
            # Convert the image to a numpy array
            img_array = np.array(img)
            
            # Add noise to the image array
            noise = np.random.normal(0, 5, img_array.shape)
            noisy_img_array = img_array + noise
            
            # Convert the noisy image array back to an image
            noisy_img = Image.fromarray(np.uint8(noisy_img_array))
            
            image_name = f"{max_number + i + 1 }.png"
            img_path = os.path.join(subdir_path, image_name)
            noisy_img.save(img_path)
def main():
    queries = ['Chihuahua [151]', 'Japanese spaniel [152]', 'Maltese dog [153]', 'Pekinese [154]', 'Shih-Tzu [155]', 'papillon [157]', 'Rhodesian ridgeback [159]', 'Afghan hound [160]', 'basset [161]', 'Pekinese [154]']
    CollectImages(queries, 50)
    CreateBackup()
    resizeImages(224, 224)
    list_of_images_per_dir = list_of_original_images()
    CropImage(list_of_images_per_dir)
    RotateImage(list_of_images_per_dir, 90)
    AddNoise(list_of_images_per_dir)

if __name__ == '__main__':
    main()