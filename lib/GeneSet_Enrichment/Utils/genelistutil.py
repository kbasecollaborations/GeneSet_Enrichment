import sys
import os
import json
import uuid
import csv 
from installed_clients.DataFileUtilClient import DataFileUtil

class genelistutil:
  def __init__(self):
      self.callback_url = os.environ['SDK_CALLBACK_URL']
      self.dfu = DataFileUtil(self.callback_url) 
      pass

  def download_genelist(self, genelistref, genesetfile):
      get_objects_params = {'object_refs' : [genelistref]} 
      geneset = self.dfu.get_objects(get_objects_params)['data'][0]['data']
      with open(genesetfile, 'w') as filehandle:
           for item in geneset['element_ordering']:
               filehandle.write('%s\n' % item)

      print(geneset['element_ordering'])
      '''
      matrix_data= ExpSet['data']
      diff_expr_matrix_file_name = 'gene_results.csv'
      result_directory = "/kb/module/work/tmp/"
      diff_expr_matrix_file = os.path.join(result_directory, diff_expr_matrix_file_name)
     
      with open(diff_expr_matrix_file, 'w') as csvfile:
           fieldnames = ['gene_id', 'log2_fold_change', 'p_value', 'q_value']
           writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter="\t")
           writer.writeheader() 
        
      with open(diff_expr_matrix_file, 'a') as csvfile:
           row_ids = matrix_data.get('row_ids')
           row_values = matrix_data.get('values')
           writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter="\t")
           for pos, row_id in enumerate(row_ids):
               row_value = row_values[pos]
               #print(row_value[0])
               if not (str(row_value[0]) == "None") :
                  writer.writerow({'gene_id': row_id,
                                         'log2_fold_change': row_value[0],
                                         'p_value': row_value[1],
                                         'q_value': row_value[2]}) 
     
      '''
      
  
