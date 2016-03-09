import sys
import json
import time
import os
import shutil

valid_extensions=['jpg','jpeg','png']

def mkpath(outpath):
  pos_slash=[pos for pos,c in enumerate(outpath) if c=="/"]
  for pos in pos_slash:
    try:
      os.mkdir(outpath[:pos])
    except:
      pass

if __name__=="__main__":
  if len(sys.argv)!=6:
    print "[Usage] python create_train_list_CMU.py CMU_images_dir cmu_cat_map.jsonl out_train_file.txt out_cats_list_map.txt out_dir"
    quit()

  CMU_images_dir=sys.argv[1]
  cmu_cat_map_filename=sys.argv[2]
  out_filename=sys.argv[3]
  out_castlist_filename=sys.argv[4]
  out_dir=sys.argv[5]
  print CMU_images_dir,cmu_cat_map_filename,out_filename,out_castlist_filename,out_dir

  cmu_cat_map=json.load(open(cmu_cat_map_filename,"rt"))

  # read cat map json and store as list
  all_cats=[]
  for key in cmu_cat_map.keys():
      cat=key.strip()
      if cat not in all_cats:
        all_cats.append(cat)

  print len(all_cats),all_cats
  with open(out_castlist_filename,"wt") as ocl:
    for i,cat in enumerate(all_cats):
      ocl.write("{} \"{}\"\n".format(i,cat))
  ocl.close()
  time.sleep(1)

  # list all images in each cateogry directory 
  out_train=open(out_filename,'wt')
  img_count=0
  for key in cmu_cat_map.keys():
    tmp_out_dir=os.path.join(out_dir,key)
    mkpath(tmp_out_dir)
    for directory in cmu_cat_map[key]:
      list_image = os.listdir(os.path.join(CMU_images_dir,directory))
      for img in list_image:
        # check image is of a valid extension
        check=[img.endswith(ext) for ext in valid_extensions]
        if check.count(True)>0:
          # we have a valid image
          ext_img=[pos for pos,ext in enumerate(valid_extensions) if img.endswith(ext)]
          out_img_name=str(img_count)+"."+valid_extensions[ext_img[0]]
          print out_img_name
          out_img_fullpath=os.path.join(tmp_out_dir,out_img_name)
          print out_img_fullpath
          out_img_shortpath=os.path.join(key,out_img_name)
          print out_img_shortpath
          time.sleep(2)
          shutil.copyfile(os.path.join(CMU_images_dir,directory,img), out_img_fullpath)
          out_train.write("{} {}\n".format(out_img_shortpath,all_cats.index(key.strip())))
          img_count=img_count+1
  out_train.close()
