/*
A KBase module: GeneSet_Enrichment
*/

module GeneSet_Enrichment {
    typedef structure {
        string report_name;
        string report_ref;
    } ReportResults;

    typedef structure{
        string obj_name;
        string workspace_name; 
        string genelist;
      } gseaparams;
 
    /*
        This example function accepts any number of parameters and returns results in a KBaseReport
    */
    funcdef run_GeneSet_Enrichment(gseaparams params) returns (ReportResults output) authentication required;

};
