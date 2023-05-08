from fastapi import FastAPI,File,UploadFile
from fastapi.responses import RedirectResponse,FileResponse
from fastapi.staticfiles import StaticFiles
from datetime import date,datetime
import database.db
import model.pred
import base64
from PIL import Image
from io import BytesIO
import os
import uuid

OUT_PATH="out_images"

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
    given_info= {}
    given_info['posted_by']=username
    given_info['longitude']=longitude
    given_info['latitude']=latitude
    given_info['uploaded_date']=current_date
    given_info['uploaded_time']=current_time
    given_info['image_name']=image_name
    #PIL Image
    img_details = predict(image_string, output_path=os.path.join(OUT_PATH, image_name))

    given_info['is_paved']=img_details["isPaved"]
    given_info['is_unpaved']=img_details["isUnpaved"]
    given_info['no_of_cracks']=img_details["totalPotholes"]
    given_info['no_of_potholes']=img_details["totalCracks"]

    database.db.add_details(given_info)
    
    return img_details
    

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
    

def predict(image_s:str, output_path):
    image_s = image_s.rstrip().lstrip()
    image_s = image_s.split(",")
    try:
        image_s = image_s[1]
    except IndexError:
        image_s = image_s[0]
    decoded_img_bytes=base64.urlsafe_b64decode(image_s)
    decoded_image=BytesIO(decoded_img_bytes)
    img=Image.open(decoded_image)
    img_details = model.pred.get_prediction(image=img, output_path=output_path)
    return img_details

    
