import pandas as pd

class fileutils:
  def __init__(self):
      pass

  def covert_csv_to_excel(self, outdirectory):
      read_file = pd.read_csv (outdirectory+"/output.txt")
      read_file.to_excel (outdirectory+"/output.xls", index = None, header=True)

      
  
