import pytest
import os
import asciitable
import collections
import pdb
from Connect import connect
from Connect import boardInfo


caffeClassifyModelsTestName=['caffe_squeezenet','caffe_mobilenet','caffe_mobilenet_v2','caffe_alexnet','caffe_googlenet','caffe_inception_v3','caffe_inception_v4','caffe_resnet50','caffe_vgg16']

caffeExamplesModelsTestName=['caffe_ssd','caffe_mssd','caffe_mtcnn_4faces','caffe_mtcnn_6faces','caffe_yolov2','caffe_lighten_cnn','caffe_faster_rcnn',]

onnxClassifyModelsTestName=['onnx_squeezenet']

mxnetClassifyModelsTestName=['mxnet_squeezenet','mxnet_mobilenet','mxnet_mobilenet_v2','mxnet_alexnet','mxnet_inception_v3','mxnet_resnet50','mxnet_vgg16']

tensorflowClassifyModelsTestName=['tensorflow_squeezenet','tensorflow_inception_resnet_v2','tensorflow_mobilenet_v1_0_75','tensorflow_mobilenet','tensorflow_mobilenet_v2','tensorflow_inception_v3','tensorflow_inception_v4','tensorflow_resnet50','tensorflow_resnet_v2','tensorflow_nasnet','tensorflow_densenet']

tensorflowExamplesModelsTestName=[]

tfliteClassifyModelsTestName=['tflite_mobilenet','tflite_mobilenet_v2','tflite_inception_v3']

tengineClassifyModelsTestName=['tengine_squeezenet_caffe','tengine_mobilenet_caffe','tengine_mobilenet_v2_caffe','tengine_alexnet_caffe','tengine_googlenet_caffe','tengine_inception_v3_caffe','tengine_inception_v4_caffe','tengine_resnet50_caffe','tengine_vgg16_caffe','tengine_squeezenet_on','tengine_squeezenet_mx','tengine_mobilenet_mx','tengine_mobilenet_v2_mx','tengine_alexnet_mx','tengine_inception_v3_mx','tengine_resnet50_mx','tengine_vgg16_mx','tengine_squeezenet_tf','tengine_mobilenet_tf','tengine_mobilenet_v2_tf','tengine_inception_v3_tf','tengine_inception_v4_tf','tengine_resnet50_tf','tengine_resnet_v2_tf','tengine_inception_resnet_v2_tf','tengine_mobilenet_v1_0_75_tf','tengine_nasnet_tf','tengine_densenet_tf','tengine_mobilenet_tflite','tengine_mobilenet_v2_tflite','tengine_inception_v3_tflite']

#tengineClassifyModelsTestName=['tengine_squeezenet_caffe','tengine_mobilenet_caffe','tengine_mobilenet_v2_caffe','tengine_googlenet_caffe','tengine_inception_v3_caffe','tengine_inception_v4_caffe','tengine_resnet50_caffe','tengine_squeezenet_on','tengine_squeezenet_mx','tengine_mobilenet_mx','tengine_mobilenet_v2_mx','tengine_inception_v3_mx','tengine_mobilenet_tflite','tengine_mobilenet_v2_tflite','tengine_inception_v3_tflite']

tengineExamplesModelsTestName=['tengine_ssd','tengine_mssd','tengine_mtcnn_4faces','tengine_mtcnn_6faces','tengine_yolov2','tengine_lighten_cnn','tengine_faster_rcnn']
#tengineExamplesModelsTestName=['tengine_ssd','tengine_mssd','tengine_mtcnn_4faces','tengine_mtcnn_6faces','tengine_lighten_cnn','tengine_faster_rcnn']

caffeWrapperTestName=['caffe_wrapper_sqz','caffe_wrapper_mobilenet','caffe_wrapper_inception_v3','caffe_wrapper_mtcnn_4faces','caffe_wrapper_mtcnn_6faces']

tensorflowWrapperTestName=['tensorflow_wrapper_inceptionv3','tensorflow_wrapper_mobilenet','tensorflow_wrapper_resnet50',]

quantInt8TestName=['quant_squeezenet_Int8','quant_mobilenet_Int8','quant_mobilenet_v2_Int8','quant_alexnet_Int8','quant_googlenet_Int8','quant_inception_v3_Int8','quant_inception_v4_Int8','quant_resnet50_Int8','quant_vgg16_Int8','quant_squeezenet_mx_Int8','quant_mobilenet_mx_Int8','quant_squeezenet_on_Int8','quant_squeezenet_tf_Int8','quant_mobilenet_tf_Int8','quant_mobilenet_v2_tf_Int8','quant_resnet50_tf_Int8','quant_resnet_v2_tf_Int8',]

#quantInt8TestName=['quant_squeezenet_Int8','quant_mobilenet_Int8','quant_mobilenet_v2_Int8','quant_alexnet_Int8','quant_googlenet_Int8','quant_inception_v3_Int8','quant_inception_v4_Int8','quant_resnet50_Int8','quant_vgg16_Int8','quant_squeezenet_mx_Int8','quant_mobilenet_mx_Int8','quant_squeezenet_on_Int8',]

#quantFP16ClassifyTestName=['quant_squeezenet_fp16','quant_mobilenet_fp16','quant_mobilenet_v2_fp16','quant_alexnet_fp16','quant_googlenet_fp16','quant_inception_v3_fp16','quant_inception_v4_fp16','quant_resnet50_fp16','quant_vgg16_fp16','quant_squeezenet_mx_fp16','quant_mobilenet_mx_fp16','quant_squeezenet_on_fp16','quant_squeezenet_tf_fp16','quant_mobilenet_tf_fp16','quant_mobilenet_v2_tf_fp16','quant_resnet50_tf_fp16','quant_resnet_v2_tf_fp16']

quantFP16ClassifyTestName=[]

#quantFP16ExamplesTestName=['quant_ssd_fp16','quant_mssd_fp16','quant_lighten_cnn_fp16','quant_yolov2_fp16','quant_faster_rcnn_fp16','quant_mtcnn_4faces_fp16','quant_mtcnn_6faces_fp16',]
quantFP16ExamplesTestName=[]

tengineModelsTestName=tengineClassifyModelsTestName + tengineExamplesModelsTestName

wrapperTestName=caffeWrapperTestName + tensorflowWrapperTestName

caffeModelsTestName=caffeClassifyModelsTestName + caffeExamplesModelsTestName
tensorflowModelsTestName=tensorflowClassifyModelsTestName + tensorflowExamplesModelsTestName
onnxModelsTestName=onnxClassifyModelsTestName
mxnetModelsTestName=mxnetClassifyModelsTestName
tfliteModelsTestName=tfliteClassifyModelsTestName

modelsTestname=caffeClassifyModelsTestName + caffeExamplesModelsTestName + onnxClassifyModelsTestName + mxnetClassifyModelsTestName + tensorflowClassifyModelsTestName + tensorflowExamplesModelsTestName + tfliteClassifyModelsTestName + tengineModelsTestName

#performanceTestName=caffeClassifyModelsTestName + caffeExamplesModelsTestName + onnxClassifyModelsTestName + mxnetClassifyModelsTestName + tensorflowClassifyModelsTestName + tensorflowExamplesModelsTestName + tfliteClassifyModelsTestName

#performanceTestName=caffeClassifyModelsTestName + caffeExamplesModelsTestName + tensorflowClassifyModelsTestName
performanceTestName=tengineModelsTestName
quantFP16TestName=quantFP16ClassifyTestName + quantFP16ExamplesTestName

quantTestName=quantInt8TestName+quantFP16TestName

commonModels_testname=caffeClassifyModelsTestName + onnxClassifyModelsTestName + mxnetClassifyModelsTestName + tensorflowClassifyModelsTestName + tfliteClassifyModelsTestName + tengineClassifyModelsTestName + quantInt8TestName+ quantFP16ClassifyTestName

examplesModels_testname=caffeExamplesModelsTestName + tensorflowExamplesModelsTestName + tengineExamplesModelsTestName + tengineExamplesModelsTestName + quantFP16ExamplesTestName

DataType=['FP32','Int8']

def caseList(testname,CPUlist):
    testlist = []
    i=0
    while i<len(testname):
        j=0
        while j<len(DataType):
            k=0
            while k<len(CPUlist):
                functionTestName=testname[i]+"_"+DataType[j]+"_"+CPUlist[k]
                testlist.append(functionTestName)
                k=k+1
            j=j+1
        i=i+1
    return testlist

def pytest_addoption(parser):
    parser.addoption(
        "--cmdopt", action="store", default="onboard",
        help="my option: onboard or cc or adb"
    )
    parser.addoption(
        "--targetdir", action="store", default="/root/tengine/",
        help="dir of target targetdir"
    )
    parser.addoption(
        "--ip", action="store", default="",
        help="ip of android device"
    )
@pytest.fixture
def cmdopt(request):
    return request.config.getoption("--cmdopt")

@pytest.fixture
def targetdir(request):
    return request.config.getoption("--targetdir")

@pytest.fixture
def ip(request):
    return request.config.getoption("--ip")

@pytest.fixture(scope='session')
def shell(pytestconfig):
    targetdir=pytestconfig.getoption('targetdir')
    shell = connect(targetdir)
    return shell

@pytest.fixture(scope='session')
def check_dict(pytestconfig):
    targetdir=pytestconfig.getoption('targetdir')
    CPUlist = boardInfo(targetdir)['cpuinfo']
    commonModelsTestList = caseList(commonModels_testname,CPUlist)
    examplesModelsTestList = caseList(examplesModels_testname,CPUlist)
    caffeWrapperTestList = caseList(caffeWrapperTestName,CPUlist)
    tensorflowWrapperTestList = caseList(tensorflowWrapperTestName,CPUlist)
    return (commonModelsTestList,examplesModelsTestList,caffeWrapperTestList,tensorflowWrapperTestList)

def pytest_generate_tests(metafunc):
    print metafunc.config.getoption('cmdopt')
    targetdir=metafunc.config.getoption('targetdir')
    CPUlist = boardInfo(targetdir)['cpuinfo']

    caffeModelsTestList = caseList(caffeModelsTestName,CPUlist)
    onnxModelsTestList = caseList(onnxModelsTestName,CPUlist)
    mxnetModelsTestList = caseList(mxnetModelsTestName,CPUlist)
    tensorflowModelsTestList = caseList(tensorflowModelsTestName,CPUlist)
    tfliteModelsTestList = caseList(tfliteModelsTestName,CPUlist)
    tengineModelsTestList = caseList(tengineModelsTestName,CPUlist)
    quantModelsTestList = caseList(quantTestName,CPUlist)
    wrapperModelsTestList = caseList(wrapperTestName,CPUlist)
    performanceTestList = caseList(performanceTestName,CPUlist)
    performanceTestList.append('performanceTestResult')
    if "CaffeModel" in metafunc.config.getoption('cmdopt'):
        metafunc.parametrize("testcase_dict", caffeModelsTestList)
        print(caffeModelsTestList)
    elif "OnnxModel" in metafunc.config.getoption('cmdopt'):
        metafunc.parametrize("testcase_dict", onnxModelsTestList)
        print(onnxModelsTestList)
    elif "MxnetModel" in metafunc.config.getoption('cmdopt'):
        metafunc.parametrize("testcase_dict", mxnetModelsTestList)
        print(mxnetModelsTestList)
    elif "TfModel" in metafunc.config.getoption('cmdopt'):
        metafunc.parametrize("testcase_dict", tensorflowModelsTestList)
        print(tensorflowModelsTestList)
    elif "TfliteModel" in metafunc.config.getoption('cmdopt'):
        metafunc.parametrize("testcase_dict", tfliteModelsTestList)
        print(tfliteModelsTestList)
    elif "TengineModel" in metafunc.config.getoption('cmdopt'):
        metafunc.parametrize("testcase_dict", tengineModelsTestList)
        print(tengineModelsTestList)
    elif "Wrapper" in metafunc.config.getoption('cmdopt'):
        metafunc.parametrize("testcase_dict", wrapperModelsTestList)
        print(wrapperModelsTestList)
    elif "Quant" in metafunc.config.getoption('cmdopt'):
        metafunc.parametrize("testcase_dict", quantModelsTestList)
        print(quantModelsTestList)
    elif "Performance" in metafunc.config.getoption('cmdopt'):
        metafunc.parametrize("testcase_dict", performanceTestList)
        print(performanceTestList)
    else:
        print "Not support function cmdopt"