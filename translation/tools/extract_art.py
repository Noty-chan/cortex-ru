"""Extract original embedded book artwork, retaining transparency and a manifest.

Usage from repo root: python translation/tools/extract_art.py 8 27
Decorative PNG page backgrounds are excluded. JP2 and JPEG artwork is retained;
JPEG has a separate stable suffix so existing JP2 references never shift.
"""
from pathlib import Path
from pypdf import PdfReader
import argparse
import json

parser = argparse.ArgumentParser()
parser.add_argument('first', type=int)
parser.add_argument('last', type=int)
args = parser.parse_args()
source = next(Path('sources').glob('Cortex Prime - Game Handbook*.pdf'))
reader = PdfReader(source)
out = Path('book/public/images/original')
out.mkdir(parents=True, exist_ok=True)
manifest_path = Path('translation/artwork-inventory.json')
manifest = json.loads(manifest_path.read_text(encoding='utf-8')) if manifest_path.exists() else {}
for number in range(args.first, args.last+1):
    items = []
    if number in (1,256):
        # The cover's resource dictionary contains many JPEG tiles (and hidden
        # objects from the full wrap). Render the visible PDF page as one asset.
        import subprocess
        from PIL import Image
        preview=Path(f'output/source-review/page-{number:03}.png')
        if not preview.exists():
            preview.parent.mkdir(parents=True,exist_ok=True)
            subprocess.run(['pdftoppm','-f',str(number),'-l',str(number),'-scale-to','1700','-png',str(source),'output/source-review/page'],check=True)
        im=Image.open(preview)
        path=out/f'pdf-{number:03}-cover.webp'
        im.save(path,format='WEBP',quality=95,method=4)
        manifest[str(number)]={'pdf_page':number,'printed_page':None,'images':[{'source_image':'visible page render (pdftoppm)','output':path.as_posix(),'width':im.width,'height':im.height,'mode':im.mode}]}
        continue
    for index, item in enumerate(x for x in reader.pages[number-1].images if x.name.endswith('.jp2')):
        path = out / f'pdf-{number:03}-art-{index+1:02}.webp'
        if not path.exists():
            item.image.save(path, format='WEBP', quality=95, method=4)
        items.append({'source_image': item.name, 'output': path.as_posix(),
                      'width': item.image.width, 'height': item.image.height,
                      'mode': item.image.mode})
    for index, item in enumerate(x for x in reader.pages[number-1].images if x.name.lower().endswith(('.jpg','.jpeg'))):
        path = out / f'pdf-{number:03}-photo-{index+1:02}.webp'
        if not path.exists():
            item.image.save(path, format='WEBP', quality=95, method=4)
        items.append({'source_image': item.name, 'output': path.as_posix(),
                      'width': item.image.width, 'height': item.image.height,
                      'mode': item.image.mode})
    manifest[str(number)] = {'pdf_page': number, 'printed_page': number-4, 'images': items}
manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print(f'Artwork inventoried: PDF {args.first}–{args.last}; entries: {len(manifest)}')
