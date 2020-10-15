# coding: utf-8
from slackbot.bot import respond_to, default_reply
from slackbot.slackclient import SlackClient
import requests

from plugins.gomisute.SQLRepository import getNamebySlackID, updateTrash, getNextTrash, restart, countMention, getMentionCount
from plugins.gomisute.logs.LogHandler import LogHandler

import configparser

logger = LogHandler('service')

conf = configparser.ConfigParser()
conf.read('./config.ini')
API_TOKEN = conf['slack']['BOT_USER_OAUTH_ACCESS_TOKEN']
attempt_user = conf['slack']['attempt_user']

endpoint = conf['chaplus']['endpoint']
chaplus_key = conf['chaplus']['api_key']
chaplus_dist = f'{endpoint}?apikey={chaplus_key}'

client = SlackClient(API_TOKEN)

@respond_to(r'^(?=.*[ごみ|ゴミ])(?!.*(終|代わ|更新))')
def sendTrashDuty2525AND2721(message, *args):
    """
    (ごみorゴミ)を含むメッセージに対し
    両室の次回のごみ捨て当番をリプライする.

    Args:
        message (Message) : メッセージに関する情報を持ったクラスのインスタンス
        args    (str)     : respond_to()内の正規表現にマッチしたメッセージ本文

    Returns:
        None
    """
    try:
        guri, gura = getNextTrash()
        message.reply('次回のごみ捨て当番は%sさん，%sさんです。' % (guri[1], gura[1]))
    except Exception as e:
        message.reply("申し訳ありません。エラーが発生したようです。")
        logger.logException(e)
    finally:
        countMention(message.body['user'])

@respond_to(r'^(?=.*[ごみ|ゴミ])(?=.*終)')
def sayThanks(message, *args):
    if message.body['user'] in [t[0] for t in getNextTrash()] :
        message.react('+1')
        message.reply('ありがとうございます!!')
    else:
        message.react('thinking_face')
        message.reply('今週のゴミ当番ではないようです。')
        message.reply('おかしな挙動をしていると考えられる場合は @Yusuke Shimizu までご連絡ください。:man-bowing:')
    countMention(message.body['user'])

@respond_to(r'^(?=.*[ごみ|ゴミ])(?=.*更新)')
def update(message, *args):
    guri, gura = updateTrash()
    # TODO: Send to #random instead of DM
    message.reply('次回のごみ捨て当番は%sさん，%sさんです。' % (guri[1], gura[1]))
    client.send_message(channel=guri[0], message="次回のごみ捨て当番です。よろしくおねがいします。")
    client.send_message(channel=gura[0], message="次回のごみ捨て当番です。よろしくおねがいします。")
    logger.logInfo(f'Send notification to {guri[1]}さん({guri[0]}), {gura[1]}さん({gura[0]}).')
    countMention(message.body['user'])
    
# Commands
@respond_to('bhaga restart')
def decideFirst(message, *args):
    guri, gura = restart()
    message.reply('次回のごみ捨て当番は%sさん、%sさんです。' % (guri[1], gura[1]))
    client.send_message(channel=guri[0], message="次回のごみ捨て当番です。よろしくおねがいします。")
    client.send_message(channel=gura[0], message="次回のごみ捨て当番です。よろしくおねがいします。")
    logger.logInfo(f'Send notification to {guri[1]}さん({guri[0]}), {gura[1]}さん({gura[0]}).')
    countMention(message.body['user'])

def chatting(user, message):
    header = {
        'Content-Type': 'application/json'
    }

    body = {
        'utterance': message,
        'username': f"{user}さん",
        'agentState': {
            'agentName': 'ごみ捨てbot',
            'tone': 'normal', # 'normal', 'kansai', 'koshu', 'dechu'
            # 'age': '23'
        },
        # 'addition': {
        #     'options': ['', '', ''],
        #     'utterancePairs': [{'utterance': '', 'response': 'hoge,fuga,bar'}],
        #     'ngwords': [],
        #     'unknownResponses': ['', '', '']
        # }
    }

    response = requests.post(chaplus_dist, headers=header, json=body)    
    resp = response.json()
    return resp['bestResponse']['utterance'].replace('さんさん', 'さん')

# Default reply
@default_reply()
def easterEgg(message, *args):
    countMention(message.body['user'])
    count = getMentionCount(message.body['user'])
    if count % 500 == 0 and 0 < count < 1000:
        message.reply('{}回目のメッセージを受信しました！この調子です！！！'.format(str(count)))
        message.react('+1')
    elif count % 100 == 0 and 0 < count < 1000:
        message.reply('{}回目のメッセージを受信しました！おめでとうございます！！！'.format(str(count)))
        message.react('tada')
    elif count == 1000:
        message.reply('{}回目のメッセージを受信しました！私の完敗です...！！！'.format(str(count)))
        message.reply('これ以上は何もありません！！！')
        message.react('+1')
    else:
        username = getNamebySlackID(message.body['user'])
        reply_msg = chatting(username, message.body['text'])
        message.reply(reply_msg)
        message.reply('ちなみになんですが、「ごみ」を含む文章を送ると次回のゴミ当番がわかるみたいですよ。')
