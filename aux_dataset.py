#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 19 18:31:51 2020

@author: margaritavenediktova
"""
# THIS SCRIPT CREATES A TOY DATAFRAME BASED ON THE ORIGINAL CLAIMS_TEST.CSV FOR FURTHER TESTING IN TASK2_DASHBOARD.PY

import pandas as pd
from datetime import datetime
from time import strptime
import itertools

# please provide path for the original claims_test.csv on your pc
path='/Users/margaritavenediktova/Desktop/claims_test.csv'
 
df=pd.read_csv(path).rename(columns=lambda x: x.lower())

df['month']=[201812 if str(x)=='201900' else x for x in df['month']]
df['date']=[datetime.strptime(str(x), "%Y%m").date() for x in df['month']]
df['month']=[x.strftime("%B") for x in df['date']]
df['year']=[datetime.strptime(str(x), "%Y-%m-%d").date().year for x in df['date']]

for i in range(len(df)):
        df.loc[i,'month']=strptime(df.loc[i,'month'][:3],'%b').tm_mon

df['claim_specialty']=[x.lower()  if type(x)==str else x for x in df['claim_specialty'] ]

df.loc[df['claim_specialty'].isnull()==True,'claim_specialty']='error'
df=df.sort_values(by='claim_specialty', ignore_index=True)

df.drop(columns=['date'], inplace=True)

               
payers=['Payer F','Payer CA']

claims_f=df[df['payer']=='Payer F']['claim_specialty'].unique()
claims_ca=df[df['payer']=='Payer CA']['claim_specialty'].unique()
claims= list(set(claims_f)& set(claims_ca))


service= df['service_category'].unique()
months= df['month'].unique()
year= df['year'].unique()


x=df[(df['claim_specialty'].isin(claims))&(df['service_category'].isin(service))&(df['payer'].isin(payers))]


# creating zero paid_amount rows for all the combinations of service categories and payers 
a=[claims,payers,service,months,year]
z=list(itertools.product(*a))


for i in range(len(z)):
    if x[(x['claim_specialty']==z[i][0])&(x['payer']==z[i][1])&(x['service_category']==z[i][2])&(x['month']==z[i][3])&(x['year']==z[i][4])].empty==True:
        temp=pd.DataFrame({'month': z[i][3], 'service_category':z[i][2],'claim_specialty':z[i][0],'payer':z[i][1],'paid_amount':0,'year':z[i][4]}, index=[i])
        x=x.append(temp)

# here the toy dataframe is saved 
# you can find this file in zip folder
#x.to_excel('../../Desktop/data/df_dashboard.xlsx')





