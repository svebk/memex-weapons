import json

kcsv="keywords_statf.csv"
cat_map="cat_statf_mapping.json"
out_kjson="keywords_statf.jsonl"

# loading categories mapping
with open(cat_map,"rt") as cm:
  cm_json=json.load(cm)

# Initialize output dict of sets
out_k={}
for cat in cm_json.keys():
  out_k[cat]=set()

# Go other the stolen list of make,model,category,caliber and map these to the clean data
with open(kcsv) as kf:
  for line in kf:
    fields=line.split(',')
    clean_cat=cm_json(fields[2])
    if clean_cat:
      unknown_fields=[True for onefield in fields if onefield==["Z"]*len(onefield)]
      if unknown_fields.count(True)>0:
	continue
      if fields[1]:
	tup=(fields[0],fields[1],fields[3])
	if tup not in out_k[clean_cat]:
          print "Adding {} to cat {}.".format(tup,clean_cat)
          out_k[clean_cat].add((fields[0],fields[1],fields[3]))

# save results
with open(out_kjson,"wt") as okj:
  json.dumps(okj,out_k)
