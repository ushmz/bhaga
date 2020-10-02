# coding: utf-8
from bhaga.logs.LogHandler import LogHandler

import configparser
import random
import sys

import mysql.connector as sql

logger = LogHandler('sql')

def getConnection():
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
    result = None

    try:
        cursor.execute("SELECT name FROM members WHERE slackID = '%s'" % (slackID,))
        result = cursor.fetchone()
    except Exception as e:
        logger.logException(e)
    finally:
        cursor.close()
        connection.close()
    return result[0]

def chooseTrash():
    connection = getConnection()
    cursor = connection.cursor()

    guri, gura = None

    try:
        cursor.execute("SELECT * FROM trash WHERE _doneInLoop = FALSE")
        result = cursor.fetchall()
        if len(result) == 0:
            restart()
        elif len(result) == 1:
            pass
        else:
            guri = result[chooseOne(len(result))]
            res = list(filter(lambda x:x['_grade'] != guri['_grade'], result))
            if len(res) == 0:
                pass
            else:
                gura = res[chooseOne(len(res))]

    except Exception as e:
        logger.logException(e)
    finally:
        cursor.close()
        connection.close()
    
    return guri, gura

def getNextTrash():
    """ 次回のゴミ捨て当番の名前を返す.

    Returns:
        pres    (str) : 次回のごみ捨て当番者の情報
    """
    connection = getConnection()
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT members.slackID, members._name FROM members, trash WHERE members.slackID = trash.slackID AND trash._onDuty = TRUE")
        result = cursor.fetchall()
    except Exception as e:
        logger.logException(e)
    finally:
        cursor.close()
        connection.close()

    return result[0], result[1]

def updateTrash():
    """ ごみ捨て当番を更新した後,次回のゴミ捨て当番の名前を返す.

    Returns:
        presentTrash(room)    (str) : 次回のごみ捨て当番者の情報
    """
    connection = getConnection()
    cursor = connection.cursor()

    guri, gura = None, None

    try:
        cursor.execute("SELECT trash.slackID FROM trash WHERE trash._onDuty = TRUE")
        worked = cursor.fetchall()
        cursor.execute("UPDATE easteregg SET _count = _count+1 WHERE slackID = '%s'" % (worked[0][0],))
        cursor.execute("UPDATE easteregg SET _count = _count+1 WHERE slackID = '%s'" % (worked[1][0],))
        connection.commit()

        cursor.execute("UPDATE trash SET _doneInLoop = TRUE, _onDuty = FALSE WHERE _onDuty = TRUE")
        connection.commit()
        
        cursor.execute("SELECT members.slackID, members._name, members._grade FROM members, trash WHERE members.slackID = trash.slackID AND trash._doneInLoop = FALSE")
        notyet = cursor.fetchall()

        if len(notyet) == 0:
            return restart()

        if len(notyet) == 1:
            guri = notyet[0]
            return restart(guri)

        guri, gura = chooseTwins(notyet, 2)

        cursor.execute("UPDATE trash SET _onDuty = TRUE WHERE slackID = '%s'" % (guri[0],))
        cursor.execute("UPDATE trash SET _onDuty = TRUE WHERE slackID = '%s'" % (gura[0],))
        connection.commit()
    except Exception as e:
        connection.rollback()
        logger.logException(e)
    finally:
        cursor.close()
        connection.close()

    return guri, gura

def restart(pair=None):
    connection = getConnection()
    cursor = connection.cursor()

    guri = None
    gura = None

    try:
        cursor.execute("UPDATE trash SET _onDuty = FALSE, _doneInLoop = FALSE")
        connection.commit()

        cursor.execute("SELECT members.slackID, _name, _grade FROM members, trash WHERE members.slackID = trash.slackID")
        result = cursor.fetchall()

        if pair:
            guri = pair
        else:
            guri = result[chooseOne(len(result))]
        res = list(filter(lambda x:x[2] != guri[2], result))
        gura = res[chooseOne(len(res))]
        
        cursor.execute("UPDATE trash SET _onDuty = TRUE WHERE slackID = '%s'" % guri[0])
        cursor.execute("UPDATE trash SET _onDuty = TRUE WHERE slackID = '%s'" % gura[0])
    except Exception as e:
        logger.logException(e)
    finally:
        connection.commit()
        cursor.close()
        connection.close()
    
    return guri, gura

def chooseTwins(results, idx):
    guri = results[chooseOne(len(results))]
    results = list(filter(lambda x:x[idx] != guri[idx], results))
    gura = results[chooseOne(len(results))]
    return guri, gura

def countMention(slackID):
    connection = getConnection()
    cursor = connection.cursor()
    cursor.execute("UPDATE easteregg SET _mentions = _mentions +1 WHERE slackID = '%s'" % (slackID,))
    connection.commit()

def getCount(slackID):
    connection = getConnection()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT _count FROM easteregg WHERE slackID = '%s'" % (slackID,))
        result = cursor.fetchone()
    except Exception as e:
        logger.logException(e)
    finally:
        cursor.close()
        connection.close()

    return result[0]

def getMentionCount(slackID):
    connection = getConnection()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT _count FROM easteregg WHERE slackID = '%s'" % (slackID,))
        result = cursor.fetchone()
    except Exception as e:
        logger.logException(e)
    finally:
        cursor.close()
        connection.close()

    return result[0]
