# coding: utf-8
import configparser

conf = configparser.ConfigParser()
conf.read('./config.ini')
VERIFICATION_TOKEN = conf['slack']['verification_token']

API_TOKEN = conf['slack']['BOT_USER_OAUTH_ACCESS_TOKEN']

PLUGINS = ['plugins']

DEFAULT_REPLY = '''
「ごみ」を含む文章：
\t→次回の両室のゴミ当番
「ごみ」と「部屋番号(半角)」を含む文章：
\t→該当部屋の次回のごみ捨て当番
「ごみ」と「終」を含む文章：
\t→次回のゴミ捨て当番が更新されるのでごみ捨てを行った人が送信してください。
「議事(録)」を含む文章：
\t→次回の議事録当番
「議事(録)」と「終」を含む文章：
\t→次回の議事録当番が更新されるので議事録当番を行った人が送信してください。
'''
