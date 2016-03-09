#!/bin/bash
# launch from /srv/skaraman
#export LD_LIBRARY_PATH=/srv/skaraman/anaconda/envs/memex-weapons/lib/:$LD_LIBRARY_PATH
#export LD_LIBRARY_PATH="/srv/skaraman/caffe/build/lib:/usr/local/cuda-6.5/lib64:/srv/skaraman/anaconda/envs/memex-weapons/lib/:$LD_LIBRARY_PATH"

base_deep_dir=/srv/skaraman/weapons/memex-weapons/deepmodels

#export LD_LIBRARY_PATH="/srv/skaraman/caffe/build/lib:/usr/local/cuda-6.5/lib64:/usr/lib/x86_64-linux-gnu/:/srv/skaraman/anaconda/envs/memex-weapons/lib/:$LD_LIBRARY_PATH"
export LD_LIBRARY_PATH="/srv/skaraman/anaconda/envs/memex-weapons/lib/:$LD_LIBRARY_PATH"
./tools/caffe train --solver=$base_deep_dir/CNN_20K_solver_ukhack_annotated_lmdb.txt --weights=$base_deep_dir/CNN_20K.caffemodel
