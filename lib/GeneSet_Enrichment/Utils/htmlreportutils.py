import uuid
import os
from installed_clients.DataFileUtilClient import DataFileUtil
from installed_clients.KBaseReportClient import KBaseReport
from installed_clients.WorkspaceClient import Workspace
from shutil import copyfile
import pandas as pd

class htmlreportutils:
    def __init__(self):
        pass
     
    def listToString(self, s):  
        str1 = " " 
        return (str1.join(s))    

    def format_files_to_html_report(self, outdirectory):
        htmlstring = "<html><body>";
        directory_list = os.listdir(outdirectory)

        for file_name in directory_list:
            htmlstring += "<a href=" + file_name + ">"+file_name+"</a></br>"
        htmlstring += "</body></html>";
        return (htmlstring)
    
    def create_table(self, filename, caption, output_dir):
        
        id = filename.split(".")[0]
        data = pd.read_csv(output_dir + "/" + filename, sep='\t')
        sorteddf = data.sort_values('pval',ascending=True)
        htmlout = "<center><b>Gene Set Enrichment using " + caption +"</b></center>"
        htmlout += "<div style=\"height: 850px; width: 590px; border: 1px ridge; black; background: #e9d8f2; padding-top: 20px; padding-right: 0px; padding-bottom: 20px; padding-left: 20px; overflow: auto;\"><table id=\"" + id + "\" class=\"table table-striped table-bordered\" style=\"width:100%\"><thead><tr><th>Feature Id</th><th>Term</th><th>Matches</th><th>P-value</th></tr></thead><tbody>"
    
        for index, row in sorteddf.iterrows():
            feature = row['ID']
            term = row['Term']
            matches = row['k']
            pvalue = format(row["pval"], '.3g')
            #print (pvalue)
            htmlout += "<tr><td>" + feature + "</td><td>" + term + "</td><td>" + str(matches) + "</td><td>" + str(pvalue) + "</td></tr>"
        htmlout += "</tbody><tfoot><tr><th>Feature Id</th><th>Term</th><th>Matches</th><th>P-value</th></tr></tfoot></table></div>"
        return htmlout

    def create_enrichment_report(self, output_dir):
        
        output = "<html><head><link rel=\"stylesheet\" type=\"text/css\" href=\"https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css\"><link rel=\"stylesheet\" type=\"text/css \"href=\"https://cdn.datatables.net/1.10.20/css/dataTables.bootstrap.min.css\"><script src=\"https://code.jquery.com/jquery-3.3.1.js\"></script><script src=\"https://cdn.datatables.net/1.10.20/js/jquery.dataTables.min.js\"></script><script src=\"https://cdn.datatables.net/1.10.20/js/dataTables.bootstrap.min.js\"></script>"


        output += "<script> $(document).ready(function() {$(\'#go_biological_process_output\').DataTable();} ); </script>"
        output += "<script> $(document).ready(function() {$(\'#go_molecular_function_output\').DataTable();} ); </script>"
        output += "<script> $(document).ready(function() {$(\'#go_cellular_component_output\').DataTable();} ); </script>"
        output += "<script> $(document).ready(function() {$(\'#kegg_enzyme_output\').DataTable();} ); </script>"
        output += "<script> $(document).ready(function() {$(\'#kog_output\').DataTable();} ); </script>"
        output += "<script> $(document).ready(function() {$(\'#panther_output\').DataTable();} ); </script>"
        output += "<script> $(document).ready(function() {$(\'#smart_output\').DataTable();} ); </script>"
        output += "<script> $(document).ready(function() {$(\'#pfam_output\').DataTable();} ); </script>"
        output += "<script> $(document).ready(function() {$(\'#pathway_output\').DataTable();} ); </script>"
        output += "</head><body><table cellpadding = \"100\" cellspacing = \"100\" >"


        output += "<tr><td style=\"padding:10px\">" + self.create_table("go_biological_process_output.txt", "GO (Biological Process)", output_dir) + "</td><td style=\"padding:10px\">" + self.create_table("go_molecular_function_output.txt", "GO (Molecular Function)", output_dir) + "</td> <td style=\"padding:10px\">" + self.create_table("go_cellular_component_output.txt", "GO (Cellular Component)", output_dir) + "</td></tr>"

        output += "<tr><td style=\"padding:10px\">" + self.create_table("kegg_enzyme_output.txt", "KEGG Enzyme", output_dir) + "</td> <td style=\"padding:10px\">" + self.create_table("kog_output.txt", "KOG", output_dir) + "</td><td style=\"padding:10px\">" + self.create_table("panther_output.txt", "Panther", output_dir) + "</td></tr>"

        output += "<tr><td style=\"padding:10px\">" + self.create_table("smart_output.txt", "SMART", output_dir) + "</td> <td style=\"padding:10px\">" + self.create_table("pfam_output.txt", "PFAM", output_dir) + "</td> <td style=\"padding:10px\">" + self.create_table("pathway_output.txt", "Pathway", output_dir) + "</td></tr>"

        output += "</table></body></html>"
      
        return output

    def create_html_report(self, callback_url, output_dir, workspace_name):
        '''
         function for creating html report
        '''

        dfu = DataFileUtil(callback_url)
        report_name = 'kb_gsea_report_' + str(uuid.uuid4())
        report = KBaseReport(callback_url)
      
        htmlstring = self.format_files_to_html_report(output_dir)
        index_file_path = output_dir + "/index.html"
        html_file = open(index_file_path, "wt")
        n = html_file.write(htmlstring)
        html_file.close()

        report_shock_id = dfu.file_to_shock({'file_path': output_dir,
                                            'pack': 'zip'})['shock_id']

        html_file = {
            'shock_id': report_shock_id,
            'name': 'index.html',
            'label': 'index.html',
            'description': 'HTMLL report for GSEA'
            }
        
        report_info = report.create_extended_report({
                        'direct_html_link_index': 0,
                        'html_links': [html_file],
                        'report_object_name': report_name,
                        'workspace_name': workspace_name
                    })
        return {
            'report_name': report_info['name'],
            'report_ref': report_info['ref']
        }
