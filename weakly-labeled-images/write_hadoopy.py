import hadoopy
import pickle
import json
import sys

print "Loading pickle file..."
sys.stdout.flush()
data=pickle.load(open('guns_america.pickle','rb'))
print "Done."
sys.stdout.flush()

print "Writing readme...",
sys.stdout.flush()
hadoopy.writetb('/data/weapons/gunsamerica/README.txt', [('README','author: svebor karaman\nsvebor.karaman@columbia.edu\n\n\
	This folder contains ads crawled by JPL from the gunsamerica.com website. \
	The goal is to use this data to train image classifiers using automatic extractions\
	as labels.\n\n\
	The file is composed of key value pairs where the key is a string like \'com/gunsamerica/www/C378FA4FB824B323B706222F826938AE660D7A1E322F501441F203BCB01239F5\' \
	extracted from the JPL imagecat id (discarding the first part \'file:/data2/USCWeaponsStatsGathering/nutch/full_dump/\') \
	and the value is a JSON with fields \'raw_html\',  \'dlimagecat_url\' and \'original_doc\'.')])
print "Done."
sys.stdout.flush()

print "Start writing whole seq file."
sys.stdout.flush()
hadoopy.writetb('/data/weapons/gunsamerica/gunsamerica.seq', [(key,json.dumps(data[key])) for key in data.keys()])
print "Done writing seq file."
sys.stdout.flush()
