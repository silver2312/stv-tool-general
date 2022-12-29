import random, datetime
from default import *

def read(s, host=default_host, user_agent = default_user_agent):
    try:
        data_read = {
            "sajax": "read"
        }
        q = ['29', '43', '64', '89', '97', '106', '110', '112', '125']
        t = random.choice(q)
        url_bk = host + "/truyen/yushubo/1/123460/" + t + "/"
        headers_read = {
            "Connection": "keep-alive",
            "User-Agent": user_agent,
            "referer": url_bk,
            "origin": host,
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5",
            "Content-type": "application/x-www-form-urlencoded"
        }
        res = s.post(url=host + '/index.php?ngmar=readcounter', headers=headers_read, data=data_read)
        print("Đang đọc truyện        ")
    except:
        print("Lỗi đọc    ")

def online(s, uid=default_uid, host=default_host, headers = default_headers):
    try:
        data_online = {
            "sajax": "online"
        }
        online = s.post(url=host + '/index.php?ngmar=ol2&u=' + uid, headers=headers, data=data_online)
        print("Đang online        ")
    except:
        print("Lỗi kiểm tra online        ")

def claim(s, host=default_host, headers = default_headers):
    time_now = datetime.datetime.now().strftime("%H:%M:%S")
    try:
        data_collect = {
            "ngmar": "collect",
            "ajax": "collect"
        }
        collect = s.post(url=host + '/index.php', headers=headers, data=data_collect)
        collect.encoding = 'utf-8-sig'
        item = collect.json()
        print(time_now + " => " + item['name'])
        item_type = int(item['type'])
        if item_type == 3 or item_type == 4:
            if str(item['name']).find(r'Công Pháp') >= 0:
                items_name = ['Đại Thiên Toạ Chiếu Đồ Lục','Pháp Chiếu Thần Nhai','Hắc Diệt Thiên Sát Lục','Tà Năng Cấm Pháp Di Thư','Cấm Thuật Thiên Cửu Chương','Ngục Hoạ Pháp Thiên Đồ Lục','Đế Chính Thiên Cảnh Thập Lục Chương']
            elif str(item['name']).find(r'Tàn quyển') >= 0:
                items_name = ['Vĩnh Hằng Chân Lý','Tàn quyển']
            elif str(item['name']).find(r'Công kích vũ kỹ') >= 0:
                items_name = ['Công kích vũ kỹ','Đoạt Mệnh Nhất Thương','Thất Thương Quyền','Bát Cực Quyền']
            elif str(item['name']).find(r'Công kích bí kỹ') >= 0:
                items_name = ['Tử Tích Thiên Trầm Sinh Diệt Lực','Sơ Nguyên Cự Ám Thần Lực','Chư Tà Tổ Nguyên Thần Lực','Thập Cấm Thiên Tức Thần Ma Lực','Đế Cảnh Ngự Thần Lực','Nguyên Sơ Cực Cấm Tổ Lực']
            elif str(item['name']).find(r'Thân pháp') >= 0:
                items_name = ['Thân pháp','Cân Đẩu Vân','Thiên Ma Bát Bộ','Geppo','Soru']
            elif str(item['name']).find(r'Tinh thần bí pháp') >= 0:
                items_name = ['Tinh thần bí pháp','Vĩnh Hoả Anh Hùng','Cương Quyết Chi Tâm','Tử Huyết Thánh Ca']
            elif str(item['name']).find(r'Luyện thể thần công') >= 0:
                items_name = ['Luyện thể thần công','Thần Tượng Kinh']
            elif str(item['name']).find(r'Luyện thể công pháp') >= 0:
                items_name = ['Luyện thể công pháp']
            elif str(item['name']).find(r'Phòng ngự vũ kỹ') >= 0:
                items_name = ['Phòng ngự vũ kỹ','Tekkai','Kim Chung Tráo','Thiết Bố Sam']
            else:
                items_name = [item['name']]
            item_info = item['info']
            item_name = random.choice(items_name)
            data_fcollect = {
                "ajax": "fcollect",
                "c": 2,
                "newname": item_name,
                "newinfo": item_info
            }
            try:
                fcollect = s.post(url=host + "/index.php?ngmar=fcl", headers=headers, data=data_fcollect)
            except:
                print("Lỗi mạng    ", end="\r")
        else:
            data_fcollect = {
                "ajax": "fcollect",
                "c": 2
            }
            try:
                fcollect = s.post(url=host + "/index.php?ngmar=fcl", headers=headers, data=data_fcollect)
            except:
                print("Lỗi mạng    ", end="\r")
        if fcollect.status_code == 200:
            print('Thành công ')
        else:
            print('Lỗi nhặt !!      ')
    except Exception as ex:
        print('Chưa có đồ    ')
