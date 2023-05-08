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

def return_image(username):
        final_list=[]
        img_list=list(data_collection.find({'posted_by':username},{"image_name":1,'_id':0}))
        for img in img_list:
                final_list.append(img['image_name'])
        return final_list
                
