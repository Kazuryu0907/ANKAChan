import tkinter
import tkinter.font as f
from tkinter import  ttk
import chat

from datetime import datetime
import hashlib

def getHash():
    t_today = datetime.now()
    s_today = t_today.strftime('%Y/%m/%d %H:%M*%S')
    crypto = hashlib.sha256(s_today.encode('utf-8')).hexdigest()
    return crypto

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

anka = chat.Anka()
def ask_url():
    url = url_input.get()
    #anka.setUrl("5qap5aO4i9A")
    anka.setUrl(url)
    anka.start()

main_w = tkinter.Tk()
anka_w = tkinter.Tk()

main_w.title("Anka")
anka_w.title("Anka Window")

main_w.geometry("500x240")
anka_w.geometry("500x240")
#texts ankas hashs
GraphicElements = []
def update():
    currentAnka_n_label["text"] = f"{anka._anchor}"
    currentspeed_n_label["text"] = f"{anka._speed}/m"
    if GraphicElements != []:
        for _,ank,has in GraphicElements:
            if anka.results[has] != "":
                ank["text"] = anka.results[has]
    main_w.after(1000,update)

def update_speed():
    anka.speed()
    main_w.after(5000,update_speed)
def addColums():
    global GraphicElements
    text = textinput.get()
    ank = ankainput.get()
    texts = ttk.Label(anka_w_frm,text=text+f": >>{ank}",font=("Noto Sans JP","15","bold"))
    ankas = ttk.Label(anka_w_frm,text="--",font=("Noto Sans JP","15","bold"))
    hashs = getHash()
    GraphicElements.append([texts,ankas,hashs])
    for i,(texL,ankL,_) in enumerate(GraphicElements):
        texL.grid_forget()
        ankL.grid_forget()
        texL.grid(column=0,row=i+1,padx=10,pady=1)
        ankL.grid(column=1,row=i+1,padx=10,pady=1)
    anka.setAnka(int(ank),hashs)
    

main_frm = ttk.Frame(main_w)
anka_frm = ttk.Frame(main_w)
anka_w_frm = ttk.Frame(anka_w)


main_frm.grid(column=0,row=0,sticky=tkinter.NSEW,padx=5,pady=10)
anka_frm.grid(column=0,row=3,sticky=tkinter.NSEW,padx=5,pady=10)
anka_w_frm.grid(column=0,row=0,sticky=tkinter.NSEW,padx=5,pady=10)

url_label = ttk.Label(main_frm,text="配信id")
url_input = ttk.Entry(main_frm,width=30)
url_btn = ttk.Button(main_frm,text="接続",command=ask_url)


font1 = f.Font(family="Noto Sans JP",weight="normal",size=8)
currentAnka_label = ttk.Label(main_frm,text="現在のレス数 >>")
currentAnka_n_label = ttk.Label(main_frm,text=f"0",font=("Noto Sans JP","15","bold"))

currentspeed_label = ttk.Label(main_frm,text="現在のレススピード>>")
currentspeed_n_label = ttk.Label(main_frm,text=f"0.0/m",font=("Noto Sans JP","15","bold"))


url_label.grid(column=0,row=0,padx=10)
url_input.grid(column=1,row=0,pady=5)
url_btn.grid(column=2,row=0,padx=10)

currentAnka_label.grid(column=0,row=1,pady=0,sticky=tkinter.E)
currentAnka_n_label.grid(column=1,row=1,sticky=tkinter.W)
currentspeed_label.grid(column=0,row=2,pady=0,sticky=tkinter.E)
currentspeed_n_label.grid(column=1,row=2,sticky=tkinter.W)

addbutton = ttk.Button(anka_frm,text="+",width=3,command=addColums)
textinput = PlaceholderEntry(anka_frm,"ex.名前",width=20)
ankainput = PlaceholderEntry(anka_frm,"ex.100,10-13",width=20)

style = ttk.Style(main_w)
style.configure("Placeholder.TEntry", foreground="#808080")

L1 = ttk.Label(anka_frm,text="備考")
L2 = ttk.Label(anka_frm,text="安価")
L3 = ttk.Label(anka_frm,text="追加")

textinput.grid(column=0,row=1)
ankainput.grid(column=1,row=1)
addbutton.grid(column=2,row=1)

L1.grid(column=0,row=0)
L2.grid(column=1,row=0)
L3.grid(column=2,row=0)

anka_L1 = ttk.Label(anka_w_frm,text="備考")
anka_L2 = ttk.Label(anka_w_frm,text="安価")
anka_L3 = ttk.Label(anka_w_frm,text="--")
anka_L1.grid(column=0,row=0)
anka_L2.grid(column=1,row=0)
anka_L3.grid(column=2,row=0)
sep = ttk.Separator(anka_w_frm,orient="vertical")
#sep.grid(column=0,row=0, sticky="ns")
main_w.after(1000,update)
main_w.after(5000,update_speed)

main_w.mainloop()
anka_w.mainloop()
