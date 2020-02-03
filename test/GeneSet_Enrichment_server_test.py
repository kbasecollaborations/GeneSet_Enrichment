# -*- coding: utf-8 -*-
import os
import time
import re
import unittest
from configparser import ConfigParser

from GeneSet_Enrichment.GeneSet_EnrichmentImpl import GeneSet_Enrichment
from GeneSet_Enrichment.GeneSet_EnrichmentServer import MethodContext
from GeneSet_Enrichment.authclient import KBaseAuth as _KBaseAuth

from installed_clients.WorkspaceClient import Workspace


class GeneSet_EnrichmentTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        token = os.environ.get('KB_AUTH_TOKEN', None)
        config_file = os.environ.get('KB_DEPLOYMENT_CONFIG', None)
        cls.cfg = {}
        config = ConfigParser()
        config.read(config_file)
        for nameval in config.items('GeneSet_Enrichment'):
            cls.cfg[nameval[0]] = nameval[1]
        # Getting username from Auth profile for token
        authServiceUrl = cls.cfg['auth-service-url']
        auth_client = _KBaseAuth(authServiceUrl)
        user_id = auth_client.get_user(token)
        # WARNING: don't call any logging methods on the context object,
        # it'll result in a NoneType error
        cls.ctx = MethodContext(None)
        cls.ctx.update({'token': token,
                        'user_id': user_id,
                        'provenance': [
                            {'service': 'GeneSet_Enrichment',
                             'method': 'please_never_use_it_in_production',
                             'method_params': []
                             }],
                        'authenticated': 1})
        cls.wsURL = cls.cfg['workspace-url']
        cls.wsClient = Workspace(cls.wsURL)
        cls.serviceImpl = GeneSet_Enrichment(cls.cfg)
        cls.scratch = cls.cfg['scratch']
        cls.callback_url = os.environ['SDK_CALLBACK_URL']
        suffix = int(time.time() * 1000)
        cls.wsName = "test_ContigFilter_" + str(suffix)
        ret = cls.wsClient.create_workspace({'workspace': cls.wsName})  # noqa

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'wsName'):
            cls.wsClient.delete_workspace({'workspace': cls.wsName})
            print('Test workspace was deleted')

    # NOTE: According to Python unittest naming rules test method names should start from 'test'. # noqa
    def test_your_method(self):
        # Prepare test objects in workspace if needed using
        # self.getWsClient().save_objects({'workspace': self.getWsName(),
        #                                  'objects': []})
        #
        # Run your method by
        # ret = self.getImpl().your_method(self.getContext(), parameters...)
        #
        # Check returned data with
        # self.assertEqual(ret[...], ...) or other unittest methods
        params = {
            'workspace_name': 'man4ish_gupta:narrative_1578459434770',
            'genelist' : ['35540/3/1','35540/3/1','35540/3/1','35540/3/1','35540/3/1','35540/3/1']
        } 

        #ret = self.serviceImpl.run_GeneSet_Enrichment(self.ctx, params)
    
    def test_build_feature_set(self):
        input_params = {
            'genome': '35540/2/1',
            'genes': "AT3G14440\nAT1G20440\nAT4G27520\nAT2G23120\nAT5G58070\nAT1G20450\nAT1G01470\nAT5G52310\nAT1G76180\nAT2G02100\nAT1G73480\nAT4G15480\nAT3G29575",
            'description': "sameple geneset",
            #'workspace_name': 'man4ish_gupta:narrative_1578459434770',
            'workspace_name': 'man4ish_gupta:narrative_1579638904735',
            'output_feature_set': 'new_feature_set',
        }
        
        result = self.serviceImpl.build_Featureset(self.ctx, input_params)
     
  

   

     

