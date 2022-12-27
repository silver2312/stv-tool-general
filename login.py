from bs4 import BeautifulSoup
from default import *

def login(s, username=default_username, password=default_pwd, host=default_host, headers = default_headers):
    data_login = {
        "ajax": "login",
        "username": username,
        "psw": password
    }
    try:
        r = s.post(url=host + '/index.php', headers=headers, data=data_login)
        if str(r.text).find("success") <= 0:
            print(r.text)
            exit()
        print(r.text)
        name = s.get(url=host + '/', headers=headers)
        soup = BeautifulSoup(name.content, 'html.parser')
        print('Xin chào: ' + soup.select_one('#menunavigator2 > ul > span').get_text())
    except:
        print("Lỗi đăng nhập        ")
        exit()
