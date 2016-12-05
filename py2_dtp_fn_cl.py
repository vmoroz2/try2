# data types; if,for; fn_def,namespaces,classes
# TO DO
#  pylint.run_pylint(); # want pylint config 
#  save vars to py file numpy,pandas (.mat save is ok);
#  functions args by name or reference? (I assume val for num/str/tuple,reference for list/arr; also lazy_eval is used)
###? save dbg_info into file (several env/stack_frm) - no easy soln;
#--- web resources --------------------------------------------------------------------------------------------------------------------------------------------
#  numpy scipy pandas matplotlib scikit
#  numpy.org,mathesaurus.sourceforge.net/matlab-numpy.html,scipy.org/NumPy_for_Matlab_Users,wiki.scipy.org/Tentative_NumPy_Tutorial
#  docs.scipy.org/doc/scipy/reference/
#pandas.pydata.org/pandas-docs/stable/
#matplotlib.sourceforge.net/gallery.html
#scikit-learn.org/stable/ # machine_learn etc
## good
# docs.python.org/2/library/index.html,docs.python.org/2/reference/index.html - HUGE refs
# wiki.python.org/moin/BeginnersGuide # ref3
#wiki.python.org/moin/BeginnersGuide/Programmers tutorial_list; kitware.com/cvpr2012.html; midas3.kitware.com/midas/community/9 py for ML users;
#stromberg.dnsalias.org/~dstromberg/Intro-to-Python/ interesting; code.activestate.com/recipes/langs/python/ ~ML_fileexchange;
#programmers.stackexchange.com/questions/74832/moving-to-python-scipy-and-numpy-for-scientific-computing ref;
#b stevetjoa.com/305/,phillipmfeldman.org/Python/Advantages_of_Python_Over_Matlab.html; most python modules have a sphinx doc website sphinx.pocoo.org;
#b hetland.org/writing/instant-python.html,rexx.com/~dkuhlman/python_101/python_101.html
#--- py QUIRKS:
# \' and \" are equivalent; 1; - will display 1 (or not?)
# has pointers; 'x is y' helps to see if same undl or not; id(x) returns some mem address
# a<b<c; a=b=c; a,b=1,2; b,a=a,b; # multiple assignment (not a tuple)
# NON-INTUITIVE: funny 'and','or' (can refurn float,string etc; (0 or "str1") -> "str1"); # 3 & 4=0 (bitwise); logical_and(3,4) UGLY; also "&" ~bitwise has high precedence in py
# int/float(deal with it,1./int(x)); np.arange(1:5:.1) # roundoff quirks, may be inconsistent, use np.linspace(ti,tf,n) (I assume ML has some quiet rounding/fix)
# idx starts at 0,intval_right_end excluded a[1:4]=[1,2,3]; pointer quirks(use A.copy()); loops - use iterators
# mutable_fn_default initiated once, then "secretly stored" (no ML equiv; use dflt=None, if A=None: A=[])
# 010=0o10(octal)=8; roundoff 3.0*.3-.9; 01/07/08 'some system tokens'; i=1; ++i; i 'silly example, ++ not defined'
# have pkg plus_inf,minus_inf,plus_zero,minus_zero (unconfirmed?)
# py3 print_fn,unicode_str/fnm,chg_classes(~types),iterators/generators,slots~dict_economy_mem,fn_annotations,properties,descriptors, ... = Ellipsis; a,*b=[1,2,3] "extended sequence unpacking"
# cpp var~"ptr/mem addr",py var ~dict(nm,val); "variable assignment,assign_obj_to_var"->"name binding,bind_obj_to_name"
#--- dictionary -----------------------------------------------------------------------------------------------------------------------------------------------
# progr general
# design patterns: inheritance/oop; composition (pkges of embedded widgets-buttons in a GUI etc); delegation child.method()->parent.method(); factories (fn_factory,class_factory)
# fn_programming avoids fn_state/classes_with_vars/etc, call fn twice - get same result, easy to understand/dbg
# refactoring is to take working code and make it work better (usually faster,sometimes less mem/storage, or more elegantly)
# expression returns value; statement is bigger, it "does stuff" like 'import pkg','open(fnm)','while 1: print(123)','def fn1(A): pass'
# expr becomes statemt if we ignore fn_value and use "fn side effects" like print etc; "expression statemt" ~fn_void/None, print_py3, L.append(xx),L.sort() etc, ~procedure (outside of py)
# compound_statement is one or more clauses, aligned at the same indentation
# sequence is ordered container of items
# tokens - identifiers, keywords (for/if/return etc), operators, delimiters, literals etc
# literal is num/str_value_const; a=1,b='dog' (1,'dogs') are literals
# script(.exe) vs module(lib,.dll); 
# pipe - file-like cmd1 | cmd2;
# hash sign '#'; TAB - "move to the right until cur col is a multiple of 4" (some ppl do tab=2); editors do "tab inserts spaces" etc;
## progr mix 
# jump_table-list/dict of "actions" eg [fn1,fn2,fn3]
# heapify(list1) - almost-sorted; Permutes a list as needed to make it satisfy the heap condition: for any i >=0, alist [ i ]<= alist [2* i +1] and alist [ i ]<= alist [2* i +2]
# embedded_system - smth with CPU for *narrow task* (mp3_player etc), not computer or smartphone
# BSD Berkeley Unix and descendants
# GNU "GNU's Not Unix" unix-like; GnuPublicLicense
# pervasive ~widespread
# socket - tcp?
#--- general py_advice ----------------------------------------------------------------------------------------------------------------------------------------
# avoid uncontrolled var/attr names, exec(),eval(),os.system() etc; use execfile() with {} as "protected environment";
eval(cmd) os.system("rm -rf *") 'BAD, not safe'; exec(),execfile() 'can mess up vars if used in env_curr'; 
        for nm in sys.argv[1:]: exec("%s=1" % nm) # BAD  sys_argparse - can get bad_varnames
d={}; \ for nm in sys.argv[1:]: d[nm]=1           # GOOD sys_argparse
def fn(arg,**kw): \ for k,v in kw.items(): exec("s.%s=v" % k) # BAD  fn_argparse- can get bad attr_names
def fn(arg,**kw): \ for k,v in kw.items(): setattr(s,k,v)     # GOOD fn_argparse
      execfile("fnm.py");     fn()      # BAD  execfile - outside vars can get in, inside vars can get out;
d={}; execfile("fnm.py",d,d); d['fn']() # GOOD execfile - insulate vars both ways;
import os;         def show_dir(fnm): return os.system(       "ls -l %s" % fnm ); # BAD  os.system() not safe: fnm == "/home/schwa ; rm -rf *"
import subprocess; def show_dir(fnm): return subprocess.call(["ls","-l",   fnm]); # GOOD os.system()
# run untrusted code in sep process (distutils.spawn?), with min privileges (use chroot, setuid, and jail), use main process to monitor it and kill if too much mem is used ("denial of service" attacks etc)
# mix
from module import * # BAD import * - very bad inside fn(slows down),just bad outside fn; useful in ipy 'one import * per session', like 'import math'
from os import *     # BAD 'from os import *' - overshadows open() with os.open()
from foo import a \ if x: a=2      # BAD  pkg.var chg (unexpected for others); foo.a!=a, chg pkg.var outside of pkg; do not change external vars (imported from oth file etc),make own copy;
import foo        \ if x: foo.a2=2 # GOOD pkg.var chg - own pkg.var2
a= fn1() \\n  +fn2()   # BAD  code_linebreak, '\' with stray space can make err; safe 
a=(fn1()  \n  +fn2())) # GOOD code_linebreak with paren around
newA=A(); newA=None # To delete A,let if fall out of scope,or explicitly "unbind the object from the name"/remove ptr "newA" with A=None
#--- data types --------------------------------------------------------------------------------------------------------
# _obj_ - internal (methods for class/obj); __obj__ - internal2; ___obj___ - fn_name,___init___.py etc
# None[null]/bool/int(auto-L,LL)/float(double64)/complex; [immutable(cannot mutate) types - diff mem_id when giving new value]; hashable type - int/float/string
# int(),float(); 5/2=2 (int division,fixed with fut_import); '+=','*=' allowed; '~=' -> '!=' ; a**b; int(x)=sign(x)*floor(abs(x))
(a is None) 'not a==None'; isinstance(3,int); 010 '-> octal 0o10=8'; sum/any/max(3) 'breaks'
#--- string -read-only ver of C (cant do a[2]='e'); \' or \"
# '\' starts an escape_seq, so cant have ''' \''' or ' \' or r' \', need silly tricks r'C:\dir1\\'[:-1] or r'C:\dir1' +'\\'; display ' \ ' turns into ' \\ ';  ' \' \n ' ok; recomm use raw_srt for regexpr r'\t abc' etc
s='a'+'- '*2+'b'; 'a- - b'; s.upper(); s.replace('a','o'); a='1;2;3;'; ','.join(a.split(';')); ";".join(["%s=%s" % (k, v) for k, v in params.items()]); unicode(), u'abc','\u0020', 'unicode str'
str(x) '~n2s'; repr(x) '~str2_machine_readable_code/fn_mem_xx'; (' %2d ' %pi) 'old str syntax'; '{}'.format(x) 'new str syntax'; s[0]+'0'+s[2:] # workaround for str_read-only property
print(x) '~str(x) for simple, repr(x) for nested'; 'cmd_line >>>x ~repr(x)'; print x, 'weird appearance,heps avoid \n'; print>>fnm,'str1';
a=sys.stdout; b=open('log.txt','a'); sys.stdout=b; print(s); b.close(); sys.stdout=a; 'redirect stdout to fnm'; sys.stdout.write(s+'\n') 'print_undl'
list('abc')=['a','b','c'] 'auto-breakdown of string2list'; 'a'[0][0][0]=='a', '1 char = str_len_1';
t=(123,('e1',5)); t2=[123,['e2',7]]; n=10; x=range(1,10); s.ljust(n),s.center(),s.rjust; repr(x).ljust(n)[:n]; '{:.3f} {:10} {!s} {!r}'.format(pi,'ABC',t,t2) 'new str syntax'
for a in range(256): print(chr(a),end=''); a2+=chr(a); ord(),chr() 'ascii2int and back, 1-128 ascii, avoid char(0) to keep C happy'
''' helps disable large blocks of code, unless there is another ''' # use "# '''"
a='string1'; while a: [...do smth] # 0<len(a), common pattern
'str 1-4bytes/char unicode etc (ML 1 byte)'; bytearray '8bit ints ~str_mutable ~ML_str', 'bin_data bin_str/img/encr';
# lg_string - avoid +=, use list_pieces (I usually write to file)
a=open('/usr/share/dict/words').readlines(); a=map(str.strip,a); a=[str.lower(w) for w in a if len(w)==3 and w[0].islower() and w.isalpha()]; len(a) # word_game_example: read dict,drop spaces,keep words of length 3
codecs.open(fnm); str.encode(),bytes(S,encoding),bytes.decode(),str(B,encoding) 'str2raw/encoded_bytes and back'
## regexp
import re; patrn='^M?M?M?$'; compiledPatrn=re.compile(patrn); re.search(patrn,'M') '<SRE_Match object at 01090490>' or None; compiledPatrn.search('M') # compile not really needed, it is done automatically
'[a-z0 -9]* $','0+ small lett/num followed by eol'; r'\bf[a-z]*','new_word starts with f'; re.sub(r'(\b[a-z]+) \1',r'\1','cat in the the hat') # 'cat in the hat', drop_repeats
pa="""    # test str for Roman numerals MCMLXXXVIII; this "pattern with comments" cannot be compiled(?)
^                # beginning of string
M{0,4}           # thousands - 0 to 4 M's
(CM|CD|D?C{0,3}) # hundreds - 900 (CM), 400 (CD), 0-300 (0 to 3 C's), or 500-800 (D, followed by 0 to 3 C's)
(XC|XL|L?X{0,3}) # tens - 90 (XC), 40 (XL), 0-30 (0 to 3 X's), or 50-80 (L, followed by 0 to 3 X's)
(IX|IV|V?I{0,3}) # ones - 9 (IX), 4 (IV), 0-3 (0 to 3 I's),
# or 5-8 (V, followed by 0 to 3 I's)
$ # end of string""" ;
re.search(pa,'MCMLXXXVIII',re.VERBOSE) '<_sre.SRE_Match at 0x3e5f290>' or None
pa1="^M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$"; pa2=re.compile(pa1); p2.search('MCMLXXXVIII')
re.match('(.*) down (.*) on (.*)','Bugger all down here on earth!').groups() # ->('Bugger all','here','earth!') # Match line to pattern
## string Templating; 
from string import Template; t=Template('${vilg}folk send $$10 to $cause.'); t.substitute(vilg='Yuk',cause='charity'); # $$ -> $; 'Yukfolk send $10 to charity.'
d=dict(vilg='Yok'); t.safe_substitute(d); # 'Yokfolk send $10 to $cause.'
import time,os.path; fnm0=['img_1074.jpg','img_1076.jpg','img_1077.jpg'] # glorified strr, ~fnm2=['Shonny_',n2s([i,n],1),fnm(end-4:end)];
class BatchRename(Template): delimiter='%' # class(Template),state template_fmt,template_substitute
fmt=raw_input('Enter rename style (%d-date %n-seqnum %f-ext):  ') # fmt='Shonny_%n%f'
t=BatchRename(fmt); date=time.strftime('%Y%m%d');
for i,fnm in enumerate(fnm0): base,ext=os.path.splitext(fnm); fnm2=t.substitute(d=date,n=i,f=ext); print '{0} --> {1}'.format(fnm,fnm2) # img_1074.jpg --> Shonny_0.jpg
#--- list ~1d cell array with limited idx (and poor man's vect/array); usually atomic("not molecular,same atoms")/homogeneous
# py list ~ .pl @array, Java class ArrayList (dynam expansion,can hold arbitrary obj) >>java array; internally implemented as vectors/dynamic_arrays, not as "linked lists"
L=[1,3,(4,7),'hi']; n=10; L=[None]*n; len(L); L[:] 'unnamed list copy'; b=L[:]+c[:]; 3 in L; L.append(1); L.pop(2); L+='abc'; L+=(1,2) 'L=L+xx fails, L+= succeeds'
L2=L; L2[1]=33 'affects L for mutable L list/dict/set etc'; L=[[1]]*4; L[0][0]=2 'BAD need deep_copy', L=[[1] for i in range(4)] 'works'; import copy; L2=copy.deepcopy(L); # shallow_copy=(copy one level of list/dict/set etc), deep_copy=(copy all levels of a nested lists etc)
s=slice(1,None) 'slice_obj',L[s]; L[1:2]; L[::-1],L.reverse() 'reverse list'; L[:0]=[a,b] ~ [a,b]+L; a[[1,3,5]] 'not allowed,use' [a[i] for i in [1,3,5]]; # neg_idx - from end; high_idx a[1:12] can be ignored; a==2 F
L[1:1]=[1,2] 'insert/overwrite,diff from ML - #el chgs!'; del L[2]; L[2]=[] 'puts [] into L[2]'; del L[2:4]; L[2:4]=[]; del L;
a.sort(); np.argsort(a); L.index(4) 'find L==4'
# list sorting - same_type shorter first,int=float,diff_type alphabetical_type (list<num<tuple<str)
# py_weak_vectorize fn(list1)=[fn(o) for o in list1], map(fn,list1)
a=range(10); len(a); a1=filter(fn1,a); a2=map(lambda x: x**2,a); a3=map(fn3,x,y); # a1=a[fn1(a)=T]; a2=fn2(a); a3=fn3(x,y); py_map "mult_apply"~R_tapply~ML_vector_ops, element-wise
a4=reduce(fn4,a,a0); fn4(fn4(a1,a2),a3); # optional x0=fn4(a0,a1); cumsum_fn
a=[x**2 for x in range(10)]; [(x,y) for x in [1,2,3] for y in [3,1,4] if x!=y]; # "list comprehension" (fast list creation)
vec=[-4,-2,0,2,4]; [x for x in vec if 0<=x]; filter(lambda x: 0<=x,vec) # vec(0<vec)
A=[[1,2,3,4],[5,6,7,8],[9,10,11,12]] # matr=list of lists;
j=1; [row[j] for row in A] [[row[j] for row in A] for j in range(len(A[0]))] # gives a column_transp; M_transp; for_j,for_rows (for_i has to be second bc of grouping)
zip([1,2,3],[4,5,6]) 'zip(list1,list2)-> (list of tuples)'; a=[(1,2),(3,4),(5,6)]; zip(*a) 'matr transp'; zip(*zip(*a))~a , zip(*zip(a))~a 'not as good';
#-- tuple[~read-only list,ordered seq,can't be changed; usually heterogeneous from unpacking args etc; ~read-only refs/pointers (good mem efficiency,"do not modify this" lbl)]
a=(); b=(1,); t=1,3,(4,7),'hi'; len(t); t[1:3]; 'hi' in t; t+(5,); t[1]=4; t*3 '3 shallow copies/pointers'
v=([1,2,3],[3,2,1]); v[0]=[1,4,8]; v[0][1]=7; ## can write into list inside a tuple
from collections import namedtuple; Rec=namedtuple('Rec',['name','age','jobs']); bob=Rec('Bob',age=40.5,jobs=['dev','mgr']) # dict/tuple/class
#--- dict(an orderless list of tuples/pairs key:value); called "hash" in perl, internally implemented with hash tables,optimized for fast lookup
# dict: hashing~ fast key lookup; hash_fn ~map(long_value,short_id), used in hash_tbl, helps with fast lookup; crypto_hash_fn text->num; mm() compressed_id ~hash
# py dict ~ .pl %hash,Java class Hashtable,Visual_Basic Scripting.Dictionary,Cpp map; an "associative array"
d={'a':1,'b':2,'c':3}; d=dict(zip(['a','b','c'],[1,2,3])); d=dict([('a',1),('b',2),('c',3)]); d=dict(a=1,b=2,c=3); d={x:x**2 for x in (2,4,6)}; d.copy() 'shallow copy D2[a] is D[a]'
d['a']; x=d.get('a',0); x=d['a'] if 'a' in d else 0; d['d']=4; d.keys(); d.values(); d.items() 'list of tuples'; 'c' in d; del d['b']; dict([(v,k) for (k,v) in d.items()]) # inv_map
sorted(d.keys()); sorted(d,key=d.get) 'sort dict_keys_list by value'; hash() 'hash_fn,unique_num used for fast sort/lookup/mgmt of list/dict/set';
for q,a in d.values(): print 'What is your {0}?  It is {1}.'.format(q,a); 
## set (unordered unique of immutables); frozenset is immutable;
a=set(); b=set(['orange','banana']); 'orange' in a; a=set('abracadabra'); b=set('alacazam'); a; a-b; a&b; a|b; a^b; v=[x for x in a]; sort(v); list(a); set(c)
set(a); a.union(b); a.intersection(b); a.difference(b); a.symmetric_difference(b); contains(a,2) # True for set member 2 in a
## obj_enumerates_list f=['john','pat','gary','michael']; a=enumerate(f); # enumerate struct used in loops (idx would be fine but slower)
a=[10,20,30,40,50]; for i,k in enumerate (a): print i,k # "enumerate" has "iterator" fn
import collections # containers, dbl-ended queue etc
## (old) some other types are module,SList,class_name[reader,writer],[Element,file,_grouper - iterators in a loop]
#--- indices (string,list,tuple)
# idx starts at 0; a[-1] ~a(end); [0:3] drop last idx; [3:1:-1]; t[:3]; t[::-1]; "graceful handling of degenerate idx" a[:-100],a[100:] - nothing; a[-100] error
# v=([],)*3; v[1].append(1); v # *3 creates "shallow copies" (ptr to same undl)
range(x1,x2,x_step) # ~[x1:x_st:x2-x_st] (py excludes x2); dict/dfr can index by id/lbl; dict['key'],dfr['id']
#--- pointers
# every obj has "id" (~mem_addr); immutable(double,str,tuple etc chg_val->chg_id ~"immortlally unchg,no mutations")/mutable (list/dict,same id on chg)
# 'x is y' - to see if pointers "point to same obj/mem"
x=1; y=x; x is y # =1; can have ambiguity with matrix assignments etc
x=1; y=1; x is y # 0 or 1
#--- if,for
# nested/compound_statemt "if","for" etc - one per line; simple_statemt a=fn(b), several on one line ok; indent of commented lines matters in some flavors!
# no "switch" in py, can use dict and d.get(key,dflt);
a=""; b="second"; c=(1 and [a] or [b])[0]; c=a if x else b 'called ternary expr'; c=(x and a) or b; c=[a,b][bool(x)]; 'also' c=a or b or dflt or None;
if a:   cmd1
elif b: cmd2
else:   cmd3

while a: cmd2 # break,continue are traditional
## loop can iterate on str,tuple,list,dict,array; traditional cnt_loop is discouraged,use list(x),enumerate(list(x)),list_comprehensions etc
for x in c: statemt(s) # "for" statemt implicitly calls "iter" to get an iterator. This is exactly equivalent to:
_tmp_iterator=iter(c) 
while True:
  try: x=_tmp_iterator.next()
  except StopIteration: breakstatement(s)
x=(k**2 for k in [0,1,2,3,4] if 0<k); sum(x) # sum with for/if inside (fewer loops)
d={'a':1,'b':2,'c':3}; d2=enumerate(d.keys()); # ~list+idx/iterator; enumerate_generator - generates "iterator" for "for" loops; "yield" - generator_fn for "enumerate" etc;
for i,v in d2: print '{} {} {}'.format(i,v,d[v])
for i in range(10):
  if(15<i): break;
else: print 'inside for_else' # if not_break/not_found (or skewed else from 'if(x): break'
for i in range(len(a)): print i,a[i] # BAD, use enumerate() for dict/tuples
for i in range(len(list1)): fn(list1[i]); # BAD,called beginner's blunder
for x in list1: fn(x);
# "pass" - placeholder do-nothing;
#--- print (a class_method,not a fn; auto n2s,respects \n etc; some odd features)
print '%f %s' % (pi,'pi') # print % is print_old (cl_method?); print '{1}' is print_intm(cl_method); py3 has print_new(fn), print '%' was almost retired;
for x in range(1,11):
  print repr(x).rjust(2),# no \n if ','
  print repr(x*x).rjust(4),'{0:2d} {1:3d} {2:4d} {!s} {!r}'.format(x,x*x,A,B) # s.format(); !s=str(A); !r=repr(B)
# nice print for mdir()
def p(E): ### cant do np.array monkey patch
  for i in range(len(E)): print '{:40s} {:20s} {:.0f} {:9.1f} {:13.4f} '.format(E[i,0][0:40],E[i,1][0:20],E[i,2],E[i,3],E[i,5])
  # w=40; w2=20; A=E.copy();
  # for i in range(len(A)):
  #   if w <len(A[i,0]): A[i,0]=A[i,0][0:w -2]+'~'
  # if w2<len(A[i,1]): A[i,1]=A[i,1][0:w2-2]+'~'
  # print '{:40s} {:20s} {:.0f} {:9.1f} {:13.4f} '.format(*A[i,np.r_[0:4,5]]) # can do A[i,0][0:40] etc
E=mdir(dir1,1); p(E)
print>>sys.stderr, 'str1'
#--- fn -------------------------------------------------------------------------------------------------------------------------------------------------------
# fn_signature=args+dflts; fn arg by reference (pointer-based)
# py fns require full arg_key (R accepted short arg_key); 
# skeleton fnm.py;
"""prints the string "Hello World" and exits.""" # help string
my_text="Hello World" # global var
def fn(): # fn definition
  """Do smth, print result""" # help2
  print(my_text)
if __name__ == "__main__": # if this is run as script (not imported),run this; ignore otherwise; __name__=pkg_name
  fn()

def fn(*args,**kargs): print "positional args:", args,"\nkwd arguments (useful for options like page_setup etc):", kargs # unnamed args precede named args;
def fn1(arg1,arg2=3.14,arg3='str1'): return arg1,arg2,arg3; # args_optional (kwd/named with defaults) follow args_required (unnamed/named with defaults),flexible on args_named order; fn always returns one value (a tuple)
args=[3,6]; range(*args); # '*'=arg_unpacking (list/tuple to args)
zip(*A) # "*" is arg_unpacking (~list2args); zip ~make_tuple (from list etc)
# fn_output - single obj, can be list/tuple/fn/class;
(lambda x: x*2) # ~ "define nameless fn in-place" (fn2(fn) need to pass fn,ML needs sep_file, eval(fn_name)/eval(expr))
## dflt_mutable quirk - obj_fn_def is actually obj_(fn+dflt) saved together; dflt_mutable change affects subsequent calls,dflt_None is safest;
def f(a,L=[]): L.append(a); return L; # BAD default L initiated only once (unless def=None),shared btw subsequent calls; f keeps a "hidden L copy"
print f(1); print f(2); print f(3)
def f(a,L=None): L=[] if (L is None) else L; L.append(a); return L # dflt=None is immutable,not shared
def delete_list(list_): list_[:]=[] # list_=[] would produce loc_var
## global,fn_scope quirk
def fn1(A): global x=10; # global_var
def fn2(A): import __main__; __main__.x=10; # global_var_hack
x=11
def fn1(): print(x);      # ok
def fn2(): print(x); x=22 # error loc/glbl, peek to x_gbl blocked by x_lcl
def fn3(): import __main__; print(__main__.x); __main__.x=12; X=22; print(X) # import mdl_encl
## generator ~"list with lazy eval", "fn with state memory and yield_statemt"
# generator_fn - "yield" (not return) inside a loop,"one outp at a time" (instead of list); fn returns "generator obj", next(obj) generates "StopIteration" error when "list" ends
def fn_gen(n):
  for i in range(n): yield i**2
a=(x for x in range(10)); next(a) # generator_expr-"list with late eval on demand"; gives "generator object" (tuple comprehensions do not exist)
# generator_obj has next()/__next__; other obj need iter(x) to get cmd next(x); iterators/generators have "next(x)" cmd,iter(gen)=gen;
# py3 smtimes output "iterable" in place of "list" (more efficient),use list("iterable") to convert
## factory_fn/closure
# factory_fn: fn1(=fn_factory) returns fn2, fn2 "has memory"/keeps some state_vars from fn1 args/scope;
# factory_fn/closure/nested_fn~(returns fn2 with state_mem), fn2 has "nested/enclosing scope"; fn2~"cheap class" (fn_obj+"packet of memory/state_retention"); factory_fn term is from fn_programming
# used in event_handlers (GUI etc),inferior/cheap low-mem to classes
def fn_maker(n):
  def fn2(A): return A**n # "make" and return fn2,fn2 retains N from enclosing scope;
  return fn2
def fn_maker(n): return lambda A: A**n # lambda functions retain state too
fna=fn_maker(1); fnb=fn_maker(2);
def tester(start): # can have multiple fn2_instances
  def fn_nested(A): print(A,fn_nested.state); fn_nested.state+=1; # fn_nested is in enclosing scope; Change attr,not fn_nested itself
  fn_nested.state=start; return fn_nested # Initial state after func defined
#--- py_general,namespaces,classes ---------------------------------------------------------------------------------------------------------------------------------------
# py is procedural(statemt-based,script/program)+OOP(class-based)+functional(fns)
# program/pkg/module/statement/expressions (expr process objects)
# nsp=(pkg of names and obj)~R_frame/env,mapping(name,obj),"symbol_table"/scope; nested_scope=fn_var_peeking into fn_def (read-only), not into fn_calling!;
# can have global vars (useful for db_conn etc),py3 has nonlocal_vars (encomp_def?)
# nsp contain fns from modules __builtin__,imports like numpy etc;
# nsp_inside_module,nsp_inside_class; 
# var/fn/pkg_lookup LEGB (local,encomp_def,global,builtin) (class_encl does not count? - recheck); nsp_module ~global from inside, mdl.attr from outside;
#--- classes are first-class (unrestricted) objects
# ClassName,fn_name capitalization; EAFP(Easier to ask for forgiveness than permission) py style try...catch; LBYL style C etc (Look before you leap);
# py_oop "key points/usefullness" inheritance/polymorphism/encapsulation
# py (weakly typed classes) if class duck-typing style - avoids is.int() etc,just uses it
# if static-type lang - no classes_by_user;

# all cl_attributes(vars)/methods(fns) are public(not private,can be overriden),fns are virtual (can be overriden/overloaded in inheritance),can't hide data,need to compile cpp
# _fn,_var is "private by convention" (access is allowed but discouraged);
# fn vs method is emphasized; method is obj/class_attr that refs/is bound to a fn; fn_call/method_call
# polymorphism fn looks at arg_type, behaves differently (int/int or float/float,repeat str/list etc)
# "abstract class" - no instance ever, used for inheritance,  - build base_class with some features,then grow on it; intmediate_restrictions
# metaclass "broad class of classes" for logging attribute access,adding thread-safety,tracking object creation,implementing singletons etc; another API to add code (like decorators) (?)

# cl is created at runtime and can be modified further (add attr etc); there is class_def_obj(~fancy fn_obj) and class_inst, cl_def_obj and cl_inst are linked, do not change cl_def_obj!
instance.method(args)=class.method(instance,args);
isinstance(obj,int) 'compares(obj.__class__,int or int_derived)'; issubclass(bool,int),issubclass(unicode,str)
# a=kl(); a.method(arg)=kl.method(a,arg)

## cl_inheritance; cl_tree base/parent/supercl on top,derived/child/subcl_inst on bottom
# cl can inherit from multiple cl_base/parent (incl cl_builtin); "overloaded" methods of derived/child class override methods of base class; can still call method_base kl0.fn (overloaded by method_child kl.fn)
# class inheritance/attr lookupDFLR -depth first,left to right (base1-base1_parents-base2)
## py3 inheritance lookup is new-style MRO (method resolution order), it takes rightmost occurrence of any given cl_parent - like "lookup does not stop, proceeds further till last cl_parent" (tried to consolidate cl+type)
# py3 __slots__ replaces __dict__ to limit new attr and to save mem (for 10^6+ instances)
# py3 classes-slots,properties,descriptors

class kl0(object): # object helps with property
  x=1.1; k=0; A=[]; # k is counter; A will be shared by kl0_inst on A.append('~') etc until kl0_inst.A=['xx']
  def __init__(self,x=1.1): self.x=x; self.B=[]; self.k+=1 # 
  def fn(self,*args): print 'kl0',self.x
  _fn=fn # "kind of" private fn (visible to world/dbg etc, "private by convention"), always points to kl0.fn() (so fn_child would not affect cl_parent) 
  def fn_y(self): return self.x*55;
  y=property(fn_y,doc='~') # read-only attr; does not respect inh/ovr, binds to class where it was defined; 'def fnA(fn): return fn;'
class kl(kl0):
  x=1.2
  def fn(self): print 'kl',self.x
  def fn2(self): kl0.fn(self) # call "unbound fn_parent" (unbound bc cl_parent does not exist). no worry that fn_parent is overriden
  # def fn3(self,*arg): super(kl,self).fn(*arg) # fails py2, confusing py3 but works
class kl2(kl0): pass
class kl3(kl2,kl): pass
def fn4(self): print 'fn4',self.x
kl.fn4=fn4 'same as defined inside kl'; a=kl0(); b=kl(); a.y=2; b.y=2 'both fail'; b.fn(); kl.fn(b); 'both call kl.fn'; b.fn2() 'ok'; c=kl3(); c.fn() 'prints kl0 - old-style depth-first';
kl.x=-1; b.x 'inst.attr changed';

c=kl0(); (a.A is c.A,a.B is c.B); a.A.append('~'); a.A is c.A; a.A=['xx']; a.A is c.A;

## operator_overloading-add generic methods __init,__del(uncommon),__str,__repr; __get/__set; can write own "builtins" like __getitem__ -> A[idx]
# cl_descriptor ~ cl_attr/method that overrides traditional cl.__get__(),__set,__delete; cl.__method__ is a "hook" that intercepts operations like "+" etc;
#    ___fn is looked up on ops like (a+b); mostly unused,possible use - custom_cl; docs.python.org/2/howto/descriptor.html
## "unbound method" 'def method1(args):',no 'self'; py3 just a fn; useful in class def/inheritance, kl.method1(kl_child,args)
## staticmethod() (no instance_obj is needed,works off cl_def_obj), is immutable on inheritance, attached to class for "packaging convenience" etc ~cpp_fn, like kl.attr but no need to init kl;
## classmethod() is "staticmethod mutable on inheritance", fn(cls,args), cl_meth is tied to cl_def_obj, not to cl_inst_obj        ~cpp_static_fn/method (fn called without cl instance)
# "decorator"/@wrapper syntax
class kl():
  def fn(args): xx # no 'self'
  fn=staticmethod(fn)
  @staticmethod # equivalent to 'fn=staticmethod(fn)'
  def fn2(args): xx
  def cl_meth(cls): print 'cl_meth for',cls.__name__ # 'cls' instead of 'self',
  cl_meth=classmethod(cl_meth) #  (no need to init kl)
  @classmethod # equivalent to 'cl_meth=classmethod(cl_meth)'
  def cl_meth(cls): xx
## name_mangling "__x_" (2+ init_,1- fin) -> _kl__x (ignoring __x__),"pseudoprivate"

## can attach attr to almost anything
import numpy as np; np.x=2; print np.x; rm np.x; # works as illustration "x can be var/fn/module"; can attach attr to any class/mdl without changing the class
class Meta(type): # cl_attr can be made read-only (messy using __metaclass__)
  def __new__(mcl,*a,**k): return type.__new__(type('Uniq',(mcl,),{}),*a,**k)
class X: __metaclass__=Meta
class Y: __metaclass__=Meta
type(X).foo=property(lambda *_: 23); type(Y).foo=property(lambda *_: 45); print X.foo,Y.foo; X.foo = 67
##  monkey patch - define fn,"make it a method"/attach it to class; 
def just_foo_cols(self): return [x for x in self.columns if 'foo' in x] # x - col_nm and col ('foo' in x - x is dbl,so x is col_nm) # """Get a list of column names containing the string 'foo' """
pd.DataFrame.just_foo_cols=just_foo_cols # monkey-patch the DataFrame class
df=pd.DataFrame([range(4)],columns= ["A","foo","foozball","bar"]); df.just_foo_cols() # ['foo','foozball']
del pd.DataFrame.just_foo_cols # remove monkey patch (cant monkey patch ndarray)

exec,eval(),execfile() # class_invoking_registered not class_current;
getattr(),setattr(),delattr(), 'also can do direct ref of  kl.__dict__ (~nsp_dict)'
# can emulate class in fn_args (define class2 with methods of class1),eg. c.read(),c.readline()
#-----------------------------------------------------------------------------------------------------------------------