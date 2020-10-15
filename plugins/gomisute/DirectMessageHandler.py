from slackbot.slackclient import SlackClient as client

import configparser

conf = configparser.ConfigParser()
conf.read('./config.ini')
API_TOKEN = conf['slack']['BOT_USER_OAUTH_ACCESS_TOKEN']
attempt_user = conf['slack']['attempt_user']

def sendDM(text, target):
    sc = client(API_TOKEN)
    client.send_message(channel=target, message=text)
