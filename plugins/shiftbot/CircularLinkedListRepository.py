from plugins.shiftbot.CircularLinkedList import CircularLinkedList

class CircularLinkedListRepository:

    def __init__(self):
        self.minutes = CircularLinkedList('minutes')
        self.trash2525 = CircularLinkedList('2525')
        self.trash2721 = CircularLinkedList('2721')

    def presentTrash(self, room=None):
        m2525 = self.trash2525.searchTrash()
        m2721 = self.trash2721.searchTrash()
        if room == '2525':
            return m2525.name
        elif room == '2721':
            return m2721.name
        else:
            return (m2525.name, m2721.name)

    def nextTrashin2525(self):
        prev = self.trash2525.searchonCursor()
        prev.onDuty = False
        prev.next.onDuty = True
        return prev.next.name

    def nextTrashin2721(self):
        prev = self.trash2721.searchonCursor()
        prev.onDuty = False
        prev.next.onDuty = True
        return prev.next.name

    def presentMinutes(self):
        member = self.minutes.searchMinutes()
        return member.name

    def nextMinutes(self, nextSpeaker):
        """ TODO
        次回発表者をタプルで受け取り含まれていればスキップ
        """
        # 変更前の議事録当番に対し，
        prev = self.minutes.searchMinutes()
        # カーソルがなければ
        # 次にカーソルが回ってくるまでスキップする．
        if prev.cursor == False:
            prev.willBeSkipped = True

        # 確認する対象を決定
        cur = self.minutes.searchonCursor()

        # 次回の議事録当番が決まるまでループ
        while cur.next != None:
            # 確認対象の人が変更前の議事録当番であれば
            # カーソルを次の人に移し次の人を確認
            if cur.onDuty:
                cur.cursor = False
                cur.next.cursor = True
                cur = cur.next
            # 確認対象の人が変更前の議事録当番でなければ，
            else:
                # skipフラグがTrueなら，カーソルが通過するまで何もせず次の人を確認
                # カーソルが通過したらフラグをFalseにしカーソルを次の人に移し，次の人を確認
                if cur.willBeSkipped:
                    if cur.cursor:
                        cur.willBeSkipped = False
                        cur.cursor = False
                        cur.next.cursor = True
                    cur = cur.next
                # skipフラグFalseで次回の発表者ならカーソルを保持したまま次の人を確認
                elif cur.name in nextSpeaker:
                    cur = cur.next
                # skipフラグFalseかつ次回の発表者でなければその人を次の議事録当番に設定
                else:
                    cur.onDuty = True
                    prev.onDuty = False
                    break

        return cur.name

    def willBeSkippedNextMinutes(self, slackID):
        mem = self.minutes.willBeSkippedDuty(slackID)
