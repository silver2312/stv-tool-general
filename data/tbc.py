from bs4 import BeautifulSoup
from .default import default_base, time_now
import time, random

def get_tbc(s):
    while True:
        try:
            host = default_base()['host']
            headers = default_base()['headers']
            print('Loading items...',end='\r')
            tbc = s.get(url=host + '/the-luc/tang-bao-cac/', headers=headers)
            soup = BeautifulSoup(tbc.content, 'html.parser')
            my_items = soup.select('#tuitruvat > a')
            tbc_items = soup.select('#khohang > a')
            context = {
                'my_items': my_items,
                'tbc_items': tbc_items,
            }
            print('Get tbc success    ')
            break
        except Exception as e:
            print('Error getting tbc...')
            time.sleep(3)
    return context

def up_tbc(s):
    host = default_base()['host']
    headers = default_base()['headers']
    print('Upload items to TBC                          ')
    print('Get items in bag',end="\r")
    all_items = get_tbc(s)['my_items']
    items = []
    #remove Lt and TTD
    for a in all_items:
        if a.get_text().find(r'Linh Thạch') < 0 and a.get_text().find(r'Tẩy Tủy Đan') < 0:
            items.append(a['iid'])
    if len(items) > 0:
        print(time_now() + ': ' + str(len(items)) + ' items left over.')
        while True:
            item_id = ''
            sl_item = []
            for li in items:
                if len(items) > 100:
                    if len(sl_item) < 100:
                        item_id += (li + ',')
                        sl_item.append(li)
                    else:
                        data_upload = {
                            'ajax': 'faction',
                            'sub': 'putstorage',
                            'itemlist': item_id[:-1]
                        }
                        print('Upload ...',end="\r")
                        try:
                            uptbc = s.post(url=host + '/index.php?ngmar=fact', headers=headers, data=data_upload)
                            if str(uptbc.text).find('ss') >= 0:
                                print(time_now(),': upload 100 item to tbc')
                        except:
                            print(time_now(),'-Network error.')
                            break
                        for c in sl_item:
                            items.remove(c)
                        print(len(items),'items left over.')
                        time.sleep(1)
                        item_id = ''
                        sl_item.clear()
                        break
                else:
                    item_id += (li + ',')
                    sl_item.append(li)
            if len(items) <= 100:
                data_upload1 = {
                    'ajax': 'faction',
                    'sub': 'putstorage',
                    'itemlist': item_id[:-1]
                } 
                try:
                    uptbc1 = s.post(url=host + '/index.php?ngmar=fact', headers=headers, data=data_upload1)
                    if str(uptbc1.text).find('ss') >= 0:
                        print(time_now(),': upload', len(sl_item),'items.')
                except:
                    print(time_now(),'-Network error!')
                break
    else:
        print(time_now() + ': No item upload.')

def send_items(s, arr, uid):
    host = default_base()['host']
    headers = default_base()['headers']
    while True:
        item_id = ''
        sl_item = []
        for i in arr:
            if len(arr) > 100:
                if len(sl_item) < 100:
                    item_id += (i + ',')
                    sl_item.append(i)
                else:
                    data = {
                        'ajax': 'faction',
                        'sub': 'takeoutstorage',
                        'target': uid,
                        'itemlist': item_id[:-1]
                    }
                    print('Upload ...',end="\r")
                    try:
                        uptbc = s.post(url=host + '/index.php?ngmar=fact', headers=headers, data=data)
                        if str(uptbc.text).find(r'Lỗi') >= 0:
                            print(time_now(),uptbc.text)
                            break
                        else:
                            print(time_now(),': Move 100 items to id: '+uid)
                    except:
                        print(time_now(),'-Network error.')
                        break
                    for c in sl_item:
                        arr.remove(c)
                    print(len(arr),'items left over.')
                    time.sleep(3)
                    item_id = ''
                    sl_item.clear()
                    break
            else:
                item_id += (i + ',')
                sl_item.append(i)
        if len(arr) <= 100:
            data1 = {
                'ajax': 'faction',
                'sub': 'takeoutstorage',
                'target': uid,
                'itemlist': item_id[:-1]
            }
            try:
                uptbc1 = s.post(url=host + '/index.php?ngmar=fact', headers=headers, data=data1)
                if str(uptbc1.text).find(r'Lỗi') >= 0:
                    print(time_now(),uptbc1.text)
                    break
                else:
                    print(time_now(),': Move',len(sl_item),'items to id: '+uid)
            except:
                print(time_now(),'-Network error!')
            break

def move_tbc(s, tl16, tl32, tl64, orther):
    print('Move items TBC to user    ')
    print('Get items in TBC',end='\r')
    list_kho = get_tbc(s)['tbc_items']
    if len(list_kho) > 0:
        print(time_now() + ': TBC have ' + str(len(list_kho)) + ' items can move.    ')
        exp_16 = []
        exp_32 = []
        exp_64 = []
        orther_items = []
        for a in list_kho:
            item = a['iid']
            # lấy danh sách tụ linh id
            if a.get_text().find('Tụ Linh') > 0:
                if str(a['l']) == '4':
                    exp_16.append(item)
                elif str(a['l']) == '5':
                    exp_32.append(item)
                elif str(a['l']) == '6':
                    exp_64.append(item)
            # lấy danh sách item khác tụ linh id
            elif a.get_text().find('Tụ Linh') < 0:
                orther_items.append(item)
        if len(orther_items) > 0:
            print('Tbc have ',len(orther_items),' orther items.')
            send_items(s, orther_items, random.choice(orther))
        else:
            print(time_now(),': No orther items to move.')
        time.sleep(3)
        if len(exp_16) > 0:
            print('Tbc have ',len(exp_16),' exp 16.')
            send_items(s, exp_16, tl16)
        else:
            print(time_now(),': No exp 16 to move.')
        time.sleep(3)
        if len(exp_32) > 0:
            print('Tbc have ',len(exp_32),' exp 32.')
            send_items(s, exp_32, tl32)
        else:
            print(time_now(),': No exp 32 to move.')
        time.sleep(3)
        if len(exp_64) > 0:
            print('Tbc have ',len(exp_64),' exp 64.')
            send_items(s, exp_64, tl64)
        else:
            print(time_now(),': No exp 64 to move.')
    else:
        print('no items in TBC    ')
