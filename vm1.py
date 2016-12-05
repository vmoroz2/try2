#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------------------------------------------------
from vm0 import * # execfile(v.q+'vm0.py');
import glob
import datetime,random,string,subprocess

### LOST: np and pd tricks from parse_xx
### ct() np.concatenate with a bunch of clauses for empty dim
### tic,toc
### mm by tuples
### mm by uk+dt with accuracy
### enhanced saveM
#--- file rename - general
def fnm_mv(fnm,fnm2,do_copy=False): # copy/move file with mkdir and no overwrite
  if os.path.exists(fnm2): print 'fnm_mv fnm2 exists, doing nothing;'; return;
  o=fnm2; q=os.path.split(o); e1=[];
  while len(q[1]) and not os.path.exists(q[0]): e1.append(q[0]); q=os.path.split(q[0])
  [os.mkdir(q) for q in arr(e1)[::-1]];
  if not do_copy: shutil.move(fnm,fnm2);
  else:           shutil.copy2(fnm,fnm2); # shutil.copystat(fnm,fnm2); # sha is still broken, yuck
  #--- rm empty dirs
def rm_empty_dir(dir1):
  def _visit(arg,dir2,nonempty):
    if not nonempty: print 'removing %s' % dir2; os.rmdir(dir2)
  os.path.walk(dir1,_visit,0)
# rm_empty_dir('M:/mov2/')
# o=mdir('M:/'); [rm_empty_dir(q) for q in o[2:,0]];

import hashlib # calculate sha5
def fnm_sha5(f, hasher=None, blocksize=64*1024):
  if hasher is None: hasher=hashlib.sha256();
  if isinstance(f,str): f=open(f,'rb')
  buf = f.read(blocksize)
  while 0 < len(buf): hasher.update(buf); buf=''; # buf = f.read(blocksize)
  return hasher.digest()
