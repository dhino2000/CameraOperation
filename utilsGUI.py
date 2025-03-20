# tkinter GUI用
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import numpy as np
import cv2
import os
import re
import time
from utils import *
from PIL import Image, ImageTk
    
"""Entry"""
# Entryの作成 ラベル付き
def createEntry(key, frame, entry_dict, row, column, text, entry_width=20, label_width=20, pad=10, rowspan=1, columnspan=1, textvariable=None, grid="horizontal", label_dict=None):
    label = tk.Label(frame, text=text, width=label_width)
    entry = tk.Entry(frame, width=entry_width, textvariable=textvariable)
    if grid == "horizontal": # 左にlabel, 右にentry配置
        label.grid(row=row, column=column, padx=pad, pady=pad)
        entry.grid(row=row, column=column+1, padx=pad, pady=pad, rowspan=rowspan, columnspan=columnspan)
    elif grid == "vertical": # 上にlabel, 下にentry配置
        label.grid(row=row, column=column, padx=pad, pady=pad)
        entry.grid(row=row+1, column=column, padx=pad, pady=pad, rowspan=rowspan, columnspan=columnspan)
    entry_dict[key] = entry
    if label_dict: # label_dictに保存するか
        label_dict[key] = label
    
# 選択したフォルダパスをentryに表示
def chooseDir(entry):
    dir = filedialog.askdirectory()
    entry.delete(0, tk.END)
    entry.insert(tk.END, dir)
    
# 選択したファイルをentryに表示
def chooseFile(entry, fTypes):
    fType = [] # ex) fType = ("mp4", "avi")
    for fTyp in fTypes:
        fType.append(("", f"*.{fTyp}"))
    filedir = filedialog.askopenfilename(filetypes=fType)
    # 選択したファイルのパスをentryに表示
    entry.delete(0, tk.END)
    entry.insert(tk.END, filedir)
    
# Entryが空である場合に注意喚起
def warnEntryEmpty(entry, title, text):
    if len(entry.get()) == 0:
        messagebox.showwarning(title, text)
        return True
    else:
        return False
# Entryが空である場合にチェック
def checkEntryEmpty(entry, title, text):
    if len(entry.get()) == 0:
        result = messagebox.askokcancel(title, text)
    else:
        result = True
    return result
    
"""Button"""
# ボタンの作成
def createButton(key, frame, button_dict, row, column, text, command, pad=10, rowspan=1, columnspan=1, state=tk.NORMAL):
    button = tk.Button(frame, text=text, command=command, state=state)
    button.grid(row=row, column=column, padx=pad, pady=pad, rowspan=rowspan, columnspan=columnspan)
    button_dict[key] = button
    
"""Pulldown"""
# プルダウンメニューの作成 ラベル付き
def createPulldown(key, frame, pulldown_dict, row, column, text, values, pulldown_width=20, pad=10, rowspan=1, columnspan=1, textvariable=None, grid="horizontal"):
    label = tk.Label(frame, text=text)
    pulldown = ttk.Combobox(frame, values=values, width=pulldown_width)
    if textvariable:
        pulldown.set(textvariable)
    if grid == "horizontal": # 左にlabel, 右にpulldown配置
        label.grid(row=row, column=column, padx=pad, pady=pad)
        pulldown.grid(row=row, column=column+1, padx=pad, pady=pad, rowspan=rowspan, columnspan=columnspan)
    elif grid == "vertical": # 上にlabel, 下にpulldown配置
        label.grid(row=row, column=column, padx=pad, pady=pad)
        pulldown.grid(row=row+1, column=column, padx=pad, pady=pad, rowspan=rowspan, columnspan=columnspan)
    pulldown_dict[key] = pulldown
    
"""Listbox"""
# リストボックスの作成
def createListbox(key, frame, listbox_dict, row, column, listbox_width=20, listbox_height=10, pad=10, rowspan=1, columnspan=1, selectmode="EXTENDED"):
    selectmode_dict = {"SINGLE":tk.SINGLE, "BROWSE":tk.BROWSE, "MULTIPLE":tk.MULTIPLE, "EXTENDED":tk.EXTENDED}
    listbox = tk.Listbox(frame, width=listbox_width, height=listbox_height, selectmode=selectmode_dict[selectmode])
    listbox.grid(row=row, column=column, padx=pad, pady=pad, rowspan=rowspan, columnspan=columnspan, sticky="nsew")
    listbox_dict[key] = listbox
    # スクロールバーのセット
    scrollbar_x = tk.Scrollbar(frame, orient="horizontal")
    scrollbar_y = tk.Scrollbar(frame, orient="vertical")
    scrollbar_x.grid(row=row+rowspan, column=column, sticky="we")
    scrollbar_y.grid(row=row, column=column+columnspan, sticky="ns")
    listbox.configure(xscrollcommand=scrollbar_x.set, yscrollcommand=scrollbar_y.set)
    scrollbar_x.config(command=listbox.xview)
    scrollbar_y.config(command=listbox.yview)
    # フレームの行と列のサイズを動的に変更
    frame.grid_rowconfigure(row, weight=1)
    frame.grid_columnconfigure(column, weight=1)
    
# リストボックス初期化
def clearListbox(listbox):
    listbox.delete(0, tk.END)
# リストボックス内の要素を削除
def deleteListbox(listbox):
    # インデックスが大きいものから削除するため、逆順にソートする
    for index in sorted(listbox.curselection(), reverse=True):
        listbox.delete(index)
# 選択した要素を１つ上に移動する
def moveUpOfListbox(listbox):
    # 選択された要素のインデックスを取得
    selected_indices = listbox.curselection()
    if not selected_indices:
        return
    index = selected_indices[0]
    # 選択された要素が一番上でない場合、要素を上に移動
    if index > 0:
        value = listbox.get(index)
        listbox.delete(index)
        listbox.insert(index-1, value)
        listbox.select_set(index-1)
# 選択した要素を１つ下に移動する
def moveDownOfListbox(listbox):
    # 選択された要素のインデックスを取得
    selected_indices = listbox.curselection()
    if not selected_indices:
        return
    index = selected_indices[0]
    # 選択された要素が一番下でない場合、要素を下に移動
    if index < listbox.size() - 1:
        value = listbox.get(index)
        listbox.delete(index)
        listbox.insert(index+1, value)
        listbox.select_set(index+1)

# リストボックスが空である場合に注意喚起
def warnListboxEmpty(listbox, title, text):
    if listbox.size() == 0:
        messagebox.showwarning(title, text)
        return True
    else:
        return False
    
# 選択したフォルダの下流にあるプロジェクトフォルダを取得してlistboxに表示
def getProjectDirectoriesAndShowListbox(listbox, list_str_include=None, list_str_exclude=None, match_include="and", match_exclude="or"):
    listbox_items = listbox.get(0, tk.END) # リストボックス内の全要素
    dir_ = filedialog.askdirectory() # フォルダ選択
    pipeline_src_project = getProjectDirectories(dir_) # プロジェクトフォルダ
    
    pipeline_src_dirs_video = []
    # プロジェクトフォルダの下流にあるフォルダを取得する場合
    if list_str_include or list_str_exclude:
        for src_project in pipeline_src_project:
            src_dirs = getAllSubDirectories(src_project)
            src_dirs = getMatchedPaths(src_dirs, list_str_include, list_str_exclude, match_include, match_exclude)
            for src_dir in src_dirs:
                pipeline_src_dirs_video.append(src_dir)
    # プロジェクトフォルダのみの場合
    else:
        for src_project in pipeline_src_project:
            pipeline_src_dirs_video.append(src_project)
    for dir in pipeline_src_dirs_video:
        if dir not in listbox_items: # 重複は避ける
            listbox.insert(tk.END, dir)
            
# 選択したフォルダの下流にあるフォルダを取得してlistboxに表示
def getDirectoriesAndShowListbox(listbox, depth=None, list_str_include=None, list_str_exclude=None, match_include="and", match_exclude="or"):
    listbox_items = listbox.get(0, tk.END) # リストボックス内の全要素
    dir_ = filedialog.askdirectory() # フォルダ選択
    dirs = getAllSubDirectories(dir_, depth) # 下流のフォルダ(depth指定の場合は探索を制限)
    if list_str_include or list_str_exclude:
        dirs = getMatchedPaths(dirs, list_str_include, list_str_exclude, match_include, match_exclude)
    
    for dir_ in dirs:
        if dir_ not in listbox_items: # 重複は避ける
            listbox.insert(tk.END, dir_)
    
# パイプライン用リストボックス
# 選択したフォルダの下流にあるプロジェクトフォルダ(関数は指定可能)をすべて取得する
def listboxPipeline(gui, frame_inputdir, frame_inputdir_listbox, row, column, key="pipeline_src", pad=10, listbox_width=60, listbox_height=10, selectmode="SINGLE", 
                    list_str_include=None, list_str_exclude=None, match_include="and", match_exclude="or"):
    createListbox(key=f"{key}", frame=frame_inputdir_listbox, listbox_dict=gui.listbox_dict,
                  row=row, column=column, listbox_width=listbox_width, listbox_height=listbox_height, pad=pad, selectmode=selectmode)
    createButton(key=f"{key}", frame=frame_inputdir, button_dict=gui.button_dict,
                 row=row, column=column+1, text="browse", 
                 command=lambda: getProjectDirectoriesAndShowListbox(gui.listbox_dict[key], list_str_include, list_str_exclude, match_include, match_exclude))
    createButton(key=f"{key}_delete", frame=frame_inputdir, button_dict=gui.button_dict,
                 row=row+1, column=column+1, text="delete", 
                 command=lambda: deleteListbox(listbox=gui.listbox_dict[key]))
    createButton(key=f"{key}_clear", frame=frame_inputdir, button_dict=gui.button_dict,
                 row=row+2, column=column+1, text="clear", 
                 command=lambda: clearListbox(listbox=gui.listbox_dict[key]))

"""Label"""
# # ラベルの作成
# def createLabel(key, frame, label_dict, row, column, text, pad=10, rowspan=1, columnspan=1, textvariable=None):
#     label = tk.Label(frame, text=text, textvariable=textvariable)
#     label.grid(row=row, column=column, padx=pad, pady=pad, rowspan=rowspan, columnspan=columnspan)
#     label_dict[key] = label

def createLabel(key, frame, label_dict, row, column, text, pad=10, rowspan=1, columnspan=1, **kwargs):
    # ラベルウィジェットの作成（kwargsを使用して、任意の追加引数を指定）
    label = tk.Label(frame, text=text, **kwargs)
    label.grid(row=row, column=column, padx=pad, pady=pad, rowspan=rowspan, columnspan=columnspan)
    # ラベルを太字にするには、font引数に"weight"オプションを指定します。
    # 例：createLabel(..., font=("Helvetica", 12, "bold"))
    label_dict[key] = label
    
# ラベルの更新
def updateLabel(label, text, color):
    label.config(text=text, fg=color)
# dict, keyをもとにラベル更新
def updateLabelwithKey(label, key, text_dict, status_dict):
    text = text_dict[key][status_dict[key]]["text"]
    color = text_dict[key][status_dict[key]]["color"]
    updateLabel(label, text, color)
    
# FPSの表示
def showFPS(t_array, label):
    if len(t_array) == 0:
        pass
    else:
        fps = 1 / np.mean(np.diff(t_array))
        label["text"] = f"{fps:.2f} fps"
    
"""Checkbutton"""
# Checkbuttonの作成 ラベル付き
def createCheckbutton(key, frame, checkbutton_dict, row, column, text, pad=10, rowspan=1, columnspan=1, check=False):
    label = tk.Label(frame, text=text)
    label.grid(row=row, column=column, padx=pad, pady=pad)
    if check:
        var = tk.IntVar(value=1)
    else:
        var = tk.IntVar(value=0)
    checkbutton = tk.Checkbutton(frame, variable=var)
    checkbutton.grid(row=row, column=column+1, padx=pad, pady=pad, rowspan=rowspan, columnspan=columnspan)
    checkbutton_dict[key] = {}
    # チェックボックスから直接状態を取得できないので分けて保存
    checkbutton_dict[key]["checkbutton"] = checkbutton
    checkbutton_dict[key]["var"] = var


"""Canvas"""
# スクロール用
def onFrameConfigure(event, canvas):
    canvas.configure(scrollregion=canvas.bbox("all"))
def onMouseWheel(event, canvas):
    canvas.yview_scroll(-1*(event.delta//120), "units")
    
# 画像crop用のモジュール
def initializeCanvasCropImage(gui, frame, row, column, rowspan=1, columnspan=1, width=1280, height=1024, key_canvas="window", key_window="main"):
    # cropした範囲 (x_min, x_max, y_min, y_max)
    gui.cropcoords = np.array(())
    # crop設定
    gui.start_x, gui.start_y = 0, 0
    gui.rect_id = None
    
    # "Window"項目の作成
    gui.canvas_dict[key_canvas] = tk.Canvas(frame, width=width, height=height, bg="black")
    gui.canvas_dict[key_canvas].grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan)
    
    # ドラッグで画像をクロップ
    def onCanvasClick(event):
        gui.start_x = event.x
        gui.start_y = event.y
        if gui.rect_id:
            gui.canvas_dict[key_canvas].delete(gui.rect_id)
    def onCanvasDrag(event):
        if gui.rect_id:
            gui.canvas_dict[key_canvas].delete(gui.rect_id)
        gui.rect_id = gui.canvas_dict[key_canvas].create_rectangle(gui.start_x, gui.start_y, event.x, event.y, outline="red")
    def onCanvasRelease(event, entry=None):
        gui.cropcoords = (gui.start_x, event.x, gui.start_y, event.y)
        if entry:
            # entryの書き換え
            entry.delete(0, tk.END)  # Entryの中身を消去
            entry.insert(tk.END, str(gui.cropcoords))  # 新しいテキストを挿入
            
    # delキーで四角を消す
    def onCanvasDelete(event):
        if gui.rect_id:
            gui.canvas_dict[key_canvas].delete(gui.rect_id)
            gui.cropcoords = np.array(())

    # キャンバスのドラッグ設定
    gui.canvas_dict[key_canvas].bind("<Button-1>", onCanvasClick)
    gui.canvas_dict[key_canvas].bind("<B1-Motion>", onCanvasDrag)
    gui.canvas_dict[key_canvas].bind("<ButtonRelease-1>", lambda event: onCanvasRelease(event, entry=gui.entry_dict["cropcoords"]))
    # delキーで四角を消す
    gui.window_dict[key_window].bind("<Delete>", onCanvasDelete)
# crop範囲を指定
def setCropcoords(gui, entry, canvas):
    if gui.rect_id:
        canvas.delete(gui.rect_id)
    entry_get = entry.get()

    if len(entry_get) > 0:
        try:
            gui.cropcoords = tuple(int(c) for c in entry_get.replace(" ","").replace("(","").replace(")","").split(","))
            # entryの書き換え
            entry.delete(0, tk.END)  # Entryの中身を消去
            entry.insert(tk.END, str(gui.cropcoords))  # 新しいテキストを挿入
            xmin, xmax, ymin, ymax = gui.cropcoords
            gui.rect_id = canvas.create_rectangle(xmin, ymin, xmax, ymax, outline="red")
        except ValueError:
            messagebox.showwarning("Crop coords check", "Set cropcoords correctly ! \n (ex) (100, 300, 200, 400)")
    else:
        gui.cropcoords = np.array(())
# canvasの初期化
def resetCanvas(canvas, width=1280, height=1024):
    blackframe = Image.new("RGB", (width, height), "black")
    blackframe = ImageTk.PhotoImage(blackframe)
    canvas.config(width=width, height=height)
    canvas.create_image(0, 0, anchor=tk.NW, image=blackframe)
    canvas.image = blackframe
# 動画の1フレーム目を表示
def showFirstFrame(video, canvas):
    # arrayをPIL形式に変更してさらにTKinter PhotoImageに変換
    im = video[0]
    im = Image.fromarray(im)
    im = ImageTk.PhotoImage(im)

    # ラベルに画像を表示
    canvas.config(width=im.width(), height=im.height())
    canvas.create_image(0, 0, anchor=tk.NW, image=im)
    canvas.image = im

"""Figure"""


"""Notebook(タブ)"""



"""Video"""
# 動画を読み込む
def readVideo(path_video, color=False):
    cap = cv2.VideoCapture(path_video)
    if cap.isOpened():
        num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))

        # 動画のフレームを格納するNumPy配列を作成
        video = np.empty((num_frames, frame_height, frame_width), dtype=np.uint8)

        frame_idx  = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            #グレースケールに変換
            if not color:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            video[frame_idx] = frame

            frame_idx  += 1
            # 10000フレームごとに表示
            if frame_idx  % 10000 == 0:
                print(f"{frame_idx} frames loaded !")
    return video

# 動画を再生
def playVideo(video, fps=60, cropcoords=None):
    if len(video) > 0:
        wait = 1 / float(fps)
        window_title = "Esc : Stop playing video"
        # 元動画は白黒であるが、表示の場合はカラーで
        # 重たい動画ではメモリオーバーとなるため、3000フレームのみ表示する
        if len(video) > 3000:
            video = video[:3000].copy()
        else:
            video = video.copy()
        video = np.stack((video, video, video), axis=-1)

        for i, im in enumerate(video):
            # cropがあればそれも描画
            if not cropcoords == None:
                rect_coords = ((cropcoords[0], cropcoords[2]), (cropcoords[1], cropcoords[3]))
                im = cv2.rectangle(im, rect_coords[0], rect_coords[1], (0, 0, 255), 2)
            cv2.imshow(window_title, im)
            time.sleep(wait) # fps
            # Escキーで中断
            if cv2.waitKey(1) & 0xFF == 27:
                break
#             # プロットがあれば動かす
#             if self.status_dict["hog"]:
#                 self.window_dict["main"].after(1, self.plotUpdate, i)
        cv2.destroyAllWindows()

"""Window"""

# windowの作成, コンフィグ等の設定
def initializeWindow(gui, width, height, title, pad=10, entry_config_width=20, entry_dir_width=60, listbox_width=60, listbox_height=10, debug=False, toplevel=False):
    # ディレクトリ
    gui.parentdir = os.path.abspath(os.path.dirname("__file__")).replace("\\", "/")
    
    # window, notebook, canvas, frame, figureのdict
    gui.window_dict = defaultdictRecursive()
    gui.notebook_dict = defaultdictRecursive()
    gui.canvas_dict = defaultdictRecursive()
    gui.frame_dict = defaultdictRecursive()
    gui.figure_dict = defaultdictRecursive()

    # GUIウィンドウを作成
    if toplevel: # 従属のウィンドウであるか
        gui.window_dict["main"] = tk.Toplevel()
    else:
        gui.window_dict["main"] = tk.Tk()
    gui.window_dict["main"].geometry(f"{width}x{height}")
    gui.window_dict["main"].title(title)

    # スクロール用のキャンバス、フレーム
    gui.canvas_dict["main"] = tk.Canvas(gui.window_dict["main"], borderwidth=0)
    gui.scrollbar_x = tk.Scrollbar(gui.window_dict["main"], orient="horizontal", command=gui.canvas_dict["main"].xview)
    gui.scrollbar_y = tk.Scrollbar(gui.window_dict["main"], orient="vertical", command=gui.canvas_dict["main"].yview)
    gui.frame_dict["main"] = tk.Frame(gui.canvas_dict["main"])

    # Configure the scrollbars to the canvas view
    gui.canvas_dict["main"].configure(xscrollcommand=gui.scrollbar_x.set, yscrollcommand=gui.scrollbar_y.set)
    gui.canvas_dict["main"].grid(row=0, column=0, sticky="nsew")
    gui.scrollbar_x.grid(row=1, column=0, sticky="ew")
    gui.scrollbar_y.grid(row=0, column=1, sticky="ns")

    # Make the canvas expandable
    gui.window_dict["main"].grid_rowconfigure(0, weight=1)
    gui.window_dict["main"].grid_columnconfigure(0, weight=1)

    gui.canvas_dict["main"].create_window((0,0), window=gui.frame_dict["main"], anchor="nw")
    gui.frame_dict["main"].bind("<Configure>", lambda event: onFrameConfigure(event, gui.canvas_dict["main"]))
    gui.canvas_dict["main"].bind_all("<MouseWheel>", lambda event: onMouseWheel(event, gui.canvas_dict["main"]))

    # 余白
    gui.pad = 10

    # エントリーの横幅
    gui.entry_config_width, gui.entry_dir_width = entry_config_width, entry_dir_width

    # リストボックスの横幅、縦幅
    gui.listbox_width, gui.listbox_height = listbox_width, listbox_height

    # entry, button, pulldown, label, listbox, checkbuttonのdict
    gui.entry_dict = defaultdictRecursive()
    gui.button_dict = defaultdictRecursive()
    gui.pulldown_dict = defaultdictRecursive()
    gui.label_dict = defaultdictRecursive()
    gui.listbox_dict = defaultdictRecursive()
    gui.checkbutton_dict = defaultdictRecursive()
    
    gui.debug = debug

    
# 終了
def exitGUI(gui):
    if gui.debug:
        gui.window_dict["debug"].destroy()
    gui.window_dict["main"].destroy()
    


    
# デバッグ用
# 指定した変数を表示する
class VariableInspector:
    def __init__(self, class_parent, title="Variable Inspector"):
        # 変数を受け取る元のクラス
        self.class_parent = class_parent
        self.entry_dict = {}
        self.button_dict = {}
        self.window = tk.Tk()
        self.window.title(title)
        self.frame = tk.Frame(self.window, width=100, height=100, bd=2, relief="groove")
        
        # フレームの配置
        self.frame.grid(row=0, column=0)
        createEntry(key="variable", frame=self.frame, entry_dict=self.entry_dict,
                         row=0, column=0, text="Variable:", entry_width=50)
        createButton(key="variable", frame=self.frame, button_dict=self.button_dict,
                          row=0, column=2, text="print", 
                          command=lambda: self.printVariable(entry=self.entry_dict["variable"]))
        
        # ×ボタンを押しても消さない
        self.window.protocol("WM_DELETE_WINDOW", self.doNothing)
        
    # 変数をprint
    def printVariable(self, entry):
        var = entry.get()
        code = f"print(self.class_parent.{var})"
        print(var)
        exec(code)
        
    def destroy(self):
        self.window.destroy()
        
    def doNothing(self):
        pass