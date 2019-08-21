import os
import re
import sys
import argparse
import time
reload(sys)
sys.setdefaultencoding('utf-8')
from Connect import connect
from Connect import boardInfo

def androidPushToBoard(boardDir):
    shell=connect(boardDir)
    androidTengineTestDir=boardDir+"tengine_model_test/android_pack/"
    testDirOnBoard="/data/local/tmp/"
    shell("ls -al %s"%(testDirOnBoard+'android_pack'))
    shell("rm -rf %s"%(testDirOnBoard+'android_pack/*.so'))
    shell("rm -rf %s"%(testDirOnBoard+'android_pack/tests'))
    shell.push(androidTengineTestDir,testDirOnBoard)
    out =shell("ls -al %s"%(testDirOnBoard+'android_pack'))
    print out


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--func", help="call function", required=False,default='tengineMakeSSH')
    parser.add_argument("-d", "--boardDir", help="boardDir of device", required=True,default='/home/firefly/')
    args = parser.parse_args()
    if  args.func=="androidPushToBoard":
        androidPushToBoard(args.boardDir)

       