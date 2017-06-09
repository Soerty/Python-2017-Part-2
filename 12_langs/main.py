#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv

from flask import Flask
from flask import request
from flask import redirect
from flask import render_template

app = Flask(__name__)


def get_langs_list():
    langs = {}

    with open('lang_codes.csv', newline='') as file:
        reader = csv.reader(file)
        for lang_name, code in reader:
            langs[code] = lang_name

    return langs


@app.route('/')
def index():
    """Main page of the application."""
    return render_template('index.html', lang_list=get_langs_list())


@app.route('/langs/<code>')
def langs(code):
    matching = []

    for lang_code, lang_name in get_langs_list().items():
        if lang_code.startswith(code.lower()):
            matching.append(lang_name)

    if not matching:
        return redirect('/not_found')

    return render_template('langs.html', results=matching)


@app.route('/not_found')
def not_found():
    return render_template('not_found.html')


@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'GET':
        return render_template('form.html')
        
    return redirect('/langs/%s' % request.form.get('lang', ''))



if __name__ == '__main__':
    app.run(debug=True)