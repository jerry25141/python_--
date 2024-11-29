## PySimpleGUI 功能測試

套件連結: [PySimpleGUI](https://www.pysimplegui.com/)

![PySimpleGUI](https://www.pysimplegui.com/assets/front/home-page/img/header.png)

### 安裝套件
```python
pip install PySimpleGUI
```

### 簡介
PySimpleGUI 使用 Python 快速輕鬆地創建圖形使用者介面 （GUI）

### 功能
* **使用者介面：** 提供直觀的輸入框和按鈕。
* **彈出視窗：** 顯示計算結果。
* **檔案選擇：** 可選擇檔案或資料夾。
* **進度條：** 顯示進度條（此功能在範例中未被直接使用於計算機功能，但可作為參考）。

### 程式碼 功能
* 加法程式
```python

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
```

* `sg.Popup`：顯示彈出視窗。
```python
sg.popup('Popup')  # 顯示 OK 按鈕
sg.popup_ok('PopupOk')  # 顯示 OK 按鈕
sg.popup_yes_no('PopupYesNo')  # 顯示 是 和 否 按鈕
sg.popup_cancel('PopupCancel')  # 顯示 取消 按鈕
sg.popup_ok_cancel('PopupOKCancel')  # 顯示 OK 和 取消 按鈕
sg.popup_error('PopupError')  # 顯示紅色的錯誤按鈕
sg.popup_timed('PopupTimed')  # 自動關閉
sg.popup_auto_close('PopupAutoClose',auto_close_duration=2)  # 同 PopupTimed
```

* `sg.popup_get_file`、`sg.popup_get_folder`：選擇檔案或資料夾。
```python

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
```

* `sg.OneLineProgressMeter`：顯示進度條。
```python
from time import sleep

title_msg = "進度顯示視窗"

for i in range(1,50):
    sg.OneLineProgressMeter(title_msg, current_value=i+1, max_value=100,
                            orientation='h', no_button=True, keep_on_top=True)
    sleep(0.05)
```
