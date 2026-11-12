"""Apply the approved local visual exploration without regenerating page content."""
from pathlib import Path
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[1]/'bootstrap'
for page in ROOT.rglob('index.html'):
 s=BeautifulSoup(page.read_text(),'html.parser')
 for link in s.select('header .wpml-ls-item a'):
  if link.select_one('.language-icon'):continue
  svg=BeautifulSoup('<svg class="icon language-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c5 5 5 13 0 18-5-5-5-13 0-18Z"/></svg>','html.parser').svg
  link.insert(0,svg)
  link['aria-label']='Switch to English' if link.get('title')=='EN' else 'Passer au français'
 for container in s.select('.accueil-nouvelles-inner,.blog-listing-inner'):
  if container.find('article',recursive=False):container['class']=list(dict.fromkeys(container.get('class',[])+['news-grid']))
 hero=s.select_one('.batisseur-milieu-row')
 if hero:
  cols=hero.select(':scope > .column')
  if len(cols)==2:
   cols[0]['class']=list(dict.fromkeys(cols[0]['class']+['hero-copy']))
   photo=cols[1].select_one('img')
   if photo and not photo.find_parent(class_='hero-photo'):
    frame=s.new_tag('div',attrs={'class':'hero-photo'})
    photo.wrap(frame)
    photo['alt']='Une famille dans son milieu de vie' if s.html.get('lang','').startswith('fr') else 'A family enjoying their home'
 page.write_text(s.prettify(formatter='minimal'))
print('Refined hero and language controls across the bilingual site.')
