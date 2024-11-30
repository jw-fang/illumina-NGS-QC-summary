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

easygui.msgbox("README: \n\n3 prompts will be shown for you to select the types of QC paramaters that you are interested in")

sum_list=['Cluster Count', 'Cluster Count Pf', 'Error Rate', 
          'First Cycle Intensity', '% Aligned', '% >= Q30',
          'Projected Yield G', 'Yield G']
lane_list=['% >= Q30', '% Aligned', '% Occupied', '% Pf', 'Cluster Count', 
           'Cluster Count Pf', 'Density', 'Density Pf', 'Error Rate', 
           'Error Rate 100', 'Error Rate 35', 'Error Rate 50', 
           'Error Rate 75', 'First Cycle Intensity', 'Phasing', 
           'Phasing Offset', 'Phasing Slope', 'Prephasing', 
           'Prephasing Offset', 'Prephasing Slope', 'Projected Yield G', 
           'Reads', 'Reads Pf', 'Tile Count', 'Yield G']
index_list=['Mapped Reads Cv', 'Max Mapped Reads', 'Min Mapped Reads',
            'Total Fraction Mapped Reads', 'Total Pf Reads', 'Total Reads']

selected_sum = easygui.multchoicebox("Prompt 1: Select the required paramters", 
                             "Prompt 1", 
                             sum_list,preselect=range(len(sum_list))
                             )
selected_lane=easygui.multchoicebox("Prompt 2: Select the required paramters", 
                             "Prompt 2", 
                             lane_list,preselect=range(len(lane_list))
                             )
selected_index=easygui.multchoicebox("Prompt 3: Select the required paramters", 
                             "Prompt 3", 
                             index_list,preselect=range(len(index_list))
                             )

def parse(location,sum_s,lane_s,index_s):
    
    col_names_summary=sum_s
    summary=ic.summary(location,columns=col_names_summary)
    df=pd.DataFrame(summary)
    
    col_names_lane=lane_s
    summary_lane=ic.summary(location,"Lane",columns=col_names_lane)
    df_lane=pd.DataFrame(summary_lane).iloc[:1]
    df_lane=df_lane.drop(df_lane.iloc[:,:3],axis=1)
    df_lane=df_lane.add_suffix("_lane")

    
    index=ic.index_summary(location,level='Barcode')
    if len(index)!=0:
        index_df=pd.DataFrame(index)
        index_df=index_df.query("Lane==1")
        sample_count=len(index_df)
        
        col_names_index=index_s
        summary_index=ic.index_summary(location,columns=col_names_index)
        df_index=pd.DataFrame(summary_index)
        df_index=df_index.head(1)
        df_index=df_index.drop(['Lane'],axis=1)
        df_index["Sample count"]=sample_count
        
        one_summary=pd.concat([df,df_index,df_lane], axis=1, join="outer")
    
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
database_n=0

for path in list:
    # try:
    path_data=pd.DataFrame()
    run_name=os.path.basename(path)
    date=run_name.split("_")[0]
    date="/".join(([date[i:i+2] for i in range(0, len(date), 2)]))

    path_data=parse(path,selected_sum,selected_lane,selected_index)
    path_data.insert(0,'Run Name',run_name)
    path_data.insert(1,'Run Date',date)
    
    database_n=len(database.columns)
    
    if len(database)==0:
        database=path_data
        
    elif database_n !=len(path_data.columns):
        data_names=database.columns.tolist()
        path_names=path_data.columns.tolist()
        
        if database_n >= len(path_names):
            difference=set(data_names)-set(path_names)
            for x in difference:
                path_data[x]="N/A"
        else:
            difference=set(path_names)-set(data_names)
            for x in difference:
                database[x]="N/A"
        
        data_names=database.columns.tolist()
        database=pd.concat([database,path_data])
        
    else:
        database=pd.concat([database,path_data])
            
    except Exception as error:
        print(f"Error for {run_name} with error {error}")
        error_counter+=1
        counter+=1
        continue
    
    counter+=1
    print(f"{run_name} has been processed {counter}/{len(list)}")

now=str(datetime.now())
now=now.split(".")[0]
now=now.replace(":","")

filename=str("database_"+now+".xlsx")
database.to_excel(filename,index=False)
print(f"{filename} exported successfully, with {error_counter} errors")




