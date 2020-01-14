# -*- coding: utf-8 -*-
#BEGIN_HEADER
import logging
from GeneSet_Enrichment.Utils.gsea import gsea
from GeneSet_Enrichment.Utils.genelistutil import genelistutil
from GeneSet_Enrichment.Utils.fileutils import fileutils
from GeneSet_Enrichment.Utils.htmlreportutils import htmlreportutils
import os
import uuid
from installed_clients.DataFileUtilClient import DataFileUtil
from installed_clients.KBaseReportClient import KBaseReport
#END_HEADER


class GeneSet_Enrichment:
    '''
    Module Name:
    GeneSet_Enrichment

    Module Description:
    A KBase module: GeneSet_Enrichment
    '''

    ######## WARNING FOR GEVENT USERS ####### noqa
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    ######################################### noqa
    VERSION = "0.0.1"
    GIT_URL = ""
    GIT_COMMIT_HASH = "567bc1b247c97110c9dc9d809d01ded9c24e700a"

    #BEGIN_CLASS_HEADER
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        self.callback_url = os.environ['SDK_CALLBACK_URL']
        self.shared_folder = config['scratch']
        logging.basicConfig(format='%(created)s %(levelname)s: %(message)s',
                            level=logging.INFO)
        self.gs = gsea()
        self.hr = htmlreportutils()
        self.gu = genelistutil()
        self.dfu = DataFileUtil(self.callback_url) 
        self.fu = fileutils()
        #END_CONSTRUCTOR
        pass


    def run_GeneSet_Enrichment(self, ctx, params):
        """
        This example function accepts any number of parameters and returns results in a KBaseReport
        :param params: instance of type "gseaparams" -> structure: parameter
           "obj_name" of String, parameter "workspace_name" of String,
           parameter "expression_matrix" of String, parameter
           "permutation_number" of Long
        :returns: instance of type "ReportResults" -> structure: parameter
           "report_name" of String, parameter "report_ref" of String
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN run_GeneSet_Enrichment
       
        result_directory = "/kb/module/work/tmp/"
        
        
        for i in range(len(params['genelist'])):
           genelist_file = os.path.join(result_directory, "genelist"+str(i))
           self.gu.download_genelist(params['genelist'][i], genelist_file)
           
        workspace = params['workspace_name']
        featurelist = ['go_biological_process', 'go_molecular_function', 'go_cellular_component', 'smart', 'pfam', 'kegg_enzyme', 'kog', 'pathway', 'panther']
       
        outputdir = '/kb/module/work/tmp/' + str(uuid.uuid1())
        #print(type(outputdir))
        os.mkdir(outputdir)
        #print(type(outputdir))

        for i in range(len(params['genelist'])): 
           gene_set_dir = os.path.join(outputdir, "output"+ str(i))
        
           if not os.path.exists(gene_set_dir):
              os.mkdir(gene_set_dir)
           

           for feature in featurelist:
              filename = os.path.join("/kb/module/work/tmp", "genelist"+str(i))
              self.gs.run_gsea(feature, filename , gene_set_dir)
              

        for i in range(len(params['genelist'])):
           gene_set_dir = os.path.join(outputdir, "output"+ str(i))
           output = self.hr.create_html(gene_set_dir)
           foutput = open(gene_set_dir + "/output.html", "w")
           foutput.write(output+"\n")
           foutput.close()
           
        output = self.hr.create_html_report(self.callback_url, outputdir, workspace)
          #self.fu.covert_csv_to_excel(feature, outputdir)

        #output = self.hr.create_html_report(self.callback_url, outputdir, workspace)
        report = KBaseReport(self.callback_url)
        #END run_GeneSet_Enrichment

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method run_GeneSet_Enrichment return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]

    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {'state': "OK",
                     'message': "",
                     'version': self.VERSION,
                     'git_url': self.GIT_URL,
                     'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]
