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
     
      
  
