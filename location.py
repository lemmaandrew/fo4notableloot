import json
import os
import re
import time

#C:\Users\Peter\Documents\Python\Fallout 4
with open('.\\cells.json') as f:
    cells = json.load(f)


def followLog(logfile):
    """tails the file, blatently stolen from https://github.com/dabeaz/generators/blob/master/examples/follow.py
    used so I don't have to read the entire file each time
    yields end line
    """
    logfile.seek(0, os.SEEK_END)
    while True:
        line = logfile.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line


if __name__ == "__main__":
    mostrecent = None
    home = os.path.expanduser('~')
    with open(os.path.join(home, 'Documents\\My Games\\Fallout4\\Logs\\Script\\Papyrus.0.log')) as f:
        for line in followLog(f):
            try:
                location = re.search(r'\[Cell <(.+?) \(', line)[1]
            except TypeError:
                continue
            try:
                loot = cells[location]
            except KeyError:
                continue
            if location in cells and loot != mostrecent:
                print(f'\n\n\033[96m{location}\033[0m')
                if loot is not None:
                    print(loot)
                else:
                    print('There is no notable loot here')
                mostrecent = loot
