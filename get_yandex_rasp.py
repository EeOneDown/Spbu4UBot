# -*- coding: utf-8 -*-

key = "key"


def get_suburban_rasp(from_station, to_station, full=False):
    import requests
    from bs4 import BeautifulSoup
    from datetime import datetime, timedelta

    server_datetime = datetime.now() + timedelta(hours=3)
    today_server_date = datetime.date(server_datetime)
    url = 'https://api.rasp.yandex.net/v1.0/search/?' + \
          'apikey={0}'.format(key) + \
          '&format=xml' + \
          '&from={0}'.format(from_station) + \
          '&to={0}'.format(to_station) + \
          '&lang=ru' + \
          '&date={0}'.format(today_server_date)
    rasp = requests.get(url).text
    soup = BeautifulSoup(rasp, "lxml")
    titles = soup.find_all('title')[:2]
    title_to, title_from = titles[0].text, titles[1].text
    close_in = ' ближайших' if not full else ''
    departure_times = soup.find_all('departure')
    arrival_times = soup.find_all('arrival')
    k = 0
    i = 0
    server_time = datetime.time(server_datetime)
    last_time = datetime.strptime(departure_times[-1].text, '%Y-%m-%d %H:%M:%S')
    time_delta = str(server_datetime - last_time)
    if time_delta[0] == '-':
        no_more = 1
        answer = 'Список{0} электричек по маршруту <b>{1}</b> => <b>{2}</b>:\n\n'.format(close_in, title_from, title_to)
        for departure_time in departure_times:
            departure_time = datetime.time(datetime.strptime(departure_time.text.split(' ')[1], '%H:%M:%S'))
            if departure_time > server_time:
                if not full:
                    i += 1
                delta = ''
                delta_hour = departure_time.hour - server_time.hour
                delta_minute = departure_time.minute - server_time.minute
                if delta_minute < 0:
                    delta_hour -= 1
                    delta_minute += 60
                if delta_hour != 0:
                    delta += str(delta_hour) + ' ч '
                delta += str(delta_minute) + ' мин\n'
                degree = '\U0001F539'
                if delta_hour == 0 and 10 < delta_minute < 20:
                    degree = '\U0001F538'
                elif delta_hour == 0 and delta_minute <= 10:
                    degree = '\U0001F3C3'
                answer += '{0} <i>Через</i> '.format(degree) + delta
                answer += '<b>Отправление в</b> '
                answer += str(departure_time)[:-3] + ' ('
                answer += arrival_times[k].text.split(' ')[-1][:-3]
                answer += ')\n\n'
                if not full and i == 3:
                    if str(departure_time) == departure_times[-1].text.split(' ')[-1]:
                        no_more = 1
                    else:
                        no_more = 0
                    break
                if str(departure_time) == departure_times[-1].text.split(' ')[-1]:
                    no_more = 1
                else:
                    no_more = 0
            k += 1
        answer += ' /=>/ ' + str(no_more)
    else:
        tomorrow_date = datetime.date(server_datetime + timedelta(days=1, hours=3))
        url = 'https://api.rasp.yandex.net/v1.0/search/?' + \
              'apikey={0}'.format(key) + \
              '&format=xml' + \
              '&from={0}'.format(from_station) + \
              '&to={0}'.format(to_station) + \
              '&lang=ru' + \
              '&date={0}'.format(tomorrow_date)
        rasp = requests.get(url).text
        soup = BeautifulSoup(rasp, "lxml")
        titles = soup.find_all('title')[:2]
        title_to, title_from = titles[0].text, titles[1].text
        answer = 'На сегодня по маршруту <b>{0}</b> => <b>{1}</b> электричек нет, но я посмотрел для тебя самые ранние на завтра:\n\n'.format(title_from, title_to)
        departure_times = soup.find_all('departure')
        i = 0
        for departure_time in departure_times:
            departure_time = datetime.time(datetime.strptime(departure_time.text.split(' ')[1], '%H:%M:%S'))
            if not full:
                i += 1
            answer += '\U0001F539 <b>Отправление в</b> '
            answer += str(departure_time)[:-3] + '\n\n'
            if not full and i == 3:
                answer += ' /=>/ ' + str(0)
                break
    return answer
