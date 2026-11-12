"""Standard-library-only shared header/footer editor. No build step for page edits.
Export: python3 tools/shared-layout.py export
Apply:  python3 tools/shared-layout.py apply
"""
from pathlib import Path
import re,sys,os
BASE=Path(__file__).resolve().parents[1]; SITE=BASE/'bootstrap'; PARTS=SITE/'maintenance'; PARTS.mkdir(exist_ok=True)
command=sys.argv[1] if len(sys.argv)>1 else ''
def part(text,tag):
 m=re.search(r'<'+tag+r'\b[^>]*>.*?</'+tag+'>',text,re.S)
 if not m:raise ValueError('Missing '+tag)
 return m
if command=='export':
 for lang,page in [('fr','index.html'),('en','en/index.html')]:
  text=(SITE/page).read_text();prefix='../' if lang=='en' else ''
  for tag in ['header','footer']:
   html=part(text,tag)[0]
   def canonical(m):
    value=m[2]
    if value.startswith(('http:','https:','tel:','mailto:','javascript:','#','data:','//')):return m[0]
    value=os.path.normpath(str(Path(page).parent/value))
    return m[1]+'{{root}}'+value+m[3]
   html=re.sub(r'((?:href|src)=")([^"]+)(")',canonical,html)
   (PARTS/f'{lang}-{tag}.partial').write_text(html+'\n')
 print('Exported bilingual headers and footers to bootstrap/maintenance/')
elif command=='apply':
 for page in SITE.rglob('index.html'):
  if any(x in {'.refactor','.git'} for x in page.relative_to(SITE).parts):continue
  rel=page.relative_to(SITE);lang='en' if rel.parts[0]=='en' else 'fr';root='../'*(len(rel.parts)-1);text=page.read_text()
  for tag in ['header','footer']:
   html=(PARTS/f'{lang}-{tag}.partial').read_text().strip().replace('{{root}}',root)
   m=part(text,tag)
   if tag=='header':
    # A shared header must preserve each page's paired English/French destination.
    language_anchors=[a for a in re.findall(r'<a\b[^>]*>.*?</a>',m[0],re.S) if re.search(r'title="(?:EN|FR)"',a)]
    if language_anchors:
     paired=re.search(r'href="([^"]+)"',language_anchors[0])[1]
     old_label=re.search(r'aria-label="([^"]+)"',language_anchors[0])
     def pair(a):
      if not re.search(r'title="(?:EN|FR)"',a[0]):return a[0]
      result=re.sub(r'href="[^"]*"',lambda _:'href="'+paired+'"',a[0])
      if old_label:result=re.sub(r'aria-label="[^"]*"',lambda _:'aria-label="'+old_label[1]+'"',result)
      return result
     html=re.sub(r'<a\b[^>]*>.*?</a>',pair,html,flags=re.S)
    else:
     html=re.sub(r'<li\b[^>]*class="[^"]*\bwpml-ls-item\b[^"]*"[^>]*>.*?</li>','',html,flags=re.S)
   # Retain each page's active navigation item and ancestors.
   active={}
   for li in re.findall(r'<li\b[^>]*>',m[0]):
    attrs=re.search(r'class="([^"]*)"',li)
    if attrs:
     tokens=attrs[1].split();key=next((x for x in tokens if re.fullmatch(r'menu-item-\d+',x)),None)
     if key:active[key]=[x for x in tokens if x.startswith('current-')]
   def retain_active(li):
    attrs=re.search(r'class="([^"]*)"',li[0])
    if not attrs:return li[0]
    tokens=[x for x in attrs[1].split() if not x.startswith('current-')]
    key=next((x for x in tokens if re.fullmatch(r'menu-item-\d+',x)),None)
    tokens+=active.get(key,[])
    return li[0][:attrs.start(1)]+' '.join(tokens)+li[0][attrs.end(1):]
   html=re.sub(r'<li\b[^>]*>',retain_active,html)
   text=text[:m.start()]+html+text[m.end():]
  page.write_text(text)
 print('Applied shared layouts. Page bodies were kept unchanged.')
else:raise SystemExit('Usage: python3 tools/shared-layout.py export|apply')
