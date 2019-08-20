##################################################################################
#############                                                      ###############
#############      PROGRAM TO READ A (.CSV) FILE TO GRAPH THE      ###############
#############            GROUND REACTION FORCE (GRF)               ###############
#############                                                      ###############
#############                                                      ###############
#############  Author  : Jesu Kiran Spurgen                        ###############
#############                                                      ###############
#############                                                      ###############
#############                                                      ###############
#############  !! FOR RESEARCH PURPOSES ONLY  !!                   ###############
#############                                                      ###############
##################################################################################



##################################################################################
##################################################################################
#############                                                      ###############
#############                 INPUT FOR THIS CODE                  ###############
#############                                                      ###############
#############                FORCE PLATE DATA (.csv)               ###############
#############                                                      ###############
#############     Before using this (.csv) file, replace all       ###############
#############     commas (,) with a fullstop (.) and save it.      ###############
#############                                                      ###############
##################################################################################
##################################################################################





# Import required Python libraries
from __future__ import division
import numpy as np
import csv
import csv_splitter
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import animation
import matplotlib.colors as cm
from scipy import ndimage
from PIL import Image
import cv2
import os


# Define some easy-to-switch plotting styles which can be tweaked as per requirement
label_size = 8
plt.rcParams['xtick.labelsize'] = label_size
plt.rcParams['ytick.labelsize'] = label_size

# Image/Video Writer: FFMPEG
plt.rcParams['animation.ffmpeg_path'] = unicode ('C:/FFMPEG/bin/ffmpeg.exe')

##################################################################################
#############               S E C T I O N    O N E                 ###############
#############                                                      ###############
############# PRE-PROCESS THE (.CSV) FILE TO MAKE IT USABLE FOR    ###############
#############               FURTHER PROCESSING                     ###############
##################################################################################

# Pre-process the (.csv) file by removing spaces/blanks and saving it into one file

# Point this as the main directory
src = 'C:/Users/jkspu/Desktop/Force_Input'
os.chdir(src)
os.mkdir('GRF_Orig')
origdest = os.path.join(src, 'GRF_Orig')

os.mkdir('GRF_Resize')
resdest = os.path.join(src, 'GRF_Resize')


# Rename the Dynamic Rolloff file as 'GaitPressure.csv'
input_file_name = 'Force' + '.csv'
input_file = os.path.join(src, input_file_name)
print(" The input force file processing right now is : " + input_file)

#input_file  = 'C:/Users/jkspu/Desktop/Force.csv'

output_file_name = 'TmpOutput' + '.csv'
output_file = os.path.join(src, output_file_name)
print(" Please find all the frames of gait pressure here : " + output_file)

#output_file = 'C:/Users/jkspu/Desktop/Op.csv'

with open(input_file,'r') as input, open(output_file, 'w') as output:
    
    try:
        read = csv.reader(input)
        for r in read:
            non_blank = (line for line in input if line.strip())            
            for i in range(17):
                next(read)                
            output.writelines(non_blank)
            
    finally:
        print("Done! TmpOutput is complete!")

##################################################################################
#############               S E C T I O N    T W O                 ###############
#############                                                      ###############
############# PRE-PROCESS THE (.CSV) FILE TO MAKE IT USABLE FOR    ###############
#############     FURTHER PROCESSING BY PREPARING THE DATA         ###############
##################################################################################
        
# np.genfromtxt is used to read a .csv, the delimiter here is tab         
data_orig = np.genfromtxt(output_file, dtype =int, delimiter = ",")

# Required to sync with the plots from PP
# Important Note: These values need to be tweaked in accordance with the width and height
# of the plots that we need finally. In this program though, the resizing option in Section five does the job.
w = 778
h = 767

# dpi of my screen (WS-01)
my_dpi = 166
fig = plt.figure(figsize=(778/my_dpi, 767/my_dpi), dpi=my_dpi)

# The actual place where it starts is 414 (415). 3 before is 411 (412). Total 524 frames. To end at 524, we do 525.
X = data_orig[412:525,1]

for i in range (1, len(X-1)):
    X[0] = 0
    X[i] = X[0] + (5*i)
    
# Divide by 1000 to get values in seconds. 
X = (X/1000)
# Division is only possible if the module above ( from __future__ import division ) is imported


Y1 = data_orig[412:525,4]
Y2 = data_orig[412:525,3]
Y3 = data_orig[412:525,2]

# Uncomment the folloing line to plot all 3 graphs
#plt.plot(X, Y1, 'r-', X, Y2, 'b--', X, Y3, 'g--')

##################################################################################
#############               S E C T I O N    T H R E E             ###############
#############                                                      ###############
#############         PLOT THE DATA USING MATPLOTLIB MODULES       ###############
#############                                                      ###############
##################################################################################

plt.plot(X, Y1, 'r-')
plt.margins(x=0)
plt.margins(y=0)
plt.axhline(0, color='black', linestyle='--')
plt.grid(True, linestyle='--')
plt.title('Ground Reaction Force (GRF)', fontsize=13)

plt.xlabel('Time [s]', fontsize=10)
plt.ylabel('Force [N]', fontsize=10)


##################################################################################
#############               S E C T I O N    F O U R               ###############
#############                                                      ###############
#############     CREATE THE ANIMATION LINE AND SAVE THE FRAMES    ###############
#############                                                      ###############
##################################################################################

X_MIN = 0.0
X_MAX = 0.6
Y_MIN = 0.0
Y_MAX = 1200

# Change the step size values according to the time-steps 
step_size = 0.005

X_VALS = np.arange(X_MIN, X_MAX+0.005, 0.005);


def update_line(num, line):
    i = X_VALS[num]
    line.set_data( [i, i], [Y_MIN, Y_MAX])
    os.chdir(origdest)
    plt.savefig("grf"+"_"+str(num+1)+".jpg", dpi = my_dpi)
    os.chdir(src)
    return line,

l , v = plt.plot(0, 0, 0.6, 1200, linewidth=2, color='gold')

anim = animation.FuncAnimation(fig, update_line, len(X_VALS), fargs=(l, ), interval=15, blit=False, repeat=False)

# Documentation can be found here ---> https://matplotlib.org/api/_as_gen/matplotlib.animation.FFMpegWriter.html
FFwriter = animation.FFMpegWriter(fps=1, extra_args=['-vcodec', 'libx264'])

#anim.save('basic_animation.mp4', writer = FFwriter)
plt.show()

##################################################################################
#############               S E C T I O N    F I V E               ###############
#############                                                      ###############
#############       RESIZE THE GRAPHS ACCORDING TO REQUIREMENT     ###############
#############                                                      ###############
##################################################################################

# Set the resize parameters
maxsize = (980, 1063)

for i in range(1,122,1):
    os.chdir(origdest)
    img = Image.open('grf'+'_'+ str(i)+'.jpg')
    img = img.resize(maxsize)
    os.chdir(resdest)
    img.save('GRF'+'_'+ str(i)+'.jpg')

print ("The plotted GRF measurments can found here: " + origdest)
print ("The resized GRF measurments can found here: " + resdest)
    
    
##################################################################################
#############               C H A N G E S    L O G                 ###############
#############                                                      ###############
#############     DOCUMENT THE CHANGES MADE IN THE FOLLOWING       ###############
#############                    FORMAT                            ###############
##################################################################################

# Last Changes Made on 19-Dec-2017 at 1:53 PM
# Last Changes Made on 15-Dec-2017 at 11:13 AM

