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


def main():
    
    filename = input("Enter the name or path of file: ")
    if os.path.isfile(filename):
        checker = src.checker.CrunchyrollChecker(filename)
    else:
        print("File not found.")


### yeaaahhhh!!!!
if __name__ == "__main__":
    main()

