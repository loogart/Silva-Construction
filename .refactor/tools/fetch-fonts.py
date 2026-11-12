from pathlib import Path
import re,urllib.request
root=Path(__file__).resolve().parents[1]/'bootstrap/assets/fonts';root.mkdir(parents=True,exist_ok=True)
css=Path('/private/tmp/silva-font-css.txt').read_text();rules=[]
for weight,url in re.findall(r'font-weight:\s*(\d+);.*?src:\s*url\(([^)]+)\)',css,re.S):
 file=f'nunito-sans-{weight}.ttf';urllib.request.urlretrieve(url,root/file)
 rules.append(f"@font-face {{ font-family:'Nunito Sans';font-style:normal;font-weight:{weight};font-display:swap;src:url('../fonts/{file}') format('truetype'); }}")
(root.parent/'css/fonts.css').write_text('\n'.join(rules)+'\n')
urllib.request.urlretrieve('https://raw.githubusercontent.com/google/fonts/main/ofl/nunitosans/OFL.txt',root/'OFL.txt')
print('Downloaded all seven existing font weights and their license.')
