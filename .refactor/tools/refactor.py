from pathlib import Path
from bs4 import BeautifulSoup, Comment
import re, os, json, tinycss2, unicodedata
from urllib.parse import urlsplit, unquote
from PIL import Image
BASE=Path(__file__).resolve().parents[1]; SRC=BASE/'original'; OUT=BASE/'bootstrap'
(OUT/'assets/css').mkdir(parents=True,exist_ok=True); (OUT/'assets/js').mkdir(exist_ok=True)
pages=sorted(SRC.rglob('*.html')); soups={p.relative_to(SRC):BeautifulSoup(p.read_text(),'html.parser') for p in pages}
shortlinks={}
for r,d in soups.items():
 for c in d.body.get('class',[]):
  if c.startswith(('page-id-','postid-')): shortlinks[c.split('-')[-1]]=r
classes=set(c for s in soups.values() for e in s.find_all(True) for c in e.get('class',[]))
mapping={'vc_col-md-push-6':'desktop-shift-right','vc_col-md-pull-6':'desktop-shift-left','vc_row':'silva-row','wpb_row':'section-row','vc_row-fluid':'section-fluid','wpb_column':'silva-column','vc_column_container':'column','vc_column-inner':'column-inner','wpb_wrapper':'content-wrap','wpb_content_element':'content-block','wpb_text_column':'text-block','wpb-content-wrapper':'page-sections','vc_inner':'inner-row','vc_row-flex':'row-flex','vc_row-o-content-middle':'align-items-center','vc_row-o-equal-height':'equal-height','vc_row-has-fill':'section-fill','vc_col-has-fill':'column-fill','vc_responsive':'silva-site','wpb-js-composer':'silva-site'}
for c in classes:
 if c.startswith('vc_col-sm-'): mapping[c]='col-md-'+c.split('-')[-1]
 elif c.startswith('vc_custom_'): mapping[c]='surface-'+c.removeprefix('vc_custom_')
 elif c.startswith(('vc_','wpb_')): mapping.setdefault(c,c.replace('vc_','silva-').replace('wpb_','silva-').replace('_','-'))
def remap(t): return re.sub(r'(?<![\w-])(?:'+ '|'.join(re.escape(k) for k in sorted(mapping,key=len,reverse=True))+r')(?![\w-])',lambda m:mapping[m[0]],t)
# Retain only used theme selectors and states, in the original cascade order.
# Bootstrap owns generic row/column widths; page-specific selectors preserve Silva spacing.
generic={'vc_row','wpb_row','vc_row-fluid','vc_column_container','wpb_column'}
css_files=sorted(SRC.rglob('*.css')); styles=[]; seen=set(); page_styles={}
def keep_selector(sel):
 cs=re.findall(r'\.([a-zA-Z_][\w-]*)',sel)
 if any(c.startswith(('fa-','wp-block','vc_tta','pp_','owl-')) for c in cs): return False
 dynamic={'scrollmin','scrolled','scrollup','submenuopen','sub-menu-open','header-mobile-menu-open','visible','active','open','no-js','not-admin'}
 if any(c not in classes and c not in dynamic for c in cs): return False
 if cs and all(c in generic or c.startswith('vc_col-') for c in cs): return False
 return True
def process(rules,cssfile):
 result=[]
 for rule in rules:
  if rule.type=='qualified-rule':
   sel=tinycss2.serialize(rule.prelude).strip(); sels=[x for x in sel.split(',') if keep_selector(x.strip())]
   if not sels: continue
   body=tinycss2.serialize(rule.content)
   def urlfix(m):
    val=m[1].strip(' \"\'')
    if val.startswith(('data:','http:','https:','#','//')): return m[0]
    target=(cssfile.parent/unquote(val)).resolve()
    return 'url("'+os.path.relpath(OUT/target.relative_to(SRC.resolve()),OUT/'assets/css')+'")'
   body=re.sub(r'url\(([^)]+)\)',urlfix,body)
   body=body.replace('../../wp-content/uploads/2020/04/pdf-icon.png','../icons/file-pdf.svg').replace('../../wp-content/uploads/2020/04/dl-icon.png','../icons/download.svg')
   selector=remap(','.join(sels))
   selector=re.sub(r'(?<=[ >])i(?=[.:#\s,>{]|$)', '.icon', selector)
   text=selector+' { '+body+' }'
   if text not in seen: seen.add(text); result.append(text)
  elif rule.type=='at-rule' and rule.content is not None and rule.lower_at_keyword in ('media','supports'):
   inner=process(tinycss2.parse_rule_list(rule.content,skip_whitespace=True,skip_comments=True),cssfile)
   if inner: result.append('@'+rule.at_keyword+' '+tinycss2.serialize(rule.prelude)+' {\n'+ '\n'.join(inner)+'\n}')
 return result
# Base is the shared stylesheet; extra page surfaces are added from the two variations.
css_files.sort(key=lambda p:0 if 'd541' in p.name else 1)
for css in css_files: styles+=process(tinycss2.parse_stylesheet(css.read_text(),skip_whitespace=True,skip_comments=True),css)
(OUT/'assets/css/silva-theme.css').write_text('/* Silva visual styling, extracted from the original static site. */\n'+'\n'.join(styles))
full=(OUT/'assets/vendor/bootstrap.min.css').read_text()
component=[]
for r in tinycss2.parse_stylesheet(full,skip_whitespace=True,skip_comments=True):
 text=tinycss2.serialize([r])
 if any(x in text for x in ['.modal','.carousel','.collapse','.collapsing',':root']): component.append(text)
(OUT/'assets/vendor/bootstrap-components.css').write_text('/* Bootstrap 5.3.8 | MIT | Modal, carousel and collapse components */\n'+'\n'.join(component))
paths={
 'fa-long-arrow-alt-right':'<path d="M3 12h18m-6-6 6 6-6 6"/>',
 'fa-bars':'<path d="M3 6h18M3 12h18M3 18h18"/>',
 'fa-chevron-right':'<path d="m9 5 7 7-7 7"/>',
 'fa-chevron-down':'<path d="m5 9 7 7 7-7"/>',
 'fa-phone-volume':'<path d="M7 3 3 5c-1 8 8 17 16 16l2-4-5-3-2 2c-3-1-5-3-6-6l2-2-3-5ZM15 3a7 7 0 0 1 6 6M15 7a3 3 0 0 1 2 2"/>',
 'fa-envelope-open-text':'<path d="m3 9 9-6 9 6v12H3V9Zm0 0 9 7 9-7M8 8h8M8 11h8"/>',
 'fa-facebook-f':'<path d="M14 22v-9h3l.5-4H14V7c0-1 .5-2 2-2h2V1h-3c-4 0-6 2-6 6v2H6v4h3v9h5Z" fill="currentColor" stroke="none"/>',
 'fa-instagram':'<rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><path d="M17 7h.01"/>'}
def icon(name,extra=''):
 return BeautifulSoup('<svg class="icon '+name+' '+extra+'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true">'+paths[name]+'</svg>','html.parser').svg
assets_index={unicodedata.normalize('NFC',str(p.relative_to(OUT))):p for p in OUT.rglob('*') if p.is_file()}
def resolve(rel,url):
 path=unquote(urlsplit(url).path)
 if not path:return None
 target=(OUT/rel).parent/path
 key=unicodedata.normalize('NFC',os.path.relpath(target.resolve(),OUT.resolve()))
 return assets_index.get(key)
image_changes=[]; inventory=[]; fixes=[]
for rel,s in soups.items():
 en=s.html.get('lang','').startswith('en'); root='../'*(len(rel.parts)-1)
 for x in s.find_all('script'):
  if x.get('id')=='tawk-script': x['type']='text/plain'; x['data-integration']='tawk'; x.attrs.pop('id',None)
  else: x.decompose()
 for x in s.select('noscript'): x.decompose()
 for x in s.find_all(string=lambda t:isinstance(t,Comment)): x.extract()
 for x in s.select('link[rel="stylesheet"]'):
  if 'fonts.googleapis.com' not in x.get('href',''): x.decompose()
 for name in ['assets/vendor/bootstrap-grid.min.css','assets/vendor/bootstrap-components.css','assets/css/silva-theme.css','assets/css/custom.css']:
  s.head.append(s.new_tag('link',rel='stylesheet',href=root+name))
 for style in s.find_all('style'):
  if style.string: style.string.replace_with(remap(str(style.string)))
 for e in s.find_all(True):
  if e.has_attr('class'):
   old=e['class']; new=[]
   for c in old:
    if c.startswith(('ewww_','js-comp-ver-','page-id-')): continue
    new.append(mapping.get(c,c))
   if 'vc_row' in old and 'row-in-grid' not in old: new+=['row','g-0']
   if 'row-in-grid-inner' in old: new+=['row','g-0']
   e['class']=list(dict.fromkeys(new))
  for a in list(e.attrs):
   if a.startswith(('data-src','data-eio','data-webp','data-lazy')) or a in ['data-rsssl','itemprop','itemscope','itemtype']: del e[a]
 for e in s.select('i'):
  name=next((c for c in e.get('class',[]) if c in paths),None)
  if name: e.replace_with(icon(name,' '.join(c for c in e.get('class',[]) if c.startswith('sub-menu-'))))
 for e in s.select('a[target="_blank"]'): e['rel']='noopener noreferrer'
 for e in s.select('a'):
  if not e.get_text(strip=True) and not e.get('aria-label'):
   e['aria-label']=e.get('title') or ('Facebook' if 'facebook' in e.get('href','') else 'Instagram' if e.select_one('.fa-instagram') else 'View' if en else 'Voir')
 # Bootstrap collapse controls retain original header geometry.
 menu=s.select_one('.header-mobile-menu'); btn=s.select_one('.mobile-menu-btn')
 if menu and btn:
  menu['id']='mobile-navigation'; menu['class']+=['collapse']
  btn.name='button'; btn['type']='button'; btn.attrs.pop('href',None)
  btn.attrs.update({'data-bs-toggle':'collapse','data-bs-target':'#mobile-navigation','aria-controls':'mobile-navigation','aria-expanded':'false','aria-label':'Open menu' if en else 'Ouvrir le menu'})
 for i,e in enumerate(s.select('.mobile-menu .sub-menu-arrow')):
  e.name='button'; e['type']='button'; e['aria-label']='About submenu' if en else 'Sous-menu entreprise'; e['data-bs-toggle']='collapse'; e['data-bs-target']=f'#submenu-{i}'; e['aria-controls']=f'submenu-{i}'; e['aria-expanded']='false'
  ul=e.find_next_sibling('ul'); ul['id']=f'submenu-{i}'; ul['class']+=['collapse']
 for n,e in enumerate(s.select('.owl-images-proprietes')):
  e['id']=f'property-carousel-{n}'; e['class']=['carousel','slide','property-carousel']; e['data-bs-ride']='carousel'; e['data-bs-interval']='6000'
  items=e.find_all('div',class_='item',recursive=False); inner=s.new_tag('div',attrs={'class':'carousel-inner'})
  for i,it in enumerate(items): it['class']=['carousel-item']+(['active'] if i==0 else []); inner.append(it.extract())
  e.append(inner)
  if items:
   for direction,label in [('prev','Previous' if en else 'Précédent'),('next','Next' if en else 'Suivant')]:
    b=s.new_tag('button',attrs={'class':'carousel-control-'+direction,'type':'button','data-bs-target':'#'+e['id'],'data-bs-slide':direction,'aria-label':label}); b.append(BeautifulSoup('<svg viewBox="0 0 24 24" class="icon" fill="none" stroke="currentColor" stroke-width="2"><path d="'+('m15 5-7 7 7 7' if direction=='prev' else 'm9 5 7 7-7 7')+'"/></svg>','html.parser').svg); e.append(b)
 # Use highest same-aspect local source only; never invent detail or alter crops.
 for img in s.select('img[src]'):
  target=resolve(rel,img['src'])
  if target and target.suffix.lower() in ['.jpg','.jpeg','.png','.webp']:
   try:
    with Image.open(target) as im: w,h=im.size
    original=re.sub(r'-\d+x\d+(?=\.[^.]+$)','',target.name); larger=target.with_name(original)
    if larger!=target and larger.exists():
     with Image.open(larger) as im: lw,lh=im.size
     if lw>w and abs(lw/lh-w/h)<.02:
      before=img['src']; img['src']=os.path.relpath(larger,(OUT/rel).parent); image_changes.append({'page':str(rel),'before':before,'after':img['src'],'width_before':w,'width_after':lw}); target=larger; w,h=lw,lh
    # Responsive original sources preserve all existing focal/crop decisions.
    img['decoding']='async'
    if img.find_parent(class_='batisseur-milieu-row') or any(c.startswith('logo') for c in img.get('class',[])):
     img['loading']='eager'
    elif not img.has_attr('fetchpriority'): img['loading']='lazy'
   except (OSError,ValueError): pass
 # Preserve forms and validation, but flag unavailable server endpoint honestly.
 for form in s.select('form'):
  form['data-contact-form']=''; form['action']='#'; form.attrs.pop('novalidate',None)
  for x in form.select('input[type="hidden"]'): x.decompose()
  for x in form.select('[aria-required="true"]'): x['required']=''; x['aria-label']=x.get('placeholder') or ('Model' if en else 'Modèle')
  note=s.new_tag('p',attrs={'class':'contact-note','role':'note'})
  note.string='Local preview: this form does not send messages. Email and telephone links remain available.' if en else 'Aperçu local : ce formulaire n’envoie aucun message. Les liens courriel et téléphone restent disponibles.'
  form.append(note)
 for a in s.select('[href]'):
  href=a['href']
  if 'index.html@p=' in href:
   # Static export has old shortlink references. Resolve by page-id against source documents.
   m=re.search(r'@p=(\d+)',href)
   if m:
    match=shortlinks.get(m[1])
    if match:
     a['href']=os.path.relpath(OUT/match,(OUT/rel).parent)+('#'+urlsplit(href).fragment if urlsplit(href).fragment else ''); fixes.append({'page':str(rel),'before':href,'after':a['href']})
 for a in s.select('a[rel]'):
  if any('prettyPhoto' in v for v in a.get('rel',[])): a['data-lightbox']=''; a['rel']=''
 for js in ['assets/vendor/bootstrap.bundle.min.js','assets/js/main.js']:
  s.body.append(s.new_tag('script',src=root+js,defer=''))
 s.html['class']=[c for c in s.html.get('class',[]) if c!='no-js']
 # Remove duplicative export metadata; leave page-specific visible content untouched.
 s.body['class']=[c for c in s.body.get('class',[]) if not c.startswith(('page-id-','postid-','wpb-','js-comp-'))]
 inventory.append({'path':str(rel),'title':s.title.get_text(),'language':'en' if en else 'fr','forms':len(s.select('form')),'gallery_images':len(s.select('[data-lightbox]'))})
 (OUT/rel).write_text(s.prettify(formatter='minimal'))
(BASE/'review/pages.json').write_text(json.dumps(inventory,ensure_ascii=False,indent=2))
(BASE/'review/image-improvements.json').write_text(json.dumps(image_changes,ensure_ascii=False,indent=2))
(BASE/'review/link-fixes.json').write_text(json.dumps(fixes,ensure_ascii=False,indent=2))
print(json.dumps({'pages':len(pages),'theme_css_bytes':(OUT/'assets/css/silva-theme.css').stat().st_size,'image_improvements':len(image_changes),'shortlink_fixes':len(fixes)},indent=2))
