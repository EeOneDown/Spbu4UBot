# Consts
test_token = "test_token"
release_token = "release_token"
my_id = 200466757
ks_id = 71591548
url = 'http://timetable.spbu.ru'
main_answer = 'Главное меню\n\n\U00002139 - информация о боте\n\U00002B50 - оценить бота/обратная связь\n\U00002699 - настройки\n\U0001F689 - электрички\n\U0001F4DD - редактор расписания'

cookies = {'_gat': '1', '_ga': 'GA1.2.76615387.1488377623', '_culture': 'ru'}
users = {}

full_info_answer = 'ИНФОРМАЦИЯ\n\n*Раздел "Расписание"*\n\U00002022 Информация о расписании берется с *официального сайта расписания СПбГУ* - http://timetable.spbu.ru\n\U00002022 Информация о паре формируется следующим образом:\n    Время\n    Тип - Название пары\n    Адрес1 (преподаватель1);\n    Адрес2 (преподаватель2);\n    и т.д.\n\U00002022 В любой день расписание смотрится по *текущей* неделе до ВОСКРЕСЕНЬЯ. В воскресенье расписание будет показано для следующей недели.\n\U00002022 _Если занятие отменено, бот его не пришлет._\n\U00002022 📅 позволит посмотреть расписание на любой день недели. После выбора дня бот пришлет расписание для *текущей* недели, а также предложит посмотреть расписание для следующей.\n\U00002022 В этом же разделе можно _подписаться на рассылку_ расписания -\U000023F0. Рассылка производится каждый день в 21:00. О выходных днях бот не уведомляет.\n\n' +\
              '*Раздел "⚙"*\n\U00002022 Можно вызвать командой /settings.\n\U00002022 Во время _смены группы_ можно воспользоваться командой *Назад* для отмены и возврата в _Главное меню_.\n\U00002022 В *шаблонах* можно быстро переключаться между сохраненными группами.\n\U00002022 Кнопка _Сохранить_ позволяет сохранить текущую группу как шаблон.\n\U00002022 Кнопка _Удалить_ позволяет удалить любую группу из сохраненных.\n\U00002022 Для тех, кто использует _редактор расписания_, будет полезна еще одна кнопка "\U0001F4DD\U00002753", которая позволит _оставить_ или _убрать_ скрытые пары при переключении группы через *шаблоны*.\n\U00002022 Если ты решишь прекратить пользоваться ботом, пожалуйста, *заверши работу* с ним (для этого необходим написать /exit или выбрать _“Завершить работу с ботом”_ в меню настроек. _Просто удалить диалог недостаточно_). Боту очень тяжело всех помнить, и ты, решив больше не использовать его, таким образом облегчишь ему работу (а мне - аренду хостинга\U0001F609)\n\n' +\
              '*Раздел "⭐"*\n\U00002022 _Следующее твое сообщение_ после вызова этой команды _будет записано_, и разработчик его обязательно прочитает и ответит, если это будет вопрос.\n\n' +\
              '*Раздел "\U0001F4DD"*\n\U00002022 Для того, чтобы _скрыть занятие_, необходимо:\n   1. Выбрать день, когда есть это занятие;\n   2. Выбрать нужное занятие;\n   3. Определиться со временем, когда скрывать занятие.\n\U00002022 Занятие можно _скрыть_:\n   1. В определенное время в определенный день недели (например, есть две пары английского в субботу, первая и вторая. Этим вариантом можно скрыть, допустим, только первую);\n   2. В любое время в определенный день недели (то есть весь английский в этот день);\n   3. В любой день (весь свой английский абсолютно 😈).\n_P.S. Любые совпадения случайны, английский выбран как предмет, который есть почти у всех._\n\U00002022 _Вернуть_ можно как определенное занятие, так и все отмененные.\n\U00002022 Для того, чтобы не запутаться в отмененных занятиях, перед каждым названием добавлен id.\n\U00002022 В настройках адреса:\n   _Полный_ - отображаться будет адрес целиком, как на сайте (Университетский просп., д. 35, корп. Д, 204Д)\n   _Аудитория_ - отображаться будет только аудитория (204Д)\n\n' +\
              '*Раздел "\U0001F689"*\n\U00002022 Данные предоставлены сервисом [Яндекс.Расписания](http://rasp.yandex.ru/).\n\U00002022 В меню доступно два направления: *из Университета* и *в Университет*.\n\U00002022 После выбора направления будет показана информация по *3 ближайшим* электричкам, а именно: _Через сколько отправление, Время отправления и Время прибытия_\n\U00002022 После этого есть возможность просмотра *всех оставшихся* на сегодня электричек.\n\U00002022 Также бот предоставит возможность *выбрать* начальную или конечную станцию при просмотре электричек в Университет или из него, соответственно.\n\U00002022 Если по выбранному маршруту на сегодня *электричек нет*, то бот пришлет расписание *первых 5* электричек на завтра.'
# _Сообщение от разработчика_\n"Спасибо, что пользуетесь этим ботом, мне очень приятно😊\nВ скором времени появится больше новых функций - я постоянно улучшаю бот(даже если вы этого не замечаете😉)."
briefly_info_answer = 'КРАТКАЯ ИНФОРМАЦИЯ\n\n*Раздел "Расписание"*\nЗдесь ты можешь _узнать расписание_ на любой день, а также _подписаться на рассылку_.\n\n' +\
                      '*Раздел "⚙"*\nЗдесь ты можешь _сменить группу_, воспользоваться _шаблонами_ или _завершить работу_ с ботом.\n\n' +\
                      '*Раздел "⭐"*\nЗдесь ты можешь _оценить бота_ или _отправить сообщение_ разработчику.\n\n' +\
                      '*Раздел "\U0001F4DD"*\nЗдесь ты можешь _скрыть_ или _вернуть занятие_ в расписании, а также настроить _отображение адреса_.\n\n' +\
                      '*Раздел "\U0001F689"*\nЗдесь ты можешь посмотреть _электрички_ от или до Университета.'

spb = 'c2'
len_prosp = 's9603435'
ligovo = 's9603837'
sosn_pol = 's9603431'
univer = 's9603770'
oran = 's9603138'
leb = 's9602688'
kalische = 's9602687'
star_petergof = 's9603547'

days = {'Пн': 'понедельник', 'Вт': 'вторник', 'Ср': 'среда', 'Чт': 'четверг', 'Пт': 'пятница', 'Сб': 'суббота'}
stations = {'Санкт-Петербург': spb, 'Ленинский Проспект': len_prosp, 'Лигово': ligovo, 'Сосновая Поляна': sosn_pol,
            'Университет': univer}
naprs_sub = {'Калище': kalische, 'Санкт-Петербург': spb, 'Ораниенбаум-1': oran, 'Лебяжье': leb, 'Университет': univer}
all_stations = {'Санкт-Петербург': spb, 'Ленинский Проспект': len_prosp, 'Лигово': ligovo, 'Сосновая Поляна': sosn_pol,
                'Университет': univer, 'Ораниенбаум-1': oran, 'Лебяжье': leb, 'Калище': kalische,
                'Старый Петергоф': star_petergof}
all_stations_const = ['Санкт-Петербург', 'Ленинский Проспект', 'Лигово', 'Сосновая Поляна', 'Старый Петергоф',
                      'Университет', 'Ораниенбаум-1', 'Лебяжье', 'Калище']


# функция для поиска расписания с сайта
# возвращает расписание на один день
def daily_tt(url, day):
    from bs4 import BeautifulSoup
    import sqlite3
    bot_db = sqlite3.connect('Bot_db')
    cursor = bot_db.cursor()
    cursor.execute("SELECT soup FROM groups_tt WHERE url = ?", (url,))
    try:
        request = cursor.fetchone()[0]
    except TypeError:
        import requests
        request = requests.get(url, cookies=cookies).text
    cursor.close()
    bot_db.close()
    soup = BeautifulSoup(request, "lxml")
    table = soup.find('div', class_="panel-group")
    days = table.find_all('div', class_="panel panel-default")
    n = 0
    lessons = []
    for day_table in days:  # поиск нужного дня
        date = day_table.find('h4').text
        if type(day) == int:
            if date.split()[1] != str(day):
                n += 1
                continue
            break
        else:
            if date.split(',')[0].strip() != day:
                n += 1
                continue
            break
    if n == len(days):
        timetable = {'weekday': 'Выходной'}
    else:
        for lesson in days[n].find_all('li'):  # для всех пар в нужном дне
            if lesson.get('title') == 'Занятие отменено':
                continue
            else:
                spans = lesson.find_all('span')  # берется вся инфа про пары - список
                if str(lesson.find('tbody')) == 'None':
                    if len(spans) == 6 or len(spans) == 7:
                        lessons.append({'time': spans[0].text.strip(),
                                        'name': spans[1].text.strip(),
                                        'place': spans[2].text.strip(),
                                        'teacher': spans[5].text.strip()})
                    else:
                        lessons.append({'time': spans[0].text.strip(),
                                        'name': spans[1].text.strip(),
                                        'place': '',
                                        'teacher': ''})
                else:
                    hidden_info = lesson.find('tbody')
                    hidden_places = []
                    hidden_teachers = []
                    for hidden_str in hidden_info.find_all('tr'):
                        hidden_places.append(hidden_str.find('span').text.strip())
                        hidden_teachers.append(';'.join([teacher.text.strip() for teacher in hidden_str.find_all('a')]))
                    lessons.append({'time': spans[0].text.strip(),
                                    'name': spans[1].text.strip(),
                                    'place': '//'.join(hidden_places),
                                    'teacher': '//'.join(hidden_teachers)})
        timetable = {'weekday': days[n].find('h4').text.strip(),
                     'lessons': lessons}
    return timetable


# собираем нормальное сообщение из набора пар
def create_answer(info_for_message, user_id, personal=True, next_week=False):
    import sqlite3
    answer = ''
    if info_for_message.get('weekday').split(',')[0] == 'Выходной':
        answer += '\U0001F634 Выходной'
    elif len(info_for_message.get('lessons')) == 0:
        answer += '\U0001F634 Выходной\n\nВ этот день все занятия отменили'
    else:
        if next_week:
            answer += info_for_message.get('weekday').split(',')[1] + ' => '
        answer += '📅 ' + info_for_message.get('weekday').split(',')[0].upper() + '\n\n'
        if personal:
            bot_db = sqlite3.connect('Bot_db')
            cursor = bot_db.cursor()
            cursor.execute(
                "SELECT l.name, l.type, l.day, l.time FROM skips AS s JOIN lessons AS l ON l.id = s.lesson_id WHERE user_id = ?", (
                    user_id,))
            skips = cursor.fetchall()
            cursor.close()
            bot_db.close()
        else:
            skips = []
        for lesson in info_for_message.get('lessons'):
            flag = False
            for skip in skips:
                if skip[0] == lesson.get('name').split(',')[0] and skip[1] == lesson.get('name').split(',')[
                    1].strip() and (skip[2] == info_for_message.get('weekday').split(',')[0] or skip[2] == 'all') and (
                        skip[3] == lesson.get('time') or skip[3] == 'all'):
                    flag = True
                    break
            if flag:
                continue
            answer += '🕒 ' + lesson.get('time') + '\n'
            try:
                if lesson.get('name').split(',')[1].strip() == 'лекция':
                    answer += '*Л - '
                elif lesson.get('name').split(',')[1].strip() == 'практическое занятие':
                    answer += '*ПР - '
                elif lesson.get('name').split(',')[1].strip() == 'лабораторная работа':
                    answer += '*ЛР - '
                else:
                    answer += '*' + lesson.get('name').split(',')[1].strip().upper() + ' - '
            except IndexError:
                answer += '*'
            answer += lesson.get('name').split(',')[0] + '*\n'
            places = lesson.get('place')
            teachers = lesson.get('teacher')
            for i in range(len(places.split('//'))):
                if i > 0 and places.split('//')[i] == places.split('//')[i - 1] and teachers.split('//')[i] == \
                        teachers.split('//')[i - 1]:
                    continue
                for teacher in teachers.split('//')[i].split(';'):
                    if is_full_place(user_id):
                        answer += places.split('//')[i].strip()
                    else:
                        answer += places.split('//')[i].split(',')[-1].strip()
                    if len(teacher.split(',')[0].strip()) > 0:
                        answer += ' (' + teacher.split(',')[0].strip() + ')'
                    else:
                        answer += ''
                    if teacher != teachers.split('//')[i].split(';')[-1]:
                        answer += ';\n'
                if places.split('//')[i].strip() != places.split('//')[-1].strip():
                    answer += ';\n'
            answer += '\n'
            answer += '\n'
    return answer


# получаем url для пользователя из бд
def get_url(user_id):
    import sqlite3
    bot_db = sqlite3.connect('Bot_db')
    cursor = bot_db.cursor()
    cursor.execute("SELECT url FROM users WHERE id = ?", (user_id,))
    url = cursor.fetchone()[0]
    cursor.close()
    bot_db.close()

    return url


# получаем необходимость полного адреса
def is_full_place(user_id):
    import sqlite3
    bot_db = sqlite3.connect('Bot_db')
    cursor = bot_db.cursor()
    cursor.execute("SELECT full_place FROM users WHERE id = ?", (user_id,))
    is_full_place = cursor.fetchone()[0]
    cursor.close()
    bot_db.close()

    return is_full_place


def get_group(user_id):
    from bs4 import BeautifulSoup
    import sqlite3
    bot_db = sqlite3.connect('Bot_db')
    cursor = bot_db.cursor()
    cursor.execute("SELECT url FROM users WHERE id = ?", (user_id,))
    url = cursor.fetchone()[0]
    cursor.execute("SELECT soup FROM groups_tt WHERE url = ?", (url,))
    request = cursor.fetchone()[0]
    cursor.close()
    bot_db.close()
    soup = BeautifulSoup(request, "lxml")
    group = soup.find('h2').text. split(' ')[1]
    return 'Твоя группа: <b>{0}</b>\n'.format(group)


def get_groups_name(user_id):
    from bs4 import BeautifulSoup
    import sqlite3
    groups = {}
    bot_db = sqlite3.connect('Bot_db')
    cursor = bot_db.cursor()
    cursor.execute("SELECT group_id FROM groups_with_users WHERE user_id = ?", (user_id,))
    ids = cursor.fetchall()
    for id in ids:
        cursor.execute("SELECT soup FROM groups_tt WHERE id = ?", (id[0],))
        request = cursor.fetchone()[0]
        soup = BeautifulSoup(request, "lxml")
        groups[soup.find('h2').text.split(' ')[1]] = id[0]
    cursor.close()
    bot_db.close()
    return groups


def is_skips(user_id):
    import sqlite3
    bot_db = sqlite3.connect('Bot_db')
    cursor = bot_db.cursor()
    cursor.execute("SELECT count(*) FROM skips WHERE user_id = ?", (user_id,))
    returning = cursor.fetchone()[0]
    cursor.close()
    bot_db.close()
    return returning


def get_interim_attestation_answer(data, user_id, only_exams=True):
    import sqlite3
    from bs4 import BeautifulSoup
    info_about_lesson = ''
    answer = ''
    bot_db = sqlite3.connect('Bot_db')
    cursor = bot_db.cursor()
    cursor.execute("SELECT interim_attestation FROM groups_tt WHERE url = ?", (get_url(user_id),))
    ia_soup = BeautifulSoup(cursor.fetchone()[0], "lxml")
    cursor.close()
    bot_db.close()
    months = ia_soup.find_all('div', class_="panel panel-default")
    n = 0
    for month_table in months:  # поиск нужного дня
        month = month_table.find('h4').text.strip()
        if month != data:
            n += 1
            continue
        break
    for lesson in months[n].find_all('li'):
        datetime = lesson.find('div', class_="col-sm-2 studyevent-datetime").text.strip()
        info_about_lesson = '📅 ' + datetime.split(' ')[0] + ' ' + datetime.split(' ')[1] + '\n'
        info_about_lesson += '🕒 ' + datetime.split(' ')[2] + '\n'
        lesson_name = lesson.find('div', class_="col-sm-4 studyevent-subject").text.strip()
        if only_exams and ('комиссия' in lesson_name or 'пересдача' in lesson_name or 'консультация групповая' in lesson_name):
            continue
        info_about_lesson += '<b>' + ', '.join(lesson_name.split(', ')[1:]).upper() + ' - ' + lesson_name.split(', ')[0] + \
                             '</b>\n'
        if lesson.find('div', class_="studyevent-location-educator-modal hidden"):
            hidden_info = lesson.find('tbody')
            hidden_places = []
            hidden_teachers = []
            for hidden_str in hidden_info.find_all('tr'):
                hidden_places.append(hidden_str.find('span').text.strip())
                hidden_teachers.append(';'.join([teacher.text.strip() for teacher in hidden_str.find_all('a')]))
            places = '//'.join(hidden_places)
            teachers = '//'.join(hidden_teachers)
        else:
            places = lesson.find('div', class_="col-sm-3 studyevent-locations").text.strip()
            teachers = lesson.find('div', class_="col-sm-3 studyevent-educators").text.strip()
        for i in range(len(places.split('//'))):
            if i > 0 and places.split('//')[i] == places.split('//')[i - 1] and teachers.split('//')[i] == \
                    teachers.split('//')[i - 1]:
                continue
            for teacher in teachers.split('//')[i].split(';'):
                if is_full_place(user_id):
                    info_about_lesson += places.split('//')[i].strip()
                else:
                    info_about_lesson += places.split('//')[i].split(',')[-1].strip()
                if len(teacher.split(',')[0].strip()) > 0:
                    info_about_lesson += ' (' + teacher.split(',')[0].strip() + ')'
                else:
                    info_about_lesson += ''
                if teacher != teachers.split('//')[i].split(';')[-1]:
                    info_about_lesson += ';\n'
            if places.split('//')[i].strip() != places.split('//')[-1].strip():
                info_about_lesson += ';\n'
        answer += info_about_lesson + '\n\n'
    return answer


def set_next_step(step, user_id):
    import sqlite3
    bot_db = sqlite3.connect('Bot_db')
    cursor = bot_db.cursor()
    cursor.execute("UPDATE users SET step = ? WHERE id = ?", (step, user_id))
    bot_db.commit()
    cursor.close()
    bot_db.close()

# лог бота
def log(message, answer):
    from datetime import datetime
    print('\n------------')
    print(datetime.now())
    print("Сообщение от {0} {1}. id = {2}\nТекст - {3}".format(message.from_user.first_name,
                                                               message.from_user.last_name,
                                                               str(message.from_user.id),
                                                               message.text))
    print('Ответ - ' + answer)
    print('------------\n')
