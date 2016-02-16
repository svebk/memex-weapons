import json
import pickle

ga_data=pickle.load(open('guns_america.pickle','rb'))
with open('guns_america.json','wt') as f: 
  for key in ga_data.keys():
    print "Saving doc",key
    f.write('{'+key+','+json.dumps(ga_data[key])+'}\n')
