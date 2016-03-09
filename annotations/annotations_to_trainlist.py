import requests
import time
import shutil
import os.path

baseurl="https://memexdev.istresearch.com/annotate/weapons/img/"
out_dir="annotated_images_task1"

def getAnnotatedImage(image_id,out_dir,base_outfn):
  url=baseurl+str(image_id)
  outpath=os.path.join(out_dir,base_outfn)
  try:
    r = requests.get(url, stream=True)
    if r.status_code == 200:
      with open(outpath, 'wb') as f:
        r.raw.decode_content = True
        shutil.copyfileobj(r.raw, f)
        return True
  except Exception as inst:
    print "Download failed for img {} that should be saved at {} from url {}.".format(image_id,base_outfn,url)
    return False 

annotations_file="annotations_type_quoted.csv"
out_file="train_type_annotation.txt"
cats_out="cats_type_annotation.txt"

cats_list=[]
of = open(out_file,"wt")

with open(annotations_file,'rt') as af:
  for line in af:
    fields=line.split("\"")
    #print fields
    imageid=fields[1]
    #cdrid=fields[3]
    tmp_cat=fields[-2]
    #print imageid,cdrid,tmp_cat
    #time.sleep(1)
    imagename=imageid+".jpg"
    #if not getAnnotatedImage(imageid,out_dir,imagename):
    #  continue
    if tmp_cat not in cats_list:
      cats_list.append(tmp_cat)
    of.write("{} {}\n".format(imagename,cats_list.index(tmp_cat)))

with open(cats_out,"wt") as co:
  for tmp_ind,tmp_cat in enumerate(cats_list):
    co.write("{} {}\n".format(tmp_ind,tmp_cat))

co.close()
of.close()
