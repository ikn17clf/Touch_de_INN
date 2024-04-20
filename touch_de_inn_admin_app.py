import tkinter as tk
import binascii
import nfc
import os
from oauth2client.service_account import ServiceAccountCredentials
import gspread

# 設定
json_file = 'touch-de-inn-e5b296c3bc22.json'
file_name = 'タッチでINN'
sheet_name = 'list'
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

def change_main():
    frame.tkraise()
    entry_realname_frame_del1.delete(0,tk.END)
    entry_handlename_frame_del1.delete(0,tk.END)

def change_reg1():
    frame_reg1.tkraise()

def change_reg2():
    frame_reg2.tkraise()

def change_del():
    def del_button():
        delete_num = []
        for i in range(people):
            if check_val[i].get():
                delete_num.append(i)
        for i in reversed(delete_num):
            people2 = int(wks.cell(1, 2).value)
            for j in range(people2-i-1):
                wks.update_cell(i+3+j, 1, wks.cell(i+4+j, 1).value)
                wks.update_cell(i+3+j, 2, wks.cell(i+4+j, 2).value)
                wks.update_cell(i+3+j, 3, wks.cell(i+4+j, 3).value)
            wks.update_cell(2+people2, 1, "")
            wks.update_cell(2+people2, 2, "")
            wks.update_cell(2+people2, 3, "")
            wks.update_cell(1, 2, str(people2-1))
        sub_win.destroy()

    sub_win = tk.Toplevel()
    sub_win.geometry("600x300")
    label_sub = tk.Label(sub_win, text="ユーザー削除画面")
    label_sub.pack()
    # スプレッドシートにアクセスする
    credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file, scope)
    gc = gspread.authorize(credentials)
    sh = gc.open(file_name)
    wks = sh.worksheet(sheet_name)
    people = int(wks.cell(1, 2).value) # 現在の登録人数を取得

    check_val = {}
    check_btn = {}
    for i in range(people):
        check_val[i] = tk.BooleanVar(sub_win)
        check_btn[i] = tk.Checkbutton(sub_win,text=wks.cell(3+i, 1).value +","+ wks.cell(3+i, 2).value +"," + wks.cell(3+i, 3).value, variable=check_val[i])
        check_btn[i].pack()
    button = tk.Button(sub_win,text="削除する", command=del_button)
    button.pack()
    
def ic_read():
    clf = nfc.ContactlessFrontend('usb')
    try:
        tag = clf.connect(rdwr={'on-connect': lambda tag: False})
    finally:
        clf.close()
    idm = binascii.hexlify(tag._nfcid)

    # スプレッドシートにアクセスする
    credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file, scope)
    gc = gspread.authorize(credentials)
    sh = gc.open(file_name)
    wks = sh.worksheet(sheet_name)
    people = int(wks.cell(1, 2).value) # 現在の登録人数を取得
    wks.update_cell(people+3, 1, entry_realname_frame_del1.get())
    wks.update_cell(people+3, 2, entry_handlename_frame_del1.get())
    wks.update_cell(people+3, 3, idm.decode())
    wks.update_cell(1, 2, str(people+1))

    frame.tkraise()
    entry_realname_frame_del1.delete(0,tk.END)
    entry_handlename_frame_del1.delete(0,tk.END)

if __name__ == "__main__":
    # rootメインウィンドウの設定
    root = tk.Tk()
    root.title("tkinter application")
    root.geometry("600x300")

    # rootメインウィンドウのグリッドを 1x1 にする
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    # メインフレームの作成と設置
    frame = tk.Frame(root)
    frame.grid(row=0, column=0, sticky="nsew", pady=20)

    # メインフレームの各種ウィジェットの作成
    label_frame = tk.Label(frame, text="タッチでINN！URC 管理アプリ")
    button_reg = tk.Button(frame, text="ユーザー登録", command=change_reg1)
    button_del = tk.Button(frame, text="ユーザー削除", command=change_del)

    # メインフレームの各種ウィジェットの設置
    label_frame.pack()
    button_reg.pack()
    button_del.pack()

    # 登録フレーム1の作成と設置
    frame_reg1 = tk.Frame(root)
    frame_reg1.grid(row=0, column=0, sticky="nsew", pady=20)

    # 登録フレーム1の各種ウィジェットの作成
    label_frame_reg1 = tk.Label(frame_reg1, text="登録ウィンドウ1")
    label_real_frame_reg1 = tk.Label(frame_reg1, text="本名を入力してください\n(例)Kentaro Inamura")
    entry_realname_frame_del1 = tk.Entry(frame_reg1)
    label_handle_frame_reg1 = tk.Label(frame_reg1, text="ハンドルネームを入力してください\n(例)inaken")
    entry_handlename_frame_del1 = tk.Entry(frame_reg1)
    button_change_to_2_frame_reg1 = tk.Button(frame_reg1, text="次へ進む", command=change_reg2)
    button_change_to_main_frame_reg1 = tk.Button(frame_reg1, text="最初に戻る", command=change_main)

    # 登録フレーム1の各種ウィジェットの設置
    label_frame_reg1.pack()
    label_real_frame_reg1.pack()
    entry_realname_frame_del1.pack()
    label_handle_frame_reg1.pack()
    entry_handlename_frame_del1.pack()
    button_change_to_2_frame_reg1.pack()
    button_change_to_main_frame_reg1.pack()

    # 登録フレーム2の作成と設置
    frame_reg2 = tk.Frame(root)
    frame_reg2.grid(row=0, column=0, sticky="nsew", pady=20)

    # 登録フレーム2の各種ウィジェットの作成
    label_frame_reg2 = tk.Label(frame_reg2, text="登録ウィンドウ2")
    label_real_frame_reg2 = tk.Label(frame_reg2, text="ICカードを読み取ります．Felicaをセットしてください．")
    button_change_to_3_frame_reg2 = tk.Button(frame_reg2, text="ICカードを読み取る", command=ic_read)
    button_change_to_main_frame_reg2 = tk.Button(frame_reg2, text="最初に戻る", command=change_main)

    # 登録フレーム2の各種ウィジェットの設置
    label_frame_reg2.pack()
    label_real_frame_reg2.pack()
    button_change_to_3_frame_reg2.pack()
    button_change_to_main_frame_reg2.pack()

    # メインフレームを前面にする
    frame.tkraise()

    root.mainloop()