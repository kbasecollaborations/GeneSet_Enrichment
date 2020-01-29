import csv
import errno
import logging
import os
import re
import string
import time
import uuid

from installed_clients.DataFileUtilClient import DataFileUtil
from installed_clients.GenomeSearchUtilClient import GenomeSearchUtil
from installed_clients.KBaseReportClient import KBaseReport
from installed_clients.WorkspaceClient import Workspace as Workspace

class FeatureSetBuilder:

    def _mkdir_p(self, path):
        """
        _mkdir_p: make directory for given path
        """
        if not path:
            return
        try:
            os.makedirs(path)
        except OSError as exc:
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else:
                raise

   
    '''@staticmethod
    def validate_params(params, expected, opt_param=set()):
        """Validates that required parameters are present. Warns if unexpected parameters appear"""
        expected = set(expected)
        opt_param = set(opt_param)
        pkeys = set(params)
        if expected - pkeys:
            raise ValueError("Required keys {} not in supplied parameters"
                             .format(", ".join(expected - pkeys)))
        defined_param = expected | opt_param
        for param in params:
            if param not in defined_param:
                logging.warning("Unexpected parameter {} supplied".format(param))'''

    def _build_fs_obj(self, params):
        new_feature_set = {
            'description': '',
            'element_ordering': [],
            'elements': {}
        }
        genome_ref = input_params['genome']
     
        element_ordering =[]
        elements = {}
       
        gene_ids = re.split(r'[\r\n \n \t \s ,]', params['genes']) 

        for ids in gene_ids:
            element_ordering.append(ids)
            geno_ref = []
            geno_ref.append(genome_ref)
            elements[ids] = geno_ref

        new_feature_set = {
            'description': input_params['description'],
            'element_ordering': element_ordering,
            'elements': elements
        }

        return new_feature_set

    def __init__(self, config):
        self.ws_url = config["workspace-url"]
        self.callback_url = config['SDK_CALLBACK_URL']
        self.token = config['KB_AUTH_TOKEN']
        self.shock_url = config['shock-url']
        self.ws = Workspace(self.ws_url, token=self.token)
        self.dfu = DataFileUtil(self.callback_url)
        self.gsu = GenomeSearchUtil(self.callback_url)
        self.scratch = config['scratch']

    def build_feature_set(self, params):
        '''self.validate_params(params, {'output_feature_set', 'workspace_name', },
                             {'genome', 'genes','description'})'''
        
        '''feature_sources = ('feature_ids', 'feature_ids_custom', 'base_feature_sets')
        if not any([params.get(x) for x in feature_sources]):
            raise ValueError("You must supply at least one feature source: {}".format(
                ", ".join(feature_sources)))'''

        gene_ids = re.split(r'[\r\n \n \t \s]', params['genes']) 
        exit(gene_ids)

        workspace_id = self.dfu.ws_name_to_id(params['workspace_name'])

        new_feature_set = self._build_fs_obj(params)
        save_object_params = {
            'id': workspace_id,
            'objects': [{'type': 'KBaseCollections.FeatureSet',
                         'data': new_feature_set,
                         'name': params['output_feature_set']}]}

        dfu_oi = self.dfu.save_objects(save_object_params)[0]
        feature_set_obj_ref = '{}/{}/{}'.format(dfu_oi[6], dfu_oi[0], dfu_oi[4])

        objects_created = [{'ref': feature_set_obj_ref,
                            'description': 'Feature Set'}]
        message = 'A new feature set containing {} features was created.'.format(
            len(new_feature_set['elements']))

        report_params = {'message': message,
                         'workspace_name': params['workspace_name'],
                         'objects_created': objects_created,
                         'report_object_name': 'kb_FeatureSetUtils_report_' + str(uuid.uuid4())}

        kbase_report_client = KBaseReport(self.callback_url)
        output = kbase_report_client.create_extended_report(report_params)

        return {'feature_set_ref': feature_set_obj_ref,
                'report_name': output['name'], 'report_ref': output['ref']}
