#!/usr/bin/env sh
# This script converts the data crawled by JPL and weakly labeled into leveldb format.
#export LD_LIBRARY_PATH=/srv/skaraman/anaconda/envs/memex-weapons/lib/:$LD_LIBRARY_PATH

DBOUTLOC=/srv/skaraman/weapons/data/caffe
TOOLS=/srv/skaraman/caffe/build/tools
MEAN_TOOLS=$TOOLS
BACKEND=leveldb
DATA=/srv/skaraman/weapons/data/task1_train_ga_weak
TRAIN_DATA_ROOT=/srv/skaraman/weapons/JPL_WeaponsImages/image_dump/
TRAIN_FILE=task1_train_ga_weak.txt
TRAIN_DB_NAME=task1_train_ga_weak_$BACKEND
MEAN_NAME=task1_ga

CREATE_DB=true
CREATE_MEAN=false

# Set RESIZE=true to resize the images to 256x256. Leave as false if images have
# already been resized using another tool.
RESIZE=true
if $RESIZE; then
  RESIZE_HEIGHT=256
  RESIZE_WIDTH=256
else
  RESIZE_HEIGHT=0
  RESIZE_WIDTH=0
fi

if [ ! -d "$TRAIN_DATA_ROOT" ]; then
  echo "Error: TRAIN_DATA_ROOT is not a path to a directory: $TRAIN_DATA_ROOT"
  echo "Set the TRAIN_DATA_ROOT variable in this script to the path" \
       "where the training data is stored."
  exit 1
fi

#if [ ! -d "$VAL_DATA_ROOT" ]; then
#  echo "Error: VAL_DATA_ROOT is not a path to a directory: $VAL_DATA_ROOT"
#  echo "Set the VAL_DATA_ROOT variable in this script to the path" \
#       "where the validation data is stored."
#  exit 1
#fi

if $CREATE_DB; then
echo "Creating train "$BACKEND"..."
cat $DATA/$TRAIN_FILE | wc -l
echo $DATA/$TRAIN_FILE

GLOG_logtostderr=1 $TOOLS/convert_imageset \
    --resize_height=$RESIZE_HEIGHT \
    --resize_width=$RESIZE_WIDTH \
    --shuffle \
    --backend="$BACKEND" \
    $TRAIN_DATA_ROOT \
    $DATA/$TRAIN_FILE \
    $DBOUTLOC/$TRAIN_DB_NAME
fi

if $CREATE_MEAN; then
	echo $MEAN_TOOLS/compute_image_mean -backend=$BACKEND $DBOUTLOC/$TRAIN_DB_NAME $DBOUTLOC/$MEAN_NAME.binaryproto
	$MEAN_TOOLS/compute_image_mean -backend=$BACKEND $DBOUTLOC/$TRAIN_DB_NAME $DBOUTLOC/$MEAN_NAME.binaryproto
fi

#echo "Creating val "$BACKEND"..."

#GLOG_logtostderr=1 $TOOLS/convert_imageset \
#    --resize_height=$RESIZE_HEIGHT \
#    --resize_width=$RESIZE_WIDTH \
#    --shuffle \
#    --backend="leveldb" \
#    $VAL_DATA_ROOT \
#    $DATA/test_view1_id.txt \
#    $EXAMPLE/lfw_view1_test_leveldb

echo "Done."
