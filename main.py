import pandas as pd 


WHITE_E = ['gmail.com','yahoo.com', 'yahoo.com.ph', 'rocketmail.com', 'icloud.com', 'deped.gov.ph', 'outlook.com', 'lht-philippines.com']
CHANGE_E = {'gmail.con': 'gmail.com', 'gamil.com': 'gmail.com', '13gmail.com': 'gmail.com'}
BLACK_E = ['aa.com',]


def phone_c(phone):
    j=0
    phone=str(phone)
    while True:
        try:
            if (phone[j].isdigit()!=True):
                phone=phone[:j] + phone[j+1:]
                j=j-1
        except IndexError:
            break
        j+=1
    while len(phone)>10:
        phone=phone[2:]
    return phone

def load_d(FILE_LOCATION):
    return pd.read_csv(FILE_LOCATION, header=0, sep=',', index_col=False)

def mail_check(data):
    gray = pd.DataFrame(columns=['host'])
    for i in range(len(data)):
        checker = data['email'][i].split('@')
        flag = False
        check = False
        for j in WHITE_E:
            if checker[1] == j:
                flag = True
            if flag:
                break
        if flag == False:
            try:
                checker[1] = CHANGE_E[checker[1]]
                check = True
            except KeyError:
                gray = gray.append({'host': checker[1]}, ignore_index=True)
        if check:
            data['email'][i] = checker[0] + '@' + checker[1]
        if flag & check:
            for j in BLACK_E:
                if checker[1] == j:
                    pass
        if flag or check: #maybe use else
            data['checker_e'][i] = 'True'              
    print(gray)
    return data

def phone_cc(data):
    pref = load_d("prefix_ph.csv")
    #gray = pd.DataFrame(columns=['tel'])
    for i in range(len(data)):
        flag = False
        phone = phone_c(data['phone_number'][i])
        for j in pref['Prefix']: 
            if str(phone[:3]) == str(j):
                flag = True
            if flag:
                data['phone_number'][i] = '+63' + phone
                if len(data['phone_number'][i]) == 13:
                    data['checker_t'][i] = 'True'
                break
    print(data)
    return data   

def main(): 
    #print(load_d('data.csv'))
    mail_check(load_d("data.csv"))
    phone_cc(load_d("data.csv"))

    

if __name__ == '__main__':
    import timeit
    load = 'main'
    print(timeit.timeit(load+'()', setup="from __main__ import " + load,number=1))