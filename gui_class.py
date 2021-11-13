import tkinter
import tkinter.font as f
from tkinter import  ttk
from tkinter import messagebox
import chat

from datetime import datetime
import hashlib
import time
class PlaceholderEntry(ttk.Entry):
    def __init__(self, container, placeholder, *args, **kwargs):
        super().__init__(container, *args, style="Placeholder.TEntry", **kwargs)
        self.placeholder = placeholder

        self.insert("0", self.placeholder)
        self.bind("<FocusIn>", self._clear_placeholder)
        self.bind("<FocusOut>", self._add_placeholder)

    def _clear_placeholder(self, e):
        if self["style"] == "Placeholder.TEntry":
            self.delete("0", "end")
            self["style"] = "TEntry"

    def _add_placeholder(self, e):
        if not self.get():
            self.insert("0", self.placeholder)
            self["style"] = "Placeholder.TEntry"

class GUI:
    def __init__(self):
        self.ankaApp = chat.Anka()
        self.main_w = tkinter.Tk()
        self.anka_w = tkinter.Tk()
        #終了処理
        self.main_w.protocol("WM_DELETE_WINDOW",self.closeAllwindow)
        self.anka_w.protocol("WM_DELETE_WINDOW",self.closeAllwindow)
        self.GraphicElements = []
        self.GraphicButtons = []
        self.setup()
        self.createWidget_main()
        self.createWidget_sub()
        self.grid_main()
        self.grid_sub()
        self.main_w.after(1000,self.update)
        self.main_w.after(5000,self.update_speed)

    def setup(self):
        self.main_w.title("AnkaChan☆ controller")
        self.anka_w.title("AnkaChan☆")
        iconame = r"3.ico"
        self.main_w.iconbitmap(iconame)
        self.anka_w.iconbitmap(iconame)
        self.main_w.geometry("500x240")
        self.anka_w.geometry("500x240")

    def createWidget_main(self):
        self.main_frm = ttk.Frame(self.main_w)
        self.anka_frm = ttk.Frame(self.main_w)
        self.main_frm.grid(column=0,row=0,sticky=tkinter.NSEW,padx=5,pady=10)
        self.anka_frm.grid(column=0,row=3,sticky=tkinter.NSEW,padx=5,pady=10)
        
        self.url_label = ttk.Label(self.main_frm,text="配信url")
        self.url_input = ttk.Entry(self.main_frm,width=30)
        self.url_btn = ttk.Button(self.main_frm,text="接続",command=self.ask_url)
   
        self.currentAnka_label = ttk.Label(self.main_frm,text="現在のレス数 >>")
        self.currentAnka_n_label = ttk.Label(self.main_frm,text=f"0",font=("Noto Sans JP","15","bold"))

        self.currentspeed_label = ttk.Label(self.main_frm,text="現在のレススピード>>")
        self.currentspeed_n_label = ttk.Label(self.main_frm,text=f"0.0/m",font=("Noto Sans JP","15","bold"))

        self.addbutton = ttk.Button(self.anka_frm,text="+",width=3,command=self.addColums)
        self.textinput = PlaceholderEntry(self.anka_frm,"ex.名前",width=20)
        self.ankainput = PlaceholderEntry(self.anka_frm,"ex.100,10-13",width=20)

        style = ttk.Style(self.main_w)
        style.configure("Placeholder.TEntry", foreground="#808080")

    def grid_main(self):
        self.url_label.grid(column=0,row=0,padx=10)
        self.url_input.grid(column=1,row=0,pady=5)
        self.url_btn.grid(column=2,row=0,padx=10)

        self.currentAnka_label.grid(column=0,row=1,pady=0,sticky=tkinter.E)
        self.currentAnka_n_label.grid(column=1,row=1,sticky=tkinter.W)
        self.currentspeed_label.grid(column=0,row=2,pady=0,sticky=tkinter.E)
        self.currentspeed_n_label.grid(column=1,row=2,sticky=tkinter.W)

        self.textinput.grid(column=0,row=1)
        self.ankainput.grid(column=1,row=1)
        self.addbutton.grid(column=2,row=1)

    def createWidget_sub(self):
        self.anka_w_frm = ttk.Frame(self.anka_w)
        self.anka_w_frm.grid(column=0,row=0,sticky=tkinter.NSEW,padx=5,pady=10)
        self.L1 = ttk.Label(self.anka_frm,text="内容")
        self.L2 = ttk.Label(self.anka_frm,text="安価")
        self.L3 = ttk.Label(self.anka_frm,text="追加")
        self.sub_L1 = ttk.Label(self.anka_w_frm,text="内容")
        self.sub_L2 = ttk.Label(self.anka_w_frm,text="安価")

    def grid_sub(self):
        self.sub_L1.grid(column=0,row=0)
        self.sub_L2.grid(column=1,row=0)

    def mainloop(self):
        self.anka_w.mainloop()
        self.main_w.mainloop()

    def getHash(self):
        t_today = datetime.now()
        s_today = t_today.strftime('%Y/%m/%d %H:%M*%S.%f')
        crypto = hashlib.sha256(s_today.encode('utf-8')).hexdigest()
        time.sleep(0.001)
        return crypto

    def ask_url(self):
        url = self.url_input.get()
        state = self.ankaApp.setUrl(url)
        if state == None:
            messagebox.showerror("エラー","無効な配信urlです")
        else:
            messagebox.showinfo("成功","接続成功")
            self.ankaApp.start()

    def update(self):
        self.currentAnka_n_label["text"] = f"{self.ankaApp._anchor}"
        self.currentspeed_n_label["text"] = f"{self.ankaApp._speed}/m"
        if self.GraphicElements != []:
            for _,ank,has in self.GraphicElements:
                try:
                    if self.ankaApp.results[has] != "":
                        ank["text"] = self.ankaApp.results[has]
                except:
                    pass
        self.main_w.after(1000,self.update)

    def update_speed(self):
        self.ankaApp.speed()
        self.main_w.after(5000,self.update_speed)

    def addColums(self):
        text = self.textinput.get()
        ank = self.ankainput.get()
        hashs = self.getHash()
        anks = []
        if "-" in ank:
            #if list
            listank = ank.split("-")
            if len(listank) != 2:
                messagebox.showerror("エラー","正しい書式で入力してください")
                return 0
            for a in listank:
                if not a.isdecimal():
                    messagebox.showerror("エラー","数値を入力してください")
                    return 0
            listank = list(map(int,listank))
            strt = listank[0]
            end = listank[1]+1
            if strt >= end:
                messagebox.showerror("エラー","正しい範囲を入力してください")
                return 0
            anks = range(strt,end)
        else:
            if not ank.isdecimal():
                messagebox.showerror("エラー","数値を入力してください")
                return 0
            anks.append(int(ank))
        for ank in anks:
            hashs = self.getHash()
            self.addColumsFunction(text,ank,hashs)

    def addColumsFunction(self,text,ank,hashs):
        texts = ttk.Label(self.anka_w_frm,text=text+f": >>{ank}",font=("Noto Sans JP","15","bold"))
        ankas = ttk.Label(self.anka_w_frm,text="--",font=("Noto Sans JP","15","bold"))
        reAnka = ttk.Button(self.anka_w_frm,text="再",width=3,command=lambda:self.reAnka(hashs))
        delete = ttk.Button(self.anka_w_frm,text="消",width=3,command=lambda: self.deleteWidget(hashs))
        self.GraphicElements.append([texts,ankas,hashs])
        self.GraphicButtons.append([reAnka,delete])
        self.updateGraphics()
        self.ankaApp.setAnka(int(ank),hashs)

    def updateGraphics(self):
        for ch in self.anka_w_frm.winfo_children():
            ch.grid_forget()
        for i,((texL,ankL,_),(reAnka,delete)) in enumerate(zip(self.GraphicElements,self.GraphicButtons)):
            texL.grid(column=0,row=i+1,padx=10,pady=1)
            ankL.grid(column=1,row=i+1,padx=10,pady=1,sticky=tkinter.W)
            reAnka.grid(column=2,row=i+1,padx=5)
            delete.grid(column=3,row=i+1,padx=5)

    def deleteWidget(self,hash):
        hashs = [has for _,_,has in self.GraphicElements]
        index = hashs.index(hash)
        self.GraphicElements.pop(index)
        self.GraphicButtons.pop(index)
        self.updateGraphics()
    
    def reAnka(self,hash):
        hashs = [has for _,_,has in self.GraphicElements]
        index = hashs.index(hash)
        tex,_,_ =  self.GraphicElements[index]
        backuptext = tex["text"]
        tex["text"] = tex["text"].split(": >>")[0] + ": >>"
        self.GraphicElements[index][1] = ttk.Entry(self.anka_w_frm,width=10)
        reAnk,delet = self.GraphicButtons[index]
        reAnk["text"] = "決"
        reAnk["command"] = lambda:self.reAnkcommand(hash,int(self.GraphicElements[index][1].get()),tex,reAnk,delet,tex["text"].split(": >>")[0] + ": >>"+str(self.GraphicElements[index][1].get()),index)
        delet["text"] = "取消"
        delet["width"] = 8
        delet["command"] = lambda:self.backbackup(tex,reAnk,delet,backuptext,hash,index)
        self.updateGraphics()

    def reAnkcommand(self,hash,num,tex,reAnk,delet,backuptext,index):
        self.reAnkafunc(hash,num)
        self.backbackup(tex,reAnk,delet,backuptext,hash,index)

    def backbackup(self,tex,reAnk,delet,backuptext,hashs,index):
        tex["text"] = backuptext
        self.GraphicElements[index][1] = ttk.Label(self.anka_w_frm,text="--",font=("Noto Sans JP","15","bold"))
        reAnk["text"] = "再"
        reAnk["command"] = lambda:self.reAnka(hashs)
        delet["text"] = "消"
        delet["width"] = 3
        delet["command"] = lambda: self.deleteWidget(hashs)
        self.updateGraphics()

    def reAnkafunc(self,hash,num):
        self.ankaApp.changeAnka(int(num),hash)
    
    def closeAllwindow(self):
        if messagebox.askokcancel("Quit","本当に終了しますか？"):
            self.main_w.destroy()
            self.anka_w.destroy()
#R_OjqP8Et3w