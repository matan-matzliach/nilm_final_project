import csv, pyodbc, glob, os, threading, time
def proc(path_list,access_driver):
    #process for changing mdb to csv
    for path in path_list:
        #create connection string to the database
        conn=pyodbc.connect(driver=access_driver,dbq=path)
        crsr=conn.cursor()
        #grab all tables
        table_list=list(crsr.tables())
        for i in table_list:
            print(i[-3]+" in time: "+str(time.asctime( time.localtime(time.time()))))
        for i in table_list:
            if(i[-2]=='TABLE'):
                    # run a query and get the results
                if ' ' not in i[-3]:
                    SQL = 'SELECT * FROM {}'.format(i[-3]) # your query goes here
                else:
                    SQL = 'SELECT * FROM [{}]'.format(i[-3]) # your query goes here
                #print(SQL)
                crsr.execute(SQL)
                rows =crsr.fetchall()
                keys=[c[0] for c in crsr.description]
                #crsr.close()
                #conn.close()
                with open('a/{}.csv'.format(os.path.basename(path)+'_'+i[-3]), 'w',newline='') as csvfile:
                    csv_writer = csv.writer(csvfile) # default field-delimiter is ","
                    csv_writer.writerow(keys)
                    for row in rows:
                        csv_writer.writerow(row)
                #break
        crsr.close()
        conn.close()
def printit(path_list,access_driver):
  #threading process to make the convertion run every 5 minutes
  threading.Timer(300, proc,args=[path_list,access_driver]).start()
  #proc(path_list,access_driver)

def main():
    print("write the path to the folder where the mdb file will be outputed to.(write it as C:/.../.../.../")
    orig_path=input()
    path_list=glob.glob(orig_path+'/*.mdb')
    for i in path_list:
        print(i)
    #find the driver
    DataSource=pyodbc.dataSources()
    #for i in DataSource:
    #    print(i)
    access_driver=pyodbc.dataSources()['MS Access Database']
    printit(path_list,access_driver)
    proc(path_list,access_driver)
    while(True):
        a="a" #a line for stalling
if __name__ == "__main__":
    main()
