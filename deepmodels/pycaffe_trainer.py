import numpy as np
import json
import cv2
import scipy
# Make sure that caffe is on the python path:
#caffe_root = '../'  # this file is expected to be in {caffe_root}/examples
#import sys
#sys.path.insert(0, caffe_root + 'python')
import caffe

class CaffeTrainerConf():
    INPUT_MODEL_FILE = './deepmodels/CNN_20K_deploy.prototxt'
    TRAIN_MODEL_FILE = './deepmodels/CNN_20K_train_ukhack_newproto.prototxt'
    PRETRAINED = './deepmodels/CNN_20K.caffemodel'
    OUT_TRAINED = './deepmodels/CNN_20K_train_ukhack_newproto.caffemodel'
    SOLVER_FILE = './deepmodels/CNN_20K_solver_ukhack.txt'
    MEAN_FILE = './deepmodels/imagenet_mean.npy'
    CAT_FILE = './deepmodels/cat_20K.txt'
    WEAPONS_CAT_FILE = './deepmodels/weapon_classes.npy'
    WEAPONS_MAPPING_FILE = './deepmodels/imagenet_memex_mapping.json'
    WITH_FLIP = True
    WITH_CROP = False
    OUTPUT_LAYERS=['prob']
    CAFFE_MODE = "CPU"

class CaffeTrainer():
    conf = None  
    net = None  
    mean_img = None

    def __init__(self, in_conf=CaffeTrainerConf()):
        self.conf = in_conf
        self.initialize()

    def initialize(self):
        # Caffe net init
        if self.conf.CAFFE_MODE == "GPU":
            caffe.set_mode_gpu()
        else:
            caffe.set_mode_cpu()
        self.mean_img = np.load(self.conf.MEAN_FILE)
        self.input_net = caffe.Net(self.conf.INPUT_MODEL_FILE, self.conf.PRETRAINED, caffe.TEST)
        # This will already load weights from layers with matching names
        self.net = caffe.Net(self.conf.TRAIN_MODEL_FILE, self.conf.PRETRAINED, caffe.TRAIN)
        # Manually copy layers with different names here...
        fc7key=[key for key in self.net.keys() if key.startswith('fc7')]
        self.net[fc7key[0]].data=self.input_net['fc7'].data
        # initialize last parameters
        self.conf.batch_size = self.net.blobs['data'].data.shape[0]
        self.conf.IN_DIM = (self.net.blobs['data'].data.shape[2],self.net.blobs['data'].data.shape[3])
        # initialize solver
        self.solver = caffe.SGDSolver(self.conf.SOLVER_FILE)

    def formatInput(self,IMAGE_FILE):
        start=(256-224)/2
        end=start+224
        input_image = cv2.imread(IMAGE_FILE)
        if input_image is None:
            return None
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

    def fillInput(self,trainingFilesList):
        self.input_data = []
        for oneImg in trainingFilesList:
            input_image = self.formatInput(IMAGE_FILE)
            if input_image is None:
                return None
            self.input_data.append(input_image)
        # How to deal with labels?
        return self.input_data

    def train(self):
        pass

if __name__ == "__main__":
    # TODO get parameters from argsparse
    ce = CaffeTrainer()
    # TODO
    # Get a list of images and corresponding labels
    trainingFilesList = None
    # get images from json files:
    # - label files are key-category 
    # - data files are 
    # Use Net.set_input_arrays to train with MemoryData layer
    ce.fillInput(trainingFilesList)
    ce.train()
