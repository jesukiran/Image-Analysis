import os
import cv2
import time
import numpy as np
import subprocess as sp
import logging
import glob
import struct
from datetime import datetime as DT
from multiprocessing import Pool
import wx_interface as wx_int

FFMPEG_BIN = '/imec/other/lensfree/public/opt/ffmpeg/ffmpeg'
#FFMPEG_BIN = 'C:/FFMPEG/bin/ffmpeg'

class XVItoMP4():

    def __init__(self):

        pass


    def get_parameters(self, fn):

        """
        Reads the header of the (.xvi) video and extracts dimensions of frame (W,H) and frames per second (FPS).

        :param fn: Location of the (.xvi) videos to be converted to (.mp4)
        :type fn: string

        :returns: W, H, FPS

        """

        with open(fn, 'rb') as infile:

            buf = infile.read(30)
            hdr = np.frombuffer(buf, dtype='uint16')
            self.W = int(hdr[8])
            self.H = int(hdr[10])

            FPSi = int(hdr[12])

        print ('*** Found size=', (self.W,self.H), ' and FPS=', FPSi)

        fsz = os.stat(fn).st_size
        print ('*** File size=', fsz*1e-6, 'MB => Frames=', int(fsz / (self.W*self.H*2)))

        self.FPS = FPSi if FPSi < 100 else 100

        return self.W, self.H, self.FPS

    def read_infile(self, fn):

        """
        Reads each frame and appends the corresponding timestamp data.

        :param fn: Location of the (.xvi) video in processing.
        :type fn: string

        """

        with open(fn, 'rb') as infile:
            infile.seek(1024)
            TS1 = None
            while True:
                try:
                    #read frame bytes into buffer
                    buf = infile.read(self.W*self.H*2)

                    ftb = infile.read(32) # footer data read
                    '''
                    Footer information table:
                    ------------------------
                    unsigned short     len     Structure length.
                    unsigned short     ver     Fixed to 0xAA00.
                    long long          soc     Time of Start Capture
                    long long          tft     Time of reception
                    dword              tfc     Frame counter
                    dword              fltref  Reference for attaching messages/frame
                    dword              hfl     Hardware footer length
                    '''
                    ftm,fct = struct.unpack_from('qI', ftb, offset=12)

                    if fct == 0: continue

                    frm = np.frombuffer(buf, dtype='uint16').reshape(self.H,self.W)
                    # Make changes below.
                    frm = frm / 16
                    frm = frm.astype(np.uint8)
                    frm = cv2.cvtColor(frm, cv2.COLOR_GRAY2BGR)

                    TS = DT.fromtimestamp(1.0e-6 * ftm)
                    if fct == 1: TS1 = TS
                    minutes, seconds = divmod((TS - TS1).total_seconds(), 60)
                    timest = '%02d:%09.6f' % (minutes, seconds)

                    cv2.putText(frm, timest, (8,12),
                            cv2.FONT_HERSHEY_PLAIN, 1.0, (255,255,255), 1)

                    frm = cv2.cvtColor(frm, cv2.COLOR_BGR2YUV_I420)
                    self.pipe.stdin.write( frm.tostring() )

                except Exception as err:

                    break
        self.pipe.terminate()

        if os.path.getsize(self.outfile) < 8:
            os.remove(self.outfile)

    def write_outfile(self, fn):

        """
        Writes video as (.mp4) using FFMPEG.

        :param fn: Location where the (.mp4) needs to be saved.
        :type fn: string

        """

        self.outfile = fn[:-4] + '.mp4'

        if os.path.exists(self.outfile): return
        print ('*** WRITING to: ', self.outfile)

        command = [ FFMPEG_BIN,
                '-y',                             # (optional) overwrite output file if it exists
                '-f', 'rawvideo',
                '-vcodec','rawvideo',
                '-pix_fmt', 'yuv420p',            # required as input format
                '-s', '%dx%d'%(self.W,self.H),    # size of one frame (WxH)
                '-r', str(self.FPS),              # input frames per second
                '-an',                            # Tells FFMPEG not to expect any audio
                '-i', '-',                        # The imput comes from a pipe

                #'-qscale:v', '5',                # output video quality (lower q = bigger file)
                '-vcodec', 'libx264',             # output video codec

                '-crf', '15',
                '-c:v','libx264',
                '-preset','medium',
                '-profile:v','high',

                self.outfile ,
                '-hide_banner' ]

        self.pipe = sp.Popen( command,
                     stdin=sp.PIPE )
        logging.info('Starting: ' + ' '.join(command))




if __name__ == '__main__':

    logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s",
                        datefmt='%Y-%m-%d %H:%M:%S',
                        level=logging.DEBUG)

    current_dir = wx_int.get_file()
    logging.info('Analyzing folders: ' + current_dir + '*.xvi')

    os.chdir(current_dir)
    flist = glob.glob('*.xvi')

    fns = []
    for fn in flist:
        if not os.path.exists(fn.replace('.xvi','.mp4')):
            fns += [fn]
    flist = fns

    logging.info('Start Transcoding of %d files:'%len(flist))
    analyse = XVItoMP4()

    if 1:
        ## Serial Trans-Coding
        for fn in flist :
            analyse.get_parameters(fn)
            analyse.write_outfile(fn)
            analyse.read_infile(fn)
            time.sleep(1)
            print ("\n DONE!")

    else:
        ## Parallel-Pool Trans-Coding
        pool    =  Pool(processes=8)
        results = [pool.apply_async(analyse.get_parameters(fn),
                                    analyse.write_outfile(fn),
                                    analyse.read_infile(fn), args=(fn,)) for fn in fns]
        results = [p.get() for p in results]
