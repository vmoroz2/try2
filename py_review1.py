# 00 general notes,IDEs;
# 01 install,path,cfg,alias,macro,magic
# 02 ipy,editor,log,hist
# 03 help,search(~which)
# 04 whos,clear,save_txt, 
# 05 dir,mv_fnm; fnm.py from shell,fnm.bat from py;
# 06 run,profile;
# 07 dbg/traceback; - TO REVIEW
# 08 github         - TO REVIEW
#--- 01 startup.py has install/update; startup/cfg --------------------------------------------------------------------
from __future__ import division
from vm0 import * # execfile(v.q+'vm0.py')
#--- 02 editor chd_hist etc -------------------------------------------------------------------------------------------
# edit(), drag-and-drop;
# %cls / %colors / %precision
# cmd_hist arrows OK
# auto completion cmd/fnm tab OK; 
# _ih,_oh,_dh, 'fn arg1 arg2'
### edit in web browser - Jupyter?
#--- 03 help on py ----------------------------------------------------------------------------------------------------
# ?A,??A, type(A) and ?type / help(A) (verbose), spyder help->python documentation (verbose), web
# A.__dict__ ~ attr(A)
### %qtconsole/QT Assistant look interesting, not set up;
# A. tab is good
# %psearch np.*.random
# dir(A) ~ methods(A) - fns that can be applied to A
#--- 04 whos(), clear(), load/save ------------------------------------------------------------------------------------
# a=234; b=12.5; c='wert'; A=13; E=[1,2,5]; i=-55; wh();
wh(),clear() # %who / %who_ls / %whos / %clear / %reset -sf / %reset_selective / %xdel
import gc,weakref; sys.getrefcount
# var explorer has save .mat
#--- 05 pwd,cd,dir etc ------------------------------------------------------------------------------------------------
# %ls,%ldir
import os; os.getcwd(); os.chdir('dir1'); os.system('mkdir dir2'); os.popen('notepad'); os.listdir("."); dir(os); # pwd; cd; mkdir; # avoid 'from os import *' bc open(),os.open() are different
import shutil; shutil.copyfile(fnm,fnm2); shutil.move(dir1,dir2); # higher level file and directory management tasks
import glob; glob.glob('D:/*/*.txt');
#--- 06 profiling -----------------------------------------------------------------------------------------------------
# %%time / %%timeit
import profile,pstats; profile.run('np.random.random((5000,5000))','fnm.stats'); pstats.Stats('fnm.stats');
from timeit import Timer; Timer('t=a;a=b;b=t','a=1; b=2').timeit(); Timer('a,b=b,a','a=1; b=2').timeit() # profile,pstats; traditional swapping args vs tuple arg pack/unpack
### check profiling_spyder
#--- 07 dbg/kbd -------------------------------------------------------------------------------------------------------
import inspect,ipdb; ipdb.launch_ipdb_on_exception(); # is not visible to py9
### pkg_reload broken %reload, reload() (.pyc,loads old ver from some cache)
# %tb:
# pdb
# TODO # FIXME # HINT

#--- ipdb h; init in .pdbrc,pdb~ipdb;
# kb(),insp_stack2(),whos2(); from numpy.lib.utils import source; source(fn1) 'fnm+src,good enough';
# help,h; alias,unalias;
# run,restart; where,w,bt; up,u; down,d; next,n; step,s; jump,j;continue,cont,c; return,r; until,unt; commands[cmd to continue]; debug[dbg2];
# whatis;args,a; pinfo,pdef,pdoc; list,l; pp,p # pp get_ipython().magic('who_ls'); src_code,print
# break,b,tbreak,enable,disable,condition,ignore,clear,cl; quit,q,exit; EOF; #bpts
# if stuck on input - do empty line; stuck on output - "q"
# b=123; whos2() 'mixed statemt fail in ipdb'; a?? fails in ipdb,eval(), use numpy.lib.utils.source(fn), insp_stack2,whos2(),
# frm_stack~stack_trace~stack_snapshot, for interactive and post-mortem debugging (pm uses traceback)
%pdb on; %debug~ipdb.pm() # open dbg at latest exception (it clobbers/kills prev ones), init in `InteractiveShell.pdb`;
## ipdb test
clear(); from vm9 import *;
import ipdb; ipdb.launch_ipdb_on_exception(); # ipdb.set_trace()
ipdb.run('wh()'); ipdb.pm() # dbg/traceback printout; ipdb.post_mortem, vars in "old fn frames" are preserved until gc
def set_trace(): from IPython.core.debugger import Pdb; Pdb(color_scheme='Linux').set_trace(sys._getframe().f_back) # set bpt
def debug(f,*args,**kargs): from IPython.core.debugger import Pdb; pdb=Pdb(color_scheme='Linux'); return pdb.runcall(f,*args,**kargs) # dbg_run_fn
def fn1(): a1=1.1; b1='b1_'; print 'in fn1'; fn2(); return
def fn2(): a2=2.2; b2='b2_'; print 'in fn2'; fn3(); return
# def fn3(): a3=4.4; b3='b3_wert'; print 'in fn3,running dbg/ipdb'; ipdb.set_trace(); return
def fn3():
  try: 1/0
  except: pass
  a3=3.3; b3='b3_'; print 'in fn3,running dbg/ipdb'; kb(); 1; # ipdb.set_trace();
ipdb.run('fn1()')
assert x<0,'x too small' # break if error (chk dupl_in_list,broken "invariants"~smth_constant_in_class,like inv_map(map) etc)
## pydevd: remote_dbg uses dbg_server and py_main_thread; launch dbg_svr, then run pydevd.settrace() in main; set bpt - green_pin,ipdb generates warn;
# start dbg server, F9 (open dbg win,run fnm_in_dbg,stop at bpt), select frm_stack_level in GUI, on bp in Debug window shows "Debug"/extended_frame/fn_stack,"variables" and "expressions (broken a bit)"
# navigate frm_stack in "Debug" window, run cmd in PyDev debug_console; use dir(),whos2() etc (%whos, a?? and oth magics do not work); running in dbg is quite slower;
### want ipdb.post_mortem(sys.last_traceback()) (problem with traceback),remote_dbg; is fn_stack with vars avail in pm?
# inspect etc; obj_introspection ~"obj?", access to internal components, code looking at mdl/fn in mem as obj, getting info and manipulating them
import inspect; getmodule,getmro # formatargspec(getargspec(fn)),getdoc,getfile,getsource,getsourcefile,isbuiltin inferior to a?/a??
# obj=a; [o[0] for o in inspect.getmembers(obj,callable) if not o[0].startswith('__')] # messy ~ a.attr_list
inspect.stack(),formatargvalues(getargvalues(frm)) # inspect.stack() base at [-1]; (frm,fnm,#,<module>,fn_call,0~err_code); currentframe=sys._getframe(0)

#--- 08 github --------------------------------------------------------------------------------------------------------
# sudo apt-get install git; cd ~/D/py/; git init;
# git config --global user.name 'vm'; git config --global user.email 'vadim.moroz@gmail.com'; git config --global color.ui 'auto'
# git add *.py;
# git mv fnm1 fnm2
# git rm --cached fnm.py # stop tracking
# git commit -m "msg" # spaces in comment crash it
# git diff; git -a commit -m "msg" (or 'git add -u')
# git log; git show <hash> # shows changed files etc

### checkout: how to restore old vers

### how to manage branches (split,merge etc)

#---
# git remote add origin2 ssh://vmoroz2@github.com/try1

# git remote add origin2 https://github.com/vmoroz2/try1.git
# git push -f origin2 master
# git push -u github_vmoroz2 master # breaks?
curl -u 'USER' https://api.github.com/user/repos -d '{"name":"REPO"}
# branch (allow to evolve ver1, ver2 at same time)/fetch/pull (=fetch+merge,chg_remote into local)

# git clone https://github.com/vmoroz2/try1 # load from web; fails on vmware_shared_dir and nonempty dir

ssh-keygen
ssh-copy-id -i ~/.ssh/id_rsa vmoroz2@github.com
git config github.com git@github.com:vmoroz2/try1.git


# %pastebin:
import numpy as np; A=np.random.random((3,4));

### start server, see as webpage, 

### pull github
### put online file + comment

### branches split/merge

### bup whole git dir

# git 

# source control slang: fnm_tracking;  branches;
# fnm can be untracked, modified, staged/unstaged (marked for commit and copied to "staging area"), commited='create repo snapshot with comment';
# working_dir,staging_area/"index" (fnm with list for next commit),.git dir (db with snapshots)
#--- other
import getopt,argparse; sys.argv; # cmd_line_args stored in a list sys.argv; processes sys.argv like Unix getopt(); argparse more powerful
sys.stderr.write('warn1\n'); sys.exit() # to terminate a script; sys module also has attributes for stdin,stdout,and stderr (can redirect stderr and make err msg visible)
# %%pypy / %%python / %%python2 / %%python3 # for fancy apps

### with()
#### matplotlib as mlp
#--- BROKEN
# !cd dir1 fails
# %%xx  - cannot terminate
# WEAK SPOTS:
# py obj classes
#--- code checkers: ---------------------------------------------------------------------------------------------------
#   PyLint (verbose,good but too sctict - var_name>3 lett) pypi.python.org/pypi/pylint,logilab.org/project/pylint
#   PEP8 (complementary to PyLint) pypi.python.org/pypi/pep8
#   PyChecker (compiles code) pypi.python.org/pypi/PyChecker,pychecker.sourceforge.net
#   pyFlakes (light and sloppy)
#----------------------------------------------------------------------------------------------------------------------
