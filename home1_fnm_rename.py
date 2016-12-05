
###--- smart robocopy
# o='ebooks/'; o='mp3/'; o='mp3_baby_aux/'; o='mp3_iTunes/'; o='mp3_2016/'; o='mp3b/'; # 
o='soft/'; o='backups/'
dir1='N:/'+o; dir2='P:/'+o; dir3='P:/ver3/'+o;

# calc ext,size_bytes,time_sec,sha,dnm_tgt,fnm_tgt ### use ct()
o=mdir(dir1,1); o=o[o[:,2]==0,:][:,range(7)+[2]*6].copy(); o[:,7]=[q[-4:] for q in o[:,0]]; o[:,8]=floor(o[:,3]*1e3+1e-7).astype(int); o[:,9]=dt2sec(o[:,5]); o[:,10]=-1; o1=o;
o=mdir(dir2,1); o=o[o[:,2]==0,:][:,range(7)+[2]*6].copy(); o[:,7]=[q[-4:] for q in o[:,0]]; o[:,8]=floor(o[:,3]*1e3+1e-7).astype(int); o[:,9]=dt2sec(o[:,5]); o[:,10]=-1; o2=o;
o=mdir(dir3,1); o=o[o[:,2]==0,:][:,range(7)+[2]*6].copy(); o[:,7]=[q[-4:] for q in o[:,0]]; o[:,8]=floor(o[:,3]*1e3+1e-7).astype(int); o[:,9]=dt2sec(o[:,5]); o[:,10]=-1; o3=o;

# match1 - dnm,size_bytes,time_sec
m=mm(zip([dir2+q[len(dir1):] for q in o1[:,0]],o1[:,8],o1[:,9]),zip(o2[:,0],o2[:,8],o2[:,9])); print sum(-1<m),' dnm matches1, dropping...'; o1=o1[m<0,:]; have_orig=o2[-1<mm(rlen(o2),m),:]; o2=o2[mm(rlen(o2),m)<0,:];
# match2 by fnm,size_bytes,time_sec (drop non-unique m)
m=mm(zip(o1[:,1],o1[:,8],o1[:,9]),zip(o2[:,1],o2[:,8],o2[:,9])); m[mm(m,m)!=rlen(m)]=-1;      
### write subroutine "match_drop_non_uniq_rematch_again"; run match2 on residuals to improve m;
### update o2[:,:2]
for o in zip(o2[m[-1<m],0],[dir2+q[len(dir1):] for q in o1[-1<m,0]]): fnm_mv(o[0],o[1]);
print sum(-1<m),' fnm matches2, files moved'; o1=o1[m<0,:];
### update have_orig
o2=o2[mm(rlen(o2),m)<0,:];
# match3 by ext,size_bytes,time_sec + sha (drop non-unique m)
m=mm(zip(o1[:,7],o1[:,8],o1[:,9]),zip(o2[:,7],o2[:,8],o2[:,9])); m[mm(m,m)!=rlen(m)]=-1;
for i in find(-1<m): o1[i,10],o2[m[i],10]=fnm_sha5(o1[i,0]),fnm_sha5(o2[m[i],0]); m[i]=-1 if o1[i,10]!=o2[m[i],10] else m[i];
# o1[-1<m,10]==o2[m[-1<m],10]
# move dir2 to dir2_dir1
for i in find(-1<m):
  q=dir2+o1[i,0][len(dir1):];
  if os.path.exists(q): os.remove(q);
  fnm_mv(o2[m[i],0],q); print q;
o1=o1[m<0,:]; o2=o2[mm(rlen(o2),m)<0,:];
#--- match3 dir3 to dir2, drop dir3_in_dir2
m=mm(zip(o3[:,7],o3[:,8],o3[:,9]),zip(o2[:,7],o2[:,8],o2[:,9])); m[mm(m,m)!=rlen(m)]=-1; 
for i in find(-1<m): o3[i,10],o2[m[i],10]=fnm_sha5(o3[i,0]),fnm_sha5(o2[m[i],0]); m[i]=-1 if o3[i,10]!=o2[m[i],10] else m[i];
print sum(-1<m),' files in dir3 and dir2 (dropping from dir3)';
[os.remove(q) for q in o3[-1<m,0]]; o3=o3[m<0,:];
#--- match2 dir3 to dir1, move_to_dir2 (hmm, have sha5 here)
m=mm(zip(o3[:,1],o3[:,8],o3[:,9]),zip(o1[:,1],o1[:,8],o1[:,9]));
x=find(m<0); y=find(mm(rlen(o2),m)<0); m2=mm(zip(o3[x,7],o3[x,8],o3[x,9]),zip(o1[y,7],o1[y,8],o1[y,9])); m[x[-1<m2]]=y[m2[-1<m2]]; m[mm(m,m)!=rlen(m)]=-1; ### can run twice for dupl, can run match3
for i in find(-1<m): o3[i,10],o1[m[i],10]=fnm_sha5(o3[i,0]),fnm_sha5(o1[m[i],0]); m[i]=-1 if o3[i,10]!=o1[m[i],10] else m[i];
for i in find(-1<m):
  q=dir2+o1[m[i],0][len(dir1):];
  if os.path.exists(q): os.remove(q); # fnm_dir3 is good enough 
  fnm_mv(o3[i,0],q); o3[i,10]=-2;
if sum(-1<m): print ' update o2 here'; assert 0;
### test sha5
# o='Part08.mp3'; i=mm([o],o1[:,1])[0]; i2=mm([o],o3[:,1])[0]; g1=[o1[i,0],o3[i2,0]]; o=open(g1[0],'rb').read(); q=open(g1[1],'rb').read(); o==q
# fnm_sha5(g1[0],hashlib.sha256()),fnm_sha5(g1[0],hashlib.sha256())
print 'moving dir2->dir3'
for i in rlen(o2):
  q=dir3+o2[i,0][len(dir2):];
  if os.path.exists(q): os.remove(q);
  fnm_mv(o2[i,0],q); o2[i,0]=q; print q;
### o3=ct(o3,o2); o2=[];

# move dir1->dir2
for o in o1[:,0]: fnm_mv(o,dir2+o[len(dir1):],1); print o;
# print len(m),sum(-1<m)
# print len(o1),len(o2)
### drop match3 here

### match4 dir3 to o1

# move o2 to dir3, o1 to dir2

# calc list of files to be moved to dir3 (move with overwrite?)
o=o2[:,-3].astype(int)*0; o[m[-1<m]]=1; x=find(o<1); print str(len(x))+'/'+str(len(o))+' extra in dir2, -> dir3';
for i in x: fnm_mv(o2[i,0],dir3+o2[i,0][len(dir2):])
# [os.remove(o2[i,0]) for i in x]

# files missing in dir2
x=find((o1[:,2]==0)&(m<0)); print str(len(x))+' missing in dir2';
for i in x: fnm_mv(o1[i,0],dir2+o1[i,0][len(dir1):],1)
### run ver3 vs dir1, mark matches
### output: fnm1(empty if fnm2 in ver2),fnm2,fnm0

#--- file rename - specific
def fnm_clean(dir1,A=[]): #--- rename mp3,mp4
 o1=mdir(dir1,1);
 for j in [0,1]:
   for i in find(o1[:,2]==j): # rnm dir second
     o=o1[i,1];
     for q in [' ','-','Copy_(2)','___','__']+A: o=o.replace(q,'_');
     for q in ['_Track_Artist_','_Unknown_Artist_','__']+A: o=o.replace(q,'_');
     # o=o.replace('Track_No','1'); o=o.replace('1Track_','1').replace('2Track_','2').replace('3Track_','3'); o=o.replace('_AudioTrack_','_Track_');
     # for k in range(10): q=str(100+k)[1:]; o=o.replace(q+'_Track_'+q[1:]+'.',q+'.');
     # for k in range(40): q=str(100+k)[1:]; o=o.replace(q+'_Track_'+q+'.',q+'.'); # '15_Track_15'
     # o='00'+o if len(o)==4 and o[0]=='.' else '0'+o if len(o)==5 and o[0] in [str(k) for k in range(10)] and o[1]=='.' else o
     # o=glob.glob('M:/mp3/*/*/*/*/*/.*'); [q.replace('\\','/') for q in o] # mdir('.mp3') does not work stupidly
     if o!=o1[i,1]:
       print o1[i,0]; fnm=o1[i,0][:-len(o1[i,1])]+o; os.rename(o1[i,0],fnm) # if not os.path.exists(fnm) else os.remove(fnm);
def fnm_rename_foscam(): ###=== foscam rename script 1 ================================
 dir1='D:/scan0/192.168.2.106/'; dir2='K:/foscam/';
 # for i in rlen(o): os.rename(o[i],o[i][:-4]+'_cam5.avi');
 e1=['VMcam1','VMcam2','VMcam3','VMcam4','manual']
 for i in rlen(e1):
   o=glob.glob(dir1+e1[i]+'_*.*'); o=[q[len(dir1):] for q in o]; k=6
   for j in rlen(o): os.rename(dir1+o[j],dir2+o[j][k+1:k+9]+'_'+o[j][k+9:-4]+'_cam'+str(1+i)+o[j][-4:]);
   if i<4:
     o=glob.glob(dir2+'20*_cam'+str(1+i)+'.*'); o=[q[len(dir2):] for q in o]
     for j in [k for k in rlen(o) if len(o[k])==24  ]: os.rename(dir2+o[j],dir2+o[j][:16]+'00_'+o[j][16:])
     for j in [k for k in rlen(o) if len(o[k])==24+2]: os.rename(dir2+o[j],dir2+o[j][:16]+'0'  +o[j][16:])
def fnm_rename_img(dir1='K:/_fmvc/foto/'): ###=== andr rename script 1 ================================
  from PIL import Image; import time;
  o=glob.glob(dir1+'IMG*.JPG')+glob.glob(dir1+'*/*/IMG_*.JPG')+glob.glob(dir1+'*/IMG_*.JPG'); # +glob.glob(dir1+'*/IMG_*.CR2');
  for i in rlen(o):
    q=Image.open(o[i])._getexif()[36867][0]; o1=os.path.split(o[i]); print o[i], o1[0]+'/'+q[:4]+q[5:7]+q[8:10]+'_'+q[11:13]+q[14:16]+q[17:19]+'_'+o1[1][4:]
    os.rename(o[i],o1[0]+'/'+q[:4]+q[5:7]+q[8:10]+'_'+q[11:13]+q[14:16]+q[17:19]+'_'+o1[1][4:]);
  # MVI date modified
  o=glob.glob(dir1+'IMG_*.MOV')+glob.glob(dir1+'MVI_*.MP4')+glob.glob(dir1+'IMG_*.CR2'); o=[q[len(dir1):] for q in o]; o
  for i in rlen(o): os.rename(dir1+o[i],dir1+time.strftime('%Y%m%d_%H%M%S',time.localtime(os.path.getmtime(dir1+o[i])))+o[i][3:])

assert 0;

#--- md5 sum (deprecated)
# def md5(fname):
#     hash_md5 = hashlib.md5() # some class
#     with open(fname, "rb") as f:
#         for chunk in iter(lambda: f.read(4096), b""):
#             hash_md5.update(chunk)
#     return hash_md5.hexdigest()
###--- sha256 sum -------------------------------------------------------------
dir_install='D:/';
dir_input='P:/ver3/mp3/'; file_output=dir_install+'fnm3.mat';

# v=lambda: None; v.q=dir_install; execfile(v.q+'py9.py');

# [(fnm, fnm_sha5(open(fnm, 'rb'), hashlib.sha256())) for fnm in fnmlist]

# calculate file list, calculate chksums, save output
dir1=dir_input; o=mdir(dir1,1); fnmlist=[q[0] for q in o if not q[2]]; n=len(fnmlist);
o1=[(fnm, fnm_sha5(open(fnm, 'rb'), hashlib.sha256())) for fnm in fnmlist]
fnm=[q[0] for q in o1]; chksum=np.zeros((n,32),int);
for i in range(n): chksum[i,:]=[ord(q) for q in o1[i][1]]
saveM(file_output,{'fnm':fnm,'chksum':chksum});
### chksum saved as int32 array
### mdir() fnm is not sorted
#======================================================================================================================
# e1=fnm; fnm=a.fnm; a.fnm=e1; e1=chksum; chksum=a.chksum; a.chksum=e1;
dir1='N:/mp3/'; dir2='P:/mp3/'; dir4='P:/ver3/mp3/'; dir9='D:/'; # dir3 will be populated later 
a=loadM(dir9+'fnm1.mat'); fnm =a.fnm; chksum =[''.join([chr(q) for q in a.chksum[i,:]]) for i in range(a.chksum.shape[0])]; # convert chksum back to str_odd_encode
a=loadM(dir9+'fnm2.mat'); fnm2=a.fnm; chksum2=[''.join([chr(q) for q in a.chksum[i,:]]) for i in range(a.chksum.shape[0])];
m=mm(chksum2,chksum); x=find(-1<m); # i=0; fnm[x[i]],fnm2[m[x[i]]] # x=find(m!=rlen(m)); i=3; o=find(m==m[x[i]]); # some dupl files
# def fnm_mv(fnm,fnm2):
for i in rlen(x):
  if (i/100)*100==i: print i
  fnm3='P:'+fnm[m[x[i]]][2:];
  if os.path.exists(fnm3): continue; # assert 0; ### if file exists, raise an error (or continue)
  fnm.move(fnm2[x[i]],fnm3);
  
e1=[];
for o in fnm:
  if not os.path.exists(o): e1.append(o);
# 6412 missing
m=mm(arr(chksum)[mm(e1,fnm)],chksum2) # some missing
# x=find(-1<m); fnm2[m[x]];
# for i in find(-1<m): shutil.move(fnm2[m[i]],e1[i])
  
dir_remove_empty('P:/ver3/mp3/')

m=mm(chksum2,chksum)

e1=[];
for i in rlen(fnm):
  o=fnm[i]; o1=[]; q=['',' '];
  while len(q[1]): q=os.path.split(o); o1.insert(0,q[1]); o=q[0];
  e1.append(o1)

e2=[];
for i in rlen(fnm2):
  o=fnm2[i]; o1=[]; q=['',' '];
  while len(q[1]): q=os.path.split(o); o1.insert(0,q[1]); o=q[0];
  e2.append(o1);

  o=os.path.split(fnm2[i]); q=os.path.split(o[0]); os.path.split(q[0])[1]+q[1]+o[1] 

#=================================================

q='Pink_Floyd/Albums/1979_The_Wall/05_Another_Brick_In_The_Wall_part_2.mp3'
e1=fnm_sha5(open(dir1+q,'rb'), hashlib.sha256()),fnm_sha5(open(dir4+q,'rb'), hashlib.sha256())
# e2=mm([dir1+q],a.fnm),mm([dir4+q],fnm)
a.chksum[e2[0][0]],chksum[  e2[1][0]]

#-------------------------------------------------------
# copyfile with mkdir
# move stray files into dir3

if 0:
  
 dir1='K:/foto_ndiv/Sean/'
 from PIL import Image; import time;
 e1=mdir(dir1,1) 
 for dir1 in e1[e1[:,2]==1,0]:
  o=glob.glob(dir1+'*.jpg');
  for i in range(0,len(o)):
    q=Image.open(o[i])._getexif(); o1=os.path.split(o[i]);
    if q is None or 36867 not in q.keys(): continue
    q=q[36867][0]; q=q[:4]+q[5:7]+q[8:10]+'_'+q[11:13]+q[14:16]+q[17:19];
    if   o1[1][:9]  !=q[:9]:     
      print 'i='+str(i)+' bad date_fnm, breaking '+o1[0]+'/'+o1[1] ; break
    elif o1[1][9:15]!=q[9:]: 
      print 'i='+str(i)+' fixing time'; os.rename(o[i],o1[0]+'/'+q+'_'+o1[1][9:]);




      # g=o1[1];
      # if int(g[:8])<2e7 or 2020<int(g[:8]) or 24e4<int(g[9:15]): print 'bad fnm, no attrib'; break;
      # else: q={36867:(g[:4]+':'+g[4:6]+':'+g[6:8]+' '+g[9:11]+':'+g[11:13]+':'+g[13:15],0)}; print 'filled attr' # arr([q for q in o1[1][:15]+': '])[[0,1,2,3,15,4,5,15,6,7,16,9,10,15,11,12,15,13,14]]


# def med(A): return '['+','.join([q for q in A if q[0]!='_'])+']'
# v=lambda: None; v.q='K:/bin/'; execfile(v.q+'py/home1.py');

#--- find fin2 not in dir1, move to dir3

o='6.foto_fat/from_others_20140601/'
dir1='P:/'+o; dir2='P:/'+o; 
o1=mdir(dir1,1); o2=mdir(dir2,1); m=mm(o1[:,0],o2[:,0]); sum(m<0)

# do "date taken" rename
dir1='P:/6.foto_fat/from_others_20140601/21.AM_extra/'
fnm_rename_img(dir1)


### grab android
dir1='K:/_fmvc/';
e1='inc','out' # 0d incoming calls, 1d outgoing
for k in [0,1]:
  o=mdir(dir1+'ca/'+str(k)+'d*'); o
  for i in rlen(o): os.rename(o[i,0],dir1+'ca/'+o[i,1][2:10]+'_'+o[i,1][10:-4].replace('p','_').replace('+1','')+'_'+e1[k]+o[i,1][-4:])
o=mdir(dir1+'DCIM/',1); [os.rename(o[i,0],dir1+o[i,1].replace('Screenshot_','')) for i in [k for k in rlen(o) if o[k,2]==0]]
o=mdir(dir1+'vo/2016-*'); [os.rename(o[i,0],dir1+'vo/'+o[i,1].replace('-','')) for i in rlen(o)];
#=== epub =============================================================================================================
from ebooklib import epub; bk=epub.read_epub('D:/scan0/lgl/20160415_Katz.epub');
for image in bk.get_items_of_type(epub.IMAGE_MEDIA_TYPES): print image;
# [EPUB_VERSION,FOLDER_NAME,IDENTIFIER_ID,
  # guide,reset,spine,
  # set_identifier,add_author,set_cover,  title,set_title, 
  # items,  get_items,get_items_of_media_type,get_items_of_type,get_item_with_href,get_item_with_id,  add_item, 
  # metadata,get_metadata,add_metadata,
  # toc,
  # templates,get_template,set_template,
  # language,set_language,uid,version]'
# # Writing
# bk = epub.EpubBook();
# # set metadata
# bk.set_identifier('id123456'); bk.add_author('Author Authorowski') ; bk.add_author('Danko Bananko', file_as='Gospodin Danko Bananko', role='ill', uid='coauthor')
# bk.set_title('Sample bk'); bk.set_language('en')
# # create chapter
# c1=epub.EpubHtml(title='Intro', file_name='chap_01.xhtml', lang='hr'); c1.content=u'<h1>Intro heading</h1><p>Zaba je skocila u baru.</p>'
# bk.add_item(c1); bk.toc = (epub.Link('chap_01.xhtml', 'Introduction', 'intro'),(epub.Section('Simple bk'), (c1, ))) # # add chapter; define Table Of Contents
# bk.add_item(epub.EpubNcx()); bk.add_item(epub.EpubNav()) # add default NCX and Nav file
# style = 'BODY {color: white;}'; nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style) # define CSS style
# bk.add_item(nav_css); bk.spine = ['nav', c1]; # add CSS file; basic spine
# epub.write_epub('test.epub', bk, {}) # write to the file
#---
import re; import epub as ep; from ebooklib import epub; # http://epub.exirel.me/genindex.html
dir1='D:/scan0/lgl/';
for fnm in ['a_20160500_20130800.epub','b_20130115_2008.epub','c_2007_2002.epub','d_2002_1991.epub','LexisNexis_201605_1991.epub']: # kk=0;
  bk=ep.open_epub(dir1+'LN_aside/'+fnm); o=[q for q in bk.namelist() if -1<q.find('index')]; o1=bk.read_item(o[0]);
  for k in range(1,len(o)): q=bk.read_item(o[k]); o1=o1[:o1.rfind('</body></html>')]+q[q.find('<body class="calibre">')+23:];
  x=[k.start() for k in re.finditer('\d* of \d* DOCUMENTS',o1)]+[o1.rfind('</body></html>')];
  # create bk2
  bk2=epub.EpubBook(); bk2.set_identifier('LN'); bk2.add_author('u'); bk2.set_title(fnm[:-5]); bk2.set_language('en');
  bk2.add_item(epub.EpubItem(uid="style_nav",file_name="style/nav.css",media_type="text/css",content='BODY {color: white;}'));
  bk2.add_item(epub.EpubNcx()); bk2.add_item(epub.EpubNav()); # define CSS style, add CSS file, add default NCX and Nav file
  c0=[]; # ch_list
  for k in rlen(x[:-1]): o='ch{:05d}'.format(1+k); q=epub.EpubHtml(title=o,file_name=o+'.xhtml'); q.content=o1[x[k]:x[k+1]]; c0.append(q); bk2.add_item(q);
  bk2.toc = (epub.Link('ch1.xhtml','intro','_'),(epub.Section(fnm[:-5]), c0)) # # add chapter; define Table Of Contents
  bk2.spine = ['nav']+c0; # define CSS style # add CSS file; basic spine
  epub.write_epub(dir1+fnm,bk2,{})
#----------------------------------------------------------------------------------------------------------------------
# for q in ['titlepage.xhtml','META-INF/container.xml','index.html']: print bk.read_item(q);
# for item in bk.opf.manifest.values(): o = bk.read_item(item); print o; break
#    k+=1; print k; print o
#    [NameToInfo,add_item,check_mode_write,close,comment,compression,
#     content_path,debug,extract,extract_item,extractall,filelist,filename,fp,get_item,get_item_by_href,
#     getinfo,infolist,mode,namelist,open,opf,opf_path,printdir,pwd,read,read_item,remove_paths,setpassword,start_dir,testzip,toc,uid,write,writestr]'
# q=bk.namelist(); k=-1; k+=1; print bk.read_item(q[k]); print q[k];
# [mimetype,META-INF/,META-INF/container.xml,content.opf,cover_image.jpg,index_split_000.html,index_split_001.html,page_styles.css,stylesheet.css,titlepage.xhtml,toc.ncx,META-INF/calibre_bookmarks.txt]
#----------------------------------------------------------------------------------------------------------------------
# o=datetime.strptime(str(o), "%m/%d/%y %H:%M:%S").strftime('%Y%m%d.%H%M%S') # to check fnm

# https://wiki.python.org/moin/UsefulModules#ID3_Handling
# https://pypi.python.org/pypi?:action=search&term=id3&submit=search
subprocess.Popen('explorer /root,'+'C:/Programs/computations/WinPython2.7.10.3/python-2.7.10.amd64/Lib/'.replace('/','\\'),shell=True,stdout=subprocess.PIPE).stdout;

import mutagen; from mutagen.easyid3 import EasyID3; from mutagen.mp3 import MP3
#---------------------------------------
dir1='M:/mp3/_jazz/_TO_FLIP/';
o=mdir(dir1)
for i in rlen(o):
  q=o[i,1]; x=q.find('_')
  os.rename(o[i,0],dir1+q[x+1:-1]+'_'+q[:x])

dir0='M:/mp3/_RUS/';
o1=mdir(dir0,1); o2=arr(['artist','album','title']); # 'genre'

bad1=[];
for i in range(40000,50000): # 
  if mod(i,300)==0: print i
  if o1[i,0][-4:]=='.mp3':
    try:
    # if 1:
        audio=mutagen.easyid3.EasyID3(o1[i,0]); k=0; # breaks if no id3 tags at all
        for o in o2:
          if o not in audio.keys(): audio[o]  ='_';                  k+=1;
          else:                     audio[o],q=cyr2lat(audio[o][0]); k+=q;
        if k: audio.save(); print i,o1[i,0]
    except:
        bad1+=[o1[i,0]]; print 'BAD                '+o1[i,0]
# o1='Aerosmith/'; o=mdir(dir1+o1+o1[:-1]+'*.mp3')
# for i in rlen(o): os.rename(o[i,0],dir1+o1+o[i,1][len(o1):])

###=============================
# vars(msg).keys()
# o=msg; [method for method in dir(o) if callable(getattr(o, method))]
# dir() pulls from __dict__; look for __class__ -- and then to go for its __bases__:
# hasattr(module_name, "attr_name")
# http://www.ibm.com/developerworks/library/l-pyint/index.html
# inpect.getmembers(re.compile(pattern))
# process docx  better to use a tool # https://python-docx.readthedocs.io/en/latest/ # soffice --headless --convert-to txt:Text /path_to/document_to_convert.doc

#--- outlook save attachment, convert to txt, etract dates from fnm ---------------------------------------------------
import win32com.client;
dir1='D:/scan0/lgl2/'; fnm_clean(dir1); o=mdir(dir1+'msg/')
outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
for i in rlen(o):
  msg = outlook.OpenSharedItem(o[i][0])
  for k in range(msg.Attachments.Count): q=msg.Attachments.Item(k+1); q.saveAsFile(dir1+'doc/'+o[i][1][:-4]+'_'+str(k)+'_'+q.Filename)
del outlook, msg
### run doc2txt here
o=mdir(dir1+'txt/');
for i in rlen(o): # calc dt, move files
  if i<=0: continue;
  try:
    fd=open(o[i][0],'r'); q=fd.read(); fd.close(); e1=', Decided \n';
    e=[q[k-50+q[k-50:k].rfind('\n')+1:k].strip() for k in (q.find(e1),q.rfind(e1))]; e
    t=[mdt(datetime.datetime.strptime(q,'%B %d, %Y').date()) for q in e];
    os.rename(o[i][0],                        dir1+'txt/'+str(t[0])+'_'+str(t[1])+'_'+o[i][1]            );
    os.rename(dir1+'doc/'+o[i][1][:-4]+'.doc',dir1+'doc/'+str(t[0])+'_'+str(t[1])+'_'+o[i][1][:-4]+'.doc')
  except: pass
# print msg.SenderName,msg.SenderEmailAddress,msg.SentOn,msg.To,msg.CC,msg.BCC,msg.Subject,msg.Body,msg.Attachments.Count
#--- patch sms dump
import smtplib; from email.mime.text import MIMEText
fnm='C:/Users/u/Desktop/aa/1.eml';
fd=open(fnm,'rb'); o=fd.read(); fd.close(); q=o.split('\n')
x=[k for k in rlen(q) if -1<q[k].find('From:') or -1<q[k].find('To:') or -1<q[k].find('Subject:') or -1<q[k].find('Date:') ]
e=arr(q)[x].tolist()+['"'+q[-1].replace('=20',' ')+'"']; o='\n'.join(q)
# want to convert .eml to .msg
# e=email.message_from_string(o); fnm2='C:/Users/u/Desktop/b/__00.eml'; fd=open(fnm2,'wb'); gen=email.generator.Generator(fd); gen.flatten(e); fd.close()
# can pull out from, to, time, text
# http://stackoverflow.com/questions/17874360/python-how-to-parse-the-body-from-a-raw-email-given-that-raw-email-does-not
# http://stackoverflow.com/questions/26322255/parsing-outlook-msg-files-with-python
#----------------------------------------------------------------------------------------------------------------------
