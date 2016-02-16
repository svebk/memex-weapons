import hadoopy
import json
import sys

print "Writing dummy file...",
sys.stdout.flush()
hadoopy.writetb('/data/weapons/gunsamerica/dummy.txt', [('dummy_key','dummy value.')])
print "Done."
sys.stdout.flush()
