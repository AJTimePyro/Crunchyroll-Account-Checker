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
        proxy_filename = None
        proxyEnable = input("Do you want to enable proxy?(y/n): ")
        if proxyEnable.lower() == 'y':
            proxyEnable = True

            proxyFilename = input("Enter the name or path of proxy(http/https only) file (optional): ")
            if proxyFilename:
                if os.path.isfile(proxyFilename):
                    proxy_filename = proxyFilename
                else:
                    print("Proxy file not found, fetching proxy from internet...")
            else:
                print("Fetching proxy from internet...")
        
        else:
            proxyEnable = False
        
        src.checker.CrunchyrollChecker.create(filename, proxy_filename, proxyEnable)
    else:
        print("File not found.")


### yeaaahhhh!!!!
if __name__ == "__main__":
    main()

