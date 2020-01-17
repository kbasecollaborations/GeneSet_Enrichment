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
  def listToString(self, s):  
    
    # initialize an empty string 
    str1 = ""  
    
    # traverse in the string   
    for ele in s:  
        str1 += ele   
    
    # return string   
    return str1 

  # function to get unique values 
  def unique(self, list1): 
    # insert the list to the set 
    list_set = set(list1) 
    # convert the set to the list 
    unique_list = (list(list_set)) 
    for x in unique_list: 
        print (x)

  def get_genomeid_from_featuresetid (self, genelistref):
      genome = {}
      get_objects_params = {'object_refs' : [genelistref]} 
      geneset = self.dfu.get_objects(get_objects_params)['data'][0]['data']
      print(type(geneset['elements'].values()))
      for k, v in geneset['elements'].items():
        print(self.listToString(v))
        genome[self.listToString(v)] = 1
      if (len(genome) != 1):
         exit("source of genome is not unique\n")
      else:
         return (list(genome.values())[0])
      #self.unique(geneset['elements'].values())



     
     
      
  
