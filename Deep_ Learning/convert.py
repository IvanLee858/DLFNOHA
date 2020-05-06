'''
import csv
import pandas as pd

cFile = open("C:/Users/96913/cgcnn-master/test_results.csv",'r')
reader = csv.reader(cFile)
i=0

for i,item in enumerate(reader):
    if item[2]!=0:
         a=item[2][:4]
         print(a)
         i+=1
         
#df=pd.DataFrame(columns=["a"])
#i=0
with open('C:/Users/96913/cgcnn-master/test_results.csv','r')as f:
   a=csv.reader(f)
   for i, row in enumerate(a):
      if(len(row) < 1):
         continue
      data=row[2]
      print (data)
'''
import numpy as np
import pandas as pd
import json
from pandas.io.json import json_normalize
from pymatgen.core.structure import Structure
df=pd.DataFrame(columns=["stability","id"])
i=0
with open("D:\db\db_lines.json","r+") as f:
    for line in f:
        data=json.loads(line)
        #print(data["lat_params"])
        #Select the data alloys with formation energy, and then write the information into the dataframe.
        if data["spacegroup"]==225 :#and np.isnan(data['delta_e'])==False: #and data["delta_e"]<1:
            #df.loc[i,"stability"]=data[key]['stability']
            df.loc[i,"stability"]=data["stability"]
            df.loc[i,"id"]=data["id"]
            i+=1
    df.to_csv("heus_stability.csv")
