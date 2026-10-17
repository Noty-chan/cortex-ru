"""Reassemble verified split artwork from original PDF pixels, without redrawing.
Run from repository root. Pair recipes and decisions: translation/visuals.md.
"""
from pathlib import Path
from PIL import Image
from pypdf import PdfReader
reader = PdfReader(next(Path('sources').glob('Cortex Prime - Game Handbook*.pdf')))
pairs = [(8,9),(18,19),(34,35),(36,37),(48,49),(68,69),(90,91),(112,113),(114,115),(118,119),(128,129),(130,131),(134,135),(136,137),(138,139),(154,155)]
out = Path('book/public/images/spreads')
out.mkdir(parents=True,exist_ok=True)
for left,right in pairs:
    target=out/f'printed-{left-4:03}-{right-4:03}.webp'
    if target.exists():
        continue
    images=[]
    for page in [left,right]:
        items=[x.image for x in reader.pages[page-1].images if x.name.endswith('.jp2')]
        index=1 if (left,right)==(134,135) and page==135 else 0
        images.append(items[index].convert('RGBA'))
    a,b=images
    assert a.height==b.height,(left,right,a.size,b.size)
    # Each source contains about 1pt of gutter bleed; remove 2px from each inner edge.
    a=a.crop((0,0,a.width-2,a.height))
    b=b.crop((2,0,b.width,b.height))
    merged=Image.new('RGBA',(a.width+b.width,a.height))
    merged.paste(a,(0,0)); merged.paste(b,(a.width,0))
    path=out/f'printed-{left-4:03}-{right-4:03}.webp'
    merged.save(path,format='WEBP',lossless=True,method=6)
    print(path,merged.size)
