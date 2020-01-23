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

class buildfeaturesetutils:

    def __init__(self, config):
        self.config = config
        self.config['SDK_CALLBACK_URL'] = os.environ['SDK_CALLBACK_URL']
        self.callback_url = config['SDK_CALLBACK_URL']
        self.ws_url = config["workspace-url"]
        self.config['KB_AUTH_TOKEN'] = os.environ['KB_AUTH_TOKEN']
        self.token = config['KB_AUTH_TOKEN']
        self.shock_url = config['shock-url']
        self.ws = Workspace(self.ws_url, token=self.token)
        self.dfu = DataFileUtil(self.callback_url)
        self.gsu = GenomeSearchUtil(self.callback_url)
        self.scratch = config['scratch']

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

    
    def _generate_report(self, up_feature_set_ref_list, down_feature_set_ref_list,
                         filtered_expression_matrix_ref_list, workspace_name):
        """
        _generate_report: generate summary report
        """

        log('start creating report')

        output_html_files = self._generate_html_report(up_feature_set_ref_list,
                                                       down_feature_set_ref_list)

        objects_created = list()
        for up_feature_set_ref in up_feature_set_ref_list:
            objects_created += [{'ref': up_feature_set_ref,
                                 'description': 'Upper FeatureSet Object'}]
        for down_feature_set_ref in down_feature_set_ref_list:
            objects_created += [{'ref': down_feature_set_ref,
                                 'description': 'Lower FeatureSet Object'}]

        for filtered_expression_matrix_ref in filtered_expression_matrix_ref_list:
            objects_created += [{'ref': filtered_expression_matrix_ref,
                                 'description': 'Filtered ExpressionMatrix Object'}]

        report_params = {'message': '',
                         'workspace_name': workspace_name,
                         'objects_created': objects_created,
                         'html_links': output_html_files,
                         'direct_html_link_index': 0,
                         'html_window_height': 333,
                         'report_object_name': 'kb_FeatureSetUtils_report_' + str(uuid.uuid4())}

        kbase_report_client = KBaseReport(self.callback_url)
        output = kbase_report_client.create_extended_report(report_params)

        report_output = {'report_name': output['name'], 'report_ref': output['ref']}

        return report_output

    def _generate_html_report(self, up_feature_set_ref_list, down_feature_set_ref_list):
        """
        _generate_html_report: generate html summary report
        """

        log('start generating html report')
        html_report = list()

        output_directory = os.path.join(self.scratch, str(uuid.uuid4()))
        self._mkdir_p(output_directory)
        result_file_path = os.path.join(output_directory, 'report.html')

        uppper_feature_content = ''
        for up_feature_set_ref in up_feature_set_ref_list:
            feature_set_obj = self.ws.get_objects2({'objects':
                                                    [{'ref':
                                                     up_feature_set_ref}]})['data'][0]
            feature_set_data = feature_set_obj['data']
            feature_set_info = feature_set_obj['info']

            feature_set_name = feature_set_info[1]

            elements = feature_set_data.get('elements')
            feature_ids = list(elements.keys())

            uppper_feature_content += '<tr><td>{}</td><td>{}</td></tr>'.format(feature_set_name,
                                                                               len(feature_ids))

        lower_feature_content = ''
        for down_feature_set_ref in down_feature_set_ref_list:
            feature_set_obj = self.ws.get_objects2({'objects':
                                                    [{'ref':
                                                     down_feature_set_ref}]})['data'][0]
            feature_set_data = feature_set_obj['data']
            feature_set_info = feature_set_obj['info']

            feature_set_name = feature_set_info[1]

            elements = feature_set_data.get('elements')
            feature_ids = list(elements.keys())

            lower_feature_content += '<tr><td>{}</td><td>{}</td></tr>'.format(feature_set_name,
                                                                              len(feature_ids))

        with open(result_file_path, 'w') as result_file:
            with open(os.path.join(os.path.dirname(__file__), 'report_template.html'),
                      'r') as report_template_file:
                report_template = report_template_file.read()
                report_template = report_template.replace('<tr><td>Upper_FeatureSet</td></tr>',
                                                          uppper_feature_content)

                report_template = report_template.replace('<tr><td>Lower_FeatureSet</td></tr>',
                                                          lower_feature_content)

                result_file.write(report_template)

        html_report.append({'path': result_file_path,
                            'name': os.path.basename(result_file_path),
                            'label': os.path.basename(result_file_path),
                            'description': 'HTML summary report'})
        return html_report

    def _generate_feature_set(self, feature_ids, genome_id, workspace_name, feature_set_name):
        """
        _generate_feature_set: generate FeatureSet object
        KBaseCollections.FeatureSet type:
        typedef structure {
            string description;
            list<feature_id> element_ordering;
            mapping<feature_id, list<genome_ref>> elements;
        } FeatureSet;
        """

        log('start saving KBaseCollections.FeatureSet object')

        if isinstance(workspace_name, int) or workspace_name.isdigit():
            workspace_id = workspace_name
        else:
            workspace_id = self.dfu.ws_name_to_id(workspace_name)

        elements = {feature_id: [genome_id] for feature_id in feature_ids}
        feature_set_data = {'description': 'Generated FeatureSet from DifferentialExpression',
                            'element_ordering': feature_ids,
                            'elements': elements}

        object_type = 'KBaseCollections.FeatureSet'
        save_object_params = {
            'id': workspace_id,
            'objects': [{'type': object_type,
                         'data': feature_set_data,
                         'name': feature_set_name}]}

        dfu_oi = self.dfu.save_objects(save_object_params)[0]
        feature_set_obj_ref = "{}/{}/{}".format(dfu_oi[6], dfu_oi[0], dfu_oi[4])

        return feature_set_obj_ref

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
        if params.get('base_feature_sets', []) and None not in params['base_feature_sets']:
            base_feature_sets = self.dfu.get_objects(
                {'object_refs': params['base_feature_sets']}
            )['data']
            for ret in base_feature_sets:
                base_set = ret['data']
                base_set_name = ret['info'][1]

                new_feature_set['element_ordering'] += [x for x in base_set['element_ordering']
                                                        if x not in new_feature_set['elements']]
                for element, genome_refs in base_set['elements'].items():
                    if element in new_feature_set['elements']:
                        new_feature_set['elements'][element] += [x for x in genome_refs if x not in
                                                                 new_feature_set['elements'][
                                                                     element]]
                    else:
                        new_feature_set['elements'][element] = genome_refs
                new_feature_set['description'] += 'From FeatureSet {}: {}\n'.format(
                    base_set_name, base_set.get('description'))
        new_feature_ids = []
        if params.get('feature_ids'):
            if isinstance(params['feature_ids'], str):
                new_feature_ids += params['feature_ids'].split(',')
            else:
                new_feature_ids += params['feature_ids']
        if params.get('feature_ids_custom'):
            new_feature_ids += params['feature_ids_custom'].split(',')
        if new_feature_ids:
            genome_feature_ids = self._get_feature_ids(genome_ref, new_feature_ids)
        for new_feature in new_feature_ids:
            if new_feature not in genome_feature_ids:
                raise ValueError('Feature ID {} does not exist in the supplied genome {}'.format(
                    new_feature, genome_ref))
            if new_feature in new_feature_set['elements']:
                if genome_ref not in new_feature_set['elements'][new_feature]:
                    new_feature_set['elements'][new_feature].append(genome_ref)
            else:
                new_feature_set['elements'][new_feature] = [genome_ref]
                new_feature_set['element_ordering'].append(new_feature)

        if params.get('description'):
            new_feature_set['description'] = params['description']

        return new_feature_set

    def build_feature_set(self, params):
        self.validate_params(params, {'output_feature_set', 'workspace_name', },
                             {'genome', 'feature_ids', 'feature_ids_custom', 'base_feature_sets',
                              'description'})
        feature_sources = ('feature_ids', 'feature_ids_custom', 'base_feature_sets')
        if not any([params.get(x) for x in feature_sources]):
            raise ValueError("You must supply at least one feature source: {}".format(
                ", ".join(feature_sources)))
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

