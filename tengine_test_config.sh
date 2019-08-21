#!/bin/bash
# Author: Shengjie.Liu
# Date: 2019-07-24
# Version: 1.0
# Description:
# How to use:

: << !
parameter table:
c->chip
s->system
p->path
b->blas
a->acl
w->wrapper
l->android-level
n->ndk
!

while getopts :c:s:p:b:a:w:l:n: opts; do
    case ${opts} in
        c)
        echo "chip=${OPTARG}"
        chip=${OPTARG}
        ;;
        s)
        echo "system=${OPTARG}"
        system=${OPTARG}
        ;;
        p)
        echo "path=${OPTARG}"
        path=${OPTARG}
        ;;
        b)
        echo "blas=${OPTARG}"
        blas=${OPTARG}
        ;;
        a)
        echo "acl=${OPTARG}"
        acl=${OPTARG}
        ;;
        w)
        echo "wrapper=${OPTARG}"
        wrapper=${OPTARG}
        ;;
        l)
        echo "android-level=${OPTARG}"
        android_level=${OPTARG}
        ;;
        n)
        echo "ndk=${OPTARG}"
        ndk=${OPTARG}
        ;;
        ?);;
    esac
done

function change_android_path() {
    grep "android-ndk" -rl ${1} | xargs sed -i "s:/home/usr/android-ndk-r16b:/root/peter/android-ndk-r16b:g"
    grep "protobuf_lib" -rl ${1} | xargs sed -i "s:/home/usr/protobuf_lib:/root/peter/protobuf_lib:g"
    grep "jni" -rl ${1} | xargs sed -i "s:/home/usr/opencv/sdk/native/jni:/root/peter/opencv/sdk/native/jni:g"
    grep "Openblas0220" -rl ${1} | xargs sed -i "s:/home/usr/Openblas0220-android:/root/peter/Openblas0220-android:g"
    grep "ComputeLibrary" -rl ${1} | xargs sed -i "s:/home/usr/ComputeLibrary:/root/peter/ComputeLibrary:g"
}

function android_config() {
        if [[ -n "${path}"  ]]; then
           grep "/home/usr/tengine_model_test" -rl ${1} | xargs sed -i "s:/home/usr/tengine_model_test:${path}tengine_model_test:g"
        fi
        if [[ ${blas} = "true" ]]; then
            grep "BLAS_DIR" -rl ${1} | xargs sed -i "s:#export BLAS_DIR=/root/peter/Openblas0220-android:export BLAS_DIR=/root/peter/Openblas0220-android:g"
        fi
        if [[ ${acl} = "true" ]]; then
            grep "ACL_DIR" -rl ${1} | xargs sed -i "s:#export ACL_DIR=/root/peter/ComputeLibrary:export ACL_DIR=/root/peter/ComputeLibrary:g"
        fi
        if [[ -n "${android_level}"  ]]; then
           grep "DANDROID_PLATFORM" -rl ${1} | xargs sed -i "s:android-21:android-${android_level}:g"
        fi
        if [[ -n "${ndk}"  ]]; then
           grep "android-ndk" -rl ${1} | xargs sed -i "s:android-ndk-r16b:android-ndk-${ndk}:g"
        fi
}

android_armv7="android_build_armv7.sh"
android_armv8="android_build_armv8.sh"

if [[ ${wrapper} = "false" ]]; then
    grep "wrapper" -rl CMakeLists.txt | xargs sed -i "s:add_subdirectory(wrapper):#add_subdirectory(wrapper):g"
fi

if [[ ${system} = "linux" ]]; then
    if [[ -n "${path}" ]]; then
        grep "/home/youj/tengine_model_test" -rl linux_build.sh | xargs sed -i "s:/home/youj/tengine_model_test:${path}tengine_model_test:g"
    fi
else
    if [[ ${chip} = "armv7" ]]; then
        change_android_path ${android_armv7}
        android_config ${android_armv7}
    else
        change_android_path ${android_armv8}
        android_config ${android_armv8}
    fi
fi

