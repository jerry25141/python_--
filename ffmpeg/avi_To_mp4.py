# %%
import subprocess
import os
import pyautogui
from tkinter import *

import PySimpleGUI as sg

# %% [markdown]
#  獲取目標資料夾內容（FLV）

# %%
file_path = "D://MyCode//Python//ffmpeg//FFmpeg 批量轉檔 範例"
save_path = "D://MyCode//Python//ffmpeg//FFmpeg 批量轉檔 範例//save"

# 或
file_path = sg.popup_get_folder("請輸入《來源》路徑:", keep_on_top=True)
save_path = sg.popup_get_folder("請輸入《目的地》路徑:", keep_on_top=True)
print(f"{file_path}")
print(f"{save_path}")
# 嘗試切換路徑

try:
    os.chdir(file_path)
    print(os.getcwd())
except Exception as e:
    print(f"無路徑或有錯誤")
    print(f"[[ 錯誤訊息 ]]\n{e}")
    
# 如果沒有save folder，嘗試建立
try:
    if "save" not in os.listdir():
        print("生成 save 資料夾")
        os.makedirs(name="save")
except Exception as e:
    pyautogui.alert(text=e)

# %%
name_list = []

# 找尋到 .avi，然後去掉副檔名，存入名稱
for each in os.listdir():
    if each.endswith(".avi"):
        print(each[:-4])
        name_list.append(each[:-4])

# %% [markdown]
#  批次處理檔案至目標

# %%
def run_file_conversion(name):
    name_file = name + ".avi"
    name_output = save_path + "//" + name + ".mp4"
    command_copy = "copy"
    
    # 印出subprocess的指令在輸出中(debug用，有更好的方法
    print(f"【執行指令】\n=======================================================================================\n")
    print(f"ffmpeg -i {name_file} -c {command_copy} {name_output}")
    print("\n=======================================================================================")

    
    subprocess.run(
        [
            "ffmpeg", "-i", name_file, "-c", command_copy, name_output
        ]
    , shell=True)

# %%
subprocess.run(["pause"], shell=True)


try:
    for name in name_list:
        run_file_conversion(name)
        subprocess.run(["pause"], shell=True)
except Exception as e:
    subprocess.run(["pause"], shell=True)
    pyautogui.alert(text=e)


