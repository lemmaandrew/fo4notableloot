from bs4 import BeautifulSoup
import json
import os
import re
import requests
import time


with open(r'C:\Users\Peter\Documents\Python\Fallout 4\cells.json') as f:
    cells = json.load(f)
rxloc = re.compile(r'\[Cell <(\w+?) \([0-9A-F]{8}\)>\]')


def grabInfo(url):
    """grabs the "Notable loot" section from https://fallout.fandom.com if it exists
    Returns the loot if it exists, or None if it doesn't
    """
    try:
        soup = BeautifulSoup(requests.get(url).text, 'html.parser')
        loot = soup.find(text='Notable loot')
        if loot is not None:
            loot = loot.findAllNext()[3].getText().strip().split('\n')
            for i, v in enumerate(loot):
                loot[i] = ':: ' + v.lstrip()
            return '\n'.join(loot)
        else:
            return None
    except ConnectionError:
        return None


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
            if location in cells and cells[location] != mostrecent:
                print(f'\n\n\033[96m{location}\033[0m')
                loot = grabInfo(f'https://fallout.fandom.com{cells[location]}')
                if loot is not None:
                    print(loot)
                else:
                    print('There is no notable loot here')
                mostrecent = cells[location]
