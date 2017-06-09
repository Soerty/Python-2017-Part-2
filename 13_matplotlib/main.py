#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv

from flask import Flask
from flask import send_from_directory
from flask import render_template
import matplotlib.pyplot as plt

app = Flask(__name__)


def get_skolkovo_twits():
    twits = {}

    with open('skolkovo_ru.csv', newline='') as file:
        for twit in csv.reader(file, delimiter=' '):
            id, date, time, time_zone, author, *message = twit

            if message[0] == 'RT':
                retwit = message[1][1:-1]
                message = ' '.join(message[2:])
                twits[id] = {'retwit': retwit}

            twits[id] = {
                'date': date,
                'time': time,
                'time_zone': time_zone,
                'author': author,
                'message': message,
            }

    return twits


def get_genproc_twits():
    twits = {}

    with open('genproc.csv', newline='') as file:
        for twit in csv.reader(file, delimiter=' '):
            id, date, time, time_zone, author, *message = twit
            twits[id] = {
                'date': date,
                'time': time,
                'time_zone': time_zone,
                'author': author,
                'message': ' '.join(message),
            }

    return twits


def draw_plot():
    plt.title('График длинны случайных 50 твитов')
    plt.ylabel('Длинна твитов')
    plt.xlabel('Количество твитов')
    plt.plot(
        [len(twit.get('message')) 
                for id, twit in get_skolkovo_twits().items()][:50], 
        label='Сколково'
    )
    plt.plot(
        [len(twit.get('message')) 
                for id, twit in get_genproc_twits().items()][:50], 
        label='Генеральная прокуратура'
    )
    plt.legend()
    plt.savefig('static/image.png')


@app.route('/')
def index():
    """Main page of the application."""
    return render_template('index.html')



if __name__ == '__main__':
    draw_plot()
    app.run(debug=True)