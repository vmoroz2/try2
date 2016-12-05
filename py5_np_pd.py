# math,print,plot,numpy,scipy,pandas,
# module ~single file,.m; pkg (numpy etc)~tbx;
# scipy - plenty of toolboxes (optimization,interpolation,linalg,fft,saveMat etc)
# math tbx
import math; math.cos(math.pi/4.0); # underlying C math
import random; random.random(); random.randrange(6); random.choice(['a','b','c']); random.sample(xrange(100),10); # sampling without replacement
# date math,format
from datetime import date; date(2013,12,2); now=date.today(); now.strftime("%m-%d-%y. %d %b %Y is a %A on the %d day of %B.");
bday=date(1971,5,14); (now-bday).days

# array() object ~compact_atomic_list; num_array stored as 2byte unsign_bin (typecode "H") rather than 16bytes per entry for regular lists of Python int objects:
from array import array; a=array('H',[4000,10,700,22222]); sum(a); a[1:3]; array('H',[10,700]);
import collections; deque() # ~list_fast_append_pops_from_left, slower lookups in the middle; useful for queues and breadth-first tree searches:
import struct # heterogeneous bin data

from decimal import * # Decimal datatype - control over precision/rounding (financial,regulatory,legal requirements)
x=Decimal('0.70')*Decimal('1.05'); # 0.7350 "as done by hand"; 5% tax on $.70 diff in dec_float and bin_float
x.quantize(Decimal('0.01')),round(.70*1.05,2) # Decimal('0.74'),0.73 round to nearest cent
(Decimal('1.00') % Decimal('.10')),(1.00 % 0.10) # Decimal('0.00'),0.0999...
(sum([Decimal('0.1')]*10)==Decimal('1.0')),(sum([0.1]*10)==1.0) # True,False; ML has smart rounding
getcontext().prec=36; Decimal(1)/Decimal(7) # Decimal('0.142857142857142857142857142857142857')
#--- plot -------------------------------------------------------------------------------------------------------------
# ipy interactive plot spyder Tools>Preferences>Ipython Console>Graphics>Graphics Backend
# plt.show(), weak win_upd; fig_window_update stopped working (need to resize win to update); plt.show(),spyder_restart did not help;
from numpy import *; from matplotlib.pyplot import *; from scipy.misc import lena;
# import numpy as np, matplotlib.pyplot as plt; from scipy.misc import lena;
# plot,axis,lbl etc
x=arange(0,2,.01); y=sin(2*pi*x); theta=arange(0,2*pi,0.001); r=sin(2*theta);
clf(); subplot(211); plot(x,y,'g+'); subplot(212); semilogy(x,1.5+y,'r',linewidth=1); # semilogy(x,linewidth=1); loglog(x,y); scatter(x,y); polar(theta,r);
axis([0,10,0,5]); text(2,.25,'t2'); xlabel('x1'); ylabel('y1'); title('a$^2$'); grid(1); # xlim,xticks;
show(); ion(); ioff(); # interactive mode (worked before,not now?)
clf(); hist(x**2,50);
# contour,surface etc
o=r_[-2:2:100j]; [x,y]=meshgrid(o,o); z=x*power(math.e,-x**2-y**2);
clf(); contour(x,y,z,cmap=cm.gray,origin='lower',extent=(-3,3,-3,3)); im=imshow(z,interpolation='bilinear',origin='lower',extent=(-3,3,-3,3));
contour(); contourf(); colorbar(); quiver(x,z); # quiver - plot arrows
clf(); imshow(lena(),cmap=cm.gray) # image_proc; cm only pseudo_color?
d=random.rand(2,100)*512; scatter(d[0,:],d[1,:]); # clf(); hist(lena().flatten(),50);
savefig('foo.pdf') # os.system('merge ...');
from matplotlib.backends.backend_pdf import PdfPages; pp=PdfPages('multipage.pdf'); pp.savefig(); pp.close(); # no '-append to fnm_existing'
#--- numpy arrays ------------------------------------------------------------------------------------------------------
###n=2; nt=5; a=[None]*n; b=np.zeros((n,nt)); b[:]=np.nan; c=np.zeros((n,nt),dtype=object); c[:]=None; # init list,vec,array NaN/None

# ML_arrays pass-by-value semantics,slice_copy,lazy copy-on-write;
# np.array pass-by-ref, slice_view(ptr); vec is 1d np.array; "usemask"~array_bool; np.array "go by row",ML "go by col"
# single_ix[3],slice[2:5],ix_arr[1,2,4],mask_arr[T,T,F,T];
# visualization: (d1,d2,d3) d1-outer,(d2,d3); ML (d1,d2),d3 outer;
# vec (array ndim=1) and array often behave differently;
# array_column-major order ML,Fortran,R; array_row-maj C/cpp,py
# array - row,col,page(3rd dim); array fn works on lists, not the opposite
import numpy as np; from numpy import r_,c_,ix_; # np.matrix more ML-like,2D-only; to be avoided;
n=3; nt=4; A=np.array([[1,2,3],[4,5,6]],dtype=np.float); A.astype('complex'); B=np.array([A,A,A,A]); # B is 3D
A.ndim; A.shape; A.dtype; A.nbytes; A.T; A.flatten(); # ndim='# of brackets' in A=array([[[...],]...]);
print A*A,' ',np.dot(A,A); np.tile(A,(n,nt)); # ~A.*A,element-wise; ~ML A*A; ~ML_repmat;
A=np.zeros((n,nt)); A=np.ones((n,nt)); A=np.eye(n); A=np.diag([1,2,3]); np.diag(A); A=np.random.randn(n,nt);
## r_,r_[vec1,vec2],[a;b];c_,[a,b]; ix_,meshgrid;
r_[:9:10j],r_[:10.],arange(10.),np.linspace(0,9,10); r_[1:3:5j]; r_[1:3,.5]; r_[range(1,4),np.r_[5:11]]; C=r_[A,A]; r_[a,b],vstack((a,b)),concatenate((a,b)); # r_->ar, r_[ar1,ar2], ~ML [A;A] (inconsistensy with r_[ar1,ar2])
c_[1:10:10j],r_[1.:11.,'c'],arange(1.,11.)[:,newaxis]; c_[np.eye(2),np.random.randn(2,3)]; c_[a,b],column_stack((a,b)),hstack((a,b)),concatenate((a,b),1); # connect_row,col
ix_(r_[0:9.],r_[0:6.]),np.ogrid[0:9.,0:6.]; # tuple col_x,row_y;
e=np.mgrid[0:9.,0:6.]; # 3D array, d3,d1,d2; x,y=e[:,8,5]; # x 0:9 vert, y 0:6 horiz
e=np.meshgrid(r_[0:9.],r_[0:6.]) # list of 2 2D arrays; x,y=e[0][5,8],e[1][5,8]; # x h,y v
## array indexing; py len(a)~size(a,1); ML length(a)=max(size(a))
a[x]=a[x,]=a[x,:] 'rows of a'; a[x,y]=a[x][y] 'a[x][y] is slower'; A[0,-2] '~ML A(1,end-1)'; b=a[,1] 'row_vec,ndim=1';
a[0:5],a[:5],a[0:5,:]; a[ix_([1,3,4],[0,2])]; a[0:3][:,4:9]=a[0:3,4:9] 'read-only (not sure)';
x=np.arange(10); x[np.array([[1,1],[2,3]])] # vec[ix_array]->array
y=np.arange(35).reshape(5,7); y[np.array([0,2,4]), np.array([0,1,2])] # ar[ix_vec1,ix_vec2] like ML A(x,y);
y[np.array([0,2,4]),1] # if idx_size_mismatch in ix_vec1,ix_vec2 they are "broadcasted"/repeated (ix_vec1 or ix_vex2 is int); Broadcasting" is idx_int->idx_vec (ML trivial)
a=np.random.randn(3,4,2); b=r_[3,7.3]; a*b # a[8 x 1 x 6 x 1],b[7 x 1 x 5]->[8 x 7 x 6 x 5]; breaks on vec1+vec2(ambiguity which first); # yuck,it is true;
x=np.arange(0,50,10); x[np.array([1, 1, 3, 1])] += 1; # note "1" incremented only once
z[1,...,2]=z[1,:,:,2]; # "ellipsis" notation looks unreliable
ix1=(1,slice(3,6)); ix2=(1,ellipsis,2) # =[1,3:6],[1,...,2]; fn(arr,idx) - use tuple for idx
z[list1]=z[list1,:]; z[tuple1]=z[t[0],t[1],...]
## reshape
np.array([2,3,4,5]).reshape(-1,1) # vec_transpose; "-1" means "calculate demaining dim_reshape from oth dim"
y[:,np.newaxis,:].shape # ugly reshape, used for ver2arr
n=5; x=r_[:n]; x[:,np.newaxis],x[np.newaxis,:]; x.reshape(n,1);
a.shape=(a.shape[1],a.shape[0]); # new array created,original deleted; 
b=20<y; y[b]; b[:,5]; y[b[:,5]] ~y[b[:,np.tile(5,(1,y.shape[1]))]].reshape(xx,y.shape[1]) # 
a[:,0,:].shape # it is 2-dim (unlike ML);
a[:] ~ a.copy();
## condition,sort etc
a[1<a]; z=np.nonzero(1<a) '(ar1_x,ar2_y), ~ML [i,j,v]=find(a)'; z=np.where(1<a); np.choose(); a.max(),a.max(0),a.max(1),maximum(a,b),unique(a),np.squeeze(a);
D=B.copy();  # assign matrices by copy; find() may require to convert to vect and back (py pointer helps);
a.ravel().argsort(); a[a[:,0].argsort(),]; a.argsort(axis=1);  # ravel()~flatten,argsort~sort,return idx;

## structured arrays~array_of_tuples;
x=np.zeros((2,),dtype=('i4,f4,a10')); x[:]=[(1,2.,'Hello'),(2,3.,"World")]; x['f1'] # array of tuples,fast_collect
dtype='3int8, float32, (2,3)float64'; # ar_type str/tuple(special extra_info)/list(name,dtype)/dict(special)
# np.ndarray() - access to mem; ndarray can be subclassed

#--- numpy math mix
polyfit(); (a,b)=polyfit(x,y,1);vlinalg.lstsq(x,y); poly(); roots(); fft(a),ifft(a),convolve(x,y); eval('e=4');
linalg.solve(a,b); v=a.compress((a!=0).flat); v=extract(a!=0,a);

## genfromtxt,loadtxt, # .gz,.bz2
from StringIO import StringIO;
# 'skip_header d=0','skip_footer d=0' kills lines; 'comments d=None' kills comments till eol; 'autostrip d=F' kills whsp;
# dlm None(whsp/tab,consolidating consecutive),',','\t'; dlm=5 - fixed-width cols;
# dtype d=float,(int,float,float),"i4,f8,|S3",double,"|S5"~str,dict(name:format),ndtype=[('a',int),('b',float),('c',int)];
# 'usecols=(0,-1)' picks selected cols; names="a,b,c",usecols=("a","c");
# if 'names=T', first commented line checked for names.
d="1,2,3\n4,5,6";
np.genfromtxt(StringIO(d),delimiter=",") 
d=StringIO("1 2 3\n 4 5 6");
np.genfromtxt(data,dtype=(int,float,int))
array([(1,2.0,3),(4,5.0,6)],dtype=[('f0','<i8'),('f1','<f8'),('f2','<i8')])
# dflt name_out are f0,f1 etc
# heterogeneous data produce array of tuples (yuck,set of vectors would be better); there are fns to process;

# format_convert with fn
fn1=lambda x: float(x.strip("%"))/100.
data="1,2.3%,45.\n6,78.9%,0"; names=("i","p","n");
np.genfromtxt(StringIO(data),delimiter=",",names=names,converters={1:fn1})
array([(1.0,0.023,45.0),(6.0,0.78900000000000003,0.0)],dtype=[('i','<f8'),('p','<f8'),('n','<f8')])
ndfromtxt  # usemask=F,   gives ndarray
mafromtxt  # usemask=T,   gives MaskedArray
recfromtxt # usemask=T/F, gives MaskedRecords/numpy.recarray; dtype d=None(auto-determine)
recfromcsv #
#--- scipy ----------------------
sp.info(np.sin),source(),dir() # sp.info spits to stdout/console (not ipy console)
fn1(a,b); fn1_addsubtract=vectorize(fn1) takes vectors;
np.cast['f'](np.pi) # pi to float
x=r_[-2:3]; np.select([1<x,0<=x],[1,x+2]) # extension of where(); FF-0; TF,TT #1, FT #2;
#--- pandas -----------------------------------------------------------------------------------------------------------
# cfg display.width etc - mon setup
# Series (vec)/TimeSeries (vec+t_lbl) 1d, DataFrame 2d(vec_of_vecs)
# df~VM_data + extra layer of lbls/dicts (on id/t/f) for easy matching; cols are ordered; df[i1:i2] *includes* i2; note ptrs;
# idx~row_lbl,rows~time; cols-fields;
# db .xls .csv .h5/HDF5(very fast,~builtin and numpy.array)
# scikits.timeseries migrated to pd
# %reset -f
execfile('D:\soft\py\py9_VM.py'); dir1='D:/soft/py/';
from numpy.random import randn;
#--- pandas -----------------------------------------------------------------------------------------------------------
### WANT:
# df - regress
#--- create s/ts,df; 
# date+time in diff formats; NaN is NaT; np.int64 #nsec since ~19700101 (~epoch time/unix time);
a=pd.Timestamp('20120501',tz='EST'); b=pd.datetime(2012,5,1); # TimeStamp is a single DateTimeIndex;

# DatetimeIndex,PeriodIndex: construct,convert,show,math
nt=500; dt=pd.date_range('20130101',periods=nt,freq='D',tz='EST'); # pd.bdate_range(); # AMWD ann/mo/wk/da HTS hr/min/s; B/' ',M busn_days; tz messes up ts.plot();
dt2=pd.period_range('20130101',periods=nt); # slightly diff,no tz;
dt.to_period().to_timestamp(); pd.to_datetime(['2005/11/23','2010.12.31','20131130','Jul 31,2009']); pd.Index(dt[[7,4,6]]);
dt+45; dt.values; mdt(dt); # add 45 periods; display is ugly;
dt3=pd.period_range('1990Q1','2000Q4',freq='Q-NOV'); (dt3.asfreq('M','e')+1).asfreq('H','s')+9 # math - chg_freq +x
# dt.reindex(); dt.tz_convert(); dt.asi8/24/3600e9 'datenum'; pd.DatetimeIndex(((dt.asi8/60e9).round()*60e9).astype(np.int64)).values # round to min
dt.tz='EST'; dt.tz_convert('UTC');

# TimeSeries: ts can hold any_type; ts is subclass of np.array,same indexing;
nt=500; dt=pd.date_range('20130101',periods=nt,freq='D');
ts=pd.Series(1+randn(nt)*3,index=dt,name='ts1').shift(2); # also tshift; time_shift
ts.index=ts.index+4; ts.name='33'; ts[np.isnan(ts)]=.01; # chg idx,nm
ts.truncate(before='20131031',after='20131231'); ts.resample('5Min',how='sum'); ts.asfreq('H',method='pad') # 'mean' 'pad' 'ohlc'
ts['2013-01-01 08:00':'2013-01-31 08:19']; ts['2013']; ts[1:]+ts[:-1] # auto-nan for missing data;
ts.cumsum().plot(); ts.str.lower(); ts.order()

# DataFrame ~list of cols/ts; integrated_data_alignment - considered powerful;
# df - ~xls/sql tbl,array with lbls; index (row labels) and cols; can be init from dict,ndarray,ts; auto_fill nan;
# structured or record array ~ndaray of tuples
d2=pd.DataFrame({'a':ts[:nt-10],'b':ts.cumsum()}); # two curves with one tail clipped
nt=1e5; d3=pd.DataFrame(randn(nt,1),index=pd.date_range('20130101',periods=nt,freq='T'),columns=['A'])
d4=pd.DataFrame({'A':1.,'B':pd.Timestamp('20130102'),'C':pd.Series(1,index=range(4),dtype='float32'),'D':np.array([3]*4,dtype='int32'),'E':'foo'}) # matched on index,stratched
nt2=6; d=pd.DataFrame(np.random.randn(nt2,4),index=dt[0:nt2],columns=list('ABCD')); d0=d.copy()
len(d); d.index[1:]=d.index[-1:0:-1]; d.columns[1:]=d.columns[-1:0:-1]; d.shape; d.head(); d.tail(3); d.values; d4.dtypes; d.T; d.describe(); # general fns; len(df)=len_dt_dim; dt-lbl,f-lbl; 
d.sort_index(axis=1,ascending=F); d.sort(columns='B'); # sort by row/col lbl/data
d.to_string(); # for display
d2.plot(); plt.legend(loc='best');

# df indexing: .iat/.at(single el),.iloc/.loc(subset),.ix(general); right_endpt excluded with ix,included with ix_lbl; lbl=[0:n] to be avoided?
d[0:3],d['20130102':'20130104'] # rows only,d[1,3] breaks;
d['A'],d.A # keep idx,col_lbl; ~d(:,mm('A',f));
d.iloc[0:2,[0,2]]; d.loc[dt[0:2],['A','C']]; # idx_py_stype (excl right_end)+dim_control; ~df(mm(idx_subset,idx),:)
d.iat[0,3];        d.at[dt[0],'A']=-3 # single_elem,ptr;
# .ix=.loc+.iloc ,mixed lbl/int
x=list('abcdef'); x[8:10]; d[8:10]; # high idx allowed in np,was forbidden(not anymore?) in df;

# multi_idx,convert to cols, pivot table: xls_tbl1,graphically set up summary_tbl2="pivot table" (it pivots/rotates following chg in graph setup)
d5=pd.DataFrame({'A':['one','one','two','three']*3,'B':['a','b','c']*4,'C':['foo','foo','foo','bar','bar','bar']*2,'D':np.random.randn(12),'E':np.random.randn(12)})
tp1=zip(*[['bar','bar','baz','baz','foo','foo','qux','qux'],['one','two','one','two','one','two','one','two']])
ix1=pd.MultiIndex.from_tuples(tp1,names=['first','second']); d5=pd.DataFrame(randn(8,4),index=ix1,columns=['A','B','C','D']); d6=d5[:4]; d7=d5.stack(); d7.unstack(); # multi-idx can be converted to cols
###? result.columns.levels # labels for multi-index; multi-ix order matters
# pd.pivot_table(d5,values='D',rows=['A','B'],cols=['C']) # summary_table - grp by A,B,C

# concat df
d=d0.copy(); pd.concat([d[:2],d[2:5],d[5:]]) # rows
pd.concat([d.ix[:,'A':'B'],d.ix[1:3,'C':'D']],axis=1) # cols; note df_single_col=TimeSeries
# o1=pd.concat([p1,p2,p3],keys=['first','second','third'],join='outer') # generates hierarchial_multi-index (multi-ix order matters); can use multiple_keys,dict etc;
d=pd.DataFrame(randn(10,4),columns=['a','b','c','d'],index=[pd.core.common.rands(5) for _ in xrange(10)]) # rand_strings
pd.concat([d.ix[:7,['a','b']],d.ix[2:-2,['c']],d.ix[-7:,['d']]],axis=1,join_axes=[d.index]) # ix_orig (othw ix_sorted)
pd.concat([d.ix[:7,['a','b']],d.ix[2:-2,['c']],d.ix[-7:,['d']]],join='inner')
# add_row/col,copy,reindex,sql-like merge,fill_nan
ts2=pd.Series([1,3,5,np.nan,6,8],index=dt[:6]); d.append([d.ix[1,],d.ix[0,]]); d.append(ts2.T,ignore_index=True); # d is NOT modified; append rows broken???
d.loc[:,'d']=np.array([5]*len(d)); d['g']=ts2[0:4] # cols; data outside of "master date list" is lost
d5=d.copy(); d6=d4.pop('C'); del d['g']
d.insert(1,'bar',d['b']) # args posn,lbl,data
d6=d.reindex(index=dt[[0,1,4]],columns=list(d.columns)+['E']) # can modify row/col names (can extract data and construct new df);
d.rename(columns={'one' : 'foo','two' : 'bar'},index={'a' : 'apple','b' : 'banana','d' : 'durian'}) # rename
# pd.DataFrame(np.asarray(d),index=new_index,columns=new_cols); # inefficient but works; d.index=xx; d.columns=xx; d.name=xx;
d7=pd.DataFrame({'key':['fo','fo'],'val1':[1,2]}); d8=pd.DataFrame({'key':['fo','fo'],'val2':[4,5]}); pd.merge(d7,d8,on='key') # sql-like merge,very high eff;
d.combine_first(d2) # ~fill_nan pref1,pref2, ~d(isnan(d))=d2(isnan(d));

# process nan
d[0<d]; # NaN's if no data
d[0<d.a]; d[0<d.iloc[:,0]]; # d(d(:,1)<0,:) select rows
d.dropna(how='any'); d.fillna(value=5); pd.isnull(d)
# f=lambda x:x.fillna(x.mean()); grp=xx; d3=grp.transform(f) # fill with grp mean

# stat,grouping
d.mean(1); ts.value_counts(); # mean etc excludes missing data
d.apply(np.cumsum); d.apply(lambda x:x.max()-x.min());

d9=pd.DataFrame({'A':['fo','ba','fo','ba','fo','ba','fo','fo'],'B':['a','a','b','c','b','b','a','c'],'C':randn(8),'D':randn(8)})
d9.groupby(['A','B']).sum()
d.sub(d['a'],axis=0) # subtract col A; also math ops and &|
d9=pd.Series(np.random.randn(100)); factor=pd.qcut(d9,[0,.25,.5,.75,1.]); d9.groupby(factor).mean() # quintile mean
# d.groupby(level=['A','B']); df.groupby(fn1,axis=1).groups
ctry=np.array(['US','UK','GR','JP']); key=ctry[np.random.randint(0,4,1000)]; d2=pd.DataFrame(randn(1e3),index=key);
grp=d2.groupby(key); grp.count(); grp.mean(); grp.agg(lambda x:x.std()); d2[key=='JP'].apply(lambda x:x.describe()) # grp['JP'].apply(lambda x:x.describe())
grp.keys; grp.indices;

# filter_on_group (A(0<A) etc),apply(f)
d=pd.DataFrame({'A':np.arange(8),'B':list('aabbbbcc')})
d.groupby('B').filter(lambda x:2<len(x),dropna=F); # (lambda x:2<x.sum()); drop unwanted data
def f(grp): return pd.DataFrame({'original':grp,'demeaned':grp-grp.mean()})
d=d0.copy(); d['A']=[1,1,2,2,3,3]; d.groupby('A')['C'].apply(f)
def f(x): return pd.Series([x,x**2],index=['x','x^2'])
s=pd.Series(np.random.rand(5)); s.apply(f) # silent dropping irrelevant cols (e.g. std([char,float]))

import pandas.util.testing as tm; tm.N=3
def unpivot(frame):
  N,K=frame.shape
  data={'value' : frame.values.ravel('F'),'variable' : np.asarray(frame.columns).repeat(N),'date' : np.tile(np.asarray(frame.index),K)}
  return pd.DataFrame(data,columns=['date','variable','value'])
d4=unpivot(tm.makeTimeDataFrame())
d4.pivot(index='date',columns='variable',values='value') # pivot~regroup,chg idx
d4['value2']=d4['value']*2 # will get 2nd df

# Panel=3D df; items(list_DataFrames)/major_axis(rows)/minor_axis(cols)
d=pd.Panel(np.random.randn(3,5,4),items=['one','two','three'],major_axis=pd.date_range('1/1/2000',periods=5),minor_axis=['a','b','c','d']); d.to_frame()
# d['df1'],wp.major_xs(xx),wp.minor_xs(xx); wp.reindex(items=['Item1']).squeeze();

#--- test2: mapping id lists (ML,py)
# time series N(1,3) 100 pts; plot it; 2D array 5 of ts; 3D array on it; add labels - column,row etc;
# ml={'AAPL','MSFT','IBM','GOOG','ORCL'}; dbl={'IBM','ORCL'}; n=size(ml,2); nt=10; A=nan(n,nt); m=mm(dbl,ml)
