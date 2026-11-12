from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urlsplit,unquote
import json,re,unicodedata,os,hashlib
BASE=Path(__file__).resolve().parents[1]
def audit(folder):
 root=BASE/folder; files={unicodedata.normalize('NFC',str(p.relative_to(root))) for p in root.rglob('*') if p.is_file() and not any(x in {'.refactor','.git'} for x in p.relative_to(root).parts)}; missing=[]; pages=[p for p in root.rglob('*.html') if not any(x in {'.refactor','.git'} for x in p.relative_to(root).parts)]; doc={}
 for p in pages:
  rel=p.relative_to(root);s=BeautifulSoup(p.read_text(),'html.parser');doc[str(rel)]=s
  for tag,attr in [('a','href'),('img','src'),('link','href'),('script','src')]:
   for e in s.find_all(tag):
    val=e.get(attr,'');url=urlsplit(val)
    if not val or url.scheme or url.netloc or val.startswith('#'):continue
    target=os.path.normpath(str(rel.parent/unquote(url.path)));target=unicodedata.normalize('NFC',target)
    if target not in files and target+'/index.html' not in files:missing.append({'page':str(rel),'attribute':attr,'url':val})
 return pages,doc,missing
op,original,om=audit('original');np,new,nm=audit('bootstrap')
def content(s):
 s=BeautifulSoup(str(s),'html.parser')
 for x in s.select('script,style,noscript,.contact-note,.source-plan-note,.footer-contact-refresh,[data-source-empty-title],.hero-title,header .wpml-ls-item,svg'):x.decompose()
 return re.sub(r'\s+','',s.body.get_text()).strip()
content_diffs=[p for p,s in original.items() if content(s)!=content(new[p])]
assets=[]
for p in (BASE/'original').rglob('*'):
 if p.is_file() and p.suffix.lower() in ['.jpg','.jpeg','.png','.webp','.pdf']:
  q=BASE/'bootstrap'/p.relative_to(BASE/'original')
  if not q.exists() or hashlib.sha256(p.read_bytes()).digest()!=hashlib.sha256(q.read_bytes()).digest():assets.append(str(p))
report={'original_pages':len(op),'refactored_pages':len(np),'fr_pages':sum(s.html.get('lang','').startswith('fr') for s in new.values()),'en_pages':sum(s.html.get('lang','').startswith('en') for s in new.values()),'visible_content_differences':content_diffs,'changed_original_media_files':assets,'original_missing_references':om,'refactor_missing_references':nm,'forms':sum(len(s.select('form')) for s in new.values()),'lightbox_links':sum(len(s.select('[data-lightbox]')) for s in new.values()),'promoted_image_headlines':json.loads((BASE/'review/live-text.json').read_text())}
(BASE/'review/audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps({k:v if not isinstance(v,list) else len(v) for k,v in report.items()},indent=2))
