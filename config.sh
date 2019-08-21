#!/bin/bash

:<<!
PARAMETER TABLE:
c->chip
s->system
p->path
b->blas
a->acl
n->ndk
l->android-level
f->fp16
t->TELIFE
o->ONNX
e->CAFFE
m->MXNET
r->TF
w->FRAMEWORK
!

while getopts ":c:s:p:b:a:n:l:f:t:o:e:m:r:w:" opt
do
    case $opt in
        c)
        echo "chip: $OPTARG"
        chip="$OPTARG"
        ;;
        s)
        echo "system: $OPTARG"
        system="$OPTARG"
        ;;
        p)
        echo "path: $OPTARG"
        path="$OPTARG"
        ;;
        b)
        echo "blas: $OPTARG"
        blas="$OPTARG"
        ;;
        a)
        echo "acl: $OPTARG"
        acl="$OPTARG"
        ;;
        n)
        echo "ndk: $OPTARG"
        ndk="$OPTARG"
        ;;
        l)
        echo "android_level: $OPTARG"
        android_level="$OPTARG"
        ;;
        f)
        echo "FP16: $OPTARG"
        FP16="$OPTARG"
        ;;
        t)
        echo "TFLIFE: $OPTARG"
        TFLIFE=$OPTARG
        ;;
        o)
        echo "ONNX: $OPTARG"
        ONNX=$OPTARG
        ;;
        e)
        echo "CAFFE: $OPTARG"
        CAFFE=$OPTARG
        ;;
        m)
        echo "MXNET: $OPTARG"
        MXNET=$OPTARG
        ;;
        r)
        echo "TF: $OPTARG"
        TF=$OPTARG
        ;;
        w)
        echo "FRAMEWORK: $OPTARG"
        FRAMEWORK=$OPTARG
        ;;
    esac
done

ACL_DIR=${path%/tengine}

ARCH_TYPE_V7="ARMv7"
ARCH_TYPE_V8="ARMv8"
ANDROID_BUILD_V7="android_build_armv7.sh"
ANDROID_BUILD_V8="android_build_armv8.sh"
DTENGINE_DIR_V7="home/usr/tengine"
DTENGINE_DIR_V8="/root/work/git/tengine_auto/tengine"

function config_android() {
  tengine_dir="${path}"
  cd ${tengine_dir}
  if [ -e android_config.txt ]; then
    rm -rf android_config.txt
    echo "CONFIG_ARCH_TYPE:${1}" >> android_config.txt
    echo "PROTOBUF_DIR:/root/peter/protobuf_lib" >> android_config.txt
    echo "CONFIG_VERSION_POSTFIX:" >> android_config.txt
    echo "BLAS_DIR:/root/peter/Openblas0220-android" >> android_config.txt
  fi
  echo "modify examples/${2}"
  grep "${3}" -rl examples/${2} | xargs sed -i "s:${3}:$tengine_dir:g"
  grep "/home/usr" -rl examples/${2} | xargs sed -i "s:home\/usr:root\/peter:g"
  grep "DBLAS_DIR" -rl examples/${2} | xargs sed -i "s:openblas_lib:Openblas0220-android:g"
  grep "DACL_DIR" -rl examples/${2} | xargs sed -i "s:acl_lib:ComputeLibrary:g"
  
  if [[ ${ndk} != "r16b" ]]; then
    grep "android-ndk-r16b" -rl examples/${2} | xargs sed -i "s:android-ndk-r16b:android-ndk-$ndk:g"
    grep "protobuf_lib" -rl examples/${2} | xargs sed -i "s:protobuf_lib:protobuf_r19:g"
  fi

  echo "                                                                "
  echo "===============${2} contents=================="
  cat examples/${2}
  echo "================================================================"
  echo "                                                                "
}

function config_linux_1() {
  tengine_dir="${path}"
  cd ${tengine_dir}
  rm -rf makefile.config
  cp -rf makefile.config.example makefile.config
}

function config_linux_2() {
  grep "home/haitao/workshop/tengine" -rl examples/linux_build.sh  | xargs sed -i "s:/home\\/haitao\\/workshop\\/tengine:$tengine_dir:g"
  grep "home/usr/acl_lib" -rl examples/linux_build.sh  | xargs sed -i "s:/home\\/usr\\/acl_lib:$ACL_DIR\\/ComputeLibrary\\/build:g"
  echo "===============examples/linux_build.sh contents=================="
  cat examples/linux_build.sh
  echo "================================================================="
}

if [ "$chip" = "armv8" ]; then
  if [ "$system" = "android" ]; then
    config_android ${ARCH_TYPE_V8} ${ANDROID_BUILD_V8} ${DTENGINE_DIR_V8}
  else
    config_linux_1
    config_linux_2
  fi
else
  if [ "$system" = "android" ]; then
    config_android ${ARCH_TYPE_V7} ${ANDROID_BUILD_V7} ${DTENGINE_DIR_V7}
  else
    config_linux_1
    grep "CONFIG_ARCH_ARM64=y" -rl makefile.config  | xargs sed -i "s/CONFIG_ARCH_ARM64=y/# CONFIG_ARCH_ARM64=y/g"
    grep "# CONFIG_ARCH_ARM32=y" -rl makefile.config  | xargs sed -i "s/# CONFIG_ARCH_ARM32=y/CONFIG_ARCH_ARM32=y/g"
    config_linux_2
  fi
fi

if [ "$system" = "android" ]; then
    if [ -z "$ndk" ]; then
        echo "please input ndk"
    else
        echo "ANDROID_NDK:/root/peter/android-ndk-$ndk" >> android_config.txt
    fi
    if [ "$blas" = "true" ]; then
        echo "CONFIG_ARCH_BLAS:ON" >> android_config.txt
    else
        echo "CONFIG_ARCH_BLAS:OFF" >> android_config.txt
    fi
    if [ "$acl" = "true" ]; then
        echo "CONFIG_ACL_GPU:ON" >> android_config.txt
        echo "ACL_ROOT:/root/peter/ComputeLibrary" >> android_config.txt
    fi
    if [ -z "$android_level" ]; then
        echo "please input android_level"
    else
        echo "API_LEVEL:$android_level" >> android_config.txt
    fi
    echo "CONFIG_KERNEL_FP32:ON" >> android_config.txt
    echo "CONFIG_KERNEL_INT8:ON" >> android_config.txt
    echo "CONFIG_KERNEL_UINT8:ON" >> android_config.txt
    if [ "$FP16" = "true" ]; then
        echo "CONFIG_KERNEL_FP16:ON"  >> android_config.txt
        grep "protobuf_lib" -rl android_config.txt | xargs sed -i "s:protobuf_lib:protobuf_r19:g"
    else
        echo "CONFIG_KERNEL_FP16:OFF" >> android_config.txt
    fi
    if [ "$TFLIFE" = "true" ]; then
        echo "CONFIG_TFLITE_SERIALIZER:ON" >> android_config.txt
    else
        echo "CONFIG_TFLITE_SERIALIZER:OFF" >> android_config.txt
    fi
    if [ "$ONNX" = "true" ]; then
        echo "CONFIG_ONNX_SERIALIZER:ON" >> android_config.txt
    else
        echo "CONFIG_ONNX_SERIALIZER:OFF" >> android_config.txt
    fi
    if [ "$CAFFE" = "true" ]; then
        echo "CONFIG_CAFFE_SERIALIZER:ON" >> android_config.txt
    else
        echo "CONFIG_CAFFE_SERIALIZER:OFF" >> android_config.txt
    fi
    if [ "$MXNET" = "true" ]; then
        echo "CONFIG_MXNET_SERIALIZER:ON" >> android_config.txt
    else
        echo "CONFIG_MXNET_SERIALIZER:OFF" >> android_config.txt
    fi
    if [ "$TF" = "true" ]; then
        echo "CONFIG_TF_SERIALIZER:ON" >> android_config.txt
    else
        echo "CONFIG_TF_SERIALIZER:OFF" >> android_config.txt
    fi
    echo "==================android_config.txt contents==================="
    cat android_config.txt
    echo "================================================================"
else
    if [ "$acl" = "true" ]; then
        grep "# CONFIG_ACL_GPU=y" -rl makefile.config  | xargs sed -i "s/# CONFIG_ACL_GPU=y/CONFIG_ACL_GPU=y/g"
	    grep "ACL_LIB" -rl linux_build.sh | xargs sed -i "s:/root\\/acllib:$ACL_DIR\\/ComputeLibrary\\/build:g"
	    grep "ACL_CFLAGS" -rl linux_build.sh | xargs sed -i "s:/root\\/aclinclude:$ACL_DIR\\/ComputeLibrary:g"
    fi
    if [ "$blas" = "true" ]; then
        grep "# CONFIG_ARCH_BLAS=y" -rl makefile.config  | xargs sed -i "s/# CONFIG_ARCH_BLAS=y/CONFIG_ARCH_BLAS=y/g"
    fi
    if [ "$CAFFE" != "true" ]; then
	    grep "CONFIG_CAFFE_SERIALIZER=y" -rl makefile.config  | xargs sed -i "s/CONFIG_CAFFE_SERIALIZER=y/# CONFIG_CAFFE_SERIALIZER=y/g"
    fi
    if [ "$MXNET" = "true" ]; then
        grep "# CONFIG_MXNET_SERIALIZER=y" -rl makefile.config  | xargs sed -i "s/# CONFIG_MXNET_SERIALIZER=y/CONFIG_MXNET_SERIALIZER=y/g"
    fi
    if [ "$ONNX" = "true" ]; then
        grep "# CONFIG_ONNX_SERIALIZER=y" -rl makefile.config  | xargs sed -i "s/# CONFIG_ONNX_SERIALIZER=y/CONFIG_ONNX_SERIALIZER=y/g"
    fi
    if [ "$TF" = "true" ]; then
        grep "# CONFIG_TF_SERIALIZER=y" -rl makefile.config  | xargs sed -i "s/# CONFIG_TF_SERIALIZER=y/CONFIG_TF_SERIALIZER=y/g"
    fi
    if [ "$TFLIFE" = "true" ]; then
        grep "# CONFIG_TFLITE_SERIALIZER=y" -rl makefile.config  | xargs sed -i "s/# CONFIG_TFLITE_SERIALIZER=y/CONFIG_TFLITE_SERIALIZER=y/g"
    fi
    if [ "$FRAMEWORK" = "true" ]; then
        grep "# CONFIG_FRAMEWORK_WRAPPER=y" -rl makefile.config  | xargs sed -i "s/# CONFIG_FRAMEWORK_WRAPPER=y/CONFIG_FRAMEWORK_WRAPPER=y/g"
    fi
    echo "=============makefile.config contents====================="
    cat makefile.config
    echo "=========================================================="
fi
