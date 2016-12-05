# 00 general notes,IDEs;
# 01 install,path,cfg,alias,macro,magic
# 02 ipy,editor,log,hist;
# 03 help,search(~which)
# 04 whos,clear,save_txt, 
# 05 dir,mv_fnm; fnm.py from shell,fnm.bat from py;
# 06 run,profile;
# 07 dbg/traceback;
# magics,clear_var,path,log; help,hist,dir,edit,load_code; run/profile; run_shell/cmd_arg; dbg/traceback,whos,search(~which),history,save_txt;  ipdb/inspect;
## magics (ipy interactive features %fn)
# text pre-processing (magic_cmd are converted to py_cmd and fed into interpreter); Line magics (1-liner,args on line1); Cell magics (2+ liner,arg1 on line1,arg2 on lines 2+ until blank line)
#--- 03 help,search(~which) -------------------------------------------------------------------------------------------
?*.sin* / ?np.*.rand* / ?obj / ??obj  'type/string_form/file/def/source' / help('abs') / help(obj) / dir(obj) # help() uses x.__doc__; # also W-sp/Tab,ecl_popup,docs.python.org/2/, win_help.chm
from spyderlib.widgets import pydocgui; pydocgui.main() # unavail 2016; need to lauch from 2nd console; "import pydoc; pydoc.gui()" broken under win
subprocess.Popen(['D:/soft/py/bin/help_pyDoc.bat']) # os.system(r'D:\soft\py\bin\help_pyDoc.bat') 'ok no wait'; os.spawnl(os.P_NOWAIT,'D:/soft/py/bin/help_pyDoc.bat') 'oddly kills parent py'
# ecl pop-up: yel_sq(pkg)/ar-(mdl)/C(cl)/M(fn)/cog_wheel(float etc)
# help feature_see_also seems unavail - too many pkg by diff ppl?); web-like intface back button (have __doc__ reader,looks useless)
# %magic / %lsmagic / %magic_name? / %guiref # -brief -rest; magic_list; magic_help
# %pdef / %pdoc / %psource / %pfile / %quickref / cmd? / cmd?? 
# %psearch -i a* function  # ?-i a* function / -i a* function? broken; search by type function/string/int/etc; ignoring _* (-a - include _*),-c/-i case-(in)sensitive [`InteractiveShell.wildcards_case_sensitive`]; matching on attr as well
#--- 04 wh(),clear() --------------------------------------------------------------------------------------------------
wh(); %who / %whos int / %who_ls / dir(),globals(),locals() # ~ML,by type (not by var); huge lists with mdl_fns_loaded etc
%reset -f '~ ML clear all'/ %reset_selective -f a 'a equiv to ML a*'/ %xdel a 'also removes all pointers,needed to kill output_hist'/ del a '~ML clear a' # -s in out dhist array
import gc,weakref; sys.getrefcount # Jython or IronPython, rely on gc from platform (JVM or the MSCLR); cannot get ful obj_ref_list (does not exist,can scan globals() for partial list)
# garbage_collection uses sys.getrefcount(obj)=n_links; obj can have circular_ref, needs special treatment
# weakref is not counted and does not stop gc; weakref is used for caching (many ints etc are cached for speed - some system_design reason);
clear(); %clear / %cls / %colors # clear terminal,colors
#--- 05 dir,mv_fnm; fnm.py from shell,fnm.bat from py -----------------------------------------------------------------
## dir,mv_fnm
%cd / %cd - tab / %dhist / %pwd / %pushd / %dirs / %popd /  # cd -3 (dir-3); cd -foo; cd -q; dir_hist; cd from dir_stack
import os; os.getcwd(); os.chdir('dir1'); os.system('mkdir dir2'); os.popen('notepad'); os.listdir("."); dir(os); # pwd; cd; mkdir; # avoid 'from os import *' bc open(),os.open() are different
import shutil; shutil.copyfile(fnm,fnm2); shutil.move(dir1,dir2); # higher level file and directory management tasks
import glob; glob.glob('D:/*/*.txt');
## fnm.py from shell,fnm.bat from py
#!/usr/bin/python # shebang directive unix; 'unix script.py' -> 'py script1.py'
# echo cat vi/emacs ; awk -F'#\[Out\]# ' '{if($2) {print $2}}' ipython_log.py # text filtering; py good for shell scripts, moving files, reformatting text etc
$python script.py < in1.txt > out.txt; python script.py | prog2; python -m module [arg]; # no interact_cons,just run script
foo='~/dir1'; a=!dir $foo | grep bar 'SList output'; os.system('xx'); import subprocess; # !! / %sx / %sc -l/ %system; # subprocess spawns processes,does io,"safe"
import getopt,argparse; sys.argv; # cmd_line_args stored in a list sys.argv; processes sys.argv like Unix getopt(); argparse more powerful
sys.stderr.write('warn1\n'); sys.exit() # to terminate a script; sys module also has attributes for stdin,stdout,and stderr (can redirect stderr and make err msg visible)
# %%script bash / for i in 1 2 3; do / echo $i / done # --bg --out OUT --err ERR --proc PROC; %%cmd / %%powershell / %killbgscripts # =`%%script cmd`;=`%%script powershell`
# dos type fnm=cat fnm; set~printenv
#--- 06 run,profile ---------------------------------------------------------------------------------------------------
# runfile - loading, execfile - as script
eval(cmd)
%prun [opts] statement # profiler; profile.help(); -r # return pstats.Stats obj; / -l # <limit> string (only some fn_names),int(#ln),float(.25 - quarter of output),e.g. '-l __init__ -l 5' top 5 ln of constructors; / -s <key> # sort by key
%prun -l 7 -s cumulative fn1(); %run -p -s cumulative fnm.py; %lprun -f fn1 -f fn2 statemt_to_profile # %prun (cProfile) for macro_profiling and %lprun (line_profiler) for micro_profiling
$python -m cProfile cprof_example.py; execfile(fnm); %run [-n -i -t [-N<N>] -d [-b<N>] -p [profile options]] fnm [args] # like $python fnm args; with ipy traceback; %run in empty nsp, %run -i in current nsp; leaves behind vars
%timeit range(1000) # Line magics (1-liner,args on line1)
%%timeit x=numpy.random.randn((100,100)) / numpy.linalg.svd(x) # setup not timed
import profile,pstats; from timeit import Timer; Timer('t=a;a=b;b=t','a=1; b=2').timeit(); Timer('a,b=b,a','a=1; b=2').timeit() # profile,pstats; traditional swapping args vs tuple arg pack/unpack
timer=time.clock if sys.platform[:3]=='win' else time.time; min(Timer.total(1000,str.upper,'spam') for i in range(50)) # profile -wall_clock,cpu_clock
# c.TerminalIPythonApp.extensions=['line_profiler']
# %load_ext line_profiler # works for iPython.exe, not for pyDev (%lprun unavail)
import unittest,doctest ## unit/system testing, white/black box testing
#--- 07 dbg/traceback(~er_msg,fnm/line#/fn/fnm_txt + fnm_caller/..),ipdb,inspect --------------------------------------
# tb_obj~err_log, it contains "stack_trace" (fnm,line#,fn_nm,er_type,er_msg),has link to frm (possibly frm_dead as well); ipdb.pm(tb_obj) (no frame stack walk here, just look at obj before gc deletes them?);
o=sys.exc_info()[2]; o=sys.last_traceback; insp_stack2(o)
%tb 'prints tb, mode set up in %xmode'; traceback.print_exc(file=open('fnm.txt','w')); threading.settrace(fn) 'tb_multithr'
from IPython.core.debugger import Tracer; Tracer()()
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
#--- ipdb test
get_ipython().magic('%reset -f'); from vm0 import *; import ipdb; ipdb.launch_ipdb_on_exception(); # ipdb.set_trace()
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
#-----------------------------------------------------------------------------------------------------------------------
