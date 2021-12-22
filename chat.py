from tkinter import Message
import pytchat
#https://github.com/taizan-hokuto/pytchat
import threading
import queue

import numpy as np
class Anka:
    def __init__(self):
        self._anchor = 0
        self._q = queue.Queue()
        self._event = threading.Event()
        self.lastspeedi = 0
        self.speedtick = 10
        self._ankaPosition = -1
        self._speed = 0
        self._ankanumbers = np.array([])
        self._hashs = np.array([])
        self._flags = np.array([],dtype=np.bool)
        self.results = {}
        self._nullarray = np.array([])

    def setUrl(self,liveurl):
        try:
            self._anchor = 0
            self.lastspeedi = 0
            self._chat = pytchat.create(liveurl)
            return 0
        except pytchat.InvalidVideoIdException:
            return None

    def readChat(self):
        while self._chat.is_alive():
            for c in self._chat.get().sync_items():
                self._anchor += 1
                if not np.array_equal(self._ankanumbers,self._nullarray):
                    whe = np.where(self._ankanumbers[self._flags]==self._anchor)[0]
                    if len(whe) != 0:
                        h = self._hashs[self._flags]
                        self.results[h[whe[0]]] = c.message
                        self._flags[self._flags][whe[0]] = False
                    self.anka = c.message
                #self._q.put([self._anchor,c.message])
                #print(f"{c.datetime} [{c.author.name}] - {c.message}")
        """
    def readAnchor(self):
        while True:
            schedule.run_pending()
            while self._q.empty:
                i,msg = self._q.get()
                if i == self._ankaPosition:
                    self.anka = msg
                    #print(msg)
                #print(i)
        """
    def start(self):
        self._th1 = threading.Thread(target=self.readChat)
        #self._th2 = threading.Thread(target=self.readAnchor)
        #self._th3 = threading.Thread(target=self.speed)

        self._th1.setDaemon(True)
        self._th1.start()
        #self._th2.setDaemon(True)
        #self._th2.start()
        #self._th3.setDaemon(True)
        #self._th3.start()
        

    def setAnka(self,num,hash):
        self._ankanumbers = np.append(self._ankanumbers,num)
        self._hashs = np.append(self._hashs,hash)
        self._flags = np.append(self._flags,True)
        self.results[hash] = ""

    def changeAnka(self,num,hash):
        index = np.where(self._hashs==hash)
        self._flags[index] = True
        self._ankanumbers[index] = num
        self.results[hash] = ""

    def speed(self):
        #t = threading.Timer(self.speedtick,self.speed)
        #t.start()
        self._speed = 1. * (self._anchor - self.lastspeedi)/self.speedtick * 60
        self.lastspeedi = self._anchor
        #print(f"speed:{self._speed}/s")


if __name__ == "__main__":
    a = Anka()
    a.setUrl("5qap5aO4i9A")
    a.start()
    a.setAnka(10)