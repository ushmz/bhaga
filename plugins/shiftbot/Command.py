from plugins.shiftbot.SQLRepository import restart
from slackbot.bot import respond_to
"""
# 2525室のごみ捨て当番を次の人に交代する
@respond_to('next trash -r 2525')
def nextTrash2525(message, args):
    repo.nextTrash('2525')
    message.reply(repo.presentTrash('2525'))

# 2721室のごみ捨て当番を次の人に交代する。
@respond_to('next trash -r 2721')
def nextTrash2525(message, args):
    repo.nextTrash('2721')
    message.reply(repo.presentTrash('2721'))

# 議事録当番を次の人に交代する。
@respond_to('next minutes')
def nextTrash2525(message, args):
    repo.nextMinutes()
    message.reply(repo.presentMinutes())

# 2525室のゴミ捨て当番を前の人に戻す。
@respond_to('prev trash -r 2525')
def prevTrash2525(message):
    repo.prevTrash('2525')
    message.reply(repo.presentTrash('2525'))

# 2721室のごみ捨て当番を前の人に戻す。
@respond_to('prev trash -r 2721')
def prevTrash2721(message):
    repo.prevTrash('2721')
    message.reply(repo.presentTrash('2721'))
"""

@respond_to('restart')
def decideFirst(message):
    name = restart()
    message.reply('次回のごみ捨て当番は%sさんです。' % name)
