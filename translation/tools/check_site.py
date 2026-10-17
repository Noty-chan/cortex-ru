"""Check generated HTML links, public assets and fragment targets before publishing."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import argparse

parser=argparse.ArgumentParser();parser.add_argument('--base',default='/');args=parser.parse_args()
root=Path('book/.vitepress/dist').resolve();base=args.base.rstrip('/')
class Page(HTMLParser):
 def __init__(self,text):
  super().__init__();self.ids=set();self.refs=[];self.feed(text)
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.add(a['id'])
  for key in ('href','src'):
   if a.get(key):self.refs.append(a[key])
pages={p:Page(p.read_text(encoding='utf-8')) for p in root.rglob('*.html')}
errors=set();checked=set()
for file,page in pages.items():
 for ref in page.refs:
  url=urlsplit(ref)
  if url.scheme or url.netloc:continue
  path=unquote(url.path)
  if path.startswith('/'):
   if base and not (path==base or path.startswith(base+'/')):
    errors.add((file.relative_to(root).as_posix(),ref,'missing project base'));continue
   path=path[len(base):].lstrip('/') if base else path.lstrip('/')
   target=root/path
  elif not path:target=file
  else:target=file.parent/path
  target=target.resolve()
  if target.is_dir():target=target/'index.html'
  elif not target.exists() and not target.suffix:target=target.with_suffix('.html')
  key=(target,url.fragment)
  if key in checked:continue
  checked.add(key)
  if not target.exists():errors.add((file.relative_to(root).as_posix(),ref,'missing file'))
  elif url.fragment and target in pages and unquote(url.fragment) not in pages[target].ids:
   errors.add((file.relative_to(root).as_posix(),ref,'missing anchor'))
print(f'Checked {len(pages)} HTML pages and {len(checked)} unique local targets; errors: {len(errors)}')
for e in sorted(errors):print(' | '.join(e))
raise SystemExit(bool(errors))
