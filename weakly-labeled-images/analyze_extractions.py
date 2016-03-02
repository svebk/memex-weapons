import json
import re
all_extr=json.load(open("guns_america_extractions2.json","r"))

all_infos=[]
for i in range(len(all_extr)):
    extrk=all_extr[i].keys()[0]
    one_cat=all_extr[i][extrk]['extractions']['category']
    title=all_extr[i][extrk]['extractions']['title']
    # Beware, some price might be auctions prices (e.g. down to 0$...)
    price=all_extr[i][extrk]['extractions']['current_price']
    condition=[all_extr[i][extrk]['extractions']['details'][ii]['value'] for ii in range(len(all_extr[i][extrk]['extractions']['details'])) if all_extr[i][extrk]['extractions']['details'][ii]['label']=='Condition']
    brand=[all_extr[i][extrk]['extractions']['details'][ii]['value'] for ii in range(len(all_extr[i][extrk]['extractions']['details'])) if all_extr[i][extrk]['extractions']['details'][ii]['label']=='Brand']
    caliber=[all_extr[i][extrk]['extractions']['details'][ii]['value'] for ii in range(len(all_extr[i][extrk]['extractions']['details'])) if all_extr[i][extrk]['extractions']['details'][ii]['label']=='Caliber']
    imgs=[x for x in enumerate(all_extr[i][extrk]['original_doc']['outlinks'])\
         for img in all_extr[i][extrk]['extractions']['images'] if x[1].endswith(img)]
    imgs_paths=[all_extr[i][extrk]['original_doc']['outpaths'][pos[0]] for pos in all_images[i]]
    all_infos.append((extrk,one_cat,imgs,imgs_paths,title,price,condition,brand,caliber))

inc_kw=json.load(open("svebor_included_keywords.json","r"))
gunsamerica_cat_exc=json.load(open("gunsamerica_categories_exclusion.json","r"))
gunsamerica_cat_inc=json.load(open("gunsamerica_categories_inclusion.json","r"))

all_infos_shotgun=[x for x in all_infos for cat_ok in gunsamerica_cat_inc['Shotgun']  if len(x[1])>0 and x[1][0].startswith(cat_ok)]
all_infos_rifle_init=[x for x in all_infos for cat_ok in gunsamerica_cat_inc['Rifle']  if len(x[1])>0 and x[1][0].startswith(cat_ok)]
all_infos_handgun=[x for x in all_infos for cat_ok in gunsamerica_cat_inc['Handgun'] if len(x[1])>0 and x[1][0].startswith(cat_ok)]
all_infos_ammo=[x for x in all_infos for cat_ok in gunsamerica_cat_inc['Ammo'] if len(x[1])>0 and x[1][0].startswith(cat_ok)]
# Machine guns seem to be listed within the Rifles category.
all_infos_machine_gun=[x for x in all_infos for kw in inc_kw['Machine Gun'] if len(x[1])>0 and x[1][0].startswith("Guns > Rifles") and kw.lower() in x[4].lower()]
# exclude machine guns from rifles
# Why is len(all_infos_rifle_init)-len(all_infos_machine_gun) != len(all_infos_rifle)
all_infos_rifle=[item for item in all_infos_rifle_init if item not in all_infos_machine_gun]
#Silencer
all_infos_silencer=[x for x in all_infos for kw in inc_kw['Silencer'] if len(x[1])>0 and kw.lower() in x[4].lower()]
# Conversion Devices/Parts
all_infos_conversion=[x for x in all_infos for kw in inc_kw['Conversion Devices/Parts'] if len(x[1])>0 and kw.lower() in x[4].lower()]
# Frame receiver?
# beware that some ads may be kits WITHOUT frame...
all_infos_frame=[x for x in all_infos for kw in inc_kw['Frame / Lower Receiver'] if len(x[1])>0 and kw.lower() in x[4].lower() and [exc_cat.lower() not in x[1][0].lower() for exc_cat in gunsamerica_cat_exc['Frame / Lower Receiver']].count(True)==len(gunsamerica_cat_exc['Frame / Lower Receiver'])]
# Explosive Ordnance?
all_infos_explosive=[x for x in all_infos for kw in inc_kw['Explosive Ordnance'] if len(x[1])>0 and kw.lower() in x[4].lower() and [exc_cat.lower() not in x[1][0].lower() for exc_cat in gunsamerica_cat_exc['Explosive Ordnance']].count(True)==len(gunsamerica_cat_exc['Explosive Ordnance'])]
