import subprocess

myrange = [1, 5, 10, 15]
for i in myrange:
    # mu increment
    subprocess.call(["python", "./task3_loadGenerator.py", "-", "normal", str(i), str(1) , str(10)])
    if (i > 1):
        # sigma increment
        subprocess.call(["python", "./task3_loadGenerator.py", "-", "normal", str(1), str(i) ,str(10)])
    subprocess.call(["python", "./task3_loadGenerator.py", "-", "poisson", str(i), str(10)])

# high value on mu & sigma
subprocess.call(["python", "./task3_loadGenerator.py", "-", "normal", str(10), str(10) , str(10)])