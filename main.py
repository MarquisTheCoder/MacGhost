
from torHandler import TorHandler
from commands import optHandler
import sys
import os

def main():
    # if not os.geteuid() == 0:
    #     sys.exit("\nOnly root can run this script\n") 
    optHandler.displayHeader()
    optHandler.displayOption()

if __name__ == "__main__":
    main()