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

class CaffeExtractorConf():
    MODEL_FILE = './deepmodels/CNN_20K_deploy.prototxt'
    PRETRAINED = './deepmodels/CNN_20K.caffemodel'
    MEAN_FILE = './deepmodels/imagenet_mean.npy'
    CAT_FILE = './deepmodels/cat_20K.txt'
    WEAPONS_CAT_FILE = './deepmodels/weapon_classes.npy'
    WEAPONS_MAPPING_FILE = './deepmodels/imagenet_memex_mapping.json'
    WITH_FLIP = True
    WITH_CROP = False
    OUTPUT_LAYERS=['prob']
    CAFFE_MODE = "CPU"

class CaffeExtractor():
    conf = None  
    net = None  
    mean_img = None

    def __init__(self, in_conf=CaffeExtractorConf()):
	self.conf = in_conf
	self.initialize()

    def initialize(self):
        if self.conf.CAFFE_MODE == "GPU":
              caffe.set_mode_gpu()
        else:
	      caffe.set_mode_cpu()
	self.net = caffe.Net(self.conf.MODEL_FILE, self.conf.PRETRAINED, caffe.TEST)
	self.mean_img = np.load(self.conf.MEAN_FILE)
	self.np_cat = self.loadCatList(self.conf.CAT_FILE)
	self.conf.batch_size = self.net.blobs['data'].data.shape[0]
	self.conf.IN_DIM = (self.net.blobs['data'].data.shape[2],self.net.blobs['data'].data.shape[3])
	self.wf=np.where(np.load(self.conf.WEAPONS_CAT_FILE)==1)[0]
    sefl.mapCatList()

    def formatInput(self,IMAGE_FILE):
	start=(256-224)/2
	end=start+224
        input_image = cv2.imread(IMAGE_FILE)
        input_image_t=np.transpose(input_image,(2,0,1))
        if self.conf.WITH_FLIP:
            input_image_fl = np.fliplr(input_image)
            input_image_fl_t=np.transpose(input_image,(2,0,1))
            if self.conf.WITH_CROP:
                input_data = np.asarray([(input_image_t[:,start:end,start:end]-self.mean_img[:,start:end,start:end]),(input_image_fl_t[:,start:end,start:end]-self.mean_img[:,start:end,start:end])])
            else:
                input_image_tr=scipy.misc.imresize(input_image_t.transpose(1,2,0),self.conf.IN_DIM).transpose(2,0,1)
        	input_image_fl_tr=scipy.misc.imresize(input_image_fl_t.transpose(1,2,0),self.conf.IN_DIM).transpose(2,0,1)
                input_data = np.asarray([(input_image_tr-self.mean_img[:,start:end,start:end]),(input_image_fl_tr-self.mean_img[:,start:end,start:end])])
        else:
            if self.conf.WITH_CROP:
                input_data = np.asarray([(input_image_t[:,start:end,start:end]-self.mean_img[:,start:end,start:end])])
            else:
                input_image_t=scipy.misc.imresize(input_image_t.transpose(1,2,0),self.conf.IN_DIM).transpose(2,0,1)
                input_data = np.asarray([(input_image_t-self.mean_img[:,start:end,start:end])])
	return input_data

    def getOutput(self,IMAGE_FILE):
	self.input_data = None
        self.input_data = self.formatInput(IMAGE_FILE)
	self.net.forward(data=self.input_data)
	self.out = {}
	for layer in self.conf.OUTPUT_LAYERS:
		self.out[layer]=self.net.blobs[layer].data
	return self.out

    @staticmethod
    def loadCatList(CAT_FILE):
        cat_lists=[]
        with open(CAT_FILE,"rt") as fcat:
            for line in fcat:
                cat_lists.append(line)
	print "We have",str(len(cat_lists)),"classes in total."
	return np.asarray(cat_lists)

    def mapCatList(self):
        with open(self.conf.WEAPONS_MAPPING_FILE,"r") as f:
            json_map=json.load(f)
            self.map_cat_lists=json_map.keys()
            self.all_mapped_cat=[]
            self.map_cat_pos={}
            for key in self.map_cat_lists:
                self.map_cat_pos[key]=[]
                for cat in self.map_cat_lists[key]:
                    self.map_cat_pos[key].extend(np.where(self.np_cat==cat))
                    self.all_mapped_cat.extend(np.where(self.np_cat==cat))

    def show_res_batch(self):     
	batch_in = self.input_data.shape[0]
	prediction = self.out['prob']
        for i in range(batch_in):
            print "Input #"+str(i)+" classified as:",self.np_cat[prediction[i].argmax()] 
            ind=np.argsort(prediction[i])[::-1]
            print "Top 10 classes are:",self.np_cat[ind[0:10]]	
	    mlw=self.wf[np.argmax(prediction[i][self.wf])]
	    print "Most likely weapon is:",self.np_cat[mlw].strip()



ce = CaffeExtractor()
IMAGE_FILE = './deepmodels/04_Marlin_Modelo_1894.jpg'
out = ce.getOutput(IMAGE_FILE)
ce.show_res_batch()


