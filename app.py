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
import numpy as np
import pandas  as pd
from datetime import datetime, timedelta
import warnings
import seaborn as sns
import plotly as py
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly.graph_objs as go
import plotly.express as px #libreria para vizualización

#%%%
db = 'https://media.githubusercontent.com/media/a2sandres/Visualizacion/main/muestra.csv'
#db = 'C:/Users/Andres/Desktop/maestria/S3/VAD/COVID-19_Vaccinations_in_the_United_States_County.csv'
d_parse = lambda x : datetime.strptime(x, "%m/%d/%Y")
df = pd.read_csv(db, parse_dates=["Date"], date_parser = d_parse)  #  Leer y guardar el archivo el daataframe row_data
print(df.head())
#%%

#df1 = df.sample(n=10000)
#filename = 'C:/Users/Andres/Desktop/maestria/S3/VAD//muestra.csv'
#df1.to_csv(filename)

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
#(df.describe(include = 'all'))
print(df.info())
print(df.describe())

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
#stripplot
plt.figure(figsize=(15,10))
sns.stripplot(x='Recip_State',y='Series_Complete_Yes', data=df, hue='MMWR_week')
plt.xticks(rotation = -45);

#%%
#correlacion pairplot
df1= df[1000:2000]
sns.pairplot(df1)

#%%
#Grafica comportamiento frente a tiempo barras, lineas, colores y grids
NVD=df.groupby(["Date"])[["Series_Complete_Yes"]].sum()
NVD["Date"]= NVD.index
NVD['MA'] = NVD.rolling(window=3).mean()
NVD
datos = NVD.values
u= datos[:,1]
v= datos[:,0]
w= datos[:,2]

plt.figure(figsize=(15,5)).add_axes([0,0,1,1]).set_title('Vacunas', fontsize=16)
plt.plot(u,w, c='k', label= 'Promedio 3 Dias', lw=3)
plt.bar(u,v, color='grey', label= 'Vacundos', alpha=0.5, width=1)
plt.legend(ncol=2)
plt.grid(axis='y', alpha=0.5)
plt.show();

#%%
#varias graficas en una sola grupos de edades
NVD12=df.groupby(["Date"])[["Series_Complete_12Plus"]].sum()
NVD12["Date"]= NVD12.index
NVD18=df.groupby(["Date"])[["Series_Complete_18Plus"]].sum()
NVD18["Date"]= NVD18.index
NVD65=df.groupby(["Date"])[["Series_Complete_65Plus"]].sum()
NVD65["Date"]= NVD65.index
datos1 = NVD12.values
datos2 = NVD18.values
datos3 = NVD65.values
x= datos1[:,1]
y= datos1[:,0]
z= datos2[:,1]
r= datos2[:,0]
s= datos3[:,1]
t= datos3[:,0]

plt.figure(figsize=(20,7)).add_axes([0,0,1,1]).set_title('Vacunados por grupo de edades', fontsize=16)
plt.plot(x,y, c='purple', label= '12+')
plt.plot(z,r, c='g', label= '18+')
plt.plot(s,t, c='k', label= '65+')
plt.bar(u,v, color='grey', label= 'Vacunados', alpha=0.5, width=1)
plt.legend(loc= 2)
plt.show();

#%%
#Grafica a partir de un filtro de texto barplot
filtro = df['Recip_State']=='CA'
dfca=df[filtro]
plt.figure(figsize=(15,5))
sns.barplot(x='MMWR_week',y='Series_Complete_Yes', data=dfca);
plt.xticks(rotation = -60);

#%%
#Datos en un mapa
df3=df.groupby(["Recip_State"])[["Series_Complete_Yes"]].sum()
df3["Recip_State"]= df3.index

data = dict(type = "choropleth",
            colorscale = "Greens_r",
            z = df3["Series_Complete_Yes"],
            locations = df3["Recip_State"],
            locationmode = "USA-states",
            text = df3["Recip_State"],           
            colorbar ={"title":"$"},
            marker = dict(line = dict(color = "rgb(255,255,255)", width = 1))
            )

layout = dict(title= "Vacunas Covid 19 USA 2022", geo = {"scope":"usa"})
choromap = go.Figure(data= [data], layout= layout)
choromap.show()