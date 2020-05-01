import csv, pyodbc, glob, os, threading, time
def proc(path_list,access_driver,orig_path):
    #process for changing mdb to csv
    for path in path_list:
        #create connection string to the database
        conn=pyodbc.connect(driver=access_driver,dbq=path)
        crsr=conn.cursor()
        #grab all tables
        table_list=list(crsr.tables())
        for i in table_list:
            if(i[-2]=='TABLE'):#we only need the tables that are relevent to the measurements gained by the device
                    # run a query and get the results
                if ' ' not in i[-3]:
                    SQL = 'SELECT * FROM {}'.format(i[-3]) #a query for collecting the rows of the table
                else:
                    SQL = 'SELECT * FROM [{}]'.format(i[-3]) #a query for collecting the rows of the table
                #print("BEFORE: "+SQL+str(time.asctime( time.localtime(time.time()))))
                crsr.execute(SQL)
                #print("AFTER: "+SQL+str(time.asctime( time.localtime(time.time()))))
                rows =crsr.fetchall()
                keys=[c[0] for c in crsr.description]
                #crsr.close()
                #conn.close()
                if(os.path.exists('{}/{}.csv'.format(orig_path,os.path.basename(path)+'_'+i[-3]))):
                    os.remove('{}/{}.csv'.format(orig_path,os.path.basename(path)+'_'+i[-3]))
                with open('{}/{}.csv'.format(orig_path,os.path.basename(path)+'_'+i[-3]), 'w',newline='') as csvfile:
                    csv_writer = csv.writer(csvfile) # default field-delimiter is ","
                    csv_writer.writerow(keys)
                    for row in rows:
                        csv_writer.writerow(row)
                print(i[-3]+" in time: "+str(time.asctime( time.localtime(time.time())))) #for the user to know what time was the last time the csv file was updated
                #break
        crsr.close()
        conn.close()
    print("Done for time:"+str(time.asctime( time.localtime(time.time()))))

def main():
    print("write the number of minutes you want to pass between updates: (has to be at least 1)")
    up_time=60.0*float(input())
    print("write the path to the folder where the mdb file will be outputed to:(write it as C:/.../.../.../)")
    orig_path=input()
    path_list=glob.glob(orig_path+'/*.mdb')
    for i in path_list:
        print(i)
    #find the driver
    DataSource=pyodbc.dataSources()
    #for i in DataSource:
    #    print(i)
    access_driver=pyodbc.dataSources()['MS Access Database']
    while(True):
        threading.Timer(0, proc,args=[path_list,access_driver,orig_path]).start() #run the process
        time.sleep(up_time)
if __name__ == "__main__":
    main()
