from pathlib import Path
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[1]/'bootstrap';count=0
for p in ROOT.rglob('index.html'):
 s=BeautifulSoup(p.read_text(),'html.parser');photos=s.select('.single-realisation-images > .single-realisation-image')
 if not photos:continue
 for i,photo in enumerate(photos):photo['class']=[c for c in photo.get('class',[]) if not c.startswith('realisation-')]+[f'realisation-{i+1}']
 p.write_text(s.prettify(formatter='minimal'));count+=1
print('Normalized full-width covers on',count,'project galleries.')
