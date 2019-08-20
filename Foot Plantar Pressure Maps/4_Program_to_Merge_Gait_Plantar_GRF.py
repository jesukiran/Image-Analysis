##################################################################################
#############                                                      ###############
#############           PROGRAM TO MERGE ALL 3 PLOTS               ###############
#############   GAIT LAB MEASUREMENTS + PLANTAR_PRESSURES + GRF    ###############
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
#############                    IMAGES FROM                       ###############
#############   GAIT LAB MEASUREMENTS + PLANTAR_PRESSURES + GRF    ###############
#############                                                      ###############
#############     Before using this (.csv) file, replace all       ###############
#############     commas (,) with a fullstop (.) and save it.      ###############
#############                                                      ###############
##################################################################################
##################################################################################

# Import required Python libraries
import cv2
import numpy as np
from PIL import Image


class Merge:
    
    def __init__(self, img1, img2, img3):
        self.img1 = cv2.imread(img1)
        self.img2 = cv2.imread(img2)
        self.img3 = cv2.imread(img3)

    def merge_image(self):
        h1 , w1 = self.img1.shape[:2]
        h2 , w2 = self.img2.shape[:2]
        h3 , w3 = self.img3.shape[:2]
        self.combine = np.zeros((max(h1, h2, h3), w1+w2+w3,3), np.uint8)
        self.combine[:h1, :w1, :3] = self.img1
        self.combine[:h2, w1:w1+w2, :3] = self.img2
        self.combine[:h3, w1+w2:w1+w2+w3, :3] = self.img3
        return self.combine

    def save_image(self):
        self.save = cv2.imwrite('C:/Users/jkspu/Desktop/Merge_Measurments/Mergedoutput_' + str(j) + '.jpg', self.combine)
        return self.save

if __name__ == '__main__':
    
    # Set the start and stop values for reading the files (change as per requirement)
    file1_start = 411
    file1_stop  = 532
    file2_start = 1
    file2_stop  = 122
    file3_start = 1
    file3_stop  = 122

    # Merge the 3 image datasets
    for i, j, k in zip(range(file1_start,file1_stop,1), range(file2_start, file2_stop, 1), range(file3_start, file3_stop, 1)):
        inpimages = Merge('C:/Users/jkspu/Desktop/Measurements_Output/cropped_measurements'+'_'+str(i)+'.jpg', 'C:/Users/jkspu/Desktop/PP_Input/PP/PP_Resize/resized_PP'+'_'+str(j)+'.jpg', 'C:/Users/jkspu/Desktop/Force_Input/GRF_Resize/GRF'+'_'+str(k)+'.jpg')
        inpimages.merge_image()
        inpimages.save_image()

    print ("Done! Please find the measurement files in the location : C:/Users/jkspu/Desktop/Merge_Measurments/ ")


start_1 = 1
stop_1 = 122
start_2 = 1
stop_2 = 122

for j, k in zip(range(start_1, stop_1, 1), range(start_2, stop_2, 1)):
    list_im = ['C:/Users/jkspu/Desktop/Merge_Measurments/Mergedoutput_'+str(j)+'.jpg', 'C:/Users/jkspu/Desktop/Merge_Simulation/cc_Job-39_incr_'+str(k)+'.png' ]
    imgs    = [ Image.open(i) for i in list_im ]
    
    # pick the image which is the smallest, and resize the others to match it (can be arbitrary image shape here)
    min_shape = sorted( [(np.sum(i.size), i.size ) for i in imgs])[0][1]
    imgs_comb = np.hstack( (np.asarray( i.resize(min_shape) ) for i in imgs ) )

    imgs_comb = np.vstack( (np.asarray( i.resize(min_shape) ) for i in imgs ) )
    imgs_comb = Image.fromarray( imgs_comb)
    imgs_comb.save( 'C:/Users/jkspu/Desktop/Measurements_vs_Simulation/Output_'+str(k)+'.jpg' )


print ("Success! Please find the merged files in the location : C:/Users/jkspu/Desktop/Measurements_vs_Simulation/")


##################################################################################
#############               C H A N G E S    L O G                 ###############
#############                                                      ###############
#############     DOCUMENT THE CHANGES MADE IN THE FOLLOWING       ###############
#############                    FORMAT                            ###############
##################################################################################

# Last Changes Made on 15-Dec-2017 at 12:49 PM    

