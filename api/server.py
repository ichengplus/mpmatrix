# coding=utf8

from flask import Flask, request, abort, render_template
from wechatpy import parse_message, create_reply
from wechatpy.utils import check_signature
from wechatpy.exceptions import (
    InvalidSignatureException,
    InvalidAppIdException,
)
from flask_redis import FlaskRedis

import config

app = Flask(__name__)

app.config.from_object(config)
app.config.from_pyfile('.wxsec.py')

if app.config['TESTING']:
    app.config['REDIS_URL'] = "redis://localhost:32769/0"

redis_store = FlaskRedis(app)

TOKEN = app.config['TOKEN']
AES_KEY = app.config['AES_KEY']
APPID = app.config['APP_ID']


@app.route('/')
def index():
    return "Hello wechatmp!"


@app.route('/wechat', methods=['GET', 'POST'])
def wechat():
    signature = request.args.get('signature', '')
    timestamp = request.args.get('timestamp', '')
    nonce = request.args.get('nonce', '')
    encrypt_type = request.args.get('encrypt_type', 'raw')
    msg_signature = request.args.get('msg_signature', '')
    try:
        check_signature(TOKEN, signature, timestamp, nonce)
    except InvalidSignatureException:
        abort(403)
    if request.method == 'GET':
        echo_str = request.args.get('echostr', '')
        return echo_str

    # POST request
    if encrypt_type == 'raw':
        # plaintext mode
        msg = parse_message(request.data)
        if msg.type == 'text':
            reply = create_reply(msg.content, msg)
        else:
            reply = create_reply('Sorry, can not handle this for now', msg)
        return reply.render()
    else:
        # encryption mode
        from wechatpy.crypto import WeChatCrypto

        crypto = WeChatCrypto(TOKEN, AES_KEY, APPID)
        try:
            msg = crypto.decrypt_message(
                request.data,
                msg_signature,
                timestamp,
                nonce
            )
        except (InvalidSignatureException, InvalidAppIdException):
            abort(403)
        else:
            msg = parse_message(msg)
            if msg.type == 'text':
                reply = create_reply(msg.content, msg)
            else:
                reply = create_reply('Sorry, can not handle this for now', msg)
            return crypto.encrypt_message(reply.render(), nonce, timestamp)


if __name__ == '__main__':
    ACCESS_TOKEN = redis_store.get('{0}_access_token'.format(app.config['APP_ID']))
    app.run('0.0.0.0', 5001)