# coding=utf8

from flask import Flask, jsonify
from flask_redis import FlaskRedis
from flask_apscheduler import APScheduler

import requests

import config
import time


app = Flask(__name__)
app.config.from_object(config)
app.config.from_pyfile('.wxsec.py')

if app.config['TESTING']:
    app.config['REDIS_URL'] = "redis://localhost:32769/0"

redis_store = FlaskRedis(app)

@app.route('/')
def hello():
    return "updated %s times." % redis_store.get('refresh_hits')

@app.route('/wechat_actoken')
def getAcToken():
    return redis_store.get('{0}_access_token'.format(app.config['APP_ID']))

def refresh():
    _http = requests.Session()
    res = _http.get(
            url='https://api.weixin.qq.com/cgi-bin/token',
            params={
                'grant_type': 'client_credential',
                'appid': app.config['APP_ID'],
                'secret': app.config['APP_SECRET']
            }
    )
    result = res.json()
    expires_in = 7200
    if 'expires_in' in result:
        expires_in = result['expires_in']
    redis_store.set('{0}_access_token'.format(app.config['APP_ID']), result['access_token'], expires_in)
    redis_store.incr('refresh_hits')

if __name__ == '__main__':
    
    if app.config['TESTING']:
        redis_store.set('{0}_access_token'.format(app.config['APP_ID']), 'actoken init...')
    else:
        refresh()

    scheduler=APScheduler()
    scheduler.init_app(app)
    scheduler.start()
    app.run(host='0.0.0.0')
