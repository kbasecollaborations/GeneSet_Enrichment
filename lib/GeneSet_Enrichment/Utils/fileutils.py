import pandas as pd

class fileutils:
  def __init__(self):
      pass

  def covert_csv_to_excel(self, outdirectory, feature):
      read_file = pd.read_csv (outdirectory + "/" + feature + "_output.txt")
      read_file.to_excel (outdirectory + "/" + feature + "_output.xls", index = None, header=True)

      
  
