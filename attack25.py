# coding: utf-8
'''
Created on 2017/02/17
LastUpdate 2018/1/6
@author: ktair
use python3.6.4

- 見た目
    - ボタン配置
- 使い勝手
    - 実行ファイル化?
'''

import tkinter as tk
from tkinter import messagebox

# 表示サイズ
PANEL_SIZE = 100
PANEL_NUM = 5
MARGIN = 20
CANVAS_SIZE = PANEL_SIZE * PANEL_NUM + MARGIN*2
TEXT_FONT = ('', PANEL_SIZE//2)
# 色設定
DEFAULT_COLOR = "lightgray"
ONCOLOR = "darkgray"
ATTACK_CHANCE_COLOR = 'yellow'
colors = [
    "#ff0000", # 1-red
    "#228b22", # 2-forestgreen
    "#00ffff", # 3-cyan
    "#ffffff", # 4-white
    "#800080", # 5-purple
    "#ffa500", # 6-orange
    "#00ff7f", # 7-springgreen
    "#0000ff", # 8-blue
    "#f5deb3", # 9-wheat
    "#ffc0cb" # 10-pink
]
# チーム名設定
teams = []
try:
    f = open('team.txt', 'r')
    for line in f:
        team = line
        team = team.replace("\n","")
        team = team.replace("\r","")
        team = team.replace("\n\r","")
        teams.append(team)
    f.close()
except:
    teams = [1,2,3,4,5]

root = tk.Tk()
root.config(bg='black')

# 色選択
colorselect = tk.IntVar()
colorselect.set(0)
rectangle_size = CANVAS_SIZE//teams.__len__()
for i in range(teams.__len__()):
    if i < 10:
        color = colors[i]
    else:
        color = colors[i-10]
    tk.Radiobutton(root, text=teams[i], bg=color, variable=colorselect, value=i,font=("",rectangle_size//5)).grid(row=0,column=i)

# 盤面
c0 = tk.Canvas(root, width=CANVAS_SIZE, height=CANVAS_SIZE, bg='black', highlightthickness=0)
c0.grid(row=2,columnspan=teams.__len__())

panels = {}
panelcolor = {}
panel_label = {}
past_panelcolor = {}
is_attackchance = False

# 初期化
def reset():
    for n in range(PANEL_NUM ** 2):
        x = PANEL_SIZE * (n%PANEL_NUM) + MARGIN
        y = PANEL_SIZE * (n//PANEL_NUM) + MARGIN
        panels[n] = c0.create_rectangle(x, y, x+PANEL_SIZE, y+PANEL_SIZE, fill=DEFAULT_COLOR, activefill=ONCOLOR, tag='free')
        panelcolor[n] = DEFAULT_COLOR
        panel_label[n] = c0.create_text(x+(PANEL_SIZE/2),y+(PANEL_SIZE/2),text=str(n+1),font=TEXT_FONT, activefill=ONCOLOR, tag='label')
reset()

# 選択したパネルのID取得
def find_items(id, items):
    for k,v in items.items():
        if v == id:
            return k
# オセロ
def reverse(color):
    selectedpanelid = c0.find_withtag("selected")[0]
    c0.itemconfigure(selectedpanelid, tag="filled")
    selectnum = find_items(selectedpanelid, panels)
    panelcolor[selectnum] = color
    # 探索
    samecolor = []
    for i in range(PANEL_NUM**2):
        if i == selectnum:
            pass
        else:
            if panelcolor[i] == color:
                samecolor.append(i)
    for num in samecolor:
        # 横
        if num//PANEL_NUM == selectnum//PANEL_NUM:
            search(num, color, selectnum, 1)
        # 縦
        if num%PANEL_NUM == selectnum%PANEL_NUM:
            search(num, color, selectnum, PANEL_NUM)
        # 斜め
        if num%(PANEL_NUM+1) == selectnum%(PANEL_NUM+1):
            search(num, color, selectnum, PANEL_NUM+1)
        else:
            if num%(PANEL_NUM-1) == selectnum%(PANEL_NUM-1):
                search(num, color, selectnum, PANEL_NUM-1)
    rescore()
# 同じ色で挟まれたパネルの探索
def search(num, color, selectnum, phase):
    reversepanel = []
    plus = selectnum + phase
    if num > plus:
        while plus < num:
            if panelcolor[plus] == DEFAULT_COLOR:
                c0.itemconfigure("reverse", tag="filled")
                reversepanel = []
                break
            else:
                reversepanel.append(plus)
                c0.itemconfigure(panels[plus], tag="reverse")
            plus += phase
        c0.itemconfigure("reverse", tag="filled", fill=color, activefill=color)
        for x in reversepanel:
            panelcolor[x] = color
    reversepanel = []
    minus = selectnum - phase
    if num < minus:
        while num < minus:
            if panelcolor[minus] == DEFAULT_COLOR:
                c0.itemconfigure("reverse", tag="filled")
                reversepanel = []
                break
            else:
                reversepanel.append(minus)
                c0.itemconfigure(panels[minus], tag="reverse")
            minus -= phase
        c0.itemconfigure("reverse", tag="filled", fill=color, activefill=color)
        for x in reversepanel:
            panelcolor[x] = color
            reversepanel = []
# 塗り替え
def change_color(event):
    backup()
    aftercolor = colors[colorselect.get()]
    c0.itemconfigure('current', fill=aftercolor, tag='selected', activefill=aftercolor)
    reverse(aftercolor)
# アタックチャンス
def set_attackchance(event):
    global is_attackchance
    if is_attackchance:
        backup()
        c0.itemconfigure('current', fill=ATTACK_CHANCE_COLOR, tag='attack', activefill=ATTACK_CHANCE_COLOR)
        attackpanelid = c0.find_withtag('attack')[0]
        attackpanelnum = find_items(attackpanelid, panels)
        panelcolor[attackpanelnum] = ATTACK_CHANCE_COLOR
        rescore()
        c0.itemconfigure('attack', tag='free')
        is_attackchance = False

c0.tag_bind('free', "<Button-1>", change_color)
c0.tag_bind('filled', "<Button-1>", set_attackchance)

# 得点表
c1 = tk.Canvas(root, width=CANVAS_SIZE, height=rectangle_size, bg='black', highlightthickness=0)
c1.grid(row=1, columnspan=teams.__len__())
scores = {}
# 初期表示
for i in range(teams.__len__()):
    if i < 10:
        color = colors[i]
    else:
        color = colors[i-10]
    c1.create_rectangle(i*rectangle_size, 0, (i+1)*rectangle_size, rectangle_size,fill=color)
    count = 0
    for j in range(panelcolor.__len__()):
        if panelcolor[j] == color:
            count += 1
    scores[i] = c1.create_text(i*rectangle_size+rectangle_size/2, rectangle_size/2, text=count,font=('',rectangle_size//2))
# 得点更新
def rescore():
    for i in range(teams.__len__()):
        count = 0
        for j in range(panelcolor.__len__()):
            if panelcolor[j] == colors[i]:
                count += 1
        c1.itemconfigure(scores[i], text=count)

# アタックチャンス
def toggle_attackchance():
    global is_attackchance
    if is_attackchance:
        is_attackchance = False
    else:
        popup_attackchance()
        is_attackchance = True
def popup_attackchance():
    messagebox.showinfo("ATTACK CHANCE", "ATTACK CHANCE")

# 一つ前に戻る
def back():
    if past_panelcolor == {}:
        return
    for n in panelcolor:
        if panelcolor[n] != past_panelcolor[n]:
            back_tag = 'filled'
            back_activefill = past_panelcolor[n]
            if past_panelcolor[n] == DEFAULT_COLOR:
                back_tag = 'free'
                back_activefill = ONCOLOR
            if past_panelcolor[n] == ATTACK_CHANCE_COLOR:
                back_tag='free'
            c0.itemconfigure(panels[n], tag=back_tag, fill=past_panelcolor[n], activefill=back_activefill)
            panelcolor[n] = past_panelcolor[n]
    rescore()
# バックアップをとる
def backup():
    for n in panelcolor:
        past_panelcolor[n] = panelcolor[n]

# アタックチャンスボタン
attackchance_button = tk.Button(root, text='ATTACK CHANCE', command=toggle_attackchance)
attackchance_button.grid(row=3, columnspan=teams.__len__())
# 戻るボタン
back_button = tk.Button(root, text='BACK', command=back)
back_button.grid(row=5, columnspan=1)
# リセットボタン
reset_button = tk.Button(root, text='RESET', command=reset)
reset_button.grid(row=5, columnspan=2)

root.mainloop()
