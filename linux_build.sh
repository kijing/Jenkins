#!/bin/bash
platform=3516cv500

cmake -DCMAKE_TOOLCHAIN_FILE=../linux_toolChain_${platform}.cmake \
              -DTENGINE_DIR=/root/nfs/peter/3516/tengine \
                    ..
