import sys
from scipy.stats import hypergeom

if len(sys.argv) < 2:
   exit("Usage: python split_gmtfile_to_category.py <go category file> <feature association file>")
   
gocateg = {}

go_categoty_file = sys.argv[1]

try:
   fcategory = open(go_categoty_file, "r")
   for gcline in fcategory:
       gcline = gcline.rstrip()
       gcategrec = gcline.split("\t")
       gocateg[gcategrec[0]] = gcategrec[1].lstrip()
   fcategory.close()
except IOError:
       print ('cannot open', go_category_file)
       fcategory.close()

feature_dict = {}

association_file = sys.argv[2]

try:
   fassoc = open(association_file, "r")
         
   for line in fassoc:
     line = line.rstrip()
     id = line.split("\t")
     feature_id = id[1]
     num_fields = len(id)
     outfile = gocateg[feature_id] + "_" + association_file
     try:
        foutput = open(outfile, "a")
        foutput.write(line)
        foutput.close() 
     except IOError:
       print ('cannot open', outfile)
       foutput.close()

   fassoc.close()

except IOError:
       print ('cannot open', association_file)
       fassoc.close()
