#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#--- 01 path,cfg
# o=sys.path;
# for i in range(len(o)): o[i]='/'.join(o[i].split('\\')); o[i].replace('C:/Programs/computations/WinPython27/python-2.7.5.amd64','C:/Programs/py')
# o.append('D:/soft/py')
# del o[o.index('D:/soft/py/.proj1')]; # no easy way to save sys.path
# edit('~/.ipython/profile_default/startup/startup.py')
from __future__ import division  # py2.x 1/2=0 (floor); py3.x 1/2=.5 ### does not stick in ipy
from __future__ import print_function # print(a)
import os,sys; print('%s %s' % (sys.executable or sys.platform, sys.version));
v=lambda:None; v.q,v.sy=('/mnt/hgfs/D/py/','lin') if sys.platform.lower()[:3]=='lin' else ('D:/scan0/py/','win'); os.chdir(v.q); print('vm startup')
#--- 01 magic
o1=['ZMQInteractiveShell.autocall=1','ZMQInteractiveShell.automagic=False','ZMQInteractiveShell.debug=True','IPCompleter.greedy=True',
    'ZMQInteractiveShell.ipython_dir="D:/scan0/py/"','ZMQInteractiveShell.pdb=True']; # call dbg, ~dbstop if error
o2=['%load_ext autoreload','%autoreload 2','%autocall 1'];
[get_ipython().magic('%config '+o) for o in o1]; [get_ipython().magic(o) for o in o2];
