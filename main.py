import pandas as pd
import numpy as np
from Simulation import inventory_simulation
from runner import *
df_full = pd.read_excel(' https://archive.ics.uci.edu/ml/machine-learning-databases/00352/Online%20Retail.xlsx',dtype={'InvoiceNo':str,'StockCode':str,'Description':str,'Quantity':np.float32,'UnitPrice':np.float32,'CustomerID':str,'Country':str})


df_full.to_feather('OnlineRetail.feather')
df_full = pd.read_feather('OnlineRetail.feather')

totaldays = (np.max(df_full['InvoiceDate']) - np.min(df_full['InvoiceDate'])).days
stockcodeQty = df_full.groupby("StockCode").size()

stockcodeQty = pd.DataFrame(stockcodeQty).reset_index()
stockcodeQty.columns = ['StockCode','Count']

stockcodeQty.Count =stockcodeQty.Count/totaldays 

CustQty = df_full.groupby("CustomerID").size()

CustQty = pd.DataFrame(CustQty).reset_index()
CustQty.columns = ['CustomerID','Count']
CustQty.Count = CustQty.Count/totaldays
avg_customer_rate = np.mean(CustQty.Count)

stockcodeQty['ROL'] = [int(np.random.uniform(10,20)) for x in np.arange(0,len(stockcodeQty))]
stockcodeQty['ROQ'] =[int(np.random.uniform(30,60)) for x in np.arange(0,len(stockcodeQty))]

stockcodeQty = stockcodeQty.merge(df_full[['StockCode','UnitPrice']],how='left',left_on='StockCode',right_on='StockCode')

stockedQty2 = df_full.groupby("StockCode").agg({"Quantity":[np.mean,np.std]})
stockedQty2 = stockedQty2.reset_index()



stockcodeQty = stockcodeQty.drop_duplicates(subset=['StockCode'])
stockcodeQty = stockcodeQty.reset_index()
stockcodeQty['SellingPrice'] = stockcodeQty['UnitPrice']*3
stockcodeQty = stockcodeQty.merge(stockedQty2,how="left",left_on="StockCode",right_on="StockCode")
stockcodeQty.columns = ['index','StockCode','Count','ROL','ROQ','C.P','S.P','mean','std']
stockcodeQty = stockcodeQty.drop_duplicates(subset=['StockCode'])

def run_simulation_for_item(item:str,df:pd.DataFrame,customer_rate:float):
  ROL = df[df['StockCode']==item]['ROL'].values[0]
  ROQ = df[df['StockCode']==item]['ROQ'].values[0]
  CP = df[df['StockCode']==item]['C.P'].values[0]
  SP = df[df['StockCode']==item]['S.P'].values[0]
  mean = df[df['StockCode']==item]['mean'].values[0]
  std = df[df['StockCode']==item]['std'].values[0]
  s= inventory_simulation(simpy.Environment(),ROL,ROQ,CP,SP,customer_rate,mean,std)
  run(s,8)
  s.plot_inventory()
  #return ROQ
run_simulation_for_item('10002',stockcodeQty,avg_customer_rate)