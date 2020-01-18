import sys
import os
import csv


def csvToDict(relative_path):
    #converts csv file to matrix
    table=dict()
    tr=dict()
    if(not(os.path.exists(os.path.abspath(relative_path)))):
        print("ERROR, can't read: "+os.path.abspath(relative_path))
    with open(os.path.abspath(relative_path), 'rt') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            header=row
            break
        for row in reader:
            for i in range(len(header)):
                tr[header[i]]=row[i]
            table[row[0]]=tr
    csvfile.close()
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


dictionary=dict()
def get_table_titles(table):
    return dictionary[table].keys

def get_table_data(table):
    return dictionary[table]

if __name__ == "__main__":
    
    
    
    parse_all_data(dictionary)
    print(get_table_titles("s1_alloff_I1")) #this is how you get the titles
    
    #print(get_table_data("s1_alloff_I1")) #this is how you get the data
    
    
    
    
    

    




    
