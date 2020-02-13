def get_id_from_phytozome(phytozome):
    id_phytozome_dict = {}
    #file = open('/kb/module/data/mapping.txt_file', 'r') 
    file = open ('/home/cades/kbase/branched_code/GeneSet_Enrichment/data/mapping_file.txt','r')
    reclines = file.readlines() 
  
    for line in reclines: 
       line = line.strip()
       arr = line.split("\t")
       id_phytozome_dict[arr[0]] = arr[1]

    return id_phytozome_dict[phytozome]   


print(get_id_from_phytozome("Athaliana_TAIR10"))
