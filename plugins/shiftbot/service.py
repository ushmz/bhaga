# coding: utf-8
from slackbot.bot import respond_to, default_reply

from plugins.shiftbot.SQLRepository import getMemberInfo4Trash, getNamebySlackID, presentTrash, nextTrash
from plugins.shiftbot.CircularLinkedListRepository import CircularLinkedListRepository
from plugins.shiftbot.logs.LogHandler import LogHandler


rp = CircularLinkedListRepository()

logger = LogHandler('init')

@respond_to(r'^(?=.*[ごみ|ゴミ])(?!.*(終|代わ))')
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
        name = presentTrash()
        message.reply('次回のごみ捨て当番は%sさんです。' % name)
    except Exception as e:
        message.reply("申し訳ありません.エラーが発生したようです.")
        logger.logException(e)


@respond_to(r'^(?=.*[ごみ|ゴミ])(?=.*終)')
def sendNextTrashDutyBySlackID(message, *args):
    frm = getNamebySlackID(message.body['user'])
    if frm == presentTrash():
        message.react('+1')
        message.reply('ありがとうございます!!')

