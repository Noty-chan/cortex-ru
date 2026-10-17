"""Build original-pagination navigation from explicit Markdown source metadata."""
from pathlib import Path
import re

pattern=re.compile(r'с\.\s*(\d+)\s*(?:[–−-]\s*(\d+))?\s*\(PDF',re.I)
pages={n:[] for n in range(4,248)}
for p in sorted(Path('book/chapters').glob('*.md')):
 text=p.read_text(encoding='utf-8')
 match=pattern.search(text.split('Статус:')[0])
 if not match:continue
 title=re.search(r'^title:\s*(.+)$',text,re.M).group(1).strip().strip('"')
 a,b=match.groups()
 for n in range(int(a),int(b or a)+1):
  if n in pages:pages[n].append((title,p.stem))
assert all(pages.values()),[n for n,v in pages.items() if not v]
out=['''---
title: Страницы оригинала
outline: false
---

# Страницы оригинала

Печатный номер и страница PDF помогают найти соответствующий раздел русского перевода. Если исходная страница разделена между несколькими разделами, перечислены все. Числа в [авторском словаре и указателе](./chapters/book-index-a-d) сохранены из оригинала и ведут сюда; подозрительные ссылки отмечены в [реестре](./source-issues#cp-031).

| Печатная | PDF | Разделы перевода |
| --- | --- | --- |
''']
for n,entries in pages.items():
 out.append(f'| <span id="p-{n}">{n}</span> | {n+4} | '+ '; '.join(f'[{t}](./chapters/{slug})' for t,slug in entries)+' |')
out.append('\nВыходные сведения PDF5–6: [авторы](./chapters/credits); PDF7: [оглавление оригинала](./chapters/original-contents). Обложки и декоративные страницы PDF1–5/252–256: [описание и перевод](./chapters/covers).\n')
Path('book/source-pages.md').write_text('\n'.join(out),encoding='utf-8')
print('Original printed pages4–247 mapped:',len(pages))
