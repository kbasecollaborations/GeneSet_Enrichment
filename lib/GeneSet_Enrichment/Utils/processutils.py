import os
from GeneSet_Enrichment.Utils.genelistutil import genelistutil
from GeneSet_Enrichment.Utils.gsea import gsea
from GeneSet_Enrichment.Utils.htmlreportutils import htmlreportutils


class processutils:
  def __init__(self):
      self.hr = htmlreportutils()
      self.gu = genelistutil()
      self.gs = gsea()
      pass

  def process_genelist (self, params, ws, outputdir):
      for i in range(len(params['genelist'])):
          genome_id = self.gu.get_genomeid_from_featuresetid(params['genelist'][i])
          phytozyme_name = self.gs.find_kbase_phytozome_genome_id(ws, str(genome_id))  # using name for id

          genelist_file = os.path.join(outputdir, phytozyme_name + str(i) + ".genelist")
          self.gu.download_genelist(params['genelist'][i], genelist_file)

  def process_enrichment(self, params, ws, outputdir):
      '''
               function for processing enrichment for features
      '''
      for i in range(len(params['genelist'])):
          genome_id = self.gu.get_genomeid_from_featuresetid(params['genelist'][i])
          phytozyme_name = self.gs.find_kbase_phytozome_genome_id(ws, str(genome_id))

          gene_set_dir = os.path.join(outputdir, phytozyme_name + str(i))

          output = self.hr.create_enrichment_report(gene_set_dir, outputdir)

          try:
              with open(gene_set_dir + "/" + phytozyme_name + ".html", "w") as foutput:
                  foutput.write(output + "\n")
          except IOError:
              print("cannot open " + gene_set_dir + "/" + phytozyme_name + ".html")
              foutput.close()

  def process_gsea(self, params, ws, outputdir):
      featurelist = ['go_biological_process', 'go_molecular_function', 'go_cellular_component', 'smart', 'pfam',
                     'kegg_enzyme', 'kog', 'pathway', 'panther', 'paper']

      for i in range(len(params['genelist'])):
          genome_id = self.gu.get_genomeid_from_featuresetid(params['genelist'][i])
          phytozyme_name = self.gs.find_kbase_phytozome_genome_id(ws, str(genome_id))

          gene_set_dir = os.path.join(outputdir, phytozyme_name + str(i))

          if not os.path.exists(gene_set_dir):
              os.mkdir(gene_set_dir)

          for feature in featurelist:
              genome_id = self.gu.get_genomeid_from_featuresetid(params['genelist'][i])
              phytozyme_name = self.gs.find_kbase_phytozome_genome_id(ws, str(genome_id))  # using name for id

              id = self.gs.get_id_from_phytozome(phytozyme_name)

              self.hr.load_organism_file('/kb/module/data/' + id + '/' + id + '_paper.names.txt')

              genelist_file = os.path.join(outputdir, phytozyme_name + str(i) + ".genelist")
              self.gs.run_gsea(feature, genelist_file, gene_set_dir, phytozyme_name)

  
