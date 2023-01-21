from bs4 import BeautifulSoup
import time
from .default import *

def get_tui(s):
    while True:
        try:
            host = default_base()['host']
            headers = default_base()['headers']
            profile = s.get(url=host + '/user/0/', headers=headers)
            time.sleep(1)
            soup = BeautifulSoup(profile.content, 'html.parser')
            list_tui = soup.select('#tuitruvat > a')
            list_activate = soup.select('#infobox > div:nth-child(19) > div > a')
            context = {
                'list_tui': list_tui,
                'list_activate': list_activate,
            }
            print('Get profile success    ')
            break
        except Exception as e:
            print('Error getting profile...')
            time.sleep(3)
    return context

def use_bk(s, list_tui):
    host = default_base()['host']
    headers = default_base()['headers']
    print('Use bí kíp                               ')
    try:
        # dùng bí kíp
        aaa = 0
        for bki in list_tui:
            if bki['tag'] == r'4' and bki['b'] == r'10' and bki['ac'] == r'false':
                aaa += 1
                data_use_bk = {
                    'ajax': 'useitem',
                    'itemid': bki['i']
                }
                print('Use bí kíp...',end='\r')
                bk = s.post(url=host + '/index.php', headers=headers, data=data_use_bk)
                if bk.status_code == 500:
                    print('Server 500.......')
                time.sleep(1)
        print('Use ' + str(aaa) + ' bí kíp        ')
    except:
        print('Error use bí kíp........')

def clean_profile(s, check_lt='y', check_lb='y', check_ttd='y', check_bk='y'):
    host = default_base()['host']
    headers = default_base()['headers']
    print('Clean profile!                                                 ')
    if check_lt == 'n' and check_lb == 'n' and check_ttd == 'n' and check_bk == 'n':
        print('You choose nothing!')
        exit()
    print('Getting profile...',end='\r')
    profile =get_tui(s)
    list_tui = profile['list_tui']
    list_activate = profile['list_activate']
    # dùng linh thạch
    if check_lt == 'y':
        try:
            sl_lt = 0
            lt_id = ''
            for lt in list_tui:
                if lt.get_text().find(r'Linh Thạch') > 0:
                    item = lt['i']
                    sl_lt+=1
                    lt_id += (item + ',')
            lt_str = lt_id[:-1]
            if sl_lt > 0:
                data_lt = {
                    'ajax': 'dungnhieu',
                    'consume': lt_str
                }
                use_lt = s.post(url=host + '/index.php', headers=headers, data=data_lt)
                if use_lt.status_code == 500:
                    print('Error 500    ')
                else:
                    print('Use ' + str(sl_lt) + ' linh thạch    ')
            else:
                print('No linh thạch to use    ')
        except:
            print('Error use linh thạch    ')
    # dùng lệnh bài
    if check_lb == 'y':
        try:
            sl_lenh = []
            for lh in list_tui:
                if lh['itn'] == 'uy-vong-lenh':
                    item = lh['i']
                    sl_lenh.append(item)
            if len(sl_lenh) > 0:
                data_lh = {
                    'ajax': 'item',
                    'sub': 'useitem',
                    'itemid': sl_lenh[0]
                }
                use_lh = s.post(url=host + '/index.php?ngmar=item', headers=headers, data=data_lh)
                if use_lt.status_code == 500:
                    print('Error 500    ')
                else:
                    print(use_lh.text + '    ')
            else:
                print('No lệnh bài to use    ')
        except:
            print('Error use lệnh bài    ')
    # Vứt tẩy tuỷ đan        
    if check_ttd == 'y':
        try:
            sl_ttd = 0
            ttd_id = ''
            for ttd in list_tui:
                if ttd.get_text().find(r'Tẩy Tủy') > 0:
                    item = ttd['i']
                    sl_ttd+=1
                    ttd_id += (item + ',')
            if sl_ttd > 0:
                data_ttd = {
                    'ajax': 'item',
                    'sub': 'removenofitem',
                    'consume': ttd_id
                }
                del_ttd = s.post(url=host + '/index.php', headers=headers, data=data_ttd)
                if del_ttd.status_code == 500:
                    print('Error 500    ')
                else:
                    print(del_ttd.text + '    ')
            else:
                print('No tẩy tuỷ đan to remove    ')
        except:
            print('Error remove tẩy tuỷ đan    ')
    # dọn bí kíp
    if check_bk == 'y':
        try:
            target_id = []
            for target in list_activate:
                if int(target['l']) < 50:
                    item = target['i']
                    target_id.append(item)
            if len(target_id) > 0:
                sl_bk = []
                bk_str = ''
                check = 0
                for bk in list_tui:
                    if bk['tag'] == '4' and bk['ac'] == 'false':
                        item = bk['i']
                        sl_bk.append(item)
                        bk_str += (item + ',')
                        check += 1
                if check > 200:
                    data_bk = {
                        'ajax': 'linhngo',
                        'itemid': target_id[0],
                        'consume': bk_str
                    }
                    use_bk1 = s.post(url=host + '/index.php', headers=headers, data=data_bk)
                    if use_bk1.status_code == 500:
                        print('Server 500    ')
                    else:
                        print('Use ' + str(len(sl_bk)) + ' bí kíp    ')
                else:
                    print('Too few bk please wait     ')
            else:
                use_bk(s, list_tui)
        except:
            print('Error use bk......')

def use_tld(s):
    host = default_base()['host']
    headers = default_base()['headers']
    print('Use tụ linh đan                       ')
    print('Getting profile...',end='\r')
    tbc = get_tui(s)
    list_a = tbc['list_tui']
    if len(list_a) > 0:
        print(time_now() + ': You have ' + str(len(list_a)) + ' items    ')
        j = 0
        sl = []
        for tld in list_a:
            if j < len(list_a) and tld.get_text().find(r'Tụ Linh Đan') >= 0 and tld['ac'] == 'false':
                item = tld['i']
                sl.append(item)
        print(time_now(),'You have',len(sl),'tụ linh đan')
        if len(sl) <= 0:
            print(time_now(),'- No tụ linh đan in bag')
            exit()
        while True:
            i = 0
            tld_id = ''
            sl_tld = []
            for a in sl:
                if len(sl) >= 200:
                    if len(sl_tld) < 200:
                        tld_id += (a + ',')
                        sl_tld.append(a)
                    else:
                        data = {
                            'ajax' : 'dungnhieu',
                            'consume' : tld_id[:-1]
                        }
                        print('Using tụ linh đan',end='\r')
                        try:
                            r = s.post(url=host + '/index.php', headers=headers,data=data)
                            if r.status_code == 200:
                                print(time_now(),': Use 200 tụ linh đan')
                        except:
                            print('Network error')
                        for c in sl_tld:
                            sl.remove(c)
                        print(len(sl),'items left over.')
                        i = 0
                        tld_id = ''
                        sl_tld.clear()
                        break
                else:
                    tld_id += (a + ',')
                    sl_tld.append(a)
                i+=1
            if len(sl) < 200:
                data = {
                    'ajax' : 'dungnhieu',
                    'consume' : tld_id[:-1]
                }
                print('Using tụ linh đan',end='\r')
                try:
                    r = s.post(url=host + '/index.php', headers=headers,data=data)
                    if r.status_code == 200:
                        print(time_now(),': Use',len(sl),'tụ linh đan')
                except:
                    print('Network error')
                break
    else:
        print(time_now() + ': No items in bag')
