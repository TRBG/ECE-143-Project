'''
Created on November 15 2019
@author : Yuchen Zhang
scatter plot of pH with temperature
'''
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(color_codes=True)
df1 = pd.read_csv("cleaned_data_of_the2000s.csv")
df1_0depth = df1[df1.Depth == 0] # only consider 0 depth
clear_df1 = df1_0depth[df1_0depth.pH!= None]
sns.regplot(x="Temperatur", y="pH", data=clear_df1,scatter_kws={'s':0.25})
plt.show()
