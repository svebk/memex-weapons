import urllib2
import json
import pickle
import time

imagecat_conf=json.load(open("imagecat_conf.json"))
user=imagecat_conf["user"]
passwd=imagecat_conf["passwd"]
imagecat_host=imagecat_conf["imagecat_host"]
nb_rows=100
step=nb_rows
#base_query=imagecat_host+'/solr/imagecatdev/query?q=id:/.*com%5C/gunsamerica.*/&fq=-mainType:image&facet=true&facet.field=contentType&rows='+str(nb_rows)+'&start='
base_query=imagecat_host+'/solr/imagecatdev/query?q=id:/.*com%5C/gunsamerica.*/&fq=url:/.*%5B0-9%5D%7B9,15%7D.*/&fq=mainType:(application%20text)&fq=subType:/.*ml.*/&fq=url:*&fl=url,id,contentType,outpaths,outlinks,ner_weapon_name_t_md,ner_weapon_type_ts_md,resourcename_t_md&rows='+str(nb_rows)+'&start='
file_prefix='file:/data2/USCWeaponsStatsGathering/nutch/full_dump/'
prefend=len(file_prefix)
imagecat_dataPref='http://imagecat.dyndns.org/weapons/alldata/'
out_jsonl="gunsamerica_ads.jsonl"

## deprecated. doing that in query now
## used to filter in loop with this.
#if 'mainType' in doc.keys() and doc['mainType'] in mainTypeFilters and 'subType' in doc.keys() and doc['subType'] in subTypeFilters:
#mainTypeFilters=['application','text']
#subTypeFilters=['xhtml+xml','html']

#if url is ending in .jpg, or starting with https://www.gunsamerica.com/WebResource.axd?
#the webpage may be a page not found webpage...
urlInvalidStart=['https://www.gunsamerica.com/WebResource.axd']
urlInvalidEnd=['.jpg']

def initUrlLib(imagecat_host,user,passwd):
	p = urllib2.HTTPPasswordMgrWithDefaultRealm()
	p.add_password(None, imagecat_host, user, passwd)
	handler = urllib2.HTTPBasicAuthHandler(p)
	opener = urllib2.build_opener(handler)
	urllib2.install_opener(opener)

initUrlLib(imagecat_host,user,passwd)


start = 0
resp = urllib2.urlopen(base_query+str(start))
json_resp=json.load(resp)
total_docs = int(json_resp['response']['numFound'])
print "We have a total of "+str(total_docs)+" docs to process."

start_time=time.time()
valid_docs=0

while start<total_docs:
	batch_start_time=time.time()
	resp = urllib2.urlopen(base_query+str(start))
	json_resp=json.load(resp)
	print "We have a batch of "+str(len(json_resp['response']['docs']))+" docs."

	for doc_id in range(len(json_resp['response']['docs'])):
		doc=json_resp['response']['docs'][doc_id]
		invalidStart=[not doc['url'].startswith(oneInvalidStart) for oneInvalidStart in urlInvalidStart]
		invalidEnd=[not doc['url'].endswith(oneInvalidEnd) for oneInvalidEnd in urlInvalidEnd]
		#print invalidStart,invalidEnd
		if invalidStart.count(True)+invalidEnd.count(True)==len(urlInvalidStart)+len(urlInvalidEnd):
			one_doc={}
			one_doc[doc['id'][prefend:]]={}
			file_path=imagecat_dataPref+doc['id'][prefend:]
			print doc['url']
			one_doc[doc['id'][prefend:]]['original_doc']=doc
			one_doc[doc['id'][prefend:]]['dlimagecat_url']=file_path
			print "Should download from",file_path
			resp_html = urllib2.urlopen(file_path)
			one_doc[doc['id'][prefend:]]['raw_html']=resp_html.read()
			print "Downloaded page from",file_path
			with open(out_jsonl,"at") as f:
				f.write(json.dumps(one_doc))
				f.write("\n") # Needed?
			valid_docs=valid_docs+1
		else:
			print 'Ignoring doc',json_resp['response']['docs'][doc_id]['id']
			#print doc['url']
	print "Processed batch in",str(time.time()-batch_start_time)
	start=start+step
	
print "Processed all docs in",str(time.time()-start_time)
