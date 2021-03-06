# -*- coding: utf-8 -*-
"""BORUTA.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1HywjrFkxaUti4k3SvFeVcmZbcOwvRJbN
"""

# import pandas to work
import pandas as pd
# creating a dataframe
X = pd.DataFrame({'X1':[30, 52, 65, 57, 89,70],
                  'X2':[200,789,156,754,379,800],
                  'X3':[12,78,654,123,456,520]})
y = pd.Series([30,39,41,58,75,80], name="Income")

# use the join method to join X and y
print("Dataframe")
print(X.join(y))

# creating shadow features
import numpy as np
np.random.seed(42)
X_shadow = X.apply(np.random.permutation) 
X_shadow.columns = ['shadow_' + feat for feat in X.columns] # returns names of the shandow dataframe if printed
X_boruta = pd.concat([X,X_shadow], axis = 1)

# print shadow features
print(" ") # output spacing
print("Shadow features: ")
print(X_shadow)
# print X_boruta
print(" ")
print("Marged data")
print(X_boruta)

# FITTING A CLASSFIER

# RandomForestRegressor class from sklearn
from sklearn.ensemble import RandomForestRegressor
# create the rfr class object and specify max_depth, the number of trees used to make a prediction, as 5,
# set an internal state of 42 so that can be used to generate pseudo numbers.
forest = RandomForestRegressor(max_depth = 5, random_state=42)
# 
forest.fit(X_boruta, y) # uses the above specified internal state to fit model with 5 trees
# returns importance of each feature in X
feat_imp_X = forest.feature_importances_[:len(X.columns)] 
# returns importance of each feature in X_shandow
feat_imp_shadow = forest.feature_importances_[len(X.columns):]
# comparing feature importance
hits = feat_imp_X > feat_imp_shadow.max()
print(" ") # output spacing
print("#Feature Importance for X")
print(feat_imp_X)
print(" ") # output spacing
print("#Features importance for `X_shadow`")
print(feat_imp_shadow)

print(" ") # output spacing
print("Max Shadow: ",feat_imp_shadow.max())
print(" ") # output spacing
print("Hits:",hits)