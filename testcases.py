import os
import re
import sys
import prettytable as pt
import time
reload(sys)
sys.setdefaultencoding('utf-8')

test_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(test_path)
from Connect import connect
from Connect import boardInfo
import conftest

tengine_model_test_dir = 'tengine_model_test/tests/build'
dirJpg = "images/bike.jpg"
setMEM = "export TENGINE_MEM_PROFILE=1"


def modelTestDir(targetdir):
    connectType=boardInfo(targetdir)['connectType']
    if connectType =="adb":
        tengineTestDir = "/data/local/tmp/android_pack"
    else:
        tengineTestDir = targetdir+ "tengine_model_test"
    return (tengineTestDir)


def tengineSoEnv(targetdir):
    connectType=boardInfo(targetdir)['connectType']
    if connectType =="adb":
        tengineEnv = "export LD_LIBRARY_PATH=."
    else:
        tengineEnv = "export LD_LIBRARY_PATH=%stengine_model_test/install/lib"%(targetdir)
    return (tengineEnv)



def setEnv(testcase_dict):
    if "FP32" in testcase_dict:
        setDataType = "export KERNEL_MODE=0"
    elif "FP16" in testcase_dict:
        setDataType = "export KERNEL_MODE=1"
    elif "Int8" in testcase_dict:
        setDataType = "export KERNEL_MODE=2"
    else:
        print "Env error"

    if "1xA72" in testcase_dict :
        setCPUList = "export TENGINE_CPU_LIST=5"
    elif "2xA72" in testcase_dict:
        setCPUList = "export TENGINE_CPU_LIST=4,5"
    elif "4xA551.57G" in testcase_dict:
        setCPUList = "export TENGINE_CPU_LIST=4,5,6,7"
    elif "1xA17" in testcase_dict or "1xA7" in testcase_dict or "1xA53" in testcase_dict or "1xA55" in testcase_dict:
        setCPUList = "export TENGINE_CPU_LIST=1"
    elif "4xA17" in testcase_dict or "4xA7" in testcase_dict or "4xA53" in testcase_dict or "4xA55" in testcase_dict :
        setCPUList = "export TENGINE_CPU_LIST=0,1,2,3"
    elif "2xA7" in testcase_dict:
        setCPUList = "export TENGINE_CPU_LIST=0,1"
    else:
        print "Env error"
    return (setDataType, setCPUList)


def Area_calculation(default_x0, default_y0, default_x1, default_y1, x0, y0, x1, y1):
    if default_x0 <= x0:
        Area_x0 = x0
    else:
        Area_x0 = default_x0
    if default_y0 <= y0:
        Area_y0 = y0
    else:
        Area_y0 = default_y0
    if default_x1 <= x1:
        Area_x1 = default_x1
    else:
        Area_x1 = x1
    if default_y1 <= y1:
        Area_y1 = default_y1
    else:
        Area_y1 = y1

    Area_Percentage = ((Area_x1 - Area_x0) * (Area_y1 - Area_y0)) / (
            (default_x1 - default_x0) * (default_y1 - default_y0))
    return Area_Percentage


def Get_coordinate_data(arr, Keyword, BOX_Number):
    Number = 0
    for char in arr:
        if Keyword in char:
            char_arr = char.splitlines()
            Number = arr.index(char_arr[0]) + int(BOX_Number)
    a = re.findall(r"\d+\.?\d*", arr[Number])
    return a


def commonAssertResult(Function_result,testDict, out):
    result = 'Function_result.%s' % (testDict)
    expectResult = eval(result)
    print "==========Expect Result=========="
    print expectResult
    print"==========Actual Result=========="
    print(out)
    assert expectResult in str(out)


def exampleAssertResult(Function_result,testDict, out):
    resultCar = 'Function_result.%s_car' % (testDict)
    resultBicycle = 'Function_result.%s_bicycle' % (testDict)
    resultDog = 'Function_result.%s_dog' % (testDict)
    expectResultCar = eval(resultCar)
    expectResultBicycle = eval(resultBicycle)
    expectResultDog = eval(resultDog)
    print "==========Expect Result=========="
    print(expectResultCar)
    print(expectResultBicycle)
    print(expectResultDog)
    print"==========Actual Result=========="
    print(out)
    arr = str(out).splitlines()
    a = Get_coordinate_data(arr, "car", "1")
    Area_result = Area_calculation(expectResultCar[0], expectResultCar[1], expectResultCar[2], expectResultCar[3],
                                   float(a[0]),
                                   float(a[1]), float(a[2]), float(a[3]))
    print("Area_result =%s" % (Area_result))
    assert (Area_result >= 0.90), "Area_result less than 90%"
    # check bicycle
    a = Get_coordinate_data(arr, "bicycle", "1")
    Area_result = Area_calculation(expectResultBicycle[0], expectResultBicycle[1], expectResultBicycle[2],
                                   expectResultBicycle[3],
                                   float(a[0]), float(a[1]), float(a[2]), float(a[3]))
    print("Area_result =%s" % (Area_result))
    assert (Area_result >= 0.90), "Area_result less than 90%"
    # check the dog
    a = Get_coordinate_data(arr, "dog", "1")
    Area_result = Area_calculation(expectResultDog[0], expectResultDog[1], expectResultDog[2], expectResultDog[3],
                                   float(a[0]),
                                   float(a[1]), float(a[2]), float(a[3]))
    print("Area_result =%s" % (Area_result))
    assert (Area_result >= 0.90), "Area_result less than 90%"


def mtcnnAssertResult(Function_result, MaxNumber, testDict, out):
    print "==========Expect Result=========="
    number = 1
    while number <= MaxNumber:
        result = 'Function_result.%s_%sface' % (testDict, number)
        expectResult = eval(result)
        print(expectResult)
        number = number + 1
    print"==========Actual Result=========="
    print(out)
    arr = str(out).splitlines()

    number = 1
    while number < MaxNumber:
        result = 'Function_result.%s_%sface' % (testDict, number)
        expectResult = eval(result)
        if "wrapper" in testDict:
            identification = "face %s" % (number - 1)
            a = Get_coordinate_data(arr, identification, "0")
            Area_result = Area_calculation(expectResult[0], expectResult[1], expectResult[2],
                                           expectResult[3], float(a[3]), float(a[4]), float(a[7]), float(a[8]))
        else:
            a = Get_coordinate_data(arr, "face", number)
            Area_result = Area_calculation(expectResult[0], expectResult[1], expectResult[2],
                                           expectResult[3], float(a[0]), float(a[1]), float(a[2]), float(a[3]))
        print("Area_result =%s" % (Area_result))
        assert (Area_result >= 0.90), "Area_result less than 90%"
        number = number + 1


def codeName(testcase_dict):
    i=len(testcase_dict.split('_'))-1
    a=str("_"+testcase_dict.split('_')[i])
    functionTestDict = testcase_dict.replace(a, "")
    if "mtcnn" in testcase_dict:
        caseName = "mtcnn"
    elif "quant" in testcase_dict:
        if len(testcase_dict.split('_')) == 7:
            caseName = testcase_dict.split('_')[1] + "_" + testcase_dict.split('_')[2] + "_" + testcase_dict.split('_')[3]
        elif len(testcase_dict.split('_')) == 6:
            caseName = testcase_dict.split('_')[1] + "_" + testcase_dict.split('_')[2]
        else:
            caseName = testcase_dict.split('_')[1]
    elif "tengine" in testcase_dict and "caffe" in testcase_dict :
        if len(testcase_dict.split('_')) == 7:
            caseName = testcase_dict.split('_')[1] + "_" + testcase_dict.split('_')[2] + "_" + testcase_dict.split('_')[3]
        elif len(testcase_dict.split('_')) == 6:
            caseName = testcase_dict.split('_')[1] + "_" + testcase_dict.split('_')[2]
        else:
            caseName = testcase_dict.split('_')[1]
    elif "tengine" in testcase_dict and "tflite" in testcase_dict :
        if len(testcase_dict.split('_')) == 7:
            caseName = testcase_dict.split('_')[1] + "_" + testcase_dict.split('_')[2] + "_" +testcase_dict.split('_')[3]
        elif len(testcase_dict.split('_')) == 6:
            caseName = testcase_dict.split('_')[1] + "_" + testcase_dict.split('_')[2]
        else:
            caseName = testcase_dict.split('_')[1]
    else:
        if len(testcase_dict.split('_')) == 8:
            caseName = testcase_dict.split('_')[1] + "_" + testcase_dict.split('_')[2] + "_" + testcase_dict.split('_')[3]+ "_" + testcase_dict.split('_')[4]+ "_" + testcase_dict.split('_')[5]
        elif len(testcase_dict.split('_')) == 7:
            caseName = testcase_dict.split('_')[1] + "_" + testcase_dict.split('_')[2] + "_" + testcase_dict.split('_')[3]+ "_" + testcase_dict.split('_')[4]
        elif len(testcase_dict.split('_')) == 6:
            caseName = testcase_dict.split('_')[1] + "_" + testcase_dict.split('_')[2] + "_" + testcase_dict.split('_')[3]
        elif len(testcase_dict.split('_')) == 5:
            caseName = testcase_dict.split('_')[1] + "_" + testcase_dict.split('_')[2]
        else:
            caseName = testcase_dict.split('_')[1]           
    return (caseName, functionTestDict)

def tengineModelName(testDict,tengineModeltype):
    a = str("_" + tengineModeltype)
    testDict = testDict.replace(a, "")
    if tengineModeltype == "tf":
        tengineModeltype = "tensorflow"
    if tengineModeltype == "on":
        tengineModeltype = "onnx"
    if tengineModeltype == "mx":
        tengineModeltype = "mxnet"
    testDict = testDict.replace("tengine", tengineModeltype)
    return (testDict)


def ModelsStandard(targetdir, testcase_dict,repeat,shell):
    setDataType = setEnv(testcase_dict)[0]
    setCPUList = setEnv(testcase_dict)[1]
    model = testcase_dict.split('_')[0]
    caseName = codeName(testcase_dict)[0]
    testDict = codeName(testcase_dict)[1]
    i = len(testcase_dict.split('_')) - 3
    tengineModeltype = testcase_dict.split('_')[i]
    tengineEnv = tengineSoEnv(targetdir)
    if model == "caffe":
        code = "classify"
    elif model == "mxnet":
        code = "mx_classify"
    elif model == "onnx":
        code = "on_classify"
    elif model == "tensorflow":
        code = "tf_classify"
    elif model == "tflite":
        code = "tflite_classify"
    elif model == "tengine":
        if tengineModeltype == "tflite":
            code = "tm_classify_tflite"
        else:
            code = "tm_classify"
        testDict= tengineModelName(testDict,tengineModeltype)
    elif model == "quant":
        if tengineModeltype == "Int8":
            code = "tm_classify_int8"
        elif tengineModeltype == "fp16":
            code = "tm_classify_fp16"
        else:
            print "tengineModeltype is not quant int8 or FP16"
    else:
        print "Not support Model"

    tengineTestDir = modelTestDir(targetdir)
    runDir = tengineTestDir + "/tests/build/" + model + "/classification"
    if model == "quant":
        runDir=tengineTestDir + "/tests/build/tengine/classification"
    if "resnet" in testcase_dict:
        runCase = "%s/%s -n %s -i %s" % (runDir,code, caseName, dirJpg)
    elif "vgg16" in testcase_dict:
        runCase = "%s/%s -n %s -i %s" % (runDir,code, caseName, dirJpg)
    elif "vgg19" in testcase_dict:
        runCase = "%s/%s -n %s -i %s" % (runDir,code, caseName, dirJpg)
    else:
        runCase = "%s/%s -n %s" % (runDir,code, caseName)
    print ("=======env=========")
    print (setDataType)
    print (setCPUList)
    print (repeat)
    print ("======runCase======")
    print ("cd %s;%s;%s;%s;%s;%s -r %s" % (tengineTestDir, setMEM, setDataType,tengineEnv, setCPUList,runCase,repeat))
    out = shell("cd %s;%s;%s;%s;%s;%s -r %s > log 2>&1;cat log" % (tengineTestDir, setMEM, setDataType,tengineEnv, setCPUList,runCase,repeat))
    return(testDict,out)


def examplesModelsStandard(targetdir, testcase_dict ,repeat,shell):
    setDataType = setEnv(testcase_dict)[0]
    setCPUList = setEnv(testcase_dict)[1]
    setRepeat="export REPEAT_COUNT=%s"%(repeat)
    model = testcase_dict.split('_')[0]
    dirName = codeName(testcase_dict)[0]
    testDict = codeName(testcase_dict)[1]
    tengineTestDir = modelTestDir(targetdir)
    tengineEnv = tengineSoEnv(targetdir)
    if model == "quant":
        model = "tengine"
    if "mssd" in testcase_dict:
        runDir = modelTestDir(targetdir)+"/tests/build/" + model + '/detection/mobilenet_ssd/'
    else:
        runDir = modelTestDir(targetdir)+"/tests/build/" + model + '/detection/'+ dirName+'/'

    if model == "tengine":
        caseName = "tm_"+dirName
        testDict=testDict.replace("tengine", "caffe")

    elif model =="quant":
        caseName = "tm_" + dirName+"_fp16"
    else:
        caseName = dirName
    if "mtcnn_6faces" in testcase_dict:
        runCase = runDir + caseName + " " + tengineTestDir + "/images/mtcnn_face6.jpg" + " " + tengineTestDir + "/models" + " mtcnn_6faces_result.jpg"
    elif "mtcnn_4faces" in testcase_dict:
        runCase = runDir + caseName + " " + tengineTestDir + "/images/mtcnn_face4.jpg" + " " + tengineTestDir + "/models" + " mtcnn_4faces_result.jpg"
    else:
        runCase = runDir + caseName
    print ("=======env=========")
    print (setDataType)
    print (setCPUList)
    print (setRepeat)
    print ("======runCase======")
    print ("cd %s;%s;%s;%s;%s;%s;%s" % (tengineTestDir, setMEM, setDataType,tengineEnv, setCPUList,setRepeat, runCase))
    out = shell("cd %s;%s;%s;%s;%s;%s;%s > log 2>&1;cat log" % (tengineTestDir, setMEM, setDataType,tengineEnv, setCPUList,setRepeat, runCase))
    return (testDict,out)

def commonModels(targetdir, testcase_dict,shell):
    Function_result = boardInfo(targetdir)['assertResult']
    (testDict,out) = ModelsStandard(targetdir, testcase_dict,1,shell)
    commonAssertResult( Function_result,testDict, out)


def examplesModels(targetdir, testcase_dict,shell):
    Function_result = boardInfo(targetdir)['assertResult']
    (testDict,out) = examplesModelsStandard(targetdir, testcase_dict,1,shell)
    if "mtcnn_6faces" in testcase_dict:
        mtcnnAssertResult(Function_result,6, testDict, out)

    elif "mtcnn_4faces" in testcase_dict:
        mtcnnAssertResult(Function_result,4, testDict, out)

    elif "lighten_cnn" in testcase_dict:
        commonAssertResult(Function_result,testDict, out)
    else:
        exampleAssertResult(Function_result,testDict, out)




# wrapper test
def caffeWrapperModels(targetdir, testcase_dict,shell):
    Function_result = boardInfo(targetdir)['assertResult']
    setDataType = setEnv(testcase_dict)[0]
    setCPUList = setEnv(testcase_dict)[1]
    testDict = codeName(testcase_dict)[1]
    tengineTestDir =  targetdir + "tengine_model_test"
    commonRunDir=targetdir + tengine_model_test_dir + '/wrapper/caffe_wrapper/classification'
    mtcnnWrapperDir = targetdir + tengine_model_test_dir + '/wrapper/caffe_wrapper/mtcnn'
    imagenetMean = tengineTestDir + "/models/imagenet_mean.binaryproto "
    synsetWords = tengineTestDir + "/models/synset_words.txt "
    inceptionSynsetWords = tengineTestDir + "/models/synset2015.txt "
    fileJpg = tengineTestDir + "/images/cat.jpg"

    if "caffe_wrapper_sqz" in testcase_dict:
        modelsPrototxt = tengineTestDir + "/models/sqz.prototxt "
        modelsCaffemodel = tengineTestDir + "/models/squeezenet_v1.1.caffemodel "
        codeCommand = "/caffe_classify "
        runCase = commonRunDir + codeCommand + modelsPrototxt + modelsCaffemodel + imagenetMean + synsetWords + fileJpg
    elif "caffe_wrapper_mobilenet" in testcase_dict:
        modelsPrototxt = tengineTestDir + "/models/mobilenet_deploy.prototxt "
        modelsCaffemodel = tengineTestDir + "/models/mobilenet.caffemodel "
        codeCommand = "/caffe_classify_mobilenet "
        runCase = commonRunDir + codeCommand + modelsPrototxt + modelsCaffemodel + imagenetMean + synsetWords + fileJpg
    elif "caffe_wrapper_inception_v3" in testcase_dict:
        modelsPrototxt = tengineTestDir + "/models/deploy_inceptionV3.prototxt "
        modelsCaffemodel = tengineTestDir + "/models/deploy_inceptionV3.caffemodel "
        codeCommand = "/caffe_classify_inceptionv3 "
        runCase = commonRunDir + codeCommand + modelsPrototxt + modelsCaffemodel + imagenetMean + inceptionSynsetWords + fileJpg
    elif "caffe_wrapper_mtcnn_4faces" in testcase_dict:
        codeCommand = "/caffe_mtcnn "
        runCase = mtcnnWrapperDir + codeCommand + tengineTestDir + "/images/mtcnn_face4.jpg " + tengineTestDir + "/models " + "wrapper_result4.jpg"
    else:
        codeCommand = "/caffe_mtcnn "
        runCase = mtcnnWrapperDir + codeCommand + tengineTestDir + "/images/mtcnn_face6.jpg " + tengineTestDir + "/models " + "wrapper_result6.jpg"
    print ("=======env=========")
    print (setDataType)
    print (setCPUList)
    print ("======runCase======")
    print ("cd %s;%s;%s;%s" % (tengineTestDir, setDataType, setCPUList,runCase))
    out = shell("cd %s;%s;%s;%s > log 2>&1;cat log" % (tengineTestDir, setDataType, setCPUList,runCase), "r")
    if "caffe_wrapper_mtcnn_6faces" in testcase_dict:
        mtcnnAssertResult(Function_result, 6, testDict, out)

    elif "caffe_wrapper_mtcnn_4faces" in testcase_dict:
        mtcnnAssertResult(Function_result, 4, testDict, out)

    else:
        commonAssertResult(Function_result, testDict, out)


def tfWrapperModels(targetdir, testcase_dict,shell):
    Function_result = boardInfo(targetdir)['assertResult']
    setDataType = setEnv(testcase_dict)[0]
    setCPUList = setEnv(testcase_dict)[1]
    testDict = codeName(testcase_dict)[1]
    tengineTestDir =  targetdir + "tengine_model_test"
    runDir=targetdir + tengine_model_test_dir + '/wrapper/tensorflow_wrapper/label_image/'
    fileJpg = tengineTestDir + "/images/bike.jpg"
    codeCommand = "label_image_" + testcase_dict.split('_')[2]
    print (codeCommand)
    if "resnet50" in testcase_dict:
        runCase = runDir+codeCommand + " -i " + fileJpg
    else:
        runCase = runDir+codeCommand
    print ("=======env=========")
    print (setDataType)
    print (setCPUList)
    print ("======runCase======")
    print ("cd %s;%s;%s;%s" % (tengineTestDir, setDataType,setCPUList, runCase))
    out = shell("cd %s;%s;%s;%s > log 2>&1;cat log" % (tengineTestDir, setDataType,setCPUList, runCase))
    commonAssertResult(Function_result, testDict, out)

# Performance

time_percentage = 1.1
performance_testname = conftest.performanceTestName
tengine_testname=conftest.tengineModelsTestName
dataType =conftest.DataType

CPUlist=["1xA72","2xA72","1xA53","4xA53","1xA7","4xA7","2xA7","1xA17","4xA17", "1xA55", "4xA55"]
checklist = ['time', 'ppm', 'spm', 'epm', 'ampm']
i = 0
testmap = {}
while i < len(performance_testname):
    j = 0
    while j < len(dataType):
        k = 0
        while k < len(CPUlist):
            l = 0
            while l < len(checklist):
                testmap[performance_testname[i] + "_" + dataType[j] + "_" + CPUlist[k] + "_" + checklist[l]] = 0.0
                l = l + 1
            k = k + 1
        j = j + 1
    i = i + 1


def performanceCommonAssertResult(targetdir,testcase_dict,testDict, out):
    Function_result = boardInfo(targetdir)['assertResult']
    cpuInfo=boardInfo(targetdir)['cpuinfo']
    i = len(testDict.split('_')) - 1
    a = str("_" + testDict.split('_')[i])
    performanceTestExpectResultName = testDict.replace(a, "")
    arr = str(out).splitlines()
    a = Get_coordinate_data(arr, "epeat", "0")
    b = Get_coordinate_data(arr, "peak", "0")
    c = Get_coordinate_data(arr, "sustain", "0")
    d = Get_coordinate_data(arr, "executable", "0")
    e = Get_coordinate_data(arr, "anon", "0")
    testmap["%s_time" % (testcase_dict)] = float(a[1])
    testmap["%s_ppm" % (testcase_dict)] = round(float(b[0]) / 1024, 2)
    testmap["%s_spm" % (testcase_dict)] = round(float(c[0]) / 1024, 2)
    testmap["%s_epm" % (testcase_dict)] = round(float(d[0]) / 1024, 2)
    testmap["%s_ampm" % (testcase_dict)] = round(float(e[0]) / 1024, 2)
    time.sleep(5)
    if len(cpuInfo)==4:
        if "FP32" in testcase_dict:
            if cpuInfo[0] in testcase_dict:
                yuan = 0
            elif cpuInfo[1] in testcase_dict:
                yuan=2
            elif cpuInfo[2] in testcase_dict:
                yuan=4
            else:
                yuan=6
        elif "Int8" in testcase_dict:
            if cpuInfo[0] in testcase_dict:
                yuan = 1
            elif cpuInfo[1] in testcase_dict:
                yuan = 3
            elif cpuInfo[2] in testcase_dict:
                yuan = 5
            else:
                yuan = 7
    elif len(cpuInfo) == 2:
        if "FP32" in testcase_dict:
            if cpuInfo[0] in testcase_dict:
                yuan = 0
            else :
                yuan = 2
        elif "Int8" in testcase_dict:
            if cpuInfo[0] in testcase_dict:
                yuan = 1
            else:
                yuan = 3
    else:
        print "len(cpuInfo) is not 2 or 4"

    print (yuan)
    print "===performanceTestExpectResultName==="
    print performanceTestExpectResultName
    testDict = performanceTestExpectResultName + "[%s]" % (yuan)
    result = "Function_result.%s" % (testDict)
    print (result)
    expectResult = float(eval(result)) * time_percentage
    print "==========Expect Result=========="
    print(expectResult)
    print"==========Actual Result=========="
    print(out)
    assert (testmap["%s_time" % (testcase_dict)] <= expectResult), "time more than expect time"

def performanceCommonModels(targetdir, testcase_dict,shell):
    if ("inception_v3" or "inception_v4" or "vgg16") in testcase_dict:
        repeat = 30
    else:
        repeat = 50
    (testDict, out) = ModelsStandard(targetdir, testcase_dict, repeat, shell)
    performanceCommonAssertResult(targetdir,testcase_dict,testDict,out)

def performanceExampleModels(targetdir, testcase_dict,shell):

    if ("MSSD" or "MTCNN" or "LIGHTEN_CNN") in testcase_dict:
        repeat = 30
    else:
        repeat = 50
    (testDict, out) = examplesModelsStandard(targetdir, testcase_dict, repeat,shell)
    performanceCommonAssertResult(targetdir,testcase_dict,testDict,out)

def addRow(item, testName,unit, caseResult,targetdir):

    cpuInfo = boardInfo(targetdir)['cpuinfo']
    if len(cpuInfo)==4:
        caseResult.field_names = ["models", "FP32_%s(%s)" % (cpuInfo[0],unit), "Int8_%s(%s)" % (cpuInfo[0],unit),"FP32_%s(%s)" % (cpuInfo[1],unit),"Int8_%s(%s)" % (cpuInfo[1],unit), "FP32_%s(%s)" % (cpuInfo[2],unit),"Int8_%s(%s)" % (cpuInfo[2],unit),"FP32_%s(%s)" % (cpuInfo[3],unit), "Int8_%s(%s)" % (cpuInfo[3],unit)]
        caseResult.add_row([testName, testmap["%s_FP32_%s_%s" % (testName, cpuInfo[0],item)], testmap["%s_Int8_%s_%s" % (testName,cpuInfo[0], item)],testmap["%s_FP32_%s_%s" % (testName, cpuInfo[1],item)], testmap["%s_Int8_%s_%s" % (testName,cpuInfo[1] ,item)],testmap["%s_FP32_%s_%s" % (testName,cpuInfo[2], item)], testmap["%s_Int8_%s_%s" % (testName,cpuInfo[2], item)],testmap["%s_FP32_%s_%s" % (testName,cpuInfo[3], item)], testmap["%s_Int8_%s_%s" % (testName,cpuInfo[3], item)]])
    else:
        caseResult.field_names = ["models", "FP32_%s(%s)" % (cpuInfo[0],unit), "Int8_%s(%s)" % (cpuInfo[0],unit),"FP32_%s(%s)" % (cpuInfo[1],unit), "Int8_%s(%s)" % (cpuInfo[1],unit)]
        caseResult.add_row([testName, testmap["%s_FP32_%s_%s" % (testName,cpuInfo[0], item)], testmap["%s_Int8_%s_%s" % (testName,cpuInfo[0],item)],testmap["%s_FP32_%s_%s" % (testName, cpuInfo[1],item)], testmap["%s_Int8_%s_%s" % (testName, cpuInfo[1],item)]])


def performanceTestName(performancetype, unit, caseResult,targetdir):
    i = 0
    while i < len(performance_testname):
        addRow(performancetype, performance_testname[i], unit,  caseResult,targetdir)
        i = i + 1

def performanceTestResult(targetdir):
    timeCaseResult = pt.PrettyTable()
    performanceTestName("time", "ms",  timeCaseResult,targetdir)
    print "======================================"
    print "Avg time per run as below:"
    print "======================================"
    print timeCaseResult

    ppmCaseResult = pt.PrettyTable()
    performanceTestName("ppm", "MB",  ppmCaseResult,targetdir)
    print "======================================"
    print "peak phys mem (data+code) as below:"
    print "======================================"
    print ppmCaseResult

    spmCaseResult = pt.PrettyTable()
    performanceTestName("spm", "MB",  spmCaseResult,targetdir)
    print "======================================"
    print "sustain phys mem (data+code) as below:"
    print "======================================"
    print spmCaseResult

    epmCaseResult = pt.PrettyTable()
    performanceTestName("epm", "MB",  epmCaseResult,targetdir)
    print "======================================"
    print "executable phys mem (code) as below:"
    print "======================================"
    print epmCaseResult

    ampmCaseResult = pt.PrettyTable()
    performanceTestName("ampm", "MB",  ampmCaseResult,targetdir)
    print "======================================"
    print "anon mapped phys mem (data) as below:"
    print "======================================"
    print ampmCaseResult