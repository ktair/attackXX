# coding: utf-8
'''
Created on 2017/02/17
@author: ktair
'''
from Tkinter import *

BOX_SIZE = 80
BOX_NUM = 5
MARGIN = 20
CANVAS_SIZE = BOX_SIZE * BOX_NUM + MARGIN*2
TEXT_FONT = ("","50")

# 色設定
DEFAULT_COLOR = "lightgray"
ONCOLOR = "darkgray"
colors = ['red', 'green', 'blue', 'white', 'yellow', 'brown']
teams = ['Fender', 'Gibson', 'Fernandes', 'Epiphone', 'prs']

root = Tk()
root.config(bg='black')
colorselect = IntVar()
colorselect.set(0)
for i in range(teams.__len__()):
    Radiobutton(bg=colors[i], variable=colorselect, value=i,).grid(row=1,column=i)

# 盤面
c0 = Canvas(root, width=CANVAS_SIZE, height=CANVAS_SIZE, bg='black', highlightthickness=0)
c0.grid(row=2,columnspan=teams.__len__())
boxes = {}
boxcolors = {}
for n in range(BOX_NUM ** 2):
    x = BOX_SIZE * (n%BOX_NUM) + MARGIN
    y = BOX_SIZE * (n/BOX_NUM) + MARGIN
    boxes[n] = c0.create_rectangle(x, y, x+BOX_SIZE, y+BOX_SIZE, fill=DEFAULT_COLOR, activefill=ONCOLOR, tag='free')
    boxcolors[n] = DEFAULT_COLOR
    c0.create_text(x+(BOX_SIZE/2),y+(BOX_SIZE/2),text=str(n+1),font=TEXT_FONT)

def find_items(id, items):
    for k,v in items.items():
        if v == id:
            return k

def reverse(color):
    selectedboxid = c0.find_withtag("selected")[0]
    c0.itemconfigure(selectedboxid, tag="filled")
    selectnum = find_items(selectedboxid, boxes)
    boxcolors[selectnum] = color
    # 探索
    samecolor = []
    for i in range(BOX_NUM**2):
        if i == selectnum:
            pass
        else:
            if boxcolors[i] == color:
                samecolor.append(i)
    for num in samecolor:
        # 横
        if num/BOX_NUM == selectnum/BOX_NUM:
            search(num, color, selectnum, 1)
        # 縦
        if num%BOX_NUM == selectnum%BOX_NUM:
            search(num, color, selectnum, BOX_NUM)
        # 斜め
        if num%(BOX_NUM+1) == selectnum%(BOX_NUM+1):
            search(num, color, selectnum, BOX_NUM+1)
        if num%(BOX_NUM-1) == selectnum%(BOX_NUM-1):
            search(num, color, selectnum, BOX_NUM-1)
    rescore()

def search(num, color, selectnum, phase):
    changecolorbox = []
    plus = selectnum + phase
    if num > plus:
        while plus < num:
            if boxcolors[plus] == DEFAULT_COLOR:
                c0.itemconfigure("reverse", tag="filled")
                changecolorbox = []
                break
            else:
                changecolorbox.append(plus)
                c0.itemconfigure(boxes[plus], tag="reverse")
            plus += phase
        c0.itemconfigure("reverse", tag="filled", fill=color, activefill=color)
        for x in changecolorbox:
            boxcolors[x] = color
    changecolorbox = []
    minus = selectnum - phase
    if num < minus:
        while num < minus:
            if boxcolors[minus] == DEFAULT_COLOR:
                c0.itemconfigure("reverse", tag="filled")
                changecolorbox = []
                break
            else:
                changecolorbox.append(minus)
                c0.itemconfigure(boxes[minus], tag="reverse")
            minus -= phase
        c0.itemconfigure("reverse", tag="filled", fill=color, activefill=color)
        for x in changecolorbox:
            boxcolors[x] = color
            changecolorbox = []

def change_color(event):
    aftercolor = colors[colorselect.get()]
    c0.itemconfigure('current', fill=aftercolor, tag="selected", activefill=aftercolor)
    reverse(aftercolor)

c0.tag_bind('free', "<Button-1>", change_color)

# 得点表
rectangle_size = CANVAS_SIZE/teams.__len__()
c1 = Canvas(root, width=CANVAS_SIZE, height=rectangle_size, bg='black', highlightthickness=0)
c1.grid(row=0, columnspan=teams.__len__())
scores = {}
# 初期表示
for i in range(teams.__len__()):
    c1.create_rectangle(i*rectangle_size, 0, (i+1)*rectangle_size, rectangle_size,fill=colors[i])
    count = 0
    for j in range(boxcolors.__len__()):
        if boxcolors[j] == colors[i]:
            count += 1
    scores[i] = c1.create_text(i*rectangle_size+rectangle_size/2, rectangle_size/2, text=count,font=TEXT_FONT)
    c1.create_text(i*rectangle_size+rectangle_size/2, 10, text=teams[i],font=("","20"))

def rescore():
    for i in range(teams.__len__()):
        count = 0
        for j in range(boxcolors.__len__()):
            if boxcolors[j] == colors[i]:
                count += 1
        c1.itemconfigure(scores[i], text=count)

root.mainloop()
