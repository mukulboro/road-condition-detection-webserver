import ultralytics
from ultralytics import YOLO
import matplotlib.pyplot as plt
import cv2
import os
import numpy as np

CURRENT_PATH = os.path.join(os.getcwd(), "model")
MODEL_PATH = os.path.join(CURRENT_PATH, "model.pt")

model = YOLO(MODEL_PATH)

def get_rectangle_color(class_name:str):
    match class_name:
        case "paved":
            return (255,0,0) # RED
        case "unpaved":
            return (0,255,0) # GREEN
        case "pothole":
            return (0,0,225) # BLUE
        case "crack":
            return (255,0,255) # PURPLE
        case _:
            return (0,0,0)

def get_model_predictions(result:ultralytics.yolo.engine.results.Results):
    class_names = ["paved", "unpaved", "pothole", "crack", ""]
    is_paved = False
    no_of_potholes = 0
    no_of_cracks = 0
    classes_in_image = []
    classes = (result.boxes.cls).cpu()
    boxes = (result.boxes.xyxy).numpy()
    original_image_array = result.orig_img
    image = cv2.cvtColor(original_image_array, cv2.COLOR_RGB2BGR)
    for class_index in classes:
        classes_in_image.append(class_names[int(class_index)])
    
    box_index = 0
    for box in boxes:
        has_text = False
        if classes_in_image[box_index] == "paved" or classes_in_image[box_index] == "unpaved":
            if not has_text:
                text = classes_in_image[box_index].title()
                rect_color = (255,255,255)
                text_color = (0,0,0)
                if text=="Unpaved":
                    is_paved = False
                    x,y,w,h = 0,0,300,75
                else:
                    is_paved = True
                    x,y,w,h = 0,0,200,75
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.rectangle(image, (x, x), (x + w, y + h), rect_color, -1)
                cv2.putText(image, text, (x + int(w/10)-20,y + int(h/2)+10), font, 2, text_color, 2)
                has_text = True
        else:
            if(classes_in_image[box_index] == "pothole"):
                no_of_potholes += 1
            if(classes_in_image[box_index] == "crack"):
                no_of_cracks += 1 
            start_point = (int(box[0]), int(box[1]))
            end_point = (int(box[2]), int(box[3]))
            box_color = get_rectangle_color(classes_in_image[box_index])
            image = cv2.rectangle(img=image, pt1=start_point, pt2=end_point, color=box_color, thickness=3)
        
        box_index += 1
    
    image_details = {
        "isPaved": is_paved,
        "isUnpaved": not is_paved,
        "totalPotholes": no_of_potholes,
        "totalCracks": no_of_cracks 
    }
    
    return image, image_details

def save_image(image, path):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    cv2.imwrite(path, img=image)

def get_prediction(image, output_path):
    result = model(image)
    predicted_image, image_details = get_model_predictions(result[0])
    save_image(predicted_image, output_path)
    # TODO: SAVE IMAGE DETAILS TO DATABASE
    return image_details
