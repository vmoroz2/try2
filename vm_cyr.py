# cyrillic ref
# cyr2lat()
#--- cyrillic ref
# print unicode('АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЫЭЮЯабвгдежзийклмнопрстуфхцчшщыэюя','utf-8') # unicodes in editor
cyr_list   =[''.join([o+q for o in 'CDEF' for q in '0123456789ABCDEF']).decode('hex'),None,None] # \xe1 hex grab # CD - capEF; E0-EF a-p; F0-FF ;
cyr_list[1]=[unicode(o,'cyrillic_asian') for o in cyr_list[0]]             # unicode py console - STANDARD
cyr_list[2]=['%'+o+q for o in 'EFEF' for q in '0123456789ABCDEF'] # %E1 url
# str_unicode.encode('utf-16') - fnm_out
# str_utf16=fd.read(); str_unicode=unicode(str_utf16,'utf-16'); # read fnm_in('utf-16') to unicode
# o='abvgde#zijklmnoprstufxchw]<y`[>q' # 26+#`+<>+[]+<> = 31  - quick visualise, bad caps;  zh # sch ] tv < e [ yu >
def cyr2lat(A):
  if len(A)==0: return '',0;
  o=[str(k) for k in range(10)];
  o1=map(   chr,range(ord('A'      ),ord('z'      )+1)); # lat
  o2=['a','b','v','g','d','e','zh','z','i','j','k','l','m','n','o','p','r','s','t','u','f','h','tz','ch','sh','sch','','y','','e','yu','ya']; o2=[q.upper() for q in o2]+o2; # latinintsa
  o3=map(unichr,range(ord(u'\u0410'),ord(u'\u044f')+1)); # looks good in itunes
  o4=['\xd0'+q for q in map(chr,range(ord('\x90'),ord('\xaf')+1))]+['\xd0'+q for q in map(chr,range(ord('\xb0'),ord('\xbf')+1))]+['\xd1'+q for q in map(chr,range(ord('\x80'),ord('\x8f')+1))] # 16bit in fnm
  o5=map(   chr,range(ord('\xc0'   ),ord('\xff')+1)); # ?
  A0=A; e=[q for q in A]; # sum(-1<mm(e,o+o3)),sum(-1<mm(e,o+o4)),sum(-1<mm(e,o+o5))
  # if -1<sum(-1<mm(e,o+o4)):
  #   for i in rlen(o1): A=A.replace(o4[i],o3[i]);
  if -1<sum(-1<mm(e,o+o5)):
    for i in rlen(o2): A=A.replace(o5[i],o3[i]); # A=A.replace(o5[i],o3[i]);
  A=A.replace('\xb8',u'\u0435') # e,yo
  return A,A!=A0;
  # o=[str(k) for k in range(10)]+['a','b','c','d','e','f']; e1=['\xd0\xb'+q for q in o]+['\xd1\x8'+q for q in o]+['\xd0\x9'+q for q in o]+['\xd0\xa'+q for q in o] # nope
#----------------------------------------------------------------------------------------------------------------------
