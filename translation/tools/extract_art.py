"""Extract original embedded book artwork, retaining transparency and a manifest.

Usage from repo root: python translation/tools/extract_art.py 8 27
Decorative PNG page backgrounds are excluded; artwork in this PDF is JP2.
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
    for index, item in enumerate(x for x in reader.pages[number-1].images if x.name.endswith('.jp2')):
        path = out / f'pdf-{number:03}-art-{index+1:02}.webp'
        if not path.exists():
            item.image.save(path, format='WEBP', quality=95, method=4)
        items.append({'source_image': item.name, 'output': path.as_posix(),
                      'width': item.image.width, 'height': item.image.height,
                      'mode': item.image.mode})
    manifest[str(number)] = {'pdf_page': number, 'printed_page': number-4, 'images': items}
manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print(f'Artwork inventoried: PDF {args.first}–{args.last}; entries: {len(manifest)}')
