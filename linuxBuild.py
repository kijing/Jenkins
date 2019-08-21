import os
import re
import sys
import argparse
import time
reload(sys)
sys.setdefaultencoding('utf-8')
from Connect import connect
from Connect import boardInfo

def compile(rootdir,boardTengineSoDir,shell):
    list = os.listdir(rootdir)
    for i in range(0, len(list)):
        tengineSoPath = os.path.join(rootdir, list[i])
        if os.path.isfile(tengineSoPath):
            os.system("chmod 777 %s"%(tengineSoPath))
            out=shell.push(tengineSoPath,boardTengineSoDir)
    return out


def tengineConfig(boardDir,branch,chip,system,path,blas,acl,TFLITE,ONNX,CAFFE,MXNET,TF,FRAMEWORK):
    shell=connect(boardDir)
    #tengine git pull
    tengineGitpullOut = shell("cd %s;git checkout .;git pull;git checkout %s;git reset --hard origin/%s"%(path,branch,branch))
    print tengineGitpullOut
    shell.push("config.sh", path + "/config.sh")

    #tengine config file modify
    print ("cd %s;chmod 777 config.sh;%s/config.sh -c %s -s %s -p %s -b %s -a %s -t %s -o %s -e %s -m %s -r %s -w %s" % (path,path,chip,system,path,blas,acl,TFLITE,ONNX,CAFFE,MXNET,TF,FRAMEWORK))
    tengineConfigOut = shell("cd %s;chmod 777 config.sh;%s/config.sh -c %s -s %s -p %s -b %s -a %s -t %s -o %s -e %s -m %s -r %s -w %s" % (path,path,chip,system,path,blas,acl,TFLITE,ONNX,CAFFE,MXNET,TF,FRAMEWORK))
    print tengineConfigOut
    shell.disconnect()

def copyTengineSoToBoard(boardDir,path,tengineSoDir):
    shell=connect(boardDir)
    shell("cd %s;rm -rf install;mkdir install"%(path))
    shell("cd %s;mkdir install/lib;mkdir install/include;mkdir install/bin" % (path))
    compile(tengineSoDir+"/lib/", path+"/install/lib/",shell)
    compile(tengineSoDir + "/include/", path + "/install/include/",shell)
    compile(tengineSoDir + "/bin/", path + "/install/bin/", shell)
    shell.disconnect()

def tengineMake(boardDir,path):
    shell=connect(boardDir)
    tengineMakeOut = shell("cd %s;./linux_build.sh;make install"%(path),wait=False)
    for line in tengineMakeOut:
        print (line)
    if tengineMakeOut.exit_code() != 0:
        sys.exit(1)
    shell.disconnect()

def tengineTestMake(boardDir,branch):
    shell=connect(boardDir)
    # git pull
    tengineTestGitpullOut = shell("cd %s/tengine_model_test;git checkout .;git pull;git checkout %s;git reset --hard origin/%s"%(boardDir,branch,branch))
    print tengineTestGitpullOut
    if tengineTestGitpullOut.exit_code() != 0:
        sys.exit(1)
    #config file modify
    if boardDir=="/root/nfs/peter/3516/":
        shell("rm -rf %s/tengine_model_test/tests/linux_build.sh"%(boardDir))
        shell.push("linux_build.sh",boardDir+"tengine_model_test/tests/linux_build.sh")
        tengineTestConfigOut = shell(
            "cd %s/tengine_model_test;./cp_lib.sh %s/tengine;" % (boardDir, boardDir))
    else:
        tengineTestConfigOut = shell("cd %s/tengine_model_test;./cp_lib.sh %s/tengine;grep \"DROOT_DIR\" -rl tests/linux_build.sh  | xargs sed -i \"s:/home/usr/:%s:g\";grep \"wrapper\" -rl tests/CMakeLists.txt | xargs sed -i \"s:add_subdirectory(wrapper):#add_subdirectory(wrapper):g\""%(boardDir,boardDir,boardDir))
    print tengineTestConfigOut
    if tengineTestConfigOut.exit_code() != 0:
        sys.exit(1)
    #make
    tengineTestMakeOut=shell("cd %s/tengine_model_test/tests;rm -rf build;mkdir build;cd build && ../linux_build.sh && make -j4"%(boardDir),wait=False)
    for line in tengineTestMakeOut:
        print (line)
    if tengineTestMakeOut.exit_code() != 0:
        sys.exit(1)

    #print tengineTestMakeOut


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--func", help="call function", required=False,default='tengineMakeSSH')
    parser.add_argument("-d", "--boardDir", help="boardDir of device", required=True,default='/home/firefly/')
    parser.add_argument("-b", "--branch", help="branch of tengine", required=False, default='master')
    parser.add_argument("-c", "--chip", help="chip of board", required=False, default='armv8')
    parser.add_argument("-s", "--system", help="system of board", required=False, default='linux')
    parser.add_argument("-p", "--path", help="path of tengine", required=False, default='/home/firefly/tengine')
    parser.add_argument("-u", "--tengineSoDir", help="path of tengineso", required=False, default='/root/peter/autoTest/testSo/linux/64/install')
    parser.add_argument("-l", "--blas", help="blas support", required=False, default='true')
    parser.add_argument("-a", "--acl", help="acl support", required=False, default='true')
    parser.add_argument("-t", "--TFLITE", help="TFLITE support", required=False, default='true')
    parser.add_argument("-o", "--ONNX", help="ONNX support", required=False, default='true')
    parser.add_argument("-e", "--CAFFE", help="CAFFE support", required=False, default='true')
    parser.add_argument("-m", "--MXNET", help="MXNET support", required=False, default='true')
    parser.add_argument("-r", "--TF", help="TF support", required=False, default='true')
    parser.add_argument("-w", "--FRAMEWORK", help="FRAMEWORK support", required=False, default='true')
    args = parser.parse_args()
    if  args.func=="tengineConfig":
        tengineConfig(args.boardDir,args.branch,args.chip,args.system,args.path,args.blas,args.acl,args.TFLITE,args.ONNX,args.CAFFE,args.MXNET,args.TF,args.FRAMEWORK)
    elif args.func == "tengineMake":
        tengineMake(args.boardDir, args.path)
    elif args.func == "tengineTestMake":
        tengineTestMake(args.boardDir, args.branch)
    elif args.func == "copyTengineSoToBoard":
        copyTengineSoToBoard(args.boardDir, args.path ,args.tengineSoDir)

