import sys
from scipy.stats import hypergeom


gene_file = sys.argv[1]
output = ""

try:
   fgene = open(gene_file, "r")
   for gline in fgene:
     gline = gline.rstrip()
     geneids = gline.split(",")
     output += "\"" + geneids[0] + "\","
   print(output)
    
except IOError:
        print ('cannot open', gene_file)
        fgene.close()

