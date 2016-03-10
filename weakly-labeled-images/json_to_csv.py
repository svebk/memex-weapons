import json


json_fn="task2.json"
out_fn="task2.csv"

of=open(out_fn,"wt")

with open(json_fn,"rt") as jf:
  json_dict=json.load(jf)
  for key in json_dict:
    for val in json_dict[key]:
      print "\"{}\",\"{}\"".format(key,val)
      of.write("\"{}\",\"{}\"\n".format(key,val))
of.close()
      
