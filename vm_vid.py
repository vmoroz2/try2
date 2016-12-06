# video functions based on ffmpeg.exe and on cv2 (for motion)
# vid_get_prop()
# vid_split()
# vid_merge()
# vid_motion()
# vid_show()
# ffmpeg man, openCV man
#--- cam education ---
# iso - some sensor current (noisy for low light/high iso)
# aperture = diafragma
# large sensor size - need longer focal length, lower depth of field = glubina rezkosti
# better sensitivity in low light
# video file has metadata with rotate; video flip often means recoding
import os,glob,subprocess;
from vm0 import *

v=lambda:None; v.q,v.sy=('/mnt/hgfs/D/py/','lin') if sys.platform.lower()[:3]=='lin' else ('D:/scan0/py/','win');
fnm0='/usr/bin/ffmpeg' if sys.platform.lower()[:3]=='lin' else'C:/Programs/auVideo/videoConverter_Total/ffmpeg.exe'; # fnm00='D:/scan0/cam/ffmpeg/bin/ffmpeg.exe'
def vid_get_prop(fnm): # h,w,fps,xx
  o1=sh(fnm0+' -i '+fnm); k=o1.find('Video:'); assert -1<k; o=o1[k:].split('\n')[0].split(', '); o[-1]=o[-1].replace(' (default)','').replace('\r','');
  o=o if len(o)==9 else o[:3]+o[2:] if len(o)==8 else o[:3]+o[2:3]+o[2:]; print o # , len(o)
  if (o[5][-4:],o[6][-4:],o[7][-4:],o[8][-4:])!=(' fps',' tbr',' tbn',' tbc'):
    print 'bad vid format in_'+fnm; # assert 0;
  q=o[3].split('x'); q[1]=q[1][:q[1].find(' ')] if -1<q[1].find(' ') else q[1];
  res=[int(q[1]),int(q[0]),float(o[5][:-4]),o[0][7:o[0].find(' ',7)]]; # q=o[0][o[0].find('(')+1:]; res+=[q[:q.find(' ')]]; 
  k=o1.find('Audio:'); res+=[o1[k:].split('\n')[0] if -1<k else '']; return res;
  # Video: mjpeg (MJPG / 0x47504A4D), yuvj420p(pc, bt470bg/unknown/unknown), 640x480, 230 kb/s, 100 

def vid_split(fnm,t): # vid_split(dir2+'20150613_0927_2103.mp4','04:48:40')
  cmd=fnm0+' -i '+fnm+' -vcodec copy -acodec copy -t ' +t+' '+fnm[:-4]+'_start.mp4';  subprocess.call(cmd)
  cmd=fnm0+' -i '+fnm+' -vcodec copy -acodec copy -ss '+t+' '+fnm[:-4]+'_end.mp4';    subprocess.call(cmd)

def vid_merge(fnm_list,fnm_out,A='-c:v copy -c:a copy'):
  fnm_list=fnm_list if isinstance(fnm_list,list) else [fnm_list]; n=len(fnm_list);
  if 0 and 1<n:
    o2=vid_get_prop(fnm_list[0]);
    for fnm in fnm_list[1:]:
      try:  assert vid_get_prop(fnm)==o2; # [480, 640, 100, 'MJPG', o2];
      except: print 'bad vid format in '+fnm; # assert 0;
  if 1<n:
    fnm1=v.q+fnmT(); fd=open(fnm1,'w'); [fd.write('file \''+q+'\'\n') for q in fnm_list]; fd.close();
    fnm1=fnm1 if v.sy=='lin' else fnm1.replace('/','\\');
    o=' -f concat -safe 0 -i '+ fnm1;
  else:
    o=' -i '+fnm_list[0]+' -safe 0'; # o=' -fflags +genpts'+o
  cmd=fnm0+o+' '+A+' '+fnm_out; print cmd; subprocess.call(cmd)
  if 1<n: os.remove(fnm1)

import glob,cv2, numpy as np; # sudo apt-get install python-opencv
resF =[ 480, 640,2,  0, 480,   0, 640,.3e6   ]; # foscam134 strange audio codec
resF2=[ 960,1280,4,  0, 960,   0,1280, 1e6   ]; # foscam2
# resA =[1080,1920,2,  0,1080,   0,1920,10e6,14]; # amcrest cam1 - bad img on movement (CBR?); 1e6<sens~30e6<300e6
# resA2=[1080,1920,2,  0,1080,   0,1920, 1e6   ]; # amcrest cam2 - need second frameRef for the door; .1e6 too sens, 1e6 too much;
# resAS=[1080,1920,2,200,1080,1300,1920        ]; # amcrest cam3 street
# resS1=[1512,2688,4,710,1460,150,1600         ]; # camS before 1106
# resS =[1440,2560,4,710,1440, 150,1600        ]; # camS after 1106

def vid_motion(fnm_list,fnm_out,res=None):
  if os.path.exists(fnm_out): print 'fnm_out='+fnm_out+' exists, doing nothing'; return;
  fnm_list=[fnm_list] if isinstance(fnm_list,str) else fnm_list;
  res+=[0,res[0],0,res[1]] if len(res)==3 else []; res+=[10e6] if len(res)==7 else []; res+=[0] if len(res)==8 else []; assert 0<=res[8];
  nref=res[2]*3; fout = cv2.VideoWriter(fnm_out,cv2.VideoWriter_fourcc(*'XVID'),res[2],(res[1],res[0]),True); print 'fnm_out= ',fnm_out
  bufRef  =np.zeros([res[4]-res[3],res[6]-res[5], 3*nref   ], np.uint8); kref=0;
  buf     =np.zeros([res[0],       res[1],        3, res[2]], np.uint8); k   =0; bufflag=[True ]*res[2];
  refFrame=np.zeros([res[4]-res[3],res[6]-res[5], 3        ], np.uint8);
  for fnm in fnm_list: # 5 min of video per file, 45G/day
    if not os.path.exists(fnm): print 'fnm= '+fnm+' does not exist';
    fin = cv2.VideoCapture(fnm); print 'processing ',fnm
    if not fin.isOpened(): print 'cant open fnm, skipping'; continue; 
    k_in,k_out,time_decay=0,0,0;
    while True: # loop over the frames of the video
      for cnt in range(1+res[8]): (grabbed, frame) = fin.read();
      k_in+=1; # print grabbed # frame indexing is (horizontal, vertical)
      if not grabbed:
        if k_in<2: print 'can`t read fnm, bad codec?'
        break; # fnm eof
      if not np.any(frame): continue; # skip blank frames
      gray = cv2.GaussianBlur(frame[res[3]:res[4],res[5]:res[6],:], (21, 21), 0) # reduced frame
      while True: # loop for initial populating of bufRef
        bufRef[:,:,3*kref:3*kref+3]=gray; kref=np.mod(kref+1,nref);
        if np.any(bufRef[:,:,3*kref:3*kref+3]): break;
      ### slow piece
      for kk in range(3): refFrame[:,:,kk]=((np.sum(bufRef[:,:,kk::3],2)+nref/2)/nref).astype(np.uint8); # detect movement vs (res[2]*3 prev avg frames)
      buf[:,:,:,k]=frame; bufflag[k]=True; k=np.mod(k+1,res[2]); # store frame in buf
      # compute the absolute difference between frame and ref frame
      thresh = cv2.threshold(cv2.absdiff(refFrame, gray), 25, 255, cv2.THRESH_BINARY)[1];
      if res[7]<np.sum(thresh): time_decay=res[2] # 1s after a hit
      if 0<time_decay:
        for cnt in range(res[2]):
          if bufflag[k]:
            fout.write(buf[:,:,:,k]); bufflag[k]=False; k=np.mod(k+1,res[2]); k_out+=1;
      time_decay-=1;
    fin.release();
    print k_in,k_out
  fout.release(); cv2.destroyAllWindows()

def vid_show(frm):
    cv2.startWindowThread(); cv2.namedWindow("cv2 window"); cv2.imshow("cv2 window",frm); cv2.waitKey(); # cv2.destroyAllWindows() # c^C,
#--- ffmpeg man
# http://www.labnol.org/internet/useful-ffmpeg-commands/28490/
# ffmpeg -i youtube.flv -c:v libx264 -preset ultrafast filename.mp4
# ffmpeg -i video.mp4 -vn audio.mp3 # kill video
# combine audio and video
# ffmpeg -i video.mp4 -i audio.mp3 -c:v copy -c:a aac -strict experimental -shortest output.mp4
#--- openCV et al
# http://stackoverflow.com/questions/37268239/python-reading-a-video
# http://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_gui/py_video_display/py_video_display.html
# http://stackoverflow.com/questions/8900637/problems-converting-video-to-pictures-using-python-2-7
# pymedia
# http://pymedia.org/
# pyffmpeg http://code.google.com/p/pyffmpeg/.
# VTK http://www.vtk.org/
# pyglet http://www.pyglet.org/
# PIMS - from PhD thesis https://pypi.python.org/pypi/PIMS/0.2
# https://wiki.hpcc.msu.edu/pages/viewpage.action?pageId=13870492
#--- openCV (essentially a wrapper for ffmpeg with own flakes): used on win for vid_movmt(), abandoned on linux
# sudo pip install opencv-python; sudo apt-get install ffmpeg;
# sudo apt-get install libopencv-dev python-opencv; sudo apt-get autoremove libopencv-dev python-opencv
# import os,cv2; dir0=v.q+'cam/';
# opencv works on rename .avi/.mp4 ; opencv cant open some h264 from cam0,cam2,blueIris, ffmpeg is fine;
#--- openCV read attib
# fnm=dir1+'../output.avi'; fin = cv2.VideoCapture(fnm); print 'processing ',fnm; print os.path.exists(fnm),fin.isOpened()
# attr1=(cv2.CAP_PROP_FRAME_HEIGHT,cv2.CAP_PROP_FRAME_WIDTH,cv2.CAP_PROP_FPS,cv2.CAP_PROP_FRAME_COUNT,cv2.CAP_PROP_FOURCC,cv2.CAP_PROP_FORMAT,cv2.CAP_PROP_MODE) # cv2.CAP_PROP_POS_FRAMES
# print [fin.get(o) for o in attr1]
# def cv2_codec(A): o=int(A); return chr((o & 0XFF)) + chr((o & 0XFF00) >> 8)+ chr((o & 0XFF0000) >> 16)+ chr((o & 0XFF000000) >> 24)
# cv2.CAP_PROP_FRAME_ WIDTH/HEIGHT/FPS/COUNT , cv2.CAP_PROP_ POS_FRAMES/FOURCC/FORMAT/MODE
# useless:
# CV_CAP_PROP_POS_ MSEC/AVI_RATIO Relative position of the video file: 0 - start of the film, 1 - end of the film.
# cv2.CAP_PROP_BRIGHTNESS/CONTRAST/SATURATION(amt of grey)/HUE(color)/GAIN/EXPOSURE (only for cameras)
# cv2.CAP_PROP_CONVERT_RGB(odd)/WHITE_BALANCE (unavail) / CV_CAP_PROP_RECTIFICATION (for stereo cams)
# DEV.LS h264
# H.264=MPEG4-AVC; H264 - MPEG4 AVC (part 10)
#----------------------------------------------------------------------------------------------------------------
