"""Russian dark SVG reproductions of the five usable appendix forms (PDF248–251).

These are code-native vector assets, not altered original artwork or fillable PDFs.
All functional labels, tracks and preprinted values also appear in Markdown.
"""
from pathlib import Path
from html import escape
import textwrap

OUT=Path('book/public/images/diagrams');OUT.mkdir(parents=True,exist_ok=True)
class Sheet:
 def __init__(self,title,subtitle,height=1700):
  self.h=height;self.parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="{height}" viewBox="0 0 1200 {height}" role="img"><title>{escape(title)}</title><desc>{escape(subtitle)}</desc><style>text{{font-family:Arial,sans-serif;fill:#edf0f7}}.muted{{fill:#abb7cd}}.accent{{fill:#f399bd}}.rule{{stroke:#69758d;stroke-width:1.5}}</style><rect width="1200" height="{height}" rx="20" fill="#191c25"/>']
  self.text(40,60,title,34,'accent');self.text(40,96,subtitle,17,'muted');self.line(40,116,1160,116)
 def text(self,x,y,s,size=20,cls=''):
  self.parts.append(f'<text x="{x}" y="{y}" font-size="{size}" class="{cls}">{escape(s)}</text>')
 def line(self,x,y,x2,y2):self.parts.append(f'<line x1="{x}" y1="{y}" x2="{x2}" y2="{y2}" class="rule"/>')
 def panel(self,x,y,w,h,title):
  self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="#252a37" stroke="#535f75"/>');self.text(x+16,y+30,title,min(22,(w-32)/max(1,len(title))/.57),'accent')
 def para(self,x,y,s,width=65,size=19):
  lines=textwrap.wrap(s,width=width,break_long_words=False,break_on_hyphens=False)
  for i,line in enumerate(lines):self.text(x,y+i*(size+7),line,size)
  return y+len(lines)*(size+7)
 def blank(self,x,y,w,label):self.text(x,y,label,18,'muted');self.line(x,y+30,x+w,y+30)
 def track(self,x,y,label,stress=False,width=330):
  self.text(x,y,label,21);self.text(x,y+32,'□ d4    □ d6    □ d8    □ d10    □ d12',17,'muted')
  if stress:self.text(x,y+61,'Стресс:  □ d4  □ d6  □ d8  □ d10  □ d12',15)
 def save(self,slug):
  self.text(40,self.h-25,'Русское воспроизведение • Cortex Prime Game Handbook, 2020 • функциональная разметка сохранена',15,'muted')
  self.parts.append('</svg>');(OUT/(slug+'.svg')).write_text('\n'.join(self.parts),encoding='utf-8')
 def identity(self,history=True):
  self.blank(40,150,350,'Имя:');self.blank(40,215,350,'Прошлое:' if history else 'Позывной:');self.blank(440,150,720,'Описание:');self.line(440,245,1160,245)

HINDER='Помеха: получите 1 PP, когда заменяете d8 этой отличительной черты на d4.'

def eidolon():
 s=Sheet('EIDOLON ALPHA — лист персонажа','Источник: с.244 / PDF248. Совет оригинала: для лучшего результата пользуйтесь карандашом.')
 s.identity();s.panel(40,280,360,400,'Роли')
 for i,l in enumerate(['Воин','Жрец','Разведчик','Другая роль: __________']):s.track(56,350+i*83,l)
 s.panel(40,700,360,850,'Атрибуты')
 for i,l in enumerate(['Мужество','Грация','Хитрость','Разум','Выносливость']):
  y=770+i*151;s.track(56,y,l,True);s.text(56,y+91,'Выделенный атрибут: ○',16,'muted')
 s.panel(430,280,730,890,'Отличительная черта эндарха d8: __________________')
 for i in range(3):s.blank(452+i*230,345,207,f'Сила {i+1} — d8:')
 y=s.para(452,440,HINDER,66)
 for i in range(3):s.blank(452,y+45+i*80,680,'Спецэффект:')
 s.para(452,785,'Призыв: отключите отличительную черту эндарха, чтобы призвать своего эйдолона в следующий ход.',65)
 s.panel(452,885,686,260,'Призванный эйдолон')
 s.text(470,950,'Базовая черта: 2d10 или 2d4',22);s.text(470,994,'Масштаб: d8',22)
 s.text(470,1040,'Силы:  d12 ______  d12 ______  d12 ______',19)
 s.text(470,1095,'Выделенные атрибуты: d12 ______  d12 ______',19)
 s.panel(430,1190,730,150,'Отличительная черта роли d8: __________________')
 s.para(450,1250,HINDER,65)
 s.panel(430,1360,730,150,'Свободная отличительная черта d8: ______________')
 s.para(450,1420,HINDER,65)
 s.blank(430,1560,730,'XP:');s.save('appendix-eidolon-dark')

def trace():
 s=Sheet('TRACE 2.0 — лист персонажа','Источник: с.245 / PDF249. Совет оригинала: для лучшего результата пользуйтесь карандашом.')
 s.identity();s.panel(40,280,360,300,'Принадлежности')
 for i,l in enumerate(['Один','Вдвоём','Отрядом']):s.track(56,347+i*78,l)
 s.panel(40,600,360,630,'Роли')
 for i,l in enumerate(['Криминалистика','Расследование','Право','Медицина','Психология','Тактика','Технологии']):s.track(56,670+i*78,l)
 s.panel(40,1250,360,355,'Ресурсы')
 for i,r in enumerate(['2d10','2d8','2d6','2d6','_____','_____']):s.blank(56,1310+i*45,328,r+' —')
 s.panel(430,280,730,300,'Отличительные черты')
 for i in range(3):s.blank(450,340+i*64,690,f'Отличительная черта №{i+1}:')
 s.para(450,610,HINDER,66)
 s.panel(430,690,730,520,'Таланты')
 for i in range(6):s.blank(450,750+i*75,690,f'Талант №{i+1}:')
 s.panel(430,1230,730,375,'Стресс')
 for i,l in enumerate(['Испуг','Гнев','Тревога','Истощение','Ранение']):
  y=1300+i*50;s.text(450,y,l,20);s.text(650,y,'□ d4   □ d6   □ d8   □ d10   □ d12',18)
 s.text(450,1570,'Пул развития — база: 2d6. Текущий пул: __________',20)
 s.save('appendix-trace-dark')

PACKAGES=['Управление толпой','Экстренная медицина','Пожаротушение','Пилот Hammerhead','Опасные вещества (HAZMAT)','Высотное спасение','Правовой специалист','Логистика','Спасение на воде','Сетевой специалист','Механик','Тактическое реагирование','Технический аналитик','Спасение в городе']

def hammerheads():
 s=Sheet('HAMMERHEADS — лист персонажа','Источник: с.246 / PDF250. Совет оригинала: для лучшего результата пользуйтесь карандашом.',1900)
 s.identity(False);s.panel(40,280,430,400,'Атрибуты')
 for i,l in enumerate(['Физический','Ментальный','Социальный']):s.track(56,350+i*110,l,True)
 s.panel(40,700,430,1100,'Пакеты подготовки')
 for i,l in enumerate(PACKAGES):
  y=765+i*72;s.text(56,y,'□ '+l,17);s.text(80,y+28,'□ d4   □ d6   □ d8   □ d10   □ d12',16,'muted')
 titles=['Ваша прежняя жизнь:','Ваш подход / настрой:','Ваша особенность / качество:']
 extra=[['Потратьте 1 PP, чтобы повысить атрибут, когда обращаетесь к прежней жизни.','Добавьте d6 в кризисный пул, чтобы удвоить кость атрибута, когда обращаетесь к прежней жизни.'],['Потратьте 1 PP, чтобы перебросить кости, когда следуете своей истинной природе.','Добавьте d6 в кризисный пул, чтобы повысить кость пакета подготовки, когда следуете своей истинной природе.'],['Потратьте 1 PP, чтобы удвоить кость отношения, когда ваша помощь отражает вашу особенность или качество.','Добавьте d6 в кризисный пул, чтобы повысить включённую в пул кость отношения, когда проявляете свою особенность или качество.']]
 for i,title in enumerate(titles):
  y=280+i*330;s.panel(500,y,660,310,title);s.line(520,y+65,1140,y+65);yy=s.para(520,y+98,HINDER,57,18)
  for p in extra[i]:yy=s.para(520,yy+15,p,57,18)
 s.panel(500,1290,660,510,'Отношения')
 for i,l in enumerate(['спас(ла) мне жизнь','много мне должен / должна','создаёт неприятности','знает своё дело','обуза','надёжный человек','с ним / ней весело']):
  y=1355+i*59;s.text(520,y,'________ '+l,18);s.text(520,y+24,'□ d4    □ d6    □ d8    □ d10    □ d12',15,'muted')
 s.text(500,1840,'XP: __________________________________________',22);s.save('appendix-hammerheads-dark')

def vehicle():
 s=Sheet('HAMMERHEADS — лист транспорта','Источник: с.247 / PDF251, верхняя половина.',1100)
 s.panel(40,150,390,630,'Атрибуты: Двигатели / Корпус / Системы')
 vehicles=[('Hammerhead One','d8 / d8 / d10','Манёвреннее; более точные датчики и приборы.'),('Hammerhead Two','d10 / d8 / d8','Быстрее; больше мощность и дальность.'),('Hammerhead Three','d8 / d10 / d8','Крупнее, прочнее и выносливее.')]
 for i,(name,dice,desc) in enumerate(vehicles):
  y=230+i*180;s.text(60,y,'○ '+name,23);s.text(60,y+45,dice,23);s.para(60,y+85,desc,30,18)
 s.panel(460,150,700,295,'Отличительные черты — все d8')
 for i,l in enumerate(['Транспорт ресурсной поддержки','По последнему слову техники','Датчики широкого спектра']):s.text(480,220+i*49,l,23)
 s.para(480,385,HINDER,60,18)
 s.panel(460,470,700,130,'Нераспределённые ресурсы')
 s.text(480,550,'d6    d6    d6    d6    d6    d6    d6',27)
 s.panel(460,620,700,380,'Пулы ресурсов')
 for i,l in enumerate(['Тактическая поддержка','Медицинские запасы','IT и сети','Пища и укрытие','Поддержка на суше, воде и в воздухе']):
  y=690+i*57;s.text(480,y,l,20);s.text(480,y+24,'База: d6     □ d6     □ d6     □ d6',17,'muted')
 s.save('appendix-vehicle-dark')

def crisis():
 s=Sheet('КРИЗИСНЫЕ ПУЛЫ','Источник: с.247 / PDF251, нижняя половина.',1100)
 s.para(40,160,'Впишите название кризисного пула в каждый сектор. Над значками подходящих костей запишите число костей его начальной оценки. Положите кости каждого кризисного пула в большую пустую область.',105,20)
 for i in range(4):
  x=40+(i%2)*575;y=270+(i//2)*380;s.panel(x,y,550,350,'Название: _____________________')
  s.text(x+20,y+80,'Начальная оценка: количество костей',19,'muted')
  s.text(x+20,y+125,'___ d6     ___ d8     ___ d10     ___ d12',20)
  s.text(x+20,y+185,'Место для костей пула',19,'muted')
 s.save('appendix-crisis-dark')

if __name__=='__main__':
 for f in [eidolon,trace,hammerheads,vehicle,crisis]:f()
 print('Five dark appendix SVG forms generated.')
