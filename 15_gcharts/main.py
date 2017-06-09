#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv

from flask import Flask
from flask import render_template

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


@app.route('/')
def index():
    """Main page of the application."""
    return render_template('index.html')


@app.route('/gannt')
def gannt():
    """Main page of the application."""
    return render_template('gannt.html')


@app.route('/skolkovo')
def skolkovo():
    """Main page of the application."""
    data = {}
    for id_twiw, twit in get_skolkovo_twits().items():
        date = twit.get('date')
        if date not in data:
            data[date] = 1
        else:
            data[date] = data[date] + 1

    return render_template('skolkovo.html', data=data)



if __name__ == '__main__':
    app.run(debug=True)