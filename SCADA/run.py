from colorama import Fore, Back, Style
from os import system
import datetime
import time

def read_data(AGV):
    if AGV == 'AGV1':
        pass
    elif AGV == 'AGV2':
        pass
    elif AGV == 'AGV3':
        pass

if __name__ == '__main__':
    try:
        while True:
            system('clear')
            print(Fore.BLACK + Back.GREEN + '{:^100s}'.format('ICS REALTIME MONITORING SYSTEM -- version 1.0'))
            print(Style.RESET_ALL)
            print(datetime.datetime.now())
            print('+============+=============+=============+============+')
            print('|            |    AGV#1    |    AGV#2    |    AGV#3   |')
            print('+============+=============+=============+============+')
            print('| Status     |','{:^11s}'.format('ON'),'|','{:^11s}'.format('OFF'),'|','{:^10s}'.format('ON'),'|')
            print('| Location X |','{:^11s}'.format('ON'),'|','{:^11s}'.format('OFF'),'|','{:^10s}'.format('ON'),'|')
            print('| Location Y |','{:^11s}'.format('ON'),'|','{:^11s}'.format('OFF'),'|','{:^10s}'.format('ON'),'|')
            time.sleep(1)
    except KeyboardInterrupt:
            print(Style.RESET_ALL)
            print('Keyboard Interrupted')

