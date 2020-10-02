# coding: utf-8
from slackbot.bot import respond_to
from slackbot.slackclient import SlackClient

from bhaga.SQLRepository import getNamebySlackID, updateTrash, getNextTrash, restart, countMention
from bhaga.logs.LogHandler import LogHandler

import configparser

logger = LogHandler('service')

conf = configparser.ConfigParser()
conf.read('./config.ini')
API_TOKEN = conf['slack']['BOT_USER_OAUTH_ACCESS_TOKEN']
attempt_user = conf['slack']['attempt_user']

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
