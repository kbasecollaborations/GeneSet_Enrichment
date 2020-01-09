def create_table( filename, caption):
    f = open(filename, "r")
    htmlout = ''
    htmlout += "<html> <head> <style>table {border-collapse: collapse; padding: 1rem; border: 1px solid black; height: 500px;} td {padding: 20px; border: 1px solid black;} caption { display: table-caption; text-align: center;} th {background-color: #4CAF50;color: white; border: 1px solid #999;padding: 0.5rem;text-align: left;background: lightblue;} tbody tr:nth-child(odd) {background: #eee;}</style></head><body><div style=\"height: 500px; width: 500px; overflow: auto\"><table><caption>"+ caption + " Enrichment </caption><tr><th>Feature Id</th><th>Matches</th><th>P-value</th></tr>"
    for x in f:
     x=x.rstrip()
     data = x.split("\t")
     feature = data[0].split(" = ")[1]
     matches = data[4].split(" = ")[1]
     pvalue = data[5].split(" = ")[1]
     htmlout += "<tr><td>" + feature + "</td><td>" + matches + "</td><td>" + pvalue + "</td></tr>"

    htmlout += "</table cellspacing=\"40\"></div></body></html>"
    return htmlout

print("<html><head> <style> td {padding: 30px;}</style></head><body><table>")
print("<tr><td>" + create_table("go_biological_process_output.txt", "GO Biological Process") + "</td> <td>" + create_table("go_molecular_function_output.txt", "GO Molecular Function") + "</td> <td>" + create_table("go_cellular_component_output.txt", "GO Cellular Component") + "</td></tr>")
print("<tr><td>" + create_table("kegg_enzyme_output.txt", "KEGG Enzyme") + "</td> <td>" + create_table("kog_output.txt", "KOG") + "</td> <td>" + create_table("panther_output.txt", "Panther") + "</td></tr>")
print("<tr><td>" + create_table("smart_output.txt", "SMART") + "</td> <td>" + create_table("pfam_output.txt", "PFAM") + "</td> <td>" + create_table("pathway_output.txt", "Pathway") + "</td></tr>")
print ("</table></body></html>")
