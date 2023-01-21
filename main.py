import requests, time, random, os
from data.default import *
from data.base_actions import *
from data.tbc import *
from data.user import *


def clear():
    # for windows
    if os.name == 'nt':
        _ = os.system('cls')
        # for mac and linux(here, os.name is 'posix')
    else:
        _ = os.system('clear')

choose = [
    'Auto exp',
    'Auto claim',
    'Auto exp and claim',
    'Upload items to TBC (trừ tẩy tuỷ đan + linh thạch)',
    'Move items in TBC',
    'Clean profile (lệnh ,tẩy tuỷ đan,linh thạch, bí kíp)',
    'Auto use bí kíp (Lưu ý: Bí kíp là tự nhặt mới có thể dùng được)',
    'Up TBC + Move TBC + Clean Profile + Auto use bí kíp',
    'Auto use Tụ Linh',
]
actions = base_action()
check_t = check_time(actions['x'], actions['y'])
clear()
intro()
print(actions['username'],'-',choose[actions['x']])
with requests.session() as s:
    while True:
        try:
            login(s, actions['username'], actions['password'])
            break
        except:
            print('Try login again...')
    while True:
        time1 = check_t['time1']
        time2 =  check_t['time2']
        i = random.randint(time1, time2)
        while i > 0:
            text = "Waiting: " + str(i) + 's     '
            print(text, end="\r")
            time.sleep(1)
            i -= 1
        else:
            # try:
            if actions['x'] == 0:
                read(s)
                online(s, actions['acc_id'])
            elif actions['x'] == 1:
                claim(s)
            elif actions['x'] == 2:
                print('Auto exp and claim')
                read(s)
                online(s, actions['acc_id'])
                claim(s)
            elif actions['x'] == 3:
                up_tbc(s)
            elif actions['x'] == 4:
                move_tbc(s, actions['tl16'], actions['tl32'], actions['tl64'], actions['orther'])
            elif actions['x'] == 5:
                clean_profile(s,actions['check_lt'], actions['check_lb'], actions['check_ttd'], actions['check_bk'])
            elif actions['x'] == 6:
                use_bk(s)
            elif actions['x'] == 7:
                print('Up TBC + Move TBC + Clean Profile + Auto use bí kíp          ')
                up_tbc(s)
                move_tbc(s, actions['tl16'], actions['tl32'], actions['tl64'], actions['orther'])
                clean_profile(s,actions['check_lt'], actions['check_lb'], actions['check_ttd'], actions['check_bk'])
            elif actions['x'] == 8:
                use_tld(s)
                break
            else:
                print('Please select a valid option')
            # except:
            #     print('Có lỗi xảy ra                                      ')
            print("===========================================")
            time.sleep(2)

