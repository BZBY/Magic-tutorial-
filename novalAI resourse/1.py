# 这是一个示例 Python 脚本。

# 按 Shift+F10 执行或将其替换为您的代码。
# 按 双击 Shift 在所有地方搜索类、文件、工具窗口、操作和设置。
import os
import urllib.request
from pathlib import Path
import re
import time
import requests


# 通过资源路径获取里面的所有URL路径
def find_url(url):
    headers = {
        'authority': 'www.acgns.org',
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9',
        # Requests sorts cookies= alphabetically
        # 'cookie': '__cf_bm=gC0rbWuOyA_EodsFzlA8gSt9Q6CR46yyAZjcOWTAxFs-1669104468-0-AYz21sPFinaX2gc01fy+/OYMR2bVlGe9GRUaBHceukrAMYEAX0vsePJqdzKj/WMLN7zCVnOtVvA156fc+Hv+spbnuvKUok4/uBxnzK3DmBTi/jIlG5DepIsvxNJzLG5GkHdTqyv96MMmwJrWXGRDTzU=; CA_VID_SSL=1669104495896218; CA_RF5_SSL=ffef995a46ae59bd; CA_LVT_SSL=1669104495896218; CA_VSD_SSL=20221122; CA_VV_SSL=4.1.4.1; CA_LAT_SSL=1669105509283; CA_PPI_SSL=05254a895af67ffa-1669105509283-1669104861659579',
        'referer': url,
        'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
    }

    file_url_list = []

    webData = requests.get(url, headers=headers)

    time.sleep(1)
    text = webData.text

    http_url_list = re.findall('"http.*?"', text)
    for http_url in http_url_list:
        strs = http_url.split()
        if len(strs) != 1:
            for i in strs:
                url = i
                if len(i) > 10:
                    if url.find('.png') != -1 or url.find('.jpg') != -1:
                        # http_url 字符串两头中包含了 " 号，需要截取掉
                        tmp = url[1:]
                        cnt = 0
                        if tmp.rfind('.png') == -1:
                            cnt = tmp.rfind('.jpg')
                        else:
                            cnt = tmp.rfind('.png')
                        if cnt == 0 or cnt == -1:
                            print("图片格式url截取 bug1")
                            print(url)
                            continue
                        file_url_list.append(tmp[:cnt + 4])
            continue
        # 找到 jpg 和 png 扩展名的 url
        if http_url.find('.png') != -1 or http_url.find('.jpg') != -1:
            # http_url 字符串两头中包含了 " 号，需要截取掉
            tmp = http_url[1:-1]
            cnt = 0
            if tmp.rfind('.png') == -1:
                cnt = tmp.rfind('.jpg')
            else:
                cnt = tmp.rfind('.png')
            if cnt == 0 or cnt == -1:
                print("图片格式url截取 bug2")
                continue
            file_url_list.append(tmp[:cnt + 4])
    print('URL 获取完毕...')
    ans = []
    for i in file_url_list:
        if i[0] != 'h':
            i = str('h') + str(i)
        ans.append(i)
    return ans


# 根据图片的资源路径下载图片到本地
def download_by_url(urls, url):
    headers = {
        'authority': 'www.acgns.org',
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9',
        # Requests sorts cookies= alphabetically
        # 'cookie': '__cf_bm=gC0rbWuOyA_EodsFzlA8gSt9Q6CR46yyAZjcOWTAxFs-1669104468-0-AYz21sPFinaX2gc01fy+/OYMR2bVlGe9GRUaBHceukrAMYEAX0vsePJqdzKj/WMLN7zCVnOtVvA156fc+Hv+spbnuvKUok4/uBxnzK3DmBTi/jIlG5DepIsvxNJzLG5GkHdTqyv96MMmwJrWXGRDTzU=; CA_VID_SSL=1669104495896218; CA_RF5_SSL=ffef995a46ae59bd; CA_LVT_SSL=1669104495896218; CA_VSD_SSL=20221122; CA_VV_SSL=4.1.4.1; CA_LAT_SSL=1669105509283; CA_PPI_SSL=05254a895af67ffa-1669105509283-1669104861659579',
        'referer': url,
        'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
    }
    cnt = 1
    for i in urls:
        cnt += 1
        picType = i[-4:]
        response = requests.get(i, headers=headers).content
        with open(str(cnt) + picType, 'wb') as f:
            f.write(response)
        time.sleep(1)

url = "https://www.acgns.org/72631"
k = find_url(url)
download_by_url(k, url)
