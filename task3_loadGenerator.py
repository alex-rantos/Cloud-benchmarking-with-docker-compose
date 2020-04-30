import numpy as np
import matplotlib.pyplot as plt

import urllib.request 
import requests
import pymongo
import json

import sys, os
import time

AMAZON_URL        = "http://ec2-18-207-226-187.compute-1.amazonaws.com"
AMAZON_URL_APP    = AMAZON_URL + "/primecheck"

CADVISOR_API_URL1 = AMAZON_URL + ":8080/api/v1.3/containers/docker/6c9de2d273ebbd0fcde484fa1cea6bd78eda2caa1761fdf41cda1636c26810cc"
CADVISOR_API_URL2 = AMAZON_URL + ":8080/api/v1.3/containers/docker/786a71077cf611fcb5283c18265ffe849761ccdef66ccb8d9230225a0502cd70"
MONGODB_URI       = "mongodb://" + AMAZON_URL[7:] + ":3306/"

def check_path(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def readJSON(response,time_list):
    """ 
    Save following values :
    timestamp
    memory usage
    cpu total usage
    Bytes_tx/rx
    """
    mylist = []
    for s in response['stats']:
        if (s['timestamp']) in time_list:
            #print(s['timestamp'] + " already in list")
            continue
        else:
            time_list.append(s['timestamp'])
            #print(s['timestamp'] + " added in list")

        for n in s['network']['interfaces']:
            #print(n)
            if (n['name'] == 'eth1'):
                bytes_tx = n['tx_bytes']
                bytes_rx = n['rx_bytes']

        databaseEntry = {
            "time"    : s['timestamp'],
            "cpu"     : s['cpu']['usage']['total'],
            "mem"     : s['memory']['usage'],
            "bytesRx" : bytes_rx,
            "bytesTx" : bytes_tx
        }
        mylist.append(databaseEntry.copy())
    return mylist
    
def monitor(sleepAmount,t1,t2):
    print("Next attemp after %s seconds" % sleepAmount)

    response1 = json.loads(requests.get(CADVISOR_API_URL1).text)
    dbEntriesList1 = readJSON(response1,t1)
    response2 = json.loads(requests.get(CADVISOR_API_URL2).text)
    dbEntriesList2 = readJSON(response2,t2)
    return [dbEntriesList1,dbEntriesList2]

def send_request(mydb, values, file_name, url, time_list1, time_list2):
    
    mongo_collection_1 = mydb[file_name + "_app1"]
    mongo_collection_2 = mydb[file_name + "_app2"]
    plt.xlabel("Seconds") 
    plt.ylabel("Times occured") 
    # create histogram and save it
    plt.hist(values,50)
    path = "./graphs/"
    check_path(path)
    plt.title(file_name)
    plt.savefig(path+file_name)
    for number in values:
        response = urllib.request.urlopen(url)
        print(response)
        if (number < 0):
            number = abs(number)
        dBentriesList = monitor(number,time_list1,time_list2)
        mongo_collection_1.insert_many(dBentriesList[0], ordered = False)
        mongo_collection_2.insert_many(dBentriesList[1], ordered = False)
        time.sleep(number)

def main(args):
    # count the arguments
    arguments = len(args) - 1
   # databaseUpdate({});

    if (arguments < 4 or arguments > 5):
        print("One of the following arguments are wrong :")
        print(args[1:])
        raise Exception("Wrong arguments. Must be [stringOfURL || '-'] {'normal' [numberOfM] [numberOfS] || 'poison' [numberOfLamda]} [numberOfIterations]")

    # if - is inserted for url assign AMAZON_URL
    url = args[1]
    if AMAZON_URL_APP != url:
        print("You did not selected AWS.")
        if url == "-":
            url = AMAZON_URL_APP
            print("- was inserted for url so the url was auto assigned to AWS url")

    inter_request = args[2]

    myclient = pymongo.MongoClient(MONGODB_URI)
    dblist = myclient.list_database_names()
    time_list1 = []
    time_list2 = []
    mydb = myclient["benchmarks"]

    if (inter_request == "normal" or inter_request == "Normal"):
        if(arguments != 5):
            raise Exception("Wrong arguments. Must be [stringOfURL || '-'] {'normal' [numberOfM] [numberOfS] || 'poison' [numberOfLamda]} [numberOfIterations]")

        if (not args[3].isnumeric):
            raise Exception("Parameters for normal distributions must be numbers. m not = number")
        m = int(args[3])

        if (not args[4].isnumeric):
            raise Exception("Parameters for normal distributions must be numbers. s not = number")
        s = int(args[4])
        
        if (not args[5].isnumeric):
            raise Exception("Parameters for normal distributions must be numbers. iterations not = number")
        iterations = int(args[5])

        file_name = inter_request + "_" + args[3] + "_" + args[4]

        values = np.random.normal(m,s,iterations)
            
        send_request(mydb, values, file_name, url, time_list1, time_list2)

    elif inter_request == "poisson" or inter_request == "Poisson":

        if(arguments != 4):
            raise Exception("Wrong arguments. Must be [stringOfURL || '-'] {'normal' [numberOfM] [numberOfS] || 'poison' [numberOfLamda]} [numberOfIterations]")

        if (not args[3].isnumeric):
            raise Exception("Parameters for normal distributions must be numbers. l not = number")
        l = int(args[3])
        
        if (not args[4].isnumeric):
            raise Exception("Parameters for normal distributions must be numbers. iterations not = number")
        iterations = int(args[4])

        file_name = inter_request + "_" + args[3]
        values = np.random.poisson(l,iterations)
        send_request(mydb, values, file_name, url, time_list1, time_list2)
        
    else:
        print("Second argument: [%s] is wrong. Must be either Normal or Poisson" % inter_request)
    

if __name__ == "__main__":
    main(sys.argv)
