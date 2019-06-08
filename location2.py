from bs4 import BeautifulSoup
import json
import re
import requests
import time


with open('cells.json') as f:
    cells = json.load(f)
cache = set()
rxloc = re.compile(r'\[Cell <(\w+?) \([0-9A-F]{8}\)>\]')


def grabInfo(url):
    try:
        soup = BeautifulSoup(requests.get(url).text, 'html.parser')
        loot = soup.find(text='Notable loot')
        if loot is not None:
            loot = loot.findAllNext()[3].getText().strip().split('\n')
            for i, v in enumerate(loot):
                loot[i] = ':: ' + v
            return '\n'.join(loot)
        else:
            return None
    except ConnectionError:
        return None


if __name__ == "__main__":
    while True:
        #IF YOU GOT THIS FILE FROM MY GITHUB YOU NEED TO REPLACE "MYNAME" WITH YOUR COMPUTER USERNAME
        with open(r'C:\Users\MyName\Documents\My Games\Fallout4\Logs\Script\Papyrus.0.log') as f:
            location = rxloc.findall(f.read())[-1]
            if location in cells and cells[location] not in cache:
                print(f'\n\n\033[96m{location}\033[0m')
                loot = grabInfo(f'https://fallout.fandom.com{cells[location]}')
                if loot is not None:
                    print(loot)
                else:
                    print('There is no notable loot here')
                cache.add(cells[location])
        time.sleep(5)
