import json

basepath="/srv/skaraman/weapons/"
website="gunsamerica"

f=open("{}{}/extr_{}_ads.jsonl","r")
fout=open("{}{}/extr_{}_ads_real.jsonl","w")
fulljson=json.load(f)
# fulljson is a list
for doc in range(len(fulljson)):
	old_doc=fulljson[doc]
	k=old_doc.keys()[0]
	new_doc={}
	new_doc[k]={}
	new_doc[k]['landmark_extractions']=old_doc[k]['extractions']
	for keepkey in ['raw_html', 'dlimagecat_url', 'original_doc']:
		new_doc[k][keepkey]=old_doc[k][keepkey]
	fout.write(json.dumps(new_doc))
fout.close()
