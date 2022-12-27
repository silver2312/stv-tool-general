from default import *
from bs4 import BeautifulSoup
import time

def use_bk(s, host = default_host, headers = default_headers):
    try:
        profile = s.get(url=host + '/user/0/', headers=headers)
        if profile.status_code == 200:
            print('Đã lấy nội dung trang cá nhân thành công    ')
            soup = BeautifulSoup(profile.content, 'html.parser')
            list_tui = soup.select('#tuitruvat > a')
            # dùng bí kíp
            aaa = 0
            for bki in list_tui:
                if bki['tag'] == r'4' and bki['b'] == r'10' and bki['ac'] == r'false':
                    aaa += 1
                    data_use_bk = {
                        'ajax': 'useitem',
                        'itemid': bki['i']
                    }
                    bk = s.post(url=host + '/index.php', headers=headers, data=data_use_bk)
                    if bk.status_code == 500:
                        print('Server quá tải.......')
                    time.sleep(1)
            print('Đã tu thêm ' + str(aaa) + ' bí kíp        ')
        else:
            print('Lỗi lấy nội dung trang cá nhân.......')
    except:
        print('Lỗi dùng bí kíp........')
