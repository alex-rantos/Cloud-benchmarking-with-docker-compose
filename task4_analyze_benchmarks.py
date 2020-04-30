import pymongo
import matplotlib.pyplot as plt
from pprint import pprint
import datetime,time
import os
import math

TO_NANOSECONDS = 10**9
TO_MB = float(1<<20)

AMAZON_URL        = "http://ec2-18-207-226-187.compute-1.amazonaws.com"
MONGODB_URI       = "mongodb://" + AMAZON_URL[7:] + ":3306/"

def check_path(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def plot_graph(directory, title, x_axis, y_axis, x1, y1):
    
    fig, ax = plt.subplots()

    plt.plot(x1, y1) 
    every_nth = math.ceil(len(x1)/(len(x1)/23))
    print(every_nth)
    for n, label in enumerate(ax.xaxis.get_ticklabels()):
        if n % every_nth != 0:
            label.set_visible(False)

    plt.xlabel(x_axis) 
    plt.ylabel(y_axis) 

    plt.title(title) 
    #plt.show()
    path = "./graphs/results/"+directory[:len(directory)-5]+"/"
    check_path(path)
    plt.savefig(path+title)

def collect_data(name,collection):

    cursor = collection.find().sort('time', pymongo.ASCENDING).distinct('time')
    print(" Collecting data from collection: " + name)
    prev_time = None
    time_list = []
    mem = []
    bytes_rx_list = []
    bytes_tx_list = []
    time_diff=[]
    cpu_list=[]
    
    count = 0

    # extract all data from collection
    for time_document in cursor: 
        document = collection.find_one({'time':time_document})
        clock_time = datetime.datetime.strptime(document['time'][:19], '%Y-%m-%dT%H:%M:%S')
        
        if (count == 0):
             prev_time = clock_time
        time_difference_seconds = (clock_time - prev_time).total_seconds()
        time_diff.append(time_difference_seconds*TO_NANOSECONDS)
        time_list.append(document['time'][11:19])
        mem.append(document['mem']/TO_MB)
        cpu_list.append(document['cpu'])
        bytes_rx_list.append(document['bytesRx'])
        bytes_tx_list.append(document['bytesTx'])
        count += 1

    # Apply formula to get the cpu % use
    cpu_list = [(cpu_list[i + 1] - cpu_list[i])/(time_diff[i+1] if time_diff[i+1] != 0 else 1) for i in range(len(cpu_list)-1)] 
    # Get the difference between rx/tx_bytes
    bytes_rx_diff_list = [bytes_rx_list[i + 1] - bytes_rx_list[i] for i in range(len(bytes_rx_list)-1)] 
    bytes_tx_diff_list = [bytes_tx_list[i + 1] - bytes_tx_list[i] for i in range(len(bytes_tx_list)-1)] 
    
    # plot all data
    plot_graph(name, name+" cpu usage", "time", "cpu %" ,time_list[:len(time_list) - 1], cpu_list)
    plot_graph(name, name+" memory usage", "time", "memory (MB)" , time_list,mem)
    plot_graph(name, name+" rx_bytes", "time", "rx_bytes (Bytes)" ,time_list[:len(time_list) - 1], bytes_rx_diff_list)
    plot_graph(name, name+" tx_bytes", "time", "tx_bytes (Bytes)" ,time_list[:len(time_list) - 1], bytes_tx_diff_list)



def analyze():
    myclient = pymongo.MongoClient(MONGODB_URI)
    mydb = myclient["benchmarks"]
    mycollections = mydb.list_collection_names(include_system_collections=False)
    for collection in mycollections:
        collect_data(collection,mydb[collection])

if __name__ == "__main__":
    analyze()