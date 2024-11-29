# %%
import PySimpleGUI as sg

# %% [markdown]
# ## 官網示範

# %%

sg.theme('DarkAmber')   # Add a touch of color

# 視窗內所有物件
layout = [  [sg.Text('這是用來相加的程式')],
            [sg.InputText(size=(3)), sg.Text('+'), sg.InputText(size=(3))],
            [sg.Button('Ok'), sg.Button('Cancel')] ]

# 建立視窗
window = sg.Window('視窗', layout, font=('微軟正黑體',15), keep_on_top=True)
# 事件循環處理“事件”並獲取輸入的“值”
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel': # 如果視窗被關掉
        break
    # values 輸出的是 dict，所以print要使用values[key]

    # 1 #   印出 values[0]資料
    # print('You entered ', values[0])

    # 2 #   印出資料
    # for each in values:
    #     print('You entered ', values[each])

    # 3 #   彈出視窗顯示答案
    ans = int(values[0]) + int(values[1])
    sg.Popup(f"ans = {ans}", keep_on_top=True)

window.close()

# %% [markdown]
# ## popup 視窗展示

# %%
# sg.popup('Popup')  # Shows OK button
# sg.popup_ok('PopupOk')  # Shows OK button
# sg.popup_yes_no('PopupYesNo')  # Shows Yes and No buttons
# sg.popup_cancel('PopupCancel')  # Shows Cancelled button
# sg.popup_ok_cancel('PopupOKCancel')  # Shows OK and Cancel buttons
# sg.popup_error('PopupError')  # Shows red error button
# sg.popup_timed('PopupTimed')  # Automatically closes
sg.popup_auto_close('PopupAutoClose',auto_close_duration=3)  # Same as PopupTimed

# %%
text = '123456789\nabcdefg\n\n\nH\ne\nl\nl\no\n_\nW\no\nr\nl\nd'
sg.popup_scrolled(text, size=(20, None), font=('微軟正黑體', 15), keep_on_top=True)

# %% [markdown]
# ### Popup檔案路徑

# %%
msg = '請選擇檔案'
text = sg.popup_get_file(msg, size=(
    20, None), font=('微軟正黑體', 15), keep_on_top=True)

print(text)

# %% [markdown]
# ### Popup資料夾路徑

# %%
msg = '請選擇資料夾'
text = sg.popup_get_folder(msg, size=(
    20, None), font=('微軟正黑體', 15), keep_on_top=True)

print(text)

# %% [markdown]
# ## Progress 進度顯示

# %%
from time import sleep

title_msg = "進度顯示視窗"

for i in range(1,100):
    sg.OneLineProgressMeter(title_msg, current_value=i+1, max_value=100,
                            orientation='h', no_button=True, keep_on_top=True)
    sleep(0.05)

# %% [markdown]
# ## EZ Print 簡易輸出
# ### (Jupyter 需要使用 PrintClose()來正常關閉，py 或 cli 會自動關閉)

# %%
for i in range(100):
    sg.Print(i)

sg.PrintClose()

# %%
print = sg.Print    # 直接覆蓋原始python的方法
for i in range(100):
    print(i)

sg.PrintClose()

# %% [markdown]
# # 【Test】

# %%
import PySimpleGUI as sg

sg.theme('Dark Blue 3')  # please make your windows colorful

layout = [[sg.Text('Rename files or folders')],
      [sg.Text('Source for Folders', size=(15, 1)), sg.InputText(), sg.FolderBrowse()],
      [sg.Text('Source for Files ', size=(15, 1)), sg.InputText(), sg.FileBrowse()],
      [sg.Submit(button_text="上傳"), sg.Cancel()]]

window = sg.Window('Rename Files or Folders', layout, keep_on_top=True)

event, values = window.read()
window.close()
folder_path, file_path = values[0], values[1]       # get the data from the values dictionary
print(folder_path, file_path)


