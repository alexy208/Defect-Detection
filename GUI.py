# -*- coding: utf-8 -*-
"""
Created on Thu Mar  9 18:52:20 2023

@author: 60183
"""
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
import numpy as np
from CV_Ass_2 import drawRect
from CV_Ass_2 import region_growing


# create a function to open the file dialog and select an image
def input_image():
    filename = filedialog.askopenfilename(title="Select an Image with defect",
                                          filetypes=(("JPEG files", "*.jpg"),
                                                     ("PNG files", "*.png"),
                                                     ("All files", "*.*")))

    # load the selected image using OpenCV
    input_img = cv2.imread(filename)
    ori_img = cv2.imread(filename)
    img = cv2.cvtColor(ori_img, cv2.COLOR_BGR2GRAY)
    return ori_img,img,input_img

# create a function to open the file dialog and select an template and run the defect detection    
def input_template(ori_img,img):
    filename = filedialog.askopenfilename(title="Select a Template",
                                          filetypes=(("JPEG files", "*.jpg"),
                                                     ("PNG files", "*.png"),
                                                     ("All files", "*.*")))
    
    template_ori = cv2.imread(filename)
    #template = cv2.imread('PCB_DATASET/PCB_USED/01.jpg',0)
    template_gray= cv2.cvtColor(template_ori, cv2.COLOR_BGR2GRAY)
    template_rgb = cv2.cvtColor(template_gray, cv2.COLOR_BGR2RGB)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))

    missing_binary_mask = np.uint8(img > 70)
    missing_temp_mask = np.uint8(template_gray >70)

    missing_output = np.uint8(missing_temp_mask^missing_binary_mask)
    missing_opening = cv2.morphologyEx(missing_output, cv2.MORPH_OPEN, kernel)

    # Define the color range to extract (here we're extracting green)
    lower = np.array([0,0, 0])
    upper = np.array([35, 80, 10])

    # Create a mask based on the color range
    mask = cv2.inRange(ori_img, lower, upper)
    mask_temp = cv2.inRange(template_ori, lower, upper)

    # Apply the mask to the original image
    output = cv2.bitwise_and(ori_img, ori_img, mask=mask)
    output_gray = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
    #output_gray = cv2.cvtColor(output_gray, cv2.COLOR_BGR2RGB)
    ret, output_bw = cv2.threshold(output_gray, 20, 255, cv2.THRESH_BINARY)

    # Apply the mask to the template
    output = cv2.bitwise_and(template_ori, template_ori, mask=mask_temp)
    output_gray_temp = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
    #output_gray_temp = cv2.cvtColor(output_gray_temp, cv2.COLOR_BGR2RGB)
    ret, output_bw_temp = cv2.threshold(output_gray_temp, 20, 255, cv2.THRESH_BINARY)


    mouse_output = output_bw_temp ^ output_bw
    mouse_opening = cv2.morphologyEx(mouse_output, cv2.MORPH_OPEN, kernel)

    spur_output = output_bw_temp - output_bw
    spur_opening = cv2.morphologyEx(spur_output, cv2.MORPH_OPEN, kernel)


    if np.sum(missing_opening ==1) >10:
        print("Defect is missing hole")
        defect = "Missing Hole"
        drawRect(missing_opening,ori_img)
        
    else:
        if np.sum(spur_opening==255) != 0:
            r_mask = region_growing(output_bw,spur_opening)
            if np.sum(r_mask==255)<3000:   
                print("Defect is Spurious Copper")
                defect = "Spurious Copper"
            
            else:
                print("Defect is Spur")
                defect = "Spur"
                
            drawRect(spur_opening,ori_img)
                
        else:
            print("Defect is mouse bite")
            defect = "Mouse Bite"
            drawRect(mouse_opening,ori_img)
    
    return ori_img,defect

# function to show the defect image and defects detected
def show_image():
    
    ori_img,img,input_img= input_image()
    ori_img,defect = input_template(ori_img, img)
    
    # resize the image to have a width of 1000 pixels and a height of 500 pixels
    image = cv2.resize(input_img, (1000, 700))

    # convert the image from BGR to RGB format
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # create a PhotoImage object from the image
    photo = ImageTk.PhotoImage(image=Image.fromarray(image))
    
    # open a file dialog to select an image
    image2 = cv2.resize(ori_img, (1000, 700))

    # convert the image from BGR to RGB format
    image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2RGB)

    # create a PhotoImage object from the image
    photo2 = ImageTk.PhotoImage(image=Image.fromarray(image2))
    
    # create a label to display the image on the left side of the window
    left_label = tk.Label(root, image=photo)
    left_label.image = photo
    left_label.grid(row = 0, column = 0, pady = 2)
    
    left_name_label = tk.Label(root, text="Input Image with Defect")
    left_name_label.grid(row = 1, column = 0, pady = 2)

    # create a label to display the image on the right side of the window
    right_label = tk.Label(root, image=photo2)
    right_label.image = photo2
    right_label.grid(row = 0, column = 1, pady = 2)
    
    right_name_label = tk.Label(root, text=f'Defect Detected: {defect}')
    right_name_label.grid(row = 1, column = 1, pady = 2)

if __name__ == '__main__':
    # create a button to open the file dialog and select an image
    # create the root window
    root = tk.Tk()
    root.geometry("2000x1200")
    root.title("Image Display")
    
    
    title_label = tk.Label(root,text = "Please Select An Image and Template to Detect Defects.")
    title_label.grid(row=2,column=0,sticky="nsew",columnspan = 2)
    open_button = tk.Button(root, text="Upload", command=show_image)
    open_button.grid(row = 3,column=0, columnspan=2)
    
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)
    root.grid_rowconfigure(2, weight=1)
    root.grid_rowconfigure(3, weight=1)

    # start the main event loop
    root.mainloop()
