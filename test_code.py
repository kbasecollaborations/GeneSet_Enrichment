import os
import uuid
outputdir = '/home/manish/Desktop/' + str(uuid.uuid1())
os.mkdir(outputdir)
for i in range(2): 
   geneset_dir = os.path.join(outputdir, "output"+ str(i))
   print("222222"+geneset_dir+"222222")
   os.mkdir(geneset_dir)
   print("333333"+geneset_dir+"333333")
