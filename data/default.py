import os, json, datetime, random

def default_base():
    f = open('account.json', )
    data = json.load(f)
    try:
        host = data[0]['host']
    except:
        host = 'http://14.225.254.182'
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
    # Get Random User Agent String.
    try:
        u = open("user_agent.txt", "r")
        list_u = u.readlines()
        user_agent = random.choice(list_u).replace('\n','')
    except:
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'
    default_username = 'thienhoa2923'
    default_pwd = 'thienhoa2923'
    default_uid = '95000'

    headers = {
        "Connection": "keep-alive",
        "User-Agent": user_agent,
        "origin": host,
    }
    context = {
        'data': data,
        'host': host,
        'user_agent': user_agent,
        'default_username': default_username,
        'default_pwd': default_pwd,
        'default_uid': default_uid,
        'headers': headers,
        'choose': choose,
    }
    return context
def time_now():
    return datetime.datetime.now().strftime("%H:%M:%S")

def intro():
    print("\n\t ~  ~  ~┌∩┐(◣_◢)┌∩┐~  ~  ~    ")
    print("\t    TOOL STV AUTO ALL  ")
    print("\t--------------------------\n")
    print("===========================================")
    print("Creator : Ngự tỷ khống - Elly - Đế Thiên")
    print("===========================================\n")

def choose_action():
    print('Choose one action ?')
    i = 0
    choose = default_base()['choose']
    while i < len(choose):
        print(i,':', choose[i])
        i+=1
    try:
        x = int(input("\nInput number: "))
        if not x:
            x = 0
    except:
        x = 0
    return x
def clear():
    # for windows
    if os.name == 'nt':
        _ = os.system('cls')
        # for mac and linux(here, os.name is 'posix')
    else:
        _ = os.system('clear')
def choose_account(x=0):
    data = default_base()['data']
    if len(data) > 0:
        clear()
        choose = default_base()['choose']
        print(choose[x])
        print('\nChoose account to use: ')
        k_data = 0
        while k_data < len(data):
            print(k_data, ':',data[k_data]['username'],'-',data[k_data]['pwd'],'-',data[k_data]['id'])
            k_data +=1
        try:
            y = int(input("Input number: "))
            if y < 0:
                y = 0
        except:
            y = 0
        if y < 0 or y > len(data):
            print('Input error please run agian.')
            exit()
    else:
        print('Please input new account in file account.json')
    username = data[y]['username']
    password = data[y]['pwd']
    acc_id = data[y]['id']
    context = {
        'y': y,
        'username': username,
        'password': password,
        'id': acc_id
    }
    return context

def base_action():
    clear()
    intro()
    data = default_base()['data']
    context = {}
    #chọn muốn làm gì
    x = choose_action()
    #chọn tài khoản
    choose_accounts = choose_account(x)
    y = choose_accounts['y']
    username = choose_accounts['username']
    password = choose_accounts['password']
    acc_id = choose_accounts['id']
    context['x'] = x
    context['y'] = y
    context['username'] = username
    context['password'] = password
    context['acc_id'] = acc_id
    #kiểm tra hành động
    if x == 4 or x == 7:
        try:
            tl16 = data[0]['tl16']
        except:
            tl16 = '95000'
        try:
            tl32 = data[0]['tl32']
        except:
            tl32 = '95000'
        try:
            tl64 = data[0]['tl64']
        except:
            tl64 = '95000'
        try:
            orther = data[0]['orther']
        except:
            orther = '95000'
        print(orther)
        context['tl16'] = tl16
        context['tl32'] = tl32
        context['tl64'] = tl64
        context['orther'] = orther
    if x == 5 or x == 7:
        check_lt = input('Dọn linh thạch(y/n - default: y): ')
        check_lb = input('Dọn lệnh bài(y/n - default: y): ')
        check_ttd = input('Dọn tẩy tuỷ đan(y/n - default: y): ')
        check_bk = input('Dọn bí kíp(y/n - default: y): ')
        if not check_lt:
            check_lt = 'y'
        if not check_lb:
            check_lb = 'y'
        if not check_ttd:
            check_ttd = 'y'
        if not check_bk:
            check_bk = 'y'
        context['check_lt'] = check_lt
        context['check_lb'] = check_lb
        context['check_ttd'] = check_ttd
        context['check_bk'] = check_bk
    return context

def check_time(x,y):
    data = default_base()['data']
    if x == 0 or x == 1 or x == 2:
        default_time1 = data[y]['time1']
        default_time2 = data[y]['time2']
    else:
        default_time1 = 240
        default_time2 = 320
    if x != 8:
        check_time = input('Do you want use default time ? ('+str(default_time1)+'~'+str(default_time2)+')(y/n - default:y)')
        if check_time == 'n':
            print('\nInput new time: ')
            time1 = int(input('Min time(min=1): '))
            time2 = int(input('Max time: '))
            if time1 is None or time2 is None:
                print('\nPlease input all time!')
                exit()
            if time1 < 1 or time2 < time1:
                print('\n Please input correct time!')
                exit()
        else:
            time1 = default_time1
            time2 = default_time2
    else:
        time1 = 5
        time2 = 10
    context = {
        'time1' : time1,
        'time2' : time2,
    }
    return context

