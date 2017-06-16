#!/usr/bin/env python3
#-*- coding: utf-8 -*-
import re
import json
import random
import http.client
import urllib.parse

from pymorphy2 import MorphAnalyzer
from pymystem3 import Mystem
from flask import Flask
from flask import request
from flask import render_template

morph = MorphAnalyzer()
app = Flask(__name__)


@app.route('/')
def index():
    """Main page of the application."""
    return render_template('index.html')


def type_by_related_name(connection, related_name):
    params = urllib.parse.urlencode({
        'screen_name': related_name,
        'access_token': '4b384e1c2f4f36fe0f5458f34d898dda571f55e0bc5fdccec41940a55ba0695dd7434f41641c38a789c72',
    })
    connection.request('POST', '/method/utils.resolveScreenName', params)
    response = connection.getresponse()

    return json.loads(response.read().decode('utf-8')).get('response')


def get_members(connection, group_id):
    params = urllib.parse.urlencode({
        'group_id': group_id,
        'access_token': '4b384e1c2f4f36fe0f5458f34d898dda571f55e0bc5fdccec41940a55ba0695dd7434f41641c38a789c72',
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

    if request.method == 'POST':
        mystem = Mystem()

        for lemma in mystem.lemmatize(request.form.get('text', '')):
            item = mystem.analyze(lemma)[0]
            analysis = item.get('analysis', None)

            if analysis is None:
                continue

            parf_of_speech = analysis[0].get('gr')
            morphology.append([item.get('text'), parf_of_speech.replace(',', ' ')])

    return render_template('mystem.html', results=morphology)


def get_agreed_word(parsed_word, already_selected):
    with open('words.txt') as file:
        for line in file:
            if random.choice([False, True, False]):
                id, word = line[:-1].split('\t')
                custom_word = morph.parse(word)[0]
                if parsed_word.tag.POS == custom_word.tag.POS and \
                        parsed_word.tag.tense == custom_word.tag.tense and \
                        parsed_word.tag.number == custom_word.tag.number and \
                        parsed_word.tag.aspect == custom_word.tag.aspect and \
                        word not in already_selected:
                    return word


@app.route('/pymorphy', methods=['GET', 'POST'])
def pymorphy():
    result = []

    if request.method == 'POST':        
        pattern = re.compile(r'\W+')

        for word in pattern.split(request.form.get('text', '')):
            if word:
                result.append(get_agreed_word(morph.parse(word)[0], result))

    return render_template('pymorphy.html', result=result)



if __name__ == '__main__':
    app.run(debug=True)