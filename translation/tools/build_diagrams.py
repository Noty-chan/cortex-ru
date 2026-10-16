"""Reproduce book diagrams as accessible Russian SVGs; run from the repo root."""
from pathlib import Path
from math import cos, sin, pi
from html import escape

OUT = Path('book/public/images/diagrams')
OUT.mkdir(parents=True, exist_ok=True)
INK = '#eee9f4'
RED = '#d82f70'


def text(x, y, label, size=23, fill=INK, anchor='middle'):
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}" fill="{fill}">{escape(label)}</text>'


def die(x, y, sides, radius=27):
    if sides == 4:
        points = [(x-radius, y-radius), (x+radius, y-radius), (x, y+radius)]
    elif sides == 6:
        points = [(x-radius, y-radius), (x+radius, y-radius), (x+radius, y+radius), (x-radius, y+radius)]
    else:
        count = {8: 4, 10: 6, 12: 12}[sides]
        points = [(x+radius*cos(-pi/2+2*pi*i/count), y+radius*sin(-pi/2+2*pi*i/count)) for i in range(count)]
    poly = ' '.join(f'{a:.1f},{b:.1f}' for a,b in points)
    return f'<polygon points="{poly}" fill="{RED}"/>' + text(x, y+8 if sides != 4 else y+1, str(sides), 22, 'white')


def svg(name, title, description, width, height, body):
    content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title><desc id="desc">{escape(description)}</desc>
<rect x="0.5" y="0.5" width="{width-1}" height="{height-1}" rx="18" fill="#25232e" stroke="#494353"/>
<g font-family="Segoe UI, Arial, sans-serif">{body}</g></svg>'''
    (OUT / name).write_text(content, encoding='utf-8')


parts = [text(330, 40, 'Изменение размера кости', 27)]
for y, a, b, label in [(100,4,6,'Повысить на 1'),(190,8,12,'Повысить на 2'),(280,12,10,'Понизить на 1')]:
    parts += [die(75,y,a), f'<path d="M 125 {y} H 200 l -10 -7 m 10 7 l -10 7" fill="none" stroke="{INK}" stroke-width="3"/>',die(250,y,b), text(320,y+8,label,24,anchor='start')]
svg('dice-steps-dark.svg','Повышение и понижение костей','d4 становится d6 при повышении на одну ступень; d8 становится d12 при повышении на две; d12 становится d10 при понижении на одну.',660,335,''.join(parts))

parts = [text(320,40,'Кости сложности: две одинаковые',26)]
for i,(sides,label) in enumerate([(4,'Очень лёгкая'),(6,'Лёгкая'),(8,'Непростая'),(10,'Трудная'),(12,'Очень трудная')]):
    y=105+85*i
    parts += [die(60,y,sides),die(130,y,sides),text(190,y+8,label,24,anchor='start'),text(570,y+8,f'2d{sides}',25)]
svg('difficulty-dark.svg','Шкала сложности','Очень лёгкая: 2d4. Лёгкая: 2d6. Непростая: 2d8. Трудная: 2d10. Очень трудная: 2d12.',640,495,''.join(parts))

parts = [text(320,40,'Типы костей',28)]
for i,(sides,label) in enumerate([(4,'Тетраэдр'),(6,'Гексаэдр'),(8,'Октаэдр'),(10,'Пятиугольный трапецоэдр'),(12,'Додекаэдр')]):
    y=105+85*i
    parts += [die(65,y,sides),text(115,y+7,f'd{sides}',23,anchor='start'),text(195,y+7,label,22,anchor='start')]
svg('dice-types-dark.svg','Обозначения типов костей','d4 — тетраэдр, d6 — гексаэдр, d8 — октаэдр, d10 — пятиугольный трапецоэдр, d12 — додекаэдр. Значки обозначают типы костей, а не результаты броска.',640,495,''.join(parts))
parts = [text(330,40,'Пирамида навыков',28)]
for offset, title, rows in [(0,'Для вершины d10',[[10],[8,8],[6,6,6]]),(300,'Для вершины d12',[[12],[10,10],[8,8,8],[6,6,6,6]])]:
    parts.append(text(330,85+offset,title,26))
    for row, dice in enumerate(rows):
        y=140+offset+65*row
        for j,sides in enumerate(dice):
            parts.append(die(330+(j-(len(dice)-1)/2)*70,y,sides,24))
    parts.append(f'<path d="M 210 {172+offset} H 450" stroke="{INK}" stroke-width="2" stroke-dasharray="7 6"/>')
svg('skill-pyramid-dark.svg','Пирамида навыков','Для навыка d10 требуются два d8 и три d6. Для навыка d12 требуются два d10, три d8 и четыре d6. Верхняя кость над пунктирной линией, необходимые навыки под ней.',660,690,''.join(parts))
print('Built 4 SVG diagrams')
