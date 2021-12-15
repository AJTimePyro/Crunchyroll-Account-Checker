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
import src


def main():
    
    filename = input("Enter the name or path of file: ")
    if os.path.isfile(filename):
        checker = src.CrunchyrollChecker(filename)
        checker.start()
    else:
        print("File not found.")


if __name__ == "__main__":
    main()

