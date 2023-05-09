import pymongo
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import math

uri = "mongodb+srv://bigyadhungana:e8H9t3w8tHpr0XWo@sadakvision.txhvkln.mongodb.net/?retryWrites=true&w=majority"

client=MongoClient(uri,server_api=ServerApi('1'))
db=client['SadakVision']
data_collection=db['data']

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

def add_details(details :dict ):
        data_collection.insert_one(details)



def nearby_coordinates(longitude,latitude):
        u_longitude=math.ceil(longitude)
        l_longitude=math.floor(longitude)
        u_latitude=math.ceil(latitude)
        l_latitude=math.floor(latitude)

        data_list=list(data_collection.find({"$and":[{'longitude':{'$gte':l_longitude,'$lte':u_longitude}},{'latitude':{'$gte':l_latitude,'$lte':u_latitude}}]},{'longitude':1,'latitude':1,'_id':0,'image_name':1}))
        return data_list



def return_image(username):
        final_list=[]
        img_list=list(data_collection.find({'posted_by':username},{"image_name":1,'_id':0}))
        for img in img_list:
                final_list.append(img['image_name'])
        return final_list
