# Cannot reproduce results from  feature_extract-memex.bin with this script for now...

import numpy as np
import matplotlib.pyplot as plt

# Make sure that caffe is on the python path:
#caffe_root = '../'  # this file is expected to be in {caffe_root}/examples
#import sys
#sys.path.insert(0, caffe_root + 'python')

import caffe
import cv2
import scipy

def show_res_batch(out,cat_lists,batch_in):
	prediction = out['prob']
	np_cat=np.asarray(cat_lists)
	for i in range(batch_in):
		print "Input #"+str(i)+" classified as:",np_cat[prediction[i].argmax()] 
		ind=np.argsort(prediction[i])[::-1]
		print "Top 10 classes are:",np_cat[ind[0:10]]	


def show_res(out,cat_lists,WITH_FLIP):
	prediction = out['prob']
	np_cat=np.asarray(cat_lists)
	if WITH_FLIP:
		ind=np.argsort(prediction)[:,::-1]
		print np_cat[ind[0][0:10]]
		print np_cat[ind[1][0:10]]
		print 'predicted class:', np_cat[prediction[0].argmax()], prediction[0].argmax()
		print 'predicted class:', np_cat[prediction[1].argmax()], prediction[1].argmax()	
	else:
		ind=np.argsort(prediction)[0,::-1]
		print np_cat[ind[0:10]]
		print 'predicted class:', np_cat[prediction.argmax()], prediction.argmax()	


# Set the right path to your model definition file, pretrained model weights,
# and the image you would like to classify.
MODEL_FILE_FLIP = './deepmodels/CNN_20K_deploy.prototxt'
MODEL_FILE = './deepmodels/CNN_20K_deploy_noflip.prototxt'
MODEL_FILE_BATCH32 = './deepmodels/CNN_20K_deploy_batch32.prototxt'
PRETRAINED = './deepmodels/CNN_20K.caffemodel'
MEAN_FILE = './deepmodels/imagenet_mean.npy'
CAT_FILE = './deepmodels/cat_20K.txt'
WITH_FLIP = True
WITH_CROP = False
IN_DIM=(224,224)

cat_lists=[]
with open(CAT_FILE,"rt") as fcat:
  for line in fcat:
    cat_lists.append(line)
print len(cat_lists)

IMAGE_FILE = '/media/04/MEMEX/memex-weapons/deepmodels/resized/04_Marlin_Modelo_1894.jpg'
caffe.set_mode_cpu()

if WITH_FLIP:
	net = caffe.Net(MODEL_FILE_FLIP, PRETRAINED, caffe.TEST)
else:
	net = caffe.Net(MODEL_FILE_BATCH32, PRETRAINED, caffe.TEST)

start=(256-224)/2
end=start+224

mean_img = np.load(MEAN_FILE)
input_image = cv2.imread(IMAGE_FILE)
input_image_t=np.transpose(input_image,(2,0,1))
if WITH_FLIP:
    input_image_fl = np.fliplr(input_image)
    input_image_fl_t=np.transpose(input_image,(2,0,1))
    if WITH_CROP:
        input_data = np.asarray([(input_image_t[:,start:end,start:end]-mean_img[:,start:end,start:end]),(input_image_fl_t[:,start:end,start:end]-mean_img[:,start:end,start:end])])
    else:
        input_image_tr=scipy.misc.imresize(input_image_t.transpose(1,2,0),IN_DIM).transpose(2,0,1)
	input_image_fl_tr=scipy.misc.imresize(input_image_fl_t.transpose(1,2,0),IN_DIM).transpose(2,0,1)
        input_data = np.asarray([(input_image_tr-mean_img[:,start:end,start:end]),(input_image_fl_tr-mean_img[:,start:end,start:end])])
else:
    if WITH_CROP:
        input_data = np.asarray([(input_image_t[:,start:end,start:end]-mean_img[:,start:end,start:end])])
    else:
        input_image_t=scipy.misc.imresize(input_image_t,IN_DIM)
        input_data = np.asarray([(input_image_t-mean_img[:,start:end,start:end])])

net.outputs
out = net.forward_all(data=input_data)
#show_res(out,cat_lists,WITH_FLIP)
show_res_batch(out,cat_lists,input_data.shape[0])


