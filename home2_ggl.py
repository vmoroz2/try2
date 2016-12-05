execfile(v.q+'py/home1.py');

import urllib;
def pu_ggl(tkr,is_g=1):
  n=len(tkr); tincr=60; ndays=30;
  o=mdt([mdt(mdt(floor(mdt(0)),1)-ndays),mdt(0)],2); q=range(9*60+30,16*60+1,1); dt=np.vstack((sort(o*len(q)),q*len(o)))*1.; dt[1,:]*=60e3; nt=dt.shape[1]; d=np.zeros((n,nt,6)); exch=['']*n;
  for i in range(n):
    if mod(i,100)==0: print i;
    if is_g:
      url_string="http://www.google.com/finance/getprices?q={0}&i={1}&p={2}d&f=d,o,h,l,c,v".format(tkr[i],tincr,ndays)
      o=urllib.urlopen(url_string).readlines(); exch[i]=o[0]; # print o[0];
      if exch[i][:22]=='<!DOCTYPE html PUBLIC ': print 'py instance blacklisted at i={},breaking'.format(i); break;
      for t in xrange(len(o)-7):
        q=o[7+t].split(',');
        if len(q)!=6: continue ### patch incomplete lines later
        q[0]=float(q[0][1:]) if q[0][0]=='a' else tincr*float(q[0]); d[i,t,:]=[float(e) for e in q];
    else:
      url_string="http://chartapi.finance.yahoo.com/instrument/1.0/{0}/chartdata;type=quote;range={1}d/csv".format(tkr[i],30)
      o=urllib.urlopen(url_string).readlines(); exch[i]=o[3];
      for t in rlen(o):
        q=o[t].split(',') if o[t][:7]!='values:' else [0];
        try:
          if len(q)==6: d[i,t,:]=[float(e) for e in q];
        except: pass
  d=d[:,:,[0,4,2,3,1,5]]
  if is_g: exch=[q.replace('\n','').replace('EXCHANGE%3D','') if q[:22]!='<!DOCTYPE html PUBLIC ' else '_' for q in exch]
  else:    exch=[q.replace('\n','').replace('Exchange-Name:','')                                           for q in exch]
  return d,dt,exch;
  ### also need splits and div

# dir1='/mnt/hgfs/_shd/a/'
def fnm_cyrillic(dir1): # need to run from linux
  o1=['\xd0\xb0','\xd0\xb1','\xd0\xb2','\xd0\xb3','\xd0\xb4','\xd0\xb5','\xd0\xb6','\xd0\xb7','\xd0\xb8','\xd0\xb9','\xd0\xba','\xd0\xbb','\xd0\xbc','\xd0\xbd','\xd0\xbe','\xd0\xbf',  
      '\xd1\x80','\xd1\x81','\xd1\x82','\xd1\x83','\xd1\x84','\xd1\x85','\xd1\x86','\xd1\x87','\xd1\x88','\xd1\x89','\xd1\x8a','\xd1\x8b','\xd1\x8c','\xd1\x8d','\xd1\x8e','\xd1\x8f',
      '\xd0\x90','\xd0\x91','\xd0\x92','\xd0\x93','\xd0\x94','\xd0\x95','\xd0\x96','\xd0\x97','\xd0\x98','\xd0\x99','\xd0\x9a','\xd0\x9b','\xd0\x9c','\xd0\x9d','\xd0\x9e','\xd0\x9f',
      '\xd0\xa0','\xd0\xa1','\xd0\xa2','\xd0\xa3','\xd0\xa4','\xd0\xa5','\xd0\xa6','\xd0\xa7','\xd0\xa8','\xd0\xa9','\xd0\xaa','\xd0\xab','\xd0\xac','\xd0\xad','\xd0\xae','\xd0\xaf',]
  o2=['a','b','v','g','d','e','zh','z','i','j','k','l','m','n','o','p','r','s','t','u','f','h','tz','ch','sh','sch','','y','','e','yu','ya']
  o2=o2+[q.upper() for q in o2];
  e1=glob.glob(dir1+'*.*');
  for j in range(len(e1)):
    o=e1[j];
    for i in range(len(o1)): o=o.replace(o1[i],o2[i])
    print e1[j],o
    os.rename(e1[j],o)

# o2='abcdefghijklmnopqrstuvwxuz'
# import string; [q for q in string.lowercase]

# upper
# ['\xd0\x91',B

# ]]'\xd1', '\x81', '\xd0', '\xb5', '\xd1', '\x80', '\xd0', '\xb8', '\xd0', '\xb8', '.', 'm', 'p', '4']
#o1=['\xd0\xb0','\xd0\xb1',       'c','\xd0\xb4','\xd0\xb5','\xd1\x84','\xd0\xb3','\xd1\x85',
#    '\xd0\xb8','\xd0\xb9','\xd0\xba','\xd0\xbb','\xd0\xbc','\xd0\xbd','\xd0\xbe','\xd0\xbf',
#           'q','\xd1\x80','\xd1\x81','\xd1\x82','\xd1\x83','\xd0\xb2',      'w',       'x',
#    '\xd1\x8b','\xd0\xb7','\xd0\xb6','\xd1\x86','\xd1\x87','\xd1\x88','\xd1\x89','\xd1\x8a','\xd1\x8c','\xd1\x8d','\xd1\x8e','\xd1\x8f','~~~~~~~~~~~~~~~~~','\xd0\x91',
#    '\xd0\x92','\xd0\x93','\xd0\x9a','\xd1\x88~','\xd0\x9b','\xd0\x9c','\xd0\xa1','\xd0\x92']
## e 
#o2=[       'a',       'b',       'c',       'd',       'e',      'f',      'g',         'h',
#           'i',       'j',       'k',       'l',       'm',      'n',      'o',         'p',
#           'q',       'r',       's',       't',       'u',      'v',      'w',         'x',
#           'y',       'z',      'zh',      'tz',      'ch',      'sh',    'sch',         '',       '',        'e',      'yu',       'ya',
#           'A',       'B',       'c',       'd',       'e',      'f',      'g',         'h',
#           'B',       'G',       'K',       'L',       'M',      'S',       'V']

assert 0;

#--- grab ggl intraday ------------------------------------------------------------------------------------------------
o=pd.read_csv('D:/soft/py/Russell_3000_Intraday.txt',header=range(10),skiprows=range(7),delim_whitespace=True, na_values=nan); tkr=arr(o)[:,1]
### can get ind from this table
# d,dt,exch=pu_ggl(tkr[2010:],1)
# fnm2=v.q+'py/ggl_'+str(int(dt[0,-1]))+'_2.mat'; saveM(fnm2,{'d':d,'tkr':tkr,'dt':dt,'exch':exch});
### can make it subprocess?

### yahoo
# d,dt,exch=pu_ggl(tkr,0);
# fnm2=v.q+'py/ggl_'+str(int(dt[0,-1]))+'_yhoo.mat'; saveM(fnm2,{'d':d,'tkr':tkr,'dt':dt,'exch':exch});
### grab name 'Company-Name:Alphabet Inc.' / 'currency:USD'
# Symbol Lookup: http://finance.yahoo.com/q?s=&ql=1

#http://trading.cheno.net/downloading-google-intraday-historical-data-with-python/
#--- hopey - tick is heavy,no bars; ~3w; 1min unavail;
# http://hopey.netfonds.no/posdump.php?date=20120423&paper=AAPL.O&csv_format=txt
# http://hopey.netfonds.no/tradedump.php?date=20131224&paper=AAPL.O&csv_format=txt
# read.csv("http://hopey.netfonds.no/tradedump.php?date=20130405&paper=AAPL.O&csv_format=tx", sep=",", header=1)
#--- stooq 6bd; also 1mo
# http://stooq.com/db/h/
#--- boring
# http://www.dukascopy.com/swiss/english/data_feed/csv_data_export/
# http://www.finam.ru/analysis/profile041CA00007/default.asp 
#----------------------------------------------------------------------------------------------------------------------

#--- consolidate course_subtitle files
dir1='D:/scan0/aut_class/a/'
o1=mdir(dir1); s='';
for o in o1[:,0]: # o1[[-1]+range(len(o1)-1)]:
  fd=open(o,'r'); q=fd.readline();
  while len(q):
    if len(q)<2 or (q[:3]!='00:' and q not in ['\n','WEBVTT\n','[MUSIC]\n']): s+=q;
    q=fd.readline(); # print q
  fd.close(); s+='\n\n'
print s

s=s.replace('\n\n','\n'); e1=s.split('\n'); e2=e1[0];
for k in rlen(e1)[:-1]:
  if 0<len(e1[k]) and 3<len(e1[k+1]): e2+=' '+e1[k+1];
  else: e2+='\n'+e1[k+1];
fd=open(dir1[:-2]+'lesson3.txt','w'); fd.write(e2); fd.close();

# for i in range(len(e1)): o=o.replace(e1[i],e2[i])