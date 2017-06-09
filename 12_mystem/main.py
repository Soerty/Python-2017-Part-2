#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pymystem3 import Mystem
from flask import Flask
from flask import request
from flask import redirect
from flask import render_template

mystem = Mystem()
app = Flask(__name__)


@app.route('/')
def index():
    """Main page of the application."""
    return render_template('index.html')


@app.route('/morphology', methods=['GET', 'POST'])
def morphology():
    results = []

    if request.method == 'POST':
        for lemma in mystem.lemmatize(request.form.get('text', '')):
            item = mystem.analyze(lemma)[0]

            if 'analysis' not in item:
                continue

            analysis = item.get('analysis')

            if analysis:
                parf_of_speech = analysis[0].get('gr')

            results.append([item.get('text'), parf_of_speech])

        print (results)

    return render_template('morphology.html', results=results)



if __name__ == '__main__':
    app.run(debug=True)