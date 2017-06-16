#!/usr/bin/env python3
#-*- coding: utf-8 -*-
import json
import http.client
import urllib.parse

from pymystem3 import Mystem
from flask import Flask
from flask import request
from flask import render_template

app = Flask(__name__)


@app.route('/')
def index():
    """Main page of the application."""
    return render_template('index.html')


def type_by_related_name(connection, related_name):
    params = urllib.parse.urlencode({
        'screen_name': related_name,
        'access_token': '8982197830b8e86e10b74bae57c91f4495bb6a9c97' \
                        'a936c92777f8450d2f9528e11435d8917d8cb3eb782',
    })
    connection.request('POST', '/method/utils.resolveScreenName', params)
    response = connection.getresponse()

    return json.loads(response.read().decode('utf-8')).get('response')


def get_members(connection, group_id):
    params = urllib.parse.urlencode({
        'group_id': group_id,
        'access_token': '8982197830b8e86e10b74bae57c91f4495bb6a9c97' \
                        'a936c92777f8450d2f9528e11435d8917d8cb3eb782',
    })
    connection.request('POST', '/method/groups.getMembers', params)
    response = connection.getresponse()

    return json.loads(response.read().decode('utf-8')).get('response')


@app.route('/vk', methods=['GET', 'POST'])
def vk():
    results = {}

    if request.method == 'POST':
        connection = http.client.HTTPSConnection('api.vk.com')

        first = type_by_related_name(connection, request.form.get('first'))
        second = type_by_related_name(connection, request.form.get('second'))
        results['first_name'] = request.form.get('first')
        results['second_name'] = request.form.get('second')

        if first.get('type') == 'group' and second.get('type') == 'group':
            first_members = get_members(connection, first.get('object_id'))
            second_members = get_members(connection, second.get('object_id'))
            results['first'] = first_members['count']
            results['second'] = second_members['count']
            results['intersection'] = len(set(first_members['users']) & set(second_members['users']))

        connection.close()

    return render_template('vk.html', results=results)


@app.route('/mystem', methods=['GET', 'POST'])
def mystem():
    """Allows the user to enter text for parsing in MyStem."""
    morphology = []
    mystem = Mystem()

    if request.method == 'POST':
        for lemma in mystem.lemmatize(request.form.get('text', '')):
            item = mystem.analyze(lemma)[0]
            analysis = item.get('analysis', None)

            if analysis is None:
                continue

            parf_of_speech = analysis[0].get('gr')
            morphology.append([item.get('text'), parf_of_speech.replace(',', ' ')])

    return render_template('mystem.html', results=morphology)


@app.route('/pymorphy')
def pymorphy():
    return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True)