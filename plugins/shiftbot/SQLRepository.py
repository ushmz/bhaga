# coding: utf-8
from plugins.shiftbot.logs.LogHandler import LogHandler

import configparser
import sys

import mysql.connector as sql

class SQLRepository:
    
    def __init__(self):
        """
        sql とのコネクションの扱い方
        """
        _parser = configparser.ConfigParser()
        _parser.read("./mysql.ini")
        
        self.connection = sql.connect(
            host=_parser["sql"]["host"],
            port=_parser["sql"]["port"],
            user=_parser["sql"]["user"],
            password=_parser["sql"]["password"],
            database=_parser["sql"]["database"]
        )

    def mod(self, num, size):
        q, m = divmod(num, size)
        if m != 0:
            return m
        else:
            return size

    def getMemberInfo4Minutes(self):
        """
        議事録当番を決める循環リストに必要な情報をデータベースから取得する．

        Returns:
            result (list) : [slackID(str), name(str), grade(str), onDuty(bool)]
        """
        self.connection.ping(reconnect=True)
        cursor = self.connection.cursor()
        try:
            cursor.execute("select members.slackID, members._name, members._grade, minutes._onDuty from members, minutes where members.slackID = minutes.slackID and minutes._order is not null order by minutes._order desc")
            result = cursor.fetchall()
        except Exception as e:
            pass
            #logs.logException(e)
        else:
            return result
        finally:
            cursor.close()
            self.connection.close()

    def getMemberInfo4Trash(self, room):
        """
        ごみ捨て当番を決める循環リストに必要な情報をデータベースから取得する．
        
        Args:
            room (str) : 部屋番号

        Returns:
            result (list) : [slackID(str), name(str), grade(str), onDuty(bool)]
        """
        self.connection.ping(reconnect=True)
        cursor = self.connection.cursor()
        try:
            cursor.execute("select members.slackID, members._name, members._grade, trash._onDuty from members, trash where members.slackID = trash.slackID and trash._order is not null and trash._room = '%s' order by trash._order desc" % room)
            result = cursor.fetchall()
        except Exception as e:
            pass
            #logs.logException(e)
        else:
            return result
        finally:
            cursor.close()
            self.connection.close()

    def getNamebySlackID(self, slackID):
        """
        slackIDから名前を取得する．
        Args:
            slackID (str) : スラックID
        
        Returns:
            result (str) : 名前
        """
        self.connection.ping(reconnect=True)
        cursor = self.connection.cursor()
        try:
            cursor.execute("select name from members where SLID = '%s'" % slackID)
            result = cursor.fetchone()
        except Exception as e:
            pass
            #logs.logException(e)
        else:
            return result[0]
        finally:
            cursor.close()
            self.connection.close()

    def presentTrash(self, room):
        """ 部屋番号を引数として受け取り,次回のゴミ捨て当番の名前を返す.

        部屋番号(str)を引数として受け取り,
        当該部屋の代理のごみ捨て当番(behalf_trashがTrue)が存在するか確認.
        存在した場合,その代理のごみ捨て当番の名前を返す.
        存在しなかった場合,順番通りのごみ捨て当番の名前を返す.

        Args:
            room    (str) : 4桁の部屋番号(2525or2721)

        Returns:
            pres    (str) : 次回のごみ捨て当番者の名前(名字)
        """
        self.connection.ping(reconnect=True)
        cursor = self.connection.cursor()

        try:
            cursor.execute("select members._name from members, trash where members.slackID = trash.slackID and trash._room = '%s' and trash._onDuty = TRUE" % room)
            result = cursor.fetchone()
            pres = result[0]
        except Exception as e:
            pass
            #logs.logException(e)
        else:
            return pres
        finally:
            cursor.close()
            self.connection.close()

    def nextTrash(self, room):
        """ 部屋番号を引数として受け取りごみ捨て当番を更新した後,次回のゴミ捨て当番の名前を返す.

        部屋番号(str)を引数として受け取り,当該部屋のごみ捨て当番の順番を変数 order に代入.
        次に部屋番号から,当該部屋の総人数を変数 mem に代入.
        order と mem の内容から,次回のごみ捨て当番を決定し,データベースを更新する.
        更新後,presentTrash()メソッドを呼出すことで,次回のごみ捨て当番の名前を返す.

        Args:
            room    (str) : 4桁の部屋番号(2525or2721)

        Returns:
            presentTrash(room)    (str) : 次回のごみ捨て当番者の名前(名字)
        """
        self.connection.ping(reconnect=True)
        cursor = self.connection.cursor()
    
        cursor.execute("select _order from trash where _room = '%s' and _onDuty = TRUE" % room)
        result = cursor.fetchone()
        order = int(result[0])

        cursor.execute("select count(*) from trash where _room = '%s' and _order is not NULL group by _room" % room)
        result = cursor.fetchone()
        mem = int(result[0])

        try:
            cursor.execute("update trash set _onDuty = FALSE where _room = '%s' and _order = '%s'" % (room, order))
            cursor.execute("update ttrash set _onDuty = TRUE where _room = '%s' and _order = '%s'" % (room, mod(order + 1, mem)))
        except Exception as e:
            connection.rollback()
            #logs.logException(e)
        else:
            connection.commit()
            return presentTrash(room)
        finally:
            cursor.close()
            self.connection.close()

    def prevTrash(self, room):
        """ 部屋番号を引数として受け取り,ごみ捨て当番を一つ前の状態に更新する.

        部屋番号(str)を引数として受け取り,当該部屋のごみ捨て当番の順番を変数 order に代入.
        次に部屋番号から,当該部屋の総人数を変数 mem に代入.
        order と mem の内容から前回のごみ捨て当番を決定し,データベースを更新する.
        間違えて更新してしまったときなど管理,テスト用.

        Args:
            room    (str) : 4桁の部屋番号(2525or2721)

        Returns:
            presentTrash(room)    (str) : 次回のごみ捨て当番者の名前(名字)
        """
        self.connection.ping(reconnect=True)
        cursor = self.connection.cursor()
        cursor.execute("select trashDuty_order from members where room = '%s' and onDuty_trash = TRUE" % room)
        result = cursor.fetchone()
        order = int(result[0])

        cursor.execute("select count(*) from members where minutesDuty_order is not null")
        rs = cursor.fetchone()
        mem = int(rs[0])

        try:
            cursor.execute("update members set onDuty_trash = FALSE where room = '%s' and trashDuty_order = '%s'" % (room, order))
            cursor.execute("update members set onDuty_trash = TRUE where room = '%s' and trashDuty_order = '%s'" % (room, mod(order - 1, mem)))
            connection.commit()
        except Exception as e:
            connection.rollback()
            #logs.logException(e)
        else:
            return presentTrash(room)
        finally:
            cursor.close()
            self.connection.close()

    def presentMinutes(self, *grade):
        """ 次回の議事録当番の名前を返す.

        はじめに代理の議事録当番(behalf_minutesがTrue)が存在するか確認.
        存在した場合,その代理の議事録当番の名前を返す.
        存在しなかった場合,順番通りの議事録当番の名前を返す.

        Args:

        Returns:
            pres    (str) : 次回の議事録当番者の名前(名字)
        """
        self.connection.ping(reconnect=True)
        cursor = self.connection.cursor()
        try:
            cursor.execute("select name from members where behalf_minutes = TRUE")
            result = cursor.fetchone()
            pres = result[0]
        except TypeError as te:
            if grade is not None:
                cursor.execute("select name from members where grade not in ('b3', '%s') and onDuty_minutes = TRUE" % grade)
            else:
                cursor.execute("select name from members where onDuty_minutes = TRUE")
            result = cursor.fetchone()
            pres = result[0]
        except Exception as e:
            pass
            #logs.logException(e)
        finally:
            cursor.close()
        return pres

    def nextMinutesWithArgo(self):
        pass
        # cursor = self.connection.cursor()
        # 曜日ごとで分岐
        # name = rp.nextMinutes
        # try:
        #     cursor.execute("update members set onDuty_minutes = FALSE where onDuty_minutes= TRUE)
        #     cursor.execute("update members set onDuty_minutes= TRUE where name = '%s'" % name)
        #     connection.commit()
        #     return name
        # except Exception as e:
        #     connection.rollback()
        #     logs.logException(e)
        # finally:
        #     cursor.close()


    # will be deleted
    def nextMinutes(self):
        """ 議事録当番を更新した後,次回の議事録当番の名前を返す.

        はじめに議事録当番の順番を変数 order に代入.
        次に議事録当番を回しているメンバーの総数を変数 mem に代入
        order と mem の内容から次回の議事録当番を決定し,データベースを更新する.
        更新後,presentMinutes()メソッドを呼出すことで,更新後の議事録当番の名前を返す.

        Args:

        Returns:
            presentTrash(room)    (str) : 次回のごみ捨て当番者の名前(名字)
        """
        self.connection.ping(reconnect=True)    
        cursor = self.connection.cursor()
        cursor.execute("select minutesDuty_order from members where onDuty_minutes = TRUE")
        result = cursor.fetchone()
        order = int(result[0])

        cursor.execute("select count(*) from members where minutesDuty_order is not null")
        rs = cursor.fetchone()
        mem = int(rs[0])
        try:
            cursor.execute("update members set onDuty_minutes = FALSE where minutesDuty_order = '%s'" % order)
            cursor.execute("update members set onDuty_minutes= TRUE where minutesDuty_order = '%s'" % mod(order + 1, mem))
            connection.commit()
            return presentMinutes()
        except Exception as e:
            connection.rollback()
            #logs.logException(e)
        finally:
            cursor.close()


    def nextMinutesInBusySeason(self, prevGrade):
        self.connection.ping(reconnect=True)
        cursor = self.connection.cursor()
        cursor.execute("select kanaOrder_grade from members where grade = '%s' and onDuty_minutes = TRUE" % prevGrade)
        result = cursor.fetchone()
        order = int(result[0])

        cursor.execute("select count(*) from members where grade = '%s' and kanaOrder_grade is not null" % prevGrade)
        rslt = cursor.fetchone()
        mem = int(rslt[0])

        try:
            cursor.execute("update members set onDuty_minutes = FALSE where kanaOrder_grade = '%s'" % order)
            cursor.execute("update members set onDuty_minutes= TRUE where kanaOrder_grade = '%s'" % mod(order + 1, mem))
            connection.commit()
            return presentMinutes(prevGrade)
        except Exception as e:
            connection.rollback()
            #logs.logException(e)
        finally:
            cursor.close()


    def nextMinutesInBusySeasonWithB3(self, prevGrade):
        self.connection.ping(reconnect=True)
        cursor = self.connection.cursor()
        try:
            cursor.execute("select name, grade from members where done = FALSE and minutesDuty_order is not null order by minutesDuty_order")
            result = cursor.fetchone()
        except TypeError as te:
            cursor.execute("update members set done = FALSE")
            cursor.execute("select name, grade from members where done = FALSE and minutesDuty_order is not null order by minutesDuty_order")
            result = cursor.fetchone()
        finally:
            name = result[0]
            grade = int(result[1])

        if grade != prevGrade:
            cursor.execute("update members set onDuty_minutes = FALSE where onDuty_minutes = TRUE")
            cursor.execute("update members set onDuty_minutes = TRUE where name = '%s'" % name)
            return name

        cursor.execute("select count(*) from members where minutesDuty_order is not null")
        rslt = cursor.fetchone()
        mem = int(rslt[0])

        try:
            cursor.execute("update members set onDuty_minutes = FALSE where kanaOrder_grade = '%s'" % order)
            cursor.execute("update members set onDuty_minutes= TRUE where kanaOrder_grade = '%s'" % mod(order + 1, mem))
            connection.commit()
            return presentMinutes(prevGrade)
        except Exception as e:
            connection.rollback()
            #logs.logException(e)
        finally:
            cursor.close()


    def trashDutyBehalfOf(self, slackID):
        """
        動作確認：未
        """
        self.connection.ping(reconnect=True)
        cursor = self.connection.cursor()
        try:
            cursor.execute("update members set behalf_trash = TRUE where SLID = '%s'" % slackID)
        except Exception as e:
            connection.rollback()
            #logs.logException(e)
        else:
            connection.commit()
        finally:
            cursor.close()
        return getNamebySlackID(slackID)


    def minutesDutyBehalfOf(self, slkid):
        """ 代理の議事録当番を登録する.

        引数として受け取ったuserIDから代理の議事録当番を決定し,データベースを更新する.
        更新後,presentMinutes()を呼び出し,議事録当番の名前を返す.

        Args:
            slkid   (str) : 代理で議事録当番をする人(送信者)のSlackID

        Returns:
            presentMinutes()    (str) : 次回の議事録当番者の名前(名字)

        """
        self.connection.ping(reconnect=True)
        cursor = self.connection.cursor()
        try:
            cursor.execute("update members set behalf_minutes = TRUE where SLID = '%s'" % slkid)
        except Exception as e:
            connection.rollback()
            #logs.logException(e)
        else:
            connection.commit()
        finally:
            cursor.close()
        return presentMinutes()


    def doneTrashDutyBehalfOf(self, room):
        """
        動作確認：未
        """
        self.connection.ping(reconnect=True)
        cursor = connection.cursor()
        try:
            cursor.execute("select name from members where room = '%s' and behalf_trash = TRUE" % room)
            result = cursor.fetchone()
            name = result[0]
            cursor.execute("update members set behalf_trash = FALSE where name = '%s'" % name)
        except Exception as e:
            connection.rollback()
            #logs.logException(e)
        else:
            connection.commit()
        finally:
            cursor.close()


    def doneMinutesDutyBehalfOf(self):
        """
        代理の議事録当番を解除する.

        Returns:
            None
        """
        self.connection.ping(reconnect=True)
        cursor = self.connection.cursor()
        try:
            cursor.execute("select name from members where behalf_minutes = TRUE")
            result = cursor.fetchone()
            name = result[0]
            cursor.execute("update members set behalf_minutes = FALSE where name = '%s'" % name)
        except TabError as te:
            return
        except Exception as e:
            connection.rollback()
            #logs.logException(e)
        else:
            connection.commit()
        finally:
            cursor.close()
