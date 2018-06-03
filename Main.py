'''
BSD 3-Clause License

Copyright (c) 2018, Sagar Shivani
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistribution of this sofware without the permission of the owner will be 
  dealt as copyright hinderence and is a punishable offence.

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

* Neither the name of the copyright holder nor the names of its
  contributors may be used to endorse or promote products derived from
  this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''
# Main.py

import cv2
import numpy as np
import os
import gui3
import DetectChars
import DetectPlates
import PossiblePlate
import Tkinter as tk
from Tkinter import *
import PIL
from PIL import ImageTk,Image
import Tkinter, Tkconstants, tkFileDialog
import importlib

import unicodedata
filename=""

def browse_button():
    # Allow user to select a directory and store it in global var
    # called folder_path
    global filename
    filename =  tkFileDialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("jpeg files",".jpg"),("all files",".*")))
    img = Image.open(filename)
    img1=img.resize((400,300))
    img2=ImageTk.PhotoImage(img1)
    #print(img2)
    #canvas.create_image(20,20,anchor=NW,image=img2)
    print(filename)
    #label=Label(leftFrame, image=img2)
    #label.pack()
    #filename.open()
    print("IAM")
    print(filename)
    img = Image.open(filename)
    photo = ImageTk.PhotoImage(img)
    label1 = tk.Label(root, height=500, width=500, image=photo, compound='left')
    label1.pack()
    global g1
    g1=f(filename)
    root.mainloop()
    #import sagar
    #from sagar import vehi
    #Main.sagar()
#def f(filename):
#    global g
#    g=filename
#top = tkinter.Tk()
#C=tkinter.Canvas(top, bg="grey", height=600, width=600)
#C.pack()
#top.mainloop()
#veh = PhotoImage(file='C:/Users/Sagar/Desktop/Software Project/OpenCV_3_License_Plate_Recognition_Python/1.png'
#C.create_image(0, 0, anchor = NW, image=my_image)
def crt():
    root = Tk()
    leftFrame = Frame(root, width=200, height = 600)
    leftFrame.pack(side=LEFT)

    #root.geometry('500x500')
    canvas = Canvas(root,width=600,height=600);
    canvas.pack()

    button2 = Button(root,text="Browse", command=browse_button)
    button2.pack()
    button2.place(anchor=NW, )
    #bottomframe = Frame(root,width=200,height=100)
    #bottomframe.pack(side=BOTTOM)
    #bottomframe = tk.Label(root, image = img)
    #bottomframe.pack(side = "bottom", fill = "both", expand = "yes")
    root.mainloop()



SCALAR_BLACK = (0.0, 0.0, 0.0)
SCALAR_WHITE = (255.0, 255.0, 255.0)
SCALAR_YELLOW = (0.0, 255.0, 255.0)
SCALAR_GREEN = (0.0, 255.0, 0.0)
SCALAR_RED = (0.0, 0.0, 255.0)

showSteps = False


def main():
    print("Yes")
    crt()
    blnKNNTrainingSuccessful = DetectChars.loadKNNDataAndTrainKNN()         
    
    if blnKNNTrainingSuccessful == False:                               
        print "\nerror: KNN traning was not successful\n"               
        return                                                          
    # end if
    
    imgOriginalScene  = cv2.imread(filename)              
    
    if imgOriginalScene is None:                            
        print "\nerror: image not read from file \n\n"     
        os.system("pause")                                 
        return                                             
    # end if

    listOfPossiblePlates = DetectPlates.detectPlatesInScene(imgOriginalScene)           

    listOfPossiblePlates = DetectChars.detectCharsInPlates(listOfPossiblePlates)        

    cv2.imshow("imgOriginalScene", imgOriginalScene)           

    if len(listOfPossiblePlates) == 0:                          
        print "\nno license plates were detected\n"             
    else:                                                       
                

                
        listOfPossiblePlates.sort(key = lambda possiblePlate: len(possiblePlate.strChars), reverse = True)

                
        licPlate = listOfPossiblePlates[0]

        cv2.imshow("imgPlate", licPlate.imgPlate)           
        cv2.imshow("imgThresh", licPlate.imgThresh)

        if len(licPlate.strChars) == 0:                     
            print "\nno characters were detected\n\n"       
            return                                          
        # end if

        drawRedRectangleAroundPlate(imgOriginalScene, licPlate)             # draw red rectangle around plate

        print "\nlicense plate read from image = " + licPlate.strChars + "\n"       # write license plate text to std out
        print "----------------------------------------"

        writeLicensePlateCharsOnImage(imgOriginalScene, licPlate)           

        cv2.imshow("imgOriginalScene", imgOriginalScene)                

        cv2.imwrite("imgOriginalScene.png", imgOriginalScene)           

    # end if else

    cv2.waitKey(0)					

    return
# end main

###################################################################################################
def drawRedRectangleAroundPlate(imgOriginalScene, licPlate):

    p2fRectPoints = cv2.boxPoints(licPlate.rrLocationOfPlateInScene)            # get 4 vertices of rotated rect

    cv2.line(imgOriginalScene, tuple(p2fRectPoints[0]), tuple(p2fRectPoints[1]), SCALAR_RED, 2)         # draw 4 red lines
    cv2.line(imgOriginalScene, tuple(p2fRectPoints[1]), tuple(p2fRectPoints[2]), SCALAR_RED, 2)
    cv2.line(imgOriginalScene, tuple(p2fRectPoints[2]), tuple(p2fRectPoints[3]), SCALAR_RED, 2)
    cv2.line(imgOriginalScene, tuple(p2fRectPoints[3]), tuple(p2fRectPoints[0]), SCALAR_RED, 2)
# end function

###################################################################################################
def writeLicensePlateCharsOnImage(imgOriginalScene, licPlate):
    ptCenterOfTextAreaX = 0                             # this will be the center of the area the text will be written to
    ptCenterOfTextAreaY = 0

    ptLowerLeftTextOriginX = 0                          # this will be the bottom left of the area that the text will be written to
    ptLowerLeftTextOriginY = 0

    sceneHeight, sceneWidth, sceneNumChannels = imgOriginalScene.shape
    plateHeight, plateWidth, plateNumChannels = licPlate.imgPlate.shape

    intFontFace = cv2.FONT_HERSHEY_SIMPLEX                      # choose a plain jane font
    fltFontScale = float(plateHeight) / 30.0                    # base font scale on height of plate area
    intFontThickness = int(round(fltFontScale * 1.5))           # base font thickness on font scale

    textSize, baseline = cv2.getTextSize(licPlate.strChars, intFontFace, fltFontScale, intFontThickness)        # call getTextSize

            # unpack roatated rect into center point, width and height, and angle
    ( (intPlateCenterX, intPlateCenterY), (intPlateWidth, intPlateHeight), fltCorrectionAngleInDeg ) = licPlate.rrLocationOfPlateInScene

    intPlateCenterX = int(intPlateCenterX)              # make sure center is an integer
    intPlateCenterY = int(intPlateCenterY)

    ptCenterOfTextAreaX = int(intPlateCenterX)         

    if intPlateCenterY < (sceneHeight * 0.75):                                                  
        ptCenterOfTextAreaY = int(round(intPlateCenterY)) + int(round(plateHeight * 1.6))      
    else:                                                                                       
        ptCenterOfTextAreaY = int(round(intPlateCenterY)) - int(round(plateHeight * 1.6))      # write the chars in above the plate
    # end if

    textSizeWidth, textSizeHeight = textSize                # unpack text size width and height

    ptLowerLeftTextOriginX = int(ptCenterOfTextAreaX - (textSizeWidth / 2))           # calculate the lower left origin of the text area
    ptLowerLeftTextOriginY = int(ptCenterOfTextAreaY + (textSizeHeight / 2))          # based on the text area center, width, and height

            # write the text on the image
    cv2.putText(imgOriginalScene, licPlate.strChars, (ptLowerLeftTextOriginX, ptLowerLeftTextOriginY), intFontFace, fltFontScale, SCALAR_YELLOW, intFontThickness)
# end function

###################################################################################################
if __name__ == "__main__":
    main()


















