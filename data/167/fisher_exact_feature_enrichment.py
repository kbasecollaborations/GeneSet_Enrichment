import sys
from scipy.stats import hypergeom
import scipy.stats as stats

if len(sys.argv) < 3:
   exit("Usage: python feature_enrichment.py <feature association file> <genelist>")
   
gene_feature = {}
feature_dict = {}

association_file = sys.argv[1]

try:
   fassoc = open(association_file, "r")
         
   for line in fassoc:
     line = line.rstrip()
     id = line.split("\t")
     feature_id = id[1]
     num_fields = len(id)
     feature_dict[feature_id] = num_fields - 2

     for i in range(3, num_fields):
         gene_id = id[i]

         if gene_id not in gene_feature:
            feature_value = []
            feature_value.append(feature_id) 
            gene_feature[gene_id] = feature_value
         else:
            gene_feature[gene_id].append(feature_id)
   fassoc.close()

except IOError:
       print ('cannot open', association_file)
       fassoc.close()


N = len(gene_feature.keys())

n = 0
featurefreq = {}

gene_file = sys.argv[2]

try:
   fgene = open(gene_file, "r")
   for gline in fgene:
     gline = gline.rstrip()
     n += 1
     geneids = gline.split(",")

     if geneids[0] in gene_feature:
        feature_list = gene_feature[geneids[0]]

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
       
       print ("Feature Id = " + feature_key + "\tN = " + str(N) + "\tK = " + str(K) + "\tn = " + str(n) + "\tk = " + str(k) + "\tFisher Exact(P value) = " +str( pvalue))

       print ("Feature Id = " + feature_key + "\tN = " + str(N) + "\tK = " + str(K) + "\tn = " + str(n) + "\tk = " + str(k) + "\tSignificance = " +str(prb))
   fgene.close()
    
except IOError:
        print ('cannot open', gene_file)
        fgene.close()

