import sys
import os
import csv
import numpy as np
import matplotlib.pyplot as plt
import math
import datetime as dt
import matplotlib.dates as md
import pandas as pd
from dateutil.relativedelta import relativedelta


def csvToDict(relative_path):
    '''converts csv file wiht the relative path to tensor'''
    
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
    '''reading tables into the dictionary data structure from the csv
    prefix_str is the name of the table to save as the key
    relative_path is the relative path to the csv file
    
    '''
    output_arr=["1","2","3"]
    table_arr=["1","2","3","4"]
    for output in output_arr:
        for table in table_arr:
            if((os.path.exists(os.path.abspath(relative_path+output+"/table"+table+".csv")))):
                dictionary[prefix_str+"_output"+output+"_table"+table]=csvToDict(relative_path+output+"/table"+table+".csv")
            
    
    prefixlist.append(prefix_str)


def parse_all_data(dictionary,dictionary_2):
    '''parses all the samples data into dictionary and dictionary_2
    where dictionary is the old format samples
    dictionary_2 is the new format samples
    '''
        
    
    
    #full_2_days
    add_tables_to_dict("Administrato","./satec_samples/",dictionary_2)
    
    

  

dictionary=dict()
dictionary_2days=dict()
prefixlist=[]
difdictionary=dict()
sumdictionary=dict()


    

def plot_graph(tableName, dic, parameterlst,dates=False,init_index=0,fin_index=-1, voltage=230):
    '''returns the plot of our samples:
        tableName- is the table from which to take the samples
        dic- the dictionary in which the table exist
        parameterlst- list of all different samples titles that will be plotted (for power use Power#)
        dates- whether to present the x axis as time or as indices
        init_index- first sample to start from, if dates is true then initial hour as string format
        init_index- last sample to end with, if dates is true then final hour as string format
        voltage- the base voltage in the house, used only if Power is in parameterlst
        '''
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
    if('Power1' in parameterlst or 'Power2' in parameterlst or 'Power3' in parameterlst):
        plt.ylabel('KW')
    #plt.savefig("plots/general_graphs/"+tableName+" PAR="+str(parameterlst)+".png", format="png")
    plt.show()
 
    
def plot_devices_graph(list_devices,devices_indices,devices_names,UD1,UD2,UD3,dates=False,init_index=0,fin_index=-1, voltage=230):
    '''returns the plot of our samples based on the system:
        list_devices- list of all our devices
        devices_indices- indices of devices we want to plot
        devices_names- names of devices we want to appear in legend, same order as devices_indices
        UD1,UD2,UD3- lists of all the events that we detected based on the phase
        dates- whether to present the x axis as time or as indices
        init_index- first sample to start from, if dates is true then initial hour as string format
        init_index- last sample to end with, if dates is true then final hour as string format
        voltage- the base voltage in the house, used only if Power is in parameterlst
        '''   
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
                        samples[ele[-1],cnt]+=list_devices[ele[-1]].current
                    cnt+=1
    cnt=0                  
    for ind in devices_indices:
        plt.plot(x_dates,samples[ind]*(voltage/1000),label=devices_names[cnt])
        cnt+=1
    plt.legend()
    plt.ylabel('KW')
    #plt.savefig("plots/general_graphs/"+tableName+" PAR="+str(parameterlst)+".png", format="png")
    plt.show()   
    


def plotTotalCost(list_devices,devices_indices, voltage=230, price=0.5, currency_name='USD', months=12):
    '''returns the plot of our cost based on the system analysis:
        list_devices- list of all our devices
        devices_indices- indices of devices we want to plot
        voltage- the base voltage in the house, used only if Power is in parameterlst
        price- price of 1kwh
        currency_name- name of the currency
        months- total of months back to show in the graph
        '''   
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
                total_amount[i]+=((t1-t0).total_seconds()/3600)*(list_devices[ind].current*voltage/1000)*price
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
    plt.show()  
    
    
    





def find_edges_abs_plus_size(table, threshold, positive_flag=True, negative_flag=True):
    '''
    finds indices and sizes (tuple) of all edges in the table:
        
    table is the table to which to find the edges from
    threshhold is the absolute threshold to pick
    positive flag is whether to include positive gradients
    negative flag is whether to include negative gradients
    '''
    
    t_arr=list()
    for t in range(1,len(table)):
        if(positive_flag and table[t]-table[t-1]>=threshold):
            t_arr.append([t,table[t]-table[t-1]])
        elif(negative_flag and table[t-1]-table[t]>=threshold):
            t_arr.append([t,table[t]-table[t-1]])
    return t_arr


def sublist(lst,indices):
    '''slices the list into given indices'''
    ls=list()
    for ind in indices:
        ls.append(lst[ind])
    return ls

def timestamps_to_strings(dic,indices):
    '''takes a table with times column and takes indices and returns all the times in these indices'''
    times=sublist(dic["StringTime"],indices)
    return times
    
def timestamps_to_strings2(dic,pairs_arr):
    '''takes a table with times column and takes (index,size) array and returns the (time,size,index) array'''
    times=sublist(dic["StringTime"],[x[0] for x in pairs_arr])
    return [[times[i],pairs_arr[i][1],pairs_arr[i][0]] for i in range(len(times))]


def up_down_connector(pairs_arr,threshold_size=0,epsilon=0):
    '''
    detects events by connection negative gradients edges to positive gradients edges of the same magnitude
    pairs_arr- an array with elements of format ('time',edge size)
    threshold_size- threshold to what counts as the minimal magnitude to count as an event
    epsilon- epsilon is the maximum distance between the absoulute value of the 2 edges
    '''
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

def addNonPairs(pairs,nonpairs,timestamp,last_index):
    '''function that fixes all the positive gradient edges that found no negative gradients ones (mostly still they are still running)'''
    t_last=dt.datetime.strptime(timestamp, '%m/%d/%y  %H:%M:%S.%f')
    for ele in nonpairs:
        t = dt.datetime.strptime(ele[0], '%m/%d/%y  %H:%M:%S.%f')
        pairs.append([ele[0],timestamp,ele[1],-ele[1],t_last-t,ele[2],last_index])
    return 0                


def filter_duration(tensor, index_time,min_time_seconds,max_time_seconds):
    '''
    filter the amount of seconds an event lasts
    tensor-input tensor
    index_time- the index in the tensor that represents the time
    min_time_seconds- minimum time for an event
    max_time_seconds - maximum time for an event
    '''
    min_t=dt.timedelta(0,min_time_seconds)
    max_t=dt.timedelta(0,max_time_seconds)
    res=[]
    for vec in tensor:
        if(vec[index_time]>=min_t and vec[index_time]<=max_t):
            res.append(vec)
    return res
            
      
def THD_avg_add(tensor,THD_dict):
    '''
    calculates the average THD over a period of an event
    '''
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
    '''
    returns the time difference of the hour of the day, independent of the date it was on
    takes as input 2 strings that represent time
    '''
    a=dt.datetime.combine(dt.date.today(),dt.datetime.strptime(t1_str, '%m/%d/%y  %H:%M:%S.%f').time())
    b=dt.datetime.combine(dt.date.today(),dt.datetime.strptime(t2_str, '%m/%d/%y  %H:%M:%S.%f').time())
    time_diff=min(abs(a-b),abs(a-b+ dt.timedelta(days=1)))
    return time_diff
    
    

def time_score(t1_str,t2_str):
    '''
    returns the score that 2 devices recieve based on the hour of the day,
    It finds the minimum amount of division of 12 hours, until we reach a period smaller than the difference between them
    minimum score 0 (12 hours difference)
    maximum score 36 (t1 equals to t2)
    time_diff of 1 second score is 20
    time_diff of 1 hour score is 32
    '''
    time_diff=get_time_difference(t1_str,t2_str)
    initial=dt.timedelta(hours=12)
    score=0
    while(time_diff<initial):
        score+=1
        initial/=2
    return 36-score    
    



class Device():
    '''
    class that represents a device
    '''
    def __init__(self,current,current_THD,start_time_arr=[],end_time_arr=[],phase=[1,0,0],phase_static=False):
        self.current=current #current
        self.current_THD=current_THD #total harmonic distortion current
        self.num_apperances=1 #number of apperances detected
        self.start_time_arr=start_time_arr #start times of device in array
        self.end_time_arr=end_time_arr  #end times of device in array
        self.fixed_power=True #whether the power is constant or changing over time
        self.phase=phase #whether the power is constant or changing over time
        self.phase_static=phase_static #flag whether the device is static in phase
        
        
    def similar(self,dev2,eps_curr,eps_THD):
        '''
        old similarity that returns True if the device is similiar to dev2 based on a few thresholds
        '''
        if(dev2.phase_static==True and sum([1 if (self.phase[i]+dev2.phase[i])>0 else 0 for i in range(len(dev2.phase))]))>1:
            #if it is on the same phase all the time and the new device is from another phase
            return False
        if(abs(self.current-dev2.current)<=eps_curr):
            if(abs(self.current_THD-dev2.current_THD)<=eps_THD):
                return True
        return False
    
    
    
        
    def similarGrade(self,dev2):
        '''
        new similarity that returns a score if the device is similiar to dev2 based on similarity in parameters
        highest score is 100 (unlikely to reach, 70-80 is close enough)
        lowest is 0
        '''
        grade=0
        alpha=[6,3,0.5,0.5]
        grade+=alpha[0]*max(5-abs(self.current-dev2.current),0)
        grade+=alpha[1]*max(5-0.5*abs(self.current_THD-dev2.current_THD),0)
        
        avg_time_score=0
        for i in range(len(self.start_time_arr)):
            avg_time_score+=time_score(self.start_time_arr[i],dev2.start_time_arr[0])
        avg_time_score/=len(self.start_time_arr)
        
        if(grade>50):
            grade+=alpha[2]*(np.clip(avg_time_score,26,36)-26)
        
        num_phase1=sum(self.phase)
        num_phase2=sum(dev2.phase)
        dist=5-5*((sum([(self.phase[i]/num_phase1-dev2.phase[i]/num_phase2)**2 for i in range(3)]))**0.5)/(2**0.5)
        
        grade+=alpha[3]*dist
        
        if(dev2.phase_static==True and sum([1 if (self.phase[i]+dev2.phase[i])>0 else 0 for i in range(len(dev2.phase))]))>1:
            #if it is on the same phase all the time and the new device is from another phase
            grade*=0
        if(dev2.current_THD>35.69 and dev2.current_THD<35.71):
            print('------------')
            print(self.start_time_arr)
            print(alpha[2]*(np.clip(avg_time_score,26,36)-26)/2)
            print(grade)
        return grade/sum(alpha)*20

    def update(self,dev2):
        #updates the devices with dev2 parameters
        n=self.num_apperances
        self.current=(self.current*n+dev2.current)/(n+1)
        self.current_THD=(self.current_THD*n+dev2.current_THD)/(n+1)
        self.num_apperances+=1
        self.phase[0]+=dev2.phase[0]
        self.phase[1]+=dev2.phase[1]
        self.phase[2]+=dev2.phase[2]
    
    def add_start_time(self,start_time):
        #add an additional start time
        self.start_time_arr.append(start_time)
    def add_end_time(self,end_time):
        #add an additional end time
        self.end_time_arr.append(end_time)
    

def print_tensor(tensor):
    '''function that prints a tensor in an easy to read format'''
    for vec in tensor:
        print("Start: %s || End: %s || Device: %d"%(vec[0],vec[1],vec[-1]))
        #print(vec)


def print_devices(list_devs):
    '''function that prints list of devices in an easy to read format'''
    for i,dev in enumerate(list_devs):
        print("DEV #%d: curr:%f, curr_THD:%f, Phase:[%d,%d,%d]:"%(i,dev.current,dev.current_THD,dev.phase[0],dev.phase[1],dev.phase[2]))



def isNewEvent(event, list_devices):
    for dev in list_devices:
        if(event[0] in dev.start_time_arr):
            return False
    return True


if __name__ == "__main__":
    
    
    
    parse_all_data(dictionary,dictionary_2days)
    tables_list=list(dictionary.keys()) #names of all the tables
    print(tables_list)
    for i in range(len(tables_list)):
        print(str(i)+"   "+tables_list[i])
        
        

    

    
    
    tablenum=2
    
    plot_graph("Administrato_output1_table%d"%tablenum,dictionary_2days,["I1 THD","I2 THD","I3 THD"],True,0)

    
    plot_graph("Administrato_output1_table%d"%tablenum,dictionary_2days,["I1","I2","I3"],True)

    
    print(dictionary_2days["Administrato_output1_table%d"%tablenum].keys())
    plot_graph("Administrato_output1_table%d"%tablenum,dictionary_2days,["Power1"],True)
    plot_graph("Administrato_output1_table%d"%tablenum,dictionary_2days,["I1","I2","I3"],True)
    
    

    
    M1=timestamps_to_strings2(dictionary_2days["Administrato_output1_table%d"%tablenum],(find_edges_abs_plus_size(dictionary_2days["Administrato_output1_table%d"%tablenum]["I1"],0.5)))
    M2=timestamps_to_strings2(dictionary_2days["Administrato_output1_table%d"%tablenum],(find_edges_abs_plus_size(dictionary_2days["Administrato_output1_table%d"%tablenum]["I2"],0.5)))
    M3=timestamps_to_strings2(dictionary_2days["Administrato_output1_table%d"%tablenum],(find_edges_abs_plus_size(dictionary_2days["Administrato_output1_table%d"%tablenum]["I3"],0.5)))

    

    

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
    
    
    '''print("up_down_connector UD1 : ")
    print_tensor(UD1)
    print()
    print("up_down_connector UD2 : ")
    print_tensor(UD2)
    print()
    print("up_down_connector UD3 : ")
    print_tensor(UD3)'''
    
    
    list_devices=list()
    device_index=list()
    
    max_grade_arr=[70,75,70]
    for phase_ind in range(len(UD_arr)):    
        for ele in UD_arr[phase_ind]: #UD1 / UD2 / UD3
            if(isNewEvent(ele,list_devices)==False):
                continue
            dev1=Device(current=0.5*(ele[2]-ele[3]),start_time_arr=[ele[0]],end_time_arr=[ele[1]],current_THD=ele[7],phase=phase_arr[phase_ind].copy())
            match_flag=False
            max_grade=0
            max_i=0
            for i,dev2 in enumerate(list_devices):
                current_grade=dev2.similarGrade(dev1)
                if(current_grade>=max_grade):
                    max_grade=current_grade
                    max_i=i
            if(max_grade>max_grade_arr[phase_ind]):
                dev2=list_devices[max_i]
                device_index.append(max_i)
                ele.append(max_i)
                dev2.update(dev1)
                dev2.add_start_time(ele[0])
                dev2.add_end_time(ele[1])
                match_flag=True
            else:
                #This is where we interact with the user and ask what device was used for the first time
                list_devices.append(dev1)
                device_index.append(len(list_devices)-1)
                ele.append(len(list_devices)-1)
                #dev1.add_start_time(ele[0])
                #dev1.add_end_time(ele[1])
       
    
    
    print()
    print("Events phase 1: ")
    print_tensor(UD1)
    print("Events phase 2: ")
    print_tensor(UD2)
    print("Events phase 3: ")
    print_tensor(UD3)
    
    print()
    print("===================")
    print("Number of devices: %d"%len(list_devices))
    print_devices(list_devices)
    print(device_index)
    
    

    
    
    plot_devices_graph(list_devices,[0,1,2,3],["Microwave","Light","Oven","Heater"],UD1,UD2,UD3,init_index="08:00:00",fin_index="16:00:00")
    
    plotTotalCost(list_devices,[0,1,2,3], price=1.0, currency_name='USD', months=6)
    


