import json
all_extr=json.load(open("guns_america_extractions2.json","r"))

# all_images=[]
# all_cats=[]
# all_images_paths=[]
# for i in range(len(all_extr)):
#     extrk=all_extr[i].keys()[0]
#     one_cat=all_extr[i][extrk]['extractions']['category']
#     all_cats.append(one_cat)
#     all_images.append([x for x in enumerate(all_extr[i][extrk]['original_doc']['outlinks'])\
#          for img in all_extr[i][extrk]['extractions']['images'] if x[1].endswith(img)])
#     all_images_paths.append([all_extr[i][extrk]['original_doc']['outpaths'][pos[0]] for pos in all_images[i]])

# print "Non-empty category list count",len([one_cat for one_cat in all_cats if one_cat])

# top_level_cat=[one_cat[0].split('>')[0] for one_cat in all_cats if len(one_cat)>0]
# top_level_cat=[one_cat[0].split('>')[0].strip() for one_cat in all_cats if len(one_cat)>0]
# print set(top_level_cat)
# second_level_cat_guns=[one_cat[0].split('>')[1].strip() for one_cat in all_cats if len(one_cat)>0 and one_cat[0].split('>')[0].strip()=="Guns"]
# second_level_cat_nonguns=[one_cat[0].split('>')[1].strip() for one_cat in all_cats if len(one_cat)>0 and one_cat[0].split('>')[0].strip()=="Non-Guns"]
# gun_parts=[one_cat[0].split('>')[2].strip() for one_cat in all_cats if len(one_cat)>0 and one_cat[0].split('>')[0].strip()=="Non-Guns"\
#    and one_cat[0].split('>')[1].strip()=="Gun Parts"]
# misc_gunsparts=[one_cat[0].split('>')[3].strip() for one_cat in all_cats if len(one_cat)>0 and one_cat[0].split('>')[0].strip()=="Non-Guns"\
#    and one_cat[0].split('>')[1].strip()=="Gun Parts" and one_cat[0].split('>')[2].strip()=="Misc"]
# # u'Pistols', u'Rifles', u'Shotguns
# # Need to look at the title to get what the parts are...


all_infos=[]
for i in range(len(all_extr)):
    extrk=all_extr[i].keys()[0]
    one_cat=all_extr[i][extrk]['extractions']['category']
    title=all_extr[i][extrk]['extractions']['title']
    price=all_extr[i][extrk]['extractions']['current_price']
    condition=[all_extr[i][extrk]['extractions']['details'][ii]['value'] for ii in range(len(all_extr[i][extrk]['extractions']['details'])) if all_extr[i][extrk]['extractions']['details'][ii]['label']=='Condition']
    brand=[all_extr[i][extrk]['extractions']['details'][ii]['value'] for ii in range(len(all_extr[i][extrk]['extractions']['details'])) if all_extr[i][extrk]['extractions']['details'][ii]['label']=='Brand']
    caliber=[all_extr[i][extrk]['extractions']['details'][ii]['value'] for ii in range(len(all_extr[i][extrk]['extractions']['details'])) if all_extr[i][extrk]['extractions']['details'][ii]['label']=='Caliber']
    imgs=[x for x in enumerate(all_extr[i][extrk]['original_doc']['outlinks'])\
         for img in all_extr[i][extrk]['extractions']['images'] if x[1].endswith(img)]
    imgs_paths=[all_extr[i][extrk]['original_doc']['outpaths'][pos[0]] for pos in all_images[i]]
    all_infos.append((extrk,one_cat,imgs,imgs_paths,title,price,condition,brand,caliber))

all_infos_shotguns=[x for x in all_infos if len(x[1])>0 and x[1][0].startswith("Guns > Shotguns")]
all_infos_rifles=[x for x in all_infos if len(x[1])>0 and x[1][0].startswith("Guns > Rifles")]
all_infos_pistols=[x for x in all_infos if len(x[1])>0 and x[1][0].startswith("Guns > Pistols")]

#TODO, analyze titles, brands, caliber, conditions.
# Machine guns seem to be listed within the Rifles category.

atf_kw=json.load(open("atf_keywords.json","r"))