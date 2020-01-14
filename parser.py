import sys
import os
import csv


if __name__ == "__main__":
    
    table_ChannelsRT1=[]
    with open(os.path.abspath("./firstSession/alloff/high/output\Channels RT.csv"), 'rt') as csvfile:
        #reader = csv.reader(codecs.iterdecode(csvfile, 'utf-8'))
        reader = csv.reader(csvfile)
        print(reader)
        for row in reader:
            table_ChannelsRT1.append(row)
        print(table_ChannelsRT1)
    
    table_ChannelsRT2=[]
    with open(os.path.abspath("./secondsession/alloff/high/output\Channels_RT.csv"), 'rt') as csvfile:
        #reader = csv.reader(codecs.iterdecode(csvfile, 'utf-8'))
        reader = csv.reader(csvfile)
        print(reader)
        for row in reader:
            table_ChannelsRT2.append(row)
        print(table_ChannelsRT2)

    
