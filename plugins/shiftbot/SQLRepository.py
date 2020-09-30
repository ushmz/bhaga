# coding: utf-8
from plugins.shiftbot.logs.LogHandler import LogHandler

import configparser
import random
import sys

import mysql.connector as sql

def getConnection():
    """
    sql とのコネクションの扱い方
    """
    _parser = configparser.ConfigParser()
    _parser.read("./mysql.ini")
    
    return sql.connect(
        host=_parser["mysql"]["host"],
        port=_parser["mysql"]["port"],
        user=_parser["mysql"]["user"],
        password=_parser["mysql"]["passwd"],
        database=_parser["mysql"]["db"]
    )

def mod(num, size):
    q, m = divmod(num, size)
    if m != 0:
        return m
    else:
        return size

def chooseOne(size):
    return random.randrange(size)

def getMemberInfo4Trash():
    """
    TODO: 名前
    ごみ捨て当番を決めるのに必要な情報をデータベースから取得する．
    
    Args:
        room (str) : 部屋番号

    Returns:
        result (list) : [slackID(str), name(str), grade(str), onDuty(bool)]
    """

    connection = getConnection()
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT members.slackID, members._name, trash._onDuty FROM members, trash WHERE members.slackID = trash.slackID AND trash._doneInLoop = FALSE")
        result = cursor.fetchall()
    except Exception as e:
        pass
        #logs.logException(e)
    else:
        return result
    finally:
        cursor.close()
        connection.close()

def getNamebySlackID(slackID):
    """
    slackIDから名前を取得する．
    Args:
        slackID (str) : スラックID
    
    Returns:
        result (str) : 名前
    """
    connection = getConnection()
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT name FROM members WHERE slackID = '%s'" % (slackID,))
        result = cursor.fetchone()
    except Exception as e:
        pass
        #logs.logException(e)
    else:
        return result[0]
    finally:
        cursor.close()
        connection.close()

def presentTrash():
    """ 次回のゴミ捨て当番の名前を返す.

    Args:
        room    (str) : 4桁の部屋番号(2525or2721)

    Returns:
        pres    (str) : 次回のごみ捨て当番者の名前(名字)
    """
    connection = getConnection()
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT members._name FROM members, trash WHERE members.slackID = trash.slackID and trash._onDuty = TRUE")
        result = cursor.fetchone()
        pres = result[0]
    except Exception as e:
        pass
        #logs.logException(e)
    else:
        return pres
    finally:
        cursor.close()
        connection.close()

def nextTrash():
    """ ごみ捨て当番を更新した後,次回のゴミ捨て当番の名前を返す.

    Returns:
        presentTrash(room)    (str) : 次回のごみ捨て当番者の名前(名字)
    """
    connection = getConnection()
    cursor = connection.cursor()

    cursor.execute("UPDATE trash SET _doneInLoop = TRUE, _onDuty = FALSE WHERE _onDuty = TRUE")
    connection.commit()

    cursor.execute("SELECT * FROM trash WHERE _doneInLoop = FALSE")
    result = cursor.fetchall()

    if len(result) == 0:
        cursor.execute("UPDATE trash SET _doneInLoop = FALSE")
        return restart()

    nxt = result[chooseOne(len(result))]

    try:
        cursor.execute("UPDATE trash SET _onDuty = TRUE WHERE slackID = %s" % (nxt["slackID"],))
    except Exception as e:
        connection.rollback()
        #logs.logException(e)
    else:
        connection.commit()
        return presentTrash()
    finally:
        cursor.close()
        connection.close()

def restart():
    connection = getConnection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM trash")
    result = cursor.fetchall()
    start = result(chooseOne(len(result)))
    cursor.execute("UPDATE trash SET _onDuty = TRUE WHERE slackID = %s" % start['slackID'])
    return start['name']
