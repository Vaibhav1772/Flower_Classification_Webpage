from fastapi import FastAPI,File,UploadFile
import uvicorn
import numpy as np
from io import BytesIO
import tensorflow as tf
from PIL import Image
from fastapi.middleware.cors import CORSMiddleware

MODEL=tf.keras.models.load_model("D:\Models")
CLASS_NAMES=["Aster","Daisy","Iris","Lavender","Lily","Marigold","Orchid","Poppy","Rose","Sunflower"]

app= FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1:5500",
    
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

@app.get("/ping")
async def ping():
    return "HELLOWORLD"

def read_files(data)->np.ndarray:
    image=Image.open(BytesIO(data))
    
    image=image.resize((256, 256))
    new_image=np.array(image)
    ##image=np.reshape(256,256,3)
    img_batch=np.expand_dims(new_image,0)
    
    predictions=MODEL.predict(img_batch)
    index=np.argmax(predictions[0])
    predict_class=CLASS_NAMES[index]
    print(predict_class)
    return predict_class


@app.post("/predict")
async def predict(file:UploadFile=File(...)):
    bytes=read_files(await file.read())
    return{
        
        "PREDICTED ":bytes
    }

if __name__=="__main__":
    uvicorn.run(app,host='localhost',port=8000)