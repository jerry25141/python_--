from tkinter import filedialog
from tkinter import messagebox
from lxml import html
from glob import glob
import tkinter as tk
import threading
import requests
import time
import re
import os
import json
import random
import urllib.request
from PIL import Image

###############################################################
# 實例化object，建立視窗root
root = tk.Tk()
root.title('DLsite重命名工具 HHH v3.5')  # 給視窗的標題取名字
root.eval('tk::PlaceWindow . center')

# jerry ADD 嘗試置中視窗
window_width = root.winfo_screenwidth()    # 取得螢幕寬度
window_height = root.winfo_screenheight()  # 取得螢幕高度
width = 350
height = 520
left = int((window_width - width)/2)       # 計算左上 x 座標
top = int((window_height - height)/2)      # 計算左上 y 座標
root.geometry(f'{width}x{height}+{left}+{top}')

text = tk.Text(root)
text.pack()

###############################################################
# 默認設定
template_RJ = 'workno title '  # 默認RJ命名模板(Voice)
template_BJ = 'workno title '  # 默認BJ命名模板(Comic)
template_VJ = 'workno title '  # 默認VJ命名模板(Game)

replace_rules = []  # 替換規則

RJ_WEBPATH = 'https://www.dlsite.com/maniax/work/=/product_id/'
RJ_G_WEBPATH = 'https://www.dlsite.com/home/work/=/product_id/'
BJ_WEBPATH = 'https://www.dlsite.com/books/work/=/product_id/'
BJ_G_WEBPATH = 'https://www.dlsite.com/comic/work/=/product_id/'
VJ_WEBPATH = 'https://www.dlsite.com/pro/work/=/product_id/'
VJ_G_WEBPATH = 'https://www.dlsite.com/soft/work/=/product_id/'
R_COOKIE = {'adultchecked': '1'}

###############################################################
# jerry ADD變數
new_name_for_cover = ""
img_codec_type = ".jpg"
img_url_list = []
cover_id_code = 1
root_dir = os.getcwd()
replace_rules_cover_img = []   # cover img 替換規則
template_Hgame      = 'workno title '  # 默認Hgame命名模板
template_Asmr       = 'workno title '  # 默認Asmr命名模板
template_Video      = 'workno title '  # 默認Video命名模板
# 設定預設 work_type_var
working_type = tk.StringVar()    
working_type.set("Hgame")       # 類型選擇 Hgame ASMR Video
###############################################################
# 通用 def #
def get_working_type():
    ans_working_type = str(working_type.get())
    return ans_working_type

###############################################################
# re.compile()返回一個匹配對像
# ensure path name is exactly RJ?(\d{8}d{7}d{6}) or BJ?(\d{8}d{7}d{6}) or VJ?(\d{8}d{7}d{6})
pattern = re.compile("([BRV][EJ])?(\d{8}|\d{7}|\d{6})")
# filter to substitute illegal filenanme characters to " "
filter = re.compile('[\\\/:"*?<>|]+')


# 避免ERROR: Max retries exceeded with url
requests.adapters.DEFAULT_RETRIES = 5  # 增加重連次數
s = requests.session()
s.keep_alive = False  # 關閉多餘連接
# s.get(url) # 你需要的網址

# 查找母串內所有子串的位置, 查找失敗返回-1

# Random User Agent List
USER_AGENT_LIST = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    ]

USER_AGENT = random.choice(USER_AGENT_LIST)
headers = {
    'user-agent': USER_AGENT
}

###############################################################
# tkinter 輸出文字 #
def txt_insert_fun(msg="", auto_rn=True):
    """
    這段程式碼嘗試將訊息插入文字小部件中，並將捲軸位置定位到最後。如果發生任何例外，程式碼會將例外訊息印出。
    
    Arg 参数：
        msg (str): tkinter中輸出的字串
        auto_rn(bool, optional): 是否自動修正前後 換行
    """
    try:
        # 檢查頭尾是否為 \n
        if auto_rn == True:
            if msg.startswith('\n') != True:
                msg = f'\n{msg}'
            if msg.endswith('\n') != True:
                msg = f'{msg}\n'
        text.insert(tk.END, msg)
        text.yview(tk.END)
    except Exception as e:
        print(f"{e}")

###############################
# 把字串半形轉全形
def strB2Q(s):
    rstring = ""
    for uchar in s:
        u_code = ord(uchar)
        if u_code == 32:  # 全形空格直接轉換
            u_code = 12288
        elif 33 <= u_code <= 126:  # 全形字元（除空格）根據關係轉化
            u_code += 65248
        rstring += chr(u_code)
    return rstring

###############################
def match_code(product_item_code):
    # requests函示庫是一個常用於http請求的模組
    if product_item_code[0] == "R":
        url = RJ_WEBPATH + product_item_code
    if product_item_code[0] == "B":
        url = BJ_WEBPATH + product_item_code
    if product_item_code[0] == "V":
        url = VJ_WEBPATH + product_item_code
    try:
        # allow_redirects=False 禁止重定向
        r = s.get(url, allow_redirects=False, cookies=R_COOKIE, headers=headers)
        # HTTP狀態碼==200表示請求成功
        if r.status_code != 200:
            #print("    Status code:", r.status_code, "\nurl:", url)
            try:
                ## 改成一般向網址
                if product_item_code[0] == "R":
                    url = RJ_G_WEBPATH + product_item_code
                if product_item_code[0] == "B":
                    url = BJ_G_WEBPATH + product_item_code
                if product_item_code[0] == "V":
                    url = VJ_G_WEBPATH + product_item_code
                r = s.get(url, allow_redirects=False, cookies=R_COOKIE)
                if r.status_code != 200:
                    return r.status_code, "", "", "", [], [], "", "", ""
            except os.error as err:
                txt_insert_fun("\n**請求超時!\n")
                txt_insert_fun("\n**請檢查網絡連接\n")
                return "", "", "", "", [], [], "", "", ""

        # fromstring()在解析xml格式時, 將字串轉換為Element對像, 解析樹的根節點
        # 在python中, 對get請求返回的r.content做fromstring()處理, 可以方便進行後續的xpath()定位等
        tree = html.fromstring(r.content)
        
        try:
            #  嘗試寫看看，有多少張範例照片就載多少張
            global img_url_list
            img_url_list = []
            

            my_xpath = f'//ul[@class="slider_items trans"]/li/picture/source/@srcset'
            ans_xpath = tree.xpath(my_xpath)
            
            img_url_main = f"https:{ans_xpath[0]}"
            img_url_list.append(img_url_main) # 添加 main img進去
            # print(img_url_main)
            url_pattern = re.search(r"^.*\/", img_url_main).group(0)


            try:
                n_imgs = 20
                for i in range(1, n_imgs+1):
                    img_url = f"{url_pattern}{
                        product_item_code}_img_smp{i}.jpg"
                    # print(img_url)

                    if s.get(img_url).status_code == 200:
                        img_url_list.append(img_url)
                    else:
                        break
            except Exception as e:
                print(f"{e}")
            
                    
        except os.error as err:
            txt_insert_fun("\n**作品封面不存在!\n")
            img_url = ""
        title = tree.xpath('//h1[@id="work_name"]/text()')[0]
        circle = tree.xpath(
            '//span[@itemprop="brand" and @class="maker_name"]/*/text()')[0]
        cvList = tree.xpath(
            '//*[@id="work_outline"]/tr/th[contains(text(), "声優")]/../td/a/text()')
        authorList = tree.xpath(
            '//*[@id="work_maker"]/tr/th[contains(text(), "著者")]/../td/a/text()')
        type = tree.xpath(
            '//*[@id="work_outline"]/tr/th[contains(text(), "作品形式")]/../td/div/a/span/text()')[0]
        # 精簡遊戲類型
        game_type_list = ["アクション", "クイズ", "アドベンチャー", "ロールプレイング", "テーブル", "デジタルノベル", "シミュレーション", "タイピング", "シューティング", "パズル", "その他ゲーム"]
        if type in game_type_list:
            type = "ゲーム"
        
        work_age = tree.xpath(
            '//*[@id="work_outline"]/tr/th[contains(text(), "年齢指定")]/../td/div/a/span/text()')
        if not work_age:
            work_age = tree.xpath(
                '//*[@id="work_outline"]/tr/th[contains(text(), "年齢指定")]/../td/div/span/text()')
        release_date = tree.xpath(
            '//*[@id="work_outline"]/tr/th[contains(text(), "販売日")]/../td/a/text()')[0]
        # 精簡日期: 20ab年cd月ef日 => abcdef
        if len(release_date) >= 11:
            release_date = release_date[2]+release_date[3]+release_date[5]+release_date[6]+release_date[8]+release_date[9]

        return 200, img_url, title, circle, cvList, authorList, work_age[0], release_date, type

    except os.error as err:
        txt_insert_fun("\n**請求超時!\n")
        txt_insert_fun("\n**請檢查網絡連接\n")
        return "", "", "", "", [], [], "", "", ""

###############################
# 轉換 jpg to webp ， 並刪除舊的jpg檔案 #
def convert_jpg_to_webp(input_dir, output_dir, quality=80):
    """
    將指定輸入目錄中的所有 JPG 圖像轉換為 WebP 格式，並保存在輸出目錄中。

    Arg 参数：
        input_dir (str): 包含 JPG 圖像的輸入目錄路徑。
        output_dir (str): 保存 WebP 圖像的輸出目錄路徑。
        quality (int, optional): WebP 圖像的品質 (0-100，數值越高品質越好)。默認值為 80。
    """

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    msg = f"\n執行刪除轉換中...\n"
    txt_insert_fun(msg)
    del_count = 0
    filename_list = os.listdir(input_dir)
    
    for filename in filename_list:
        if filename.endswith('.jpg'):
            del_count += 1
            
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename.replace('.jpg', '.webp'))

            try:
                image = Image.open(input_path)
                image = image.convert('RGB')  # WebP doesn't support other modes
                image.save(output_path, 'WEBP', quality=quality)
                # 嘗試刪除
                try:
                    # 如果存在 > 刪除檔案
                    if os.path.exists(input_path):
                        # 使用 `os.remove()` 函數刪除檔案
                        os.remove(input_path)
                        msg = f"({del_count})"
                        # print(msg)
                        txt_insert_fun(msg,False)
                    else:
                        msg = f"<!{del_count}!>"
                        # print(msg)
                        txt_insert_fun(msg,False)

                except Exception as e:
                    print(f"\n!!刪除失敗...!!\n")
            except Exception as e:
                print(f"錯誤 Failed to convert {input_path}: {e}")
                messagebox.showinfo(title="錯誤", message=f"{e}" + "\n")

###############################
def nameChange():
    # askdirectory()檔案對話框, 選擇目錄, 返回目錄名
    path = filedialog.askdirectory()
    if path == "":
        messagebox.showinfo(title="錯誤", message="請選擇路徑!" + "\n")
    else:
        # 重新讀取configs
        cbtn_deltext.config(state=tk.DISABLED)
        cbtn_dlcover.config(state=tk.DISABLED)
        cbtn_recursive.config(state=tk.DISABLED)
        btn.config(state=tk.DISABLED)
        btn['text'] = "等待完成"
        txt_insert_fun("《選擇路徑》: " + path + "\n")
        # os.listdir()返回指定的資料夾包含的檔案或資料夾的名字的列表
        if recursive.get(): # 遞迴檢索
            files = [y for x in os.walk(path) for y in glob(os.path.join(x[0], '*'))]
        else: # 根目錄檢索
            files = os.listdir(path)
            
        for file in files:
            if recursive.get(): # 遞迴檢索需要修正路徑
                path = os.path.split(file)[0]
            
            # 嘗試獲取code
            code_list = re.findall(pattern, file.upper())[0]
            # 如果無法獲取 RJ code(之類的) or 不是資料夾
            if code_list  == None:
                break
            code = ''.join(code_list)
            
            # 如果提取到code 且 是資料夾
            file_dir = os.path.join(path, file)
            print(f"Working on...:\n{file_dir}")
            if code and os.path.isdir(file_dir) == True:   # 檢查 code + 是資料夾 
                #print('Processing: ' + code)
                msg = '\n*------------------' + '\nProcessing: ' + code + '\n'
                txt_insert_fun(msg)
                r_status, img_url, title, circle, cvList, authorList, work_age, release_date, type = match_code(code)
                # 如果順利爬取網頁訊息
                if r_status == 200 and title and circle:
                    if deltext.get():
                        # 刪除title中的【.*?】
                        title = re.sub(u"\\【.*?】", "", title)

                    if code[0] == "R":
                        new_name = template_RJ.replace("workno", code)
                    if code[0] == "B":
                        new_name = template_BJ.replace("workno", code)
                    if code[0] == "V":
                        new_name = template_VJ.replace("workno", code)
                
                    new_name = new_name.replace("title", title)
                    new_name = new_name.replace("circle", circle)
                    new_name = new_name.replace("work_age", work_age)
                    new_name = new_name.replace("release_date", release_date)
                    new_name = new_name.replace("type", type)

                    author = ""
                    if authorList:  # 如果authorList非空
                        for name in authorList:
                            author += "," + name
                        new_name = new_name.replace("author", author[1:])
                    else:
                        new_name = new_name.replace("(author)", "")  

                    cv = ""
                    if cvList:  # 如果cvList非空
                        for name in cvList:
                            cv += "," + name
                        new_name = new_name.replace("cv", cv[1:])
                    else:
                        new_name = new_name.replace("(CV. cv)", "")
                        
                    #####################
                    # 加入 Cover 命名規則 #
                    #####################

                    # 1. 將Windows文件名中的非法字元替換成空白
                    # re.sub(pattern, repl, string)
                    # new_name = re.sub(filter, " ", new_name)

                    # 1. 將Windows文件名中的非法字元替換成全形
                    # re.match(pattern, string, flags=0)
                    fixed_filename = "";
                    for char in new_name:
                        if re.match(filter, char):
                            fixed_filename += strB2Q(char)
                        else:
                            fixed_filename += char
                            
                    # 2. 多空格轉單空格
                    new_name = ' '.join(fixed_filename.split())
                    

                    ######################
                    # 加入 多個封面 且是資料夾 #
                    ######################
                    
                    if dlcover.get() and img_url and os.path.isdir(os.path.join(path, file)):
                        try:
                            
                            def generage_cover_img(img_url, cover_id=1, if_dl_cover_error = False):
                                try:
                                    # 嘗試下載封面
                                    if cover_id == 1:
                                        # cover_filename = f"{code}_cover{img_codec_type}"
                                        img_filename = ""
                                        # cover 檔案名稱 命名 + 置換
                                        if if_dl_cover_error == True:
                                            img_filename = "(01)" + img_codec_type
                                        elif get_working_type() == "Hgame":
                                            img_filename = "(01)" + img_codec_type
                                        elif get_working_type() == "ASMR":
                                            img_filename = "(01)" + img_codec_type
                                        elif get_working_type() == "Video":
                                            img_filename = "(01)" + img_codec_type
                                        txt = f"\n*-- 下載封面 --*\n{img_filename}\n"
                                        txt_insert_fun(txt)
                                    
                                    # 在數字前加上0
                                    elif cover_id < 10:
                                        img_filename = f"(0{cover_id}){img_codec_type}"
                                    else:
                                        img_filename = f"({cover_id}){img_codec_type}"
                                    
                                    # 儲存路徑
                                    store_path = os.path.join(path, file, img_filename)
                                    
                                    # 下載  imgs 檔案 # 
                                    if not os.path.isfile(store_path):
                                        # 下載進度更新
                                        txt = f"({cover_id})"
                                        txt_insert_fun(txt,False)

                                        # 下載 #
                                        # urllib.request.urlretrieve(img_url, store_path)
                                        r = requests.get(img_url)
                                        with open(store_path, 'wb') as f:
                                            f.write(r.content)

                                    # 如果封面已經存在，跳過
                                    else:
                                        txt = f"\n**封面 ({cover_id}) 已存在，跳過下載!\n"
                                        txt_insert_fun(txt)
                                
                                except Exception as e:
                                    # 如果出現錯誤，嘗試備案
                                    print(f"\nError jerry's code 0\n錯誤訊息:\n{e}\n")
                                    print("命名失敗，嘗試使用 (01)img 命名備案")
                                    return False
                                
                            #######################
                            # 依序下載所有cover圖片 #
                            #######################
                            try:
                                cover_id = 0
                                tmp_working_type = get_working_type()
                                # # ASMR cover以外跳過
                                # if tmp_working_type == "ASMR": break                                        
                                # # Video folder以外跳過
                                # if tmp_working_type == "Video": break
                                
                                # 嘗試抓取所有圖片
                                for img_url in img_url_list:
                                    cover_id += 1
                                    if generage_cover_img(img_url, cover_id) == False:
                                        # 如果有錯誤就用備案
                                        generage_cover_img(img_url, cover_id, True)
                                    
                            except Exception as e:
                                print(f"\nError jerry's code 1\n錯誤訊息:\n{e}\n")
                            
                            #########################
                            # 轉換jpg to webp 並刪除 #
                            #########################
                            try:
                                dir_path = os.path.join(path, file)
                                convert_jpg_to_webp(dir_path,dir_path)
                            except Exception as e:
                                msg = f"\n**轉換 + 刪除過程中出現錯誤!\n"
                                print(msg)
                                txt_insert_fun(msg)
                        
                        except os.error as err:
                            txt_insert_fun("\n**下載封面過程中出現錯誤!\n")
                    
                    
                    ##################
                    # 加入URL連結檔案 #
                    ##################
                    try: # 嘗試加入URL連結檔案
                        store_path = os.path.join(path, file, code + "_link" +".url")
                        if not os.path.isfile(store_path):
                            txt_insert_fun("\n  建立URL檔...\n")
                            target_url = "www.dlsite.com/maniax/work/=/product_id/" + code
                            # 寫檔，寫入url格式(windows可用)
                            with open(store_path, 'w', encoding="utf-8") as f:
                                f.write('[InternetShortcut]\n')
                                f.write('URL=%s' % target_url)
                        else:
                            txt_insert_fun("\n--URL已存在，跳過建立!\n")
                    except os.error as err:
                        txt_insert_fun("\n--建立URL過程中出現錯誤!\n")
                    
                    ##################

                    # 嘗試重命名
                    try:
                        # strip() 去掉字串兩邊的空格
                        if os.path.isfile(os.path.join(path, file)):  # 如果是檔案
                            temp, file_extension = os.path.splitext(file)
                            os.rename(os.path.join(path, file),
                                    os.path.join(path, new_name.strip()+file_extension))
                        else:  # 如果是資料夾
                            os.rename(os.path.join(path, file),
                                    os.path.join(path, new_name.strip()))
                    except os.error as err:
                        txt_insert_fun("\n**重命名失敗!\n")
                        msg = "  " + os.path.join(path, file) + "\n"
                        txt_insert_fun(msg)
                        txt_insert_fun("\n**請檢查是否存在重複的名稱\n")
                elif r_status == 404:
                    txt_insert_fun("\n**爬取DLsite過程中出現錯誤!\n")
                    txt_insert_fun("\n**請檢查本作是否已經下架或被收入合集\n")
                elif r_status != "":
                    txt_insert_fun("\n**爬取DLsite過程中出現錯誤!\n")
                    txt_insert_fun("  網頁 URL: " +
                                RJ_WEBPATH + code + "\n")
                    txt_insert_fun("  HTTP 狀態碼: " +
                                str(r_status) + "\n")

                # set delay to avoid being blocked from server
                time.sleep(0.1)
        # print("~Finished.")
        txt_insert_fun("*******完成!*******\n\n\n\n")
        tk.messagebox.showinfo(title="提示", message="完成!")

        cbtn_deltext.config(state=tk.NORMAL)
        cbtn_dlcover.config(state=tk.NORMAL)
        cbtn_recursive.config(state=tk.NORMAL)
        btn.config(state=tk.NORMAL)
        btn['text'] = "選擇路徑"

###############################
def thread_it(func, *args):
    '''將函數打包進線程'''
    # 建立
    t = threading.Thread(target=func, args=args, daemon=True)
    # 守護 !!!
    # t.setDaemon(True)
    # 啟動
    t.start()
    # 阻塞--卡死界面！
    # t.join()

###############################
# 讀取配置文件
# os.path.dirname(__file__) 當前腳本所在路徑
def read_config():
    global template_RJ, template_BJ, template_VJ
    basedir = os.path.abspath(os.path.dirname(__file__))
    try:
    # 根據類別，選擇不同config # 類型選擇 Hgame ASMR Video
        if get_working_type() == "Hgame":
            config_fname = os.path.join(basedir, 'config_Hgame.json')
            print(f"{config_fname=}")
        
        elif get_working_type() == "ASMR":
            config_fname = os.path.join(basedir, 'config_ASMR.json')
            print(f"{config_fname=}")

        elif get_working_type() == "Video":
            config_fname = os.path.join(basedir, 'config_Video.json')
            print(f"{config_fname=}")
        
        else:   # 有問題，使用預設Hgame
            print(f"找不到 config 程序有誤，使用預設 Hgame設定")
            config_fname = os.path.join(basedir, 'config_Hgame.json')
    
        with open(config_fname, 'r', encoding='utf-8') as f:
            config = json.load(f)
            for tag in config['replace_rules']:  
                if ("workno" in tag['to']): # 模板非空
                    if tag['type'] == "rj":
                        txt_insert_fun("\n**使用自定義RJ命名模板:\n")
                        template_RJ = tag['to']
                        text.insert(tk.END, "  " + template_RJ.strip() + "\n\n")
                    if tag['type'] == "bj":
                        txt_insert_fun("\n**使用自定義BJ命名模板:\n")
                        template_BJ = tag['to']
                        txt_insert_fun("  " + template_BJ.strip() + "\n\n")
                    if tag['type'] == "vj":
                        txt_insert_fun("\n**使用自定義VJ命名模板:\n")
                        template_VJ = tag['to']
                        txt_insert_fun("  " + template_VJ.strip() + "\n\n")
                else:
                    txt_insert_fun("\n**模板格式錯誤: 模板中必須包含\"workno\"!\n")
                    txt_insert_fun("  使用默認命名模板:\n")
                    txt_insert_fun("  workno title \n\n")
                    
    except os.error as err:
    # 生成配置文件
        print(f"\n!生成配置文件!\n")
        json_data = {
        "replace_rules":
        [
            {
                "type": "rj",
                "from": "",
                "to": "workno title "
            },
            {
                "type": "bj",
                "from": "",
                "to": "workno title "
            },
            {
                "type": "vj",
                "from": "",
                "to": "workno title "
            }
        ]
    }
        with open(config_fname, "w", encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, sort_keys=False,indent=4)
            txt_insert_fun("\n**使用默認命名模板:\n")
            txt_insert_fun("  workno title \n")

read_config()

##########################################################
# jerry add config cover img name seting #
def read_config_cover():
    global template_Hgame, template_Asmr, template_Video
    basedir = os.path.abspath(os.path.dirname(__file__))
    try:
        f_name = os.path.join(basedir, 'config_by_jerry.json')
        with open(f_name, "r", encoding='utf-8') as f:
            config_jerry = json.load(f)
        
            for tag in config_jerry['replace_rules_cover_img']:
                if   tag['fileType'] == 'Hgame':
                    txt_insert_fun("\n**使用Jerry自定義Hgame命名模板:\n")
                    template_Hgame = tag['to']
                    txt_insert_fun("  " + template_Hgame.strip() + "\n\n")
                elif tag['fileType'] == 'Asmr':
                    txt_insert_fun("\n**使用Jerry自定義Asmr命名模板:\n")
                    template_Asmr = tag['to']
                    txt_insert_fun(template_Asmr.strip() + "\n\n")
                elif tag['fileType'] == 'Video':
                    txt_insert_fun("\n**使用Jerry自定義Video命名模板:\n")
                    template_Video = tag['to']
                    txt_insert_fun("  " + template_Video.strip() + "\n\n")
                
        # TODO 寫好 修好 replace_rules_cover_img 沒有正常作用在cover的問題
        # 1.確保 非空,2.確保 type == list,3.確保 len是否大於零
            if config_jerry["replace_rules_cover_img"] and type(config_jerry["replace_rules_cover_img"]) == list and len(config_jerry["replace_rules_cover_img"]):
                replace_rules_cover_img = config_jerry["replace_rules_cover_img"]

    except Exception as e:
        messagebox.showinfo(title="錯誤", message=f"{e}" + "\n")

read_config_cover()

##########################################################

deltext = tk.IntVar()  # 定義整數變數用來存放選擇行為返回值
dlcover = tk.IntVar()
recursive = tk.IntVar()
deltext.set(1)
dlcover.set(1)
recursive.set(0)

###############################################################
# 選擇不同 worktype 按鈕建立 #
frame = tk.Frame(root)
frame.pack()

def btn_fun(txt):
    # 重新讀取configs
    text.delete(0.0, tk.END)
    read_config()
    read_config_cover()
    print(txt)

# 建立 radiobuttons 來表示 不同 worktype
# 類型選擇 Hgame ASMR Video
radio1 = tk.Radiobutton(frame, text="Hgame", variable=working_type, value="Hgame",  command=lambda: btn_fun(working_type.get()))
radio1.grid(row=0, column=0)
radio2 = tk.Radiobutton(frame, text="ASMR", variable=working_type, value="ASMR",    command=lambda: btn_fun(working_type.get()))
radio2.grid(row=0, column=1)
radio3 = tk.Radiobutton(frame, text="Video", variable=working_type, value="Video",  command=lambda: btn_fun(working_type.get()))
radio3.grid(row=0, column=2)

cbtn_deltext = tk.Checkbutton(root, text='去除title中【】之間的內容', variable=deltext,
                      onvalue=1, offvalue=0)  # 傳值原理類似於radiobutton物件
cbtn_dlcover = tk.Checkbutton(root, text='下載封面', variable=dlcover,
                      onvalue=1, offvalue=0)
cbtn_recursive = tk.Checkbutton(root, text='遞迴檢索', variable=recursive,
                      onvalue=1, offvalue=0)                    

btn = tk.Button(root, text='選擇路徑', command=lambda: thread_it(nameChange))

###############################################################

btn.pack()
cbtn_deltext.pack()
cbtn_dlcover.pack()
cbtn_recursive.pack()

root.mainloop()
