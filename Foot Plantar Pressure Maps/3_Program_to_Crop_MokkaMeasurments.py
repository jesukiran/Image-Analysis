##################################################################################
#############                                                      ###############
#############  PROGRAM TO CROP THE MOKKA GAIT MEASUREMENTS IMAGES  ###############
#############                                                      ###############
############# Please Note: The crop values are set on a trial-and  ###############
#############    -check method. Please change if it deems needful. ###############
#############                                                      ###############
#############                                                      ###############
#############  Author  : Jesu Kiran Spurgen                        ###############
#############                                                      ###############
#############                                                      ###############
#############                                                      ###############
#############                                                      ###############
#############                                                      ###############
##################################################################################


##################################################################################
##################################################################################
#############                                                      ###############
#############                 INPUT FOR THIS CODE                  ###############
#############                                                      ###############
#############  TIME_FRAMEWISE MEASUREMENTS (.png/.jpg) FROM MOKKA  ###############
#############       DIMENSIONS OF THIS IMAGE: 2127 x 1113          ###############
#############                                                      ###############
#############                                                      ###############
##################################################################################
##################################################################################




# Import required Python libraries
import cv2
import numpy as np
from PIL import Image
import os

# Point this as the main directory
src = 'C:/Users/jkspu/Desktop/'

os.chdir(src)

inpdest = os.path.join(src, 'Measurements_Input')
os.mkdir('Measurements_Output')
outdest = os.path.join(src, 'Measurements_Output')

class Bild:
    def __init__(self, img_name):
        self.img = cv2.imread(img_name)
        self.__name = img_name
        self.r = 800.0/self.img.shape[1]
        self.dim = (800, int(self.img.shape[0] * self.r))
        #self.img_res = cv2.resize(self.img, dim, interpolation = cv2.INTER_AREA)
           
    def __str__(self):
        return self.__name

    def resize(self):
        
        self.img_res = cv2.resize(self.img, self.dim, interpolation = cv2.INTER_AREA)                                                  
        return self.img_res

    def crop(self):
        
        self.cropped = self.img[50:1120, 600:1830]
        return self.cropped

    def save_image(self):
        
        self.save = cv2.imwrite('cropped_measurements_'+str(i)+'.jpg', self.cropped)
        return self.save
        

if __name__ == '__main__':
    
    file_start = 411
    file_end   = 532
    
    for i in range(file_start, file_end, 1):
        os.chdir(inpdest)
        inpimage = Bild('PAD_Dyn_Right_04'+str(i)+'.png')
        #inpimage.resize()
        inpimage.crop()
        os.chdir(outdest)
        inpimage.save_image()
        os.chdir(inpdest)

print ("The cropped gait measurments can found here: " + outdest)

##################################################################################
#############           O P T I O N A L    S E C T I O N           ###############
#############                                                      ###############
#############      RESIZE THE (.jpg) IMAGE FILE AND SAVE IT IN     ###############
#############                IMAGE FORMAT (.jpg)                   ###############
##################################################################################

    # Resize the image according to the dimensions mentioned in maxsize
    #maxsize = (480, 763)
    
    #for i in range(file_start,file_end,1):
    #    img = Image.open('Z:/to_Jesu/meas/Out/Output_'+str(i)+'.jpg')
    #    img = img.resize(maxsize)
    #    img.save('Z:/to_Jesu/meas/Resize/img'+'_'+ str(i)+'.jpg')
        
##################################################################################
#############               C H A N G E S    L O G                 ###############
#############                                                      ###############
#############     DOCUMENT THE CHANGES MADE IN THE FOLLOWING       ###############
#############                    FORMAT                            ###############
##################################################################################


# Last Changes Made on 19-Dec-2017 at 1:28 PM   
# Last Changes Made on 15-Dec-2017 at 1:12 PM   
        
        
        
