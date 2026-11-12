from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import unquote,urlsplit
from PIL import Image
import re,os,json
BASE=Path(__file__).resolve().parents[1];ROOT=BASE/'bootstrap';files=list(ROOT.rglob('index.html'));covers={};changes=[];dimensions={}
def target(page,url):return (page.parent/unquote(urlsplit(url).path)).resolve()
for page in files:
 s=BeautifulSoup(page.read_text(),'html.parser')
 for card in s.select('.realisation-inner'):
  a=card.select_one('a[href]');image=card.select_one('[style*="background-image"]')
  if a and image:
   m=re.search(r'url\([\"\']?([^\)\"\']+)',image['style'])
   if m:
    dest=target(page,a['href']);photo=target(page,m[1])
    if photo.is_file():covers[str(dest)]=photo
for page in files:
 s=BeautifulSoup(page.read_text(),'html.parser');en=s.html.get('lang','').startswith('en');title=s.select_one('.blog-single-title');name=title.get_text(' ',strip=True) if title else 'Silva Construction'
 existing={str(target(page,i['src'])) for i in s.select('img[src]') if '.html' not in i['src']}
 for img in list(s.select('img[src]')):
  if '.html' not in img['src']:continue
  container=img.find_parent(class_='single-realisation-image') or img.find_parent(class_='carousel-item');cover=covers.get(str(page.resolve()))
  if container and cover and str(cover) not in existing:
   src=os.path.relpath(cover,page.parent);img['src']=src;a=img.find_parent('a')
   if a:a['href']=src
   existing.add(str(cover));changes.append({'page':str(page.relative_to(ROOT)),'action':'restored supplied project cover','source':str(cover.relative_to(ROOT.resolve()))})
  elif container:
   changes.append({'page':str(page.relative_to(ROOT)),'action':'removed invalid empty image slot','original':img['src']});container.decompose()
 for carousel in s.select('.property-carousel'):
  items=carousel.select('.carousel-item')
  if items and not carousel.select_one('.carousel-item.active'):items[0]['class']+=['active']
 for i,img in enumerate(s.select('img[src]')):
  src=target(page,img['src'])
  if src.exists():
   if src not in dimensions:
    try:
     with Image.open(src) as image:dimensions[src]=image.size
    except OSError:dimensions[src]=None
   size=dimensions[src]
   if size:img['width'],img['height']=map(str,size)
  if img.find_parent(class_='single-realisation-image'):
   if not img.get('alt'):img['alt']=f'{name} — photo {i+1}'
   img['loading']='lazy';img['decoding']='async'
 for section in s.select('.modeles-button-plan'):
  a=section.select_one('a')
  if a and '.pdf' not in a.get('href','').lower():
   old=a['href'];a.name='button';a.attrs.pop('href',None);a['type']='button';a['disabled']='';a['aria-disabled']='true'
   note=s.new_tag('p',attrs={'class':'source-plan-note'})
   note.append('Original PDF not supplied. Request the plan: ' if en else 'PDF original non fourni. Demandez le plan : ')
   phone=s.new_tag('a',href='tel:8195257800');phone.string='819 525-7800';note.append(phone);section.append(note)
   changes.append({'page':str(page.relative_to(ROOT)),'action':'flagged missing original PDF; replaced self-link with phone request','original':old})
 html=s.prettify(formatter='minimal');heading=s.select_one('.hero-title')
 if heading:
  for n in list(heading.find_all(string=True)):
   if n.strip():n.replace_with(n.strip())
   else:n.extract()
  html=re.sub(r'<h1\b[^>]*class="hero-title"[^>]*>.*?</h1>',lambda _:heading.decode(formatter='minimal'),html,flags=re.S)
 page.write_text(html)
(BASE/'review/media-repairs.json').write_text(json.dumps(changes,ensure_ascii=False,indent=2))
print('Media and plan checks:',len(changes),'repairs/notices; original media files retained.')
