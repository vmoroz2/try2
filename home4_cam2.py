# webcam step1 (gentle convert video)/step2(convert audio, merge to mp4/avi)/step 3 (Calc mvt)
# youtube dnld
#--- cam project
# orig      .avi: video index errors,fps_tag=100/fps_actual=1...100, ffmpeg errors, audio on/off,files fat/split
# converted .mp4: video mp4v resoln,fps<=fps0,avi_index fixed; audio mp4a; fps=2/4, merged_by_date,+mvt folder (mvt mute);
# foscam video codec is approx (VLS fixes index, reports bad fps=100), and audio codec is obscure. ffmpeg breaks often (error messages during conversion, bad output - stuck VLC , dropped audio)
# ffmpeg has lots of default and guess settings. It works well if mp4/avi was created with it
# ffmpeg pass 1 to convert to codec_video_ffmpeg with min recoding             (-c:v copy,audio_adjust,conversion to mp4 does not change video errors)
# ffmpeg and pass 2 to convert codec_audio_aac, to convert to mp4 and to merge (-c:a copy breaks)
# ffmpeg has several flavors - free (limited codecs, extra errors) and paid (from bigasoft)
# mp4 conversion : fmp4(avi)->mp4v(mp4); sometimes breaks on '-c:v copy -c:a copy'; changes fps to "actual" (even after reencoding fps=1 to fps=4); not sure what happens on merge (fps=1 to fps=4) and fps=4
# bad merge sometimes: get bad_seek/stuck (fixed by ->avi or '-an'; '-r 4 -b:v 5M' on mp4 does not help), get lost audio
#--- foscam2: .avi is not shown properly by VLC player; wmplayer is OK; key rate <10 unavail; frame rate 5 OK, 2 is bad
# bit rate 4M looks bad; best settings : resolution 960, bit rate 2M, frame rate 5, key frame interval 10,
# variable bit rate - no (?); 0/960p/1fps/1M works for WMPlayer; oddly VLC player shows only first frame
#--- street_cam1 web app
# zoom - OK, want 1.5x extra; resolution 5M - good; low light - good; video stream, recording - yuck
# x1 1 frame interval ? 16/4 ; x2 Bitrate 6000 / 10000 ; x3 Frame rate 15/60 ; x4 LBR disable/ (enable, motion level Nearly Stationary, noise level Low)
# x5 BaseProfile Disable/Enable ; x6 WDR setting Disable/Enable ; x7 Encode mode Basic/Advance ; x8 Noise level 1/9 ; Shutter mode Auto ; "shadow" walking / slow img update, want to get rid of "tails"
# record skype video on android - apowersoft screen recorder
# win - showmore
runfile(v.q+'vm_vid.py'); dir0=v.q # v=lambda:None; v.q='D:/scan0/py/'; v.sy='win';

if 0: #--- step 1 (gentle conversion to ffmpeg-created video with minimal re-encoding and minimal quality loss)
  dir1=dir0+'a1/'; dir2=dir0+'out_merged/'; o=mdir1(dir1+'20*.mp4');
  for fnm in o:
    fnm2=dir2+os.path.split(fnm)[1];
    if not os.path.exists(fnm2):
      print 'pass1 patch video '+fnm; 
      cmd=fnm0+' -i '+fnm+' -r 29.99 -b:v 50M -c:a copy '+fnm2; o1=sh(cmd); print o1 # ' -c:a libfdk_aac -b:a 128k '
  
  fnm=dir2+'20150715a_bad_seek.mp4';
  cmd=fnm0+' -i '+fnm+' -c:v copy -c:a copy '+fnm[:-4]+'.avi'; subprocess.call(cmd);
  #--- step 2 (convert audio, convert to mp4,merge by day)
  # manually rename files by date_tstamp, run pass2
  o=list(set([int(os.path.split(q)[1][:8]) for q in mdir1(dir1+'*.mp4')])); o.sort(); date_list=o;
  date_list=[20160617];
  for t in date_list:
    fnm2=dir2+str(t)+'.mp4';
    if not os.path.exists(fnm2):  ' -c:v copy -bsf:a aac_adtstoasc -b:a 128k '
  #--- step 3 calc mvt
  dir1=dir0+'cam2/no_mvt/'; dir2=dir0+'cam2/mvt/';
  for o in mdir1(dir1+'*.mp4'): vid_motion(o,dir2+os.path.split(o)[1],res=resF2):
  # cam0_street file 5 min chunks; load breaks at night; need to check no zoom, fps before 1030; mvmt sensitivity higher outside aptmt;
  #--- check dates missed in processing
  # o=mdir1(dir1+'*.???'); o1=[int(os.path.split(q)[1][:8]) for q in o]; o=mdir1(dir2+'*.???'); o2=[int(os.path.split(q)[1][:8]) for q in o]; print set([q for q in o2 if q not in o1]),set([q for q in o1 if q not in o2])
  #--- ffmpeg error check; also use manual test on VLS seek + audio at eof
  # cmd=fnm0 +' -v error -i '+fnm2+' -f null '+dir0+'junk.mp4'; o1=sh(cmd); print o1 # + ' 2>'+fnm1 # +' 2>&1'; -v error -i file.avi -f null - >error.log 2>&1
  # if len(o1): break
  #--- change resoln,flip,slow down/speed up
  # '-vf scale=1280:960 -b:v 5M ' change resoln; '-vf hflip -b:v 5M' flip; '-filter:v "setpts=2.0*PTS" -b:v 5M' slow down 2x; '-r 4 -filter:v "setpts=0.5*PTS" -b:v 5M' speed up 2x; '-r 4 -filter:v "setpts=0.25*PTS" -b:v 5M' speed up 4x;
  #--- split into parts

if 0: #--- youtube downld
  # c:/Programs/calc/py/scripts/pip install pytube
  # conda install -c https://conda.binstar.org/menpo opencv
  import pytube; from pprint import pprint;

  vid_list=['3cr9e5QfPvE','L49VXZwfup8','CBooW61D4tQ','VCQ24gXfRrc','RK4x3Snzfo0','Sb5nf9DkzTs','ZXG5jTSWGu8','ZCr0LG-X9hY','5GU8p4_RLNc',
            'vprH-cb7Nqg','BmHAei23zMQ','7uQjg5nYngo','3uIMzwtiJX8','8f_y-saFZjo','iyCmm2qn3g0','IsEzg_EYxf0','Q6OfmJFtPaA','DfnKL_glVT0']
  vid_list=['V1bFr2SWP1I','R0xoMhCT-7A']
  for i in range(len(vid_list)): # i+=1
    yt=pytube.YouTube('https://www.youtube.com/watch?v='+vid_list[i]); pprint(yt.videos)  # pprint(yt.get_videos()); pprint(yt.filename); pprint(yt.filter('mp4')) # list resolutions
    try:    yt.get('mp4','720p').download(dir0); 
    except: yt.get('mp4').download(dir0);

#--- video collection: dvd rip, deinterlace, avi to mp4, merge
  dir1=dir0+'merge_in/'; dir1=r'N:/mp3_iTunes/mp4/92_BabyBumbleBee/'; dir1='K:/_fmvc/foto/mov/'; 
  dir2=dir0+'merge_out/';
# for o in mdir1(dir1+'*.vob'  ): vid_merge(o,dir1+os.path.split(o)[1][:-4]+'.avi','-c:v libx264 -vf yadif -c:a libfdk_aac -b:a 256k') # dvd rip - convert
# for o in mdir1(dir1+'L_*.avi'): vid_merge(o,dir0+'a/'+os.path.split(o)[1],       '-vf yadif -b:v 10M     -c:a copy') # deinterlace
for o in mdir1(dir1+'*.mov'): vid_merge(o,dir2+os.path.split(o)[1][:-4]+'.mp4','-c:v copy -c:a copy ') # avi to mp4 if possible '-c:v copy -bsf:a aac_adtstoasc ' - fix audio
# ffmpeg msg in yellow "pts has no value" /ffmpeg.exe -fflags +genpts -i xx 
# ffmpeg msg in yellow "Que input is backwards in time" - give up
# -vf hflip -vf vflip -b:v 20M  -metadata:s:v rotate=90

o=mdir1(dir1+'20*.*'); vid_merge(o,dir2+os.path.split(o[0])[1][:-4]+'.mp4','-c:v copy -c:a copy') # merge videos

dir1=r'M:/mov2/music_classic/Mozart/2005_Great.Piano.Concertos/';
for o in glob.glob(dir1+'*.flac'): vid_merge(o,dir1+os.path.split(o)[1][:-5].replace('._','_')+'.mp4',' -c:a libfdk_aac -b:a 256k')

vid_merge(glob.glob(dir1+'*.avi'),dir1+'act_.avi','-c:v copy -c:a copy')

# dir1=dir0+'avi_broken/';
# fd=open(dir1+'a.avi','rb'); o=fd.read(1024*32); fd.close(); fd=open(dir1+'20140524_160021_07_cam2.avi','rb'); q=fd.read(); fd.close(); fd=open(dir1+'aa.avi','wb'); fd.write(o); fd.write(q); fd.close();



# vid_merge(mdir1(dir1+'gaz*.mp4')[:2],dir2+'d.mp4','-c:v copy -c:a copy ') # -c:a libfdk_aac -b:a 256k
  

  # ffmpeg -f lavfi -i nullsrc -c:v libx264 -preset help -f mp4 -
#----------------------------------------------------------------------------------------------------------------
