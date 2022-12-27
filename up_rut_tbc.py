from default import *
from bs4 import BeautifulSoup
import datetime

def up_tbc(s, so_luong=200, host =default_host, headers=default_headers):
    x = datetime.datetime.now().strftime("%H:%M:%S")
    try:
        tbc = s.get(url=host + '/the-luc/tang-bao-cac/', headers=headers)
        soup = BeautifulSoup(tbc.content, 'html.parser')
        list_a = soup.select('#tuitruvat > a')
        if len(list_a) > 0:
            if tbc.status_code == 200:
                print('Đã lấy danh sách đồ thành công    ')
            print(x + ': bạn đang có ' + str(len(list_a)) + ' đồ    ')
            item_id = ''
            j = 1
            sl = []
            for li in list_a:
                if j <= so_luong and j <= len(list_a) and li.get_text().find(r'Linh Thạch') < 0 and li.get_text().find(
                        r'Tẩy Tủy Đan') < 0:
                    item = li['iid']
                    item_id += (item + ',')
                    sl.append(item)
                    j += 1
            if len(sl) > 0:
                data_upload = {
                    'ajax': 'faction',
                    'sub': 'putstorage',
                    'itemlist': item_id[:-1]
                }
                uptbc = s.post(url=host + '/index.php?ngmar=fact', headers=headers, data=data_upload)
                if str(uptbc.text).find('ss') > 0:
                    print('Đã up ' + str(len(sl)) + ' đồ    ')
                else:
                    print(uptbc.text)
                    uptbc_1 = s.post(url=host + '/index.php?ngmar=fact', headers=headers, data=data_upload)
                    if uptbc_1.status_code == 500:
                        print('Server quá tải                  ')
                    else:
                        print('Đã up ' + str(len(sl)) + ' đồ    ')
            else:
                print('Chưa có đồ để up    ')
        else:
            print(x + ': đã hết đồ trong túi')
    except:
        print('Lỗi up đồ bang             ')

def rut_tbc(s, tl16=default_uid, tl32=default_uid, tl64=default_uid , orther=default_uid, host=default_host, headers=default_headers):
    x = datetime.datetime.now().strftime("%H:%M:%S")
    tbc = s.get(url=host + '/the-luc/tang-bao-cac/', headers=headers)
    soup = BeautifulSoup(tbc.content, 'html.parser')
    list_kho = soup.select('#khohang > a')
    if len(list_kho) > 0:
        if tbc.status_code == 200:
            print('Đã lấy danh sách đồ thành công    ')
        print(x + ': bạn đang có ' + str(len(list_kho)) + ' đồ    ')
        list_orther = ''
        list_16 = ''
        list_32 = ''
        list_64 = ''
        j = 0
        k = 0
        sl_other = []
        sl_16 = []
        sl_32 = []
        sl_64 = []
        for a in list_kho:
            item = a['iid']
            # lấy danh sách tụ linh id
            if j < 200 and j < len(list_kho) and a.get_text().find('Tụ Linh') > 0:
                if str(a['l']) == '4':
                    sl_16.append(a)
                    list_16 += (item + ',')
                    j += 1
                elif str(a['l']) == '5':
                    sl_32.append(a)
                    list_32 += (item + ',')
                    j += 1
                else:
                    sl_64.append(a)
                    list_64 += (item + ',')
                    j += 1
            # lấy danh sách item khác tụ linh id
            if k < 200 and k < len(list_kho) and a.get_text().find('Tụ Linh') < 0:
                list_orther += (item + ',')
                sl_other.append(a)
                k += 1
        data_tl16 = {
            'ajax': 'faction',
            'sub': 'takeoutstorage',
            'target': tl16,
            'itemlist': list_16[:-1]
        }
        data_tl32 = {
            'ajax': 'faction',
            'sub': 'takeoutstorage',
            'target': tl32,
            'itemlist': list_32[:-1]
        }
        data_tl64 = {
            'ajax': 'faction',
            'sub': 'takeoutstorage',
            'target': tl64,
            'itemlist': list_64[:-1]
        }
        data_other = {
            'ajax': 'faction',
            'sub': 'takeoutstorage',
            'target': orther,
            'itemlist': list_orther[:-1]
        }
        # tụ linh 16
        if len(sl_16) > 0:
            rut_tbc16 = s.post(url=host + '/index.php?ngmar=fact', headers=headers, data=data_tl16)
            if str(rut_tbc16.text).find(r'Lỗi') >= 0:
                print(rut_tbc16.text + '    ')
            else:
                print(x,': Đã chuyển ',len(sl_16),' tụ linh 16 cho id: ',tl16)
        else:
            print('Chưa có tụ linh 16 để rút    ')
        # tụ linh 32
        if len(sl_32) > 0:
            rut_tbc32 = s.post(url=host + '/index.php?ngmar=fact', headers=headers, data=data_tl32)
            if str(rut_tbc32.text).find(r'Lỗi') >= 0:
                print(rut_tbc32.text + '    ')
            else:
                print(x,': Đã chuyển ',len(sl_32),' tụ linh 32 cho id: ',tl32)
        else:
            print('Chưa có tụ linh 32 để rút    ')
        # tụ linh 64
        if len(sl_64) > 0:
            rut_tbc64 = s.post(url=host + '/index.php?ngmar=fact', headers=headers, data=data_tl64)
            if str(rut_tbc64.text).find(r'Lỗi') >= 0:
                print(rut_tbc64.text + '    ')
            else:
                print(x,': Đã chuyển ',len(sl_64),' tụ linh 16 cho id: ',tl64)
        else:
            print('Chưa có tụ linh 64 để rút    ')
        # đồ khác
        if len(sl_other) > 0:
            rut_tbc_another = s.post(url=host + '/index.php?ngmar=fact', headers=headers, data=data_other)
            if str(rut_tbc_another.text).find(r'Lỗi') >= 0:
                print(rut_tbc_another.text + '    ')
            else:
                print(x,': Đã chuyển ',len(sl_other),' đồ cho id: ',orther)
        else:
            print('Chưa có đồ để rút    ')
    else:
        print('Đã hết đồ trong kho bang    ')

def clean_profile(s, check_lt='y', check_lb='y', check_ttd='y', check_bk='y', host = default_host, headers = default_headers):
    if check_lt == 'n' and check_lb == 'n' and check_ttd == 'n' and check_bk == 'n':
        print('Bạn không dọn gì cả')
        exit()
    profile = s.get(url=host + '/user/0/', headers=headers)
    if profile.status_code == 200:
        print('Đã lấy nội dung trang cá nhân thành công    ')
        soup = BeautifulSoup(profile.content, 'html.parser')
        list_tui = soup.select('#tuitruvat > a')
        list_activate = soup.select('#infobox > div:nth-child(19) > div > a')
        # dùng linh thạch
        if check_lt == 'y':
            try:
                sl_lt = []
                lt_id = ''
                for lt in list_tui:
                    if lt.get_text().find(r'Linh Thạch') > 0:
                        item = lt['i']
                        sl_lt.append(lt)
                        lt_id += (item + ',')
                lt_str = lt_id[:-1]
                if len(sl_lt) > 0:
                    data_lt = {
                        'ajax': 'dungnhieu',
                        'consume': lt_str
                    }
                    use_lt = s.post(url=host + '/index.php', headers=headers, data=data_lt)
                    if use_lt.status_code == 500:
                        print('Server quá tải    ')
                    else:
                        print('Đã dùng ' + str(len(sl_lt)) + ' linh thạch    ')
                else:
                    print('Chưa có linh thạch để dùng    ')
            except:
                print('Lỗi dùng linh thạch    ')
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
                        print('Server quá tải    ')
                    else:
                        print(use_lh.text + '    ')
                else:
                    print('Chưa có lệnh bài để dùng    ')
            except:
                print('Lỗi dùng lệnh bài    ')
        # Vứt tẩy tuỷ đan        
        if check_ttd == 'y':
            try:
                sl_ttd = []
                ttd_id = ''
                for ttd in list_tui:
                    if ttd.get_text().find(r'Tẩy Tủy') > 0:
                        item = ttd['i']
                        sl_ttd.append(item)
                        ttd_id += (item + ',')
                if len(sl_ttd) > 0:
                    data_ttd = {
                        'ajax': 'item',
                        'sub': 'removenofitem',
                        'consume': ttd_id
                    }
                    del_ttd = s.post(url=host + '/index.php', headers=headers, data=data_ttd)
                    if del_ttd.status_code == 500:
                        print('Server quá tải    ')
                    else:
                        print(del_ttd.text + '    ')
                else:
                    print('Chưa có tẩy tuỷ đan để vứt    ')
            except:
                print('Lỗi vứt tẩy tuỷ đan    ')
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
                        use_bk = s.post(url=host + '/index.php', headers=headers, data=data_bk)
                        if use_bk.status_code == 500:
                            print('Server quá tải    ')
                        else:
                            print('Đã dùng ' + str(len(sl_bk)) + ' bí kíp    ')
                    else:
                        print('Ít bí kíp quá chờ tý đi     ')
                else:
                    print('Đã max cấp bí kíp vui lòng học thêm     ')
            except:
                print('Có lỗi xảy ra......')
    else:
        print('Lỗi lấy trang cá nhân    ')

