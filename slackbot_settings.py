# coding: utf-8
import configparser

conf = configparser.ConfigParser()
conf.read('./config.ini')
VERIFICATION_TOKEN = conf['slack']['verification_token']

API_TOKEN = conf['slack']['BOT_USER_OAUTH_ACCESS_TOKEN']

PLUGINS = ['plugins.gomisute']
