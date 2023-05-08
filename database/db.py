import pymongo
from pymongo import MongoClient
import math

client=MongoClient()
db=client['SadakVision']
data_collection=db['test']

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

          
