# TomoAcquire
![OS](https://img.shields.io/badge/os-Windows-lightgray)
![Code](https://img.shields.io/badge/python-3.4-yellow)
![License](https://img.shields.io/badge/license-GPL3.0-blue)
![Version](https://img.shields.io/badge/version-v0.0.1-blue)
![Testing](https://img.shields.io/badge/test-Experimental-orange)

## 1. Description

The TomoAcquire (tomoacquire) library is a toolkit for acuiring images using novel tilting schmes during scanning transmission electron tomography (STEM). It is a temscript software that allows a user to connect to a microscope and perform an experiment. Please Note:  This is a pre-release tkinter gui intended for usage on FEI microscopes running python 3.4 and up - The first stable release is intended to run on a remote pc accessing the microscope pc. 

Requires tkinter, numpy and temscript are available on the microscope pc.

## 3. Usage
To use download the folder tomogui and copy it onto the microscope. The following command, will open the tkinter gui. 

```bash
python -B -m tomogui.main
```

Open the imaging tab 
 - Select the detectors used for imaging
 - For scannning and acquisition select the image size, dwell time (us) and frame time (s). The frame time is the number of pixels multiplied by the dwell time plus a lag. The appropriate frame time can be found in TIA in the scanning menu.
 - Confirm the imaging settings.

Enter the tomography menu
 - Select the a file to save the data to (supported file types h5).
 - Select a tilt scheme and set the start and end angles.
 - In options select backlash corrected and manual acquisition - all other options must be deselected.
 - Confirm Settings

In the Experiment tab, adjust focus and tracking using the microscope controls and select next angle to acquire the next projection. 

## 4. License
This code is licensed under GNU general public license version 3.0.



