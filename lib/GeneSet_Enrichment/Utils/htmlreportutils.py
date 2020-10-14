import uuid
import os
from installed_clients.DataFileUtilClient import DataFileUtil
from installed_clients.KBaseReportClient import KBaseReport
import pandas as pd


class htmlreportutils:
    def __init__(self):
        pass

    def get_css(self):
        css = "<style>" \
              ".dropbtn {background-color: #F8F8F8;color: black;padding: 16px;font-size: 16px;" \
              "border: none;cursor: pointer;} .dropdown {position: relative;isplay: inline-block;}  " \
              ".dropdown-content {display: none; position: absolute; right: 0; background-color: #f9f9f9; " \
              "min-width: 160px; box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2); z-index: 1; } " \
              ".dropdown-content a { color: black; padding: 12px 16px; ext-decoration: none; " \
              "display: block;} .dropdown-content a:hover {background-color: #f1f1f1;} " \
              ".dropdown:hover .dropdown-content { display: block; } .dropdown:hover .dropbtn { background-color: #F8F8F8;}" \
              "</style>"
        return css

    def get_menu_options(self, report_list):
        dp_menu = "<div class=\"dropdown\" style=\"float:left;\">" \
                  "<button class=\"dropbtn\">Click to select Feature Set</button>" \
                  "<div class=\"dropdown-content\" style=\"left:0;\">"
        for html_file in report_list:
            dp_menu += "<a href=" + html_file + ".html" + ">" + html_file + "</a>"

        dp_menu += "</div></div>"
        return dp_menu

    def listToString(self, s):
        str1 = " "
        return (str1.join(s))

    def get_genelist(self, genelistfile):

        try:
            with open(genelistfile, 'r') as f:
                genelist = []

                for x in f:
                    genelist.append(x.rstrip())
        except IOError as e:
            print("I/O error({0}): {1}".format(e.errno, e.strerror))
        except:  # handle other exceptions such as attribute errors
            print("Unexpected error:", sys.exc_info()[0])

        geneset = ""
        geneset += "[" + ", ".join(genelist) + "]"
        return geneset

    def get_subfiles(self, dir):
        "Get a list of immediate subfiles"
        return next(os.walk(dir))[2]

    def get_subdirs(self, dir):
        "Get a list of immediate subdirectories"
        return next(os.walk(dir))[1]

    def create_table(self, filename, caption, output_dir):

        id = filename.split(".")[0]

        if (filename.find('paper') != -1):
            html_out = "<div style=\"height: 1400px; width: 1700px; border: 1px ridge; black;\">"
            html_out += "<center><h3>Gene Set Enrichment using " + caption + "</h3></center>"
            html_out += "<table id=\"" + id + "\" " + "class=\"display\" style=\"width:100%\">" \
                                              "<thead><tr><th>Pubmed Url</th><th>Title</th><th>Matches</th><th>P-Value</th><th>Genes</th>" \
                                              "<th>Organism Name</th></tr></thead><tfoot><tr><th>Pubmed Url</th><th>Title</th>" \
                                              "<th>Matches</th><th>P-Value</th><th>Genes</th><th>Organism Name</th></tr></tfoot></table>"
        else:
            html_out = "<div style=\"height: 630px; width: 1700px; border: 1px ridge; black;\">"
            html_out += "<center><h3>Gene Set Enrichment using " + caption + "</h3></center>"
            html_out += "<table id=\"" + id + "\" " + "class=\"display\" style=\"width:100%\">" \
                                              "<thead><tr><th>Feature Id</th><th>Term</th><th>Matches</th><th>P-Value</th><th>Genes</th>" \
                                              "</tr></thead><tfoot><tr><th>Feature Id</th><th>Term</th>" \
                                              "<th>Matches</th><th>P-Value</th><th>Genes</th></tr></tfoot></table>"
        html_out += "</div>"
        return html_out

    def create_enrichment_report(self, output_dir, dir, featureset):
        '''
                function for adding enrichment score to report
        '''

        dirs = next(os.walk(dir))[1]

        output = "<html><head>" \
                 + self.get_css() + "<link rel=\"stylesheet\" type=\"text/css" \
                                    "\" href=\"https://cdn.datatables.net/1.10.22/css/jquery.dataTables.min.css\">" \
                                    "<link rel=\"stylesheet\" type=\"text/css " \
                                    "\"href=\"https://cdn.datatables.net/scroller/2.0.3/css/scroller.dataTables.min.css\">" \
                                    "<script src=\"https://code.jquery.com/jquery-3.5.1.js\"></script>" \
                                    "<script src=\"https://cdn.datatables.net/1.10.22/js/jquery.dataTables.min.js\"></script>" \
                                    "<script src=\"https://cdn.datatables.net/scroller/2.0.3/js/dataTables.scroller.min.js\"></script>" \
                                    "<script src=\"https://cdn.datatables.net/buttons/1.6.4/js/dataTables.buttons.min.js\"></script>" \
                                    "<script src=\"https://cdn.datatables.net/buttons/1.6.4/js/buttons.flash.min.js\"></script>" \
                                    "<script src=\"https://cdnjs.cloudflare.com/ajax/libs/jszip/3.1.3/jszip.min.js\"></script>" \
                                    "<script src=\"https://cdnjs.cloudflare.com/ajax/libs/pdfmake/0.1.53/pdfmake.min.js\"></script>" \
                                    "<script src=\"https://cdnjs.cloudflare.com/ajax/libs/pdfmake/0.1.53/vfs_fonts.js\"></script>" \
                                    "<script src=\"https://cdn.datatables.net/buttons/1.6.4/js/buttons.html5.min.js\"></script>" \
                                    "<script src=\"https://cdn.datatables.net/buttons/1.6.4/js/buttons.print.min.js\"></script>" \
                                    "<script src=\"https://cdn.datatables.net/buttons/1.6.4/js/buttons.colVis.min.js\"></script>" \
                                    "<script src=\"https://cdn.datatables.net/fixedcolumns/3.3.2/js/dataTables.fixedColumns.min.js\"></script>"

        output += "<script> $(document).ready(function() { $.getJSON(\'" + featureset + "/go_biological_process_output.json\', function(data){ $(\'#go_biological_process_output\').DataTable( {" \
                  "dom: \'Bfrtip\', lengthMenu: [[10, 25, 50, 100], [10, 25, 50, 100]], buttons: [\'colvis\', \'csv\', \'pageLength\'], columnDefs : [{targets: [1],width : \"50%\"},{targets: [ 4 ], visible: false}], data: data, deferRender: true,scrollY: 399, scrollCollapse: true, scroller: true });" \
                  "}).fail(function(){ console.log(\"An error has occurred.\");});});</script>"

        output += "<script> $(document).ready(function() { $.getJSON(\'" + featureset + "/go_molecular_function_output.json\', function(data){ $(\'#go_molecular_function_output\').DataTable( {" \
                  "dom: \'Bfrtip\', lengthMenu: [[10, 25, 50, 100], [10, 25, 50, 100]], buttons: [\'colvis\', \'csv\', \'pageLength\'], columnDefs : [{targets: [1],width : \"50%\"},{targets: [ 4 ], visible: false}], data: data, deferRender: true,scrollY: 399, scrollCollapse: true, scroller: true });" \
                  "}).fail(function(){ console.log(\"An error has occurred.\");});});</script>"

        output += "<script> $(document).ready(function() { $.getJSON(\'" + featureset + "/go_cellular_component_output.json\', function(data){ $(\'#go_cellular_component_output\').DataTable( {" \
                  "dom: \'Bfrtip\', lengthMenu: [[10, 25, 50, 100], [10, 25, 50, 100]], buttons: [\'colvis\', \'csv\', \'pageLength\'], columnDefs : [{targets: [1], width : \"50%\"},{targets: [ 4 ], visible: false}], data: data, deferRender: true,scrollY: 399, scrollCollapse: true, scroller: true });" \
                  "}).fail(function(){ console.log(\"An error has occurred.\");});});</script>"

        output += "<script> $(document).ready(function() { $.getJSON(\'" + featureset + "/kegg_enzyme_output.json\', function(data){ $(\'#kegg_enzyme_output\').DataTable( {" \
                  "dom: \'Bfrtip\', lengthMenu: [[10, 25, 50, 100], [10, 25, 50, 100]], buttons: [\'colvis\', \'csv\', \'pageLength\'], columnDefs : [{targets: [1], width : \"50%\"},{targets: [ 4 ], visible: false}], data: data, deferRender: true,scrollY: 399, scrollCollapse: true, scroller: true });" \
                  "}).fail(function(){ console.log(\"An error has occurred.\");});});</script>"

        output += "<script> $(document).ready(function() { $.getJSON(\'" + featureset + "/kog_output.json\', function(data){ $(\'#kog_output\').DataTable( {" \
                  "dom: \'Bfrtip\', lengthMenu: [[10, 25, 50, 100], [10, 25, 50, 100]], buttons: [\'colvis\', \'csv\', \'pageLength\'], columnDefs : [{targets: [1], width : \"50%\"},{targets: [ 4 ], visible: false}], deferRender: true,scrollY: 399, scrollCollapse: true, scroller: true });" \
                  "}).fail(function(){ console.log(\"An error has occurred.\");});});</script>"

        output += "<script> $(document).ready(function() { $.getJSON(\'" + featureset + "/panther_output.json\', function(data){ $(\'#panther_output\').DataTable( {" \
                  "dom: \'Bfrtip\', lengthMenu: [[10, 25, 50, 100], [10, 25, 50, 100]], buttons: [\'colvis\', \'csv\', \'pageLength\'], columnDefs : [{targets: [1], width : \"50%\"},{targets: [ 4 ], visible: false}], data: data, deferRender: true,scrollY: 399, scrollCollapse: true, scroller: true });" \
                  "}).fail(function(){ console.log(\"An error has occurred.\");});});</script>"

        output += "<script> $(document).ready(function() { $.getJSON(\'" + featureset + "/smart_output.json\', function(data){ $(\'#smart_output\').DataTable( {" \
                  "dom: \'Bfrtip\', lengthMenu: [[10, 25, 50, 100], [10, 25, 50, 100]], buttons: [\'colvis\', \'csv\', \'pageLength\'], columnDefs : [{targets: [1], width : \"50%\"},{targets: [ 4 ], visible: false}], data: data, deferRender: true,scrollY: 399, scrollCollapse: true, scroller: true });" \
                  "}).fail(function(){ console.log(\"An error has occurred.\");});});</script>"

        output += "<script> $(document).ready(function() { $.getJSON(\'" + featureset + "/pfam_output.json\', function(data){ $(\'#pfam_output\').DataTable( {" \
                  "dom: \'Bfrtip\', lengthMenu: [[10, 25, 50, 100], [10, 25, 50, 100]], buttons: [\'colvis\', \'csv\', \'pageLength\'], columnDefs : [{targets: [1], width : \"50%\"},{targets: [ 4 ], visible: false}], data: data, deferRender: true,scrollY: 399, scrollCollapse: true, scroller: true });" \
                  "}).fail(function(){ console.log(\"An error has occurred.\");});});</script>"

        output += "<script> $(document).ready(function() { $.getJSON(\'" + featureset + "/pathway_output.json\', function(data){ $(\'#pathway_output\').DataTable( {" \
                  "dom: \'Bfrtip\', lengthMenu: [[10, 25, 50, 100], [10, 25, 50, 100]], buttons: [\'colvis\', \'csv\', \'pageLength\'], columnDefs : [{targets: [1], width : \"50%\"},{targets: [ 4 ], visible: false}], data: data, deferRender: true,scrollY: 399, scrollCollapse: true, scroller: true });" \
                  "}).fail(function(){ console.log(\"An error has occurred.\");});});</script>"

        output += "<script> $(document).ready(function() { $.getJSON(\'" + featureset + "/paper_output.json\', function(data){ $(\'#paper_output\').DataTable( {" \
                  "dom: \'Bfrtip\', lengthMenu: [[10, 25, 50, 100], [10, 25, 50, 100]], buttons: [\'colvis\', \'csv\', \'pageLength\'], columnDefs : [{targets: [1], width : \"50%\"},{targets: [ 4 ], visible: false}], data: data, deferRender: true,scrollY: 799, scrollCollapse: true, scroller: true });" \
                  "}).fail(function(){ console.log(\"An error has occurred.\");});});</script>"


        output += "</head>" \
                  "<body>" + self.get_menu_options(dirs)

        output += "<table style=\"width:95%\" cellpadding = \"50\" cellspacing = \"50\" >"
        output += "<caption> <h1> Geneset Results for " + featureset + "</h1> </caption>"
        output += "<tr><td style=\"padding:10px\">" + self.create_table("go_biological_process_output.txt", "GO (Biological Process)", output_dir) + "</td></tr>" \
                  + "<tr><td style=\"padding:10px\">" + self.create_table("go_molecular_function_output.txt",  "GO (Molecular Function)", output_dir) + "</td></tr>" \
                  + "<tr><td style=\"padding:10px\">" + self.create_table("go_cellular_component_output.txt", "GO (Cellular Component)", output_dir) + "</td></tr>"


        output += "<tr><td style=\"padding:10px\">" + self.create_table("kegg_enzyme_output.txt", "KEGG Enzyme",output_dir) + "</td></tr>" \
                  + "<tr><td style=\"padding:10px\">" + self.create_table("kog_output.txt", "KOG", output_dir) + "</td></tr>" \
                  + "<tr><td style=\"padding:10px\">" + self.create_table("panther_output.txt", "Panther",output_dir) + "</td></tr>"

        output += "<tr><td style=\"padding:10px\">" + self.create_table("smart_output.txt", "SMART", output_dir) + "</td></tr>" \
                  + "<tr><td style=\"padding:10px\">" + self.create_table("pfam_output.txt", "PFAM", output_dir) + "</td></tr>" \
                  + "<tr><td style=\"padding:10px\">" + self.create_table("pathway_output.txt", "Pathway", output_dir) + "</td></tr>"

        output += "<tr><td style=\"padding:10px\">" + self.create_table("paper_output.txt", "Publication", output_dir) + "</td></tr>"

        output += "</table>"

        output += "</body></html>"


        return output

    def create_html_report(self, callback_url, output_dir, workspace_name):
        '''
         function for creating html report
        '''

        dfu = DataFileUtil(callback_url)
        report_name = 'kb_gsea_report_' + str(uuid.uuid4())
        report = KBaseReport(callback_url)

        report_list = self.get_subdirs(output_dir)
        htmlstring = "<html><head>" + self.get_css() + "</head><body>" + self.get_menu_options(report_list)
        htmlstring += "</body></html>"

        index_file_path = output_dir + "/index.html"

        try:
            with open(index_file_path, "wt") as hfile:
                n = hfile.write(htmlstring)
        except IOError as e:
            print ("I/O error({0}): {1}".format(e.errno, e.strerror))
        except:  # handle other exceptions such as attribute errors
            print ("Unexpected error:", sys.exc_info()[0])

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



