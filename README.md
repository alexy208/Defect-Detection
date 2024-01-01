## Project Description
This PCB Defect Detection System is a specialized tool designed to identify and highlight defects in printed circuit boards (PCBs). It serves a crucial role in quality assurance, ensuring PCBs are defect-free before they are used in larger assemblies. The system is capable of detecting a range of common PCB defects, including:
* Missing Hole: Detects if a hole that should be present in the PCB is missing.
* Mouse Bite: Identifies irregularities or small notches along the edge of the PCB, resembling a bite.
* Spur: Locates any unwanted, small copper areas extending from a PCB trace.
* Spurious Copper: Identifies any unwanted or excess copper on the PCB that could potentially cause short circuits.

# Project Setup Instructions
Before you begin, ensure you have Python installed on your system. 
Installation

1) Clone or Download the Project:
   use git clone to clone the repository, or download it as a ZIP file and extract it.
   ```bash
   git clone https://github.com/alexy208/Defect-Detection.git
   ```
   

2) Install Required Libraries:
   This project requires several Python libraries. You can install them using pip. Open your terminal or command prompt and navigate to the project directory, then run the following command:
   ```bash
   pip install numpy opencv-python matplotlib pillow
   ```
   
3) Running the Application
   Launch the Application:
   Open a terminal or command prompt.
   Navigate to the project directory.
   Run the following command:
   ```bash
   python gui.py
   ```
   
## How It Works

The system operates through a simple yet effective process:

1) Gui of the system
![image](https://github.com/alexy208/Defect-Detection/assets/126884588/d64757d2-5eca-4776-90e0-51dd5f5cb3b1)

3) Image Selection: The user starts by selecting an image of the defective PCB. This image is the subject of the inspection.
![image](https://github.com/alexy208/Defect-Detection/assets/126884588/ec11c0b0-4a26-4a56-ae4f-c6cad26022e7)

An example of the defect image (missing hole):
![04_missing_hole_01](https://github.com/alexy208/Defect-Detection/assets/126884588/fd9e542a-e0f7-4803-94db-08da5e2f4260)

5) Template Selection: Next, the user selects an image of a template PCB. This image represents a defect-free version of the PCB and serves as a benchmark for comparison.
![image](https://github.com/alexy208/Defect-Detection/assets/126884588/b5eda8f6-72d3-45f6-a3e5-05ca85ce3f0e)

An example of the defect free image (missing hole):
![04](https://github.com/alexy208/Defect-Detection/assets/126884588/259a979e-4631-4e0c-badb-82fcb68fd954)

7) Defect Detection: The system then compares the defective PCB image with the template. It uses sophisticated algorithms to identify discrepancies between the two images, focusing on the specified defect types (missing holes, mouse bites, spurs, and spurious copper).

8) Highlighting Defects: Once a defect is detected, the system highlights it with a red box on the defective PCB image. This visual cue makes it easy to identify and locate the defects.
![image](https://github.com/alexy208/Defect-Detection/assets/126884588/15438b58-e9c8-42e1-a7cf-0db17635fe7b)

9) Result Presentation: The final output is presented to the user, showing the defective PCB image with clearly marked defects. This allows for quick assessment and decision-making regarding the PCB's quality and further actions.

Through its user-friendly interface and robust detection capabilities, this PCB Defect Detection System streamlines the process of PCB quality control, making it more efficient and reliable.

## Examples of detecting different types of defects:

Mouse Bite:
![image](https://github.com/alexy208/Defect-Detection/assets/126884588/59916d8e-78f6-4bbc-99ec-5bfee3df3ff2)

Spur:
![image](https://github.com/alexy208/Defect-Detection/assets/126884588/e7574e76-655b-42b3-914c-c0056f20ef1d)

Spurious Copper:
![image](https://github.com/alexy208/Defect-Detection/assets/126884588/d374b715-eeea-4c1e-a3a2-14ac1391d832)

# Technical Details
## Overview

The PCB Defect Detection System employs a combination of image processing techniques using Python libraries such as NumPy, OpenCV (cv2), and Matplotlib. The system is designed to detect four types of defects in PCB images: Missing Hole, Mouse Bite, Spur, and Spurious Copper.

## Core Functions
1. Region Growing Algorithm

    The region_growing function is central to detecting specific defect types.
    It works by expanding a seed point to adjacent areas based on predefined connectivity and threshold criteria.
    The function processes a grayscale image (r_img) and a binary mask (defec) indicating potential defect regions.
    It uses a combination of seed point initiation, boundary conditions, and a loop mechanism to grow the region until it encompasses the entire defect area.

2. Defect Detection and Highlighting

    The drawRect function identifies contours in the defect masks and draws red rectangles around detected defects on the original PCB image.
    For each defect type, the system performs specific image processing operations such as thresholding, masking, and morphological operations to isolate defect regions.
    Based on the processed images, the system then classifies and highlights each defect.

## Image Processing Workflow

- The program begins by reading template PCB images and corresponding defect images.
- It performs color range extraction and binary thresholding to isolate regions of interest.
- The system uses bitwise operations, grayscale conversion, and morphological transformations to prepare images for defect detection.
- The detection logic involves comparing the processed images against the template, identifying discrepancies, and classifying the type of defect.
- Each identified defect is then highlighted using the drawRect function.

# Acknowledgement
- This project utilizes the PCB Defects dataset available on Kaggle, provided by [Akhatova](https://www.kaggle.com/datasets/akhatova/pcb-defects). This dataset has been instrumental in testing the defect detection capabilities of this system.
    
