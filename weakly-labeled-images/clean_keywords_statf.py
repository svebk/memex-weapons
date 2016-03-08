import json

kcsv="keywords_statf.csv"
mmcsv="maker_mapping_quoted.csv"
cat_map="cat_statf_mapping.json"
out_kjson="keywords_statf.jsonl"

# loading categories mapping
with open(cat_map,"rt") as cm:
  cm_json=json.load(cm)

# Initialize output dict of sets
out_k={}
for cat in cm_json:
  #print cm_json[cat]
  out_k[cm_json[cat]]=set()

mmd={}
# Initialize maker mapping
with open(mmcsv) as mmf:
  for line in mmf:
    fields=line.split('","')
    print len(fields),fields
    mmd[fields[0].strip("\" ")]=(fields[1].strip("\" "),fields[2].strip("\" \n"))

# Go other the stolen list of make,model,category,caliber and map these to the clean data
with open(kcsv) as kf:
  for line in kf:
    fields=line.split(',')
    try:
      clean_cat=cm_json[fields[2]]
    except:
      continue
    if clean_cat:
      unknown_fields=[True for onefield in fields if onefield.strip()==''.join(["Z"]*len(onefield.strip()))]
      #print fields[0].strip(),''.join(["Z"]*len(onefield.strip())),unknown_fields
      if unknown_fields.count(True)>0:
        continue
      if fields[1]:
        tup=(fields[0].strip(),mmd[fields[0].strip()][0],fields[1].strip(),fields[3].strip(),mmd[fields[0].strip()][1])
        if tup not in out_k[clean_cat]:
          print "Adding {} to cat {}.".format(tup,clean_cat)
          out_k[clean_cat].add(tup)

# set to list because JSON does not know how to serialize sets
for key in out_k:
  out_k[key]=list(out_k[key])
  print out_k[key]

# save results
with open(out_kjson,"wt") as okj:
  for key in out_k:
    okj.write(json.dumps({key:out_k[key]}))
    okj.write("\n") 
okj.close()

