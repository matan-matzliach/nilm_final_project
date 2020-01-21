import sys
import os
import csv
import numpy as np
import matplotlib.pyplot as plt

def csvToDict(relative_path):
    #converts csv file to matrix
    table=dict()
    if(not(os.path.exists(os.path.abspath(relative_path)))):
        print("ERROR, can't read: "+os.path.abspath(relative_path))
    else:
        with open(os.path.abspath(relative_path), 'rt') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                header=row
                break
            for row in reader:
                tr=dict()
                tr['FIND_KEY']=int(row[0])
                tr['sequence']=int(row[1])
                tr['DoubleTimeStart']=float(row[2]) #there is no double in python so we used float
                tr['StringTimeStart']=row[3]
                tr['DoubleTimeTrigg']=float(row[4]) #there is no double in python so we used float
                tr['StringTimeTrigg']=row[5]
                tr['SeriesNo']=int(row[6])
                tr['RecordNo']=int(row[7])
                tr['EvtType']=int(row[8])
                tr['EvtSeq']=int(row[9])
                tr['PointID']=int(row[10])
                tr['TrigPoint']=int(row[11])
                tr['PointsPerCycle']=int(row[12])
                tr['PointsPerRecord']=int(row[13])
                tr['SampleFreq']=float(row[14])
                tr['SampleRate']=float(row[15])
                tr['Scale']=float(row[16])
                tr['ScaleAD']=int(row[17])
                tr['ZeroOffs']=int(row[18])
                tr['HWDelay']=int(row[19])
                tr['SWDelay']=int(row[20])
                tr['Data']=[int(i) for  i in row[21].split(",")]
                table[int(row[0])]=tr
        csvfile.close()
    return table
def dictPower(dictionary,I,V):
    table=dict()
    header=dictionary[I][0].keys()
    for row in(dictionary[I]):
        tr=dict()
        tr['FIND_KEY']=dictionary[I][row]['FIND_KEY']
        tr['sequence']=dictionary[I][row]['sequence']
        tr['DoubleTimeStart']=dictionary[I][row]['DoubleTimeStart']
        tr['StringTimeStart']=dictionary[I][row]['StringTimeStart']
        tr['DoubleTimeTrigg']=dictionary[I][row]['DoubleTimeTrigg']
        tr['StringTimeTrigg']=dictionary[I][row]['StringTimeTrigg']
        tr['SeriesNo']=dictionary[I][row]['SeriesNo']
        tr['RecordNo']=dictionary[I][row]['RecordNo']
        tr['EvtType']=dictionary[I][row]['EvtType']
        tr['EvtSeq']=dictionary[I][row]['EvtSeq']
        tr['PointID']=dictionary[I][row]['PointID']
        tr['TrigPoint']=dictionary[I][row]['TrigPoint']
        tr['PointsPerCycle']=dictionary[I][row]['PointsPerCycle']
        tr['PointsPerRecord']=dictionary[I][row]['PointsPerRecord']
        tr['SampleFreq']=dictionary[I][row]['SampleFreq']
        tr['SampleRate']=dictionary[I][row]['SampleRate']
        tr['Scale']=dictionary[I][row]['Scale']
        tr['ScaleAD']=dictionary[I][row]['ScaleAD']
        tr['ZeroOffs']=dictionary[I][row]['ZeroOffs']
        tr['HWDelay']=dictionary[I][row]['HWDelay']
        tr['SWDelay']=dictionary[I][row]['SWDelay']
        tr['Data']=[dictionary[I][row]['Data'][i]*dictionary[V][row]['Data'][i] for  i in range(len(dictionary[I][row]['Data']))]
        table[row]=tr
    return table
def add_tables_to_dict(prefix_str,relative_path,dictionary,mode=0):
    #since some of the tables have different names, We created mode to control what tables type to read
    if(mode==0):
        dictionary[prefix_str+"_I1"]=csvToDict(relative_path+"\RT_I1 RT Waveform.csv")
        dictionary[prefix_str+"_I2"]=csvToDict(relative_path+"\RT_I2 RT Waveform.csv")
        dictionary[prefix_str+"_I3"]=csvToDict(relative_path+"\RT_I3 RT Waveform.csv")
        dictionary[prefix_str+"_V1"]=csvToDict(relative_path+"\RT_V1 RT Waveform.csv")
        dictionary[prefix_str+"_V2"]=csvToDict(relative_path+"\RT_V2 RT Waveform.csv")
        dictionary[prefix_str+"_V3"]=csvToDict(relative_path+"\RT_V3 RT Waveform.csv")
    else:
        dictionary[prefix_str+"_I1"]=csvToDict(relative_path+"\RT_I1_RT_Waveform.csv")
        dictionary[prefix_str+"_I2"]=csvToDict(relative_path+"\RT_I2_RT_Waveform.csv")
        dictionary[prefix_str+"_I3"]=csvToDict(relative_path+"\RT_I3_RT_Waveform.csv")
        dictionary[prefix_str+"_V1"]=csvToDict(relative_path+"\RT_V1_RT_Waveform.csv")
        dictionary[prefix_str+"_V2"]=csvToDict(relative_path+"\RT_V2_RT_Waveform.csv")
        dictionary[prefix_str+"_V3"]=csvToDict(relative_path+"\RT_V3_RT_Waveform.csv")
    ###POWER
    dictionary[prefix_str+"_P1"]=dictPower(dictionary,prefix_str+"_I1",prefix_str+"_V1")
    dictionary[prefix_str+"_P2"]=dictPower(dictionary,prefix_str+"_I2",prefix_str+"_V2")
    dictionary[prefix_str+"_P3"]=dictPower(dictionary,prefix_str+"_I3",prefix_str+"_V3")
    prefixlist.append(prefix_str)


def parse_all_data(dictionary):
    #first_session
    add_tables_to_dict("s1_alloff","./firstSession/alloff/high/output",dictionary)
    add_tables_to_dict("s1_alloffwithairconditionoutsideofbsharasroom","./firstSession/alloffwithairconditionoutsideofbsharasroom/high/output",dictionary)
    add_tables_to_dict("s1_allofwithbsharasaircondition","./firstSession/allofwithbsharasaircondition/high/output",dictionary)
    add_tables_to_dict("s1_bsharamorning","./firstSession/bsharamorning/high/output",dictionary)
    add_tables_to_dict("s1_twolight","./firstSession/twolight/high/output",dictionary)
    #second_session
    add_tables_to_dict("s2_alllights","./secondSession/alllights/high/output",dictionary,1)
    add_tables_to_dict("s2_alloff","./secondSession/alloff/high/output",dictionary,1)
    add_tables_to_dict("s2_kettle","./secondSession/kettle/high/output",dictionary)
    add_tables_to_dict("s2_mw","./secondSession/mw/high/output",dictionary)
    add_tables_to_dict("s2_runninglabwithbasharaaircondition","./secondSession/runninglabwithbasharaaircondition/high/output",dictionary)
    #third_session
    add_tables_to_dict("s3_alloff","./thirdSession/alloff/high/output",dictionary,1)
    add_tables_to_dict("s3_alloffAirConditiokettle","./thirdSession/alloffAirConditiokettle/high/output",dictionary)
    add_tables_to_dict("s3_alloffairconditiononelight","./thirdSession/alloffairconditiononelight/high/output",dictionary,1)
    add_tables_to_dict("s3_alloffwithairconditionTwoLight","./thirdSession/alloffwithairconditionTwoLight/high/output",dictionary,1)
    add_tables_to_dict("s3_alloffwithairconditioOutsideBasharaRoom","./thirdSession/alloffwithairconditioOutsideBasharaRoom/high/output",dictionary,1)
    add_tables_to_dict("s3_alloffwithkettle","./thirdSession/alloffwithkettle/high/output",dictionary)
    add_tables_to_dict("s3_onelight","./thirdSession/onelight/high/output",dictionary)
    add_tables_to_dict("s3_secondlight","./thirdSession/secondlight/high/output",dictionary)
    #forth_session
    add_tables_to_dict("s4_2bashsarsComputers","./forthSession/2bashsarsComputers/highfreq/output",dictionary)
    add_tables_to_dict("s4_aircoditionMW","./forthSession/aircoditionMW/high/output",dictionary)
    add_tables_to_dict("s4_airconditionAndkettleandlight","./forthSession/airconditionAndkettleandlight/high/output",dictionary)
    add_tables_to_dict("s4_alloff","./forthSession/alloff/high/output",dictionary)
    add_tables_to_dict("s4_alloffAircon","./forthSession/alloffAircon/high/output",dictionary,1)
    add_tables_to_dict("s4_alloffonelight","./forthSession/alloffonelight/high/output",dictionary)
    add_tables_to_dict("s4_kettelandlight","./forthSession/kettelandlight/high/output",dictionary)
    add_tables_to_dict("s4_mw","./forthSession/mw/high/output",dictionary)
    add_tables_to_dict("s4_onelightAndAircondi","./forthSession/onelightAndAircondi/high/output",dictionary)
    add_tables_to_dict("s4_twolightandAirco","./forthSession/twolightandAirco/high/output",dictionary,1)

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

def graph_8_cycles(table_sample):
    meas=table_sample["Data"]
    t=[i*(8/50)/len(meas) for i in range(len(meas))]
    plt.plot(t,meas)
    plt.show()
def graph_8_cycles_dif_sum(table_sample):
    t=[i*(8/50)/len(table_sample) for i in range(len(table_sample))]
    plt.plot(t,table_sample)
    plt.show()
    
if __name__ == "__main__":
    
    
    
    parse_all_data(dictionary)
    diff_all_data(dictionary,difdictionary,prefixlist)
    print(get_table_data("s1_alloff_I1")[3]) #this is how you get the titles
    #graph_8_cycles(get_table_data("s1_alloff_V1")[3])
    #graph_8_cycles(get_table_data("s1_alloff_I1")[3])
    #graph_8_cycles_dif_sum(difdictionary["s1_alloff_V1 - s2_alloff_V1"]*8)
    #graph_8_cycles_dif_sum(sumdictionary["s1_alloff_I1 + s2_alloff_I1"]*8)
    #print(get_table_data("s1_alloff_I1")) #this is how you get the data
