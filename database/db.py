import pymongo
from pymongo import MongoClient

client=MongoClient()
db=client['SadakVision']
data_collection=db['test']

def add_details(details :dict ):
        data_collection.insert_one(details)



# def find_details():
#         info=list(data_collection.find({'name':'im'}))
#         for items in info:
#                 print(info)

