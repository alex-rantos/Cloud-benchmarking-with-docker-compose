import pymongo
import matplotlib.pyplot as plt
from pprint import pprint
import datetime

TO_NANOSECONDS = 10**9
TO_MB = 10**6

AMAZON_URL        = "http://ec2-18-207-226-187.compute-1.amazonaws.com"
MONGODB_URI       = "mongodb://" + AMAZON_URL[7:] + ":3306/"

def plot_graph(title,x_axis,y_axis,x,y):
    
    fig, ax = plt.subplots()

    plt.plot(x, y) 
        
    every_nth = len(x)/10
    for n, label in enumerate(ax.xaxis.get_ticklabels()):
        if n % every_nth != 0:
            label.set_visible(False)

    plt.xlabel(x_axis) 
    plt.ylabel(y_axis) 

    plt.title(title) 
    
    plt.savefig("./graphs/"+title)

def draw_graphs(name,collection):

    cursor = collection.find().sort('time', pymongo.ASCENDING).distinct('time')
    print(" ----------------------" + name)
    prev_time = None
    time_list = []
    cpu = []
    mem = []
    bytes_rx_list = []
    bytes_tx_list = []
    time_diff=[]
    cpu_list=[]
    
    count = 0

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

    cpu_list = [(cpu_list[i + 1] - cpu_list[i])/time_diff[i+1] for i in range(len(cpu_list)-1)] 
    print(cpu_list)
    bytes_rx_diff_list = [bytes_rx_list[i + 1] - bytes_rx_list[i] for i in range(len(bytes_rx_list)-1)] 
    bytes_tx_diff_list = [bytes_tx_list[i + 1] - bytes_tx_list[i] for i in range(len(bytes_tx_list)-1)] 

    print(time_list)
    
    print(count)
    print(cpu)
    
    plot_graph(name+" cpu usage", "time", "cpu %" ,time_list[:len(time_list) - 1], cpu_list)
    plot_graph(name+" memory usage", "time", "memory (MB)" , time_list,mem)

    plot_graph(name+" rx_bytes", "time", "bytes" ,time_list[:len(time_list) - 1], bytes_rx_diff_list)
    plot_graph(name+" tx_bytes", "time", "bytes" ,time_list[:len(time_list) - 1], bytes_tx_diff_list)

    print(mem)
    print(bytes_rx_diff_list)
    print(bytes_tx_diff_list)

def analyze():
    myclient = pymongo.MongoClient(MONGODB_URI)
    mydb = myclient["benchmarks"]
    mycollections = mydb.collection_names(include_system_collections=False)

    for collection in mycollections:
       # print(mydb[collection].count())
        draw_graphs(collection,mydb[collection])


if __name__ == "__main__":
    analyze()