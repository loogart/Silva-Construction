from pathlib import Path
from bs4 import BeautifulSoup
import re
ROOT=Path(__file__).resolve().parents[1]/'bootstrap'
for page in ROOT.rglob('index.html'):
 s=BeautifulSoup(page.read_text(),'html.parser');en=s.html.get('lang','').startswith('en');root='../'*(len(page.relative_to(ROOT).parts)-1)
 slot=s.select_one('.footer-col-1 .footer-col-inner')
 if not en and slot and not slot.get_text(strip=True) and not slot.select('img'):
  block=BeautifulSoup('<div class="footer-logo-tel-row footer-contact-refresh"><div class="footer-logo"><a href="'+root+'index.html" aria-label="Silva Construction — Accueil"><img src="'+root+'wp-content/uploads/2020/04/footer-logo.png" alt="Silva Construction" loading="lazy" decoding="async" width="314" height="104"/></a></div><div class="footer-tel"><a href="tel:8195257800"><svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M7 3 3 5c-1 8 8 17 16 16l2-4-5-3-2 2c-3-1-5-3-6-6l2-2-3-5Z"/></svg>819 525-7800</a></div></div>','html.parser').div;slot.append(block)
 for img in s.select('.footer-logo img'):img['width']='272';img['height']='85'
 html=s.prettify(formatter='minimal');h=s.select_one('.hero-title')
 if h:
  for n in list(h.find_all(string=True)):
   if n.strip():n.replace_with(n.strip())
   else:n.extract()
  html=re.sub(r'<h1\b[^>]*class="hero-title"[^>]*>.*?</h1>',lambda _:h.decode(formatter='minimal'),html,flags=re.S)
 page.write_text(html)
