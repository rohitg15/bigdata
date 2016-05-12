import csv 
import pandas as pd 

data=pd.read_csv('ipfile.csv')
data.dropna().to_csv("opfile",float_format='%.f', index= False)