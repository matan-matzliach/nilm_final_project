import pandas as pd
from dateutil.relativedelta import relativedelta
import sys
import os
import csv
import numpy as np
import matplotlib.pyplot as plt
import math
import time
import datetime as dt
import matplotlib
matplotlib.use('Agg')
import matplotlib.dates as md
from flask import Flask,request,render_template,Response,send_file,jsonify
import random
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import threading
from OpenSSL import SSL


def csvToDict(relative_path):
    #converts csv file to matrix
    table=dict()
    num_to_header=dict()
    if(not(os.path.exists(os.path.abspath(relative_path)))):
        print("ERROR, can't read: "+os.path.abspath(relative_path))
    else:
        with open(os.path.abspath(relative_path), 'rt') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                header=row
                break
            i=0
            for head in header:
                if("DoubleTime" in head):
                    table["DoubleTime"]=list()
                    num_to_header[i]="DoubleTime"
                else:
                    table[head]=list()
                    num_to_header[i]=str(head)
                i+=1
            for row in reader: #second line does has data that does not match the real values
                break
            for row in reader:
                for i in range(len(row)):
                    if(num_to_header[i]=="StringTime"):
                        table[num_to_header[i]].append(str(row[i]))
                    else:
                        if(str(row[i])==""):
                            table[num_to_header[i]].append(0.0) #appears in ./forthSession/aircoditionMW/low/output2/table2.csv
                        else:
                            table[num_to_header[i]].append(float(row[i]))
        csvfile.close()
    return table


def add_tables_to_dict(prefix_str,relative_path,dictionary):
    output_arr=["1","2","3"]
    table_arr=["1","2","3","4"]
    for output in output_arr:
        for table in table_arr:
            if((os.path.exists(os.path.abspath(relative_path+output+"/table"+table+".csv")))):
                dictionary[prefix_str+"_output"+output+"_table"+table]=csvToDict(relative_path+output+"/table"+table+".csv")
            
    
    prefixlist.append(prefix_str)


def parse_all_data(dictionary,dictionary_2):
    #first_session
    add_tables_to_dict("s1_alloff","./firstSession/alloff/low/output",dictionary)
    add_tables_to_dict("s1_alloffwithairconditionoutsideofbsharasroom","./firstSession/alloffwithairconditionoutsideofbsharasroom/low/output",dictionary)
    add_tables_to_dict("s1_allofwithbsharasaircondition","./firstSession/allofwithbsharasaircondition/low/output",dictionary)
    add_tables_to_dict("s1_bsharamorning","./firstSession/bsharamorning/low/output",dictionary)
    add_tables_to_dict("s1_twolight","./firstSession/twolight/low/output",dictionary)
    #second_session
    add_tables_to_dict("s2_alllights","./secondSession/alllights/low/output",dictionary)
    add_tables_to_dict("s2_alloff","./secondSession/alloff/low/output",dictionary)
    add_tables_to_dict("s2_kettle","./secondSession/kettle/low/output",dictionary)
    add_tables_to_dict("s2_mw","./secondSession/mw/low/output",dictionary)
    add_tables_to_dict("s2_runninglabwithbasharaaircondition","./secondSession/runninglabwithbasharaaircondition/low/output",dictionary)
    #third_session
    add_tables_to_dict("s3_alloff","./thirdSession/alloff/low/output",dictionary)
    add_tables_to_dict("s3_alloffAirConditiokettle","./thirdSession/alloffAirConditiokettle/low/output",dictionary)
    add_tables_to_dict("s3_alloffairconditiononelight","./thirdSession/alloffairconditiononelight/low/output",dictionary)
    add_tables_to_dict("s3_alloffwithairconditionTwoLight","./thirdSession/alloffwithairconditionTwoLight/low/output",dictionary)
    add_tables_to_dict("s3_alloffwithairconditioOutsideBasharaRoom","./thirdSession/alloffwithairconditioOutsideBasharaRoom/low/output",dictionary)
    add_tables_to_dict("s3_alloffwithkettle","./thirdSession/alloffwithkettle/low/output",dictionary)
    add_tables_to_dict("s3_onelight","./thirdSession/onelight/low/output",dictionary)
    add_tables_to_dict("s3_secondlight","./thirdSession/secondlight/low/output",dictionary)
    #forth_session
    add_tables_to_dict("s4_2bashsarsComputers","./forthSession/2bashsarsComputers/lowfreq/output",dictionary)
    add_tables_to_dict("s4_aircoditionMW","./forthSession/aircoditionMW/low/output",dictionary)
    add_tables_to_dict("s4_airconditionAndkettleandlight","./forthSession/airconditionAndkettleandlight/low/output",dictionary)
    add_tables_to_dict("s4_alloff","./forthSession/alloff/low/output",dictionary)
    add_tables_to_dict("s4_alloffAircon","./forthSession/alloffAircon/low/output",dictionary)
    add_tables_to_dict("s4_alloffonelight","./forthSession/alloffonelight/low/output",dictionary)
    add_tables_to_dict("s4_kettelandlight","./forthSession/kettelandlight/low/output",dictionary)
    add_tables_to_dict("s4_mw","./forthSession/mw/low/output",dictionary)
    add_tables_to_dict("s4_onelightAndAircondi","./forthSession/onelightAndAircondi/low/output",dictionary)
    add_tables_to_dict("s4_twolightandAirco","./forthSession/twolightandAirco/low/output",dictionary)
    
    
    #full_2_days
    add_tables_to_dict("Administrato","./satec_samples/",dictionary_2)
    
    

def diff_all_data(dictionary,difdictionary,prefixlist):
    for i in range(len(prefixlist)):
        for j in prefixlist[i:]:
            print(prefixlist[i]+" and "+j)
            index1,index2=sync_voltage(prefixlist[i]+"_V1",j+"_V1",64)
            difdictionary[prefixlist[i]+"_V1 - "+j+"_V1"]=find_difference_between_Data_in_tabels(prefixlist[i]+"_V1",j+"_V1",64,index1,index2)
            sumdictionary[prefixlist[i]+"_V1 + "+j+"_V1"]=find_sum_of_Data_in_tabels(prefixlist[i]+"_V1",j+"_V1",64,index1,index2)
            difdictionary[prefixlist[i]+"_I1 - "+j+"_I1"]=find_difference_between_Data_in_tabels(prefixlist[i]+"_I1",j+"_I1",64,index1,index2)
            sumdictionary[prefixlist[i]+"_I1 + "+j+"_I1"]=find_sum_of_Data_in_tabels(prefixlist[i]+"_I1",j+"_I1",64,index1,index2)
            difdictionary[prefixlist[i]+"_P1 - "+j+"_P1"]=find_difference_between_Data_in_tabels(prefixlist[i]+"_P1",j+"_P1",64,index1,index2)
            sumdictionary[prefixlist[i]+"_P1 + "+j+"_P1"]=find_sum_of_Data_in_tabels(prefixlist[i]+"_P1",j+"_P1",64,index1,index2)
            difdictionary[j+"_V1 - "+prefixlist[i]+"_V1"]=[-i for i in difdictionary[prefixlist[i]+"_V1 - "+j+"_V1"]]
            sumdictionary[j+"_V1 - "+prefixlist[i]+"_V1"]=sumdictionary[prefixlist[i]+"_V1 + "+j+"_V1"]
            difdictionary[j+"_I1 - "+prefixlist[i]+"_I1"]=[-i for i in difdictionary[prefixlist[i]+"_I1 - "+j+"_I1"]]
            sumdictionary[j+"_I1 - "+prefixlist[i]+"_I1"]=sumdictionary[prefixlist[i]+"_I1 + "+j+"_I1"]
            difdictionary[j+"_P1 - "+prefixlist[i]+"_P1"]=[-i for i in difdictionary[prefixlist[i]+"_P1 - "+j+"_P1"]]
            sumdictionary[j+"_P1 + "+prefixlist[i]+"_P1"]=sumdictionary[prefixlist[i]+"_P1 + "+j+"_P1"]
            index1,index2=sync_voltage(prefixlist[i]+"_V1",j+"_V2",64)
            difdictionary[prefixlist[i]+"_V1 - "+j+"_V2"]=find_difference_between_Data_in_tabels(prefixlist[i]+"_V1",j+"_V2",64,index1,index2)
            sumdictionary[prefixlist[i]+"_V1 + "+j+"_V2"]=find_sum_of_Data_in_tabels(prefixlist[i]+"_V1",j+"_V2",64,index1,index2)
            difdictionary[prefixlist[i]+"_I1 - "+j+"_I2"]=find_difference_between_Data_in_tabels(prefixlist[i]+"_I1",j+"_I2",64,index1,index2)
            sumdictionary[prefixlist[i]+"_I1 + "+j+"_I2"]=find_sum_of_Data_in_tabels(prefixlist[i]+"_I1",j+"_I2",64,index1,index2)
            difdictionary[prefixlist[i]+"_P1 - "+j+"_P2"]=find_difference_between_Data_in_tabels(prefixlist[i]+"_P1",j+"_P2",64,index1,index2)
            sumdictionary[prefixlist[i]+"_P1 + "+j+"_P2"]=find_sum_of_Data_in_tabels(prefixlist[i]+"_P1",j+"_P2",64,index1,index2)
            difdictionary[j+"_V1 - "+prefixlist[i]+"_V2"]=[-i for i in difdictionary[prefixlist[i]+"_V1 - "+j+"_V2"]]
            sumdictionary[j+"_V1 - "+prefixlist[i]+"_V2"]=sumdictionary[prefixlist[i]+"_V1 + "+j+"_V2"]
            difdictionary[j+"_I1 - "+prefixlist[i]+"_I2"]=[-i for i in difdictionary[prefixlist[i]+"_I1 - "+j+"_I2"]]
            sumdictionary[j+"_I1 - "+prefixlist[i]+"_I2"]=sumdictionary[prefixlist[i]+"_I1 + "+j+"_I2"]
            difdictionary[j+"_P1 - "+prefixlist[i]+"_P2"]=[-i for i in difdictionary[prefixlist[i]+"_P1 - "+j+"_P2"]]
            sumdictionary[j+"_P1 + "+prefixlist[i]+"_P2"]=sumdictionary[prefixlist[i]+"_P1 + "+j+"_P2"]
            index1,index2=sync_voltage(prefixlist[i]+"_V1",j+"_V3",64)
            difdictionary[prefixlist[i]+"_V1 - "+j+"_V3"]=find_difference_between_Data_in_tabels(prefixlist[i]+"_V1",j+"_V3",64,index1,index2)
            sumdictionary[prefixlist[i]+"_V1 + "+j+"_V3"]=find_sum_of_Data_in_tabels(prefixlist[i]+"_V1",j+"_V3",64,index1,index2)
            difdictionary[prefixlist[i]+"_I1 - "+j+"_I3"]=find_difference_between_Data_in_tabels(prefixlist[i]+"_I1",j+"_I3",64,index1,index2)
            sumdictionary[prefixlist[i]+"_I1 + "+j+"_I3"]=find_sum_of_Data_in_tabels(prefixlist[i]+"_I1",j+"_I3",64,index1,index2)
            difdictionary[prefixlist[i]+"_P1 - "+j+"_P3"]=find_difference_between_Data_in_tabels(prefixlist[i]+"_P1",j+"_P3",64,index1,index2)
            sumdictionary[prefixlist[i]+"_P1 + "+j+"_P3"]=find_sum_of_Data_in_tabels(prefixlist[i]+"_P1",j+"_P3",64,index1,index2)
            difdictionary[j+"_V1 - "+prefixlist[i]+"_V3"]=[-i for i in difdictionary[prefixlist[i]+"_V1 - "+j+"_V3"]]
            sumdictionary[j+"_V1 - "+prefixlist[i]+"_V3"]=sumdictionary[prefixlist[i]+"_V1 + "+j+"_V3"]
            difdictionary[j+"_I1 - "+prefixlist[i]+"_I3"]=[-i for i in difdictionary[prefixlist[i]+"_I1 - "+j+"_I3"]]
            sumdictionary[j+"_I1 - "+prefixlist[i]+"_I3"]=sumdictionary[prefixlist[i]+"_I1 + "+j+"_I3"]
            difdictionary[j+"_P1 - "+prefixlist[i]+"_P3"]=[-i for i in difdictionary[prefixlist[i]+"_P1 - "+j+"_P3"]]
            sumdictionary[j+"_P1 + "+prefixlist[i]+"_P3"]=sumdictionary[prefixlist[i]+"_P1 + "+j+"_P3"]
            index1,index2=sync_voltage(prefixlist[i]+"_V2",j+"_V2",64)
            difdictionary[prefixlist[i]+"_V2 - "+j+"_V2"]=find_difference_between_Data_in_tabels(prefixlist[i]+"_V2",j+"_V2",64,index1,index2)
            sumdictionary[prefixlist[i]+"_V2 + "+j+"_V2"]=find_sum_of_Data_in_tabels(prefixlist[i]+"_V2",j+"_V2",64,index1,index2)
            difdictionary[prefixlist[i]+"_I2 - "+j+"_I2"]=find_difference_between_Data_in_tabels(prefixlist[i]+"_I2",j+"_I2",64,index1,index2)
            sumdictionary[prefixlist[i]+"_I2 + "+j+"_I2"]=find_sum_of_Data_in_tabels(prefixlist[i]+"_I2",j+"_I2",64,index1,index2)
            difdictionary[prefixlist[i]+"_P2 - "+j+"_P2"]=find_difference_between_Data_in_tabels(prefixlist[i]+"_P2",j+"_P2",64,index1,index2)
            sumdictionary[prefixlist[i]+"_P2 + "+j+"_P2"]=find_sum_of_Data_in_tabels(prefixlist[i]+"_P2",j+"_P2",64,index1,index2)
            difdictionary[j+"_V2 - "+prefixlist[i]+"_V2"]=[-i for i in difdictionary[prefixlist[i]+"_V2 - "+j+"_V2"]]
            sumdictionary[j+"_V2 - "+prefixlist[i]+"_V2"]=sumdictionary[prefixlist[i]+"_V2 + "+j+"_V2"]
            difdictionary[j+"_I2 - "+prefixlist[i]+"_I2"]=[-i for i in difdictionary[prefixlist[i]+"_I2 - "+j+"_I2"]]
            sumdictionary[j+"_I2 - "+prefixlist[i]+"_I2"]=sumdictionary[prefixlist[i]+"_I2 + "+j+"_I2"]
            difdictionary[j+"_P2 - "+prefixlist[i]+"_P2"]=[-i for i in difdictionary[prefixlist[i]+"_P2 - "+j+"_P2"]]
            sumdictionary[j+"_P2 + "+prefixlist[i]+"_P2"]=sumdictionary[prefixlist[i]+"_P2 + "+j+"_P2"]
            index1,index2=sync_voltage(prefixlist[i]+"_V2",j+"_V3",64)
            difdictionary[prefixlist[i]+"_V2 - "+j+"_V3"]=find_difference_between_Data_in_tabels(prefixlist[i]+"_V2",j+"_V3",64,index1,index2)
            sumdictionary[prefixlist[i]+"_V2 + "+j+"_V3"]=find_sum_of_Data_in_tabels(prefixlist[i]+"_V2",j+"_V3",64,index1,index2)
            difdictionary[prefixlist[i]+"_I2 - "+j+"_I3"]=find_difference_between_Data_in_tabels(prefixlist[i]+"_I2",j+"_I3",64,index1,index2)
            sumdictionary[prefixlist[i]+"_I2 + "+j+"_I3"]=find_sum_of_Data_in_tabels(prefixlist[i]+"_I2",j+"_I3",64,index1,index2)
            difdictionary[prefixlist[i]+"_P2 - "+j+"_P3"]=find_difference_between_Data_in_tabels(prefixlist[i]+"_P2",j+"_P3",64,index1,index2)
            sumdictionary[prefixlist[i]+"_P2 + "+j+"_P3"]=find_sum_of_Data_in_tabels(prefixlist[i]+"_P2",j+"_P3",64,index1,index2)
            difdictionary[j+"_V2 - "+prefixlist[i]+"_V3"]=[-i for i in difdictionary[prefixlist[i]+"_V2 - "+j+"_V3"]]
            sumdictionary[j+"_V2 - "+prefixlist[i]+"_V3"]=sumdictionary[prefixlist[i]+"_V2 + "+j+"_V3"]
            difdictionary[j+"_I2 - "+prefixlist[i]+"_I3"]=[-i for i in difdictionary[prefixlist[i]+"_I2 - "+j+"_I3"]]
            sumdictionary[j+"_I2 - "+prefixlist[i]+"_I3"]=sumdictionary[prefixlist[i]+"_I2 + "+j+"_I3"]
            difdictionary[j+"_P2 - "+prefixlist[i]+"_P3"]=[-i for i in difdictionary[prefixlist[i]+"_P2 - "+j+"_P3"]]
            sumdictionary[j+"_P2 + "+prefixlist[i]+"_P3"]=sumdictionary[prefixlist[i]+"_P2 + "+j+"_P3"]
            index1,index2=sync_voltage(prefixlist[i]+"_V3",j+"_V3",64)
            difdictionary[prefixlist[i]+"_V3 - "+j+"_V3"]=find_difference_between_Data_in_tabels(prefixlist[i]+"_V3",j+"_V3",64,index1,index2)
            sumdictionary[prefixlist[i]+"_V3 + "+j+"_V3"]=find_sum_of_Data_in_tabels(prefixlist[i]+"_V3",j+"_V3",64,index1,index2)
            difdictionary[prefixlist[i]+"_I3 - "+j+"_I3"]=find_difference_between_Data_in_tabels(prefixlist[i]+"_I3",j+"_I3",64,index1,index2)
            sumdictionary[prefixlist[i]+"_I3 + "+j+"_I3"]=find_sum_of_Data_in_tabels(prefixlist[i]+"_I3",j+"_I3",64,index1,index2)
            difdictionary[prefixlist[i]+"_P3 - "+j+"_P3"]=find_difference_between_Data_in_tabels(prefixlist[i]+"_P3",j+"_P3",64,index1,index2)
            sumdictionary[prefixlist[i]+"_P3 + "+j+"_P3"]=find_sum_of_Data_in_tabels(prefixlist[i]+"_P3",j+"_P3",64,index1,index2)
            difdictionary[j+"_V3 - "+prefixlist[i]+"_V3"]=[-i for i in difdictionary[prefixlist[i]+"_V3 - "+j+"_V3"]]
            sumdictionary[j+"_V3 - "+prefixlist[i]+"_V3"]=sumdictionary[prefixlist[i]+"_V3 + "+j+"_V3"]
            difdictionary[j+"_I3 - "+prefixlist[i]+"_I3"]=[-i for i in difdictionary[prefixlist[i]+"_I3 - "+j+"_I3"]]
            sumdictionary[j+"_I3 - "+prefixlist[i]+"_I3"]=sumdictionary[prefixlist[i]+"_I3 + "+j+"_I3"]
            difdictionary[j+"_P3 - "+prefixlist[i]+"_P3"]=[-i for i in difdictionary[prefixlist[i]+"_P3 - "+j+"_P3"]]
            sumdictionary[j+"_P3 + "+prefixlist[i]+"_P3"]=sumdictionary[prefixlist[i]+"_P3 + "+j+"_P3"]
            
        

dictionary=dict()
dictionary_2days=dict()
prefixlist=[]
difdictionary=dict()
sumdictionary=dict()
def get_table_titles(table):
    return dictionary[table][0].keys()

def get_table_data(table):
    return dictionary[table]

def find_difference_between_Data_in_tabels(table1,table2,num_of_samples,index1,index2):#num_of_samples<=64
    l=[]
    adjusted_row1=dictionary[table1][0]['Data'][index1:index1+num_of_samples]
    adjusted_row2=dictionary[table2][0]['Data'][index2:index2+num_of_samples]
    for i in range(num_of_samples):
        l.append(adjusted_row1[i]-adjusted_row2[i])
    return l
def find_sum_of_Data_in_tabels(table1,table2,num_of_samples,index1,index2):#num_of_samples<=64
    l=[]
    adjusted_row1=dictionary[table1][0]['Data'][index1:index1+num_of_samples]
    adjusted_row2=dictionary[table2][0]['Data'][index2:index2+num_of_samples]
    for i in range(num_of_samples):
        l.append(adjusted_row1[i]+adjusted_row2[i])
    return l


def mean_square(l1,l2,num_of_samples):
    return sum([(l1[i]-l2[i])**2 for i in range(num_of_samples)])/num_of_samples
def sync_voltage(table1,table2,num_of_samples):#num_of_samples will be between 1 and 64
    #we used the fact that a cycle is 64 samples because the sample rate is 50HZ and we can see from the tables that it is close to that value for each sampling
    l=[]
    minimum=np.inf
    index=(0,0)
    for i in range(64): 
        for j in range(128):#we will go over 2 cycles
            x=mean_square(dictionary[table1][0]['Data'][i:i+num_of_samples],dictionary[table2][0]['Data'][j:j+num_of_samples],num_of_samples)
            if x<minimum:
                    minimum=x
                    indexes=(i,j)
    return indexes
    

def plot_graph(tableName, dic, parameterlst,dates=False,init_index=0,fin_index=-1,stringo="",im_id=0,voltage=230):
    #better use Power1 instead of P1 for displaying, as it is more accurate
    if(isinstance(init_index,str) and dates==True):
        t0=dt.datetime.strptime(init_index,"%H:%M:%S").time()
        t0=dt.datetime.combine(dt.date.today(), t0)
        flag_found=False
        for i in range(len(dic[tableName]["StringTime"])):
            t1=dt.datetime.strptime(dic[tableName]["StringTime"][i],"%m/%d/%y  %H:%M:%S.%f").time()
            t1=dt.datetime.combine(dt.date.today(), t1)
            if(abs(t1-t0)<dt.timedelta(0,10)):
                init_index=i
                flag_found=True
                break
        if(not(flag_found)):
            print("Error: initial time is not after of "+str(t0))
            return
    
    if(isinstance(fin_index,str) and dates==True):
        t0=dt.datetime.strptime(fin_index,"%H:%M:%S").time()
        t0=dt.datetime.combine(dt.date.today(), t0)
        flag_found=False
        for i in range(len(dic[tableName]["StringTime"])):
            t1=dt.datetime.strptime(dic[tableName]["StringTime"][i],"%m/%d/%y  %H:%M:%S.%f").time()
            t1=dt.datetime.combine(dt.date.today(), t1)
            if(abs(t1-t0)<dt.timedelta(0,10)):
                fin_index=i
                flag_found=True
                break
        if(not(flag_found)):
            print("Error: final time is not before of "+str(t0))
            return
    
    
    if(len(parameterlst)==1):
        plt.title(str(parameterlst[0])+ " graph: "+tableName)
    else:
         plt.title(str(parameterlst)+ " graph: "+tableName)
    print(dic.keys())
    if(dates==True):
        #xfmt = md.DateFormatter('%d-%m  %H:%M:%S')
        xfmt = md.DateFormatter('%H:%M')
        plt.xticks( rotation= 80 )
        ax=plt.gca()
        ax.xaxis.set_major_formatter(xfmt)
        ax.xaxis_date()
        x_dates=[dt.datetime.strptime(val,"%m/%d/%y  %H:%M:%S.%f") for val in dic[tableName]["StringTime"][init_index:fin_index]]
        print(len(x_dates))
        for parameterName in parameterlst:
            if(parameterName in ['Power1','Power2','Power3']):
                samples=dic[tableName]['I'+parameterName[5]][init_index:fin_index]
                samples=np.array(samples)*(voltage/1000)
            else:
                samples=dic[tableName][parameterName][init_index:fin_index]
            plt.plot(x_dates,samples,label=parameterName)
    else:
        for parameterName in parameterlst:
            if(parameterName in ['Power1','Power2','Power3']):
                samples=dic[tableName]['I'+parameterName[5]][init_index:fin_index]
                samples=np.array(samples)*(voltage/1000)
            else:
                samples=dic[tableName][parameterName][init_index:fin_index]
            plt.plot(samples,label=parameterName)
    plt.legend()
    plt.tight_layout()
    if os.path.exists("static/nilmgraph_"+stringo+".html"):
        os.remove("static/nilmgraph_"+stringo+".html")
    plt.savefig("static/plots/general_graphs/"+stringo+".png", format="png")
    cmd=""
    cmd+="echo ^<img src=\"{{url_for('static',filename='/plots/general_graphs/"+stringo+".png')}}\"/^> >"
    cmd2=""
    cmd2+="templates/nilmgraph_"
    cmd2+=stringo
    cmd2+=".html"
    print(cmd+cmd2)
    if(os.system(cmd+cmd2)):
        print("FAIL")
    
    
    plt.cla()
    plt.clf()
    plt.close()
    #plt.show()
    return "static/plots/general_graphs/"+stringo+".png"
    
def plot_devices_graph(list_devices,devices_indices,devices_names,UD1,UD2,UD3,dates=False,init_index=0,fin_index=-1, voltage=230):
    #list devices is the list with all the devices with their data
    #devices indices is the devices we want to print for- exmaple [0,6,7]
    day=dt.datetime.strptime(UD1[0][0],"%m/%d/%y  %H:%M:%S.%f")
    today=(day).strftime('%m/%d/%y ')
    t0=dt.datetime.strptime(today+init_index,"%m/%d/%y %H:%M:%S")
    t1=dt.datetime.strptime(today+fin_index,"%m/%d/%y %H:%M:%S")
    
    timestamp0 = dt.datetime.timestamp(t0)
    timestamp1 = dt.datetime.timestamp(t1)
    
    timestamps_arr=[i for i in range(int(timestamp0),int(timestamp1))]
    times_arr=[dt.datetime.fromtimestamp(i) for i in timestamps_arr]
    
    
    if(len(devices_names)==1):
        plt.title("power graph: "+str(devices_names[0]))
    else:
         plt.title("power graph: "+str(devices_names))
    
    #xfmt = md.DateFormatter('%d-%m  %H:%M:%S')
    xfmt = md.DateFormatter('%H:%M')
    plt.xticks( rotation= 80 )
    ax=plt.gca()
    ax.xaxis.set_major_formatter(xfmt)
    ax.xaxis_date()
    
    x_dates=times_arr
    samples=np.zeros((len(list_devices),len(x_dates)))
    UD_arr=[UD1,UD2,UD3]
    for UD in UD_arr:
        for ele in UD:
            if(ele[-1] in devices_indices):
                t0=dt.datetime.strptime(ele[0],"%m/%d/%y  %H:%M:%S.%f")
                t1=dt.datetime.strptime(ele[1],"%m/%d/%y  %H:%M:%S.%f")
                cnt=0
                for t in x_dates:
                    if(t>=t0 and t<=t1):
                        samples[int(ele[-1]),int(cnt)]+=list_devices[int(ele[-1])].current
                    cnt+=1
    cnt=0                  
    for ind in devices_indices:
        plt.plot(x_dates,samples[ind]*(voltage/1000),label=devices_names[cnt])
        cnt+=1
    plt.legend()
    plt.tight_layout()
    #plt.savefig("plots/general_graphs/"+tableName+" PAR="+str(parameterlst)+".png", format="png")
    #plt.show()
    
    if os.path.exists("static/nilmgraph_"+"devices"+".html"):
        os.remove("static/nilmgraph_"+"devices"+".html")
    plt.savefig("static/plots/general_graphs/"+"devices"+".png", format="png")
    cmd=""
    cmd+="echo ^<img src=\"{{url_for('static',filename='/plots/general_graphs/"+"devices"+".png')}}\"/^> >"
    cmd2=""
    cmd2+="templates/nilmgraph_"
    cmd2+="devices"
    cmd2+=".html"
    print(cmd+cmd2)
    if(os.system(cmd+cmd2)):
        print("FAIL")
    
    
    plt.cla()
    plt.clf()
    plt.close()
    #plt.show()
    return "static/plots/general_graphs/"+"devices"+".png"


def plotTotalCost(list_devices,devices_indices, voltage=230, price=0.5, currency_name='USD', months=12):
    #display the data from the last year 
    start=dt.datetime.today()
    last_months=[]
    total_amount=[0 for i in range(months)]
    for i in range(months):
        last_months.append((start.year,start.month))
        start += relativedelta(months = -1)
    
    for ind in devices_indices:
        for t_ind,t_str in enumerate(list_devices[ind].start_time_arr):
            t_end=list_devices[ind].end_time_arr[t_ind]
            t0=dt.datetime.strptime(t_str,"%m/%d/%y  %H:%M:%S.%f")
            t1=dt.datetime.strptime(t_end,"%m/%d/%y  %H:%M:%S.%f")
            if (t0.year,t0.month) in last_months:
                i=0
                for i in range(len(last_months)):
                    if (t0.year,t0.month)==last_months[i]:
                        break
                total_amount[i]+=((t1-t0).total_seconds()/3600)*(voltage/1000)*price
    lm=['(%d,%02d)'%(tup[0],tup[1]) for tup in last_months]
    
    
    for i in range(len(lm)):
        lm[i] = dt.datetime.strptime(lm[i],'(%Y,%m)')


    ax=plt.gca()
    xfmt = md.DateFormatter('%b, %Y')
    ax.xaxis.set_major_formatter(xfmt)
    ax.xaxis_date()
    plt.xticks(lm,rotation=80)
    
    plt.bar(lm,total_amount,width=200/months)
    plt.ylabel(currency_name)
    plt.tight_layout()
    #plt.show()
    
    if os.path.exists("static/nilmgraph_"+"cost"+".html"):
        os.remove("static/nilmgraph_"+"cost"+".html")
    plt.savefig("static/plots/general_graphs/"+"cost"+".png", format="png")
    cmd=""
    cmd+="echo ^<img src=\"{{url_for('static',filename='/plots/general_graphs/"+"cost"+".png')}}\"/^> >"
    cmd2=""
    cmd2+="templates/nilmgraph_"
    cmd2+="cost"
    cmd2+=".html"
    print(cmd+cmd2)
    if(os.system(cmd+cmd2)):
        print("FAIL")
    
    
    plt.cla()
    plt.clf()
    plt.close()
    #plt.show()
    return "static/plots/general_graphs/"+"cost"+".png"
    


def plot_power_graph(tableName):
    plt.title("power graph: "+tableName)
    plt.plot(dictionary[tableName]["kW"],label="kW")
    plt.plot(dictionary[tableName]["kvar"],label="kvar")
    plt.legend()
    plt.savefig("plots/time/"+tableName+".png", format="png")
    plt.show()
    
def plot_power_graph_spectrum(tableName):
    plt.title("power graph spectrum: "+tableName)
    plt.yscale('log')
    #print(np.abs(np.fft.fft(dictionary[tableName]["kW"]))[0])
    plt.plot(dft_vector(dictionary[tableName]["kW"]),label="kW")
    plt.plot(dft_vector(dictionary[tableName]["kvar"]),label="kvar")
    plt.legend()
    
    plt.savefig("plots/spectrum/"+tableName+".png", format="png")
    plt.show()

def plot_power_graph2(tableName1,tableName2):
    #plt.title("power graphs: "+tableName1+" "+tableName2)
    fig, [ax1, ax2] = plt.subplots(2, 1)
    ax1.set_title(tableName1)
    ax1.plot(dictionary[tableName1]["kW"],label="kW")
    ax1.plot(dictionary[tableName1]["kvar"],label="kvar")
    ax2.set_title(tableName2)
    ax2.plot(dictionary[tableName2]["kW"],label="kW")
    ax2.plot(dictionary[tableName2]["kvar"],label="kvar")
    ax1.legend()
    ax2.legend()
    #plt.savefig("plots/time/"+tableName+".png", format="png")
    fig.show()


def dft_vector(vector):
    return np.abs(np.fft.fft(vector))

def l1_distance(v1,v2):
    return sum([abs(v1[i]-v2[i]) for i in range(min(len(v1),len(v2)))])

def l2_distance(v1,v2):
    return sum([math.pow(v1[i]-v2[i],2) for i in range(min(len(v1),len(v2)))])**0.5
 
def diff_l2based(table1,table2):
      return l2_distance(dft_vector(table1),dft_vector(table2))
def diff_l1based(table1,table2):
      return l1_distance(dft_vector(table1),dft_vector(table2))



def find_edges(table, threshold, positive_flag, negative_flag):
    #threshhold is relative to table values
    #positive flag is for positive gradients
    #negative flag is for negative gradients
    t_arr=list()
    for t in range(1,len(table)):
        if(positive_flag and table[t]-table[t-1]>=threshold*table[t]):
            t_arr.append(t)
        elif(negative_flag and table[t-1]-table[t]>=threshold*table[t]):
            t_arr.append(t)
    return t_arr


def already_exist_at_dist(indices,ind,threshold):
    for i in indices:
        if (i-ind)**2<=threshold**2:
            return True
    return False


def already_exist_at_dist2(edges_pairs,pair,threshold):
    for pair2 in edges_pairs:
        if (pair[0]-pair2[0])**2<=threshold**2 and pair[0]>pair2[0] and pair[1]==pair2[1]: 
            return True
    return False

def edges_cleaner(indices,threshold):
    new_indices=list()
    for ind in indices:
        if (already_exist_at_dist(new_indices,ind,threshold)==False):
            new_indices.append(ind)
    return new_indices


def edges_cleaner2(edges_pairs,threshold):
    new_pairs=list()
    for pair in edges_pairs:
        if (already_exist_at_dist2(edges_pairs,pair,threshold)==False):
            new_pairs.append(pair)
    return new_pairs


def find_edges_abs(table, threshold, positive_flag, negative_flag):
    #threshhold is relative to table values
    #positive flag is for positive gradients
    #negative flag is for negative gradients
    t_arr=list()
    for t in range(1,len(table)):
        if(positive_flag and table[t]-table[t-1]>=threshold):
            t_arr.append(t)
        elif(negative_flag and table[t-1]-table[t]>=threshold):
            t_arr.append(t)
    return t_arr


def find_edges_abs_plus_size(table, threshold, positive_flag=True, negative_flag=True):
    #threshhold is relative to table values
    #positive flag is for positive gradients
    #negative flag is for negative gradients

    t_arr=list()
    for t in range(1,len(table)):
        if(positive_flag and table[t]-table[t-1]>=threshold):
            t_arr.append([t,table[t]-table[t-1]])
        elif(negative_flag and table[t-1]-table[t]>=threshold):
            t_arr.append([t,table[t]-table[t-1]])
    return t_arr


def sublist(lst,indices):
    ls=list()
    for ind in indices:
        ls.append(lst[ind])
    return ls

def timestamps_to_strings(dic,indices):
    times=sublist(dic["StringTime"],indices)
    return times
    
def timestamps_to_strings2(dic,pairs_arr):
    times=sublist(dic["StringTime"],[x[0] for x in pairs_arr])
    return [[times[i],pairs_arr[i][1],pairs_arr[i][0]] for i in range(len(times))]


def up_down_connector(pairs_arr,threshold_size=0,epsilon=0):
    #gets an array with elements of format ('time',edge size)
    #first element is just an array with all the non-pairs for efficient computation
    res=[[]]
    i=0
    while(i<len(pairs_arr)-1):
        if(pairs_arr[i][1] >=threshold_size): #i.e it is up and we want to find its down pair
            size=pairs_arr[i][1]
            t1 = dt.datetime.strptime(pairs_arr[i][0], '%m/%d/%y  %H:%M:%S.%f')
            t2 = dt.datetime.strptime(pairs_arr[i+1][0], '%m/%d/%y  %H:%M:%S.%f')
            k=i+1
            FoundFlag=False
            if(i<len(pairs_arr) and pairs_arr[i][1]+pairs_arr[i+1][1]>=threshold_size and t2-t1<=dt.timedelta(0,10)): #10 seconds difference
                    size+=pairs_arr[i+1][1]
                    k+=1
            for j in range(k,len(pairs_arr)): #for all possible elements after it
                t2 = dt.datetime.strptime(pairs_arr[j][0], '%m/%d/%y  %H:%M:%S.%f')
                if(abs(size+pairs_arr[j][1])<=epsilon): #one sample difference
                    res.append([pairs_arr[i][0],pairs_arr[j][0],size,pairs_arr[j][1],(t2-t1),pairs_arr[i][2],pairs_arr[j][2]])
                    i=i+1
                    FoundFlag=True
                    break
                if(j+1==len(pairs_arr)):
                    break
                t3 = dt.datetime.strptime(pairs_arr[j+1][0], '%m/%d/%y  %H:%M:%S.%f')
                if(abs(size+pairs_arr[j][1]+pairs_arr[j+1][1])<=epsilon and t3-t2<=dt.timedelta(0,10)): #two sample difference               
                    res.append([pairs_arr[i][0],pairs_arr[j+1][0],size,pairs_arr[j][1]+pairs_arr[j+1][1],t3-t1,pairs_arr[i][2],pairs_arr[j+1][2]])
                    i=i+2
                    FoundFlag=True
                    break
            if(FoundFlag==False):
                res[0].append([pairs_arr[i][0],pairs_arr[i][1],pairs_arr[i][2]]) #add
        i+=1
    return res
                


def filter_duration(tensor, index_time,min_time_seconds,max_time_seconds):
    min_t=dt.timedelta(0,min_time_seconds)
    max_t=dt.timedelta(0,max_time_seconds)
    res=[]
    for vec in tensor:
        if(vec[index_time]>=min_t and vec[index_time]<=max_t):
            res.append(vec)
    return res
            
      
def THD_avg_add(tensor,THD_dict):
    res=list()
    for vec in tensor:
        i1=vec[-2]
        i2=vec[-1]
        avg_thd=0
        for i in range(i1,i2):
            avg_thd+=THD_dict[i]
        avg_thd/=(i2-i1)
        res.append(vec+[avg_thd])
    return res
    
    
def get_time_difference(t1_str,t2_str):
    #returns the time difference of the hour of the day, independent of the date it was on
    a=dt.datetime.combine(dt.date.today(),dt.datetime.strptime(t1_str, '%m/%d/%y  %H:%M:%S.%f').time())
    b=dt.datetime.combine(dt.date.today(),dt.datetime.strptime(t2_str, '%m/%d/%y  %H:%M:%S.%f').time())
    time_diff=min(abs(a-b),abs(a-b+ dt.timedelta(days=1)))
    return time_diff
    
    
def time_score(t1_str,t2_str):
    #returns the score that 2 devices recieve based on the hour of the day
    #minimum score 0
    #maximum score 36
    #time_diff of 1 second score is 16
    #time_diff of 1 hour score is 4
    time_diff=get_time_difference(t1_str,t2_str)
    initial=dt.timedelta(hours=12)
    score=0
    while(time_diff<initial):
        score+=1
        initial/=2
    print(score)
    
    



class Device():
    def __init__(self,current,current_THD,start_time_arr=[],end_time_arr=[],phase=[1,0,0],phase_static=False):
        self.current=current
        self.current_THD=current_THD
        self.num_apperances=1
        self.end_time_arr=end_time_arr
        self.start_time_arr=start_time_arr #start times of device in array
        self.fixed_power=True #whether the power is constant or changing over time
        self.phase=phase #whether the power is constant or changing over time
        self.phase_static=phase_static
        self.name='temporal_name'
        
        
    def similar(self,dev2,eps_curr,eps_THD):
        if(dev2.phase_static==True and sum([1 if (self.phase[i]+dev2.phase[i])>0 else 0 for i in range(len(dev2.phase))]))>1:
            #if it is on the same phase all the time and the new device is from another phase
            return False
        if(abs(self.current-dev2.current)<=eps_curr):
            if(abs(self.current_THD-dev2.current_THD)<=eps_THD):
                return True
        return False

    def update(self,dev2):
        n=self.num_apperances
        self.current=(self.current*n+dev2.current)/(n+1)
        self.current_THD=(self.current_THD*n+dev2.current_THD)/(n+1)
        self.num_apperances+=1
        self.phase[0]+=dev2.phase[0]
        self.phase[1]+=dev2.phase[1]
        self.phase[2]+=dev2.phase[2]
    
    def add_start_time(self,start_time):
        self.start_time_arr.append(start_time)
    def add_end_time(self,end_time):
        self.end_time_arr.append(end_time)
    def set_name(self,_name):
        self.name=_name
    def tojson(self):
        return {'name':self.name,'current':self.current,'current_THD':self.current_THD,'phase0':self.phase[0],'phase1':self.phase[1],'phase2':self.phase[2]}
        #return {'name':str(self.name),'current':str(self.current),'current_THD':str(self.current_THD),'phase[0]':str(self.phase[0]),'phase[1]':str(self.phase[1]),'phase[2]':str(self.phase[2])}

def print_tensor(tensor):
    for vec in tensor:
        print(vec)


def print_devices(list_devs):
    for i,dev in enumerate(list_devs):
        print("DEV #%d: curr:%f, curr_THD:%f, Phase:[%d,%d,%d]:"%(i,dev.current,dev.current_THD,dev.phase[0],dev.phase[1],dev.phase[2]))


def addNonPairs(pairs,nonpairs,timestamp,last_index):
    t_last=dt.datetime.strptime(timestamp, '%m/%d/%y  %H:%M:%S.%f')
    for ele in nonpairs:
        t = dt.datetime.strptime(ele[0], '%m/%d/%y  %H:%M:%S.%f')
        pairs.append([ele[0],timestamp,ele[1],-ele[1],t_last-t,ele[2],last_index])
    return 0
app=Flask(__name__) #setup the application
#create index route to not go imidatly to 404
@app.route('/app',methods=['POST','GET'])
def form():
    for i in range(150):#delay to make the line "device added succesfully apear longer"
        print(i)
    for phase_ind in range(len(UD_arr)):    
        for ele in UD_arr[phase_ind]: #UD1 / UD2 / UD3
            dev1=Device(current=0.5*(ele[2]-ele[3]),current_THD=ele[7],phase=phase_arr[phase_ind].copy())
            match_flag=False
            for i,dev2 in enumerate(list_devices):
                if(dev1.similar(dev2,eps_curr=1,eps_THD=eps_THD_arr[phase_ind])):
                    device_index.append(i)
                    ele.append(i)
                    dev2.update(dev1)
                    dev2.add_start_time(ele[0])
                    dev2.add_end_time(ele[1])
                    match_flag=True
                    break
            if(match_flag==False):
                #print("ENTERED")
                #This is where we interact with the user and ask what device was used for the first time
                return jsonify({'needed':'yes','dev':dev1.tojson()})
    return jsonify({'needed':'no','dev':dev1.tojson()})
@app.route('/add_device_json',methods=['GET','POST'])
def add():
    #ADD
    print("H")
    print(request.get_json())
    inpdev=request.get_json()
    a=0
    s=inpdev['name']
    print(s)
    for dev in list_devices:
        if(inpdev['name']==dev.name):
            a=1
    if a==0:
        dev1=Device(current=float(inpdev['current']),current_THD=float(inpdev['current_THD']),phase=[int(inpdev['phase0']),int(inpdev['phase1']),int(inpdev['phase2'])])
        dev1.set_name(inpdev['name'])
        list_devices.append(dev1)
        device_index.append(len(list_devices)-1)
        #print(i)
        #device_index.append(len(list_devices)-1)
        #ele.append(len(list_devices)-1)
        #remove
        #list_devices.append(dev1)
        #device_index.append(len(list_devices)-1)
        #ele.append(len(list_devices)-1)
        return jsonify(dev1.tojson())
    else:
        inpdev['name']=s+str(0)
        return jsonify(inpdev)
        
@app.route('/remove_device_json',methods=['GET','POST'])
def remove():
    #REMOVE
    inpdev=request.get_json()
    dev='a'
    ind=0
    for i in range(len(list_devices)):
        if list_devices[i].name==inpdev['name']:
            dev=list_devices[i]
            ind=i
    if(dev!='a'):
        for j in range(ind,len(device_index)):
            device_index[j]-=1
        list_devices.remove(dev)
        device_index.remove(device_index[ind])
        return jsonify({'name':inpdev['name'],'success':'yes'})
    #print(i)
    #device_index.append(len(list_devices)-1)
    #ele.append(len(list_devices)-1)
    #remove
    #list_devices.append(dev1)
    #device_index.append(len(list_devices)-1)
    #ele.append(len(list_devices)-1)
    return jsonify({'name':inpdev['name'],'success':'no'})
@app.route('/nilmgraph/I',methods=['GET'])
def show_i():
    return render_template("nilmgraph_I.html")
@app.route('/get_device_list' , methods=['GET'])
def get_device_list():
    #return jsonify({'devices':[i.tojson() for i in list_devices]})
    return jsonify([i.tojson() for i in list_devices])
@app.route('/nilmgraph/I THD',methods=['GET'])
def show_i_thd():
    return render_template("nilmgraph_I_THD.html")
@app.route('/nilmgraph/P_KVAR',methods=['GET'])
def show_p_kvar():
    return render_template("nilmgraph_P_KVAR.html")
@app.route('/nilmgraph/P_KW',methods=['GET'])
def show_p_kw():
    return render_template("nilmgraph_P_KW.html")
@app.route('/nilmgraph_power',methods=['POST'])
def graph_form_post_power():
    start=str(request.form['starttime'])
    end=str(request.form['endtime'])
    parse_all_data(dictionary,dictionary_2days)
    tables_list=list(dictionary.keys()) #names of all the tables    
    tablenum=2
    print("HELLO")
    ############get init index and fin index form user
    plot_graph("Administrato_output1_table%d"%tablenum,dictionary_2days,["Power1","Power2","Power3"],True,init_index=start,fin_index=end,stringo="Power")
    return jsonify({})
@app.route('/nilmgraph_devices',methods=['POST'])
def graph_form_post_devices():
    print(UD1)
    print(UD2)
    print(UD3)
    r=request.get_json()
    start=str(r['starttime'])
    end=str(r['endtime'])
    parse_all_data(dictionary,dictionary_2days)
    tables_list=list(dictionary.keys()) #names of all the tables    
    tablenum=2
    print("HELLO")
    curindxs=[]
    devsplot=r['devices_to_plot']
    print(devsplot)
    for i in devsplot:
        for j in range(len(list_devices)):
            if(i==list_devices[j].name):
                curindxs.append(j)
    print(curindxs)
    ############get init index and fin index form user
    plot_devices_graph(list_devices,curindxs,devsplot,UD1,UD2,UD3,init_index=start,fin_index=end)
    return jsonify({})
@app.route('/nilmgraph_cost',methods=['POST'])
def graph_form_post_cost():
    r=request.get_json()
    price=r['price']
    months=r['months']
    currency=r['currency']
    parse_all_data(dictionary,dictionary_2days)
    tables_list=list(dictionary.keys()) #names of all the tables    
    tablenum=2
    print("HELLO")
    ############get init index and fin index form user
    plotTotalCost(list_devices,device_index, price=price, currency_name=currency, months=months)
    return jsonify({})
if __name__ == "__main__":
    tablenum=2
    parse_all_data(dictionary,dictionary_2days)
    tables_list=list(dictionary.keys()) #names of all the tables
    print(tables_list)
    for i in range(len(tables_list)):
        print(str(i)+"   "+tables_list[i])
    #print("I1 Edges timestamps:",timestamps_to_strings(dictionary_2days["Administrato_output1_table2"],edges_cleaner(find_edges_abs(dictionary_2days["Administrato_output1_table2"]["I1"],0.5,positive_flag=True,negative_flag=True),100)))
    #print("I2 Edges timestamps:",timestamps_to_strings(dictionary_2days["Administrato_output1_table2"],edges_cleaner(find_edges_abs(dictionary_2days["Administrato_output1_table2"]["I2"],0.5,positive_flag=True,negative_flag=True),0)))
    #print("I3 Edges timestamps:",timestamps_to_strings(dictionary_2days["Administrato_output1_table2"],edges_cleaner(find_edges_abs(dictionary_2days["Administrato_output1_table2"]["I3"],0.5,positive_flag=True,negative_flag=True),0)))
    
    
    #print("I1 Edges timestamps:",timestamps_to_strings2(dictionary_2days["Administrato_output1_table2"],edges_cleaner2(find_edges_abs_plus_size(dictionary_2days["Administrato_output1_table2"]["I1"],0.5,positive_flag=True,negative_flag=True),0)))
    #print("I3 Edges timestamps:",timestamps_to_strings2(dictionary_2days["Administrato_output1_table2"],edges_cleaner2(find_edges_abs_plus_size(dictionary_2days["Administrato_output1_table2"]["I3"],0.5,positive_flag=True,negative_flag=True),0)))
    M1=timestamps_to_strings2(dictionary_2days["Administrato_output1_table%d"%tablenum],edges_cleaner2(find_edges_abs_plus_size(dictionary_2days["Administrato_output1_table%d"%tablenum]["I1"],0.5),0))
    M2=timestamps_to_strings2(dictionary_2days["Administrato_output1_table%d"%tablenum],edges_cleaner2(find_edges_abs_plus_size(dictionary_2days["Administrato_output1_table%d"%tablenum]["I2"],0.5),0))
    M3=timestamps_to_strings2(dictionary_2days["Administrato_output1_table%d"%tablenum],edges_cleaner2(find_edges_abs_plus_size(dictionary_2days["Administrato_output1_table%d"%tablenum]["I3"],0.5),0))
    #print("up_down_connector M1 : ",up_down_connector(M1,2,1))
    #print("up_down_connector M2 : ",up_down_connector(M2,2,1))
    #print("up_down_connector M3 : ",up_down_connector(M3,2,1))
    

    

    res1=up_down_connector(M1,2,1)
    res2=up_down_connector(M2,2,1)
    res3=up_down_connector(M3,2,1)

    nonpairs1=res1[0]   
    nonpairs2=res2[0]   
    nonpairs3=res3[0] 
   
    res1=res1[1:]
    res2=res2[1:]
    res3=res3[1:]
    
    
    
    UD1=filter_duration(res1, 4,5,50000)
    UD2=filter_duration(res2, 4,5,50000)
    UD3=filter_duration(res3, 4,5,50000)
    
    addNonPairs(UD1,nonpairs1,dictionary_2days["Administrato_output1_table%d"%tablenum]["StringTime"][-1],len(dictionary_2days["Administrato_output1_table%d"%tablenum]["StringTime"])-1)
    addNonPairs(UD2,nonpairs2,dictionary_2days["Administrato_output1_table%d"%tablenum]["StringTime"][-1],len(dictionary_2days["Administrato_output1_table%d"%tablenum]["StringTime"])-1)
    addNonPairs(UD3,nonpairs3,dictionary_2days["Administrato_output1_table%d"%tablenum]["StringTime"][-1],len(dictionary_2days["Administrato_output1_table%d"%tablenum]["StringTime"])-1)
    
    
    
    
    UD1=THD_avg_add(UD1,dictionary_2days["Administrato_output1_table%d"%tablenum]["I1 THD"])
    UD2=THD_avg_add(UD2,dictionary_2days["Administrato_output1_table%d"%tablenum]["I2 THD"])
    UD3=THD_avg_add(UD3,dictionary_2days["Administrato_output1_table%d"%tablenum]["I3 THD"])
    UD_arr=[UD1,UD2,UD3]
    
    phase1=[1,0,0]
    phase2=[0,1,0]
    phase3=[0,0,1]
    phase_arr=[phase1,phase2,phase3]
    eps_THD_arr=[5,2,1]
    list_devices=list()
    device_index=list()
    app.run(debug=True,use_reloader=False, host='0.0.0.0',port=5000,ssl_context='adhoc')
    
    



