from fastapi import FastAPI,File,UploadFile
from fastapi.responses import RedirectResponse,FileResponse
from fastapi.staticfiles import StaticFiles
from datetime import date,datetime
import database.db
import base64
from PIL import Image
from io import BytesIO
import os
import uuid

saved_img_directory="D:/img"

app = FastAPI()

@app.get("/health")
async def health():
    return {"health":True}


@app.post("/post")
def post_details(longitude:float,latitude :float,username:str,image_string:str):

    """
    ROUTE TO POST IMAGE ALONG WITH LONGITUDE,LATITUDE

    """
   
    current_date=date.today().strftime("%B %d, %Y")
    current_time=datetime.now().strftime("%H:%M")
    
    image_name=str(uuid.uuid4())+".jpg"

    #dictionary
    given_info={}
    given_info['posted_by']=username
    given_info['longitude']=longitude
    given_info['latitude']=latitude
    given_info['uploaded_date']=current_date
    given_info['uploaded_time']=current_time
    given_info['image_name']=image_name
    database.db.add_details(given_info)

    #PIL Image
    img=decode_img(image_string)

    img.save(saved_img_directory+"/"+image_name)
    
    return "done"
    

@app.get("/road_info")
def get_users_info():
    """ROUTE TO RECEIVE REQUIRED DATA"""
    #under construction 
    return ":("


@app.get("/view-image/{image_name}")
def get_image(image_name:str):
    """
    SERVES IMAGE WHEN GIVEN IMAGE NAME
    """
    for image in os.listdir(saved_img_directory):
        if (image==image_name):
            return FileResponse(saved_img_directory+"/"+image_name)
    return (f"{image_name} doesnot exists")


@app.get("/get_user_contibutions")
def return_list(username):
    return database.db.return_image(username)
    

def decode_img(image_s):
    decoded_img_bytes=base64.b64decode(image_s)
    decoded_image=BytesIO(decoded_img_bytes)
    img=Image.open(decoded_image)
    #img.show()
    return img 
    
