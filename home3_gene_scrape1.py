#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import os,time,glob,csv,subprocess,urllib2 as u; from lxml import html; from HTMLParser import HTMLParser; import numpy as np;

dir0='/mnt/hgfs/D/py/'; dir1=dir0+'genR/'; # os.mkdir(dir1) if not os.path.exists(dir1) else None;
# execfile(dir0+'vm1_cyr.py');
fd=open(dir0+'proxy_servers.csv','rb'); o=csv.reader(fd,delimiter=','); proxy_list=[':'.join(q) for q in o]; fd.close();
url_hdr={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3','Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8','Connection': 'keep-alive'}


### print nm # breaksin subroutine   
nmax=5*1000; nmax=1000;
imax=10*1000; 

def name_ru(N): # def name_ru(name_list,fat_list,exc_list):
  fnm1=dir1+'fat_'+str(1000+N)[1:]+'.csv'; fnm2=dir1+'exc_'+str(1000+N)[1:]+'.csv'
  if os.path.exists(fnm1): print 'fnm1='+fnm1+' exists, doing nothing'; return;
  fd=open(fnm1,'w'); # to reserve a spot
  fnm0=dir0+'name_list.csv'; fnm0=dir0+'exc_list.csv'; fnm0=dir0+'exc_list2.csv';
  fd=open(fnm0,'r'); o=fd.read(); fd.close(); name_list=unicode(o,'utf-16').replace(u'\ufeff','').split('\n')[nmax*N:nmax*(N+1)]; # 410k names
  print nmax,N,len(name_list)
  d2=dict(zip(cyr_list[1],cyr_list[2])+[(' ','%20'),(u'\u0451','%B8')]); # dict to convert e1 to e2;
  fat_list=[]; exc_list=[]; # ppl with popular filename
  for kk in range(len(name_list)):
    nm=name_list[kk]; 
    for o in nm:
      if o not in d2.keys(): d2[o]=o; # print '"'+o+'"';
    try:
      link0=('http://rosgenea.ru/?alf='+str(1+unicode('абвгдежзийклмнопрстуфхцчшщыэюя','utf-8').find(nm[0].lower())),'&serchcatal='+''.join([d2[o] for o in nm])+'&radiobutton=1'); print kk,len(fat_list),len(exc_list) # ,nm;
      for i in range(imax):
        link1=link0[0]+('' if i==0 else '&page='+str(1+i))+link0[1]; o='';
        for _ in range(5):
          try:    url1=u.urlopen(u.Request(link1,headers=url_hdr),timeout=10); o=url1.read(); break;
          except: time.sleep(1);
        if len(o)<1: print 'bad downld, breaking'; assert 0;
        k =[o.find('<table id="catal_cont_1" cellpadding="0" cellspacing="0">')+65,o.rfind('<div id="yandex_ad"></div>')-25]; assert k[0]<k[1]; # assert k[2]<k[3];
        k+=[o.find('(window, document, "yandex_context_callbacks");',k[1]     )+50,o.rfind('<table width="100%">'      )-25];
        g1=unicode(o[k[0]:k[1]]+(o[k[2]:k[3]] if k[2]<k[3] else '')+'\n','cyrillic_asian').replace('<br /><br />\n','\n').replace('<h2>','').replace('<br />','').replace('</h2>',','); # g1 substr_cleaned
        for q in ' \n':
          while not g1.find('\n'+q)<0: g1=g1.replace('\n'+q,'\n')
        g1=g1.replace('\nscript>\n','\n'); g2=g1.split('\n')[:-1];
        if 1+i!=len(o[:k[0]].split('&radiobutton=1')): len(g2)==45; fat_list+=g2; # x=0; np=len(o[x:k[0]].split('&radiobutton=1')) if -1<x else 1; # x=??? x=o.find(xx)
        else: assert (0<len(g2)) and(len(g2)<46); fat_list+=g2; break;
        if imax-2<i: print 'imax<i (very popular last name?)'; assert 0;
    except:
      exc_list+=[nm];
  fd=open(fnm1,'w'); [fd.write((o+'\n').encode('utf-16')) for o in fat_list]; fd.close();
  fd=open(fnm2,'w'); [fd.write((o+'\n').encode('utf-16')) for o in exc_list]; fd.close();

#def read_csv(fnm):
#  E=[];
#  with open(fnm,'r') as fd:
#    while True:
#      o=fd.read(100*1000);
#      if not len(o): break
#      E+=unicode(o,'utf-16').replace(u'\ufeff','').split('\n')
#  return E
    
if 0: #---rosgenea full download .4m names, 2.6m ppl --------------------------------------------------------------------------------------
  execfile('/mnt/hgfs/D/py/gene_scrape2.py'); execfile(dir0+'vm0.py');
  # for n in range(0,6*1000/nmax+1): sh_('execfile("'+dir0+'gene_scrape2.py");name_ru('+str(n)+')',n); time.sleep(.1); # batch run, 200/hr, err_rate~2%
  # import sys; print sys.version; import platform; platform.architecture()
  fat_list=read_csv(dir0+'gene_fat_list.csv');
  o1=[];
  for o in mdir1(dir0+'leftovers*.csv'): fd=open(o); q=fd.read(); fd.close(); o1+=unicode(q,'utf-16').replace(u'\ufeff','').split('\n')
  g1=list(set(o1)-set(fat_list)); len(g1)
  # fd=open(dir0+'leftovers0.csv','w'); [fd.write((o+'\n').encode('utf-16')) for o in g1]; fd.close();

  #--- calc name_list,fat_list,list_exc,name_list_from_fat,
  fd=open(dir0+'name_list.csv','r'); o=fd.read(); fd.close(); name_list=unicode(o,'utf-16').replace(u'\ufeff','').split('\n');
  o1=[];
  # fd=open(dir0+'fat_list.csv','w'); [fd.write((o+'\n').encode('utf-16')) for o in fat_list]; fd.close();
  # o1=unique([o.split()[0] for o in fat_list if len(o)]);  # 410691 nm2
  # g1=list(set(o1)-set(name_list)); g1.sort(); len(g1) # 64 new names/typos
  # g2=list(set(name_list)-set(o1)); g2.sort(); len(g2) # 211 names with spaces etc
  # fat_list=unique(fat_list+list(set(name_list)-set(o1))); # 211 bad names added
if 0: # look up Ryas
  # http://winrus.com/keyboard.htm
  g1=[];
  for o in fat_list:
    k=o.find(unicode('Афанасия Максимовна','utf-8'));
    # k=o.find(unicode('Федоровка','utf-8')); # k=o.find(unicode('Абаз','utf-8'));
    # if -1<k and -1<o.find(unicode('Полтав','utf-8')): g1+=[o]
    if -1<k: g1+=[o]
    # k=o.find(unicode('Федоровка','utf-8')); # k=o.find(unicode('Абаз','utf-8'));
    # if -1<k and -1<o.find(unicode('Полтав','utf-8')): g1+=[o]
    # k=o.find(unicode('Ряс','utf-8'));
    # if -1<k and o[k+3] not in unicode(' .абвгдежзийлмнопртуфхцчшщыэюя' ,'utf-8'): g1+=[o] # break # sk ss s`
  fd=open(dir0+'afan.csv','w'); [fd.write((o+'\n').encode('utf-16')) for o in g1]; fd.close();
    # run2 unsuccessfullt tried c^C, got names for exc_list
    # import locale; locale.setlocale(locale.LC_ALL,('RU','UTF8'))
if 0: #--- rosgenea collect all last names ----------------------------------------------------------------------------
  name_list=[];
  for kk in range(1,35):
    for i in range(1,1000):
      link1='http://rosgenea.ru/?alf='+str(kk)+'&page='+str(i); o=''; print kk,i # printl(q)
      for _ in range(5):
        try:    url1=u.urlopen(u.Request(link1,headers=url_hdr),timeout=3); o=url1.read(); break;
        except: time.sleep(1);
      if -1<o.find('<a class="surname" '):
        name_list+=[q[:q.find('&r=4')] for q in unicode(o,'cyrillic_asian').split('href="?alf='+str(kk)+'&serchcatal=')[1:]];
      else:
        print 'k=-1,letter scan complete?'; # break;
      if len(np.unique(name_list))<len(name_list): print 'name_list non_unique, breaking'; break
    name_list=np.unique([o.replace('=','') for o in name_list]).tolist();
if 0: #--- nomer.org --------------------------------------------------------------------------------------------------
  name_list=[
    '%D0%BC%D0%BE%D1%80%D0%BE%D0%B7',                                     # Moroz        64k    288 #w
    '%D0%B3%D0%BE%D1%80%D0%B1%D0%B5%D0%BD%D0%BA%D0%BE',                   # Gorbenko     13793 920 #17
    '%d0%b3%d1%80%d1%8b%d0%bd%d1%8c',                                     # Gryn`          178 OKc
    '%D0%BB%D0%B5%D1%89%D1%83%D0%BA',                                     # Leschuk       3929 OKc
    '%D0%9A%D0%B0%D0%BC%D0%BB%D0%B8%D1%87%D0%B5%D0%BD%D0%BA%D0%BE',       # Kamlichenko      5 OKc
    '%D0%9A%D0%BE%D0%BC%D0%BB%D0%B8%D1%87%D0%B5%D0%BD%D0%BA%D0%BE',       # Komlichenko    440 OKc
    '%D0%9A%D0%B0%D0%BB%D0%B5%D0%BD%D0%B8%D1%87%D0%B5%D0%BD%D0%BA%D0%BE', # Kalenichenko  2019 OKc
    '%D0%9A%D0%B0%D0%BB%D0%B8%D0%BD%D0%B8%D1%87%D0%B5%D0%BD%D0%BA%D0%BE'] # Kalinichenko 20k
    # Nadijka, Nadejka 0; Abazovka - net poiska po nasel punktu
    # Moroz Vadim 200 chel, Andr 994, vlad 2400; pavel 400, mixail 1200,maks 200,roman 407, anat 1208, evg 401, taisia 71, Lubov 1001, tatyana 2000, dmit 700

  k0=1; link0='http://nomerorg.com/allukraina/lastName_'+name_list[k0]+'_pagenumber_';
  nm=1+int(65645/15);
  k_proxy=0; u.install_opener(u.build_opener(u.ProxyHandler({'http': proxy_list[k_proxy]})))
  for k in range(877,nm):
    link1=link0+str(k)+'.html'; flag1=False; fd=open(dir0+'name'+str(k0)+'_'+str(10000+k)+'_.csv','w'); print k,k_proxy
    while not flag1:
      try:    url1=u.urlopen(u.Request(link1,headers=url_hdr),timeout=3); page1=html.fragments_fromstring(url1.read()); flag1=(1<len(page1));
      except: k_proxy+=1; u.install_opener(u.build_opener(u.ProxyHandler({'http': proxy_list[k_proxy]}))); print k,k_proxy # print HTMLParser().unescape(u.unquote(page1[0]))
    o=html.tostring(page1[3]); o=o[:o.find('</table>')-10].replace('</td><td>',',').replace('</td></tr><tr><td>','\n');
    o=o[o.rfind('/th></tr><tr><td>')+17:]+'\n'; o=HTMLParser().unescape(u.unquote(o));
    if -1<o.find('adsbygoogle'): break
    fd.write(o.encode('utf-16')); time.sleep(.1); fd.close();
  # Forbidden (blocked py queries)/ connection refused (try again)
  #--- consolidate files
  k=1; o1=glob.glob(dir0+'name1/name'+str(k)+'_1*.csv')
  fd=open(dir0+'name'+str(k)+'.csv','wb');
  for q in o1: fd_in=open(q,'rb'); o=fd_in.read(); fd_in.close(); fd.write(o);
  fd.close();


      
      