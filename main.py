#!/usr/bin/env python3
"""
       _____          __________   __________   __________   ___________   __________   _________  ___        ___  _________     _______
      /     \        |___    ___| |___    ___| |___    ___| |           | |   _______| |   ___   | \  \      /  / |   ___   |   /  ___  \
     /  / \  \           |  |         |  |         |  |     |  |\   /|  | |  |_______  |  |___|  |  \  \    /  /  |  |___|  |  /  /   \  \
    /  /___\  \          |  |         |  |         |  |     |  | \ / |  | |   _______| |   ______|   \  \  /  /   |      ___| |  |     |  |
   /  /_____\  \    __   |  |         |  |         |  |     |  |     |  | |  |         |  |           \  \/  /    |  |\  \    |  |     |  |
  /  /       \  \  |  |__|  |         |  |      ___|  |___  |  |     |  | |  |_______  |  |            |    |     |  | \  \    \  \__/   /
 /__/         \__\ |________|         |__|     |__________| |__|     |__| |__________| |__|            |____|     |__|  \__\    \_______/
"""

### Importing
# Importing Inbuilt-Packages
import os

# Importing Dev Defined Script
import src.checker


def createDir(dirname : str):
    if not os.path.exists(dirname):
        os.makedirs(dirname)

def main():
    
    createDir('result')
    createDir('resources')
    
    filename = input("Enter the name or path of file: ")
    if os.path.isfile(filename):
        proxy_filename = input("Enter the name or path of proxy(http/https only) file (optional): ")
        if not proxy_filename:
            proxy_filename = None
        elif not os.path.isfile(proxy_filename):
            proxy_filename = None
            print("Proxy file not found, fetching proxy from internet...")
        
        src.checker.CrunchyrollChecker.create(filename, proxy_filename)
    else:
        print("File not found.")


### yeaaahhhh!!!!
if __name__ == "__main__":
    main()

