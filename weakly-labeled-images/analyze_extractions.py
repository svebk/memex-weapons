import json
all_extr=json.load(open("guns_america_extractions2.json","r"))

all_images=[]
all_cats=[]
all_images_paths=[]
for i in range(len(all_extr)):
    extrk=all_extr[i].keys()[0]
    one_cat=all_extr[i][extrk]['extractions']['category']
    all_cats.append(one_cat)
    all_images.append([x for x in enumerate(all_extr[i][extrk]['original_doc']['outlinks'])\
         for img in all_extr[i][extrk]['extractions']['images'] if x[1].endswith(img)])
    all_images_paths.append([all_extr[i][extrk]['original_doc']['outpaths'][pos[0]] for pos in all_images[i]])

print "Non-empty category list count",len([one_cat for one_cat in all_cats if one_cat])

top_level_cat=[one_cat[0].split('>')[0] for one_cat in all_cats if len(one_cat)>0]
top_level_cat=[one_cat[0].split('>')[0].strip() for one_cat in all_cats if len(one_cat)>0]
print set(top_level_cat)
second_level_cat_guns=[one_cat[0].split('>')[1].strip() for one_cat in all_cats if len(one_cat)>0 and one_cat[0].split('>')[0].strip()=="Guns"]
second_level_cat_nonguns=[one_cat[0].split('>')[1].strip() for one_cat in all_cats if len(one_cat)>0 and one_cat[0].split('>')[0].strip()=="Non-Guns"]
third_level_cat_nonguns=[one_cat[0].split('>')[2].strip() for one_cat in all_cats if len(one_cat)>0 and one_cat[0].split('>')[0].strip()=="Non-Guns"\
   and one_cat[0].split('>')[1].strip()=="Gun Parts"]
