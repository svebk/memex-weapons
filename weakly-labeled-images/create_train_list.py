import sys
import json
import time

#basepath="/srv/skaraman/weapons/"
#website="gunsamerica"

if __name__=="__main__":
  if len(sys.argv)!=4:
    print "[Usage] python create_train_list.py ads_cat_list.txt extr.jsonl out_train_file.txt"
    quit()

  ads_cat_list=sys.argv[1]
  extr_filename=sys.argv[2]
  out_filename=sys.argv[3]
  print ads_cat_list,extr_filename,out_filename

  # read cat list and store as dict
  ads_cats={}
  all_cats=[]
  with open(ads_cat_list,'rt') as acl:
    for line in acl:
        init_cat=line.index('[')
        rem_line=line[:init_cat]
        cat_raw=line[init_cat:]
        fields=rem_line.split(' ')
        #print fields,cat_raw
        cat = "Other"
        tmp_cat=[cc.strip() for cc in cat_raw.strip('[]\n').split('\'') if cc and cc!="','"]
        if len(tmp_cat)>1:
          print "We have an ambiguity: {}.".format(tmp_cat)
          continue
          # discarding this for now.
          if "Silencer" in tmp_cat:
            print "Using Silencer as category"
            cat = "Silencer"
          if "Handgun" in tmp_cat and "Machine Gun" in tmp_cat:
            print "Using Machine Gun as category"
            cat = "Machine Gun"
          if "Shotgun" in tmp_cat and "Machine Gun" in tmp_cat:
            print "Using Shotgun as category"
            cat = "Shotgun"
          if "Ammo" in tmp_cat and "Other" in tmp_cat:
            print "Using Ammo as category"
            cat = "Ammo"
        #time.sleep(1)
        elif tmp_cat:
          cat=tmp_cat[0]
        ads_cats[fields[0].strip()]=cat
        if cat not in all_cats:
          all_cats.append(cat)

  print len(all_cats),all_cats
  #print ads_cats
  time.sleep(1)

  extr_file=open(extr_filename,'rt')
  out_train=open(out_filename,'wt')
  #extr_file=open("{}{}/extr_{}_ads.jsonl".format(basepath,website,website),"r")
  for line in extr_file:
    one_extr=json.loads(line)
    extrk=one_extr.keys()[0].strip()
    # find corresponding clean category
    if extrk not in ads_cats:
    #print "No category match for {}. Skipping".format(extrk)
        continue
    cat=ads_cats[extrk]       
    # Beware, some price might be auctions prices (e.g. down to 0$...)
    price=one_extr[extrk]['landmark_extractions']['current_price']
    condition=[one_extr[extrk]['landmark_extractions']['details'][ii]['value'] for ii in range(len(one_extr[extrk]['landmark_extractions']['details'])) if one_extr[extrk]['landmark_extractions']['details'][ii]['label']=='Condition']
    brand=[one_extr[extrk]['landmark_extractions']['details'][ii]['value'] for ii in range(len(one_extr[extrk]['landmark_extractions']['details'])) if one_extr[extrk]['landmark_extractions']['details'][ii]['label']=='Brand']
    caliber=[one_extr[extrk]['landmark_extractions']['details'][ii]['value'] for ii in range(len(one_extr[extrk]['landmark_extractions']['details'])) if one_extr[extrk]['landmark_extractions']['details'][ii]['label']=='Caliber']
    imgs=[x for x in enumerate(one_extr[extrk]['original_doc']['outlinks'])\
         for img in one_extr[extrk]['landmark_extractions']['images'] if x[1].endswith(img)]
    imgs_paths=[one_extr[extrk]['original_doc']['outpaths'][pos[0]] for pos in imgs]
    # print images and label in train_files
    start_out=len("file:/data2/USCWeaponsStatsGathering/nutch/full_dump/")
    for img in imgs_paths:
      #print img[start_out:],cat,all_cats.index(cat)
      out_train.write("{} {}\n".format(img[start_out:],all_cats.index(cat)))
  out_train.close()
