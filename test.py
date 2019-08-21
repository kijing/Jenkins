import pytest
import os
import asciitable
import collections
import pprint
import pdb
import subprocess
import sys
test_path = (os.path.dirname(os.path.abspath(__file__)))
import testcases
import conftest


def testTengine(testcase_dict,cmdopt,targetdir,check_dict,variables,shell):
    if "Function" in cmdopt:
        if testcase_dict in check_dict[0]:
            tc="testcases.commonModels(\"%s\",\"%s\",shell)"%(targetdir,testcase_dict)

        elif testcase_dict in check_dict[1]:
            tc="testcases.examplesModels(\"%s\",\"%s\",shell)"%(targetdir,testcase_dict)

        elif testcase_dict in check_dict[2]:
            tc="testcases.caffeWrapperModels(\"%s\",\"%s\",shell)"%(targetdir,testcase_dict)

        elif testcase_dict in check_dict[3]:
            tc="testcases.tfWrapperModels(\"%s\",\"%s\",shell)"%(targetdir,testcase_dict)

        else:
            print "testcase_dict out of testcases"
    elif "Performance" in cmdopt:
        if testcase_dict in check_dict[0]:
            tc = "testcases.performanceCommonModels(\"%s\",\"%s\",shell)"%(targetdir,testcase_dict)

        elif testcase_dict in check_dict[1]:
            tc = "testcases.performanceExampleModels(\"%s\",\"%s\",shell)"%(targetdir,testcase_dict)
        else:
            tc="testcases.%s(targetdir)"%(testcase_dict)
    print tc
    eval(tc)

