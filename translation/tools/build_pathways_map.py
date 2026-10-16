"""Russian dark reproduction of the completed pathways map, printed p80."""
from pathlib import Path
from html import escape
out=Path('book/public/images/diagrams/pathways-map-dark.svg')
parts=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1100 1090" role="img" aria-labelledby="title desc">','<title id="title">Готовая карта жизненных путей</title>','<desc id="desc">Инженер связана с Героем, Мудрецом, Иоландой, Светящимися существами, Очками инженера, Новой паровой эпохой, Паровым городом, HMS Astonish и Гражданскими волнениями. Связи других PC и неназванные элементы показаны отдельно.</desc>','<rect width="1100" height="1090" rx="22" fill="#25232e"/>','<g font-family="Arial, sans-serif" text-anchor="middle" fill="#eee9f4">','<text x="550" y="44" font-size="27">Готовая карта жизненных путей</text>']
nodes={
'eng':(550,360,'pc',['Инженер']), 'hero':(310,730,'pc',['Герой']), 'sage':(790,730,'pc',['Мудрец']),
'light':(410,155,'gmc',['Светящиеся','существа']), 'mother':(700,155,'gmc',['Иоланда']),
'goggles':(200,360,'res',['Очки','инженера']), 'age':(900,360,'sit',['Новая паровая','эпоха']),
'city':(220,530,'res',['Паровой','город']), 'ship':(550,600,'res',['HMS','Astonish']), 'unrest':(880,530,'sit',['Гражданские','волнения']),
'h1':(110,700,'res',[]),'h2':(110,830,'res',[]),'h3':(310,920,'gmc',[]),
's1':(990,700,'sit',[]),'s2':(990,830,'sit',[]),'s3':(790,920,'res',[]),'shared':(550,940,'gmc',[])}
def line(a,b,color,dash=False,width=2):
 x,y,*_=nodes[a];xx,yy,*_=nodes[b];parts.append(f'<path d="M{x},{y} L{xx},{yy}" fill="none" stroke="{color}" stroke-width="{width}"'+(' stroke-dasharray="10 8"' if dash else '')+'/>')
for key in ['hero','sage','light','mother','goggles','age','city','ship','unrest']:line('eng',key,'#ed558e',width=4 if key in ['hero','sage'] else 2)
for who in ['hero','sage']:
 for key in ['city','ship','unrest']:line(who,key,'#78cba4')
line('hero','sage','#78cba4',width=4)
for who,keys in [('hero',['h1','h2','h3','shared']),('sage',['s1','s2','s3','shared'])]:
 for key in keys:line(who,key,'#78cba4',True)
for key,(x,y,kind,labels) in nodes.items():
 c={'pc':'#c90050','gmc':'#396f5a','res':'#79549d','sit':'#18171e'}[kind];stroke='#eee9f4' if kind=='sit' else c
 attrs=f'fill="{c if labels else "#25232e"}" stroke="{stroke}" stroke-width="2"'+(' stroke-dasharray="9 7"' if not labels else '')
 if kind=='pc':shape=f'<rect x="{x-95}" y="{y-37}" width="190" height="74" rx="3" {attrs}/>'
 elif kind=='gmc':shape=f'<ellipse cx="{x}" cy="{y}" rx="90" ry="40" {attrs}/>'
 elif kind=='res':shape=f'<polygon points="{x},{y-58} {x+85},{y} {x},{y+58} {x-85},{y}" {attrs}/>'
 else:shape=f'<polygon points="{x},{y-60} {x+75},{y+45} {x-75},{y+45}" {attrs}/>'
 parts.append(shape)
 for i,label in enumerate(labels):parts.append(f'<text x="{x}" y="{y+(i-(len(labels)-1)/2)*23+7}" font-size="{23 if kind=="pc" else 18}" font-weight="bold">{escape(label)}</text>')
parts+=['<text x="550" y="1010" font-size="17">Прямоугольник — PC · Овал — второстепенный персонаж</text>','<text x="550" y="1037" font-size="17">Треугольник — ситуация · Ромб — ресурс</text>','<text x="550" y="1064" font-size="16">Розовые линии — связи Инженера · Зелёные — других PC · Пунктир — незаполненные элементы</text>','</g></svg>']
out.write_text('\n'.join(parts)+'\n',encoding='utf-8');print(out)
