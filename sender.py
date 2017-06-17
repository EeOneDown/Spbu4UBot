# -*- coding: utf-8 -*-
def sending():
    import telebot
    import sqlite3
    from constants import daily_tt, create_answer, release_token
    from datetime import datetime, timedelta
    print('Рассылка пошла!')
    bot = telebot.TeleBot(release_token)
    bot_db = sqlite3.connect('Bot_db')
    cursor = bot_db.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    for user in users:
        if user[3]:
            answer = 'Расписание на завтра\n\n'
            tomorrow = (datetime.now() + timedelta(1.125)).day
            info_for_message = daily_tt(user[1], tomorrow)
            tt = create_answer(info_for_message, user[0])
            if tt.split(' ')[1].strip() == 'Выходной':
                continue
            answer += tt
            print(user[0])
            bot.send_message(user[0], answer, parse_mode='Markdown')
    print('Всё')
    cursor.close()
    bot_db.close()

if __name__ == '__main__':
    sending()
