from collections import defaultdict
goannotation_dict = defaultdict(list)

go_count={}
f=open("210_go.gmt", "r")
for x in f:
  x=x.rstrip()
  id=x.split("\t")
  key = id[1]
  length = len(id)
  for i in range(3,length):
      go_count[id[i]]=1    
  goannotation_dict[key].append(id[i])
  #print (length)

N=len(go_count.keys())
print(goannotation_dict)
#print("N = "+str(N))
