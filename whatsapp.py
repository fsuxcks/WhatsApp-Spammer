currentversion = "0.83"
import os
import sys
import time
import random
import shutil
import logging
import traceback
from datetime import datetime,timezone,timedelta
os.system("cls")
os.system(f"title WhatsApp Tool v{currentversion}")
os.system("color 2")
print(f"[*] WhatsApp Tool by maxhack01 (t.me/emil_mmd) v{currentversion}")
print("[*] Инициализация...")
try:
    import pywhatkit as kit
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
except Exception as e:
    print("[!] Не удалось загрузить библиотеки. Необходимо установить зависимости.")
    input()
    sys.exit()
logging.basicConfig(
    filename='Logs.log',
    filemode='a',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

os.system("cls")

try:

    job = 0

    def load_file(filename):
        try:
            with open(f"{filename}", "r", encoding='utf-8') as file:
                return [line.strip() for line in file.readlines() if line.strip()]
        except Exception as e:
            print(e)
            print(f"[!] Не удалось найти файл {filename}, Убедитесь что она находится с одной папке с программой!")
            time.sleep(10)
            sys.exit()
        if not [line.strip() for line in file.readlines() if line.strip()]:
            print(f"[!] Файл {filename} пустой!")
            time.sleep(8)
            sys.exit() 


    def getInfo():
        print("[+] Рассылка сообщений [1]")
        print("[+] Рассылка сообщений с нескольких номеров WhatsApp в фоновом режиме [2]")
        try:
            jobIn = int(input(">>> "))
            if jobIn == 1:
                return 1
            if jobIn == 2:
                return 2
            if jobIn !=2 or jobIn != 3:
                print("[!] Неправильное значение.")
                time.sleep(2)
                os.system("cls")
                start(0)
        except: 
            print("[!] Неправильное значение.")
            time.sleep(2)
            os.system("cls")
            start(0)
            
    def send_messages(numbers_file,min,max,wait_time):
        os.system("cls")
        print(f"[*] WhatsApp Tool v{currentversion}")
        print(f"[+] Начинаем работу")

        numbers = load_file("numbers.txt")
        messages = load_file("text.txt")

        print(f"[+] Загружено номеров: {len(numbers)}")
        print(f"[+] Загружено сообщений: {len(messages)}")
        print("=============================")

        for i, number in enumerate(numbers, 1):
            message = random.choice(messages)
            print(f"[{i}/{len(numbers)}] Отправка на {number}: {message}")
            ping = random.randint(min,max)
            try:
                phone = str(number).strip()
                if not phone.startswith("+"):
                    raise ValueError(f"[!] Номер должен начинаться с '+': {phone}")
                    time.sleep(10)
                    sys.exit()
                msg = str(message)

                kit.sendwhatmsg_instantly(
                    phone_no=phone,
                    message=msg,
                    wait_time=wait_time,
                    tab_close=True
                )
                print(f"[+] Отправлено в {datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}")
                with open("sent_numbers_trial.txt", 'a', encoding='utf-8') as file:
                            file.write(f"{phone}\n")
                print(f"[+] Задержка в секундах: {ping} ")
                time.sleep(ping)
            except Exception as e:
                print(f"[!] Ошибка при отправке на {phone}: {e}")
                with open("failed_numbers_trial.txt", 'a', encoding='utf-8') as file:
                            file.write(f"{phone}\n")
                time.sleep(2)

        input("[*] Программа завершила свою работу! Нажмите Enter чтобы перезапустить.")
        start(job=0)

    def send_messages_numbers(cycle, amount, mindelay, maxdelay,bigdelay,chanceofdelay):
        os.system("cls")
        print(f"[*] WhatsApp Tool v{currentversion}")
        print(f"[+] Начинаем работу")
        print("=========================")
        numbers = load_file("numbers.txt")
        messages = load_file("text.txt")
        print(f"[+] Загружено номеров: {len(numbers)}")
        print(f"[+] Загружено сообщений: {len(messages)}")
        print(f"[+] Количество профилей: {amount}")


        drivers = []
        driversession = []
        profile_dir = os.path.join(os.getenv("APPDATA"), "WATool")
        if not os.path.exists(profile_dir):
            os.makedirs(profile_dir)

        def startSeleniumProfiles(i):
            profile_dirs = os.path.join(profile_dir, "profiles", f"wa_user{i}")
            options = Options()
            #options.add_argument("--headless")
            options.add_argument("--window-size=350,700")
            options.add_argument("--log-level=3")
            options.add_experimental_option("excludeSwitches", ["enable-logging"])
            options.add_argument(f"--user-data-dir={profile_dirs}")
            service = Service(log_path=os.devnull)
            driver = webdriver.Chrome(options=options, service=service)
            driver.get("https://web.whatsapp.com")
            return driver

        def startSelenium(i):
            profile_dirs = os.path.join(profile_dir, "profiles", f"wa_user{i}")
            options = Options()
            options.add_argument("--headless")
            options.add_argument("--disable-gpu")
            options.add_argument("--window-size=1000,700")
            options.add_argument("--log-level=1")
            options.add_experimental_option("excludeSwitches", ["enable-logging"])
            options.add_argument(f"--user-data-dir={profile_dirs}")
            service = Service(log_path=os.devnull)
            options.add_argument('--remote-debugging-pipe')
            driver = webdriver.Chrome(options=options, service=service)
            return driver
        
        def newprofiles():
            shutil.rmtree(profile_dir)
            os.makedirs(profile_dir)
            print("[+] Запускаем профили...")
            for i in range(amount):
                driver = startSeleniumProfiles(i)
                drivers.append(driver)
                time.sleep(3)
            input("[+] Войдите в свои аккаунты WhatsApp и нажмите Enter...")
            for driver in drivers:
                driver.quit()

        def checkforprofile():
            if os.path.exists(f"{profile_dir}/profiles"):
                count = 0
                for item in os.listdir(f"{profile_dir}/profiles"):
                    if os.path.isdir(os.path.join(f"{profile_dir}/profiles", item)):
                        count += 1
                if amount > count or amount < count:
                    try:
                        p = input("[+] Количество указанных профилей больше/меньше чем количество существующих профилей. Создать новые? [y/n]: ")
                    except:
                        print("[!] Неверное значение")
                        time.sleep(5)
                        checkforprofile()
                    if p == "n":
                        print("[!] Закрываем программу...")
                        time.sleep(2)
                        sys.exit()
                    if p == "y":
                        newprofiles()
                if amount == count:
                    try:
                        g = input("[?] Хотите оставить текущие профили?[y/n]: ")
                    except:
                        print("[!] Неверное значение")
                        time.sleep(5)
                        checkforprofile()
                    if g == "n":
                        shutil.rmtree(f"{profile_dir}/profiles")
                        newprofiles()
            else:
                newprofiles()


        def checkforbigdelay():
            chance = random.randint(1,100)
            if chance > chanceofdelay or chance == chanceofdelay:
                return False
            else:
                return True

        checkforprofile()
        print("[+] Запускаем сессии...")
        for i in range(amount):
            drivernew = startSelenium(i)
            driversession.append(drivernew)
            time.sleep(2)
        time.sleep(2)
        cycle = cycle+1
        for m in range(cycle):
            print(f"[+] Цикл #{m+1}")
            for i, number in enumerate(numbers):
                msg = random.choice(messages)
                if len(driversession) == 1:
                    profilenum = 1
                else:
                    profilenum = i+1
                    if profilenum > len(driversession):
                        profilenum = profilenum - len(driversession)
                print(f"[{i+1}/{len(numbers)}] Отправка на {number}: {msg} через Профиль #{profilenum}")
                driverfor = driversession[i % len(driversession)]
                driverfor.execute_script(f"window.open('https://web.whatsapp.com/send?phone={number}&text={msg}', '_blank');")
                driverfor.switch_to.window(driverfor.window_handles[1])
                time.sleep(2)
                try:
                    WebDriverWait(driverfor, 12).until(EC.presence_of_element_located((By.ID, "pane-side")))
                    time.sleep(2.5)
                except:
                    driverfor.quit()
                    driversession.remove(driverfor)
                    if not driversession:
                        print("Профили WhatsApp", "Программа завершила свою работу так как все текущие профили потеряли доступ либо получили бан")
                        input()
                        sys.exit()
                    print(f"Не удалось войти в профиль #{profilenum}, возможно аккаунт заблокирован или потерял доступ")
                    time.sleep(3)
                    continue
                try:
                    send_button = driverfor.find_element(By.XPATH, '/html/body/div[1]/div/div/div[3]/div/div[4]/div/footer/div[1]/div/span/div/div[2]/div/div[4]/button/span')
                    send_button.click()
                    print(f"[+] Отправлено в {datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}")
                    with open("sent_numbers.txt", 'a', encoding='utf-8') as file:
                            file.write(f"{number}\n")
                    if chanceofdelay > 0:
                        if checkforbigdelay():
                            print(f"[+] Случайная задержка: {bigdelay} минут(-а)")
                            for i in range(bigdelay):
                                time.sleep(60)
                                q = driverfor.title
                        else:
                            delay = random.randint(mindelay,maxdelay)
                            print(f"[+] Задержка в секундах: {delay} ")
                            for i in range(delay):
                                time.sleep(1)
                                q = driverfor.title
                    if chanceofdelay == 0:
                        delay = random.randint(mindelay,maxdelay)
                        print(f"[+] Задержка в секундах: {delay} ")
                        for i in range(delay):
                            time.sleep(1)
                            q = driverfor.title
                except:
                    try:
                        send_button = driverfor.find_element(By.XPATH, '/html/body/div[1]/div/div/div[3]/div/div[4]/div/footer/div[1]/div/span/div/div[2]/div[2]/button/span')
                        send_button.click()
                        print(f"[+] Отправлено в {datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}")
                        with open("sent_numbers.txt", 'a', encoding='utf-8') as file:
                            file.write(f"{number}\n")
                        if chanceofdelay > 0:
                            if checkforbigdelay():
                                print(f"[+] Случайная задержка: {bigdelay} минут(-а)")
                                for i in range(bigdelay):
                                    time.sleep(60)
                                    q = driverfor.title
                            else:
                                delay = random.randint(mindelay,maxdelay)
                                print(f"[+] Задержка в секундах: {delay} ")
                                for i in range(delay):
                                    time.sleep(1)
                                    q = driverfor.title
                        if chanceofdelay == 0:
                            delay = random.randint(mindelay,maxdelay)
                            print(f"[+] Задержка в секундах: {delay} ")
                            for i in range(delay):
                                time.sleep(1)
                                q = driverfor.title
                    except Exception as e:
                        print(f"[!] Не удалось отправить сообщение на номер {number}. Попробуйте перезаписать профиль.")
                        with open("failed_numbers.txt", 'a', encoding='utf-8') as file:
                            file.write(f"{number}\n")
                        time.sleep(2)
                
                driverfor.close()
                driverfor.switch_to.window(driverfor.window_handles[0])
        for drivers in driversession:
            drivers.quit()
        driversession.clear()
        input("[*] Программа завершила свою работу! Нажмите Enter чтобы перезапустить.")
        os.system("cls")
        start(job=0)

    def start(job):
        print(f"[*] WhatsApp Tool by maxhack01 (t.me/emil_mmd) v{currentversion}")
        print(f"[*] Добро пожаловать !")
        print("=================================")
        if job == 0:
            job = getInfo()
        if job == 1:
            try:
                mindelay = int(input("[?] Введите минимальную задержку в секундах: "))
                maxdelay = int(input("[?] Введите максимальную задержку в секундах: "))
                waittime = int(input("[?] Введите задержку для прогрузки WhatsApp Web (15s): "))
                if mindelay>maxdelay:
                    print("[!] Минимальное значение не может быть больше максимального!")
                    time.sleep(3)
                    os.system("cls")
                    start(1)
            except:
                print("[!] Введите только цифры.")
                time.sleep(3)
                os.system("cls")
                start(1)
            send_messages(numbers_file="numbers.txt", min=mindelay, max=maxdelay, wait_time=waittime)
        if job == 2:
            try:
                amount = int(input("[?] Введите количество аккаунтов: "))
                mindelay = int(input("[?] Введите минимальную задержку в секундах: "))
                maxdelay = int(input("[?] Введите максимальную задержку в секундах: "))
                cycle = int(input("[?] Использовать циклы для прогрева [0 - нет / кол-во циклов - да]: "))
                chanceofdelay = int(input("[?] Использовать случайные задержки [0 - нет / шанс задержик (%) - да]: "))
                if chanceofdelay != 0:
                    bigdelay = int(input("[?] Введите случайную задержку в минутах: "))
                else:
                    bigdelay = 0
            except:
                print("[!] Неверное значения!")
                time.sleep(3)
                os.system("cls")
                start(3)
            if mindelay > maxdelay:
                print("Минимальное значение не может быть больше максимального.")
                time.sleep(5)
                os.system("cls")
                start(3)
            send_messages_numbers(cycle, amount,mindelay,maxdelay,bigdelay,chanceofdelay)

    start(job=job)

except Exception as e:
    print(f"[!] Произошла ошибка: {e}")
    error_message = traceback.format_exc()
    logging.error("[!] Произошла ошибка! %s", error_message)
    input("[!] Ошибка записана в лог. Обратитесь в Telegram: t.me/emil_mmd")
