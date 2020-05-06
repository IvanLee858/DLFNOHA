import numpy as np
import pandas as pd
import json
from pandas.io.json import json_normalize
from pymatgen.core.structure import Structure
# Create an empty dataframe to record the "material_id", "lat_params" and "delta_e" of each material
df=pd.DataFrame(columns=["delta_e","material_id","structure"])
i=0
name=['a','b','c','alpha','beta','gamma']
with open("D:\db\db_lines.json","r+") as f:
    for line in f:
        data=json.loads(line)
        #print(data["lat_params"])
        #Select the data alloys with formation energy, and then write the information into the dataframe.
        if data["spacegroup"]==225 :#and np.isnan(data['delta_e'])==False: #and data["delta_e"]<1:
            #df.loc[i,"stability"]=data[key]['stability']
            df.loc[i,"delta_e"]=data["delta_e"]
            d=zip(name,data["lat_params"])
            if data["composition"][data["A"]]==2.0 :
                dict1={'lattice':dict(d),'sites':[{'label':data["A"],'abc':[0.0,0.0,0.0],'species':[{"occu":1,"element":data["A"]}],'properties':{'magmom':data["magmom"]}},{'label':data["A"],'abc':[0.500,0.500,0.500],'species':[{"occu":1,"element":data["A"]}],'properties':{"magmom":data["magmom"]}},{'label':data["B"],'abc':[0.250,0.250,0.250],'species':[{"occu":1,"element":data["B"]}],'properties':{'magmom':data["magmom"]}},{'label':data["C"],'abc':[0.750,0.750,0.750],'species':[{"occu":1,"element":data["C"]}],'properties':{'magmom':data["magmom"]}}]}
            elif data["composition"][data["B"]]==2.0 :
                dict1={'lattice':dict(d),'sites':[{'label':data["B"],'abc':[0.0,0.0,0.0],'species':[{"occu":1,"element":data["B"]}],'properties':{'magmom':data["magmom"]}},{'label':data["B"],'abc':[0.500,0.500,0.500],'species':[{"occu":1,"element":data["B"]}],'properties':{"magmom":data["magmom"]}},{'label':data["A"],'abc':[0.250,0.250,0.250],'species':[{"occu":1,"element":data["A"]}],'properties':{'magmom':data["magmom"]}},{'label':data["C"],'abc':[0.750,0.750,0.750],'species':[{"occu":1,"element":data["C"]}],'properties':{'magmom':data["magmom"]}}]}
            else :
                dict1={'lattice':dict(d),'sites':[{'label':data["C"],'abc':[0.0,0.0,0.0],'species':[{"occu":1,"element":data["C"]}],'properties':{'magmom':data["magmom"]}},{'label':data["C"],'abc':[0.500,0.500,0.500],'species':[{"occu":1,"element":data["C"]}],'properties':{"magmom":data["magmom"]}},{'label':data["B"],'abc':[0.250,0.250,0.250],'species':[{"occu":1,"element":data["B"]}],'properties':{'magmom':data["magmom"]}},{'label':data["A"],'abc':[0.750,0.750,0.750],'species':[{"occu":1,"element":data["A"]}],'properties':{'magmom':data["magmom"]}}]}
            df.loc[i,"structure"]=Structure.from_dict(dict1)
            df.loc[i,"material_id"]=data["material_id"]
            i+=1
df["delta_e"].astype('float64').hist(bins=50)
import seaborn as sns
sns.set(style="whitegrid")
ax = sns.violinplot(y=df["delta_e"].astype('float64'))
from matminer.featurizers.base import MultipleFeaturizer
from matminer.featurizers.structure import (SiteStatsFingerprint, StructuralHeterogeneity, ChemicalOrdering, StructureComposition, MaximumPackingEfficiency)
from matminer.featurizers.composition import ElementProperty, Stoichiometry, ValenceOrbital, IonProperty
from matminer.featurizers.site import CoordinationNumber,LocalPropertyDifference
from matminer.utils.data import MagpieData

element_properties=('Electronegativity','Row','Column','Number','MendeleevNumber','AtomicWeight','CovalentRadius','MeltingT',
         'NsValence','NpValence','NdValence','NfValence','NValence','NsUnfilled','NpUnfilled','NdUnfilled','NfUnfilled',
         'NUnfilled','GSvolume_pa','SpaceGroupNumber','GSbandgap','GSmagmom')

#The following features will be created by using matminer package.
featurizer = MultipleFeaturizer([
    SiteStatsFingerprint(CoordinationNumber().from_preset('VoronoiNN'),stats=('mean','std_dev','minimum','maximum')),
    StructuralHeterogeneity(),
    ChemicalOrdering(),
    MaximumPackingEfficiency(),
    SiteStatsFingerprint(LocalPropertyDifference(properties=element_properties),stats=('mean','std_dev','minimum','maximum','range')),
    StructureComposition(Stoichiometry()),
    StructureComposition(ElementProperty.from_preset("magpie")),
    StructureComposition(ValenceOrbital(props=['frac'])),
    StructureComposition(IonProperty(fast=True))    
])

#Generate VT based features from the material's crystal lat_params.
feature_data=featurizer.featurize_dataframe(df,col_id=['structure'],ignore_errors=True)
#"lat_params","compound possible" and "material_id" are not resonable physical features, so we drop these three columns
feature_data=feature_data.drop(["structure","compound possible","material_id"],axis=1)
#write the data into a csv file for later use
feature_data.to_csv("data_delta_e_data.csv",index=False)
from sklearn.model_selection import KFold,cross_val_score
from sklearn.model_selection import train_test_split,KFold,ShuffleSplit
from sklearn.ensemble import RandomForestRegressor,GradientBoostingRegressor
data_df=pd.read_csv("data_delta_e_data.csv")
#fill the NaN with the mean value of the corresponding column
data_df=data_df.fillna(data_df.mean())
y=data_df["delta_e"].values
X=data_df.drop(["delta_e"],axis=1).values
#75% of data is used for training, the rest is for testing.
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.25,random_state=1)
lr=GradientBoostingRegressor(n_estimators=700,random_state=1,max_depth=5)
#use 5-fold cross-validation approach to find the best model parameters
cv=ShuffleSplit(n_splits=5,test_size=0.2,random_state=1)
scores=cross_val_score(lr,X_train,y_train,cv=cv,scoring="neg_mean_absolute_error")
print("scores:  ",str(-np.mean(scores)))
lr.fit(X_train,y_train)
y_pred=lr.predict(X_test)
#calculate and print test error
print("MAE:  ",np.mean(abs(y_pred-y_test)))
import matplotlib.pyplot as plt
#%matplotlib inline

x1=np.linspace(-100,9,100)
plt.figure(figsize=(8,8))
plt.scatter(y_test,y_pred)
plt.xlim([-3,3])
plt.ylim([-3,3])
plt.xticks([-3,-2,-1,0,1,2,3],fontsize=20)
plt.yticks([-3,-2,-1,0,1,2,3],fontsize=20)
plt.xlabel("y_test_true",fontsize=20)
plt.ylabel("y_test_prediction",fontsize=20)
plt.gca().set_aspect('equal', adjustable='box')
plt.plot(x1,x1,c='k',lw=3)
plt.show()
#Define a function to plot the relative feature importance
def plot_feature_importances(feature_importances,title,feature_names):
   feature_importances=100.0*(feature_importances/max(feature_importances))
   index_sorted=np.flipud(np.argsort(feature_importances))[:5]
   pos=np.arange(index_sorted.shape[0])+0.5
   plt.figure(figsize=(9,9))
   plt.bar(pos,feature_importances[index_sorted],align="center")
   plt.xticks(pos,feature_names[index_sorted],fontsize=5)
   plt.yticks([0,20,40,60,80,100],fontsize=10)
   plt.ylabel("Relative importance",fontsize=20)
   plt.title(title,fontsize=20)
   plt.show()

#Sort the feature importance in descending order and call plot_feature_importance function to plot them.
features=data_df.drop(["delta_e"],axis=1).columns.values
importances=lr.feature_importances_
indices = np.argsort(importances)[::-1]
plot_feature_importances(importances,"Gradientboosting rgegression",features)
