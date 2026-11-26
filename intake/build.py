#!/usr/bin/env python3
"""Шаблон анкеты для встречи: вопросы живой формы «Анкета поступающего» на бумаге.
Запуск: python3 build.py  → anketa-dlya-vstrechi.html (+ PDF через Chrome headless)."""
import subprocess, pathlib, html
H = pathlib.Path(__file__).parent
e = html.escape
def L(n=1): return '<div class="l"></div>' * n
def opts(items, other=True, col=False):
    s = ''.join(f'<span class="o"><i class="cb"></i>{e(x)}</span>' for x in items)
    if other: s += '<span class="o oth"><i class="cb"></i>другое: <u></u></span>'
    return f'<div class="opts{" col" if col else ""}">{s}</div>'
def q(title, body, desc=''):
    d = f'<div class="d">{e(desc)}</div>' if desc else ''
    return f'<div class="q"><div class="t">{e(title)}</div>{d}{body}</div>'
def f(label, wide=False):
    return f'<div class="f{" w" if wide else ""}"><span>{e(label)}</span><u></u></div>'
WHO = ['мама', 'папа', 'бабушка', 'дедушка', 'опекун']
VACC = ['Туберкулёз (БЦЖ или поливакцина)', 'Гепатит B', 'Дифтерия, столбняк, коклюш (АКДС)', 'Полиомиелит',
        'Корь, краснуха, паротит (КПК)', 'Ветрянка', 'Гепатит A', 'Ротавирус']
vacc = ('<table class="v"><tr><th></th><th>делали</th><th>не делали</th><th>не знаю</th></tr>'
        + ''.join(f'<tr><td>{e(v)}</td>' + '<td class="c"><i class="cb"></i></td>' * 3 + '</tr>' for v in VACC) + '</table>')

P = []
P.append('''<div class="hdr"><h1>Анкета поступающего <span class="yr">· для встречи с куратором</span></h1>
<div class="small">Если семья не заполнила анкету заранее. Вопросы те же, что в анкете для родителей.</div>
<div class="small after"><b>После встречи, в тот же день:</b> сфотографируйте заполненные страницы и пришлите в чат кураторов — в тред под сообщением о ребёнке, а если сообщения не было, отдельным сообщением с его именем.</div>
<div class="row">''' + f('Дата встречи') + f('Куратор') + f('Класс') + '</div></div>')

P.append('<h2>Ребёнок</h2>')
P.append('<div class="row">' + f('Фамилия и имя ребёнка на кириллице', True) + '</div>')
P.append('<div class="row">' + f('Фамилия и имя на латинице, как в загранпаспорте', True) + '</div>')
P.append('<div class="row">' + f('Дата рождения') + '</div>')

P.append('<h2>Контакты</h2>')
P.append('<div class="d">Школьное приложение называется Mojo: расписание, задания, оценки, комментарии педагогов, чат с куратором. '
         'Личный кабинет регистрируется для каждого взрослого по e-mail. Записываем тех, кому семья хочет показывать всю информацию о ребёнке.</div>')
P.append('<h3>Основной контакт</h3>')
P.append('<div class="row">' + f('Фамилия и имя', True) + '</div>')
P.append('<div class="row">' + f('E-mail для Mojo', True) + '</div>')
P.append(q('Кто вы ребёнку?', opts(WHO)))
P.append('<div class="row">' + f('Телефон') + f('Telegram: ссылка или номер') + '</div>')
P.append('<div class="d">Телефон — по которому возьмут трубку в учебное время; если тайского номера пока нет, тот, что есть. '
         'Telegram — для подключения к фото-дайджесту и дублирования связи с куратором.</div>')
P.append('<h3>Второй взрослый <span class="dim">— если нужен доступ в Mojo или ему можно звонить</span></h3>')
P.append('<div class="row">' + f('Фамилия и имя', True) + '</div>')
P.append('<div class="row">' + f('E-mail для Mojo') + f('Телефон') + '</div>')
P.append(q('Кто он ребёнку?', opts(WHO)))
P.append(q('Нужен доступ в Mojo ещё кому-то?', L(2), 'По одному человеку в строке: имя и фамилия, почта, кто ребёнку.'))

P.append('''<div class="box"><div class="t">Согласие на сведения о здоровье</div>
<div class="d2">Я родитель или законный представитель ребёнка и разрешаю школе собрать и использовать сведения о его здоровье и особенностях: прививки, хронические состояния, лекарства, аллергии и непереносимости, занятия со специалистами, трудности в учёбе. Это нужно для безопасности ребёнка и поддержки в учёбе. Согласие можно отозвать в любой момент — письмом на team@kindervilleschool.com.</div>
<div class="row">''' + f('Фамилия и имя родителя') + f('Подпись') + '</div></div>')
P.append('<h2 class="pb">Здоровье</h2>')
P.append(q('Какие прививки ребёнку делали?', vacc))
P.append(q('Прививки отмечены по сертификату или по памяти?', opts(['по прививочному сертификату', 'по памяти'], other=False)))
P.append(q('Есть ли аллергия или непереносимость?',
           opts(['нет', 'да, на еду', 'да, на другое: лекарства, укусы, пыльца', 'да, и на еду, и на другое'])))
P.append(q('Если да: на что, как проявляется и что делать при реакции? Если ребёнок носит лекарство с собой — какое.', L(2)))
P.append(q('Что школе нужно знать о здоровье ребёнка?', opts(['ничего'], other=False) + L(2),
           'Например: хронические состояния, лекарства, что делать при приступе, ограничения по нагрузке и бассейну, зрение, слух.'))
P.append(q('С кем ребёнок занимается или занимался вне школы?',
           opts(['логопед / дефектолог', 'психолог', 'нейропсихолог', 'невролог', 'репетитор', 'кружки и секции', 'нет']),
           'Документы не нужны.'))
P.append(q('Репетитор — по какому предмету? Кружки и секции — какие?', L(2)))

P.append('<h2>Учёба до нас</h2>')
P.append(q('Где ребёнок учился до нас?', opts(['в одной школе', 'в двух и больше', 'дистанционно', 'в школу ещё не ходил'])))
P.append(q('Как называлась школа или сад?', L(1), 'Если несколько — все.'))
P.append(q('По какой программе учился?', opts(['российская', 'международная на английском', 'в школу ещё не ходил'])))
P.append(q('Как ребёнок себя чувствовал в прошлой школе или саду?',
           opts(['скорее хорошо', 'ровно', 'скорее тяжело', 'по-разному', 'не ходил'])))
P.append(q('Английский у ребёнка сейчас — что ближе?',
           opts(['почти не знает: отдельные слова, может быть, алфавит',
                 'учил, но сам говорит мало, в основном заученными фразами',
                 'может объясниться сам: ответит о себе, попросит, поймёт педагога без перевода',
                 'учился на английском или говорит на нём дома', 'не знаю'], col=True),
           'Нужно, чтобы предварительно подобрать группу по английскому. Когда педагог лучше поймёт уровень ребёнка, группу могут поменять. '
           'Тестирование не проводим: в стрессе оно почти бесполезно.'))
P.append(q('Как ребёнок читает по-русски?',
           opts(['пока не читает', 'читает по слогам',
                 'читает словами, но медленно: к концу предложения теряет смысл',
                 'сам читает небольшой текст и может сказать, о чём он',
                 'читает бегло, понимает прочитанное — может ответить на вопросы или пересказать',
                 'читает бегло, сам берёт книги'], other=False, col=True)))
P.append(q('Какой курс математики был в предыдущей школе?', opts(['Школа России', 'Петерсон', 'Cambridge', 'не знаю'])))
P.append(q('Что куратору стоит знать о ребёнке?', L(4),
           'Что легко, что трудно, что помогает, когда расстроен. Например: «тихий, первые две недели будет присматриваться», «есть сложности в математике».'))

P.append('<h2>Напоследок</h2>')
P.append(q('Что вас беспокоит перед первым днём — и что мы можем сделать?', L(3)))

P.append('''<div class="foot"><b>Как мы храним ответы.</b> Ответы читают руководитель начальной школы и куратор. Отдельные сведения видят те, кому они нужны по делу: педагог английского — про язык, кухня и педсостав — имя, продукт и что делать при реакции. Также данные могут быть предоставлены врачу и тайскому регулятору по официальному запросу.<br>
Отвечая на вопросы анкеты, вы как родитель или законный представитель разрешаете школе Kinderville Nova (KNIS, Чалонг, Пхукет) обработать эти сведения о себе и о ребёнке: подготовить встречу с куратором, а если ребёнок придёт к нам — и его первые недели в классе: подобрать группу английского, открыть доступ в Mojo, дозвониться до вас в учебное время и спланировать поддержку ребёнку, если она понадобится.</div>''')

CSS = '''
@page{size:A4;margin:12mm 15mm 11mm}
*{box-sizing:border-box}
body{font-family:Arial,Helvetica,sans-serif;font-size:10.5pt;color:#222;margin:0;line-height:1.35;background:#fff}
.sheet{max-width:180mm;margin:0 auto}
@media screen{body{background:#f1f3f2}.sheet{background:#fff;padding:14mm 15mm;margin:16px auto;box-shadow:0 1px 6px rgba(0,0,0,.12)}
 .bar{max-width:180mm;margin:16px auto 0;display:flex;gap:10px;align-items:center;padding:0 4px;font-size:10pt;color:#555;flex-wrap:wrap}
 .bar a,.bar button{background:#1C7066;color:#fff;border:0;border-radius:16px;padding:6px 16px;font-size:10pt;text-decoration:none;cursor:pointer}
 .bar a.sec{background:none;color:#1C7066;padding:6px 4px}}
@media screen and (max-width:700px){.sheet{padding:16px;margin:10px 0}.bar{padding:0 16px}}
@media print{.bar{display:none} h2.pb{page-break-before:always;margin-top:0}}
h1{font-size:14pt;margin:0 0 4px;color:#1C7066} h1 .yr{color:#222;font-weight:normal}
.hdr{margin:0 0 6px;padding:0 0 8px;border-bottom:2px solid #1C7066}
.small{font-size:9pt;color:#444;margin:0 0 6px}
h2{font-size:11pt;color:#1C7066;border-bottom:1px solid #CFE0DD;padding-bottom:2px;margin:10px 0 4px;page-break-after:avoid}
h3{font-size:10.5pt;margin:9px 0 2px;page-break-after:avoid} .dim{color:#777;font-weight:normal;font-size:9.5pt}
.q{margin:6px 0 0;page-break-inside:avoid} .t{font-weight:bold}
.d,.d2{color:#777;font-size:9pt;margin:1px 0 2px} .d2{color:#444;margin:3px 0 4px}
.l{border-bottom:1px solid #9A9A9A;height:6.4mm}
.row{display:flex;gap:6mm;flex-wrap:wrap;margin-top:1px;page-break-inside:avoid}
.f{display:flex;align-items:flex-end;flex:1 1 40mm;min-height:8mm;gap:2mm} .f.w{flex-basis:100%}
.f span{color:#444;font-size:9.5pt;white-space:nowrap;padding-bottom:1px} .f u{flex:1;border-bottom:1px solid #9A9A9A;text-decoration:none;min-width:20mm}
.opts{margin:3px 0 1px;line-height:1.6} .opts.col{line-height:1.35}
.o{display:inline-block;white-space:nowrap;margin-right:6mm} .opts.col .o{display:block;white-space:normal;margin:0 0 .6mm;padding-left:5.6mm;text-indent:-5.6mm}
.o.oth{display:block} .o.oth u{display:inline-block;width:110mm;border-bottom:1px solid #9A9A9A;height:4mm;text-decoration:none;vertical-align:baseline} 
.cb{display:inline-block;width:3.6mm;height:3.6mm;border:1px solid #444;border-radius:.5mm;margin-right:2mm;vertical-align:-.6mm;text-indent:0}
table.v{border-collapse:collapse;margin:4px 0 2px;width:100%;max-width:150mm} table.v th{font-weight:normal;color:#444;font-size:9.5pt;padding:1px 6px;width:19mm}
table.v td{border-bottom:1px solid #ECECEC;padding:2px 6px 2px 0} table.v td.c{text-align:center} table.v .cb{margin:0}
.box{border:1px solid #CFCFCF;background:#F7F7F5;padding:7px 11px 9px;margin:16px 0 4px;page-break-inside:avoid}
.foot{color:#777;font-size:8pt;margin-top:9px;line-height:1.3;border-top:1px solid #CFE0DD;padding-top:6px;page-break-inside:avoid}
'''
page = f'''<!DOCTYPE html><html lang="ru"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex"><title>Анкета поступающего — для встречи с куратором</title><style>{CSS}</style></head><body>
<div class="bar"><a href="anketa-dlya-vstrechi.pdf">Скачать PDF</a><button onclick="window.print()">Напечатать</button><a class="sec" href="../#/ankety">← Анкеты поступающих</a></div>
<div class="sheet">{"".join(P)}</div></body></html>'''
out = H / 'anketa-dlya-vstrechi.html'
out.write_text(page, encoding='utf-8')
subprocess.run(['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', '--headless=new', '--disable-gpu', '--no-pdf-header-footer',
                f'--print-to-pdf={H/"anketa-dlya-vstrechi.pdf"}', out.as_uri()], check=True, capture_output=True)
print('ok')
