from slackbot.slackclient import SlackClient as client

import configparser

class DirectMessageHandler:
    conf = configparser.ConfigParser()
    conf.read('./config.ini')
    API_TOKEN = conf['slack']['BOT_USER_OAUTH_ACCESS_TOKEN']
    attempt_user = conf['slack'][attempt_user]

    def sendDMTest(self, text, target):
        # sc = client(API_TOKEN)
        # client.send_message(self=sc, channel=attempt_user, message=text)
        print("Send msg'%s' to %s" % (text, target))
    
    def sendDM(self, text, target):
        sc = client(API_TOKEN)
        client.send_message(self=sc, channel=target, message=text)
