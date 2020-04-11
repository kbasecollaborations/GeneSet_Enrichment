# -*- coding: utf-8 -*-
#BEGIN_HEADER
import logging
import os
import uuid
import json

from GeneSet_Enrichment.Utils.fileutils import fileutils
from GeneSet_Enrichment.Utils.htmlreportutils import htmlreportutils
from GeneSet_Enrichment.Utils.processutils import processutils
from GeneSet_Enrichment.Utils.featuresetbuilder import featuresetbuilder
from installed_clients.DataFileUtilClient import DataFileUtil
from installed_clients.WorkspaceClient import Workspace


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
    GIT_URL = "https://github.com/kbasecollaborations/GeneSet_Enrichment.git"
    GIT_COMMIT_HASH = "aa9f06e195dde7407c7b7b54920679a56295a6ae"

    #BEGIN_CLASS_HEADER
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        self.callback_url = os.environ['SDK_CALLBACK_URL']
        self.shared_folder = config['scratch']
        self.ws_url = config['workspace-url']
        logging.basicConfig(format='%(created)s %(levelname)s: %(message)s',
                            level=logging.INFO)
        self.config = config
        #self.gs = gsea()
        self.hr = htmlreportutils()
        #self.gu = genelistutil()
        self.dfu = DataFileUtil(self.callback_url) 
        self.fu = fileutils()
        self.pr = processutils()
        self.fsb  = featuresetbuilder(config)
        #END_CONSTRUCTOR
        pass


    def run_GeneSet_Enrichment(self, ctx, params):
        """
        This example function accepts any number of parameters and returns results in a KBaseReport
        :param params: instance of type "gseaparams" -> structure: parameter
           "obj_name" of String, parameter "workspace_name" of String,
           parameter "genelist" of list of String
        :returns: instance of type "ReportResults" -> structure: parameter
           "report_name" of String, parameter "report_ref" of String
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN run_GeneSet_Enrichment

        self.fu.validate_params(params)

        gmap = self.fu.get_biomart_genomemap("/kb/module/data/mapping_file.txt")

        outputdir = self.shared_folder + '/' + str(uuid.uuid1())
        os.mkdir(outputdir)

        self.ws = Workspace(self.ws_url, token=ctx['token'])

        logging.info('--->\nProcessing genelist')
        self.pr.process_genelist(params, self.ws, outputdir)

        logging.info('--->\nProcessing gsea')
        self.pr.process_gsea(params, self.ws, outputdir)

        logging.info('--->\nProcessing enrichment')
        self.pr.process_enrichment(params, self.ws, outputdir)

        workspace = params['workspace_name']
        logging.info('--->\nCreating HTML Report')

        output = self.hr.create_html_report(self.callback_url, outputdir, workspace)
        #self.fu.covert_csv_to_excel(feature, outputdir)

        #END run_GeneSet_Enrichment

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method run_GeneSet_Enrichment return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]

    def build_Featureset(self, ctx, params):
        """
        :param params: instance of type "featuresetparams" -> structure:
           parameter "genome" of type "obj_ref" (An X/Y/Z style reference @id
           ws), parameter "workspace_name" of String, parameter "genes" of
           String, parameter "description" of String, parameter
           "output_feature_set" of String
        :returns: instance of type "BuildFeatureSetResult" -> structure:
           parameter "feature_set_ref" of type "obj_ref" (An X/Y/Z style
           reference @id ws), parameter "report_name" of String, parameter
           "report_ref" of String
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN build_Featureset
        fsb.validate_params(params)
        print('--->\nRunning FeatureSetUtils.build_feature_set\nparams:')
        print(json.dumps(params, indent=1))

        output = self.fsb.build_feature_set(params)
        #END build_Featureset

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method build_Featureset return value ' +
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
