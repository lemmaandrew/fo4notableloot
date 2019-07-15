"""While Fallout 4 is running, checks the logs for location updates,
and prints the relevant text into the terminal
"""
import json
import os
import re
import time


with open('.\\cellloot.json') as f:
    LOOT = json.load(f)
with open('.\\cellnames.json') as f:
    NAMES = json.load(f)


def follow_log(logfile):
    """Tails the file

    Blatently stolen from https://github.com/dabeaz/generators/blob/master/examples/follow.py

    Yields
    ------
    str
        end line of file
    """
    logfile.seek(0, os.SEEK_END)
    while True:
        currentline = logfile.readline()
        if not currentline:
            time.sleep(0.1)
            continue
        yield currentline


if __name__ == "__main__":
    mostrecent = None
    with open(os.path.expanduser('~\\Documents\\My Games\\Fallout4\\Logs\\Script\\Papyrus.0.log')) as f:
        for line in follow_log(f):
            try:
                location = re.search(r'\[Cell <(.+?) \(', line)[1]
                loot = LOOT[location]
                name = NAMES[location]
            except (TypeError, KeyError):
                continue
            if loot != mostrecent:
                print(f'\n\n\033[96m{name}\033[0m')
                if loot is not None:
                    print(loot)
                else:
                    print('There is no notable loot here')
                mostrecent = loot
