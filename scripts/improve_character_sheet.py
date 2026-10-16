"""Add field tooltips and keyboard order without changing the source form.

Requires pypdf and PyMuPDF. Run from any directory with Python 3.
"""
from pathlib import Path
from collections import Counter
import hashlib
import json
import fitz
from pypdf import PdfReader, PdfWriter
from pypdf.generic import NameObject, TextStringObject

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'sources/RUS_Cortex_Prime_Core_Character_Sheet_form-fillable.pdf'
TARGET = ROOT / 'book/public/sheets/cortex-character-sheet-v1.pdf'
skills = ['Вождение', 'Восприятие', 'Влияние', 'Выживание', 'Драка', 'Знание',
          'Исполнение', 'Концентрация', 'Медицина', 'Метание', 'Обман',
          'Пилотирование', 'Подвижность', 'Ремесло', 'Ремонт', 'Скрытность',
          'Стрельба', 'Труд', 'Устройства']
text_labels = {
    'untitled20': 'Имя персонажа', 'untitled21': 'Пункты сюжета — количество',
    'untitled23': 'Описание персонажа', 'untitled136': 'Дополнительные черты',
    'untitled137': 'Особенность 1 — название', 'untitled138': 'Особенность 2 — название',
    'untitled139': 'Особенность 3 — название',
    'untitled140': 'Особое имущество 1 — название',
    'untitled141': 'Особое имущество 2 — название',
}
for name, number, effect in [('untitled24',1,1),('untitled119',1,2),
                             ('untitled120',2,1),('untitled121',2,2),
                             ('untitled122',3,1),('untitled123',3,2)]:
    text_labels[name] = f'Особенность {number} — SFX {effect}: описание'
for i, name in enumerate(['untitled142','untitled146','untitled147','untitled148',
    'untitled149','untitled150','untitled151','untitled152','untitled153','untitled154',
    'untitled155','untitled157','untitled174','untitled175','untitled176','untitled177',
    'untitled178','untitled179','untitled180']):
    text_labels[name] = f'{skills[i]} — специализация или заметка'

labels = {}
doc = fitz.open(SOURCE)
for page in doc:
    for w in page.widgets():
        x, y = w.rect.x0, w.rect.y0
        if w.field_name in text_labels:
            label = text_labels[w.field_name]
        elif x < 210 and y < 300:
            attr = ['Физический', 'Ментальный', 'Социальный'][min(2,round((y-158)/52))]
            die = [4,6,8,10,12][min(4,max(0,round((x-86)/23)))]
            label = f'{attr} атрибут — d{die}'
        elif x < 210 and 300 <= y <= 710:
            skill = skills[min(18,max(0,round((y-303)/21)))]
            die = [4,6,8,10,12][min(4,max(0,round((x-148)/10.2)))]
            label = f'{skill} — d{die}'
        elif x > 530:
            label = f'Правое поле отметок — ячейка {max(1,round((y-355)/18)+1)}'
        elif y > 650 and x >= 430:
            item = 1 if y < 685 else 2
            die = [6,8,10,12][min(3,max(0,round((x-450)/19.5)))]
            label = f'Особое имущество {item} — d{die}'
        else:
            block = min(3,max(1,int((y-140)//168)+1))
            label = f'Особенность {block} — отметка SFX ({w.field_name})'
        labels[w.field_name] = label
doc.close()

reader = PdfReader(SOURCE)
writer = PdfWriter(clone_from=reader)
for page in writer.pages:
    # ISO PDF row-based tab order, recognized by compatible viewers.
    page[NameObject('/Tabs')] = NameObject('/R')
    for ref in page.get('/Annots', []):
        field = ref.get_object()
        if field.get('/Subtype') == '/Widget' and field.get('/T') in labels:
            field[NameObject('/TU')] = TextStringObject(labels[str(field['/T'])])
writer.add_metadata({
    '/Title': 'Cortex — русский интерактивный лист, доработка v1',
    '/Subject': 'Подсказки к полям и построчная навигация Tab; исходная механика сохранена',
})
TARGET.parent.mkdir(parents=True, exist_ok=True)
with TARGET.open('wb') as output:
    writer.write(output)

before, after = reader.get_fields(), PdfReader(TARGET).get_fields()
assert set(before) == set(after), 'Field names changed'
for name, original in before.items():
    assert original.get('/V') == after[name].get('/V'), name
    assert original.get('/FT') == after[name].get('/FT'), name
    assert after[name].get('/TU'), name
assert len({str(f['/TU']) for f in after.values()}) == len(after), 'Duplicate tooltips'
report = {'source_sha256': hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
          'fields': len(after), 'types': dict(Counter(str(v.get('/FT')) for v in after.values())),
          'all_tooltips_present': True, 'original_names_types_values_preserved': True,
          'target': TARGET.relative_to(ROOT).as_posix()}
output = ROOT / 'output/pdf'
output.mkdir(parents=True, exist_ok=True)
(output/'character-sheet-validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
render = fitz.open(TARGET)
render[0].get_pixmap(matrix=fitz.Matrix(.8,.8)).save(str(output/'character-sheet-after.png'))
print(json.dumps(report,ensure_ascii=False))
