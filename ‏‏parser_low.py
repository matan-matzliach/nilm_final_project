import sys
import os
import csv
import numpy as np

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
                table[head]=list()
                num_to_header[i]=str(head)
                i+=1
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


def parse_all_data(dictionary):
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
    
    
if __name__ == "__main__":
    
    
    
    parse_all_data(dictionary)
    #diff_all_data(dictionary,difdictionary,prefixlist)
    print(dictionary["s3_alloff_output1_table1"]["kW"]) #this is how you get the titles
    
    #print(get_table_data("s1_alloff_I1")) #this is how you get the data


