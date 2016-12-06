# 00 general notes,IDEs;
# 01 install,path,cfg,alias,macro,magic
# 02 ipy,editor,log,hist
# 03 help,search(~which)
# 04 whos,clear,save_txt, 
# 05 dir,mv_fnm; fnm.py from shell,fnm.bat from py;
# 06 run,profile;
# 07 dbg/traceback; - TO REVIEW
# 08 github         - TO REVIEW

from __future__ import division;
# mreadx,squeeze2(for saveMat),saveMat tests
#--- bugs and workarounds
# editor: weak save_cfg (need startup.py);
# cmd: no Cc in py (only in ipy), ugly navigation in milti-line input (ar_up - ok, ar_dn - Cz to get out); silly roundoff (pd init helps a bit)
# dbg/ipdb:
#   no hist, no Cc; output often goes to console (not cmd_window), use %qtconsole and sep window; %whos,wh() do not show data in 0<frm; pkg_reload - need to restart interpreter;
#   ugly traceback
#   no consolidated help info (need to google,pydoc,stackexchange)
# str_unicode_default - no fix
#--- VM coding notes
# avoid orderless dicts, use vec; avoid macros and magics (they may run differently from cmd line and script); (dict helps in mm() and struct_fields); .099999- can scan and patch, or limit # digits displayed
### del with wildcard?
### pkg_reload broken %reload, reload() (.pyc,loads old ver from some cache)
#--- tutorial_unsorted:
# hook=(code attaching fn_event_handler); callback_fn ~event_handler/listener=fn2_thread2; at runtime fn1_thread1 runs init and waits for fn2_thread2(click/web_data etc), fn2 passes data/"calls back" fn1
# callback~event/listener,"fn2 calls fn1 back when event occurs"
# traceback ~dbg; frame,namespace ~list (names,vals) for fns,vars; sys.exit() call to exit fn;fn_prototype(=fn_def); raising_err(generate err~err_code)
# hashtable~dict (addr-value etc)
# relational db ~match by id/align by labels
if 0:
  #--- startup examples
  from vm0 import * # execfile(v.q+'vm0.py'); # interactive_vars not visible to vm0
  # import ipdb; ipdb.launch_ipdb_on_exception(); ### generates garbage in script
  # o=v.q+'vm0.pyc'; os.system('rm '+o) if os.path.exists(o) else None; # py import cache prevents repeated load
  # mpl.rcParams['interactive']=1; mpl.matplotlib_fname(); plt.plot([1,3,7,2,-2]); plt.show(0) # can set up dflt somewhere
  # np.set_printoptions(precision=5,linewidth=200); pd.set_option('line_width',200); pd.set_option('expand_frame_repr',T); # displ setup
  # T,F=True,False; ### want -Qwarn flag on startup
#------------------------------------
print 'vm0_ver1.4'; # to see if annoying caching
import os,inspect,subprocess,signal,datetime; import sys,uuid,shutil,random,string
import numpy as np, pandas as pd, matplotlib as mpl, matplotlib.pyplot as plt; # kills sys.exc_info()
#--- 00 ---------------------------------------------------------------------------------------------------------------
def mm(A,B): # need to use -1; problem for [[1,2,3]]
  if   isinstance(A,set)|isinstance(A,pd.Series): A=list(A)
  if   isinstance(B,set)|isinstance(B,pd.Series): B=list(B)
  elif isinstance(B,str): B=[B] 
  n=len(A); E=np.zeros(n)-1; D={};
  for i in np.r_[len(B)-1:-1:-1]: D[B[i]]=i # dict
  for i in range(n):  
    try: E[i]=D[A[i]]
    except: pass
  return E.astype(int)
def dt2sec(A): return ((mdt(floor(A+1e-7),1)-mdt(19991231,1))*24*3600+floor(mod(A+1e-7,1)*1e6)).astype(int); # 20151231.013000-> #sec
def mdt(A=0,p=0): # types are date,dnum,pdate
  A=A if not (isnum(A) and A==0) else datetime.datetime.now(); dd=datetime; date=dd.date
  if p==-9: # date,dnum->pdate
    kb(not isinstance(A,int),'mdt(-9) bad A_type')
    if 1950e4<A<2050e4: return date(A//10000,(A/100)%100,A%100)
    elif 7e5<A<7.5e5:   return date(2000,01,01)+dd.timedelta(A-730486) # dnum->pdate
    else: kb(1,'mdt(-9) bad A_value')
  elif p==-6: o='{}'.format(A); return o[:4]+'/'+o[4:6]+'/'+o[6:8]+'/'+o+'.'
  elif p==0: # dnum,pdate,pdtime etc->date
    if isinstance(A,(int,long,float,np.float64)): ## this clause not vectorized
      if   1950e4<A<2050e4: return A
      elif 7e5<A<7.5e5: o=A%1*24; A=dd.datetime(2000,01,01,int(o//1),int(o%1*60//1),int(round(o*60%1*60)))+dd.timedelta(A//1-730486); # dnum->pdate
      elif 3e7<A<2e9  : A=dd.datetime.fromtimestamp(int(round(A))) # 1972..1925 # pdate_timestamp->pdtime
    if isinstance(A,dd.date) and not isinstance(A,dd.datetime): return 10000*A.year+100*A.month+A.day;                                # pdate->date
    kb(not isinstance(A,(dd.datetime,pd.tslib.Timestamp,pd.tseries.index.DatetimeIndex,pd.tseries.period.PeriodIndex)),'mdt(0) bad type(A)')
    return 10000*A.year+100*A.month+A.day+.01*A.hour+1e-4*A.minute+1e-6*A.second                                                      # pdtime->date.time
  elif p==1: # date->dnum
    if isinstance(A,list) or isinstance(A,np.ndarray): return arr([mdt(q,1) for q in A]);
    o=int(A//1); a=A%1*1e6; return (date(o//10000,(o//100)%100,o%100)-date(2000,1,1)).days+730486+(a//10000*3600+(a//100)%100*60+a%100)/24./3600; # kb(not isinstance(A,int),'mdt(1) bad A_type')
  elif p==2: # date->dv
    if isinstance(A,int): A=[A,A];
    elif(len(A)<2): A=[A[0],A[0]]
    return [int(mdt(o)) for o in range(int(mdt(A[0],1)),int(mdt(A[1],1))+1) if mdt(o,-9).weekday()<5] # Mon=0
def strr(A,B): # A is str, B is list/tpl if list/tpl pairs, like [[a,a2],[b,b2]]
  A=str(A);
  if isinstance(B,tuple) and len(B)==2 and isinstance(B[0]+B[1],str): B=[B];
  for o in B: A=o[1].join(A.split(o[0]))
  return A
# def strr(A,B): # sloppy but works; A is str;
#   A=str(A); print('make sure B is dbl_list');
#   for i in range(len(B)): A=A.replace(B[i][0],B[i][1])
#   return A
# def med(A): return str(A).replace(', ',',')

def rlen(A): return range(len(A));
def arr(A):  return np.array(A);
def find(A): return np.nonzero(A)[0];
def isnum(A): return isinstance(A,bool) or isinstance(A,int) or isinstance(A,long) or isinstance(A,float) or isinstance(A,np.float64); # not an array
def floor(A): return np.floor(A) if isnum(A) else arr([floor(q) for q in A]); # beware the roundoff
def mod(A,B=1): return np.mod(A,B);
def sort(A): return np.sort(A);
def unique(A): E=list(set(A)); E.sort(); return E; # unique=np.unique
### plot
def plot(A): ### make this better
  mpl.pyplot.plot(A); mpl.pyplot.show();
### attr
def med(A): return '['+','.join(attr(audio.info))+']'
def diff(A): return A[1:]-A[:-1]
### lost fancy diff

#---
def df0(d): d.reset_index(drop=True,inplace=True); d.rename(columns=dict(zip(d.columns,range(len(d.columns)))),inplace=True); return d; # def df0(A): return pd.DataFrame(np.array(d));
def df2(d,d2): return df0(pd.merge(d,d2,on=0,how='outer',copy=False)); # merge by uk
nan=np.nan; np.cat=np.concatenate;
#--- 02 ---------------------------------------------------------------------------------------------------------------
def edit(fnm):
  fnm=(os.getcwd()+'/'+fnm) if not len(os.path.split(fnm)[0]) else fnm;
  if not os.path.exists(os.path.split(fnm)[0]): print 'edit: path does not exist, breaking'; assert 0;
  open(fnm,'w').close() if not os.path.exists(fnm) else None;
  sh(['/usr/local/bin/spyder','c:/programs/calc/py/Scripts/spyder.exe'][sys.platform.lower()[:3]=='win']+' '+fnm) # v.sy=='win'
def print3(*A,**B): # so print can be used in comprehensions
  sep,end,file=B.pop('sep',' '),B.pop('end','\n'),B.pop('file',sys.stdout); output='';
  if B: raise TypeError('extra keywords: %s' % B)
  for arg in A: output+=sep+str(arg)
  file.write(output[len(sep):]+end)
  # output=''; first=True / for arg in A: output +=('' if first else sep)+str(arg); first=False / file.write(output+end) / for i in range(len(A)): A[i]=str(A[i]); / file.write(sep.join(A)+end) # chgs A
def printl(A): [print3(o) for o in A]; # print list
#--- 04 ---------------------------------------------------------------------------------------------------------------
def wh(A='',p=0,B=0): # wh(-3); wh('',-2,locals()); wh('d*'); wh(int); going inside fn frm#<0
  # argchk: A is str/type; p is int; B is frameno/frame/dict/list;
  A,p=('',A) if isinstance(A,int) else (A,p); # wh(-3); wh(-2);
  # convert B to dict/list
  B=inspect.stack()[B+1][0].f_locals if isinstance(B,int) else B.f_locals if type(B).__name__=='frame' else B; # sys._getframe(B+1),locals() identical; .f_globals similar;
  if p==-3: return ['bool','int','int32','int64','long','float','str','tuple','list','dict','ndarray','TimeSeries','DataFrame','function','ufunc','builtin_function_or_method','module','type','classobj']
  if p==-2: #--- clean up locals() etc,return list
    B=B.keys() if isinstance(B,dict) else B[:]
    for i in reversed(range(len(B))): # drop _i22 etc
      if 2<len(B[i]) and B[i][0]=='_': o=B[i][1:]; o=o[1:] if o[0]=='i' else o; B.pop(i) if len(o) and ord('0')<=min(map(ord,o)) and max(map(ord,o))<=ord('9') else None;       
    x=range(len(B));
    if type(A)==str and A: x=[i for i in x if B[i][:len(A)-1]==A[:-1]] if A[-1]=='*' else B.index(A) # drop unneeded E for wh('d*')
    B=[B[i] for i in x];
    # drop fn_vm,fn_aux etc
    o1s=['v','nan','mm','mdt','dt2sec', 'arr','diff','find','floor','isnum','med','mod','plot','rlen','sort','strr','unique','df0','df2', 'T','F', 'edit','print3','printl',  'wh','attrC','clear','loadM','saveM', 'fnmT','mdir', 
         'sh','sh_','mawk','mzip','meml',
         'insp_stack2','kb',   'In','_ih','_i','_ii','_iii','_Out','Out','_oh','_','__','___','_1','_2','_3','_4','_5','_dh',
         'division','help','print_function','__builtin__','__builtins__','__doc__','__name__','__package__','__warningregistry__','_exit_code']
    return [o for o in B if o not in o1s]
  #--- p=-3,p=-2 ends ---------------------
  # below B must be dict; clean up C,calc cell_arr,type,mdl
  # wh2(_a='',_p=0,_b=0): C=get_ipython().magic('who_ls'); A=_a; p=_p; B=_b; del _a,_b,_p # avoid var_nm collision (%who_ls); # list_smart_sub; 
  C=wh('',-2,B.keys()[:]); E=np.zeros((len(C),5),dtype=object); E[:]='-'; # f=['nm','type','var_ptr/val/(sz)/fn_fnm','mdl','MB'] # B.keys() can evolve; B=copy.deepcopy(A0) 'breaks'
  for o in C:
    i=C.index(o); E[i,0]=o; E[i,2]=B[o];
    try: E[i,1]=type(B[o]).__name__; E[i,3]=inspect.getmodule(B[o]).__name__; # print o,'type('+o+')'
    except: pass
    # if (not E[i,3] is None) and E[i,3].startswith('numpy'): np.delete(E[i,:],0,i);
  # report/drop pkg(fnm grp)/module(fnm)
  x=[i for i in range(E.shape[0]) if isinstance(E[i,3],str) and E[i,3].startswith('IPython.core.')]; E=np.delete(E,x,0);
  x=[i for i in range(E.shape[0]) if E[i,1]=='module' and E[i,0]==E[i,3]];
  if x: print 'imports:  '+','.join(sorted(list(E[x,0])));           E=np.delete(E,x,0) # collect modules (nm=mdl)
  x=[i for i in E[:,0].argsort()  if E[i,1]=='module'];
  if x: print 'imports2: '+','.join([E[i,0]+'='+E[i,3] for i in x]); E=np.delete(E,x,0)
  x=range(E.shape[0]);
  if type(A)==str and A: x=[i for i in x if E[i,0][:len(A)-1]==A[:-1]] if A[-1]=='*' else E[:,0].tolist().index(A) # drop unneeded E for wh('d*')
  if type(A)==type:      x=[i for i in x if E[i,1]==A.__name__]
  if not len(x): return None
  # sort by type,calc E[:,2]
  E=E[x,:]; n=E.shape[0]; o=1000*mm(E[:,1],wh(-3))+np.argsort(E[:,0]); o[o==-1]=1000*1000; E=E[np.argsort(o),:]
  o2s=[['True','T'],['False','F'],[', ',',']]
  for i in range(n): # bad style - uses eval
    a=B[E[i,0]]; b=E[i,1]; E[i,4]='-';
    if   b in ['bool','int','int32','int64','long','float']: E[i,2]=strr(a,o2s)
    elif b in ['str']:                                       E[i,2]='\''+a+'\''          ### unicode->str
    elif b in ['list','tuple','dict']:                       E[i,2]='('+str(len(a))+')'
    elif b in ['ndarray','TimeSeries','DataFrame']:
      E[i][2]=strr(a.shape,o2s+[('L','')]);
      o=a.as_matrix() if (b in ['DataFrame']) else a; E[i,4]=str(np.round(o.nbytes/1024.**2,2))
    elif b in ['function']:                         o=E[i,2].func_code.co_filename; E[i,2]=o[o.rfind('\\')+1:]
    else:                                                   E[i,2]='-'
    # sort fn by fnm/mdl
    # m2=mm(E[:,0],np.unique(E[:,0])); m=mm(E[:,1],wh(-3)); m[m==13]=12.008; m[m==14]=12.009; m[m==-1]=99;
    # m3=np.zeros(n); x=np.nonzero(abs(m-12)<.5); o=mm(E[x,2][0],np.unique(E[x,2])); o[o==-1]=max(o)+1; m3[x]=o; # non-uniq messes up argsort,yucks
    # F=E[np.argsort(1e8*m+1e4*m3+m2)];
    # xcl ALL_CAPITALIZED vars,fn;
  print 'nm_______________type_____________val/(sz)/fnm_____mdl________MB___'
  for i in range(n): print '{:16s} {:16s} {:16s} {:10s} {}'.format(E[i,0][0:16],E[i,1][0:16],E[i,2][0:16],E[i,3],E[i,4]);
  # return E
# def get_frm(frm_no=0): return inspect.stack()[frm_no][0];
# def get_var(var_nm,frm_no=0): a=inspect.stack()[frm_no][0]; return a.f_locals[var_nm]
# def set_var(var_nm,obj,frm_no=0): a=inspect.stack()[frm_no][0]; a.f_locals[var_nm]=obj  # a=inspect.stack()[0][0].f_locals; b['a']; b['eee']=333
# def eval2(cmd,frm_no): o=get_frm(frm_no); a=eval(cmd,o.f_globals,o.f_locals); set_var(var_nm,a,o)
#--- getattr(obj,argnm,dflt)
def attrC(obj,spacing=10,collapse=0): #  print methods and doc strings for pkg/model/cl,dict/list/str; polluted with builtins etc;
  fn1=(lambda s: " ".join(s.split())) if collapse else (lambda s: s)
  print "\n".join(["%s %s" % (o.ljust(spacing),fn1(str(getattr(obj,o).__doc__))) for o in dir(obj) if callable(getattr(obj,o))])
  print [o for o in dir(obj) if o[0]!='_']
###--- want user_attr - no easy way to filter
def clear(A=''):
  gl=inspect.stack()[1][0].f_globals
  if type(A)==str and (A=='' or A[-1]=='*'):
    o=wh(A,-2,1);
    A=[q for q in o if q not in ['get_ipython','exit','quit'] and type(gl[q]).__name__[:10] not in ['module','function']];
  A=[A] if type(A)==str else A;
  for o in A: del gl[o]
# def loadM(fnm,vars=None): return loadmat(fnm,variable_names=vars,squeeze_me=True); # o=loadmat(fnm,variable_names=vars[:],squeeze_me=True); a=lambda: None; [setattr(a,q,o[q]) for q in vars]; return q; ### convert dict into a list
def loadM(fnm,vars=None):
  import scipy.io
  vars=[q[0] for q in scipy.io.whosmat(fnm)] if vars is None else vars;
  vars=[vars] if isinstance(vars,str) else vars;
  o=scipy.io.loadmat(fnm,variable_names=vars[:],squeeze_me=True); a=lambda: None; [setattr(a,q,o[q]) for q in vars]; return a;
def saveM(fnm,A):
  import scipy.io
  for o in A.keys():
    if isinstance(A[o],pd.DataFrame) or isinstance(A[o],pd.Series): A[o]=np.array(A[o]+0.);
    if isinstance(A[o],list) or (isinstance(A[o],np.ndarray) and A[o].ndim==1):
      if isinstance(A[o][0],str): o1=np.zeros((1,len(A[o])),dtype=np.object); o1[:]=A[o]; A[o]=o1;
      else: A[o]=np.reshape(np.array(A[o])+0.,(1,len(A[o])));
  fnm2=fnmT()+'.mat'; scipy.io.savemat(fnm2,format='5',do_compression=1,mdict=A); shutil.move(fnm2,fnm);
#--- 05 ---------------------------------------------------------------------------------------------------------------
def fnmT(): return datetime.datetime.now().strftime("%Y%m%d_%H%M%S_")+''.join(random.SystemRandom().choice(string.ascii_uppercase+string.ascii_lowercase + string.digits) for _ in range(32))
# def fnmT(): return v.q+'junk/fnmT_'+str(uuid.uuid4());
# def mdir1(fnm): o=glob.glob(fnm); o.sort(); return o;
def mdir(dir1,p=0): # mdir(dir1m,1) use glob.glob(); os.walk(dirname); os.path,getsize(fnm)
 dir1=dir1.replace('\\','/'); kb(os.path.isdir(dir1) and dir1[-1]!='/','mdir bad dir1') 
 o1=np.array(os.listdir(dir1)); n=len(o1); E=np.zeros((n,7),dtype=object);
 if n==0: return E
 for i in range(n):
   o=os.stat(dir1+o1[i]); E[i,:]=[dir1+o1[i],o1[i],0,o.st_size,o.st_atime,o.st_mtime,o.st_mode]; o2=o;
   o=o2; kb(bool(o.n_fields-o.n_sequence_fields-o.n_unnamed_fields)|bool(o.n_sequence_fields-len(o))|bool(o.n_unnamed_fields-3),'mdir 1');
   o=o2; kb(abs(o.st_ino)+abs(o.st_dev)+abs(o.st_nlink)+abs(o.st_uid)+abs(o.st_gid),'mdir 2'); kb(o.st_atime-o.st_atime,'mdir 3');
   "['n_fields','n_sequence_fields','n_unnamed_fields','st_mode','st_ino','st_dev','st_nlink','st_uid','st_gid','st_size','st_atime','st_mtime','st_ctime']"
   # n_fields=n_sequence_fields+n_unnamed_fields; n_sequence_fields=len(o2); st_ino=st_dev=st_nlink=st_uid=st_gid=0; st_ctime=st_atime;
 # calc isd,size_kb,dt
 o=(33206.-E[:,6])/16311; # print type(o),o
 for i in range(n): o[i]=int(round(o[i])); ### ugly, round(o) and np.round(o) fail
 E[:,2]=o; x=np.nonzero(o)[0]; # kb(mm(set(o),[0,1])<0,'mdir 4');
 for i in x:
   if E[i,1][-1]!='/': E[i,0]+='/'; E[i,1]+='/';
 E[:,3]=E[:,3]/1e3; ## E[x,3]=0; # o1[x] # some dir have 0<size
 for j in [4,5]:
   for i in range(n): E[i,j]=mdt(E[i,j])
 if p:
   for i in x: o=mdir(E[i,0],p); E=np.r_[E,o];
 E=E[np.argsort(-E[:,2]*(len(E)+1)+mm(E[:,1],np.sort(E[:,1]))),:]; return E
 o=pd.DataFrame(E,columns=['dnm','nm','isd','sz','dt','dt2','attr']); o.n=len(E) # df allows E.isd,E.sz,E.n etc
# def show_directory(name): return os.system("ls -l %s" % name); # BAD not safe: name == "/home/schwa ; rm -rf *"
# def show_directory(name): return subprocess.call(["ls","-l",name]); # GOOD safe
# mdir - want to process links as well (identify)
# os.path.isdir; os.walk os.stat,filecmp,shutil
#--- 06 ---------------------------------------------------------------------------------------------------------------
def sh(cmd, **kargs): return subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,preexec_fn=lambda:signal.signal(signal.SIGPIPE, signal.SIG_DFL),**kargs).stdout # .read()
def sh_(cmd,n=None):
  fnm0=v.q+'tmp/'+str(1000*1000+n)[1:]; fnm=fnm0+'_cmd.py'; fd=open(fnm,'w'); fd.write(cmd); fd.close(); # subprocess.Popen(['/usr/bin/python2.7',fnm3]); time.sleep(.1);
  with open(fnm0+'_out.log','wb') as out, open(fnm0+'_err.log','wb') as err:
    subprocess.Popen(['/usr/bin/python2.7',fnm],stdout=out,stderr=err)
def mawk(fnm,fA,sep=',',cmdA=''):
  fnm=fnm if (fnm[-3:]=='.gz' or os.path.exists(fnm) or not os.path.exists(fnm+'.gz')) else fnm+'.gz';
  if not os.path.exists(fnm): print 'mawk fnm(+.gz) does not exist '+fnm; return None;
  sep=sep.strip(); cmd=('zcat ' if fnm[-3:]=='.gz' else 'cat ')+fnm+' | awk '+('' if sep=='' else '-F"'+sep+'" ')+'-v OFS="," \'{print '+','.join(['${:d}'.format(i) for i in fA])+'}\' '+cmdA; return msh(cmd); # print cmd
def mzip(fnm0,fnm): msh('gzip -f '+fnm0+'; if [ -f '+fnm+' ]; then rm -f '+fnm0+'.gz; else mv -f '+fnm0+'.gz '+fnm+'; fi &'); # save zip no incomplete files; using tmp file to avoid conflicts
def meml(to,subj,body): o=subprocess.Popen('/usr/sbin/sendmail -f vmoroz@kcg.com {}'.format(to),stdin=subprocess.PIPE,shell=True); print>>o.stdin,'From: vmoroz@kcg.com\nTo:{}\nSubject:{}\n{}\n'.format(to,subj,body); o.stdin.close(); o.wait(); # o,subject,body sendmail
#--- 07 ---------------------------------------------------------------------------------------------------------------
def kb(A=1,txt='kb msg_dummy'):
  if A is None: A=0
  if type(A) not in [bool,int,long,float,str]: A=any(1e-10<abs(A)) # if any(1e-10<abs(-1+np.zeros((10,3)))):
  if bool(A):
    print txt; # ipdb.set_trace(); # ipdb smtimes permanently redirects prints to console,yuck
    # pydevd.settrace(); # bpt has to be on line with statemt (comment is not good enough)
    
    while 0: # no "var peek" into fn_calling, only into fn_def
      a=raw_input('*>') # ipdb.set_trace(); [examine vars]; c;
      if not a: continue
      elif a=='qqq': print 'kb qqq=continue...'; break # insp_stack2() ->2; wh(0,2); _b=inspect.stack()[2][0].f_locals; _b.keys()
      elif a.startswith('. '): a='_b["'+a[2:]+'"]' # . moduleList
      try:      print 'kb_eval:\n',a,  eval(a),       ' ~kb' # print_expr,breaks on a=1 etc;
      except:
        try:    print 'kb_exec:';    exec(a); print ' ~kb' # run_statemt
        except: print 'kb_except\n'; pass
      ### o=eval(); if o not is None: print o # to kill print_None
  return
#---
def insp_stack2(p=0): # pretty_outp; also frm=sys._getframe(n),frm=inspect.getouterframes(inspect.currentframe())[n],traceback.extract_stack(limit=2)[-2][2],
  # lineno,fnm_lineno_text +-2 bc fnm not refreshed on execfile()
  o1s=[['<ipython-input-','<ipy-'],['\\','/'],['D:/soft/py/eclipse/plugins/org.python.pydev_3.0.0.201311051910/pysrc/','~/pydev/'],['C:/Programs/computations/WinPython27/python-2.7.5.amd64/','~/'],['~/lib/site-packages/IPython/core/interactiveshell.','~/~ipy.'],['~/lib/site-packages/IPython/core/','~/ipy/']]
  o2s=['~/~ipy.py','~/pydev/pydev','~/pydev/_pyde','~/lib/SocketS','~/lib/BaseHTT','~/lib/SimpleX']
  if type(p).__name__=='traceback': # print tb_obj - tb,line# etc
    o2=p; print 'insp_stack2(tb) tback/err msg (most recent call last): fnm/fn, tb line# er_type: msg' # A=sys.last_traceback;
    while o2: print '{:40} {:20} tb_{:8} {:5} {}: {}'.format(strr(o2.tb_frame.f_code.co_filename,o1s),o2.tb_frame.f_code.co_name,str(o2)[31:-1],o2.tb_lineno,'o1.f_exc_type.__name__','o1.f_exc_value'); o2=o2.tb_next
    return
  A=inspect.stack(); E=[]; # frm,fnm/ipy_prompt,line#,fn_parent,fnm_line_text,xx0
  for i in range(len(A)):
    o=[str(A[i][0])]+list(A[i][1:])[:]; kb(o[5],'o[5]'); o1=A[i][0]; o2=o1.f_exc_traceback;
    o3=['frm_'+o[0][27:-2].lower(),strr(o[1],o1s),str(o[2]),o[3][:19],'-' if(o[4] is None) else o[4][0].strip()[:59],
       ('-' if(o2 is None) else 'tb_%s %3d %s: %s' % (str(o2)[31:-1],o2.tb_lineno,o1.f_exc_type.__name__,o1.f_exc_value))]
    if p or o3[1][:13] not in o2s: E+=["{:2} {:12}{:40}{:5}{:20}{:60}{:12}".format(i-1,*o3)]
  n=len(E); o=['','\n']; print 'frm#__frm_________fnm___________________________________line#__inside_this_fn______executing_this_code(=fnm_line#_txt)_________________________tback'
  for i in range(n-1): print '{:2} '.format(i)+E[n-1-i]+o[(1-bool((i+1)%3))*(i!=n-2)] ### recalc frm_base# for 0<p?
  print '-'*160
# inspect.stack() can be replicated with o=sys._getframe(i),rpt above and reading src_code from fnm.py;
#   n=2; frm=sys._getframe(n); [frm,frm.f_code.co_filename,frm.f_lineno,frm.f_code.co_name,0,0] # xx~frm.f_code.co_code[frm.f_lineno], need to read fnm.py to get src_code;
# frm                        has f_code.co_filename,f_lineno,f_globals,f_locals, f_back 'frm_parent', f_builtins 'boring',f_exc_traceback,f_exc_type,f_exc_value,f_lasti 'idx of last_attempted_instr',f_trace 'tracing fn for this frame',f_restricted 'frame is in restricted execution mode' # traceback if raised in this frame, or None
# frm.f_code                 has co_argcount,co_cellvars,co_freevars,co_consts 'const in nsp',co_names 'fns called in nsp?',co_varnames, co_filename,co_firstlineno,co_name 'nsp/fn_name', co_code 'bin_xx',co_lnotab 'bin_xx', co_nlocals '?',co_flags '?',co_stacksize '?'
# frm.f_exc_traceback~tb_obj has tb_frame,tb_lineno,tb_lasti,tb_next 'next inner tb_obj (called by this level)'; tb_frame ~frm_parent,tb_lineno 2 GOOD,tb_lasti 9,tb_next None; 
#   o=sys._getframe(n-1); o.f_exc_traceback.tb_lineno,o.f_exc_type.__name__,o.f_exc_value # ['line#','exc_type','exc_msg'] # 'ZeroDivisionError','integer division or modulo by zero',
#   [x for x in dir(e.f_exc_type) if not x.startswith('__')]
# QUIRK f_exc* is bound to frm_child (bound to frm 1lvl deeper than frm_where_exc_raised); frm_child.f_exc_traceback.tb_frame points to frm_where_exc_raised
#   n=2; frm=sys._getframe(n); o=sys._getframe(n-1).f_exc_traceback; o.tb_frame is frm; # o.tb_frame points to frame_parent=frm_inside_fn3, while 1/0 was called inside fn3
# o=sys.exc_info(); o=sys.last_exception
# tb study: o=sys.exc_info() 'list of raised exceptions BROKEN? tb shows on scrn but does not stick'; ipdb.post_mortem(sys.last_traceback)
# o1=inspect.stack(); o1=[o[0] for o in o1]; o2=sys.last_traceback; wh(o2.tb_frame); ipdb.post_mortem(o2);
# while o2: print (str(o2)+'\n') if (o2.tb_frame in o1) else '~'; o2=o2.tb_next
#----------------------------------------------------------------------------------------------------------------------
#--- mreadx
# import xlrd;
# def mreadx(fnm):
#  bk=xlrd.open_workbook(fnm) # bk.sheet_names(); sh=bk.sheet_by_index(2); sh=bk.sheet_by_name('sheet 1')
#  E=[]; f=[]
#  for sh in bk.sheets():
#    n,nt=sh.nrows,sh.ncols; B=np.zeros((n,nt),dtype=object) # print sh.name,n,nt; # E=[[None]*nt for i in range(n)];
#    for i in range(n):
#      for t in range(nt): B[i,t]=sh.cell(i,t).value
#    if 0<n+nt: E.append(B); f.append(sh.name)
#  for j in range(len(E)): # clean up unicode
#    if type(f[j]) is unicode: f[j]=str(f[j])
#    n,nt=E[j].shape
#    for i in range(n): # map() does not work bc 
#      for t in range(nt):
#        if type(E[j][i,t]) is unicode: E[j][i,t]=str(E[j][i,t])
#  return (E,f)
#----------------------------------------------------------------------------------------------------------------------
