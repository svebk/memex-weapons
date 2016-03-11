import sys
import json
import time
import os
import requests
import shutil
import pickle
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
    print "[Usage] python parallel_dl_task2.py base_ads_cat base_extr out_dir"
    quit()

  # to be called with something like
  # python parallel_dl_task2.py ./task2/ ../../  ../../data/task2_train &> logDlTask2.txt


  websites=["gunsamerica", "armslist", "slickguns"]
  start={}
  start["armslist"]="http://cdn2.armslist.com/sites/armslist/uploads"
  start["slickguns"]="http://cdn2.armslist.com/sites/armslist/uploads"

  ads_cat_list_base=sys.argv[1]
  extr_filename_base=sys.argv[2]
  out_dir=sys.argv[3]

  ads_cats={}
  all_cats_count={}
  for web in websites:
    print "Getting image for website {}.".format(web)
    ads_cat_list=os.path.join(ads_cat_list_base,web+"2.jl")
    extr_filename=os.path.join(extr_filename_base,web,"extr_"+web+"_ads.jsonl")
    print ads_cat_list,extr_filename,out_dir

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
        if key not in all_cats_count:
          all_cats_count[key]=0
        else:
          all_cats_count[key]=all_cats_count[key]+1

    extr_file=open(extr_filename,'rt')

    #extr_file=open("{}{}/extr_{}_ads.jsonl".format(basepath,website,website),"r")
    for line in extr_file:
      one_extr=json.loads(line)
      extrk=one_extr.keys()[0].strip()
      # find corresponding clean category
      if extrk not in ads_cats:
        #print "No category match for {}. Skipping".format(extrk)
        continue
      cat=ads_cats[extrk]       
      if web == "gunsamerica":
        #gunsamerica
        imgs=[x for x in enumerate(one_extr[extrk]['original_doc']['outlinks'])\
             for img in one_extr[extrk]['landmark_extractions']['images'] if x[1].endswith(img)]
      elif web == "slickguns":
        #slickguns
        imgs=[x for x in enumerate(one_extr[extrk]['original_doc']['outlinks'])\
             for img in one_extr[extrk]['landmark_extractions']['images'] if img.startswith(start_slickguns) and x[1].endswith(img)]
        fimg = one_extr[extrk]['landmark_extractions']['featured_image']
        featured_img=[x for x in enumerate(one_extr[extrk]['original_doc']['outlinks']) if fimg.startswith(start_slickguns) and x[1].endswith(fimg)]
        imgs.extend(featured_img)
      elif web == "armslist":
        #armslist
        imgs=[x for x in enumerate(one_extr[extrk]['original_doc']['outlinks'])\
             for img in one_extr[extrk]['landmark_extractions']['images'] if img['src'].startswith(start_armslist) and x[1].endswith(img['src'])]
      imgs_paths=[(one_extr[extrk]['original_doc']['outpaths'][pos[0]],pos[1]) for pos in imgs]
      for img in imgs_paths:
        q.put((img,out_dir))
  print all_cats_count
  pickle.dump(all_cats,open("all_cats_task2.pickle","wb"))
  q.join()
