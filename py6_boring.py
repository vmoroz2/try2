# exceptions,multithread,list_queue_tools
#--- documentation (first nonblank line determines indent): ---------------------
# """Do ABC,ignore xx. [fn purpose] / [blank] / long story,examplpes
# tab=spaces,indent=4,width=79,avoid non-ascii;
#--- traceback(~dbg),raising/handling err,exceptions
import sys
try: f=open(fnm); s=f.readline(); i=int(s.strip());
except IOError as er: print 'error fnm {1} {2}'.format(er.errno,er.strerror)
except ValueError:    print 'ValueError ',ValueError
except:               print 'error unexpected,re-raising to handle elsewhere',sys.exc_info()[0]; raise; # re-raise err to handle elsewhere;
finally:              print 'cleaning up'; # f.close(),disconnect etc; this is executed after any breaks (in try or except);

raise NameError('text1'); # ZeroDivisionError etc; can define user_text for error
#Traceback (most recent call last):
#  File "<stdin>",line 1,in ? # this means cmd_line
  
try: raise Exception('text1','text2') # Exception can have user_text (2_str_tuple?);
except Exception as ex: print type(ex),'\n',ex.args,'\n',ex  # the exception instance,arguments stored in .args,__str__ allows args to printed directly
x,y=ex.args; print 'x =',x,'\ny =',y;

class MyError(Exception): # define own error
  def __init__(self,value): self.value=value
  def __str__(self): return repr(self.value)

try: raise MyError(2*2);
except MyError as e: print 'My exception occurred,value:',e.value
finally: print 'Goodbye,world!'

with open(fnm) as f: # auto-fclose() if err
  for line in f: print line,

# raise Class,instance; raise instance # = raise instance.__class__,instance # looks through inheritance for handling iterators,base_classes with iterators
try: smth(); foo=opne("file") # misspelled "open"
except: sys.exit("could not open file!") # BAD err_msg misleading

try: foo=opne("file")
except IOError: sys.exit("could not open file") # good err_msg 
#--- scanning a module and validating tests in docstrings --------------------
def average(a): 
 """Computes the arithmetic mean of a list of numbers. \ \ print average([20,30,70]) \ 40.0 \ """
 return sum(a,0.0)/len(a)
import doctest; doctest.testmod(); # automatically validate the embedded tests

import unittest # more comprehensive tests to be maintained in a separate file:
class TestStatisticalFunctions(unittest.TestCase):
 def test_average(self):
   self.assertEqual(average([20,30,70]),40.0)
   self.assertEqual(round(average([1,5,7]),1),4.3)
   with self.assertRaises(ZeroDivisionError): average([])
   with self.assertRaises(TypeError): average(20,30,70)
unittest.main() # cmd_line call invokes all tests
#--- Multi-threading ---
Threading is a technique for decoupling tasks which are not sequentially dependent. Threads can be used to improve the 
responsiveness of applications that accept user input while other tasks run in the background. A related use case is
running I/O in parallel with computations in another thread.

The following code shows how the high level threading module can run tasks in background while the main program continues to run:

import threading,zipfile
class AsyncZip(threading.Thread):
 def __init__(self,fnm,fnm2): threading.Thread.__init__(self); self.fnm=fnm; self.fnm2=fnm2;
 def run(self): f=zipfile.ZipFile(self.fnm2,'w',zipfile.ZIP_DEFLATED); f.write(self.fnm); f.close(); print 'done backg zip of: ',self.fnm;
bgr=AsyncZip('fnm.txt','fnm.zip'); bgr.start(); print 'The main program continues to run in foreground.'
bgr.join(); print 'Main program waited until bgr was done.'; # Wait for the background task to finish
# main difficulty for multithr is shared resources/data. Threading module provides synch primitives like locks,events,cond_vars,and semaphores.

import Queue # to manage resource access in a single thread; other threads feed requests. Queue.Queue objects provide inter-thread communication/coordination
# "global interpreter lock" - block data for parallel threads; impedes parallel_proc;
#--- mix_boring
## boring file_bin exercise
import struct # pack() and unpack() functions for working with variable length binary record formats.
# low-level .zip header analysis without using the zipfile module.
# Pack codes "H"/"I" (two/four byte unsigned num),The "<" indicates that they are standard size and in little-endian byte order:
d=open('myfile.zip','rb').read(); k=0;
for i in range(3):                      # show the first 3 file headers
  k+=14; fields=struct.unpack('<IIIHH',d[k:k+16]); crc32,comp_sz,uncomp_sz,fnmsz,extra_sz=fields;
  k+=16; fnm=d[k:k+fnmsz]; k+=fnmsz; extra=d[k:k+extra_sz]; print fnm,hex(crc32),comp_sz,uncomp_sz; k+=extra_sz+comp_sz # skip to the next header

## example of "weakref" - gc,mem efficiency
import weakref,gc
class A:
  def __init__(self,value): self.value=value
  def __repr__(self): return str(self.value)
a=A(10); d=weakref.WeakValueDictionary(); # create a "reference" in numspace
d['primary']=a; del a; gc.collect(); # make a ptr,no "reference"; remove the one reference; run garbage collection right away
d['primary']                         # err- entry was automatically removed

## list tools - deque,bisect (sorted lists),heapq(reg lists)
from collections import deque
d=deque(["task1","task2","task3"]); d.append("task4");
print "Handling",d.popleft() # Handling task1
unsearched=deque([starting_node])
def breadth_first_search(unsearched):
  node=unsearched.popleft()
  for m in gen_moves(node):
    if is_goal(m): return m
    unsearched.append(m)
# In addition to alternative list implementations,the library also offers other tools such as the bisect module with functions for manipulating sorted lists:
import bisect; scores=[(100,'perl'),(200,'tcl'),(400,'lua'),(500,'python')]; bisect.insort(scores,(300,'ruby')); scores
# The heapq module provides functions for implementing heaps based on regular lists. The lowest valued entry is always kept at position zero. This is useful for applications which repeatedly access the smallest element but do not want to run a full list sort:
from heapq import heapify,heappop,heappush
data=[1,3,5,7,9,2,4,6,8,0]; heapify(data); heappush(data,-5); [heappop(data) for i in range(3)] # rearrange the list into heap order; add a new entry; fetch the three smallest entries
a=([[1 ,2 ,3]]*3); a[0][0]=2; # list shallow copy - how to avoid?
#--------------------------------
