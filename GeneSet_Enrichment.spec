/*
A KBase module: GeneSet_Enrichment
*/

module GeneSet_Enrichment {
    /* An X/Y/Z style reference
        @id ws
    */
    typedef string obj_ref; 
    typedef structure {
        string report_name;
        string report_ref;
    } ReportResults;

    typedef structure{
        string obj_name;
        string workspace_name; 
        list <string> genelist;   /*change it to featureset later*/
      } gseaparams;
 
    typedef structure{
        obj_ref genome; 
        string workspace_name;
        string genes;
        string description;
        string output_feature_set;
      } featuresetparams;
    
     
    typedef structure{
        obj_ref feature_set_ref;
        string report_name;
        string report_ref;
    } BuildFeatureSetResult;    
    
 
    /*
        This example function accepts any number of parameters and returns results in a KBaseReport
    */
    funcdef run_GeneSet_Enrichment(gseaparams params) returns (ReportResults output) authentication required;
    funcdef build_Featureset(featuresetparams params) returns (BuildFeatureSetResult output) authentication required; 
};
