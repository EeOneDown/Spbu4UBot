# -*- coding: utf-8 -*-

def clear_not_using_groups():
    import sqlite3
    bot_db = sqlite3.connect('Bot_db')
    cursor = bot_db.cursor()
    cursor.execute("SELECT g_tt.id FROM groups_tt as g_tt LEFT OUTER JOIN users AS u ON g_tt.url = u.url WHERE u.id ISNULL")
    ids = cursor.fetchall()
    for id in ids:
        cursor.execute("DELETE FROM groups_tt WHERE id = ?", (id[0],))
        bot_db.commit()
        print('deleted: ' + str(id[0]))
    cursor.close()
    bot_db.close()

def update_db():
    print('-----------------------------------')
    import requests
    import sqlite3
    from time import time
    cookies = {'_gat': '1', '_ga': 'GA1.2.76615387.1488377623', '_culture': 'ru'}
    tic = time()
    bot_db = sqlite3.connect('Bot_db')
    cursor = bot_db.cursor()
    cursor.execute("SELECT id, url FROM groups_tt")
    urls = cursor.fetchall()
    cursor.execute("SELECT g_tt.id FROM groups_tt as g_tt LEFT OUTER JOIN users AS u ON g_tt.url = u.url WHERE u.id ISNULL")
    ids = [id[0] for id in cursor.fetchall()]
    print('count of groups: ' + str(len(urls)))
    count = 0
    for url in urls:
        if url[0] in ids:
            count += 1
            continue
        soup = requests.get(url[1], cookies=cookies).text
        cursor.execute("UPDATE groups_tt SET soup = ? WHERE url = ?", (soup, url[1]))
        bot_db.commit()
    cursor.close()
    bot_db.close()
    print('count of skipped: ' + str(count))
    print('success')
    print('update time: ' + str(time() - tic))
    print('-----------------------------------\n')

def update_ia():
    import requests
    import sqlite3
    from bs4 import BeautifulSoup
    cookies = {'_gat': '1', '_ga': 'GA1.2.76615387.1488377623', '_culture': 'ru'}
    bot_db = sqlite3.connect('Bot_db')
    cursor = bot_db.cursor()
    cursor.execute("SELECT id, soup FROM groups_tt")
    soups = cursor.fetchall()
    cursor.execute("SELECT g_tt.id FROM groups_tt as g_tt LEFT OUTER JOIN users AS u ON g_tt.url = u.url WHERE u.id ISNULL")
    ids = [id[0] for id in cursor.fetchall()]
    for soup in soups:
        if soup[0] in ids:
            continue
        url_soup = BeautifulSoup(soup[1], "lxml")
        att_url = url_soup.find('a', text=u'пром. аттестация').get('href')
        ia_soup = requests.get('http://timetable.spbu.ru' + att_url, cookies=cookies).text
        cursor.execute("UPDATE groups_tt SET interim_attestation = ? WHERE id = ?", (ia_soup, soup[0]))
        bot_db.commit()
    cursor.close()
    bot_db.close()

def clear_db():
    import sqlite3
    bot_db = sqlite3.connect('Bot_db')
    cursor = bot_db.cursor()
    cursor.execute("DELETE FROM users")
    bot_db.commit()
    cursor.execute("DELETE FROM skips")
    bot_db.commit()
    cursor.execute("DELETE FROM lessons")
    bot_db.commit()
    cursor.execute("DELETE FROM groups_tt")
    bot_db.commit()
    cursor.close()
    bot_db.close()

if __name__ == '__main__':
    import time
    if time.localtime().tm_hour == 18:
        print('-----------------------------------')
        import os
        os.system('python3.5 sender.py')
    elif time.localtime().tm_hour == 17:
        time.sleep(2400)
    update_db()
    if time.localtime().tm_hour == 0:
        update_ia()
