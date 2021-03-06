import csv
import errno
import logging
import os
import re
import string
import time
import uuid

from installed_clients.DataFileUtilClient import DataFileUtil
from installed_clients.KBaseReportClient import KBaseReport
from installed_clients.WorkspaceClient import Workspace as Workspace
from installed_clients.GenomeSearchUtilClient import GenomeSearchUtil

class featuresetbuilder:

    def __init__(self, config):
        self.ws_url = config["workspace-url"]
        self.callback_url = os.environ['SDK_CALLBACK_URL']
        self.dfu = DataFileUtil(self.callback_url)
        self.gsu = GenomeSearchUtil(self.callback_url)

    def validate_params(self, params):
        if 'genome' not in params:
            raise ValueError('required genome field was not defined')
        elif 'genes' not in params:
            raise ValueError('required genes field was not defined')
        elif 'description' not in params:
            raise ValueError('required description field was not defined')
        elif 'output_feature_set' not in params:
            raise ValueError('required output_feature_set field was not defined')

    def _get_feature_ids(self, genome_ref, ids):
        """
        _get_feature_ids: get feature ids from genome
        """
        
        genome_features = self.gsu.search({'ref': genome_ref,
                                           'limit': len(ids),
                                           'structured_query': {"$or": [{"feature_id": x}
                                                                        for x in ids]},
                                           'sort_by': [['feature_id', True]]})['features']

        features_ids = set((feature.get('feature_id') for feature in genome_features))

        return features_ids 

    def _build_fs_obj(self, params):
        new_feature_set = {
            'description': '',
            'element_ordering': [],
            'elements': {}
        }
        genome_ref = params['genome']
     
        element_ordering =[]
        elements = {}
       
        gene_ids = re.split(r'[\r\n \n \t \s ,]', params['genes']) 

        
        new_feature_ids = []
        new_feature_ids = gene_ids
        
        if new_feature_ids:
            genome_feature_ids = self._get_feature_ids(genome_ref, new_feature_ids)
        for new_feature in new_feature_ids:
            if new_feature not in genome_feature_ids:
                print(new_feature)
                raise ValueError('Feature ID {} does not exist in the supplied genome {}'.format(
                    new_feature, genome_ref)) 
        

        for ids in gene_ids:
            element_ordering.append(ids)
            geno_ref = []
            geno_ref.append(genome_ref)
            elements[ids] = geno_ref

        new_feature_set = {
            'description': params['description'],
            'element_ordering': element_ordering,
            'elements': elements
        }
        return new_feature_set

    def build_feature_set(self, params):

        workspace_id = self.dfu.ws_name_to_id(params['workspace_name'])
        new_feature_set = self._build_fs_obj(params)
        save_object_params = {
            'id': workspace_id,
            'objects': [{'type': 'KBaseCollections.FeatureSet',
                         ''
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
