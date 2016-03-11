import sys
import json
import time
import os
import requests
import shutil
from Queue import *
from threading import Thread

#basepath="/srv/skaraman/weapons/"
#website="gunsamerica"

imagecat=json.load(open('imagecat_conf.json','rt'))
nb_threads=16

def mkpath(outpath):
  pos_slash=[pos for pos,c in enumerate(outpath) if c=="/"]
  for pos in pos_slash:
    try:
      os.mkdir(outpath[:pos])
    except:
      pass

def copyFromDump(image_id,out_dir,base_outfn):
  try:
    dump_dir="/srv/skaraman/weapons/JPL_WeaponsImages/image_dump/"
    outpath=os.path.join(out_dir,base_outfn)
    mkpath(outpath)
    shutil.copyfile(dump_dir+image_id, outpath)
    return True
  except Exception as inst:
    print inst
    return False

def getImageFromImagecat(image_id,out_dir,base_outfn):
  url=imagecat['imagecat_host']+"/weapons/alldata/"+str(image_id)
  outpath=os.path.join(out_dir,base_outfn)
  mkpath(outpath)
  try:
    r = requests.get(url, stream=True, auth=(imagecat['user'], imagecat['passwd']), timeout=5)
    if r.status_code == 200:
      with open(outpath, 'wb') as f:
        r.raw.decode_content = True
        shutil.copyfileobj(r.raw, f)
        return True
  except Exception as inst:
    print "Download failed for img {} that should be saved at {} from url {}.".format(image_id,base_outfn,url)
    print inst 
    return False

def getImageFromOriginalURL(url,out_dir,base_outfn):
  outpath=os.path.join(out_dir,base_outfn)
  mkpath(outpath)
  try:
    r = requests.get(url, stream=True, timeout=5)
    if r.status_code == 200:
      with open(outpath, 'wb') as f:
        r.raw.decode_content = True
        shutil.copyfileobj(r.raw, f)
        return True
  except Exception as inst:
    print "Download failed for img that should be saved at {} from url {}.".format(base_outfn,url)
    print inst
    return False

def getImg(img,out_dir):
  start_out=len("file:/data2/USCWeaponsStatsGathering/nutch/full_dump/")
  if not os.path.isfile(os.path.join(out_dir,img[0][start_out:])): 
    if not copyFromDump(img[0][start_out:],out_dir,img[0][start_out:]):
      if not getImageFromImagecat(img[0][start_out:],out_dir,img[0][start_out:]):
        if not getImageFromOriginalURL(img[1],out_dir,img[0][start_out:]):
          return False
  return True


def worker():
        while True:
                tupInp = q.get()
                getImg(tupInp[0], tupInp[1])
                q.task_done()

q= Queue()
for i in range(nb_threads):
        t=Thread(target=worker)
        t.daemon=True
        t.start()



if __name__=="__main__":
  if len(sys.argv)!=4:
    print "[Usage] python create_train_list.py ads_cat_list.jsonl extr.jsonl out_dir"
    quit()

  ads_cat_list=sys.argv[1]
  extr_filename=sys.argv[2]
  out_dir=sys.argv[3]
  print ads_cat_list,extr_filename,out_dir

  ads_cats={}
  with open(ads_cat_list,'rt') as acl:
    for line in acl:
      jl=json.loads(line)
      key=jl.keys()[0]
      cat = "Other"
      #print jl[key]
      tmp_cat=jl[key].strip()
      #time.sleep(1)
      if tmp_cat:
        cat=tmp_cat
      ads_cats[key]=cat

  extr_file=open(extr_filename,'rt')
  start_armslist="http://cdn2.armslist.com/sites/armslist/uploads"

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
    #price=one_extr[extrk]['landmark_extractions']['current_price']
    #condition=[one_extr[extrk]['landmark_extractions']['details'][ii]['value'] for ii in range(len(one_extr[extrk]['landmark_extractions']['details'])) if one_extr[extrk]['landmark_extractions']['details'][ii]['label']=='Condition']
    #brand=[one_extr[extrk]['landmark_extractions']['details'][ii]['value'] for ii in range(len(one_extr[extrk]['landmark_extractions']['details'])) if one_extr[extrk]['landmark_extractions']['details'][ii]['label']=='Brand']
    #caliber=[one_extr[extrk]['landmark_extractions']['details'][ii]['value'] for ii in range(len(one_extr[extrk]['landmark_extractions']['details'])) if one_extr[extrk]['landmark_extractions']['details'][ii]['label']=='Caliber']
    imgs=[x for x in enumerate(one_extr[extrk]['original_doc']['outlinks'])\
         for img in one_extr[extrk]['landmark_extractions']['images'] if img['src'].startswith(start_armslist) and x[1].endswith(img['src'])]
    imgs_paths=[(one_extr[extrk]['original_doc']['outpaths'][pos[0]],pos[1]) for pos in imgs]
    for img in imgs_paths:
      q.put((img,out_dir))
  q.join()
