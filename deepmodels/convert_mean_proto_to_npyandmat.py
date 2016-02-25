import caffe
import numpy as np
import sys
import scipy.io as sio

if len(sys.argv) != 3:
	print "Usage: python convert_protomean.py proto.mean outbasename"
	sys.exit()

input_name = sys.argv[1]
output_name= sys.argv[2]
print "Reading",input_name
data = open(input_name, 'rb' ).read()
blob = caffe.proto.caffe_pb2.BlobProto()
blob.ParseFromString(data)
arr = np.array( caffe.io.blobproto_to_array(blob) )
out = arr[0]
print "Saving to",output_name
np.save(output_name, out)
sio.savemat(output_name, {'mean': out})
