# -*- coding: utf-8 -*-


import flask
import telebot
import logging
from flask_sslify import SSLify
from constants import release_token, my_id, url, cookies, users, main_answer, full_info_answer, briefly_info_answer, \
    get_group, spb, univer, days, all_stations, all_stations_const, get_interim_attestation_answer, set_next_step, ks_id
import time


main_keyboard = telebot.types.ReplyKeyboardMarkup(True)
if time.localtime().tm_mon in [12, 1, 5, 6]:
    main_keyboard.row('СЕССИЯ', 'Расписание')
else:
    main_keyboard.row('Расписание')
main_keyboard.row(u'\U00002139', u'\U00002B50', u'\U00002699', u'\U0001F689', u'\U0001F4DD')

# BOT
API_TOKEN = release_token

WEBHOOK_HOST = 'eeonedown.pythonanywhere.com'
WEBHOOK_PORT = 443  # 443, 80, 88 or 8443 (port need to be 'open')

WEBHOOK_URL_BASE = "https://{0}:{1}".format(WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/{0}/".format(API_TOKEN)


logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

bot = telebot.TeleBot(API_TOKEN, threaded=False)
app = flask.Flask(__name__)
sslify = SSLify(app)


# # Empty webserver index, return nothing, just http 200
# @app.route('/SetWebhook', methods=['GET', 'HEAD'])
# def SetWebhook():
#     bot.remove_webhook()
#     bot.set_webhook(url=WEBHOOK_URL_BASE+WEBHOOK_URL_PATH)

#     bot.send_message(200466757, 'Webhook перезапущен')

#     page = '<a href="/">Home</a>'

#     return page, 200


# @app.route('/remove_webhook', methods=['GET', 'HEAD'])
# def removeWebhook():
#     bot.remove_webhook()

#     bot.send_message(200466757, 'Webhook убран')

#     page = '<a href="/">Home</a>'

#     return page, 200


@app.route('/', methods=['GET', 'HEAD'])
def main_page():

    page = '<a href="https://t.me/Spbu4UBot">@SPbU4U</a>'

    return page, 200

# Process webhook calls
@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        try:
            # from time import time
            # tic = time()
            bot.process_new_updates([update])
            # bot.send_message(my_id, str(time() - tic), disable_notification=True)
        except Exception as e:
            bot.reply_to(update.message, 'Я тебя не понял, повтори, пожалуйста.\nЕсли же проблема повторяется не первый раз, можешь обратиться к <a href="https://vk.com/write74088921">разработчику</a>.', parse_mode='HTML', disable_web_page_preview=True)
            bot.forward_message(my_id, update.message.chat.id, update.message.message_id)
            bot.send_message(my_id, str(e), disable_notification=True)
            print(str(e))
        return 'ok', 200
    else:
        flask.abort(403)


# -------------------------------------------------------------------
# -------------------------------------------------------------------
# Bot ---------------------------------------------------------------
# -------------------------------------------------------------------
# -------------------------------------------------------------------


# Начало работы
@bot.message_handler(commands=['start'])
def handle_start(message):
    import requests
    from bs4 import BeautifulSoup
    import sqlite3
    bot.send_chat_action(message.from_user.id, 'typing')
    soup = BeautifulSoup(requests.get(url, cookies=cookies).text, "lxml")
    naprs_html = soup.find('div', class_="panel panel-default").find_all('a')
    naprs = [napr.text for napr in naprs_html]
    napr_keyboard = telebot.types.ReplyKeyboardMarkup(True, False)
    for napr in naprs:
        if napr == 'Свободные искусства и науки' or napr == 'Юриспруденция основное расписание':
            continue
        napr_keyboard.row(napr)
    answer = ''
    if message.text == '/start':
        answer += 'Приветствую!\n'
    bot_db = sqlite3.connect('Bot_db')
    cursor = bot_db.cursor()
    try:
        cursor.execute("INSERT INTO users (id, url, step) VALUES (?, ?, ?)", (message.from_user.id, url, 'select_napr'))
        bot_db.commit()
    except sqlite3.IntegrityError:
        bot_db.rollback()
    try:
        cursor.execute("INSERT INTO users_info_choice (user_id) VALUES (?)", (message.from_user.id, ))
        bot_db.commit()
        cursor.close()
        bot_db.close()
    except sqlite3.IntegrityError:
        bot_db.rollback()
        cursor.execute("UPDATE users_info_choice SET soup_stages = NULL, napr = NULL, soup_programs = NULL, stage = NULL, soup_years = NULL, program = NULL, soup_groups = NULL, year = NULL, link = NULL, group_name = NULL WHERE user_id = ?",
                       (message.from_user.id,))
        bot_db.commit()
        cursor.close()
        bot_db.close()
    answer += 'Выбери свое направление'
    bot.send_message(message.from_user.id, answer, reply_markup=napr_keyboard)
    set_next_step('select_napr', message.from_user.id)


def select_napr(message):
    if message.text == '/start' or message.text == '/settings' or message.text == '/exit':
        return
    elif message.text == 'Назад':
        answer = get_group(message.from_user.id) + main_answer
        bot.send_message(message.from_user.id, answer, reply_markup=main_keyboard, parse_mode='HTML')
        set_next_step('handle_main_menu', message.from_user.id)
        return
    import requests
    from bs4 import BeautifulSoup
    bot.send_chat_action(message.from_user.id, 'typing')
    soup = BeautifulSoup(requests.get(url, cookies=cookies).text, "lxml")
    naprs_html = soup.find('div', class_="panel panel-default").find_all('a')
    naprs = [napr.text for napr in naprs_html]
    links = [link.get('href') for link in naprs_html]
    try:
        i = naprs.index(message.text)
    except ValueError:
        i = -1
        print(i)
    if i != -1:
        import sqlite3
        url2 = url + links[i]
        soup = BeautifulSoup(requests.get(url2, cookies=cookies).text, "lxml")
        bot_db = sqlite3.connect('Bot_db')
        cursor = bot_db.cursor()
        cursor.execute("UPDATE users_info_choice SET soup_stages = ?, napr = ? WHERE user_id = ?",
                       (str(soup), message.text, message.from_user.id))
        bot_db.commit()
        cursor.close()
        bot_db.close()
        stages_html = soup.find_all('div', class_="panel-heading")
        stages = [stage.text.strip() for stage in stages_html]
        stage_keyboard = telebot.types.ReplyKeyboardMarkup(True, False)
        for stage in stages:
            stage_keyboard.row(stage)
        stage_keyboard.row('Другое направление')
        bot.send_message(message.from_user.id, 'Ты выбрал: <b>{0}</b>\nВыбери степень'.format(message.text),
                         reply_markup=stage_keyboard, parse_mode='HTML')
        set_next_step('select_stage', message.from_user.id)
    else:
        bot.send_message(message.from_user.id, 'Пожалуйста, выбери свое направление')
        set_next_step('select_napr', message.from_user.id)


def select_stage(message):
    if message.text == '/start' or message.text == '/settings' or message.text == '/exit':
        return
    elif message.text == 'Назад':
        answer = get_group(message.from_user.id) + main_answer
        bot.send_message(message.from_user.id, answer, reply_markup=main_keyboard, parse_mode='HTML')
        set_next_step('handle_main_menu', message.from_user.id)
        return
    import sqlite3
    from bs4 import BeautifulSoup
    bot.send_chat_action(message.from_user.id, 'typing')
    bot_db = sqlite3.connect('Bot_db')
    cursor = bot_db.cursor()
    cursor.execute("SELECT soup_stages FROM users_info_choice WHERE user_id = ?", (message.from_user.id,))
    soup = BeautifulSoup(cursor.fetchone()[0], "lxml")
    cursor.close()
    bot_db.close()
    stages_html = soup.find_all('div', class_="panel-heading")
    stages = [stage.text.strip() for stage in stages_html]
    programs_html = soup.find_all('ul')
    try:
        i = stages.index(message.text)
    except ValueError:
        i = -1
    if i != -1:
        programs = programs_html[i].find_all('div', class_="col-sm-6")[2:]
        bot_db = sqlite3.connect('Bot_db')
        cursor = bot_db.cursor()
        cursor.execute("UPDATE users_info_choice SET soup_programs = ?, stage = ? WHERE user_id = ?",
                       (str(programs_html[i]), message.text, message.from_user.id))
        bot_db.commit()
        cursor.close()
        bot_db.close()
        program_keyboard = telebot.types.ReplyKeyboardMarkup(True, False)
        for program in programs:
            program_keyboard.row(program.text.strip())
        program_keyboard.row('Другая степень')
        bot.send_message(message.from_user.id, 'Ты выбрал: <b>{0}</b>\nВыбери программу'.format(message.text),
                         reply_markup=program_keyboard, parse_mode='HTML')
        set_next_step('select_program', message.from_user.id)
    elif message.text == 'Другое направление':
        handle_start(message)
        return
    else:
        bot.send_message(message.from_user.id, 'Пожалуйста, выбери степень')
        set_next_step('select_stage', message.from_user.id)


def select_program(message):
    if message.text == '/start' or message.text == '/settings' or message.text == '/exit':
        return
    elif message.text == 'Назад':
        answer = get_group(message.from_user.id) + main_answer
        bot.send_message(message.from_user.id, answer, reply_markup=main_keyboard, parse_mode='HTML')
        set_next_step('handle_main_menu', message.from_user.id)
        return
    bot.send_chat_action(message.from_user.id, 'typing')
    import sqlite3
    from bs4 import BeautifulSoup
    bot_db = sqlite3.connect('Bot_db')
    cursor = bot_db.cursor()
    cursor.execute("SELECT soup_programs FROM users_info_choice WHERE user_id = ?", (message.from_user.id,))
    soup = BeautifulSoup(cursor.fetchone()[0], "lxml")
    cursor.close()
    bot_db.close()
    programs_html = soup.find_all('li')
    programs = [program.text.strip() for program in soup.find_all('div', class_="col-sm-6")[2:]]
    try:
        i = programs.index(message.text)
    except ValueError:
        i = -1
    if i != -1:
        bot_db = sqlite3.connect('Bot_db')
        cursor = bot_db.cursor()
        cursor.execute("UPDATE users_info_choice SET soup_years = ?, program = ? WHERE user_id = ?",
                       (" //OTHER// ".join(
                           [str(prog) for prog in programs_html[i + 1].find_all('div', class_="col-sm-1")]),
                        message.text,
                        message.from_user.id))
        bot_db.commit()
        cursor.close()
        bot_db.close()
        years = [year.text.strip() for year in programs_html[i + 1].find_all('div', class_="col-sm-1")]
        years_keyboard = telebot.types.ReplyKeyboardMarkup(True, False)
        for year in years:
            years_keyboard.row(year)
        years_keyboard.row('Другая программа')
        bot.send_message(message.from_user.id, 'Ты выбрал: <b>{0}</b>\nУкажи год поступления'.format(message.text),
                         reply_markup=years_keyboard,
                         parse_mode='HTML')
        set_next_step('select_year', message.from_user.id)
    elif message.text == 'Другая степень':
        set_next_step('select_napr', message.from_user.id)
        bot_db = sqlite3.connect('Bot_db')
        cursor = bot_db.cursor()
        cursor.execute("SELECT napr FROM users_info_choice WHERE user_id = ?", (message.from_user.id,))
        message.text = cursor.fetchone()[0]
        cursor.execute(
            "UPDATE users_info_choice SET soup_stages = NULL, napr = NULL, soup_programs = NULL, stage = NULL, soup_years = NULL, program = NULL, soup_groups = NULL, year = NULL, link = NULL, group_name = NULL WHERE user_id = ?",
            (message.from_user.id,))
        bot_db.commit()
        cursor.close()
        bot_db.close()
        select_napr(message)
        return
    else:
        bot.send_message(message.from_user.id, 'Пожалуйста, выбери программу')
        set_next_step('select_program', message.from_user.id)


def select_year(message):
    if message.text == '/start' or message.text == '/settings' or message.text == '/exit':
        return
    elif message.text == 'Назад':
        answer = get_group(message.from_user.id) + main_answer
        bot.send_message(message.from_user.id, answer, reply_markup=main_keyboard, parse_mode='HTML')
        set_next_step('handle_main_menu', message.from_user.id)
        return
    bot.send_chat_action(message.from_user.id, 'typing')
    import sqlite3
    from bs4 import BeautifulSoup
    bot_db = sqlite3.connect('Bot_db')
    cursor = bot_db.cursor()
    cursor.execute("SELECT soup_years FROM users_info_choice WHERE user_id = ?", (message.from_user.id,))
    years_html = [BeautifulSoup(i, "lxml") for i in cursor.fetchone()[0].split(" //OTHER// ")]
    cursor.close()
    bot_db.close()
    years = [year.find('a').text for year in years_html]
    links = [link.find('a').get('href') for link in years_html]
    try:
        i = years.index(message.text)
    except ValueError:
        i = -1
    if i != -1:
        import requests
        from bs4 import BeautifulSoup
        group_url = url + links[i]
        soup = BeautifulSoup(requests.get(group_url, cookies=cookies).text, "lxml")
        groups_html = soup.find('ul')
        bot_db = sqlite3.connect('Bot_db')
        cursor = bot_db.cursor()
        cursor.execute("UPDATE users_info_choice SET soup_groups = ?, year = ? WHERE user_id = ?",
                       (str(groups_html), message.text, message.from_user.id))
        bot_db.commit()
        cursor.close()
        bot_db.close()
        groups = [group.text.strip() for group in groups_html.find_all('div', class_="col-sm-4")]
        groups_keyboard = telebot.types.ReplyKeyboardMarkup(True, False)
        for group in groups:
            groups_keyboard.row(group)
        groups_keyboard.row('Другой год')
        bot.send_message(message.from_user.id, 'Ты выбрал: <b>{0}</b>\nОсталось выбрать группу'.format(message.text),
                         reply_markup=groups_keyboard, parse_mode='HTML')
        set_next_step('select_group', message.from_user.id)
    elif message.text == 'Другая программа':
        set_next_step('select_stage', message.from_user.id)
        bot_db = sqlite3.connect('Bot_db')
        cursor = bot_db.cursor()
        cursor.execute("SELECT stage FROM users_info_choice WHERE user_id = ?", (message.from_user.id,))
        message.text = cursor.fetchone()[0]
        cursor.execute(
            "UPDATE users_info_choice SET soup_programs = NULL, stage = NULL, soup_years = NULL, program = NULL, soup_groups = NULL, year = NULL, link = NULL, group_name = NULL WHERE user_id = ?",
            (message.from_user.id,))
        bot_db.commit()
        cursor.close()
        bot_db.close()
        select_stage(message)
        return
    else:
        bot.send_message(message.from_user.id, 'Пожалуйста, выбери год поступления')
        set_next_step('select_year', message.from_user.id)


def select_group(message):
    if message.text == '/start' or message.text == '/settings' or message.text == '/exit':
        return
    elif message.text == 'Назад':
        answer = get_group(message.from_user.id) + main_answer
        bot.send_message(message.from_user.id, answer, reply_markup=main_keyboard, parse_mode='HTML')
        set_next_step('handle_main_menu', message.from_user.id)
        return
    bot.send_chat_action(message.from_user.id, 'typing')
    import sqlite3
    from bs4 import BeautifulSoup
    bot_db = sqlite3.connect('Bot_db')
    cursor = bot_db.cursor()
    cursor.execute("SELECT soup_groups FROM users_info_choice WHERE user_id = ?", (message.from_user.id,))
    soup = BeautifulSoup(cursor.fetchone()[0], "lxml")
    cursor.close()
    bot_db.close()
    links_html = soup.find_all('div', class_="tile")
    links = [onclick.get('onclick').split('=')[1][1:-1] for onclick in links_html]
    groups = [group.text.strip() for group in soup.find_all('div', class_="col-sm-4")]
    try:
        i = groups.index(message.text)
    except ValueError:
        i = -1
    if i != -1:
        user_link = url + links[i]
        bot_db = sqlite3.connect('Bot_db')
        cursor = bot_db.cursor()
        cursor.execute("UPDATE users_info_choice SET link = ?, group_name = ? WHERE user_id = ?",
                       (str(user_link), message.text, message.from_user.id))
        bot_db.commit()
        cursor.execute("SELECT napr, stage, program, year, group_name FROM users_info_choice WHERE user_id = ?",
                       (message.from_user.id,))
        choice = cursor.fetchone()
        cursor.close()
        bot_db.close()
        answer = 'Твой выбор: <b>' + '</b> => <b>'.join(choice) + '</b>\nВсе верно?'
        choice_keyboard = telebot.types.ReplyKeyboardMarkup(True, False)
        choice_keyboard.row('Все верно')
        choice_keyboard.row('Другая группа')
        choice_keyboard.row('Другой год')
        choice_keyboard.row('Другая программа')
        choice_keyboard.row('Другая степень')
        choice_keyboard.row('Другое направление')
        bot.send_message(message.from_user.id, answer, reply_markup=choice_keyboard, parse_mode='HTML')
        set_next_step('confirm_choice', message.from_user.id)
    elif message.text == 'Другой год':
        set_next_step('select_program', message.from_user.id)
        bot_db = sqlite3.connect('Bot_db')
        cursor = bot_db.cursor()
        cursor.execute("SELECT program FROM users_info_choice WHERE user_id = ?", (message.from_user.id,))
        message.text = cursor.fetchone()[0]
        cursor.execute(
            "UPDATE users_info_choice SET soup_years = NULL, program = NULL, soup_groups = NULL, year = NULL, link = NULL, group_name = NULL WHERE user_id = ?",
            (message.from_user.id,))
        bot_db.commit()
        cursor.close()
        bot_db.close()
        select_program(message)
        return
    else:
        bot.send_message(message.from_user.id, 'Пожалуйста, выбери группу')
        set_next_step('select_group', message.from_user.id)


def confirm_choice(message):
    if message.text == '/start' or message.text == '/settings' or message.text == '/exit':
        return
    elif message.text == 'Назад':
        answer = get_group(message.from_user.id) + main_answer
        bot.send_message(message.from_user.id, answer, reply_markup=main_keyboard, parse_mode='HTML')
        set_next_step('handle_main_menu', message.from_user.id)
        return
    elif message.text == 'Все верно':
        bot.send_chat_action(message.from_user.id, 'typing')
        import sqlite3
        bot_db = sqlite3.connect('Bot_db')
        cursor = bot_db.cursor()
        cursor.execute("SELECT link, group_name FROM users_info_choice WHERE user_id = ?", (message.from_user.id,))
        info = cursor.fetchone()
        user_link, group_name = info[0], info[1]
        cursor.execute("DELETE FROM users WHERE id = ? AND url = ?", (message.from_user.id, url))
        cursor.execute("DELETE FROM users_info_choice WHERE user_id = ?", (message.from_user.id,))
        bot_db.commit()
        flag_new_user = False
        try:
            cursor.execute(
                "INSERT INTO users(id, url) VALUES (?, ?)", (message.from_user.id, user_link))
            flag_new_user = True
            bot_db.commit()
        except sqlite3.IntegrityError:
            bot_db.rollback()
            cursor.execute("DELETE FROM skips WHERE user_id = ?", (message.from_user.id,))
            bot_db.commit()
            cursor.execute("UPDATE users SET full_place = 1, url = ? WHERE id = ?", (
                user_link, message.from_user.id))
            bot_db.commit()
        import requests
        request = requests.get(user_link, cookies=cookies).text
        try:
            cursor.execute("INSERT INTO groups_tt (url, soup) VALUES (?, ?)",
                           (user_link,
                            request))
            bot_db.commit()
        except sqlite3.IntegrityError:
            import requests
            bot_db.rollback()
            cursor.execute("UPDATE groups_tt SET soup = ? WHERE url = ?",
                           (request,
                            user_link))
            bot_db.commit()
        from bs4 import BeautifulSoup
        cursor.execute("SELECT id FROM groups_tt WHERE url = ?", (user_link,))
        group_id = cursor.fetchone()[0]
        soup = BeautifulSoup(request, "lxml")
        att_url = soup.find('a', text=u'пром. аттестация').get('href')
        ia_soup = requests.get('http://timetable.spbu.ru' + att_url, cookies=cookies).text
        cursor.execute("UPDATE groups_tt SET interim_attestation = ? WHERE id = ?", (ia_soup, group_id))
        bot_db.commit()
        cursor.close()
        bot_db.close()
        if flag_new_user:
            answer = u'Поздравляю! Теперь ты с нами, {0}\n\nДля завершения работы с ботом необходимо воспользоваться командой /exit или найти соответствующий раздел в _настройках_(⚙)\nКоманда *Назад* является универсальной и может быть написана в любое время для возврата в _Главное меню_'.format(
                message.from_user.first_name)
            bot.send_message(message.from_user.id,
                             answer,
                             parse_mode='Markdown')
            handle_help(message)
            bot.send_message(my_id,
                             'Новый юзер:\n*id*: {0}\n*Имя:* {1} {2}\n*Группа*: {3}'.format(str(message.from_user.id),
                                                                                            message.from_user.first_name,
                                                                                            message.from_user.last_name,
                                                                                            group_name),
                             parse_mode='Markdown')
            bot.send_message(ks_id,
                             'Новый юзер:\n*id*: {0}\n*Имя:* {1} {2}\n*Группа*: {3}'.format(str(message.from_user.id),
                                                                                            message.from_user.first_name,
                                                                                            message.from_user.last_name,
                                                                                            group_name),
                             parse_mode='Markdown')
        bot.send_message(message.from_user.id,
                         'Твоя группа: <b>{0}</b>\n'.format(group_name) + main_answer,
                         reply_markup=main_keyboard,
                         parse_mode='HTML')
        set_next_step('handle_main_menu', message.from_user.id)
    elif message.text == 'Другая группа':
        set_next_step('select_year', message.from_user.id)
        import sqlite3
        bot_db = sqlite3.connect('Bot_db')
        cursor = bot_db.cursor()
        cursor.execute("SELECT year FROM users_info_choice WHERE user_id = ?", (message.from_user.id,))
        message.text = cursor.fetchone()[0]
        cursor.execute(
            "UPDATE users_info_choice SET soup_groups = NULL, year = NULL, link = NULL, group_name = NULL WHERE user_id = ?",
            (message.from_user.id,))
        bot_db.commit()
        cursor.close()
        bot_db.close()
        select_year(message)
        return
    elif message.text == 'Другой год':
        set_next_step('select_group', message.from_user.id)
        select_group(message)
        return
    elif message.text == 'Другая программа':
        set_next_step('select_year', message.from_user.id)
        select_year(message)
        return
    elif message.text == 'Другая степень':
        set_next_step('select_program', message.from_user.id)
        select_program(message)
        return
    elif message.text == 'Другое направление':
        set_next_step('select_stage', message.from_user.id)
        select_stage(message)
        return
    else:
        bot.send_message(message.from_user.id, 'Пожалуйста, подтверди выбор')
        set_next_step('confirm_choice', message.from_user.id)


# выход
@bot.message_handler(commands=['exit'])
def handle_exit(message):
    import sqlite3
    bot_db = sqlite3.connect('Bot_db')
    cursor = bot_db.cursor()
    cursor.execute("DELETE FROM skips WHERE user_id = ?", (message.from_user.id,))
    cursor.execute("DELETE FROM groups_with_users WHERE user_id = ?", (message.from_user.id,))
    cursor.execute("DELETE FROM users WHERE id = ?", (message.from_user.id,))
    bot_db.commit()
    cursor.close()
    bot_db.close()
    answer = 'Прощай, {0}\U0001F44B\U0001F3FB\nТы всегда можешь вернуться, и мы начнем все заново :)'.format(
        message.from_user.first_name)
    exit_keyboard = telebot.types.ReplyKeyboardRemove(True)
    bot.send_message(message.from_user.id, answer, reply_markup=exit_keyboard)


# настройки бота
@bot.message_handler(commands=['settings'])
def handle_settings(message):
    try:
        from constants import get_url
        get_url(message.from_user.id)
    except TypeError:
        bot.send_message(message.from_user.id, 'Мы стобой еще не знакомы. Давай я начну')
        handle_start(message)
        return
    settings_keyboard = telebot.types.ReplyKeyboardMarkup(True, False)
    settings_keyboard.row('Сменить группу', 'Шаблоны')
    settings_keyboard.row('Завершить работу с ботом')
    settings_keyboard.row('Назад')
    bot.send_message(message.from_user.id,
                     'Настройки',
                     reply_markup=settings_keyboard)
    set_next_step('settings', message.from_user.id)


def settings(message):
    if message.text == '/start' or message.text == '/settings' or message.text == '/exit':
        return
    elif message.text == 'Сменить группу':
        handle_start(message)
        return
    elif message.text == 'Назад':
        answer = get_group(message.from_user.id) + main_answer
        bot.send_message(message.from_user.id, answer, reply_markup=main_keyboard, parse_mode='HTML')
        set_next_step('handle_main_menu', message.from_user.id)
        return
    elif message.text == 'Завершить работу с ботом':
        handle_exit(message)
        return
    elif message.text == 'Шаблоны':
        from constants import get_groups_name
        groups = get_groups_name(message.from_user.id)
        templates_keyboard = telebot.types.ReplyKeyboardMarkup(True, False)
        if len(groups) != 0:
            for key in groups.keys():
                templates_keyboard.row(key)
            answer = 'Выбери группу для быстрого переключения\n'
        else:
            answer = 'У тебя еще нет шаблонов, но ты можешь сохранить текущую группу\n'
        answer += get_group(message.from_user.id)
        templates_keyboard.row('Удалить', 'Сохранить', '\U0001F4DD\U00002753')
        templates_keyboard.row('Назад в \U00002699')
        bot.send_message(message.from_user.id, answer, reply_markup=templates_keyboard, parse_mode='HTML')
        set_next_step('templates', message.from_user.id)


# Шаблоны
def templates(message):
    if message.text == '/start' or message.text == '/settings' or message.text == '/exit':
        return
    elif message.text == 'Назад':
        answer = get_group(message.from_user.id) + main_answer
        bot.send_message(message.from_user.id, answer, reply_markup=main_keyboard, parse_mode='HTML')
        set_next_step('handle_main_menu', message.from_user.id)
        return
    from constants import get_groups_name
    groups = get_groups_name(message.from_user.id)
    if message.text == 'Назад в \U00002699':
        handle_settings(message)
        return
    elif message.text == 'Сохранить':
        from constants import get_url, get_groups_name
        import sqlite3
        templates_keyboard = telebot.types.ReplyKeyboardMarkup(True, False)
        bot_db = sqlite3.connect('Bot_db')
        cursor = bot_db.cursor()
        cursor.execute("SELECT id FROM groups_tt WHERE url = ?", (get_url(message.from_user.id),))
        now_group_id = cursor.fetchone()[0]
        try:
            cursor.execute("INSERT INTO groups_with_users (group_id, user_id) VALUES (?, ?)",
                           (now_group_id, message.from_user.id))
            bot_db.commit()
            answer = 'Сохранил'
            groups = get_groups_name(message.from_user.id)
            for key in groups.keys():
                templates_keyboard.row(key)
            templates_keyboard.row('Удалить', 'Сохранить', '\U0001F4DD\U00002753')
            templates_keyboard.row('Назад в \U00002699')
        except sqlite3.IntegrityError:
            bot_db.rollback()
            answer = 'Уже сохранено'
        cursor.close()
        bot_db.close()
        bot.send_message(message.from_user.id, answer, reply_markup=templates_keyboard)
    elif message.text == 'Удалить':
        if len(groups) == 0:
            bot.send_message(message.from_user.id, 'Нечего удалять')
        else:
            groups_keyboard = telebot.types.ReplyKeyboardMarkup(True, False)
            for key in groups.keys():
                groups_keyboard.row(key)
            groups_keyboard.row('Отмена')
            answer = 'Выбери группу, которую хочешь удалить из шаблонов\n'
            answer += get_group(message.from_user.id)
            bot.send_message(message.from_user.id, answer, reply_markup=groups_keyboard, parse_mode='HTML')
            set_next_step('delete_template', message.from_user.id)
    elif message.text == '\U0001F4DD\U00002753':
        inline_skips = telebot.types.InlineKeyboardMarkup()
        inline_skips.row(*[telebot.types.InlineKeyboardButton(text=name, callback_data=name) for
                           name in ['Оставлять', 'Обнулять']])
        answer = 'Мне оставлять твои настройки <i>редактора расписания</i> после переключения группы?\nЧерез <i>смениь группу</i> все обнулится'
        bot.send_message(message.from_user.id, answer, reply_markup=inline_skips, parse_mode='HTML')
    elif message.text in groups:
        import sqlite3
        bot_db = sqlite3.connect('Bot_db')
        cursor = bot_db.cursor()
        cursor.execute("SELECT url FROM groups_tt WHERE id = ?", (groups[message.text],))
        new_url = cursor.fetchone()[0]
        cursor.execute("SELECT delete_skips FROM users WHERE id = ?", (message.from_user.id,))
        is_delete_skips = cursor.fetchone()[0]
        if is_delete_skips:
            cursor.execute("DELETE FROM skips WHERE user_id = ?", (message.from_user.id,))
            cursor.execute("UPDATE users SET full_place = 1, url = ? WHERE id = ?", (new_url, message.from_user.id))
        else:
            cursor.execute("UPDATE users SET url = ? WHERE id = ?", (new_url, message.from_user.id))
        bot_db.commit()
        cursor.close()
        bot_db.close()
        answer = get_group(message.from_user.id) + main_answer
        bot.send_message(message.from_user.id, answer, parse_mode='HTML', reply_markup=main_keyboard)
        set_next_step('handle_main_menu', message.from_user.id)


def delete_template(message):
    if message.text == '/start' or message.text == '/settings' or message.text == '/exit':
        return
    from constants import get_groups_name
    groups = get_groups_name(message.from_user.id)
    if message.text == 'Отмена':
        set_next_step('settings', message.from_user.id)
        message.text = 'Шаблоны'
        settings(message)
        return
    elif message.text in groups:
        import sqlite3
        bot_db = sqlite3.connect('Bot_db')
        cursor = bot_db.cursor()
        cursor.execute("DELETE FROM groups_with_users WHERE group_id = ?", (groups[message.text],))
        bot_db.commit()
        cursor.close()
        bot_db.close()
        answer = 'Удалил <b>' + message.text + '</b>\n'
        from constants import get_groups_name
        groups = get_groups_name(message.from_user.id)
        templates_keyboard = telebot.types.ReplyKeyboardMarkup(True, False)
        if len(groups) != 0:
            for key in groups.keys():
                templates_keyboard.row(key)
            answer += 'Выбери группу для быстрого переключения\n'
        else:
            answer += 'Теперь у тебя нет шаблонов, но ты можешь сохранить текущую группу\n'
        answer += get_group(message.from_user.id)
        templates_keyboard.row('Удалить', 'Сохранить', '\U0001F4DD\U00002753')
        templates_keyboard.row('Назад в \U00002699')
        bot.send_message(message.from_user.id, answer, reply_markup=templates_keyboard, parse_mode='HTML')
        set_next_step('templates', message.from_user.id)


def tt_editor(message):
    if message.text == '/start' or message.text == '/settings' or message.text == '/exit':
        return
    user_id = message.from_user.id
    if message.text == 'Адрес':
        inline_place = telebot.types.InlineKeyboardMarkup()
        inline_place.row(*[telebot.types.InlineKeyboardButton(text=name, callback_data=name) for
                           name in ['Полный', 'Аудитория']])
        answer = 'В каком формате отображать адрес?'
        bot.send_message(user_id, answer, reply_markup=inline_place)
    elif message.text == 'Скрыть занятие' or message.text == 'Другой день' or message.text == 'Отмена':
        d_l_day_keyboard = telebot.types.ReplyKeyboardMarkup(True, False)
        d_l_day_keyboard.row('Понедельник')
        d_l_day_keyboard.row('Вторник')
        d_l_day_keyboard.row('Среда')
        d_l_day_keyboard.row('Четверг')
        d_l_day_keyboard.row('Пятница')
        d_l_day_keyboard.row('Суббота')
        d_l_day_keyboard.row(u'Назад в \U0001F4DD')
        bot.send_message(user_id, 'Выбери день, когда есть это занятие', reply_markup=d_l_day_keyboard)
        set_next_step('delete_lesson_day', message.from_user.id)
    elif message.text == 'Вернуть':
        import sqlite3
        bot_db = sqlite3.connect('Bot_db')
        cursor = bot_db.cursor()
        cursor.execute(
            "SELECT s.lesson_id, l.name, l.type, l.day, l.time FROM skips AS s JOIN lessons AS l ON l.id = s.lesson_id WHERE user_id = ?",
            (
                message.from_user.id,))
        lessons = cursor.fetchall()
        cursor.close()
        bot_db.close()
        if len(lessons) > 0:
            users[message.from_user.id] = []
            lessons_list_keyboard = telebot.types.ReplyKeyboardMarkup(True, False)
            lesson_answer = 'Вот список скрытых тобой занятий:\n\n'
            for lesson in lessons:
                users[message.from_user.id].append(str(lesson[0]))
                lesson_answer += '*id:* {0}\n*Название:* {1}\n*Тип:* {2}\n*День:* {3}\n*Время:* {4}\n\n'.format(
                    str(lesson[0]),
                    lesson[1],
                    lesson[2], lesson[3],
                    lesson[4])
                lessons_list_keyboard.row(str(lesson[0]) + ' - ' + lesson[1])
            lessons_list_keyboard.row('Вернуть все')
            lessons_list_keyboard.row(u'Назад в \U0001F4DD')
            bot.send_message(user_id, lesson_answer, reply_markup=lessons_list_keyboard, parse_mode='Markdown')
            bot.send_message(user_id, 'Выберу то, которое хочешь вернуть')
            set_next_step('return_lesson', message.from_user.id)
        else:
            bot.send_message(user_id, 'Скрытых занятий нет')
            set_next_step('tt_editor', user_id)
    elif message.text == 'Назад':
        answer = get_group(message.from_user.id) + main_answer
        bot.send_message(user_id, answer, reply_markup=main_keyboard, parse_mode='HTML')
        set_next_step('handle_main_menu', user_id)


def delete_lesson_day(message):
    if message.text == '/start' or message.text == '/settings' or message.text == '/exit':
        return
    elif message.text == u'Назад в \U0001F4DD':
        tt_editor_keyboard = telebot.types.ReplyKeyboardMarkup(True, False)
        tt_editor_keyboard.row('Скрыть занятие')
        tt_editor_keyboard.row('Назад', 'Адрес', 'Вернуть')
        answer = 'Редактор расписания'
        bot.send_message(message.from_user.id,
                         answer,
                         reply_markup=tt_editor_keyboard)
        set_next_step('tt_editor', message.from_user.id)
        return
    elif message.text == 'Назад':
        answer = get_group(message.from_user.id) + main_answer
        bot.send_message(message.from_user.id, answer, reply_markup=main_keyboard, parse_mode='HTML')
        set_next_step('handle_main_menu', message.from_user.id)
        return
    try:
        from constants import get_url, daily_tt, create_answer
        user_id = message.from_user.id
        user_url = get_url(user_id)
        info_for_message = daily_tt(user_url, message.text.lower())
        d_l_lesson_keyboard = telebot.types.ReplyKeyboardMarkup(True, False)
        for lesson in info_for_message.get('lessons'):
            d_l_lesson_keyboard.row(lesson.get('name'))
        d_l_lesson_keyboard.row(u'Назад в \U0001F4DD', 'Другой день')
        answer = create_answer(info_for_message, user_id, personal=False)
        users[message.from_user.id] = info_for_message
        bot.send_message(user_id, 'Вот полное расписание:\n\n' + answer, parse_mode='Markdown',
                         reply_markup=d_l_lesson_keyboard)
        bot.send_message(user_id, 'Выбери пару')
        set_next_step('delete_lesson_name', user_id)
    except TypeError:
        set_next_step('delete_lesson_day', message.from_user.id)
        return


def delete_lesson_name(message):
    if message.text == '/start' or message.text == '/settings' or message.text == '/exit':
        return
    elif message.text == u'Назад в \U0001F4DD':
        tt_editor_keyboard = telebot.types.ReplyKeyboardMarkup(True, False)
        tt_editor_keyboard.row('Скрыть занятие')
        tt_editor_keyboard.row('Назад', 'Адрес', 'Вернуть')
        answer = 'Редактор расписания'
        bot.send_message(message.from_user.id,
                         answer,
                         reply_markup=tt_editor_keyboard)
        set_next_step('tt_editor', message.from_user.id)
        return
    elif message.text == 'Назад':
        answer = get_group(message.from_user.id) + main_answer
        bot.send_message(message.from_user.id, answer, reply_markup=main_keyboard, parse_mode='HTML')
        set_next_step('handle_main_menu', message.from_user.id)
        return
    user_id = message.from_user.id
    if message.text == 'Другой день':
        set_next_step('tt_editor', message.from_user.id)
        tt_editor(message)
        return
    else:
        lessons = users[message.from_user.id].get('lessons')
        try:
            [lesson.get('name') for lesson in lessons].index(message.text)
        except ValueError:
            return
        users[message.from_user.id] = [users[message.from_user.id].get('weekday').split(', ')[0]]
        for lesson in lessons:
            if lesson.get('name') == message.text:
                users[message.from_user.id].append(lesson)
        d_l_data_keyboard = telebot.types.ReplyKeyboardMarkup(True, False)
        day = users[message.from_user.id][0].split(',')[0]
        if day == 'понедельник' or day == 'вторник' or day == 'четверг':
            day += 'а'
        day += 'м'
        d_l_data_keyboard.row('Только по ' + day)
        d_l_data_keyboard.row('Отмена', 'Всегда')
        bot.send_message(user_id, 'Когда мне скрывать пару?', reply_markup=d_l_data_keyboard)
        set_next_step('delete_lesson_data', user_id)


def delete_lesson_data(message):
    if message.text == '/start' or message.text == '/settings' or message.text == '/exit':
        return
    elif message.text == 'Отмена':
        set_next_step('tt_editor', message.from_user.id)
        tt_editor(message)
        return
    elif message.text == 'Назад':
        answer = get_group(message.from_user.id) + main_answer
        bot.send_message(message.from_user.id, answer, reply_markup=main_keyboard, parse_mode='HTML')
        set_next_step('handle_main_menu', message.from_user.id)
        return
    elif message.text == 'Всегда':
        import sqlite3
        bot_db = sqlite3.connect('Bot_db')
        cursor = bot_db.cursor()
        try:
            cursor.execute("INSERT INTO lessons (name, type) VALUES (?, ?)", (
                users[message.from_user.id][1].get('name').split(',')[0],
                users[message.from_user.id][1].get('name').split(',')[1].strip()))
            cursor.execute(
                "SELECT id FROM lessons WHERE name = ? AND type = ? AND day = 'all' AND time = 'all'", (
                    users[message.from_user.id][1].get('name').split(',')[0],
                    users[message.from_user.id][1].get('name').split(',')[1].strip()))
            lesson_id = cursor.fetchone()[0]
        except sqlite3.IntegrityError:
            bot_db.rollback()
            cursor.execute(
                "SELECT id FROM lessons WHERE name = ? AND type = ? AND day = 'all' AND time = 'all'", (
                    users[message.from_user.id][1].get('name').split(',')[0],
                    users[message.from_user.id][1].get('name').split(',')[1].strip()))
            lesson_id = cursor.fetchone()[0]
            bot_db.commit()
        try:
            cursor.execute("INSERT INTO skips VALUES (?, ?)", (message.from_user.id, lesson_id))
            bot_db.commit()
            cursor.close()
        except sqlite3.IntegrityError:
            bot_db.rollback()
            cursor.close()
        bot_db.close()

        answer = get_group(message.from_user.id) + main_answer
        bot.send_message(message.from_user.id, 'Больше я её не буду показывать')
        bot.send_message(message.from_user.id, answer, reply_markup=main_keyboard, parse_mode='HTML')
        set_next_step('handle_main_menu', message.from_user.id)
    elif message.text.find(users[message.from_user.id][0].split(',')[0]) != -1:
        d_l_time_keyboard = telebot.types.ReplyKeyboardMarkup(True, False)
        for lesson in users[message.from_user.id][1:]:
            d_l_time_keyboard.row(lesson.get('time'))
        d_l_time_keyboard.row('Отмена', 'В любое время')
        bot.send_message(message.from_user.id, 'В какое время ты не хочешь ее видеть в этот день?',
                         reply_markup=d_l_time_keyboard)
        set_next_step('delete_lesson_time', message.from_user.id)
    else:
        return


def delete_lesson_time(message):
    if message.text == '/start' or message.text == '/settings' or message.text == '/exit':
        return
    elif message.text == 'Отмена':
        set_next_step('tt_editor', message.from_user.id)
        tt_editor(message)
        return
    elif message.text == 'Назад':
        answer = get_group(message.from_user.id) + main_answer
        bot.send_message(message.from_user.id, answer, reply_markup=main_keyboard, parse_mode='HTML')
        set_next_step('handle_main_menu', message.from_user.id)
        return
    import sqlite3
    bot_db = sqlite3.connect('Bot_db')
    cursor = bot_db.cursor()
    if message.text == 'В любое время':
        try:
            cursor.execute("INSERT INTO lessons (name, type, day) VALUES (?, ?, ?)", (
                users[message.from_user.id][1].get('name').split(',')[0],
                users[message.from_user.id][1].get('name').split(',')[1].strip(),
                users[message.from_user.id][0]))
            cursor.execute("SELECT id FROM lessons WHERE name = ? AND type = ? AND day = ? AND time = 'all'", (
                users[message.from_user.id][1].get('name').split(',')[0],
                users[message.from_user.id][1].get('name').split(',')[1].strip(),
                users[message.from_user.id][0]))
            bot_db.commit()
        except sqlite3.IntegrityError:
            bot_db.rollback()
            cursor.execute(
                "SELECT id FROM lessons WHERE name = ? AND type = ? AND day = ? AND time = 'all'", (
                    users[message.from_user.id][1].get('name').split(',')[0],
                    users[message.from_user.id][1].get('name').split(',')[1].strip(),
                    users[message.from_user.id][0]))
    else:
        try:
            [lesson.get('time') for lesson in users[message.from_user.id][1:]].index(message.text)
        except ValueError:
            return
        try:
            cursor.execute("INSERT INTO lessons (name, type, day, time) VALUES (?, ?, ?, ?)", (
                users[message.from_user.id][1].get('name').split(',')[0],
                users[message.from_user.id][1].get('name').split(',')[1].strip(),
                users[message.from_user.id][0],
                message.text))
            cursor.execute("SELECT id FROM lessons WHERE name = ? AND type = ? AND day = ? AND time = ?", (
                users[message.from_user.id][1].get('name').split(',')[0],
                users[message.from_user.id][1].get('name').split(',')[1].strip(),
                users[message.from_user.id][0],
                message.text))
            bot_db.commit()
        except sqlite3.IntegrityError:
            bot_db.rollback()
            cursor.execute("SELECT id FROM lessons WHERE name = ? AND type = ? AND day = ? AND time = ?", (
                users[message.from_user.id][1].get('name').split(',')[0],
                users[message.from_user.id][1].get('name').split(',')[1].strip(),
                users[message.from_user.id][0],
                message.text))
    lesson_id = cursor.fetchone()[0]
    try:
        cursor.execute("INSERT INTO skips VALUES (?, ?)", (message.from_user.id, lesson_id))
        bot_db.commit()
        cursor.close()
    except sqlite3.IntegrityError:
        bot_db.rollback()
        cursor.close()
    bot_db.close()
    answer = get_group(message.from_user.id) + main_answer
    bot.send_message(message.from_user.id, 'Больше я её не буду показывать')
    bot.send_message(message.from_user.id, answer, reply_markup=main_keyboard, parse_mode='HTML')
    set_next_step('handle_main_menu', message.from_user.id)


def return_lesson(message):
    if message.text == '/start' or message.text == '/settings' or message.text == '/exit':
        return
    elif message.text == u'Назад в \U0001F4DD':
        tt_editor_keyboard = telebot.types.ReplyKeyboardMarkup(True, False)
        tt_editor_keyboard.row('Скрыть занятие')
        tt_editor_keyboard.row('Назад', 'Адрес', 'Вернуть')
        answer = 'Редактор расписания'
        bot.send_message(message.from_user.id,
                         answer,
                         reply_markup=tt_editor_keyboard)
        set_next_step('tt_editor', message.from_user.id)
        return
    elif message.text == 'Назад':
        answer = get_group(message.from_user.id) + main_answer
        bot.send_message(message.from_user.id, answer, reply_markup=main_keyboard, parse_mode='HTML')
        set_next_step('handle_main_menu', message.from_user.id)
        return
    import sqlite3
    bot_db = sqlite3.connect('Bot_db')
    cursor = bot_db.cursor()
    if message.text == 'Вернуть все':
        cursor.execute("DELETE FROM skips WHERE user_id = ?", (message.from_user.id,))
        bot_db.commit()
        cursor.close()
        bot_db.close()
        bot.send_message(message.from_user.id, 'Ок, я все вернул')
    else:
        cursor.execute("SELECT lesson_id FROM skips WHERE user_id = ?", (message.from_user.id,))
        lessons_id = [l_id[0] for l_id in cursor.fetchall()]
        if int(message.text.split(' - ')[0]) in lessons_id:
            cursor.execute("DELETE FROM skips WHERE user_id = ? AND lesson_id = ?", (
                message.from_user.id, message.text[0]))
            bot_db.commit()
            cursor.close()
            bot_db.close()
            bot.send_message(message.from_user.id, 'Эту пару я вернул в расписание')
        else:
            return
    answer = get_group(message.from_user.id) + main_answer
    bot.send_message(message.from_user.id, answer, reply_markup=main_keyboard, parse_mode='HTML')
    set_next_step('handle_main_menu', message.from_user.id)


# инфо бота
@bot.message_handler(commands=['help'])
def handle_help(message):
    inline_keyboard = telebot.types.InlineKeyboardMarkup()
    inline_keyboard.row(*[telebot.types.InlineKeyboardButton(text=name, callback_data=name) for
                          name in ['Полное ИНФО']])
    answer = briefly_info_answer
    bot.send_message(message.from_user.id, answer, parse_mode='Markdown', reply_markup=inline_keyboard,
                     disable_web_page_preview=True)


# отзывы
def rate(message):
    if message.text == '/start' or message.text == '/settings' or message.text == '/exit':
        return
    if message.text != 'Назад':
        bot.forward_message(my_id, message.chat.id, message.message_id)
        bot.forward_message(ks_id, message.chat.id, message.message_id)
        bot.send_message(my_id, 'user_id: {0}\nmessage_id: {1}'.format(message.from_user.id, message.message_id))
        answer = 'Записал'
        bot.send_message(message.from_user.id, answer)
    answer = get_group(message.from_user.id) + main_answer
    bot.send_message(message.from_user.id, answer, reply_markup=main_keyboard, parse_mode='HTML')
    set_next_step('handle_main_menu', message.from_user.id)


commands = ['\U0001F689', 'Расписание', 'Назад', u'\U00002699', u'\U00002B50', u'\U00002139', u'\U0001F4DD', 'Users',
            'Ответ', 'СЕССИЯ', 'Сессия', 'сессия']


# Реакция на текстовое сообщение
@bot.message_handler(content_types=['text'])
def select_step(message):
    import sqlite3
    bot_db = sqlite3.connect('Bot_db')
    cursor = bot_db.cursor()
    cursor.execute("SELECT step FROM users WHERE id = ?", (message.from_user.id,))
    step = cursor.fetchone()[0]
    cursor.close()
    bot_db.close()
    # bot.send_message(message.from_user.id, step)
    # bot.send_message(message.from_user.id, message.text)
    if step == 'handle_main_menu':
        handle_main_menu(message)
    elif step == 'time_table':
        time_table(message)
    elif step == 'suburban':
        suburban(message)
    elif step == 'rate':
        rate(message)
    elif step == 'tt_editor':
        tt_editor(message)
    elif step == 'settings':
        settings(message)
    elif step == 'feed_back':
        feed_back(message)
    elif step == 'return_lesson':
        return_lesson(message)
    elif step == 'delete_lesson_day':
        delete_lesson_day(message)
    elif step == 'delete_lesson_name':
        delete_lesson_name(message)
    elif step == 'delete_lesson_data':
        delete_lesson_data(message)
    elif step == 'delete_lesson_time':
        delete_lesson_time(message)
    elif step == 'templates':
        templates(message)
    elif step == 'delete_template':
        delete_template(message)
    elif step == 'select_napr':
        select_napr(message)
    elif step == 'select_stage':
        select_stage(message)
    elif step == 'select_program':
        select_program(message)
    elif step == 'select_year':
        select_year(message)
    elif step == 'select_group':
        select_group(message)
    elif step == 'confirm_choice':
        confirm_choice(message)


def handle_main_menu(message):
    if message.from_user.id in users:
        users.pop(message.from_user.id)
    user_id = message.from_user.id
    try:
        from constants import get_url
        get_url(user_id)
    except TypeError:
        bot.send_message(message.from_user.id, 'Мы стобой еще не знакомы. Давай я начну')
        handle_start(message)
        return
    if message.text == 'Расписание':
        tt_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        tt_markup.row('Сегодня', 'Завтра', '📅')
        tt_markup.row('Назад', '⏰')
        answer = 'Выбери день\n\n📅 - день недели\n⏰ - рассылка'
        bot.send_message(user_id, answer, reply_markup=tt_markup)
        set_next_step('time_table', user_id)
    elif message.text == u'\U00002699':
        handle_settings(message)
        return
    elif message.text == u'\U00002B50':
        rate_keyboard = telebot.types.ReplyKeyboardMarkup(True, False)
        rate_keyboard.row(u'\U0001F44E', u'\U0001F44D')
        rate_keyboard.row('Назад')
        answer = 'Напиши мне что-нибудь'
        bot.send_message(user_id, answer, reply_markup=rate_keyboard)
        set_next_step('rate', user_id)
    elif message.text == u'\U00002139':
        handle_help(message)
        return
    elif message.text == u'\U0001F4DD':
        tt_editor_keyboard = telebot.types.ReplyKeyboardMarkup(True, False)
        #        tt_editor_keyboard.row('Преподаватель', 'Скрыть занятие')
        tt_editor_keyboard.row('Скрыть занятие')
        tt_editor_keyboard.row('Назад', 'Адрес', 'Вернуть')
        #        answer = 'Здесь ты можешь настроить отображение адреса, скрыть некоторые пары и выбрать своего преподавателя'
        answer = 'Редактор расписания'
        bot.send_message(user_id,
                         answer,
                         reply_markup=tt_editor_keyboard)
        set_next_step('tt_editor', user_id)
    elif message.text == '\U0001F689':
        suburban_keyboard = telebot.types.ReplyKeyboardMarkup(True, False)
        suburban_keyboard.row('Из Универа', 'В Универ')
        # loc_button = telebot.types.KeyboardButton(text='ads',  request_location=True)
        suburban_keyboard.row('Назад', 'Свой маршрут')
        answer = 'Электрички'
        answer += '\n\nДанные предоставлены сервисом <a href = "http://rasp.yandex.ru/">Яндекс.Расписания</a>'
        bot.send_message(user_id,
                         answer,
                         reply_markup=suburban_keyboard,
                         parse_mode='HTML')
        bot.send_message(user_id,
                         'P.S. Пиши в <i>обратную связь</i> станции, которые надо добавить.',
                         parse_mode='HTML')
        set_next_step('suburban', user_id)
    elif message.text == 'Назад':
        answer = get_group(message.from_user.id) + main_answer
        bot.send_message(user_id, answer, reply_markup=main_keyboard, parse_mode='HTML')
        set_next_step('handle_main_menu', user_id)
    elif (message.from_user.id == my_id or message.from_user.id == ks_id) and message.text == 'Users':
        import sqlite3
        bot_db = sqlite3.connect('Bot_db')
        cursor = bot_db.cursor()
        cursor.execute("SELECT count(id) FROM users WHERE url != ?", (url,))
        answer = cursor.fetchone()[0]
        cursor.close()
        bot_db.close()
        bot.send_message(message.from_user.id, 'Количество зарегистрированных пользователей: *{0}*'.format(str(answer)),
                         parse_mode='Markdown')
    elif message.from_user.id == my_id and message.text == 'Ответ':
        bot.send_message(my_id, 'user_id: \nmessage_id: \ntext')
        set_next_step('feed_back', user_id)
    elif message.text.upper() == 'СЕССИЯ':
        import sqlite3
        from bs4 import BeautifulSoup
        bot_db = sqlite3.connect('Bot_db')
        cursor = bot_db.cursor()
        cursor.execute("SELECT interim_attestation FROM groups_tt WHERE url = ?", (get_url(user_id),))
        ia_soup = BeautifulSoup(cursor.fetchone()[0], "lxml")
        cursor.close()
        bot_db.close()
        inline_keyboard = telebot.types.InlineKeyboardMarkup()
        if ia_soup.find('div', class_='alert alert-warning'):
            answer = 'Нет событий'
        else:
            try:
                table = ia_soup.find('div', class_="panel-group")
                months = table.find_all('h4')
                for month in months:
                    inline_keyboard.row(*[telebot.types.InlineKeyboardButton(text=name, callback_data=name) for
                                          name in [month.text.strip()]])
                answer = 'Выбери месяц:'
            except AttributeError:
                answer = 'Нет событий'
        bot.send_message(user_id, answer, reply_markup=inline_keyboard)
    # else:
    #     inline_keyboard = telebot.types.InlineKeyboardMarkup()
    #     inline_keyboard.row(*[telebot.types.InlineKeyboardButton(text=name, callback_data=name, url="https://vk.com/write74088921") for
    #                           name in ['Сообщение в ВК']])
    #     answer = 'Если ты считаешь, что бот не реагирует на твои команды, ты можешь его перезапустить /start.\nИли написать разработчику.'
    #     bot.send_message(user_id, answer, reply_markup=inline_keyboard)


# Ответы юзерам
def feed_back(message):
    info = message.text.split('\n')
    chat_id, reply_to_message_id, text = int(info[0].split(': ')[-1]), int(info[1].split(': ')[-1]), info[2]
    try:
        bot.send_message(chat_id=chat_id, text=text, reply_to_message_id=reply_to_message_id, parse_mode='Markdown')
        bot.send_message(my_id, 'Ответил')
        set_next_step('handle_main_menu', my_id)
    except:
        bot.send_message(my_id, 'Не ответил')
        set_next_step('handle_main_menu', my_id)


# Расписание
def time_table(message):
    user_id = message.from_user.id
    try:
        from constants import get_url
        user_url = get_url(user_id)
    except TypeError:
        bot.send_message(message.from_user.id, 'Мы стобой еще не знакомы. Давай я начну')
        handle_start(message)
        return
    if message.text == 'Сегодня':
        from constants import daily_tt, create_answer
        from datetime import datetime, timedelta
        day = (datetime.now() + timedelta(0.125)).day
        info_for_message = daily_tt(user_url, day)
        answer = create_answer(info_for_message, user_id)
        bot.send_message(user_id, answer, parse_mode='Markdown')
    elif message.text == 'Завтра':
        from constants import daily_tt, create_answer
        from datetime import datetime, timedelta
        tomorrow = (datetime.now() + timedelta(1.125)).day
        info_for_message = daily_tt(user_url, tomorrow)
        answer = create_answer(info_for_message, user_id)
        bot.send_message(user_id, answer, parse_mode='Markdown')
    elif message.text == '📅':
        inline_keyboard = telebot.types.InlineKeyboardMarkup()
        inline_keyboard.row(*[telebot.types.InlineKeyboardButton(text=name, callback_data=name) for
                              name in ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб']])
        answer = 'Выбери день недели'
        bot.send_message(user_id, answer, reply_markup=inline_keyboard)
    elif message.text == 'Назад':
        answer = get_group(message.from_user.id) + main_answer
        bot.send_message(user_id, answer, reply_markup=main_keyboard, parse_mode='HTML')
        set_next_step('handle_main_menu', user_id)
    elif message.text == '⏰':
        import sqlite3
        bot_db = sqlite3.connect('Bot_db')
        cursor = bot_db.cursor()
        cursor.execute("SELECT sending FROM users WHERE id = ?", (message.chat.id,))
        is_send = cursor.fetchone()[0]
        cursor.close()
        bot_db.close()
        inline_keyboard = telebot.types.InlineKeyboardMarkup()
        if is_send:
            inline_keyboard.row(*[telebot.types.InlineKeyboardButton(text=name, callback_data=name) for
                                  name in ['\U0000274CОтписаться']])
        else:
            inline_keyboard.row(*[telebot.types.InlineKeyboardButton(text=name, callback_data=name) for
                                  name in ['\U00002705Подписаться']])
        answer = 'Здесь ты можешь <b>подписаться</b> на рассылку расписания на следующий день или <b>отписаться</b> от неё.' + \
                 '\nРассылка производится в 21:00'
        bot.send_message(user_id, answer, reply_markup=inline_keyboard, parse_mode='HTML')


# Электрички
def suburban(message):
    user_id = message.from_user.id
    try:
        from constants import get_url
        get_url(user_id)
    except TypeError:
        bot.send_message(message.from_user.id, 'Мы стобой еще не знакомы. Давай я начну')
        handle_start(message)
        return
    directions = ['Из Универа', 'В Универ']
    if message.text in directions:
        bot_message = bot.send_message(message.from_user.id, '\U000023F3Идет запрос..')
        from get_yandex_rasp import get_suburban_rasp
        inline_keyboard = telebot.types.InlineKeyboardMarkup()
        if message.text == 'Из Универа':
            to_station, from_station = spb, univer
        else:
            to_station, from_station = univer, spb
        answer = get_suburban_rasp(from_station, to_station)
        answer, no_more = answer.split(' /=>/ ')[0], int(answer.split(' /=>/ ')[1])
        if not no_more:
            inline_keyboard.row(*[telebot.types.InlineKeyboardButton(text=name, callback_data=name) for
                                  name in ['Оставшиеся', 'Обновить']])
        else:
            inline_keyboard.row(*[telebot.types.InlineKeyboardButton(text=name, callback_data=name) for
                                  name in ['Обновить']])
        if message.text == 'Из Универа':
            inline_keyboard.row(*[telebot.types.InlineKeyboardButton(text=name, callback_data=name) for
                                  name in ['Другое направление']])
        else:
            inline_keyboard.row(*[telebot.types.InlineKeyboardButton(text=name, callback_data=name) for
                                  name in ['Другая станция']])
        bot.edit_message_text(answer, message.from_user.id,
                              parse_mode='HTML',
                              reply_markup=inline_keyboard,
                              message_id=bot_message.message_id)
    elif message.text == 'Свой маршрут':
        inline_keyboard = telebot.types.InlineKeyboardMarkup()
        for station in all_stations_const:
            inline_keyboard.row(*[telebot.types.InlineKeyboardButton(text=name, callback_data=name) for
                                name in [station]])
        bot.send_message(message.from_user.id, 'Укажи *начальную* станцию:', reply_markup=inline_keyboard,
                         parse_mode='Markdown')
    elif message.text == 'Назад':
        answer = get_group(message.from_user.id) + main_answer
        bot.send_message(user_id, answer, reply_markup=main_keyboard, parse_mode='HTML')
        set_next_step('handle_main_menu', user_id)


# Обработка inline апросов
@bot.callback_query_handler(func=lambda call_back: True)
def inline(call_back):
    from constants import get_url
    user_id = call_back.message.chat.id
    user_url = get_url(user_id)
    if call_back.data in days:
        from constants import daily_tt, create_answer
        inline_keyboard = telebot.types.InlineKeyboardMarkup()
        inline_keyboard.row(*[telebot.types.InlineKeyboardButton(text=name, callback_data=name) for
                              name in ['Следующая неделя']])
        day = days[call_back.data]
        info_for_message = daily_tt(user_url, day)
        answer = create_answer(info_for_message, user_id)
        if answer.split()[0] == '\U0001F634':
            answer = '📅 ' + days[call_back.data].upper() +'\n\n' + answer
        bot.edit_message_text(text=answer,
                              chat_id=call_back.message.chat.id,
                              message_id=call_back.message.message_id,
                              parse_mode='Markdown',
                              reply_markup=inline_keyboard)
    elif call_back.data == 'Следующая неделя':
        import requests
        from bs4 import BeautifulSoup
        from constants import daily_tt, create_answer, url
        bot.send_chat_action(user_id, 'typing')
        day = call_back.message.text.split()[1].lower()
        bot.edit_message_text(text='\U000023F3Идет запрос..',
                              chat_id=call_back.message.chat.id,
                              message_id=call_back.message.message_id,
                              parse_mode='Markdown')
        soup = BeautifulSoup(requests.get(user_url, cookies=cookies).text, "lxml")
        next_week_url = soup.find('a', class_='next-week').get('href')
        info_for_message = daily_tt(url + next_week_url, day)
        answer = create_answer(info_for_message, user_id, next_week=True)
        try:
            inline_answer, message_answer = 'Будет' + answer.split(' => ')[0], answer.split(' => ')[1]
        except IndexError:
            inline_answer, message_answer = 'Будет выходной)', answer
        bot.answer_callback_query(call_back.id, inline_answer, cache_time=1)
        bot.edit_message_text(text=message_answer,
                              chat_id=call_back.message.chat.id,
                              message_id=call_back.message.message_id,
                              parse_mode='Markdown')
    elif call_back.data == '\U0000274CОтписаться':
        import sqlite3
        bot_db = sqlite3.connect('Bot_db')
        cursor = bot_db.cursor()
        cursor.execute("UPDATE users SET sending = 0 WHERE id = ?", (call_back.message.chat.id,))
        bot_db.commit()
        cursor.close()
        bot_db.close()

        bot.edit_message_text(text='\U0001F4EAРассылка *отключена*',
                              chat_id=call_back.message.chat.id,
                              message_id=call_back.message.message_id,
                              parse_mode='Markdown')
    elif call_back.data == '\U00002705Подписаться':
        import sqlite3
        bot_db = sqlite3.connect('Bot_db')
        cursor = bot_db.cursor()
        cursor.execute("UPDATE users SET sending = 1 WHERE id = ?", (call_back.message.chat.id,))
        bot_db.commit()
        cursor.close()
        bot_db.close()

        bot.edit_message_text(text='\U0001F4EB Рассылка *активирована*\nЖди рассылку в 21:00',
                              chat_id=call_back.message.chat.id,
                              message_id=call_back.message.message_id,
                              parse_mode='Markdown')
    elif call_back.data == 'Полный':
        import sqlite3
        bot_db = sqlite3.connect('Bot_db')
        cursor = bot_db.cursor()
        cursor.execute("UPDATE users SET full_place = 1 WHERE id = ?", (call_back.message.chat.id,))
        bot_db.commit()
        cursor.close()
        bot_db.close()

        bot.edit_message_text(text='\U0001F3EB Теперь адрес отображается *целиком*',
                              chat_id=call_back.message.chat.id,
                              message_id=call_back.message.message_id,
                              parse_mode='Markdown')
    elif call_back.data == 'Аудитория':
        import sqlite3
        bot_db = sqlite3.connect('Bot_db')
        cursor = bot_db.cursor()
        cursor.execute('UPDATE users SET full_place = 0 WHERE id = ?', (call_back.message.chat.id,))
        bot_db.commit()
        cursor.close()
        bot_db.close()

        bot.edit_message_text(text='\U0001F6AA Теперь вместо адреса отображается только *аудитория*',
                              chat_id=call_back.message.chat.id,
                              message_id=call_back.message.message_id,
                              parse_mode='Markdown')
    elif call_back.data == 'Обнулять':
        import sqlite3
        bot_db = sqlite3.connect('Bot_db')
        cursor = bot_db.cursor()
        cursor.execute("UPDATE users SET delete_skips = 1 WHERE id = ?", (call_back.message.chat.id,))
        bot_db.commit()
        cursor.close()
        bot_db.close()
        bot.edit_message_text(text='Хорошо, буду *обнулять*',
                              chat_id=call_back.message.chat.id,
                              message_id=call_back.message.message_id,
                              parse_mode='Markdown')
    elif call_back.data == 'Оставлять':
        import sqlite3
        bot_db = sqlite3.connect('Bot_db')
        cursor = bot_db.cursor()
        cursor.execute('UPDATE users SET delete_skips = 0 WHERE id = ?', (call_back.message.chat.id,))
        bot_db.commit()
        cursor.close()
        bot_db.close()
        bot.edit_message_text(text='Хорошо, твои настройки *останутся*',
                              chat_id=call_back.message.chat.id,
                              message_id=call_back.message.message_id,
                              parse_mode='Markdown')
    elif call_back.data == 'Полное ИНФО':
        inline_keyboard = telebot.types.InlineKeyboardMarkup()
        inline_keyboard.row(*[telebot.types.InlineKeyboardButton(text=name, callback_data=name) for
                              name in ['Краткое ИНФО']])
        answer = full_info_answer
        bot.edit_message_text(text=answer,
                              chat_id=call_back.message.chat.id,
                              message_id=call_back.message.message_id,
                              parse_mode='Markdown',
                              disable_web_page_preview=True,
                              reply_markup=inline_keyboard)
    elif call_back.data == 'Краткое ИНФО':
        inline_keyboard = telebot.types.InlineKeyboardMarkup()
        inline_keyboard.row(*[telebot.types.InlineKeyboardButton(text=name, callback_data=name) for
                              name in ['Полное ИНФО']])
        answer = briefly_info_answer
        bot.edit_message_text(chat_id=user_id,
                              message_id=call_back.message.message_id,
                              text=answer,
                              parse_mode='Markdown',
                              disable_web_page_preview=True,
                              reply_markup=inline_keyboard)
    elif call_back.data == 'Обновить':
        from get_yandex_rasp import get_suburban_rasp
        bot.edit_message_text(text='\U000023F3Идет запрос..',
                              chat_id=call_back.message.chat.id,
                              message_id=call_back.message.message_id)
        to_from_stations = call_back.message.text.split(' => ')
        to_station, from_station = to_from_stations[1].split(':')[0].split(' электричек нет')[0], \
                                   to_from_stations[0].split('по маршруту ')[-1]
        to_station, from_station = all_stations[to_station], all_stations[from_station]
        if len(call_back.message.text.split('\n\n')) <= 4:
            answer = get_suburban_rasp(from_station, to_station)
            full = False
        else:
            answer = get_suburban_rasp(from_station, to_station, True)
            full = True
        try:
            answer, no_more = answer.split(' /=>/ ')[0], int(answer.split(' /=>/ ')[1])
        except IndexError:
            answer, no_more = answer.split(' /=>/ ')[0], 1
        inline_keyboard = telebot.types.InlineKeyboardMarkup()
        if full:
            inline_keyboard.row(*[telebot.types.InlineKeyboardButton(text=name, callback_data=name) for
                                name in ['Ближайшие', 'Обновить']])
        else:
            if not no_more:
                inline_keyboard.row(*[telebot.types.InlineKeyboardButton(text=name, callback_data=name) for
                                      name in ['Оставшиеся', 'Обновить']])
            else:
                inline_keyboard.row(*[telebot.types.InlineKeyboardButton(text=name, callback_data=name) for
                                      name in ['Обновить']])
        if to_station == univer:
            inline_keyboard.row(*[telebot.types.InlineKeyboardButton(text=name, callback_data=name) for
                                  name in ['Другая станция']])
        elif from_station == univer:
            inline_keyboard.row(*[telebot.types.InlineKeyboardButton(text=name, callback_data=name) for
                                  name in ['Другое направление']])
        bot.edit_message_text(answer, call_back.message.chat.id, call_back.message.message_id, parse_mode='HTML',
                              reply_markup=inline_keyboard)
    elif call_back.data == 'Оставшиеся':
        from get_yandex_rasp import get_suburban_rasp
        bot.edit_message_text(text='\U000023F3Идет запрос..',
                              chat_id=call_back.message.chat.id,
                              message_id=call_back.message.message_id)
        to_from_stations = call_back.message.text.split(' => ')
        to_station, from_station = to_from_stations[1].split(':')[0].split(' электричек нет')[0], \
                                   to_from_stations[0].split('по маршруту ')[-1]
        to_station, from_station = all_stations[to_station], all_stations[from_station]
        answer = get_suburban_rasp(from_station, to_station, True)
        answer = answer.split(' /=>/ ')[0]
        inline_keyboard = telebot.types.InlineKeyboardMarkup()
        inline_keyboard.row(*[telebot.types.InlineKeyboardButton(text=name, callback_data=name) for
                              name in ['Ближайшие', 'Обновить']])
        if to_station == univer:
            inline_keyboard.row(*[telebot.types.InlineKeyboardButton(text=name, callback_data=name) for
                                  name in ['Другая станция']])
        elif from_station == univer:
            inline_keyboard.row(*[telebot.types.InlineKeyboardButton(text=name, callback_data=name) for
                                  name in ['Другое направление']])
        bot.edit_message_text(answer, call_back.message.chat.id, call_back.message.message_id, parse_mode='HTML',
                              reply_markup=inline_keyboard)
    elif call_back.data == 'Ближайшие':
        from get_yandex_rasp import get_suburban_rasp
        bot.edit_message_text(text='\U000023F3Идет запрос..',
                              chat_id=call_back.message.chat.id,
                              message_id=call_back.message.message_id)
        to_from_stations = call_back.message.text.split(' => ')
        to_station, from_station = to_from_stations[1].split(':')[0].split(' электричек нет')[0], \
                                   to_from_stations[0].split('по маршруту ')[-1]
        to_station, from_station = all_stations[to_station], all_stations[from_station]
        answer = get_suburban_rasp(from_station, to_station)
        answer = answer.split(' /=>/ ')[0]
        inline_keyboard = telebot.types.InlineKeyboardMarkup()
        inline_keyboard.row(*[telebot.types.InlineKeyboardButton(text=name, callback_data=name) for
                              name in ['Оставшиеся', 'Обновить']])
        if to_station == univer:
            inline_keyboard.row(*[telebot.types.InlineKeyboardButton(text=name, callback_data=name) for
                                  name in ['Другая станция']])
        elif from_station == univer:
            inline_keyboard.row(*[telebot.types.InlineKeyboardButton(text=name, callback_data=name) for
                                  name in ['Другое направление']])
        bot.edit_message_text(answer, call_back.message.chat.id, call_back.message.message_id, parse_mode='HTML',
                              reply_markup=inline_keyboard)
    elif call_back.data == 'Другая станция':
        inline_keyboard = telebot.types.InlineKeyboardMarkup()
        for station in all_stations_const:
            if station == 'Университет':
                continue
            inline_keyboard.row(*[telebot.types.InlineKeyboardButton(text=name, callback_data=name) for
                                name in [station]])
        answer = 'Выбери начальную станцию:'
        bot.edit_message_text(answer, call_back.message.chat.id, call_back.message.message_id,
                              reply_markup=inline_keyboard)
    elif call_back.message.text == 'Выбери начальную станцию:':
        from get_yandex_rasp import get_suburban_rasp
        bot.edit_message_text(text='\U000023F3Идет запрос..',
                              chat_id=call_back.message.chat.id,
                              message_id=call_back.message.message_id)
        inline_keyboard = telebot.types.InlineKeyboardMarkup()
        to_station = univer
        answer = get_suburban_rasp(all_stations[call_back.data], to_station)
        answer, no_more = answer.split(' /=>/ ')[0], int(answer.split(' /=>/ ')[1])
        if not no_more:
            inline_keyboard.row(*[telebot.types.InlineKeyboardButton(text=name, callback_data=name) for
                                  name in ['Оставшиеся', 'Обновить']])
        else:
            inline_keyboard.row(*[telebot.types.InlineKeyboardButton(text=name, callback_data=name) for
                                  name in ['Обновить']])
        inline_keyboard.row(*[telebot.types.InlineKeyboardButton(text=name, callback_data=name) for
                              name in ['Другая станция']])
        bot.edit_message_text(answer, call_back.message.chat.id, call_back.message.message_id,
                              reply_markup=inline_keyboard, parse_mode='HTML')
    elif call_back.data == 'Другое направление':
        inline_keyboard = telebot.types.InlineKeyboardMarkup()
        for station in all_stations_const:
            if station == 'Университет':
                continue
            inline_keyboard.row(*[telebot.types.InlineKeyboardButton(text=name, callback_data=name) for
                                name in [station]])
        answer = 'Выбери направление электричек:'
        bot.edit_message_text(answer, call_back.message.chat.id, call_back.message.message_id,
                              reply_markup=inline_keyboard)
    elif call_back.message.text == 'Выбери направление электричек:':
        from get_yandex_rasp import get_suburban_rasp
        bot.edit_message_text(text='\U000023F3Идет запрос..',
                              chat_id=call_back.message.chat.id,
                              message_id=call_back.message.message_id)
        inline_keyboard = telebot.types.InlineKeyboardMarkup()
        from_station = univer
        answer = get_suburban_rasp(from_station, all_stations[call_back.data])
        answer, no_more = answer.split(' /=>/ ')[0], int(answer.split(' /=>/ ')[1])
        if not no_more:
            inline_keyboard.row(*[telebot.types.InlineKeyboardButton(text=name, callback_data=name) for
                                  name in ['Оставшиеся', 'Обновить']])
        else:
            inline_keyboard.row(*[telebot.types.InlineKeyboardButton(text=name, callback_data=name) for
                                  name in ['Обновить']])
        inline_keyboard.row(*[telebot.types.InlineKeyboardButton(text=name, callback_data=name) for
                              name in ['Другое направление']])
        bot.edit_message_text(answer, call_back.message.chat.id, call_back.message.message_id,
                              reply_markup=inline_keyboard, parse_mode='HTML')
    elif call_back.message.text == 'Укажи начальную станцию:':
        inline_keyboard = telebot.types.InlineKeyboardMarkup()
        for station in all_stations_const:
            if station == call_back.data:
                continue
            inline_keyboard.row(*[telebot.types.InlineKeyboardButton(text=name, callback_data=name) for
                                name in [station]])
        inline_keyboard.row(*[telebot.types.InlineKeyboardButton(text=name, callback_data=name) for
                            name in ['Другая начальная']])
        answer = 'Ты выбрал: <b>{0}</b>\nУкажи <b>конечную</b> станцию:'.format(call_back.data)
        bot.edit_message_text(text=answer, chat_id=call_back.message.chat.id, message_id=call_back.message.message_id,
                              reply_markup=inline_keyboard, parse_mode='HTML')
    elif call_back.data == 'Другая начальная':
        inline_keyboard = telebot.types.InlineKeyboardMarkup()
        for station in all_stations_const:
            inline_keyboard.row(*[telebot.types.InlineKeyboardButton(text=name, callback_data=name) for
                                  name in [station]])
        answer = 'Укажи <b>начальную</b> станцию:'
        bot.edit_message_text(text=answer, chat_id=call_back.message.chat.id, message_id=call_back.message.message_id,
                              reply_markup=inline_keyboard, parse_mode='HTML')
    elif call_back.message.text.split('\n')[-1] == 'Укажи конечную станцию:':
        from get_yandex_rasp import get_suburban_rasp
        bot.edit_message_text(text='\U000023F3Идет запрос..',
                              chat_id=call_back.message.chat.id,
                              message_id=call_back.message.message_id)
        from_station = call_back.message.text.split('\n')[0].split(': ')[-1]
        to_station, from_station = all_stations[call_back.data], all_stations[from_station]
        answer = get_suburban_rasp(from_station, to_station)
        answer, no_more = answer.split(' /=>/ ')[0], int(answer.split(' /=>/ ')[1])
        inline_keyboard = telebot.types.InlineKeyboardMarkup()
        if not no_more:
            inline_keyboard.row(*[telebot.types.InlineKeyboardButton(text=name, callback_data=name) for
                                  name in ['Оставшиеся', 'Обновить']])
        else:
            inline_keyboard.row(*[telebot.types.InlineKeyboardButton(text=name, callback_data=name) for
                                  name in ['Обновить']])
        bot.edit_message_text(answer, call_back.message.chat.id, call_back.message.message_id, parse_mode='HTML',
                              reply_markup=inline_keyboard)
    elif call_back.data == 'Показать все' or call_back.data == 'Убрать пересдачи':
        answer = call_back.message.text.split('\n\n')[0] + '\n\n'
        inline_keyboard = telebot.types.InlineKeyboardMarkup()
        if call_back.data == 'Показать все':
            only_exams = False
            inline_keyboard.row(*[telebot.types.InlineKeyboardButton(text=name, callback_data=name) for
                                  name in ['Убрать пересдачи']])
        else:
            only_exams = True
            inline_keyboard.row(*[telebot.types.InlineKeyboardButton(text=name, callback_data=name) for
                                  name in ['Показать все']])
        answer += get_interim_attestation_answer(call_back.message.text.split('\n\n')[0], user_id, only_exams)
        if len(answer) <= 4096:
            bot.edit_message_text(text=answer, chat_id=user_id, message_id=call_back.message.message_id, parse_mode='HTML',
                                  reply_markup=inline_keyboard)
        else:
            for ans in answer.split('\n\n'):
                bot.send_message(user_id, ans, parse_mode='HTML')
    else:
        answer = call_back.data + '\n\n'
        answer += get_interim_attestation_answer(call_back.data, user_id, True)
        inline_keyboard = telebot.types.InlineKeyboardMarkup()
        inline_keyboard.row(*[telebot.types.InlineKeyboardButton(text=name, callback_data=name) for
                              name in ['Показать все']])
        if len(answer) <= 4096:
            bot.edit_message_text(text=answer, chat_id=user_id, message_id=call_back.message.message_id, parse_mode='HTML',
                                  reply_markup=inline_keyboard)
        else:
            for ans in answer.split('\n\n'):
                bot.send_message(user_id, ans, parse_mode='HTML')
