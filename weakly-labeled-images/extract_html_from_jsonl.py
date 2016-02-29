import json

filename="slickguns_ads_first10.jsonl"
output_base="slickguns_html"

i=0
with open(filename,"rt") as f:
   for line in f:
	tmpdoc=json.loads(line)
	i=i+1
	k=tmpdoc.keys()[0]
	with open(output_base+"_"+k.split('/')[-1]+"_"+str(i)+".html","wt") as h:
		h.write(tmpdoc[k]['raw_html'].encode('utf8'))
