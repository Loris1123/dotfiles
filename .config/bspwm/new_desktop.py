#!/bin/python
# Prints the number of the next empty desktop

import subprocess

# get the names (numbers) of the desktops and convert into an array
desktops = subprocess.run(["bspc", "query", "-D", "--names"], stdout=subprocess.PIPE).stdout.decode("utf-8").strip().split("\n")

# Convert all strings into ints
desktops = list(map(int, desktops))

for desktop in range(1,10):
    if desktop not in desktops:
        print(desktop)
        break
