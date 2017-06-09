#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from flask import Flask
from flask import request
from flask import redirect
from flask import render_template

app = Flask(__name__)


@app.route('/')
def index():
    """Main page of the application."""
    return render_template('index.html')


@app.route('/processing', methods=['POST'])
def processing():
    """Form processing and redirection to the results page."""
    username = request.form.get('username')
    choice = request.form.get('choice')

    if choice is None:
        choice = 'Does not like animals'

    with open('fake_database.txt', 'a') as db:
        db.write('%s: %s\n' % (username, choice))

    return redirect('/results')


@app.route('/results')
def result():
    """Displays the results of the responses."""
    lines = open('fake_database.txt').readlines() \
            if os.path.exists('fake_database.txt') else []
    return render_template('results.html', results=lines)



if __name__ == '__main__':
    app.run(debug=True)