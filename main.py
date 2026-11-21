import time

import config
from services.desktop_tracker import get_active_window

def main():
    try:
        while True:
            info = get_active_window()
            if info is None:
                print("No active window")
            else:
                print(info)
            time.sleep(config.POLL_INTERVAL)
    except KeyboardInterrupt:
        print("stopped")

if __name__ == '__main__':
    main()