# -*- coding: utf-8 -*-
"""
Spyder Editor

"""
import interop.core as ic
import pandas as pd
import os
import glob
from datetime import datetime
import easygui

filepath=easygui.diropenbox(title='Choose exported folder')
def parse(location):
    
    # summary function values
    # array(['Cluster Count', 'Cluster Count Pf', 'Error Rate', 'First Cycle Intensity', '% Aligned',
    # '% >= Q30','Projected Yield G', 'Yield G'], dtype=object)
    
    col_names_summary=['% >= Q30','Error Rate', '% Aligned','Yield G','Reads', 'Reads Pf']
    summary=ic.summary(location,columns=col_names_summary)
    df=pd.DataFrame(summary)
    df[['Reads']]=df[['Reads']].div(10**6)
    df[['Reads Pf']]=df[['Reads Pf']].div(10**6)
    
    #summary_lane values
    # # array(['ReadNumber', 'IsIndex', 'Lane', 'Cluster Count',
    #        'Cluster Count Pf', 'Density', 'Density Pf', 'Error Rate',
    #        'Error Rate 100', 'Error Rate 35', 'Error Rate 50',
    #        'Error Rate 75', 'First Cycle Intensity', '% Aligned', '% >= Q30',
    #        '% Pf', 'Phasing', 'Prephasing', 'Projected Yield G', 'Reads',
    #        'Reads Pf', 'Tile Count', 'Yield G']
    
    col_names_lane=['Density', 'Density Pf','% Pf','Tile Count']
    summary_lane=ic.summary(location,"Lane",columns=col_names_lane)
    df_lane=pd.DataFrame(summary_lane).iloc[:1]
    df_lane=df_lane[['Density','% Pf','Tile Count']]
    df_lane[['Density']]=df_lane[['Density']].div(1000)
    
    one_summary=pd.concat([df,df_lane], axis=1, join="outer")    
    #summary_index values
    # #array(['Lane', 'Mapped Reads Cv', 'Max Mapped Reads', 'Min Mapped Reads',
    #        'Total Fraction Mapped Reads', 'Total Pf Reads', 'Total Reads']
    index=ic.index_summary(location,level='Barcode')
    
    if len(index)!=0:
        index_df=pd.DataFrame(index)
        index_df=index_df.query("Lane==1")
        sample_count=len(index_df)
        
        col_names_index=['Mapped Reads Cv','Total Fraction Mapped Reads']
        summary_index=ic.index_summary(location,columns=col_names_index)
        df_index=pd.DataFrame(summary_index)
        df_index=df_index.head(1)
        df_index=df_index.drop(['Lane'],axis=1)
        df_index["Sample count"]=sample_count
        
        one_summary=pd.concat([df,df_lane,df_index], axis=1, join="outer")
    
    else:
        one_summary=pd.concat([df,df_lane], axis=1, join="outer")
        one_summary["Mapped Reads Cv"]=""
        one_summary["Total Fraction Mapped Reads"]=""
        one_summary["Sample count"]=""
    
    cycle=max(ic.imaging(location)['Cycle Within Read'])
    one_summary['Cycles']=cycle
    
    return one_summary


list=glob.glob(filepath+"/**/[0-9]*_*_*_*",recursive=True)
list=[x for x in list if os.path.isdir(x)]

database=pd.DataFrame()
counter=0
error_counter=0

for path in list:
    try:
        run_name=os.path.basename(path)
        date=run_name.split("_")[0]
        date="/".join(([date[i:i+2] for i in range(0, len(date), 2)]))
        
        path_data=parse(path)
        
        path_data['Run Name']=run_name
        path_data['Run Date']=date
    
        if len(database)==0:
            database=path_data
        else:
            database=pd.concat([database,path_data])
            
    except Exception as error:
        print(f"Error for {run_name} with error {error}")
        error_counter+=1
        counter+=1
        continue
    
    counter+=1
    print(f"{run_name} has been processed {counter}/{len(list)}")
    

database['Reads PF and Average % >= Q30']=database['Reads Pf'].multiply(database["% >= Q30"]/100)
database['Yield Total Average % >= Q30']=database['Yield G'].multiply(database["% >= Q30"]/100)
database['Final sample Yield Total Average % >= Q30 (GB) - PhiX']=database['Yield Total Average % >= Q30']*((100-database['% Aligned'])/100)

col_list=['Run Date','Run Name','Cycles','Tile Count','Density','% >= Q30','% Pf','Reads','Reads Pf','Total Fraction Mapped Reads','Reads PF and Average % >= Q30','Yield G','Yield Total Average % >= Q30', 'Final sample Yield Total Average % >= Q30 (GB) - PhiX','Sample count','Mapped Reads Cv','Error Rate','% Aligned']
database=database[col_list]

now=str(datetime.now())
now=now.split(".")[0]
now=now.replace(":","")

filename=str("database_"+now+".xlsx")
database.to_excel(filename,index=False)
print(f"{filename} exported successfully, with {error_counter} errors")




