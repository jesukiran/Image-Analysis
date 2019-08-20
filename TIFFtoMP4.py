from __future__ import division
import os
import cv2
import time
import numpy as np
import subprocess as sp
import logging
import glob
import csv

from datetime import timedelta

from skimage import exposure

from xml.dom import minidom
import wx_interface as wx_int

FFMPEG_BIN = '/imec/other/lensfree/public/opt/ffmpeg/ffmpeg'

class TIFFtoMP4():

    def __init__(self):

        self.actual_timestamp = []

    def read_timestamp_data(self, tiff_loc):

        """
        Reads the timestamp data.

        :param tiff_loc: Location of the timestamps (.txt) file
        :type tiff_loc: string

        :returns: timestamps

        """


        with open(tiff_loc + 'timestamps.txt') as inf:
            reader = csv.reader(inf, delimiter="\t")
            second_col = list(zip(*reader))[1]
            second_col = np.asarray(second_col).astype('int')

        np.savetxt(TC.tiff_loc +'timestamps.csv', np.c_[second_col], fmt='%f')

        self.actual_timestamp = np.asarray(second_col)

        return self.actual_timestamp


    def read_infile(self, tiffCounter):

        """
        Reads each frame and appends the corresponding timestamp data.

        :param tiffCounter: Number of (.tiff) files in folder.
        :type tiffCounter: int

        """

        for files in glob.glob("*.tiff"):
                f = os.path.splitext(files)[0]

        self.file_length = len(f)

        for i in range(0,tiffCounter,1):
            if self.file_length == 5:
                frm = cv2.imread('%05d.tiff'%i, 0)
            elif self.file_length == 6:
                frm = cv2.imread('%06d.tiff'%i, 0)
            frm = frm.astype(np.uint8)
            frm = cv2.cvtColor(frm, cv2.COLOR_GRAY2BGR)
            frm = exposure.adjust_gamma(frm, 2.5)

            val = int(self.actual_timestamp[i])
            time = str(timedelta(seconds=1e-6*val))

            cv2.putText(frm, time, (8,12), cv2.FONT_HERSHEY_PLAIN, 1.0, (255,255,255), 1)
            frm = cv2.cvtColor(frm, cv2.COLOR_BGR2YUV_I420)

            self.pipe.stdin.write(frm.tostring())

        self.pipe.terminate()
        self.actual_timestamp = []

    def write_outfile(self, filename):

        """
        Writes video as (.mp4) using FFMPEG.

        :param filename: Location where the (.mp4) needs to be saved.
        :type filename: string

        """

        self.outfile = 'IR_movie.mp4'
        print ('*** WRITING to: ', self.outfile)

        command = [ FFMPEG_BIN,
                '-y',                             # (optional) overwrite output file if it exists
                '-f', 'rawvideo',
                '-vcodec','rawvideo',
                '-pix_fmt', 'yuv420p',            # required as input format
                '-s', '%dx%d'%(640,512),          # size of one frame (WxH)
                '-r', str(98),                    # input frames per second
                '-an',                            # Tells FFMPEG not to expect any audio
                '-i', '-',                        # The imput comes from a pipe

                '-qscale:v', '1',                 # output video quality (lower q = bigger file)
                '-vcodec', 'libx264',             # output video codec

                '-crf', '5',
                '-c:v','libx264',
                '-preset','medium',
                '-profile:v','high',

                self.outfile ,
                '-hide_banner' ]

        self.pipe = sp.Popen( command, stdin=sp.PIPE )
        logging.info('Starting: ' + ' '.join(command))

        print ('DONE.')



if __name__ == '__main__':

    logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s",
                        datefmt='%Y-%m-%d %H:%M:%S',
                        level=logging.DEBUG)

    current_dir = wx_int.get_file()
    logging.info('Analyzing folders: ' + current_dir)

    for root, dirs, files in os.walk(current_dir):

        for filename in dirs:
            tiff_loc = current_dir + filename +'/'
            os.chdir(tiff_loc)
            tiffCounter = len(glob.glob1(tiff_loc,"*.tiff"))
            logging.info('Start Transcoding of %d files:'%tiffCounter)
            analyse = TIFFtoMP4()
            analyse.read_timestamp_data(tiff_loc)
            analyse.write_outfile(filename)
            analyse.read_infile(tiffCounter)
            time.sleep(1)
