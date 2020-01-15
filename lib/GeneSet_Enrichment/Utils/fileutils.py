import pandas as pd

class fileutils:
  def __init__(self):
      pass

  def covert_csv_to_excel(self, outdirectory, feature):
      read_file = pd.read_csv (outdirectory + "/" + feature + "_output.txt")
      read_file.to_excel (outdirectory + "/" + feature + "_output.xls", index = None, header=True)

  def get_biomart_genomemap(self, mapping_file):
      genomemap = {}
      genome_file = pd.read_csv (mapping_file, sep='\t')

      for index, row in genome_file.iterrows():
            kbase_id = row['kbase_id']
            biomart_id = row['biomart_id']
            Genome_name = row['Genome_name']
            genomemap[biomart_id] = Genome_name

      return genomemap   
                 
 
 
      
    
  
