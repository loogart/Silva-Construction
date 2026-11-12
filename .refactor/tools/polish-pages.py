"""Apply shared inner-page styling and promote image headlines to accessible text."""
from pathlib import Path
from bs4 import BeautifulSoup
import json,re
BASE=Path(__file__).resolve().parents[1];ROOT=BASE/'bootstrap';promoted=[]
for page in ROOT.rglob('index.html'):
 s=BeautifulSoup(page.read_text(),'html.parser');en=s.html.get('lang','').startswith('en');root='../'*(len(page.relative_to(ROOT).parts)-1)
 for link in s.select('link[rel="stylesheet"]'):
  if 'fonts.googleapis.com' in link.get('href',''):link.decompose()
 if not s.select_one('link[href$="assets/css/fonts.css"]'):
  first=s.head.find('link',rel='stylesheet');new=s.new_tag('link',rel='stylesheet',href=root+'assets/css/fonts.css');first.insert_before(new)
 if not s.select_one('link[href$="assets/css/polish.css"]'):s.head.append(s.new_tag('link',rel='stylesheet',href=root+'assets/css/polish.css'))
 hero=s.select_one('.hero-copy')
 if hero:
  image=hero.select_one('img')
  title=hero.select_one('.hero-title')
  if not title:
   label='Builders of uniques living environments.' if en else 'Bâtisseur de milieux de vie uniques.'
   title=s.new_tag('h1',attrs={'class':'hero-title','aria-label':label})
   markup='Builders of<br/>uniques living<br/>environments<span class="brand-stop">.</span>' if en else 'B<span class="brand-accent" data-letter="â">â</span>tisseur<br/>de milieux<br/>de vie uniques<span class="brand-stop">.</span>'
   title.append(BeautifulSoup(markup,'html.parser'))
   if image:image.find_parent(class_='silva-single-image').replace_with(title)
   else:hero.select_one('.content-wrap').append(title)
  promoted.append({'page':str(page.relative_to(ROOT)),'text':title['aria-label']})
 section=s.select_one('.page-sections')
 if section and 'home' not in s.body.get('class',[]):
  first=section.find('div',recursive=False)
  if first:first['class']=list(dict.fromkeys(first.get('class',[])+['page-intro']))
 for intro in s.select('.archive-realisation-title,.blog-single-top'):
  intro['class']=list(dict.fromkeys(intro.get('class',[])+['page-intro']))
 for a in s.select('.logo-wrapper a,.header-mobile-logo a'):
  a['aria-label']='Silva Construction — Home' if en else 'Silva Construction — Accueil'
 for img in s.select('.carousel-item.active img'):
  img['loading']='eager';img['fetchpriority']='high'
 # Repair invalid nested headings inherited from the export, keeping every label intact.
 for h4 in s.select('.blog-inventaire h4'):
  inner=h4.find('h5')
  if inner:h4.insert_after(inner.extract())
 for iframe in s.select('iframe'):
  iframe['title']='Silva Construction — location map' if en else 'Silva Construction — carte de localisation'
 # Standardized empty model panels retain routes/content but no decorative empty block.
 for panel in s.select('.modeles-content'):
  if not panel.get_text(strip=True) and not panel.select('img,iframe'):panel['hidden']=''
 # Decorative icons cannot replace the actual field names or labels.
 for form in s.select('form[data-contact-form]'):
  form['aria-label']='Information request' if en else 'Demande d’information'
 title=s.select_one('.hero-title')
 if title:
  for node in list(title.find_all(string=True)):
   if node.strip():node.replace_with(node.strip())
   else:node.extract()
 html=s.prettify(formatter='minimal')
 if title:html=re.sub(r'<h1\b[^>]*class="hero-title"[^>]*>.*?</h1>',lambda _:title.decode(formatter='minimal'),html,flags=re.S)
 page.write_text(html)
(BASE/'review/live-text.json').write_text(json.dumps(promoted,ensure_ascii=False,indent=2))
print('Updated 131 bilingual pages; image headlines are now live text.')
