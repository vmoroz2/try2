# web_help; import,compile; save/load; db;
#--- import,compile ------------------------------------------------------------------------------------------------------------------------------------------
# package=[collection of modules in a dir],__init__.py is required; module=fnm.py; lib1.py on sys.path is loaded;
# file_as_script:     __name__=__main__ (often for lib_test),or for lib_init
# file_as_module/lib: __name__=__lib1__ just define fns; __init__.py is executed on import; it can list files to load: __all__=["echo","surround","reverse"]
# module.namespace; inside mdl - part of nsp, outside mdl - modl.attr
# py has explicit fn import and nsp,multiple fns in a file (similar to R)
import pip,distutils,setuptools; pip.index '~PyPi'; $python setup.py install; $pip install; $virtualenv; # to manage pkg; pip wrapper pip-installer.org
# .pyc(~ML .p): compile .py->.pyc into "bytecode" - speedup on import, not on execution; .pyc is platform-independent,depends on py version;
# .pyc is created automatically,timestamp checked at load/import time (sloppy chk on win); .pyc to .py - several pkg on web;
a=sys.modules; b=[o for o in a.keys() if '.'.join(o.split('.')[:-1]) not in a.keys()]; ','.join(sorted(c)) # list of pkg_installed
## 'import module ~.pl 'require module',java 'import module'; 'from module import *' ~.pl 'use module',java 'import module.*'
import pkg1.pkg2.pkg3 as pk; pk.fn1(); from pkg1 import fn1 as fn1_aux,fn2 as fn2_aux; fn1_aux(); from pkg1 import * # use * with care
import numpy as np # NumPy (arrays,lin alg etc); np.linalg; nt.fftpack; np.optimize; np.io; # sci-kits
import scipy as sp,pandas as pd # SciPy (signal and img proc); sp.io.loadmat/savemat(); pandas-dfrm,~py_R
import matplotlib as mpl,matplotlib.pyplot as plt # 2D/3D plot lib
import pylab; %pylab # most numpy+scipy+matplotlib+int_support
import pylab,scipy; k=set(dir(pylab)).intersection(set(dir(scipy))); conflicts=[f for f in k if getattr(scipy,f) is not getattr(pylab,f)] # conflicts btw similar fns
import scipy.scikits-learn # machine-learn and data mining
import distutils,py2exe # also $pyInstaller; generate distributable pkg; compilation by "python -m compileall"; C/cpp in py easy by design - Cython,SWIG/boost,manually is messy;
## mdl reload
%load_ext / %reload_ext / %unload_ext /%autoreload 2 / reload() / dreload() # %config for cfg; reload seemed not reliable (.pyc,caching?), autoreload,dreload mostly work; execfile(), restart kernel guarantees reload
import mdl1; do_smth; import mdl1 # mdl1.py is *executed* on import1; nothing is done on import2, even if mdl1.py has been edited in outside editor;
reload(mdl1) 'does not reload imports in mdl1'; dreload(mdl1) 'mostly works'; from mdl1 import fn1 'not affected by reload';
reload(mdl1.fn1); fn1=mdl1.fn1 'works'; execfile('mdl1.py') 'always latest version, like cmd_line, avoids import_cache';

import lib1; fn1=lib1.fn1; # better than 'from mdl1 import *';
#################
import module1 # file is *executed* on import
import module1 # nothing is done, even if module1.py has been edited in outside editor
from module1 import fn1 # not affected by reload
reload(module1) # does not reload imports in module1
from module1 import fn1 # not affected by reload - recheck
reload(module1.fn1); fn1=module1.fn1
import etc is a *statement* (others are fn,class,type etc)
execfile('module.py') # always latest version, like cmd_line, avoids import_cache
__pycache__ dir

from .spam import name # relative import: pkg.mod1.mod1a wants to import pkg.mod1.spam
__builtins__
module global_scope inside,attr outside
# import mymod; print mymod.test() # note separate nsp
# from mymod import test; print test()
# a=myclient.__dict__.keys(); [o for o in a if not o.startswith('__')] # list of fns etc in mdl/nsp

#fnm=thismod.py # hacks on import/global_vars
var=90;
def glob2(): import thismod; thismod.var +=1 # Import myself,Change global var (only one module_inst)
def glob3(): import sys; glob=sys.modules['thismod']; glob.var +=1 # Import system table,Get module object (or use __name__)

py pkg
pwd/start_dir,PYTHONPATH,std_dirs,.pth,"The site-packages home of third-party extensions"
sys.path
sys.path.append or sys.path.insert
A compiled extension module,coded in C,C++,or another language,and dynamically linked when imported (eg b.so on Linux,or b.dll or b.pyd)
static linking/lib
frozen executables?
### compile: can call py from C
#include <Python.h>
Py_Initialize(); PyRun_SimpleString("py_cmd")
compile(source,fnm,mode)
# weave.inline() # C compile for matrix ops
###c extensions

import hooks,import from .zip,decrypt
distutils (for some pkg),eggs(chk compatibility)
"statically"-bf code runs
imporf fnm1; fnm1.__file__
import is an assignment (load obj,assign to name); import is always *full*
from modl import*# does not import _*
var_global_inside_fnm/module
reload(module) single module only; "from module1 import xx" not affected
import dir1.dir2.mod
PYTHONPATH/dir1/dir2/mod.py
need __init__.py in dir1,dir2 etc
from . import spam # used inside pkg1,look only inside pkg1
everything is in some module; cmd_prompt is __main__
numpy.__dict__.keys()
namespace-pkg of fns,vars and classes
modname='string'
>>> exec('import '+modname)
modname='string'
>>> string=__import__(modname)
a=Tkinter; [o for o in a.__dict__.keys() if type(getattr(a,o))==type(numpy)]
self test with __name__=='__main__'
import struct # data packing (not ML-like) 
#--- import - reload
try: reload(o)
except: print 'yuck'
dict_visited[modl]=1
import types; from imp import reload                                   # from required in 3.X
def status(module): print('reloading '+module.__name__)
   
def tryreload(module):
  try: reload(module)                                   # 3.3 (only?) fails on some
  except: print('FAILED: %s' % module)
def transitive_reload(module,visited):
  if not module in visited: # Trap cycles,duplicates
    status(module)                                   # Reload this module
    tryreload(module)                                # And visit children
    visited[module]=True
    for attrobj in module.__dict__.values(): # For all attrs
      if type(attrobj)==types.ModuleType: transitive_reload(attrobj,visited) # Recur if module
               
def reload_all(*args):
  visited={}                                         # Main entry point
  for arg in args: # For all passed in
  if type(arg)==types.ModuleType: transitive_reload(arg,visited)
def tester(reloader,modname): # Self-test code
  import importlib,sys                                # Import on tests only
  if len(sys.argv)>1: modname=sys.argv[1]          # command line (or passed)
  module=importlib.import_module(modname); reloader(module) # Import by name string; Test passed-in reloader
from modl import fn does a copy (not a link) like "nested scope fn",no easy reload
import module; reload(module)
from module import function

## mthreading: py has 'global interpreter lock' - one interpreter bytecode at a time,need several inst of py
# lock(T/F), fnm/db/etc locked/released by another proc; semaphores/counting_semaphores (0.bit_length..n, n is set at s creation) are generalized locks, useful to manage a fixed pool of resources (e.g., 4 printers or 20 sockets), Queues are often more robust though
import thread,threading; L=threading.local(); print 'in main thread, setting zop to 42'; L.zop=42;
def targ(): print 'in subthread, setting zop to 23'; L.zop=23; print 'in subthread, zop is now',L.zop
t=threading.Thread(target=targ); t.start(); t.join(); print 'in main thread, zop is now',L.zop;
# emits: in main thread, setting zop to 42; in subthread, setting zop to 23; in subthread, zop is now 23; in main thread, zop is now 42
import mmap,hotshot # file-like mem_data shared btw subproc,profiling for multithr
# multiprocessing.freeze_support(); p=multiprocessing.Process(target=new_proc); p.start(); p.join()

###
# no real multithreading; do multiproc yourself; GPU - single precision
# We won`t cover Python`s multithreading modules in this book (for more on that topic,see follow-up application-level texts such as Programming Python) but the lock and condition synchronization objects they define may also be used with the with statement,because they support the context management protocol, in this case adding both entry and exit actions around a block:
lock=threading.Lock()                        # After: import threading
with lock: print('...access shared resources..') # critical section of code
multiple_thread thread1 runs thread2
#--- file r/w,save/load json,pickle (ascii+tar),np.array.tofile,struct.pack --------------------------------------------
wd='D:/soft/py/'; fd=open(wd+'stocks.csv','rb'); fd.close(); fd.closed; # r/w/r+,r+ is rw; win_ascii breaks files with \n,best to use binary 'rb' etc
fd.tell(); fd.seek(offset,from_what); fd.readline(); fd.read(size); fd.write(str((A,B,C))); # cur_posn; beg,curr,end; readline preserves "\n";
for line in fd: print line, # note "," to avoid \n
return dir+"/"+fnm # SLOPPY
os.path.join(dir,fnm); os.path.basename(),dirname(),splitext() # safer
def get_status(fnm): # SLOPPY,very popular though
  if not os.path.exists(fnm): print "fnm not found"; sys.exit(1);
  return open(fnm).readline() # will break if fnm disappeared btw exists() and open() - unlikely though
def get_status(fnm):
  with open(fnm) as fd: return fd.readline() # "safe" open_fnm, othw fnm is closed when it falls out of scope and gc
%load [-y] fnm.py/7-27/macro/http..fnm.py # [lg_file OK] # %store var > fnm.txt # save,auto_load next session; var_names not saved though
import csv,zlib,bz2 # read/write in common db format; bz2,gzip,tarfile,zipfile,zlib
s='witch which has which witches wrist watch'; len(s); t=zlib.compress(s); len(t); zlib.decompress(t); zlib.crc32(s)
#--- fnm ------------------------------------------------------------------------------------------------------
with open('data') as fd,open('res','w') as fout: # Context manager form
  for line in fd:
    if 'some key' in line: fout.write(line)
auto-close on gc, but safer to close explicitly
import struct # store bin data
import os; F=os.popen('dir'); F.readline() # Read pipe line by line
for o in [line.split()[6] for line in open('input.txt')]: print(o) # print col#7
def awker(fnm,col): return [line.rstrip().split()[col-1] for line in open(fnm)]
'str1' in open(fnm); list(open(fnm))
iter_obj - has fn_next(), easy to use; py3 has more of them (iter_obj in place of some lists etc, more mem efficient but cant have 2 iter on one obj)
iterable_obj; iterator=iter(iterable_obj); iterator_obj has __next__;
with open(fnm) as fd: process(fd)
fd=open(fnm)
py auto-file-close,auto-gc()
#--- text parsing/Sum columns in a text file separated by commas
import sys; fnm=sys.argv[1]; ncols=int(sys.argv[2]); totals=[0]*ncols
for line in open(fnm): cols=line.split(','); nums=[int(x) for x in cols]; totals=[(x+y) for(x,y) in zip(totals,nums)];
print(totals)
#--- data saving - needs to be "serialized/marshalled (low-level io)"; big/little-endian machines have diff bin formats;
d1={'a':[1,2.0,3,4+6j],'b':('string',u'Unicode string'),'c':None}; d2=[1,2,3]; d2.append(d2); # d2 is odd "recursive list"
import marshal # low level io for .pyc
import json; json.dumps(d); json.dump(d,fd); d2=json.load(fd); # json "serializes" lists,dict etc and saves to txt
## pickle/cpickle: cpickle is much faster but has fewer classes; pickle does ascii0(default),bin1 or bin2(best)
# .spydata=tar of several py_pickle_files; pickle breaks on nested fns; "hacked pickle data" can execute bad py code
import pickle,copy_reg,pprint; import cPickle as pickle; 
fnm=wd+'data1.pkl'; fd=open(fnm,'wb'); pickle.dump(d1,fd,2); pickle.dump(d2,fd,2); fd.close(); # save/pickle dictionary/list using protocol 0/-1.
fd=open(fnm,'rb'); d3=pickle.load(fd); pprint.pprint(d3); d4=pickle.load(fd); pprint.pprint(d2); fd.close();
## shelve~several pickles
import shelve; fnm=wd+'shelve2.out'; fd=shelve.open(fnm,'n') # 'n' for new_file
for key in get_ipython().magic('who_ls'): # in dir(): this saves fns etc
  try: fd[key]=globals()[key]; print '-',key; # can try locals(); saves too much
  except TypeError: print('err shelving: {0}'.format(key)) # __builtins__,fd, and imported modules can not be shelved.
fd.close();
import shelve; fnm='D:/soft/py/shelve2.out'; fd=shelve.open(fnm); # restore
for key in fd:
  try: globals()[key]=fd[key];
  except: pass
fd.close();
### "save all" soln - whos2(), pickle.dump/np.save/pd.save on each, zip; then do pickle.load;
# shelve on mutable objects a bit tricky:
import shelve; s=shelve.open('fnm.pks'); s['a']=range(3); print s['a']; s['a'].append('44'); print s['a'] # fails prints [0,1,2]; trying direct mutation... doesn't take, prints: [0,1,2]
x=s['a']; x.append('55'); s['a']=x; print s['akey'] # works - fetch the object,perform mutation,store the object back; prints [0,1,2,'55']
s=shelve.open('fnm.pks',writeback=True) # also works but can be very slow

# use shelve to persist lists of ( filename , line-number ) pairs:
import fileinput, shelve; wordPos={  }
for line in fileinput.input( ):
  pos=fileinput.filename( ), fileinput.filelineno( )
  for o in line.split( ): wordPos.setdefault(o,[  ]).append(pos)
shOut=shelve.open('indexfiles','n')
for o in wordPos: shOut[o]=wordPos[o]
shOut.close( )
# We must use shelve to read back the data stored to the DBM-like file indexfiles, as shown in the following example:
import sys, shelve, linecache shIn=shelve.open('indexfiles')
for o in sys.argv[1:]:
  if not shIn.has_key(o): sys.stderr.write('Word %r not found in index file\n' % o); continue
  places=shIn[o]
  for fnm, lineno in places: print "Word %r occurs in line %s of file %s:" % (o,lineno,fnm); print linecache.getline(fnm, lineno),
# These two examples are the simplest and most direct of the various equivalent pairs of examples shown throughout this section. This reflects the fact that module shelve is higher-level than the modules used in previous examples.

### save(shelve)/db/ftp/web_svr/email
#--- shelve example
rec1={'name': {'first': 'Bob','last': 'Smith'},'job': ['dev','mgr'],'age': 40.5}
rec2={'name': {'first': 'Sue','last': 'Jones'},'job': ['mgr'],'age': 35.0}
import shelve; db=shelve.open('dbfile'); db['bob']=rec1; db['sue']=rec2; db.close();
# print and update shelve created in prior script
import shelve; db=shelve.open('dbfile')
for key in db: print(key,'=>',db[key])
bob=db['bob']; bob['age'] +=1; db['bob']=bob; db.close()

## np.save (bin np vec/arr with lbl),np.tofile,np.memmap; struct.pack()
a=np.random.random(size=(1000,1000,5)); np.save(fnm,a); b=np.load(fnm); # savez(),savetxt()
A.tofile(fnm,'2f',format='%.6f',sep=';'); B=fromfile(fnm); # fd.write(A.tostring()) # define fmt_out,write data
d=np.memmap(fnm,mode='w+',dtype=np.float,offset=x1,shape=(n,nt),order='C'); d[1:10]=np.random.rand(9); d.flush(); del d; # create memmap,put some data into it,flush to disk
import struct; a=[10,50,100,2500,256]; d=struct.pack('i'*len(a),*a); fd=open(fnm,'w'); fd.write(d); fd.close(); # looks weak

### REVISIT THIS
fnm='D:/soft/py/test1.hd5'; d=pd.DataFrame([1,2,3,'str1',mm]); d.to_hdf(fnm,'dh'); d1b=pd.read_hdf(fnm,'d_'); d3=d; 
d4=pd.concat([d3,d3,d3,d3,d3],axis=1); d4.columns=list('ABCDE'); d4.to_hdf(fnm,'d4h'); d4b=pd.read_hdf(fnm,'d4'); sum(abs((d4b-d4).values))
import pandas.io.pytables,h5py
### attempting save_hd5_whos
o=whos2(1); n=len(o); o1=np.c_[o,np.zeros((n,1),dtype=object)];
for i in range(n): o1[i,3]=eval(o1[i,0]);
m=mm(o1[:,1],['module','builtin_function_or_method']); o2=o1[m<0,:]; # fn OK,df some,
d=pd.DataFrame(o2[0:20,:]);
d=pd.DataFrame(o2[np.r_[0:12,20:29,31:len(o2)],:]); d
d.to_hdf(fnm,'d_'); d1b=pd.read_hdf(fnm,'d_');
# this df breaks on "df" 12,14 15 16,17,19
d.to_csv(fnm); d.read_csv(fnm); d.to_hdf(fnm.h5,'d'); read_hdf(fnm.h5,'d');
d.to_excel(fnm,sh_name='sheet1'); read_excel(fnm,'sheet1',index_col=None,na_values=['NA'])
from pandas.core.common import save; from scipy.io.matlab.mio import whosmat # overshadowed fns/vars - recheck
#--- db ---
# MySQL,Oracle etc - relational db mgmt system (RDBMS); everybody uses different SQL dialects,despite SQL standards;
# db pythoncentral.io/introduction-to-sqlite-in-python,stackoverflow.com/questions/14431646/how-to-write-pandas-dataframe-to-sqlite-with-index
import odbc # win - for DBAPI<2.0,unsupported; ODBC - Open DataBase Connectivity, a standard way to connect to many db, including msAccess/msJet.
import mxODBC; msODBC.connect(dsn,user,pass) # lemburg.com/files/Python/mxODBC.html; paramstyle is 'qmark'
import DCOracle2; xx('user/pass@dsn') # zope.org/Members/matt/dco2; paramstyle is 'numeric'; a widespread commercial RDBMS.
import cx_oracle; xx('user/pass@dsn'); xx(dsn=a,usr=b,passwd=c);  # python.net/crew/atuining/cx_Oracle/index.html; paramstyle is 'named'
import mssqldb,pymssql; xx(dsn=a,usr=b,passwd=c); # object-craft.com.au/projects/mssql,pymssql.sourceforge.net; paramstyle is 'qmark'; Microsoft SQL Server
import DB2; xx(dsn,uid,pwd) # sourceforge.net/projects/pydb2; paramstyle is 'format'; DB/2
import MySQLdb; xx(db,host,user,passwd) # sourceforge.net/projects/mysql-python; paramstyle is 'format'; a widespread, open source RDBMS
import psycopg; xx(dsn='host=host dbname=dbn user=usr password=pass'); # initd.org/Software/psycopg; paramstyle is 'pyformat'; PostgreSQL, an excellent(?) open source RDBMS
import sapdbapi; xx(user,password,database,host(opt)) # sapdb.org/sapdbapi.html; paramstyle is 'pyformat'; SAP_DB open-source (formerly Adabas closed source), a powerful RDBMS
import anydbm,dumbdbm,dbm, gdbm, dbhash; # dbm - poor-man's db
from sqlite3.test import dbapi # popular example in books
#--- url,mail etc
The socket Module
The socket module supplies a factory function, also named socket, that you call to generate a socket object s. To perform network operations, call methods on s. In a client program, connect to a server by calling s .connect. In a server program, wait for clients to connect by calling s .bind and s .listen. When a client requests a connection, accept the request by calling s .accept, which returns another socket object s1 connected to the client. Once you have a connected socket object, transmit data by calling its method send and receive data by calling its method recv.
Python supports both current Internet Protocol (IP) standards. IPv4 is more widespread; IPv6 is newer. In IPv4, a network address is a pair ( host , port ). host is a Domain Name System (DNS) hostname such as 'http://www.python.org' or a dotted-quad IP address such as '194.109.137.226'. port is an integer that indicates a socket's port number. In IPv6, a network address is a tuple ( host , port , flowinfo , scopeid ). IPv6 infrastructure is not yet widely deployed; I do not cover IPv6 further in this book. When host is a DNS hostname, Python looks up the name on your platform's DNS infrastructure, using the IP address that corresponds to the name.
Module socket supplies an exception class error. Functions and methods of socket raise error to diagnose socket-specific errors. Module socket also supplies many functions. Many of these functions translate data, such as integers, between your host's native format and network standard format. The higher-level protocol that your program and its counterpart are using on a socket determines what conversions you must perform.

The SocketServer Module
The Python library supplies a framework module, SocketServer, to help you implement simple Internet servers. SocketServer supplies server classes TCPServer, for connection-oriented servers using TCP, and UDPServer, for datagram-oriented servers using UDP, with the same interface.
An instance s of either TCPServer or UDPServer supplies many attributes and methods, and you can subclass either class and override some methods to architect your own specialized server framework. However, I do not cover such advanced and rarely used possibilities in this book.
Classes TCPServer and UDPServer implement synchronous servers that can serve one request at a time. Classes ThreadingTCPServer and ThreadingUDPServer implement threaded servers, spawning a new thread per request. You are responsible for synchronizing the resulting threads as needed. Threading is covered in "Threads in Python" on page 341.

Event-Driven Socket Programs
Socket programs, particularly servers, must often perform many tasks at once. Example 20-1 accepts a connection request, then serves a single client until that client has finished, other requests must wait. This is not acceptable for servers in production use. Clients cannot wait too long: the server must be able to service multiple clients at once.
One way to let your program perform several tasks at once is threading, covered in "Threads in Python" on page 341. Module SocketServer optionally supports threading, as covered in "The SocketServer Module" on page 528. An alternative to threading that can offer better performance and scalability is event-driven (also known as asynchronous) programming.
An event-driven program sits in an event loop and waits for events. In networking, typical events are "a client requests connection," "data arrived on a socket," and "a socket is available for writing." The program responds to each event by executing a small slice of work to service that event, then goes back to the event loop to wait for the next event. The Python library provides minimal support for event-driven network programming with the low-level select module and the higher-level asyncore and asynchat modules. Much richer support for event-driven programming is in the Twisted package (available at http://www.twistedmatrix.com), particularly in subpackage twisted.internet.
### want web_svr
import urllib2 # retrieve data from URLs
for line in urllib2.urlopen('tycho.usno.navy.mil/cgi-bin/timer.pl'):
  if ('EST' in line) or ('EDT' in line): print line # look for Eastern Time
import smtplib; svr=smtplib.SMTP('localhost'); svr.sendmail('from@a.org','to@b.org',"""To: to@a.org \ From: from@b.org \ text1 \ """); svr.quit(); # send email
# remote calls (xml-based,no need to know xml)
import xmlrpclib,SimpleXMLRPCServer # remote procedure calls (no direct handling xml).
import email # build/decode msg+atchmt,including MIME and other RFC 2822-based message documents,intnet encoding and header protocols
import smtplib,poplib # send and receive messages
import xml.dom,xml.sax # parsingxml
#----------------------------------------------------------------------------------------------------------------------
#--- db/Database script to populate and query a MySql db --------------------------------------------------------------
from MySQLdb import Connect
conn=Connect(host='localhost',user='root',passwd='XXXXXXX'); c=conn.cursor();
try: c.execute('drop database testpeopledb')
except: pass                                           # Did not exist
c.execute('create database testpeopledb'); c.execute('use testpeopledb'); c.execute('create table people (name char(30),job char(10),pay int(4))');
c.execute('insert people values (%s,%s,%s)',('Bob','dev',50000)); c.execute('insert people values (%s,%s,%s)',('Sue','dev',60000)); c.execute('insert people values (%s,%s,%s)',('Ann','mgr',40000));
c.execute('select*from people');
for row in c.fetchall(): print(row)
c.execute('select*from people where name=%s',('Bob',)); print(c.description); colnames=[desc[0] for desc in c.description]
while True:
  print('-'*30); o=c.fetchone()
  if not o: break
  for(name,value) in zip(colnames,row): print('%s=> %s' % (name,value))
conn.commit() # Save inserted records
#--- ftp/Fetch and open/play a file by FTP --------------------------------------------------------------------------------------------------------------------
if sys.version[0]=='2': input=raw_input  # 2.X compatibility
import webbrowser,sys; from ftplib import FTP; from getpass import getpass; # Socket-based FTP tools; Hidden password input
sitename=input('Site?'); user=input('User?'); dir2=input('Dir? ') or '.'; fnm2=input('File?'); # FTP site to contact,dir_rmt to fetch from; fnm_rmt to be downloaded
userinfo=() if not user else (user,getpass('Pswd?')); print('Connecting...')
c=FTP(sitename); c.login(*userinfo); c.cwd(dir2); # c.set_pasv(False)# Connect to FTP site; Default is anonymous login; Xfer 1k at a time to fnm; Force active FTP svr requires
fnm=open(fnm2,'wb'); c.retrbinary('RETR '+fnm2,fnm.write,1024); c.quit(); fnm.close(); print('Downloaded,opening...'); webbrowser.open(fnm2) # Local file to store download
#--- xml example
# <books>
#     <date>1995~2013</date>
#     <title>Learning Python</title>
#     <title>Programming Python</title>
#     <title>Python Pocket Reference</title>
#     <publisher>O'Reilly Media</publisher>
# </books>
import re; text=open('mybooks.xml').read(); found=re.findall('<title>(.*)</title>',text);
for title in found: print(title)
#--- CGI server-side script to interact with a web browser ----------------------------------------------------------------------------------------------------
#!/usr/bin/python
import cgi; form=cgi.FieldStorage()  # Parse form data
print("Content-type: text/html\n","<HTML>","<title>Reply Page</title>","<BODY>") # hdr plus blank line, HTML reply page
if not 'user' in form: print("<h1>Who are you?</h1>")
else: print("<h1>Hello <i>%s</i>!</h1>" % cgi.escape(form['user'].value))
print("</BODY></HTML>")
#--- email inbox email inbox scan/print_selected/delete -------------------------------------------------------------------------------------------------------
"""scan pop email box,fetching just headers,allowing deletions without downloading the complete message"""
import poplib,getpass,sys; c=['pop.server.net','user',getpass.getpass('pass for msvr')]; print('Connecting...')
svr=poplib.POP3(c[0]); svr.user(c[1]); svr.pass_(c[2])
try: # nm=msgCount,i+1=msgnum
  print(svr.getwelcome()); nm,mboxSize=svr.stat(); print(nm,' msg,size_tot=',mboxSize); msginfo=svr.list(); print(msginfo)
  for i in range(nm):
    msgsize=msginfo[1][i].split()[1]; resp,hdrlines,octets=svr.top(i+1,0); print('-'*80); print('[%d: octets=%d,size=%s]' % (i+1,octets,msgsize));         # Get hdrs only
    for line in hdrlines: print(line)
    if input('Print?').upper()=='Y':
      for line in svr.retr(i+1)[1]: print(line)    # Get whole msg
    if input('Delete?').upper()=='Y': print('deleting'); server.dele(i+1) # Delete on srvr
    else: print('skipping')
finally: svr.quit() # Make sure we unlock mbox
input('Bye.') # Keep window up on Windows
#-------------------------------------------------------------------------------------------------------------------------------------------------------------