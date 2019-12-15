import pymongo

AMAZON_URL        = "http://ec2-18-207-226-187.compute-1.amazonaws.com"
MONGODB_URI       = "mongodb://" + AMAZON_URL[7:] + ":3306/"

def clear_database():
    myclient = pymongo.MongoClient(MONGODB_URI)
    myclient.drop_database("benchmarks")

if __name__ == "__main__":
    clear_database()