# 00 general notes,IDEs;
# 01 install,path,cfg,alias,macro,magic
# 02 ipy,editor,log,hist
#--- 00 general notes on py/ipy
# .py .pyc .ipy; fnm.ipy - as if cmd was entered on cmd line (not useful for complex proj)
# >>> - py(just scripts,little interaction); [1] - ipy (py+tab_compltn,hist,magic_fns,traceback/dbg, more like R and ML)
# segmented product,has many several versions of "half-baked" GUI/IDEs,limited community (vs R and ML)
# py flavors:
#   CPython(traditional),RPython (compiles py code) -> PyPy - just-in-time compiler (C libs etc) py 2 exe written in py itself, 10x faster except file ops;
#   Cython(libs in C),IronPython(C# .NET Common Language Runtime platform),Jython (compiles py program into Java byte code for any JavaVM, with acess to Java lib from py);
#   some pkgs py to cpp,.pyo (modest speed imprvmt)
#   The Pyrex lang - easy-write-py-extensions (compile via C code to py ext) cosc.canterbury.ac.nz/~greg/python/Pyrex/; Pyrex is a large subset of Python, with optional C-like types for vars
# IDEs:
#   eclipse+PyDev; wingIDE (no ipy); IDLE (auto-import,auto dir_add); pyCharm,KomodoIDE
#   canopy,winpy pkg have editor,cmd_win,help_win(object inspector),var_explorer enthought.com/products/epd/ win,osX,RHL (32/64) - good package (matlab-like GUI)
#   spyder - even mode MATLAB-like GUI (on top of canopy or part of winPy)
# code checkers:
#   PyLint (verbose,good but too sctict - var_name>3 lett) pypi.python.org/pypi/pylint,logilab.org/project/pylint
#   PEP8 (complementary to PyLint) pypi.python.org/pypi/pep8
#   PyChecker (compiles code) pypi.python.org/pypi/PyChecker,pychecker.sourceforge.net
#   pyFlakes (light and sloppy)
# PyDoc ~help()+GUI_html - doc_system (broken on py2.7_win); win_help .chm ok; Sphinx - py_doc_fancy;
#--- 01 py/ipy install ------------------------------------------------------------------------------------------------
# python.org 2.7.12 and 3.5 (py3.* to be avoided - not enough users/packages)
# win64 numpy 1.11.2 for py2.7; there is no good free Fortran64 compiler,"unofficial numpy1.xx" licensing is in grey zone
# numpy on sforge 1.8.0 for py 2.7 and 3.5
# scipy.org(0.18),pandas (0.19)
# SimPy - Mathematica alternative
# frozen_binaries - PythonVM+"attached code",single-file executable
# 2to3 - convert py2.7 to py3
# import distutils,py2exe; $pyInstaller - generate distributable pkgs
# curses - lib for very old tex-only terminals (useless)
# VM py installs: winPython C:\Programs\calc\py\Scripts\ipython.exe; Eclipse+pyDev; mklink /D "C:/Programs/py" "C:/Programs/calc/WinPython27/python-2.7.5.amd64";
#   py_canopy C:\Programs\calc\py_canopy\Canopy\App\pythonw.exe,C:\Programs\calc\py_canopy\Canopy\App\appdata\canopy-1.1.0.1371.win-x86_64\Scripts\ipython.exe
# winpy/spyder (Qtconsole) setup: C:\Programs\calc\py\scripts\spyder.exe /wait 1min/editor "New Window" to dock out/Interpreters "Open ipy"
#   vert_line 160; sep_line 120; C:\Programs\py\Lib; install ipdb to py2.7.5
# pyDoc C:/Programs/py/python.exe C:/Programs/py/Lib/pydoc.py -g # ugly; pydoc text search broken; some win pkg missing, not supported
# win - install anaconda; conda may overshadow pip;
# lin sudo apt-get install spyder,sudo pip install spyder
# pip list --outdated | sed 's/(.*//g' | xargs -n1 pip install -U)
# pip list --outdated | cut -d ' ' -f1 | xargs -n1 pip install -U
#--- 01 path,cfg,alias,macro (~.bashrc/startup.m)
# conda update --all (win pip blocked by conda)
sys.path 'a list'; sys.path.append('path1'); # lib1.py on sys.path is loaded
o=dict(os.environ); ','.join(sorted(o.keys())) 'env_vars';
# in lin py listens to env_vars $PYTHONPATH etc (~ ML addpath in startup.m)
# $ipython.exe -h (boring, can do inside ipy)
## ipy_cfg (oddly no effect on pyDev)
# C:\Users\u\.ipython\profile_default\ipython_config.py
%automagic # on/off;  if 'automagic' enabled (via cmd line or %automagic),no need for '%' for line magics (cell magics still need '%%')
%autocall 1 # 0/1/2 off/smart/on; "fn args"->"fn(args)"; ML is "on"
# "/fn1 arg1,arg2" -> fn1(arg1,arg2); "/fn 1,2" -> fn(1,2) / ",fn1 a b c" -> fn1("a","b","c") / ";fn1 a b" -> fn1("a b")
%pprint / %precision # pretty_print,precision (also via `numpy.set_printoptions`)
%env / %config / %config IPCompleter / %config IPCompleter.greedy = x
%alias name cmd / %alias bracket echo "in <%l>" / bracket a b / %unalias # can be shadowed by vars etc; %l tells alias "till end of line"; bracket: <hello world>
%alias parts echo first %s second %s          / %parts A B / %alias_magic [-l --line] [-c --cell] name targe # l and s mutually exclusive; alias for existing fn_magic
%macro [options] name n1-n2 n3-n4 ...# ranges of history,fnm and strings
%macro macro1 44-47 49 / print macro1 # from lines in hist
#--- 01 magic_useless -------------------------------------------------------------------------------------------------
%install_ext url # install pkg [.py .zip]
%rehash / %rehashx # rescan executable files in $PATH
%pinfo obj / %pinfo2 obj # help; = ?obj ,obj? ; ??obj ,obj ??
%bookmark: # bmk_dirs; %cd -bmk <name> or cd <name>; saved in profile_info
%connect_info # info for connecting other clients to this kernel (same vars?)
%profile # print your currently active IPython profile (I get 'default')
%doctest_mode # make ipy like py (>>> prompt,exception_plain,disable pretty_print)
%ed # open notepad,execute code (edit is better)
%more / %less / %page / %pycat # uses env_var PAGER,~ poor man's "display"; syntax_highlight
%recall / %rec / %rerun # put hist to cmd_line
%gui [guiname] # "threaded shells","event loop integration"
%loadpy # = %load
%%file # save_code into fnm.py
%%capture # = %run,collect output
%pastebin # upload to code_share_website
%pylab # matplotlib pkg
%qtconsole # sep_console (not in pyDev)
%save # save input/macro/etc into .py
echo # alias to system echo, poor man's print
#--- 02 ecl_pyDev -----------------------------------------------------------------------------------------------------
# installed C:\Programs\computations\jdk1.7.0_45, ecl(portable); point ecl to py; Window->Preferences,General-Keys - sort by key,F9->out,CAEnter->F9 (run selection in interpreter); pydev-editor - Comments,chg color
# ecl dir struct ~java_classes (plenty of subdirs,empty_dirs,xml); .metadata (4k+ files); fnm_lbl (silly); new_project->fnm; "perspective"="set of windows"; pyDev/dbg/resource (?); ant - for xml;
# editor: C-space is "tab-cpl equiv"; comment C/; C-rclick go to fn_def;
# console: can have several interpreters (Console - yellow_plus - new_console_view helps); kill console selectively - terminate (red sq); perspective_switch_button (py/dbg template,var_browser,remembers window posn)
# drop_down in cmd; F9 sends cmd_editor_Select to "active" console; auto-help in cmd (searches by pkg), auto_import in cmd and editor;
# broken/odd: ipy with '>>>' prompt; not there: %qtconsole, C-D(win)C-Z/(lin) to exit; run_in_menu gives terminated console; plot slow; ecl annoying popup_cmd - no easy escape
# 3-click new ipy console; ipy/pydev startup msg,constrained prompt '>>>',dbg
# ecl profiling C:\Programs\computations\jdk1.7.0_45\bin\jvisualvm.exe ecl startup 30s,py_cons 10s/5s (libs/guis/dirs)
# D:/soft/py/startup.py executed at startup (ecl setting)
### ecl edit_new_file - drag-and-drop; finddiff - need to use ecl_filesystem,messy; dbg_perspective F9 is broken;
### iPython.exe - broken prompt (bad chars)
$ipython notebook # ipy cmd_intface_browser chrome bad init; IE ok
#--- 02 change prompt '>>>' (fails in pyDev)
import sys
class Ps1b(object):
  def __init__(self): self.p=0
  def __str__( self): self.p+=1; return '[%d]>>> ' % self.p
class Ps2b(object):
  def __str__(self): return '[%d]... ' % sys.ps1.p
sys.ps1=Ps1b(); sys.ps2=Ps2b() # [1]>>> (2 +\ [1]... 2)\ 4\ [2]>>>
#--- 02 ipy,editor,log,hist
x=raw_input('enter int:') 'to keep window from closing'; import getpass; a=getpass.getpass(prompt='passwd: ') # kb_input
# x=123+ \ 456 ; a='abc\def'; # wrapping long lines with "\"
%edit [options] [args] -x fnm.py # set ``TerminalInteractiveShell.editor`` ; see edit()
import readline # interactive cmd_hist, tab_compl etc
# to comment out code in ecl: C/;
# raise SystemError (requires try/except in caller's mdl); wrap into a fn (still need indent)
# 'if 0:' or 'def fn:' (unwanted indent is unavoidable)
# -*- coding: utf-8 -*- # for non-ascii cars
%logstart [-o|-r|-t] [log_name [log_mode]] / %logon / %logoff / %logstate / %logstop # start/restart/stop/state/full_stop logging
logging.debug('dbg info'); logging.info('info msg'); logging.warning('warn: %s not found','fnm.cfg'); # logging.getLogger().setLevel(logging.DEBUG); msg priority DEBUG,INFO,WARNING,ERROR,CRITICAL
logging.error('err1'); logging.critical('critical err1'); # default log goes to stderr; can direct to file,email,datagrams/netwk,sockets,HTTP svr
%history -t [-o -p -t -n] [-f filename] [range | -g pattern | -l number] / %hist / # cmd history (can be "prev session,line 2-7")
# global_vars _i _ii _iii _ih[n] _ih14,_ih[14]; exec In[2] ~'eval',Out[4],'_' ~'ans'
#----------------------------------------------------------------------------------------------------------------------