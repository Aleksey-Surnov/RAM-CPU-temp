import psutil
import os
import time, csv
import platform, cpuinfo, re
import subprocess
import termcolor
from datetime import datetime, timedelta

def monitoring_go_eng():
     print('------------------------------------------')
     print('INFO_System:')
     print('OS:'+' '+str(platform.platform()))
     print('RAM total:' + ' ' + str((psutil.virtual_memory().total ) / (1024 * 1024 * 1024)) + ' ' + 'Gb')
     print('Brand CPU:'+' '+str(cpuinfo.get_cpu_info()['brand']))
     print('Count CPU:'+' '+str(psutil.cpu_count()))
     print('------------------------------------------')
     data_monitoring=[['Time','Temperature CPU (С)','Load CPU (%)', 'Used RAM (Gb)']]


     min=input('enter time measurement in minutes and press the button "Enter": ').replace(',', '.')
     start = datetime.now()
     file_date_time = str(time.strftime("%Y-%m-%d_%H-%M-%S"))
     sys_data=['Measurement date:'+' '+file_date_time,'OS:'+' '+str(platform.platform()), 'Brand CPU:'+' '+str(cpuinfo.get_cpu_info()['brand']), 'Count CPU:'+' '+str(psutil.cpu_count()), 'RAM total:'+' '+str((psutil.virtual_memory().total) / (1024*1024*1024))+' ' + 'Gb','Measurement data']


     def type_corr(min=0): # input validation function, returns a Boolean value
         if re.search(r'^[-+]?[0-9]*[.,]?[0-9]+(?:[eE][-+]?[0-9]+)?$', min) is not None: return True
         else: return False


     while type_corr(min)==False:
         min = input('enter time measurement in minutes and press the button "Enter": ').replace(',', '.')


     def get_os_info(): # get name OS
         os_info = str(platform.uname().system) # name OS
         return os_info # return name OS


     def get_temperature_info_windows(data_monitoring):  # a function of production data if ОS windows
         import wmi
         import colorama
         colorama.init()
         w = wmi.WMI(namespace="root\wmi")
         data_itermonitoring=[] # the list of data for save
         temperature_info = w.MSAcpi_ThermalZoneTemperature()[0] # getting the total CPU temperature
         temperature_info = round(((temperature_info.CurrentTemperature / 10) - 273), 4) # the translation to Celsius
         cpu_proc1 = str(psutil.cpu_percent())  # load CPU
         cpu_proc2 = int(cpu_proc1[:cpu_proc1.find('.')]) # load CPU for progress-bar
         termcolor.cprint('|'+'Temperature CPU= ' + str(temperature_info) + ' ' + 'C', 'red')  # the output of temperature into the terminal
         termcolor.cprint('|'+sym * round(temperature_info) + '|','red') #the output of progress-bar
         termcolor.cprint('|'+'Load CPU=' + str(cpu_proc1) + ' '+'%', 'green')  # the output of load CPU into the terminal
         termcolor.cprint('|'+sym * cpu_proc2 + '|', 'green') #the output of progress-bar
         termcolor.cprint('|'+'Used RAM=' + str((psutil.virtual_memory().used) / (1024*1024*1024)) + ' ' + 'Gb', 'yellow')  # the output of RAM uses into the terminal
         termcolor.cprint('|'+sym * round((psutil.virtual_memory().used) / (1024 * 1024 * 1024)) + '|', 'yellow') #the output of progress-bar
         data_itermonitoring.append((time.strftime("%H:%M:%S")))
         data_itermonitoring.append(str(temperature_info))
         data_itermonitoring.append(str(cpu_proc1))
         data_itermonitoring.append(str((psutil.virtual_memory().used) / (1024*1024*1024)))
         data_monitoring.append(data_itermonitoring)
         time.sleep(2)
         os.system('cls')  # clear terminal

     def get_temperature_info_linux(data_monitoring):  # a function of production data if ОS linux
         from termcolor import cprint
         data_itermonitoring = [] # the list of data for save
         temperature_info = []  # the list of temperature for each CPU core
         for i in range(0, len(psutil.sensors_temperatures()['coretemp'])):
             temperature_info.append(psutil.sensors_temperatures()['coretemp'][i][1])  # temperature of each CPU core
         temperature_info = float((sum(temperature_info)) / (len(psutil.sensors_temperatures()['coretemp']))) # arithmetic mean of temperature CPU
         cpu_proc1 = str(psutil.cpu_percent())  # load CPU
         cpu_proc2 = int(cpu_proc1[:cpu_proc1.find('.')]) # load CPU for progress-bar
         termcolor.cprint('|'+'Temperature CPU=' + str(temperature_info) + ' ' + 'C', 'red')  # the output of temperature into the terminal
         termcolor.cprint('|'+sym * round(temperature_info) + '|' ,'red') #the output of progress-bar
         termcolor.cprint('|'+'Load CPU=' + str(cpu_proc1) + ' '+'%', 'green')  # the output of load CPU into the terminal
         termcolor.cprint('|'+sym * cpu_proc2 + '|', 'green') #the output of progress-bar
         termcolor.cprint('|'+'Used RAM=' + str((psutil.virtual_memory().used) / (1024*1024*1024)) + ' ' + 'Gb', 'yellow')  # the output of RAM uses into the terminal
         termcolor.cprint('|'+sym * round((psutil.virtual_memory().used) / (1024 * 1024 * 1024)) + '|', 'yellow') #the output of progress-bar
         data_itermonitoring.append((time.strftime("%H:%M:%S")))
         data_itermonitoring.append(str(temperature_info))
         data_itermonitoring.append(str(cpu_proc1))
         data_itermonitoring.append(str((psutil.virtual_memory().used) / (1024 * 1024 * 1024)))
         data_monitoring.append(data_itermonitoring)
         time.sleep(2)
         os.system('clear')  # clear terminal


     while datetime.now() - start <= timedelta(seconds=float(min)*60): # make out the specified time in minutes
         if get_os_info() == 'Windows': get_temperature_info_windows(data_monitoring) # function call for Windows
         elif get_os_info() == 'Linux': get_temperature_info_linux(data_monitoring)   # function call for Linux
         else:
             print("Stop: Doesn't suit for ОS")
             break


     def save_monitoring(data_monitoring): # to save monitoring data
         with open(f'measurement_data_{file_date_time}.csv', 'w') as resultFile:
             wr = csv.writer(resultFile, delimiter =';')
             for item in sys_data:
                 wr.writerow([item])
             wr.writerows(data_monitoring)

     def quest_save():
         quest_s = input('Do you want to save monitoring data [yes/no]: ').lower()
         if quest_s.lower()=="yes":return True
         else: return False

     while True:
         if quest_save()==True:
             save_monitoring(data_monitoring)
             break
         else: break


def monitoring_go_rus():
    print('------------------------------------------')
    print('ИНФОРМАЦИЯ О СИСТЕМЕ:')
    print('OC:' + ' ' + str(platform.platform()))
    print('Доступная физическая оперативная память:' + ' ' + str((psutil.virtual_memory().total) / (1024 * 1024 * 1024)) + ' ' + 'Gb')
    print('Марка ЦП:' + ' ' + str(cpuinfo.get_cpu_info()['brand']))
    print('Количество ядер:' + ' ' + str(psutil.cpu_count()))
    print('------------------------------------------')
    data_monitoring = [['Время', 'Температура ЦП (С)', 'Загрузка ЦП (%)', 'Использование ОЗУ (Гб)']]
    min = input('введите время выволения мониторинга в минутах и нажмите "Enter": ').replace(',', '.')
    start = datetime.now()
    file_date_time = str(time.strftime("%Y-%m-%d_%H-%M-%S"))
    sys_data = ['Дата измеренеий:'+' '+str(time.strftime("%Y-%m-%d %H:%M:%S")), 'ОС:' + ' ' + str(platform.platform()),'Марка ЦП:' + ' ' + str(cpuinfo.get_cpu_info()['brand']), 'Количество ядер:' + ' ' + str(psutil.cpu_count()),'Доступная физическая оперативная память:' + ' ' + str((psutil.virtual_memory().total) / (1024 * 1024 * 1024)) + ' ' + 'Гб','Таблица  измерений:']

    def type_corr(min=0):  # фукнция проверки правильности ввода, возвращет логическое значение
        if re.search(r'^[-+]?[0-9]*[.,]?[0-9]+(?:[eE][-+]?[0-9]+)?$', min) is not None:
            return True
        else:
            return False

    while type_corr(min) == False:  # ввод времени мониторинга в минутах, возможно вводить десятичные дроби
        min = input('введите время выволения мониторинга в минутах и нажмите "Enter": ').replace(',', '.')

    def get_os_info():  # получить название ОС
        os_info = str(platform.uname().system)  # имя ОС
        return os_info  # вернуть название ОС

    def get_temperature_info_windows(data_monitoring):  # функция получения данных если ОС windows
        import wmi
        import colorama
        colorama.init()
        w = wmi.WMI(namespace="root\wmi")
        data_itermonitoring = [] #список для хранения данных измерений

        temperature_info = w.MSAcpi_ThermalZoneTemperature()[0]  # получение общей температуры процессора
        temperature_info = round(((temperature_info.CurrentTemperature / 10) - 273), 4)  # перевод в градусы C
        cpu_proc1 = str(psutil.cpu_percent())  # загрузка ЦП для вывода
        cpu_proc2 = int(cpu_proc1[:cpu_proc1.find('.')])  # загрузка ЦП для умножения строки и показания прогресс бара
        termcolor.cprint('|'+'температура ЦП=' + str(temperature_info) + ' ' + 'C','red')  # вывод температуры в терминал
        termcolor.cprint('|'+sym * round(temperature_info) + '|','red')
        termcolor.cprint('|'+'загрузка ЦП=' + str(cpu_proc1) + ' '+'%','green')  # вывод загрузки ЦП в терминал
        termcolor.cprint('|'+sym * cpu_proc2 + '|', 'green')
        termcolor.cprint('|'+'ОЗУ=' + str((psutil.virtual_memory().used) / (1024 * 1024 * 1024)) + ' ' + 'Gb', 'yellow')
        termcolor.cprint('|'+sym * round((psutil.virtual_memory().used) / (1024*1024*1024)) + '|', 'yellow')  # вывод используемой памяти в терминал
        data_itermonitoring.append((time.strftime("%H:%M:%S")))
        data_itermonitoring.append(str(temperature_info))
        data_itermonitoring.append(str(cpu_proc1))
        data_itermonitoring.append(str((psutil.virtual_memory().used) / (1024*1024*1024)))
        data_monitoring.append(data_itermonitoring)
        time.sleep(2)
        os.system('cls')  # очистка терминала

    def get_temperature_info_linux(data_monitoring):  # функция получения данных если ОС linux
        from termcolor import cprint
        data_itermonitoring = []
        temperature_info = []  # список в который заноcится температура по ядрам
        for i in range(0, len(psutil.sensors_temperatures()['coretemp'])):
            temperature_info.append(psutil.sensors_temperatures()['coretemp'][i][1])  # получение температуры по ядрам
        temperature_info = float((sum(temperature_info)) / (len(psutil.sensors_temperatures()['coretemp'])))  # подсчет среднего значения температуры
        cpu_proc1 = str(psutil.cpu_percent())  # загрузка ЦП для вывода
        cpu_proc2 = int(cpu_proc1[:cpu_proc1.find('.')])  # загрузка ЦП для умножения строки и показания прогресс бара
        termcolor.cprint('|'+'температура ЦП=' + str(temperature_info) + ' ' + 'C','red')  # вывод температуры в терминал
        termcolor.cprint('|'+sym * round(temperature_info) + '|','red')
        termcolor.cprint('|'+'загрузка ЦП=' + str(cpu_proc1) +' '+'%','green')  # вывод загрузки ЦП в терминал
        termcolor.cprint('|'+sym * cpu_proc2 + '|', 'green')
        termcolor.cprint('|'+'ОЗУ=' + str((psutil.virtual_memory().used) / (1024*1024*1024)) + ' ' + 'Gb', 'yellow')  # вывод используемой памяти в терминал
        termcolor.cprint('|'+sym * round((psutil.virtual_memory().used) / (1024 * 1024 * 1024))+'|', 'yellow')
        data_itermonitoring.append((time.strftime("%H:%M:%S")))
        data_itermonitoring.append(str(temperature_info))
        data_itermonitoring.append(str(cpu_proc1))
        data_itermonitoring.append(str((psutil.virtual_memory().used) / (1024 * 1024 * 1024)))
        data_monitoring.append(data_itermonitoring)
        time.sleep(2)
        os.system('clear')  # очистка терминала

    while datetime.now() - start <= timedelta(seconds=float(min) * 60):  # выполнять заданное время в минутах
        if get_os_info() == 'Windows': get_temperature_info_windows(data_monitoring)  # вывзов функции для Windows
        elif get_os_info() == 'Linux': get_temperature_info_linux(data_monitoring)  # вывзов функции для Linux
        else:
            print('Стоп: Программа не подходит для данной ОС')
            break

    def save_monitoring(data_monitoring):
        with open(f'данные_мониторинга_{file_date_time}.csv',  'w') as resultFile:
            wr = csv.writer(resultFile, delimiter=';')
            for item in sys_data:
                wr.writerow([item])
            wr.writerows(data_monitoring)

    def quest_save():
        quest_s = input('сохранить данные мониторинга [да/нет]: ').lower()
        if quest_s.lower() == "да":
            return True
        else: return False

    while True:
        if quest_save() == True:
            save_monitoring(data_monitoring)
            break
        else: break

def select_your_language(): # a function for enter your language/функция ввода языкка
    language=input('enter your language/введите язык [rus/eng]: ').lower()
    print('------------------------------------------')
    return language

lang=select_your_language()


def soft_info_rus():
    rus_info=['Разработчик: Алексей Сурнов', 'RAM-CPU-temp служит для контроля в реальном времени за параметрами:', '--температуры процессора'
              , '--задействованной оперативной памяти', '--загрузки процессора',
              'Вы можете сохранить результаты в отдельный файл после выполнения измерений.',
              'Файл с данными в формате csv будет находится в той же папке что и программа',
              'Использовать в операционных системаx: ', '--Windows v.7,8,10 ', '--Linux Debian, Linux Mint, Linux Ubuntu.']
    for info in rus_info:
        print(info)
    print('------------------------------------------')



def soft_info_eng():
    eng_info=['Developer: Alexey Surnov', 'RAM-CPU-temp serves for real-time monitoring of parameters:', '--СPU temperature'
              , '--involved RAM', '--CPU load',
              'You can save the results in a separate file after taking measurements.',
              'The data file in csv format will be located in the same folder as the program',
              'Use in operating systems: ', '--Windows v.7,8,10 ', '--Linux Debian, Linux Mint, Linux Ubuntu.']
    for info in eng_info:
        print(info)
    print('------------------------------------------')


if lang=='rus': soft_info_rus()
elif lang=='eng': soft_info_eng()
sym = '▌'  # символ прогресс бара/a symbol of the progress bar

while True:
    if lang=='rus':
        flag = input('Начать выполнение мониторинга [да/нет]: ')
        if flag == 'да': monitoring_go_rus()
        elif flag=='нет':
            input('Для выхода нажмите Enter')
            break
        else:
            print('неправильный ввод'+' '+'вы ввели:'+ ' '+'|'+flag+'|'+' '+ 'повторите попытку')
            print('введите [да/нет]')
    elif lang=='eng':
        flag = input('Do you want to start monitoring [yes/no]: ')
        if flag == 'yes': monitoring_go_eng()
        elif flag=='no':
            input('To exit the program press the button "Enter"')
            break
        else:
            print('invalid input'+' '+'you made:'+' '+'|'+flag+'|'+' '+ 'please try again')
            print('enter [yes/no]')
    else:
        print('invalid input, please try again / неправильный ввод языка, повторите попытку')
        lang = select_your_language()



