import time
from src.order_processing import Handler

if __name__ == '__main__':
    win = Handler()
    while True:
        try:
            win.site_monitor()
            time.sleep(10)
        except KeyboardInterrupt:
            print('Программа завершена.')
            break
