import sys
from scipy.stats import hypergeom
import scipy.stats as stats
from statsmodels.sandbox.stats.multicomp import multipletests

if len(sys.argv) < 5:
   exit("Usage: python gocategory_feature_enrichment.py <category term> <go category file> <feature association file> <genelist>")


pvaluelist = []

go_categoty_term = sys.argv[1]
   
gocateg = {}

go_categoty_file = sys.argv[2]

try:
   fcategory = open(go_categoty_file, "r")
   for gcline in fcategory:
       gcline = gcline.rstrip()
       gcategrec = gcline.split("\t")
       #print(gcategrec[0] +"----"+gcategrec[1])
       gocateg[gcategrec[0]] = gcategrec[1].lstrip()
   fcategory.close()
except IOError:
       print ('cannot open', go_category_file)
       fcategory.close()

gene_feature = {}
feature_dict = {}

association_file = sys.argv[3]

try:
   fassoc = open(association_file, "r")
         
   for line in fassoc:
     line = line.rstrip()
     id = line.split("\t")
     feature_id = id[1]
     num_fields = len(id)
     feature_dict[feature_id] = num_fields - 2
     
     #print("****"+gocateg[feature_id]+"****"+go_categoty_term)
     if (gocateg[feature_id] == go_categoty_term):      
        for i in range(3, num_fields):
            gene_id = id[i]

            if gene_id not in gene_feature:
               feature_value = []
               feature_value.append(feature_id) 
               gene_feature[gene_id] = feature_value
               #print(gene_id)
            else:
               gene_feature[gene_id].append(feature_id)
   fassoc.close()

except IOError:
       print ('cannot open', association_file)
       fassoc.close()

N = len(gene_feature.keys())
#print(N)
n = 0
featurefreq = {}

gene_file = sys.argv[4]

try:
   fgene = open(gene_file, "r")
   for gline in fgene:
     gline = gline.rstrip()
     n += 1
     geneids = gline
     #geneids = gline.split(",")

     if geneids in gene_feature:
        feature_list = gene_feature[geneids]

        for feature in feature_list: 
            if feature in featurefreq:
               featurefreq[feature] += 1 
            else:
               featurefreq[feature] = 1


   for feature_key, frequency in featurefreq.items():
       k = frequency
       K = feature_dict[feature_key]
       prb = hypergeom.pmf(k, N, K, n)
       a = k     # frequency of particular GO term in genelist
       b = K - k # frequency of particular GO term in non genelist
       c = n - k # frequency of non particular GO term in genelist
       d = N - K # frequency of non particular GP term in no genelist

       print (str(a) + "\t" + str(b) + "\t" + str(c) + "\t" + str(d))
       oddsratio, pvalue = stats.fisher_exact([[a, b], [c, d]])
       pvaluelist.append(pvalue)
       print ("Feature Id = " + feature_key + "\tN = " + str(N) + "\tK = " + str(K) + "\tn = " + str(n) + "\tk = " + str(k) + "\tFisher Exact(P value) = " +str( pvalue))
        
       print ("Feature Id = " + feature_key +"\t" + gocateg[feature_key] +"\tN = " + str(N) + "\tK = " + str(K) + "\tn = " + str(n) + "\tk = " + str(k) + "\tSignificance = " +str(prb))
   fgene.close()
    
except IOError:
       print ('cannot open', gene_file)
       fgene.close()

p_adjusted = multipletests(pvaluelist, alpha=0.05, method='bonferroni')

print (pvaluelist)

print(p_adjusted[1])

