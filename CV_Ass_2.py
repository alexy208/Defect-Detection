# -*- coding: utf-8 -*-
"""
Created on Thu Mar  9 11:14:51 2023

@author: 60183
"""
import numpy as np
import cv2
import matplotlib.pyplot as plt
import os
from os import listdir
from os.path import isfile, join

#os.chdir('C:/Users/Alex/Desktop/CV Assignment')

path = ["Missing_hole","Mouse_bite","Spur","Spurious_copper"]
img_class = [4,5]



def region_growing(r_img,defec):
    
    row,col = np.where(defec == 255)
    # to set the connectivity of region growing
    directions = [(0,-1), (1,0),(0,1),(-1,0)]
    
    # to set the seed point
    seeds = [(row[0],col[0])]
    
    # to get the shape of the input image
    ver,hon = r_img.shape
    
    # create a mask with the shape of the input image
    r_mask = np.zeros(shape=(r_img.shape), dtype=np.uint8)
    count = 0
    status = False
    
    for num in range(len(seeds)):
        seeds2 =[]
        seeds2.append(seeds.pop(0))
        
        for seeding in seeds2:
            count += 1
            if count == 5000:
                status = True
                break
            # to obtain the position of the seeds
            x = seeding[1]
            y = seeding[0]
            
            # setting the seedpoint to 255
            r_mask[y][x] = 255
            
            # to grow the seed in the directions stated before
            
            for direct in directions:
                
                # if position is within size of the image, grow
                if x<hon-1 and x>0 and y < ver-1 and y>0:
                    current_x = x + direct[1]
                    current_y = y + direct[0]
                    
                # else continue with the current position
                else:
                    current_x = x
                    current_y = y
                
                                    
                # if the current location reaches border of the image, 
                # or the current pixel intensity is not 0 (indicates not part of defect)
                # ignore and continue the loop
                if current_x >= hon-1 or current_y >= ver-1 or r_img[(current_y,current_x)] ==255:
                    continue
                
                # if the current location has not been visited
                # and the current pixel intensity is == 0 (indicates part of the defect)
                # set the pixel intensity to 255 in mask
                # append the location as next seed point
                
                if (not r_mask[current_y][current_x]) and r_img[(current_y,current_x)] ==0 :
                    r_mask[current_y][current_x] = 255
                    seeds2.append((current_y,current_x)) 
            
            if status:
                break
            
    return r_mask

#function used to draw rectangular box on the image
def drawRect(defec,ori):
    contours, _ = cv2.findContours(defec, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(ori, (x-20, y-20), (x+w+20, y+ h+20), (0,0,255), 2)

if __name__ == '__main__': 
    for n in img_class:
        template_ori = cv2.imread(f'PCB_DATASET/PCB_USED/0{n}.jpg')
        #template = cv2.imread('PCB_DATASET/PCB_USED/01.jpg',0)
        template_gray= cv2.cvtColor(template_ori, cv2.COLOR_BGR2GRAY)
        template_rgb = cv2.cvtColor(template_gray, cv2.COLOR_BGR2RGB)

        # Define the color range to extract (here we're extracting green)
        lower = np.array([0,0, 0])
        upper = np.array([35, 80, 10])

        mask_temp = cv2.inRange(template_ori, lower, upper)
        # Apply the mask to the template
        output = cv2.bitwise_and(template_ori, template_ori, mask=mask_temp)
        output_gray_temp = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
        #output_gray_temp = cv2.cvtColor(output_gray_temp, cv2.COLOR_BGR2RGB)
        ret, output_bw_temp = cv2.threshold(output_gray_temp, 20, 255, cv2.THRESH_BINARY)
        defect_list = []
        for classes in path:
            mypath =f'PCB_DATASET/images/0{n}/{classes}'
            onlyfiles = [f for f in listdir(mypath) if isfile (join(mypath,f))]
            images = [cv2.imread(f'{mypath}/{x}') for x in onlyfiles]
            output_img = []
            
            for ori_img in images:
                img = cv2.cvtColor(ori_img, cv2.COLOR_BGR2GRAY)
                
                kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        
                missing_binary_mask = np.uint8(img > 80)
                missing_temp_mask = np.uint8(template_gray >80)
                
                missing_output = np.uint8(missing_temp_mask^missing_binary_mask)
                missing_opening = cv2.morphologyEx(missing_output, cv2.MORPH_OPEN, kernel)
                 
                # Create a mask based on the color range
                mask = cv2.inRange(ori_img, lower, upper)
                
                # Apply the mask to the original image
                output = cv2.bitwise_and(ori_img, ori_img, mask=mask)
                output_gray = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
                #output_gray = cv2.cvtColor(output_gray, cv2.COLOR_BGR2RGB)
                ret, output_bw = cv2.threshold(output_gray, 20, 255, cv2.THRESH_BINARY)
                
                mouse_output = output_bw_temp ^ output_bw
                mouse_opening = cv2.morphologyEx(mouse_output, cv2.MORPH_OPEN, kernel)
        
                spur_output = output_bw_temp - output_bw
                spur_opening = cv2.morphologyEx(spur_output, cv2.MORPH_OPEN, kernel)
                
                if np.sum(missing_opening ==1) >10:
                    print("Defect is missing hole")
                    defect = "Missing_hole"
                    drawRect(missing_opening,ori_img)
                    
                    
                else:
                    if np.sum(spur_opening==255) != 0:
                        r_mask = region_growing(output_bw,spur_opening)
                        if np.sum(r_mask==255)<3000:   
                            print("Defect is Spurious Copper")
                            defect = "Spurious_copper"
                        
                        else:
                            print("Defect is Spur")
                            defect = "Spur"
                            
                        drawRect(spur_opening,ori_img)
                    else:
                        print("Defect is mouse bite")
                        defect = "Mouse_bite"
                        drawRect(mouse_opening,ori_img)
                if defect == classes:
                    defect_list.append(1)
                else:
                    defect_list.append(0)         
                output_img.append(ori_img)
            
            #writing the output as jpeg
            # output_path = f'PCB_DATASET/Output/0{img_class}/{classes}'
            # for num, x in enumerate(output_img):
            #     cv2.imwrite(os.path.join(output_path, onlyfiles[num]),x)
        
        #Evaluation
        #Evaluate based on number of correctly detected defect images/ number of images
        if n ==4:
            Accuracy_04 = defect_list.count(1)/len(defect_list)
        else:
            Accuracy_05 = defect_list.count(1)/len(defect_list)
    
    overall_acc = (Accuracy_04 + Accuracy_05)/2

    print(f'Accuracy of image class 04: {Accuracy_04}')
    print(f'Accuracy of image class 05: {Accuracy_05}')
    print(f'Overall Accuracy: {overall_acc}')
