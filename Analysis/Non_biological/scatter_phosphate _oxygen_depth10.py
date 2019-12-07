'''
Created on November 15 2019
@author : Yuchen Zhang
plot scatter of phosphate vs oxygen with 10 depth
'''
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
#using the cleaned data of 2000s
df1 = pd.read_csv("cleaned_data_of_the2000s.csv")
df1_0depth = df1[df1.Depth == 10]
clear_df1 = df1_0depth[df1_0depth.Phosphate!=None]
sns.regplot(x="Oxygen", y="Phosphate", data=clear_df1,scatter_kws={'s':0.1}) #plot the scattering with phosphate vs oxygen
plt.show()


