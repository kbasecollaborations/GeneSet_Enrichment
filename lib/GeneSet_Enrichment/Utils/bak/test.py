from shutil import copyfile
import pandas as pd
import os

class htmlreportutils:
    def __init__(self):
        pass
     
    def listToString(self, s):  
        str1 = " " 
        return (str1.join(s))  

    def get_subfiles(self, dir):
       "Get a list of immediate subfiles"
       return next(os.walk(dir))[2]

    def get_genelist(self, genelistfile):
      f = open(genelistfile, "r")
     
      genelist = []
      
      for x in f:
         genelist.append(x.rstrip())
      geneset = ""
      geneset += "[" + ", ".join(genelist) + "]"
      return geneset

    def get_subdirs(self, organism_name, dir, filepath):
       "Get a list of immediate subdirectories"
       htmlstring = "<html><body><br>Organims Name\tGene List\tOutput Html Link<br>";
       dirs = next(os.walk(dir))[1]
       for i in range(len(next(os.walk(dir))[1])):
          path = os.path.join(dir,(next(os.walk(dir))[1])[i])
          files_in_subdir = self.get_subfiles(path)
          for files in files_in_subdir:
             if(files.endswith(".html")):    
                htmlstring += organism_name +"\t" +self.get_genelist(filepath) +"\t" + "<a href=" + path + "/"+ files + ">"+files+"</a></br>"
       htmlstring += "</body></html>"         
       return htmlstring  
      
    def create_html_report(self, organism_name, output_dir, filepath):
       '''
       function for creating html report
       '''
      
       htmlstring = self.get_subdirs(organism_name, output_dir, filepath)
       index_file_path = output_dir + "/index.html"
       html_file = open(index_file_path, "wt")
       n = html_file.write(htmlstring)
       html_file.close()     

hr = htmlreportutils() 
#print(hr.get_genelist("/home/manish/Desktop/GeneSet_Enrichment/test_local/workdir/tmp/Athaliana_TAIR100"))
#hr.create_html_report( "Arabidopsis Thailana", "/home/manish/Desktop/GeneSet_Enrichment/test_local/workdir/tmp/d8b48f6a-3cd7-11ea-9d21-0242ac110003", "/home/manish/Desktop/GeneSet_Enrichment/test_local/workdir/tmp/Athaliana_TAIR100") 
