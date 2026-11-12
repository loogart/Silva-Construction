from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urlsplit,unquote
import os,json
BASE=Path(__file__).resolve().parents[1];ROOT=BASE/'bootstrap';pages={str(p.relative_to(ROOT)):p for p in ROOT.rglob('index.html')};partners={}
for rel,p in pages.items():
 s=BeautifulSoup(p.read_text(),'html.parser');link=s.select_one('header .wpml-ls-item a')
 if link:
  target=os.path.normpath(str(Path(rel).parent/unquote(urlsplit(link['href']).path)))
  if target in pages and target not in ['index.html','en/index.html']:
   partners.setdefault(target,rel)
changes=[]
for rel,p in pages.items():
 s=BeautifulSoup(p.read_text(),'html.parser')
 if s.select_one('header .wpml-ls-item a'):continue
 en=s.html.get('lang','').startswith('en');peer=partners.get(rel,'index.html' if en else 'en/index.html');code='FR' if en else 'EN';hreflang='fr' if en else 'en'
 href=os.path.relpath(ROOT/peer,p.parent);label=('Passer au français' if en else 'Switch to English') if rel in partners else ('Voir la page d’accueil en français' if en else 'Visit the English homepage')
 for menu in s.select('.header-top-right ul.menu,.header-mobile-top-right ul.menu'):
  li=s.new_tag('li',attrs={'class':'menu-item wpml-ls-item language-control'});a=s.new_tag('a',href=href,title=code,attrs={'aria-label':label,'hreflang':hreflang,'lang':hreflang})
  icon=BeautifulSoup('<svg class="icon language-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c5 5 5 13 0 18-5-5-5-13 0-18Z"/></svg>','html.parser').svg;a.append(icon);span=s.new_tag('span',attrs={'class':'wpml-ls-native','lang':hreflang});span.string=code;a.append(span);li.append(a);menu.append(li)
 p.write_text(s.prettify(formatter='minimal'));changes.append({'page':rel,'target':peer,'paired_translation':rel in partners})
(BASE/'review/language-controls.json').write_text(json.dumps(changes,ensure_ascii=False,indent=2));print('Completed language controls on',len(changes),'pages.')
