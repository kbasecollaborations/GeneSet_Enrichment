import sys
import os
import json
import uuid
import gzip

from scipy.stats import hypergeom
from GeneSet_Enrichment.Utils.htmlreportutils import htmlreportutils
from GeneSet_Enrichment.Utils.genelistutil import genelistutil

class gsea:
  def __init__(self):
      self.hr = htmlreportutils()
      self.gu = genelistutil()
      pass

  def find_kbase_phytozome_genome_id(self, ws, genome_ref_id):
    
    '''
    Input a KBase genome ref
    Output: 
     return Phytozome genome name in KBase
     return 0 if not a phytozome genome / copy of phytozome genome
    '''
    
    provenance = ws.get_object_provenance([{"ref":genome_ref_id}])
    original_ws_id = provenance[0]['orig_wsid']
    original_workspace_name  = ws.get_workspace_info({'id':original_ws_id})[1]

    if original_workspace_name != 'Phytozome_Genomes':
        return 0

    provenance = ws.get_object_provenance([{"ref":genome_ref_id}])

    if 'copied' in provenance[0]:
        copied = True
        
    while (copied==True):
        provenance = ws.get_object_provenance([{"ref":genome_ref_id}])

        if 'copied' in provenance[0]:
            copied = True
            genome_ref_id = provenance[0]['copied']
        else:
            copied = False

    phytozome_obj_name = ws.get_object_info3({'objects': [{'ref': genome_ref_id}]})['infos'][0][1]

    return phytozome_obj_name
  
  def get_id_from_phytozome(self, phytozome):
    id_phytozome_dict = {}
    file = open('/kb/module/data/mapping_file.txt', 'r') 
    reclines = file.readlines()

    for line in reclines:
       line = line.strip()
       arr = line.split("\t")
       id_phytozome_dict[arr[0]] = arr[1]

    return id_phytozome_dict[phytozome]

      
  def run_gsea(self, featurename, gene_file, outdirectory, phytozyme_name):           
      id = self.get_id_from_phytozome(phytozyme_name)
      association_file = "/kb/module/data/"+id+"/"+id+"_" + featurename + ".gmt"

      feature_dict = {}
      gene_feature = {}
      feature_term = {}
            
      try:
         if(featurename == "paper"):
            fassoc = gzip.open(association_file + '.gz','rt')
         else:
            fassoc = open(association_file, "r")
         
         for line in fassoc:
           line = line.rstrip()
           id = line.split("\t")
           feature_id = id[1]
           num_fields = len(id)

           feature_dict[feature_id] = num_fields - 2
           feature_term[feature_id] = id[0]
           
           for i in range(2, num_fields):
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
            #fassoc.close()

      N = len(gene_feature.keys())

      n = 0
      featurefreq = {}

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
         try:
            with open(outdirectory + "/" + featurename + "_output.txt","a") as fout:
               fout.write("ID\tTerm\tN\tK\tn\tk\tpval\n")

               for feature_key, frequency in featurefreq.items():
                  k = frequency
                  K = feature_dict[feature_key]

                  prb = hypergeom.pmf(k, N, K, n)

                  term = (feature_term[feature_key]).split("_")[1]

                  fout.write (feature_key + "\t"+ term +"\t" + str(N) + "\t" + str(K) + "\t" + str(n) + "\t" + str(k)
                              + "\t" +str(format(prb, '.3g')) + "\n")

         except IOError:
             print("cannot open" + outdirectory + "/" + featurename + "_output.txt")
             fout.close()

      except IOError:
         print ('cannot open', gene_file)
         fgene.close()
      
      return (outdirectory)

  def process_gsea(self, params, ws, outputdir):
      featurelist = ['go_biological_process', 'go_molecular_function', 'go_cellular_component', 'smart', 'pfam',
                     'kegg_enzyme', 'kog', 'pathway', 'panther', 'paper']

      for i in range(len(params['genelist'])):
          genome_id = self.gu.get_genomeid_from_featuresetid(params['genelist'][i])
          phytozyme_name = self.find_kbase_phytozome_genome_id(ws, str(genome_id))

          gene_set_dir = os.path.join(outputdir, phytozyme_name + str(i))

          if not os.path.exists(gene_set_dir):
              os.mkdir(gene_set_dir)

          for feature in featurelist:
              genome_id = self.gu.get_genomeid_from_featuresetid(params['genelist'][i])
              phytozyme_name = self.find_kbase_phytozome_genome_id(ws, str(genome_id))  # using name for id

              id = self.get_id_from_phytozome(phytozyme_name)

              self.hr.load_organism_file('/kb/module/data/' + id + '/' + id + '_paper.names.txt')

              genelist_file = os.path.join(outputdir, phytozyme_name + str(i) + ".genelist")
              self.run_gsea(feature, genelist_file, gene_set_dir, phytozyme_name)

      
  
