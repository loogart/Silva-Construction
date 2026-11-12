from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import json,math
BASE=Path(__file__).resolve().parents[1];R=BASE/'review';dest=R/'contact-sheets';dest.mkdir(exist_ok=True)
pages={x['id']:x['path'] for x in json.loads((R/'final-checks.json').read_text())}
font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',13)
for kind,cols,rows,thumb in [('desktop',4,4,(320,222)),('mobile',8,4,(120,277))]:
 files=sorted((R/('final-'+kind)).glob('*.jpg'));w,h=thumb;cellh=h+38
 for start in range(0,len(files),cols*rows):
  subset=files[start:start+cols*rows];sheet=Image.new('RGB',(cols*w,math.ceil(len(subset)/cols)*cellh),'#eef0f5');draw=ImageDraw.Draw(sheet)
  for n,p in enumerate(subset):
   image=Image.open(p);image.thumbnail((w-8,h));x=(n%cols)*w;y=(n//cols)*cellh;sheet.paste(image,(x+(w-image.width)//2,y))
   label=p.stem+' '+pages[p.stem].removesuffix('/index.html');draw.text((x+4,y+h+3),label[:43] if kind=='desktop' else p.stem,fill='#042744',font=font)
  sheet.save(dest/f'{kind}-{start//(cols*rows)+1:02}.jpg',quality=88)
print('Created desktop and mobile review sheets.')
