import matplotlib.pyplot as plt
import numpy as np
import math
import sys

args = sys.argv
# count the arguments
arguments = len(args) - 1
# databaseUpdate({});

if (arguments < 4 or arguments > 5):
    print("One of the following arguments are wrong :")
    print(args[1:])
    raise Exception("Wrong arguments. Must be [stringOfURL || '-'] {'normal' [numberOfM] [numberOfS] || 'poison' [numberOfLamda]} [numberOfIterations]")

# if - is inserted for url assign AMAZON_URL
url = args[1]

interRequest = args[2]

if (interRequest == "normal" or interRequest == "Normal"):
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
    fileName = interRequest + "_" + args[3] + "_" + args[4]
    values = np.random.normal(m,s,iterations)
    plt.hist(values,50)
    plt.savefig("./"+fileName)

        

elif interRequest == "poisson" or interRequest == "Poisson":
    if(arguments != 4):
        raise Exception("Wrong arguments. Must be [stringOfURL || '-'] {'normal' [numberOfM] [numberOfS] || 'poison' [numberOfLamda]} [numberOfIterations]")

    if (not args[3].isnumeric):
        raise Exception("Parameters for normal distributions must be numbers. l not = number")
    l = int(args[3])
    
    if (not args[4].isnumeric):
        raise Exception("Parameters for normal distributions must be numbers. iterations not = number")
    iterations = int(args[4])
    
    fileName = interRequest + "_" + args[3] 
    values = np.random.poisson(l,iterations)
    plt.hist(values,50)
    plt.show()
        
else:
    print("Second argument: [%s] is wrong. Must be either Normal or Poisson" % interRequest)