"""Regenerate Hebrew Abundance and Testimonials pages after editing English copy.
Run: python3 tools/generate-hebrew.py
Missing translations fail instead of silently leaving English content.
"""
from pathlib import Path
from html.parser import HTMLParser
from html import escape,unescape
from urllib.parse import urljoin,urlsplit
import json,re
ROOT=Path(__file__).resolve().parents[1]
TEXT=json.loads((ROOT/'content/hebrew-translations.json').read_text())
ROUTES={'/abundance/':'/abundance/he/','/IEMT/':'/IEMT/he/','/testimonials/':'/testimonials/he/','/':'/abundance/he/'}
class HebrewPage(HTMLParser):
 def __init__(self,page,protected=None):
  super().__init__(convert_charrefs=True);self.page=page;self.out=[];self.skip=False;self.missing=[];self.language=False;self.protected=protected or []
 def handle_decl(self,data):self.out.append('<!'+data+'>')
 def handle_comment(self,data):
  if data.startswith('HE_COPY:'):self.out.append(self.protected[int(data.split(':')[1])])
  else:self.out.append('<!--'+data+'-->')
 def handle_starttag(self,tag,attrs):
  a=dict(attrs);self.language=tag=='a' and a.get('class')=='site-language'
  if tag in ['script','style']:self.skip=True
  if tag=='html':a.update(lang='he',dir='rtl')
  if tag=='header' and a.get('class')=='site-header':a['dir']='rtl'
  if tag=='link' and a.get('rel')=='canonical':a['href']='https://danielleronit.com/'+self.page+'/he/'
  elif tag=='link' and a.get('rel')=='alternate':
   a['href']='https://danielleronit.com/'+self.page+('/' if a.get('hreflang')=='en' else '/he/')
  for k,v in list(a.items()):
   if k in ['href','src'] and v and not v.startswith(('#','https:','http:','mailto:','tel:','data:')):
    resolved=urlsplit(urljoin('https://danielleronit.com/'+self.page+'/',v))
    path=resolved.path
    if k=='href':path=ROUTES.get(path.removesuffix('index.html'),path)
    a[k]=path+('?' + resolved.query if resolved.query else '')+('#'+resolved.fragment if resolved.fragment else '')
   if k in ['alt','aria-label','data-video-title'] or (tag=='meta' and a.get('name')=='description' and k=='content'):
    if v and re.search('[A-Za-z]',v):
     if v not in TEXT:self.missing.append(v)
     a[k]=TEXT.get(v,v)
  if self.language:a.update(href='/'+self.page+'/',lang='en',dir='ltr')
  if a.get('dir')=='ltr' and tag=='footer':a['dir']='rtl'
  # Numeric time labels remain left-to-right inside the Hebrew layout.
  if tag in ['strong','small'] and self.page=='abundance':a['dir']='auto'
  self.out.append('<'+tag+''.join(' '+k+('="'+escape(v,quote=True)+'"' if v is not None else '') for k,v in a.items())+'>')
 def handle_startendtag(self,t,a):
  self.handle_starttag(t,a);self.out[-1]=self.out[-1][:-1]+" />"
 def handle_endtag(self,t):
  if t in ['script','style']:self.skip=False
  if t=='a':self.language=False
  if t=='head':
   self.out.append('<link rel="stylesheet" href="/assets/hebrew.css?v=1">\n<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+Hebrew:wght@300;400;500;700&amp;family=Noto+Serif+Hebrew:wght@300;400;500&amp;display=swap">\n')
  self.out.append('</'+t+'>')
 def handle_data(self,d):
  if self.skip:self.out.append(d);return
  text=d.strip()
  if self.language:self.out.append('English');return
  if re.search('[A-Za-z]',text):
   if text not in TEXT:self.missing.append(text)
   if text in TEXT:d=d.replace(text,TEXT[text])
  self.out.append(escape(d,quote=False))
for page in ['abundance','testimonials']:
 source=(ROOT/page/'index.html').read_text()
 protected=[]
 def translated_emphasis(match):
  body=match['body']
  if not re.search(r'<(?:strong|em)>',body) or re.search(r'<(?!/?(?:strong|em)[ >])',body):return match[0]
  plain=unescape(re.sub(r'</?(?:strong|em)>','',body))
  if plain not in TEXT:return match[0]
  translated=escape(TEXT[plain],quote=False)
  phrases=re.findall(r'<(strong|em)>(.*?)</\1>',body)
  for tag,phrase in phrases:
   phrase=unescape(phrase)
   assert phrase in TEXT, 'Missing emphasized Hebrew phrase: '+phrase
   equivalent=escape(TEXT[phrase],quote=False)
   assert equivalent in translated, 'Emphasis not found in Hebrew sentence: '+phrase
   translated=translated.replace(equivalent,'<'+tag+' dir="auto">'+equivalent+'</'+tag+'>',1)
  protected.append('<'+match['tag']+match['attrs']+'>'+translated+'</'+match['tag']+'>')
  return '<!--HE_COPY:'+str(len(protected)-1)+'-->'
 source=re.sub(r'<(?P<tag>p|li)(?P<attrs>[^>]*)>(?P<body>.*?)</(?P=tag)>',translated_emphasis,source,flags=re.S)
 p=HebrewPage(page,protected);p.feed(source)
 assert not p.missing,'Missing Hebrew translations: '+repr(sorted(set(p.missing)))
 out=ROOT/page/'he/index.html';out.parent.mkdir(exist_ok=True);out.write_text(''.join(p.out))
 print(out.relative_to(ROOT))
