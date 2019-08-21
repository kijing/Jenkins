import citizenshell
from serial import EIGHTBITS, PARITY_NONE
import os
import sys
sys.path.insert(0, 'expect_result/')
import firefly_linuxResult
import tinkerboard_linuxResult
import bananapi_linuxResult
import eaidk_linuxResult
import firefly_androidResult
import tinkerboard_androidResult
import bananapi_androidResult
import hi3516cv500_linuxResult
import a55_androidResult
dict_default = {'connectType':"",'assertResult':"",'board':"",'ip':"",'user':"",'password':"",'port':"",'baudrate':"",'cpuinfo':""}

dict_bananapiLinux = {'connectType':"ssh",'assertResult':bananapi_linuxResult,'board':"bananapiLinux",'ip':"192.168.91.122",
                      'user':"pi",'password':"bananapi",'port':"22",'baudrate':"",'cpuinfo':["1xA7", "4xA7"]}

dict_tinkerboardLinux = {'connectType':"ssh",'assertResult':tinkerboard_linuxResult,'board':"tinkerboardLinux",'ip':"192.168.92.197",
                      'user':"linaro",'password':"linaro",'port':"22",'baudrate':"",'cpuinfo':["1xA17", "4xA17"]}

dict_fireflyLinux = {'connectType':"ssh",'assertResult':firefly_linuxResult,'board':"fireflyLinux",'ip':"192.168.93.34",
                      'user':"firefly",'password':"firefly",'port':"22",'baudrate':"",'cpuinfo':["1xA72", "2xA72", "1xA53", "4xA53"]}

dict_rk3399proLinux = {'connectType':"ssh",'assertResult':firefly_linuxResult,'board':"rk3399proLinux",'ip':"192.168.94.16",
                      'user':"peter",'password':"12345678",'port':"22",'baudrate':"",'cpuinfo':["1xA72", "2xA72", "1xA53", "4xA53"]}

dict_rk3399Linux = {'connectType':"ssh",'assertResult':firefly_linuxResult,'board':"rk3399Linux",'ip':"192.168.92.14",
                      'user':"firefly",'password':"firefly",'port':"22",'baudrate':"",'cpuinfo':["1xA72", "2xA72", "1xA53", "4xA53"]}

dict_eaidkLinux = {'connectType':"ssh",'assertResult':eaidk_linuxResult,'board':"eaidkLinux",'ip':"192.168.89.188",
                      'user':"openailab",'password':"openailab",'port':"22",'baudrate':"",'cpuinfo':["1xA72", "2xA72", "1xA53", "4xA53"]}

dict_3516Linux_telnet = {'connectType':"telnet",'assertResult':hi3516cv500_linuxResult,'board':"3516Linux",'ip':"192.168.92.235",
                      'user':"root",'password':"123456",'port':"23",'baudrate':"",'cpuinfo':["1xA7", "2xA7"]}

dict_3516Linux_serial = {'connectType':"serial",'assertResult':eaidk_linuxResult,'board':"3516Linux",'ip':"192.168.89.121",
                      'user':"/root/",'password':"123456",'port':"/dev/ttyUSB11",'baudrate':115200,'cpuinfo':["1xA72", "2xA72", "1xA53", "4xA53"]}

dict_tinkerboardAndroid = {'connectType':"adb",'assertResult':tinkerboard_androidResult,'board':"tinkerboardAndroid",'ip':"192.168.94.55",'user':"",'password':"",'port':"",'baudrate':"",'cpuinfo':["1xA17", "4xA17"]}


dict_fireflyAndroid = {'connectType':"adb",'assertResult':firefly_androidResult,'board':"fireflyAndroid",'ip':"192.168.90.73",
                      'user':"",'password':"",'port':"",'baudrate':"",'cpuinfo':["1xA72", "2xA72", "1xA53", "4xA53"]}

dict_eaidkAndroid = {'connectType':"adb",'assertResult':firefly_androidResult,'board':"eaidkAndroid",'ip':"192.168.92.214",
                      'user':"",'password':"",'port':"",'baudrate':"",'cpuinfo':["1xA72", "2xA72", "1xA53", "4xA53"]}

dict_a55Android = {'connectType':"adb",'assertResult':a55_androidResult,'board':"spreadtrum",'ip':"192.168.92.247",
                      'user':"",'password':"",'port':"",'baudrate':"",'cpuinfo':["1xA55", "4xA55"]}

dict_bananapiAndroid = {'connectType':"adb",'assertResult':bananapi_androidResult,'board':"bananapiAndroid",'ip':"192.168.92.122",
                      'user':"",'password':"",'port':"",'baudrate':"",'cpuinfo':["1xA7", "4xA7"]}

def boardInfo(dir):
    if dir == "/home/pi/":
        return dict_bananapiLinux
    elif dir == "/home/linaro/":
        return dict_tinkerboardLinux
    elif dir == "/home/firefly/":
        return dict_fireflyLinux
    elif dir =="/home/firefly/aipark/":
        return dict_rk3399Linux
    elif dir =="/home/peter/rk3399pro/":
        return dict_rk3399proLinux
    elif dir == "/home/openailab/":
        return dict_eaidkLinux
    elif dir == "/root/nfs/peter/3516/":
        return dict_3516Linux_telnet
    elif dir =="/root/peter/":
        return dict_3516Linux_serial
    elif dir =="/root/peter/autoTest/tinkerboardAndroid/":
        return dict_tinkerboardAndroid
    elif dir =="/root/peter/autoTest/fireflyAndroid/":
        return dict_fireflyAndroid
    elif dir =="/root/peter/autoTest/eaidkAndroid/":
        return dict_eaidkAndroid
    elif dir =="/root/peter/autoTest/a55Android/":
        return dict_a55Android
    elif dir =="/root/peter/autoTest/bananapiAndroid/":
        return dict_bananapiAndroid
    else:
        print "Not support board"
        return dict_default


def connect(dir):
    connectType=boardInfo(dir)['connectType']
    host = boardInfo(dir)['ip']
    user = boardInfo(dir)['user']
    password = boardInfo(dir)['password']
    print"=================="
    print host
    print user
    print password
    print "================="
    if connectType=="ssh":
        shell = citizenshell.SecureShell(hostname=host, username=user,
                            password=password)
    elif connectType=="telnet":
        shell = citizenshell.TelnetShell(hostname=host, username=user,
                            password=password)
    elif connectType=="adb":
        shell =citizenshell.AdbShell(hostname=host)
    elif connectType=="serial":
        port=boardInfo(dir)['port']
        baudrate = boardInfo(dir)['baudrate']
        shell = citizenshell.SerialShell(port=port, username=user,
                            password=password,
                            baudrate=baudrate, parity=PARITY_NONE, bytesize=EIGHTBITS)
    else:
        shell = LocalShell()
    return (shell)