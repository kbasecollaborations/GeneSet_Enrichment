import sys
import os
import json
import uuid
import gzip
from scipy.stats import hypergeom
from GeneSet_Enrichment.Utils.htmlreportutils import htmlreportutils

class gsea:
  def __init__(self):
      self.organism_dict = {}
      self.hr = htmlreportutils()
      pass

  #def load_organism_file(self, filename):
  def load_organism_file(self, filename, id):
      try:
          with open(filename, 'r') as f:
              for x in f:
                  x = x.rstrip()
                  line = x.split("\t")
                  if(id == '444'):
                      self.organism_dict[line[0]] = [line[1], line[2]]  #quick fix for 444
                  else:
                      self.organism_dict[line[0]] = line[1]
      except IOError as e:
          print ("I/O error({0}): {1}".format(e.errno, e.strerror))
      except:  # handle other exceptions such as attribute errors
          print ("Unexpected error:", sys.exc_info()[0])

  def get_organism(self, pubmed_url):
      if pubmed_url in self.organism_dict.keys():
          return self.organism_dict[pubmed_url]
      else:
          return ''

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

               if gene_id not in gene_feature.keys():
                  feature_value = []
                  feature_value.append(feature_id) 
                  gene_feature[gene_id] = feature_value
               else:
                  gene_feature[gene_id].append(feature_id)     # dictionary of gene and feature

         fassoc.close()

      except IOError:
            print ('cannot open', association_file)
            #fassoc.close()

      N = len(gene_feature.keys())

      n = 0
      featurefreq = {}

      feature_gene_dict = {}

      try:
         fgene = open(gene_file, "r")

         for gline in fgene:
           gline = gline.rstrip()

           n += 1

           geneids = gline.split(",")


           if geneids[0] in gene_feature.keys():
              feature_list = gene_feature[geneids[0]]

              for feature in feature_list:
                  if feature in featurefreq:
                     (feature_gene_dict[feature]).append(geneids[0])
                     featurefreq[feature] += 1 
                  else:
                     feature_gene_dict[feature] = [geneids[0]]
                     featurefreq[feature] = 1
         try:
            with open(outdirectory + "/" + featurename + "_output.txt","a") as fout:
               fout.write("ID\tTerm\tN\tK\tn\tk\tpval\tGene Id\n")

               for feature_key, frequency in featurefreq.items():
                  k = frequency
                  K = feature_dict[feature_key]

                  prb = hypergeom.pmf(k, N, K, n)

                  term = (feature_term[feature_key]).split("_")[1]
                  gene_list = feature_gene_dict[feature_key]
                  fout.write (feature_key + "\t"+ term +"\t" + str(N) + "\t" + str(K) + "\t" + str(n) + "\t" + str(k)
                              + "\t" +str(format(prb, '.3g')) + "\t" + ','.join(gene_list) + "\n")

         except IOError:
             print("cannot open" + outdirectory + "/" + featurename + "_output.txt")
             fout.close()

         try:
            with open(outdirectory + "/" + featurename + "_output.json","a") as fjout:
               #fout.write("ID\tTerm\tN\tK\tn\tk\tpval\n")
               out_list = []

               for feature_key, frequency in featurefreq.items():
                  k = frequency
                  K = feature_dict[feature_key]

                  prb = hypergeom.pmf(k, N, K, n)

                  term = (feature_term[feature_key]).split("_")[1]
                  gene_list = feature_gene_dict[feature_key]
                  if(featurename == "paper"):
                      species_list = self.get_organism(feature_key)
                      if(len(species_list) == 2):
                          organism = species_list[0]
                          taxonomy = species_list[1]
                          out_list.append([feature_key, term, str(k), str(format(prb, '.3g')),  ', '.join(gene_list), "Organism:" +organism, taxonomy])
                      else:
                          if(len(species_list) != 0):
                              organism = species_list[0]
                          else:
                              organism = ''
                          out_list.append([feature_key, term, str(k), str(format(prb, '.3g')), ', '.join(gene_list), "Organism:" + organism])
                  else:
                      out_list.append([feature_key, term, str(k), str(format(prb, '.3g')),  ', '.join(gene_list)])

                  #fout.write (feature_key + "\t"+ term +"\t" + str(N) + "\t" + str(K) + "\t" + str(n) + "\t" + str(k)
                  #            + "\t" +str(format(prb, '.3g')) + "\n")
               fjout.write(json.dumps(out_list))

         except IOError:
             print("cannot open" + outdirectory + "/" + featurename + "_output.txt")
             fout.close()


      except IOError:
         print ('cannot open', gene_file)
         fgene.close()
      
      return (outdirectory)


      
  
