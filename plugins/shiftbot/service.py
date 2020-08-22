# coding: utf-8
from slackbot.bot import respond_to, default_reply

from plugins.shiftbot.SQLRepository import SQLRepository
from plugins.shiftbot.CircularLinkedListRepository import CircularLinkedListRepository
from plugins.shiftbot.logs.LogHandler import LogHandler


rp = CircularLinkedListRepository()
repo = SQLRepository()

logger = LogHandler('init')

@respond_to(r'^(?=.*(ごみ|ゴミ))(?!.*(2525|2721|終|代わ))')
def sendTrashDuty2525AND2721(message, *args):
    """
    (ごみorゴミ)を含み,(2525or2721or「終」)を含まないメッセージに対し
    両室の次回のごみ捨て当番をリプライする.

    Args:
        message (Message) : メッセージに関する情報を持ったクラスのインスタンス
        args    (str)     : respond_to()内の正規表現にマッチしたメッセージ本文

    Returns:
        None
    """

    try:
        name2525 = repo.presentTrash('2525')
        name2721 = repo.presentTrash('2721')
        message.send('次回のごみ捨て当番は\n2525室：%sさん\n2721室：%sさん\nです。' % (name2525, name2721))
    except Exception as e:
        message.reply("申し訳ありません.内部エラーが発生したようです.")
        logger.logException(e)


@respond_to(r'^(?=.*(ごみ|ゴミ|trash|garbage))(?!.*(終|代わ))(?=.*2525)')
def sendTrashDutyIn2525(message, *args):
    """
    (ごみorゴミ)を含み、かつ部屋番号「2525」が含まれているメッセージに対し
    2525室の次回のごみ捨て当番をリプライする。

    Args:
        message (Message) : メッセージに関する情報を持ったクラスのインスタンス
        args    (str)     : respond_to()内の正規表現にマッチしたメッセージ本文

    Return:
        None
    """

    try:
        name = repo.presentTrash('2525')
        message.send('2525室の次回のごみ捨て当番は%sさんです。' % name)
    except Exception as e:
        message.reply("申し訳ありません.内部エラーが発生したようです.")
        logger.logException(e)


@respond_to(r'^(?=.*(ごみ|ゴミ|trash|garbage))(?!.*(終|代わ))(?=.*2721)')
def sendTrashDutyIn2721(message, *args):
    """
    (ごみorゴミ)を含み,かつ部屋番号「2721」が含まれているメッセージに対し
    2721室の次回のごみ捨て当番をリプライする.

    Args:
        message (Message) : メッセージに関する情報を持ったクラスのインスタンス
        args    (str)     : respond_to()内の正規表現にマッチしたメッセージ本文

    Return:
        None
    """

    try:
        name = repo.presentTrash('2721')
        message.send('2721室の次回のごみ捨て当番は%sさんです。' % name)
    except Exception as e:
        message.reply("申し訳ありません.内部エラーが発生したようです.")
        logger.logException(e)


@respond_to(r'^(?=.*(議事録|議事))(?!.*(終|今日|代わ))')
def sendMinutesTaker(message, *args):
    """
    (議事録or議事)が含まれているメッセージに対し
    次回の議事録当番をリプライする.

    Args:
        message (Message) : メッセージに関する情報を持ったクラスのインスタンス
        args    (str)     : respond_to()内の正規表現にマッチしたメッセージ本文

    Return:
        None
    """

    try:
        name = rp.presentMinutes()
        message.send('次回の議事録当番は%sさんです。' % name)
    except Exception as e:
        message.reply("申し訳ありません.内部エラーが発生したようです.")
        logger.logException(e)


@respond_to(r'^(?=.*(ごみ|ゴミ))(?=.*終)')
def sendNextTrashDutyBySlackID(message, *args):
    nextDuty = repo.nextTrashbyID(message.body['user'])
    message.reply('ありがとうございます。%s室の次回のごみ捨て当番は%sさんです。よろしくお願いします。' % nextDuty)


@respond_to(r'^(?=.*(ごみ|ゴミ))(?=.*終)(?=.*2525)')
def sendNextTrashDutyIn2525(message, *args):
    """
    (ごみorゴミ)かつ「終」かつ「2525」が含まれているメッセージに対し
    2525室の次回のゴミ捨て当番を更新し,その内容をリプライする.

    Args:
        message (Message) : メッセージに関する情報を持ったクラスのインスタンス
        args    (str)     : respond_to()内の正規表現にマッチしたメッセージ本文

    Return:
        None
    """

    # presID = repo.getSlackIDofTrashDuty('2525')
    # if presID != message.body['user']:
    #     message.reply('ごみ捨てを担当した本人が送信してください...')
    #     return

    try:
        repo.doneTrashDutyBehalfOf('2525')
        name2525 = repo.nextTrash('2525')
        message.send('ありがとうございます。2525室の次回のごみ捨て当番は%sさんです。よろしくお願いします。' % name2525)
    except Exception as e:
        message.reply("申し訳ありません.内部エラーが発生したようです.")
        logger.logException(e)

@respond_to(r'^(?=.*(ごみ|ゴミ))(?=.*終)(?=.*2721)')
def sendNextTrashDuty(message, *args):
    """
    (ごみorゴミ)かつ「終」かつ「2721」が含まれているメッセージに対し
    2721室の次回のゴミ捨て当番を更新し,その内容をリプライする.

    Args:
        message (Message) : メッセージに関する情報を持ったクラスのインスタンス
        args    (str)     : respond_to()内の正規表現にマッチしたメッセージ本文

    Return:
        None
    """

    # presID = repo.getSlackIDofTrashDuty('2721')
    # if presID != message.body['user']:
    #     message.reply('ごみ捨てを担当した本人が送信してください...')
    #     return

    try:
        repo.doneTrashDutyBehalfOf('2721')
        name2721 = repo.nextTrash('2721')
        message.send('ありがとうございます。2721室の次回のごみ捨て当番は%sさんです。よろしくお願いします。' % name2721)
    except Exception as e:
        message.reply("申し訳ありません.内部エラーが発生したようです.")
        logger.logException(e)

# @respond_to(r'^(?=.*(議事録|議事|ミーティング|mtg))(?=.*終)')
def sendNextMinutesDuty(message, *args):
    """
    (議事録or議事)が含まれ,かつ「終」が含まれているメッセージに対し
    次回の議事録当番を更新し,その内容をリプライする。
    定例ミーティング終了時に呼び出されることを想定している.

    Args:
        message (Message) : メッセージに関する情報を持ったクラスのインスタンス
        args    (str)     : respond_to()内の正規表現にマッチしたメッセージ本文

    Return:
        None
    """

    try:
        # どうにかして次回発表者の名前を受け取る．
        nextSpeaker = ()
        name = rp.nextMinutes(nextSpeaker)
        print('定例ミーティングお疲れさまです。\n次回の議事録当番は%sさんです。よろしくお願いします。' % name)
        # message.send('定例ミーティングお疲れさまです。\n次回の議事録当番は%sさんです。よろしくお願いします。' % name)
    except Exception as e:
        message.reply("申し訳ありません.内部エラーが発生したようです.")
        logger.logException(e)

@respond_to(r'^(?=.*今日)(?=.*(議事録|議事))')
def sendTodaysMinutesDuty(message, *args):
    """
    「今日」が含まれ,かつ(議事録or議事)が含まれているメッセージに対し
    次回の議事録当番をリプライする。
    メッセージの内容が変わっているのみで,sendMinutesTaker()と同じ動作をする.

    Args:
        message (Message) : メッセージに関する情報を持ったクラスのインスタンス
        args    (str)     : respond_to()内の正規表現にマッチしたメッセージ本文

    Return:
        None
    """

    try:
        name = rp.presentMinutes()
        message.send('本日の議事録当番は%sさんです。よろしくお願いします。' % name)
    except Exception as e:
        message.reply("申し訳ありません.内部エラーが発生したようです.")
        logger.logException(e)


@respond_to(r'^(?=.*(代理|代わ))(?=.*(ゴミ|ごみ))')
def willDiscardBehalfOf(message, *args):
    """
    条件に合うメッセージに対し,
    代理のごみ捨て当番を登録し,その内容をリプライする.

    Args:
        message (Message) : メッセージに関する情報を持ったクラスのインスタンス
        args    (str)     : respond_to()内の正規表現にマッチしたメッセージ本文

    Returns:
        None
    """

    try:
        name = repo.trashDutyBehalfOf(message.body['user'])
        message.reply('次回のごみ捨て当番は%sさんに変更しました。よろしくお願いします。' % name)
    except Exception as e:
        message.reply("申し訳ありません.内部エラーが発生したようです.")
        logger.logException(e)


@respond_to(r'^(?=.*(代理|代わ))(?=.*(議事録|議事))')
def willTakeBehalfOf(message, *args):
    """
    条件に合うメッセージに対し,
    代理の議事録当番を登録し,その内容をリプライする.

    Args:
        message (Message) : メッセージに関する情報を持ったクラスのインスタンス
        args    (str)     : respond_to()内の正規表現にマッチしたメッセージ本文

    Returns:
        None
    """

    try:
        repo.minutesDutyBehalfOf(message.body['user'])
        name = repo.presentMinutes()
        message.reply('次回の議事録当番は%sさんに変更しました。よろしくお願いします。' % name)
    except Exception as e:
        message.reply("申し訳ありません.内部エラーが発生したようです.")
        logger.logException(e)


@default_reply()
def getSlackId(message, *args):
    for arg in args:
        logger.logInfo(message.body['user'] + ' : ' + arg)
    message.reply('「ごみ」を含む文章：\n\t→次回の両室のゴミ当番\n「ごみ」と「部屋番号(半角)」を含む文章：\n\t→該当部屋の次回のごみ捨て当番\n「ごみ」と「終」を含む文章：\n\t→次回のゴミ捨て当番が更新されるのでごみ捨てを行った人が送信してください。\n「議事(録)」を含む文章：\n\t→次回の議事録当番\n「議事(録)」と「終」を含む文章：\n\t→次回の議事録当番が更新されるので議事録当番を行った人が送信してください。\n「代理」と代理を登録したい当番を含む文章：\n\t→次回の当番をこのメッセージを送信した人に変更します。')
