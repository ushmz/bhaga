from threading import Lock
from plugins.shiftbot.SQLRepository import SQLRepository

class Node:
    """
    In this class, Member class is substituet class for 'Node'
    """

    def __init__(self, data):
        self.data = data
        self.next = None


class Member:

    def __init__(self, slackid, name, grade, onDuty=False, cursor=False, willBeSkipped=False):
        self.slackid = slackid
        self.name = name
        self.grade = grade  #TODOができればいらない
        self.onDuty = onDuty
        self.cursor = cursor
        self.willBeSkipped = willBeSkipped
        self.next = None


class CircularLinkedList:

    """
        議事録当番決定用にする
        or
        ごみ捨てと議事録決定で一つのインスタンスにするか
    """

    _uniqueInstance = None
    _lock = Lock()

    def __new__(cls):
        raise NotImplementedError('Cannot initialize via constructor')

    @classmethod
    def __internal_new__(cls, params):
        inst = super().__new__(cls)

        inst.head = None
        if params:
            for p in params:
                if r[3]:
                    m = Member(slackid=p[0], name=p[1], grade=p[2], onDuty=bool(p[3]), cursor=True)
                else:
                    m = Member(slackid=p[0], name=p[1], grade=p[2], onDuty=bool(p[3]))
                self.push(m)

        return inst

    @classmethod
    def getInstance(cls, *params):
        if not cls._uniqueInstance:
            with cls._lock:
                if not cls._uniqueInstance:
                    cls._uniqueInstance = cls.__internal_new__(params)
        return cls._uniqueInstance

    def push(self, data):
        if type(data) is Member:
            ptr1 = data
        else:
            ptr1 = Member(data)
        temp = self.head

        ptr1.next = self.head

        if self.head is not None:
            while(temp.next != self.head):
                temp = temp.next
            temp.next = ptr1

        else:
            ptr1.next = ptr1

        self.head = ptr1

    def search(self, value):
        cur = self.head

        while cur != None:
            if cur.data == value:
                return True
            else:
                cur = cur.next

            if cur == self.head:
                return False
                break

    def searchMember(self, slackid):
        current = self.head
        try:
            while current != None:
                if current.slackid == slackid:
                    return current
                else:
                    current = current.next

                if current == self.head:
                    raise Exception('slack id not found.')
                    break
        except Exception as e:
            pass
            #logs.logException(e)

    def searchMinutes(self):
        current = self.head

        try:
            while current != None:
                if current.onDuty:
                    return current
                else:
                    current = current.next

                if current == self.head:
                    raise Exception('Nobady is on duty of minutes')
                    break
        except Exception as e:
            pass
            #logs.logException(e)

    def searchonCursor(self):
        current = self.head
        try:
            while current != None:
                if current.cursor:
                    return current
                else:
                    current = current.next

                if current == self.head:
                    raise Exception('Nobady has cursor in this list')
                    break
        except Exception as e:
            pass
            #logs.logException(e)

    def setCursorNext(self):
        current = self.searchonCursor()
        current.cursor = False
        current.next.cursor = True

    def willBeSkippedDuty(self, slackID):
        target = self.searchMember(slackID)

    def printList(self):
        temp = self.head
        if self.head is not None:
            while(True):
                print ('name:%s, onDuty:%s, cursor:%s, willBeSkipped:%s' % (temp.name, temp.onDuty, temp.cursor, temp.willBeSkipped))
                temp = temp.next
                if (temp == self.head):
                    break
