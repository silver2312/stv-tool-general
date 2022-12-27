import os, requests, json, time, random
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
from login import login
from bi_kip import use_bk
from read_claim import read, online, claim
from up_rut_tbc import up_tbc, rut_tbc, clean_profile
f = open('account.json', )
data = json.load(f)
host = data[0]['host']

software_names = [SoftwareName.CHROME.value]
operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]
user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=100)
# Get Random User Agent String.
user_agent = user_agent_rotator.get_random_user_agent()

headers = {
    "Connection": "keep-alive",
    "User-Agent": user_agent,
    "origin": host,
}

choose = [
    'Treo tu luyện',
    'Treo nhặt đồ',
    'Treo tu luyện + nhặt đồ',
    'Chuyển đồ lên tàng bảo các (trừ tẩy tuỷ đan + linh thạch)',
    'Rút đồ ở tàng bảo các',
    'Dọn túi (lệnh ,tẩy tuỷ đan,linh thạch, bí kíp)',
    'Tự động dùng bí kíp (Lưu ý: Bí kíp là tự nhặt mới có thể dùng được)',
]
def clear():
    # for windows
    if os.name == 'nt':
        _ = os.system('cls')
        # for mac and linux(here, os.name is 'posix')
    else:
        _ = os.system('clear')

def intro():
    print("\n\t ~  ~  ~┌∩┐(◣_◢)┌∩┐~  ~  ~    ")
    print("\t    TOOL STV AUTO ALL  ")
    print("\t--------------------------\n")
    print("===========================================")
    print("Creator : Ngự tỷ khống - Elly - Đế Thiên")
    print("===========================================\n")

def new_account(uname, pwd, uid):
    data.append( { 'username':uname, 'pwd':pwd, 'id':uid,'time1':65,'time2':75 } )
    with open('account.json', 'w', encoding='utf8') as s:
        json.dump(data,s, indent=4, sort_keys=True, ensure_ascii=False)

def choose_action():
    print('Bạn muốn làm gì ?')
    i = 0
    while i < len(choose):
        print(i,':', choose[i])
        i+=1
    try:
        x = int(input("\nNhập số: "))
        if not x:
            x = 0
    except:
        x = 0
    return x

clear()
intro()
#chọn muốn làm gì
x = choose_action()
#chọn tài khoản
if len(data) > 0:
    clear()
    print(choose[x])
    print('\nChọn tài khoản muốn dùng')
    k_data = 0
    while k_data < len(data):
        print(k_data, ':',data[k_data]['username'],'-',data[k_data]['pwd'],'-',data[k_data]['id'])
        k_data +=1
    print((len(data)),': Thêm tài khoản mới')
    y = input("Nhập số: ")
    try:
        y = int(y)
    except:
        y = 0
    if y < 0 or y > len(data):
        print('Nhập sai vui lòng chạy lại.')
        exit()
    if y == len(data):
        clear()
        print('Nhập thông tin tài khoản mới ')
        username = input("Tài khoản: ")
        password = input("Mật khẩu: ")
        acc_id = input("ID: ")
        new_account(username,password,acc_id)
    else:
        check_edit = input('Bạn có muốn sửa thông tin tài khoản không(y/n - default: n)?  ')
        username = data[y]['username']
        password = data[y]['pwd']
        acc_id = data[y]['id']
        if check_edit == 'y':
            print('Sửa thông tin tài khoản:')
            new_username = input('Nhập tài khoản mới: ')
            new_pwd = input('Nhập mật khẩu mới: ')
            new_id = input('Nhập id mới: ')
            data[y]['username'] = new_username
            data[y]['pwd'] = new_pwd
            data[y]['id'] = new_id
            if not new_username or not new_pwd or not new_id:
                print('vui lòng nhập đầy đủ thông tin')
                exit()
            with open('account.json', 'w', encoding='utf8') as s:
                        json.dump(data,s, indent=4, sort_keys=True, ensure_ascii=False)
            username = new_username
            password = new_pwd
            acc_id = new_id
else:
    clear()
    print(choose[x])
    print('Thêm tài khoản mới: ')
    username = input("Tài khoản: ")
    password = input("Mật khẩu: ")
    acc_id = input("ID: ")
    if not username or not password or not acc_id:
        print('Vui lòng nhập đầy đủ thông tin')
        exit()
    new_account(username,password,acc_id)
#kiểm tra hành động
if x == 4:
    print('Mặc định id: 95000')
    tl16 = input('Nhập id người nhận tụ linh 16: ')
    tl32 = input('Nhập id người nhận tụ linh 32: ')
    tl64 = input('Nhập id người nhận tụ linh 64: ')
    orther = input('Nhập id người nhận đồ còn lại: ')
elif x == 3:
    so_luong = input('Nhập số lượng 1 lần up(default:200): ')
    if so_luong:
        try:
            so_luong = int(so_luong)
            if so_luong <= 0:
                so_luong = 200
        except:
            so_luong = 200
elif x == 5:
    check_lt = input('Dọn linh thạch(y/n - default: y): ')
    check_lb = input('Dọn lệnh bài(y/n - default: y): ')
    check_ttd = input('Dọn tẩy tuỷ đan(y/n - default: y): ')
    check_bk = input('Dọn bí kíp(y/n - default: y): ')

if x == 0 or x == 1 or x == 2:
    default_time1 = data[y]['time1']
    default_time2 = data[y]['time2']
else:
    default_time1 = 300
    default_time2 = 420
check_time = input('Bạn có muốn dùng thời gian mặc định không ? ('+str(default_time1)+'~'+str(default_time2)+')(y/n - default:y)')
if check_time == 'n':
    print('\nNhập khoảng thời gian chạy: ')
    time1 = int(input('Giá trị nhỏ nhất(min=1): '))
    time2 = int(input('Giá trị lớn nhất: '))
    if time1 is None or time2 is None:
        print('\nVui lòng nhập đầy đủ thời gian')
        exit()
    if time1 < 1 or time2 < time1:
        print('\n Vui lòng nhập đúng khoảng thời gian')
        exit()
else:
    time1 = default_time1
    time2 = default_time2
clear()
intro()
print(username,'-',choose[x])
with requests.session() as s:
    login(s, username, password, host, headers)
    while True:
        i = random.randint(time1, time2)
        while i > 0:
            text = "Đang chờ: " + str(i) + ' giây     '
            print(text, end="\r")
            time.sleep(1)
            i -= 1
        else:
            try:
                if x == 0:
                    print('Tự động tu luyện       ')
                    read(s, host = host, user_agent = user_agent)
                    online(s, acc_id, host = host, headers = headers)
                elif x == 1:
                    print('Tự động nhặt đồ        ')
                    claim(s, host = host, headers = headers)
                elif x == 2:
                    print('Tự động tu luyện + nhặt     ')
                    read(s, host = host, user_agent = user_agent)
                    online(s, acc_id, host = host, headers = headers)
                    claim(s, host = host, headers = headers)
                elif x == 3:
                    print('Tự động up đồ bang         ')
                    up_tbc(s, so_luong, host = host, headers = headers)
                elif x == 4:
                    print('Tự động rút đồ bang       ')
                    rut_tbc(s, tl16, tl32, tl64, orther, host = host, headers = headers)
                elif x == 5:
                    print('Tự động dọn túi          ')
                    clean_profile(s,check_lt, check_lb, check_ttd, check_bk, host = host, headers = headers)
                elif x == 6:
                    print('Tự động sử dụng bí kíp          ')
                    use_bk(s, host = host, headers = headers)
                else:
                    print('Vui lòng nhập đúng số     ')
            except:
                print('Có Lỗi xảy ra            ')
            print("===========================================")
            time.sleep(2)
