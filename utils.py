#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.io
from collections import defaultdict
import paramiko

import re
import os
import sys
import tkinter.filedialog
import tkinter

# 何層下でも一気に定義する事が可能なdefaultdict
def defaultdictRecursive():
    return defaultdict(defaultdictRecursive)

# 指定したディレクトリの下流のすべてのディレクトリのパスを取得
# 下る階層数を指定することも可能
def getAllSubDirectories(path, depth=None):
    dirs_sub = [dirpath.replace("\\", "/") for dirpath, dirnames, filenames in os.walk(path)] # \\ -> /
    if type(depth) == int:
        sep_num = len(path.rsplit("/")) # 基準となるフォルダの階層数
        sep_thresh = sep_num + depth
        dirs_sub = [dirpath for dirpath in dirs_sub if len(dirpath.rsplit("/")) <= sep_thresh]
    return dirs_sub

# 指定したディレクトリの下流のすべてのファイルのパスを取得
def getAllSubFiles(path, depth=None):
    paths_sub = []
    sep_num = len(path.rsplit("/")) # 基準となるフォルダの階層数
    for root, dirs, files in os.walk(path):
        for file in files:
            path = os.path.join(root, file).replace("\\", "/")
            if type(depth) == int:
                sep_thresh = sep_num + depth
                if len(path.rsplit("/")) <= sep_thresh:
                    paths_sub.append(path)
            else:
                paths_sub.append(path)
    return paths_sub

# 指定したフォルダのサブディレクトリリストから正規表現を用いてプロジェクトディレクトリのみを選択
def getProjectDirectories(path, depth=None):
    dirs_sub = getAllSubDirectories(path, depth)
    dirs_project = []
    for dir_sub in dirs_sub:
        # パスを分割
        dir_split = dir_sub.split("/")[-4:]
        if len(dir_split) != 4:
            continue
        dir1, dir2, dir3, dir4 = dir_split
        # 条件を確認 database, database_MultiMod, 230224, IM07,
        if re.match("^\d{6}$", dir4) and re.match("^[a-zA-Z]{2}\d{2}$", dir3) and dir2.startswith("database_") and dir1=="database":
            dirs_project.append(dir_sub)
    return dirs_project

# リストのすべての文字列を含む(and)、あるいは1つでも含む(or)パスのみを選択
# 除外検索も可能
# case_sensitive=Trueで大文字小文字を区別する
# def getMatchedPaths(list_path, list_str_include=None, list_str_exclude=None, match_include="and", match_exclude="or", case_sensitive=True):
#     assert match_include in ("and", "or"), "match_include must be either 'and' or 'or'"
#     assert match_exclude in ("and", "or"), "match_exclude must be either 'and' or 'or'"
#     # デフォルトのリストを空のリストとして設定
#     if list_str_include is None:
#         list_str_include = []
#     if list_str_exclude is None:
#         list_str_exclude = []
    
#     list_match_path = []
#     for path in list_path:
#         # 大文字小文字の区別が不要な場合、すべての文字列を小文字に変換
#         if not case_sensitive:
#             path = path.lower()
#             list_str_include = [s.lower() for s in list_str_include]
#             list_str_exclude = [s.lower() for s in list_str_exclude]
            
#         include_condition = True
#         # match_include条件に基づいて文字列を含むパスを選択
#         if list_str_include:
#             if match_include == "and":
#                 include_condition = all(s in path for s in list_str_include)
#             elif match_include == "or":
#                 include_condition = any(s in path for s in list_str_include)
#         # match_exclude条件に基づいて文字列を含まないパスを選択
#         exclude_condition = False
#         if list_str_exclude:
#             if match_exclude == "and":
#                 exclude_condition = all(s in path for s in list_str_exclude)
#             elif match_exclude == "or":
#                 exclude_condition = any(s in path for s in list_str_exclude)
#         # 指定した文字列を含むパスと含まないパスの両方を選択
#         if include_condition and not exclude_condition:
#             list_match_path.append(path)

#     return list_match_path

# 正規表現にも対応
def getMatchedPaths(list_path, list_str_include=None, list_str_exclude=None, match_include="and", match_exclude="or", case_sensitive=True):
    if list_str_include is None:
        list_str_include = []
    if list_str_exclude is None:
        list_str_exclude = []

    re_flags = 0 if case_sensitive else re.IGNORECASE
    list_str_include = [re.compile(s, re_flags) for s in list_str_include]
    list_str_exclude = [re.compile(s, re_flags) for s in list_str_exclude]

    list_match_path = []
    for path in list_path:
        path_lower = path.lower() if not case_sensitive else path

        include_condition = True
        if list_str_include:
            include_condition = all(pattern.search(path_lower) for pattern in list_str_include)
        
        exclude_condition = False
        if list_str_exclude:
            exclude_condition = any(pattern.search(path_lower) for pattern in list_str_exclude)

        if include_condition and not exclude_condition:
            list_match_path.append(path)

    return list_match_path

# trialの番号に従ってsort, sorted()のkeyとして使用
def sortTrial(string):
    match = re.search(r"trial(\d+)", string)
    if match:
        return int(match.group(1))
    return 0

# list, valueを受け取り、listの要素のうち最もvalueに使いインデックスの要素を1, それ以外は0で返す
def extractNearestValueFromList(list_, target):
    # targetがnanの時はnanのarrayを返す
    if np.isnan(target):
        result = np.array([np.nan for i in range(len(list_))])
    else:
        # 最も近い値のインデックスを逆順リストから見つける
        nearest_index = len(list_) - np.abs(np.array(list_[::-1]) - target).argmin() - 1
        # 条件を満たす最大のインデックスだけを1で返す
        result = np.array([1 if i == nearest_index else 0 for i in range(len(list_))])
    return result

# プロジェクトフォルダ内のセッション数のカウント
def countSessionSet(dir_project):
    set_session = []

    # "_(1桁の数字)-"の正規表現
    re_pattern = r'(.*)_(\d)-(.*)'

    for dir_ in os.listdir(dir_project):
        try:
            session_num = re.match(re_pattern, dir_).group(2)
            set_session += [int(session_num)]
        except AttributeError:
            pass

    set_session = set(set_session)
    return set_session

# 指定のセッションにおけるトライアル数のカウント
def countTrialSet(dir_session):
    set_trial = []

    # "trial"の後に続く数字だけを抽出する正規表現パターン
    re_pattern = r'trial(\d+)'

    # リストの各要素に対して正規表現を適用
    for dir_ in os.listdir(dir_session):
        match = re.findall(re_pattern, dir_)
        if match:
            set_trial.append(int(match[0]))  # findallはリストを返すため、その先頭要素（マッチした数字）を追加

    set_trial = set(set_trial)
    return set_trial

# プロジェクトフォルダおよびその下流のパスからexperiment, mouse, dateを抽出する
def extractExperimentMouseDateFromString(path):
    # ①/database_{experiment}/を抽出してexperimentを取り出す
    experiment = re.search(r'/database_(.*?)/', path).group(1)
    # ②/mouse/を抽出してmouseを取り出す
    mouse = re.search(r'/([A-Za-z]{2}\d{2})/', path).group(1)
    # ③/date/を抽出してdateを取り出す
    date = re.search(r'/(\d{6})/', path).group(1)
    return experiment, mouse, date

"""
SSH Connection
"""
# SSH接続で接続先のマシンのpyファイルを実行させる(主にラズパイ)
def executePythonWithSSH(pyfilename, hostname='raspberrypiNIPS553.local', port=22, username='pi', password = 'pi'):
    # nohupを使用してバックグラウンドで実行し、出力をリダイレクト
    command = f'nohup python3 /home/pi/Desktop/RaspberryPi/{pyfilename}.py > /home/pi/Desktop/SSH/{pyfilename}_output.log 2>&1 &'

    # SSH接続
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # 初回接続時のホストキーを自動的に受け入れる
    ssh.connect(hostname, port, username, password)

    # コマンドの実行
    stdin, stdout, stderr = ssh.exec_command(command)

    # 接続の終了
    ssh.close()

    print("Command has been executed in the background.")
