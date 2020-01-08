/*
A KBase module: GeneSet_Enrichment
*/

module GeneSet_Enrichment {
    typedef structure {
        string report_name;
        string report_ref;
    } ReportResults;

    /*
        This example function accepts any number of parameters and returns results in a KBaseReport
    */
    funcdef run_GeneSet_Enrichment(mapping<string,UnspecifiedObject> params) returns (ReportResults output) authentication required;

};
