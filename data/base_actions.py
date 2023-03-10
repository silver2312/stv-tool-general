from bs4 import BeautifulSoup
import random
from .default import default_base, time_now

def login(s, username, password):
    host = default_base()['host']
    headers = default_base()['headers']
    data_login = {
        "ajax": "login",
        "username": username,
        "psw": password
    }
    s.post(url=host + '/index.php', headers=headers, data=data_login)
    name = s.get(url=host + '/', headers=headers)
    soup = BeautifulSoup(name.content, 'html.parser')
    print('Hello: ' + soup.select_one('#menunavigator2 > ul > span').get_text())

def online(s, uid):
    host = default_base()['host']
    headers = default_base()['headers']
    try:
        data_online = {
            "sajax": "online"
        }
        s.post(url=host + '/index.php?ngmar=ol2&u=' + uid, headers=headers, data=data_online)
        print("Online...        ")
    except:
        print("Online error!        ")

def read(s):
    host = default_base()['host']
    user_agent = default_base()['user_agent']
    try:
        data_read = {
            "sajax": "read"
        }
        q = ['30962080', '30962081', '30962082', '30962084', '30962085', '30962086', '30962087', '30962088']
        t = random.choice(q)
        url_bk = host + "/truyen/69shu/1/45559/" + t + "/"
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
        s.post(url=host + '/index.php?ngmar=readcounter', headers=headers_read, data=data_read)
        print("Reading...        ")
    except:
        print("Reading error!    ")

def claim(s):
    host = default_base()['host']
    headers = default_base()['headers']
    try:
        data_collect = {
            "ngmar": "collect",
            "ajax": "collect"
        }
        collect = s.post(url=host + '/index.php', headers=headers, data=data_collect)
        collect.encoding = 'utf-8-sig'
        item = collect.json()
        print(time_now() + " => " + item['name'])
        item_type = int(item['type'])
        if item_type == 3 or item_type == 4:
            if str(item['name']).find(r'C??ng Ph??p') >= 0:
                items_name = ['?????i Thi??n To??? Chi???u ????? L???c','Ph??p Chi???u Th???n Nhai','H???c Di???t Thi??n S??t L???c','T?? N??ng C???m Ph??p Di Th??','C???m Thu???t Thi??n C???u Ch????ng','Ng???c Ho??? Ph??p Thi??n ????? L???c','????? Ch??nh Thi??n C???nh Th???p L???c Ch????ng']
            elif str(item['name']).find(r'T??n quy???n') >= 0:
                items_name = ['V??nh H???ng Ch??n L??','T??n quy???n']
            elif str(item['name']).find(r'C??ng k??ch v?? k???') >= 0:
                items_name = ['C??ng k??ch v?? k???','??o???t M???nh Nh???t Th????ng','Th???t Th????ng Quy???n','B??t C???c Quy???n']
            elif str(item['name']).find(r'C??ng k??ch b?? k???') >= 0:
                items_name = ['T??? T??ch Thi??n Tr???m Sinh Di???t L???c','S?? Nguy??n C??? ??m Th???n L???c','Ch?? T?? T??? Nguy??n Th???n L???c','Th???p C???m Thi??n T???c Th???n Ma L???c','????? C???nh Ng??? Th???n L???c','Nguy??n S?? C???c C???m T??? L???c']
            elif str(item['name']).find(r'Th??n ph??p') >= 0:
                items_name = ['Th??n ph??p','C??n ?????u V??n','Thi??n Ma B??t B???','Geppo','Soru']
            elif str(item['name']).find(r'Tinh th???n b?? ph??p') >= 0:
                items_name = ['Tinh th???n b?? ph??p','V??nh Ho??? Anh H??ng','C????ng Quy???t Chi T??m','T??? Huy???t Th??nh Ca']
            elif str(item['name']).find(r'Luy???n th??? th???n c??ng') >= 0:
                items_name = ['Luy???n th??? th???n c??ng','Th???n T?????ng Kinh']
            elif str(item['name']).find(r'Luy???n th??? c??ng ph??p') >= 0:
                items_name = ['Luy???n th??? c??ng ph??p']
            elif str(item['name']).find(r'Ph??ng ng??? v?? k???') >= 0:
                items_name = ['Ph??ng ng??? v?? k???','Tekkai','Kim Chung Tr??o','Thi???t B??? Sam']
            else:
                items_name = [item['name']]
            item_info = str(item['info']).replace('<b>','').replace('</b>','')
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
                print("Network error!    ", end="\r")
        else:
            data_fcollect = {
                "ajax": "fcollect",
                "c": 2
            }
            try:
                fcollect = s.post(url=host + "/index.php?ngmar=fcl", headers=headers, data=data_fcollect)
            except:
                print("Network error    ", end="\r")
        if fcollect.status_code == 200:
            print('successs ')
        else:
            print('Claim error!!      ')
    except Exception as ex:
        print('No item found to claim.    ')
