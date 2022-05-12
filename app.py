# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 11:40:09 2022

@author: Andres Ardila

#COVID-19 Vaccinations in the United States,County ,Vacunas COVID-19 en los Estados Unidos, condado

https://data.cdc.gov/Vaccinations/COVID-19-Vaccinations-in-the-United-States-County/8xkx-amqh

Datos generales de administración de la vacuna COVID-19 de EE. UU. A nivel de condado. 
Los datos representan a todos los socios de vacunas, incluidas las clínicas asociadas jurisdiccionales, 
las farmacias minoristas, los centros de atención a largo plazo, los centros de diálisis, 
los sitios asociados de la Agencia Federal para el Manejo de Emergencias y la Administración de Recursos y Servicios de Salud,
 y las instalaciones de entidades federales.
"""

import matplotlib.pyplot as plt
#import numpy as np
import pandas  as pd
from datetime import datetime, timedelta
#import warnings
import seaborn as sns
#import plotly as py
#from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
#import plotly.graph_objs as go
#import plotly.express as px #libreria para vizualización

#%%%
db = 'https://media.githubusercontent.com/media/a2sandres/Visualizacion/main/muestra.csv'
#db = 'C:/Users/Andres/Desktop/maestria/S3/VAD/COVID-19_Vaccinations_in_the_United_States_County.csv'
#d_parse = lambda x : datetime.strptime(x, "%m/%d/%Y")
d_parse = lambda x : datetime.strptime(x, "%Y-%m-%d")
df = pd.read_csv(db, parse_dates=["Date"], date_parser = d_parse)  #  Leer y guardar el archivo el daataframe row_data
#print(df.head())
#%%
'''
df1 = df.sample(n=1000)
filename = 'C:/Users/Andres/Desktop/maestria/S3/VAD//muestra.csv'
df1.to_csv(filename, encoding='utf-8')
'''

#%%
#Alivianar DB

df['MMWR_week']=pd.to_numeric(df['MMWR_week'], downcast ='integer' , errors='coerce')
df['Series_Complete_Pop_Pct']=pd.to_numeric(df['Series_Complete_Pop_Pct'], downcast='float', errors='coerce')
df['Series_Complete_Yes']=pd.to_numeric(df['Series_Complete_Yes'], downcast='integer' , errors='coerce')
df['Series_Complete_12Plus']=pd.to_numeric(df['Series_Complete_12Plus'], downcast='integer' , errors='coerce')
df['Series_Complete_12PlusPop_Pct']=pd.to_numeric(df['Series_Complete_12PlusPop_Pct'], downcast='float' , errors='coerce')
df['Series_Complete_18Plus']=pd.to_numeric(df['Series_Complete_18Plus'], downcast='integer' , errors='coerce')
df['Series_Complete_18PlusPop_Pct']=pd.to_numeric(df['Series_Complete_12PlusPop_Pct'], downcast='float' , errors='coerce')
df['Series_Complete_65Plus']=pd.to_numeric(df['Series_Complete_18Plus'], downcast='integer' , errors='coerce')
df['Series_Complete_65PlusPop_Pct']=pd.to_numeric(df['Series_Complete_12PlusPop_Pct'], downcast='float' , errors='coerce')
df['Completeness_pct']=pd.to_numeric(df['Completeness_pct'], downcast='float', errors='coerce')


#%%
#Agrupar Datos
dfg=sns.PairGrid(df, hue="Recip_State", x_vars=['Series_Complete_Pop_Pct', 'Series_Complete_Yes'], y_vars=['Series_Complete_12PlusPop_Pct', 'Series_Complete_12Plus'])
dfg.map(plt.scatter)
##dfg.add_legend(); ## se comenta por la cantidad de lugares

#%%
#tabla pivote para grafica de calor
tvdf= df.pivot_table(values="Series_Complete_Yes", index= "Recip_State", columns= "MMWR_week")
plt.figure(figsize=(15,15)).add_axes([0,0,1,1])
sns.heatmap(tvdf, cmap= "Greens", linecolor= "w", linewidths= 1)

#%%
#variables categoricas barplot
plt.figure(figsize=(12,5))
sns.barplot(x="Recip_State",y="Series_Complete_Yes", data=df)
plt.xticks(rotation = 70);


#%%
#Grafica a partir de un filtro de texto barplot
filtro = df['Recip_State']=='CA'
dfca=df[filtro]
plt.figure(figsize=(15,5))
sns.barplot(x='MMWR_week',y='Series_Complete_Yes', data=dfca);
plt.xticks(rotation = -60);

