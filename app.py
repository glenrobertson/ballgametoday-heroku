import logging
import urllib2
import json

from flask import Flask, request, jsonify

app = Flask(__name__)

CITIES = [
    'atlanta',
    'baltimore',
    'bayarea',
    'boston',
    'chicago',
    'cincinnati',
    'dallas',
    'denver',
    'losangeles',
    'minneapolis',
    'neworleans',
    'newyork',
    'oakland',
    'philadelphia',
    'phoenix',
    'pittsburgh',
    'sanfrancisco',
    'sanjose',
    'seattle',
    'washington',
]


@app.route('/', methods=['POST'])
def index():
    params = request.form
    token = params['token']

    user = params['user_name']
    command = params['command']
    channel = params['channel_name']

    if 'text' in params and params['text']:
        pretty_location = params['text'].title()
    else:
        pretty_location = 'San Francisco'
    location = pretty_location.replace(' ', '').lower()

    cities_str = 'Valid locations are:\n {}'.format('\n'.join(CITIES))
    if location == 'help':
        return jsonify({
            'text': cities_str + '\n\nData provided by http://gametonight.in'
        })
    elif location not in CITIES:
        return jsonify({
            'text': 'Invalid location "{}". {}'.format(params['text'], cities_str)
        })

    try:
        response = urllib2.urlopen('http://gametonight.in/' + location + '/json').read()
    except:
        return jsonify({
            'text': 'Not sure what you mean'
        })

    data = json.loads(response)

    if data['game_tonight']:
        result = ':warning: Yes'
        today = data.get('today', {})
        if len(today) > 0:
            titles = ', '.join(event['title'] + ': ' + event['date'].split(' ')[1] for date, event in today.items())
            result += ' ({})'.format(titles)
    else:
        result = ':beers: No ballgame in {}'.format(pretty_location)
    return jsonify({
        'response_type': 'in_channel',
        'text': result
    })
