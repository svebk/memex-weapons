#!/bin/bash
# launch from /srv/skaraman
#export LD_LIBRARY_PATH=/srv/skaraman/anaconda/envs/memex-weapons/lib/:$LD_LIBRARY_PATH
#export LD_LIBRARY_PATH="/srv/skaraman/caffe/build/lib:/usr/local/cuda-6.5/lib64:/srv/skaraman/anaconda/envs/memex-weapons/lib/:$LD_LIBRARY_PATH"
#export LD_LIBRARY_PATH="/srv/skaraman/caffe/build/lib:/usr/local/cuda-6.5/lib64:/usr/lib/x86_64-linux-gnu/:/srv/skaraman/anaconda/envs/memex-weapons/lib/:$LD_LIBRARY_PATH"
export LD_LIBRARY_PATH="/srv/skaraman/caffe/build/lib:/usr/local/cuda/lib64:/usr/lib/x86_64-linux-gnu/:/srv/skaraman/anaconda/envs/memex-weapons/lib/:$LD_LIBRARY_PATH"
./tools/caffe train --solver=/srv/skaraman/weapons/memex-weapons/deepmodels/CNN_20K_solver_ukhack_annotated.txt --weights=/srv/skaraman/weapons/memex-weapons/deepmodels/CNN_20K.caffemodel
