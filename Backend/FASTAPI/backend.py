import os
from io import BytesIO
import tempfile
import cv2
import joblib
import numpy as np
from PIL import Image
import uvicorn
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi import HTTPException

# Load the model from the file
path = "Backend/FASTAPI/Model.joblib"  
MODEL = joblib.load(path)

app = FastAPI()

# CORS middleware
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Flower details for different classes
flower_details = {
    "daisy": {
        "scientific_name": "Bellis perennis",
        "description": "Daisies are small, herbaceous perennial plants native to Europe and North America.",
        "habitat": "Grasslands, meadows, gardens.",
        "uses": "Ornamental, herbal (medicinal use)."
    },
    "dandelion": {
        "scientific_name": "Taraxacum",
        "description": "Dandelions are a family of flowering plants that grow in many parts of the world.",
        "habitat": "Fields, lawns, gardens.",
        "uses": "Edible leaves, roots used in herbal medicine."
    },
    "tulip": {
        "scientific_name": "Tulipa",
        "description": "Tulips are spring-blooming perennial herbaceous bulbiferous geophytes.",
        "habitat": "Originally from Turkey and later cultivated in various regions.",
        "uses": "Ornamental, cultural (symbolism)."
    },
    "orchid": {
        "scientific_name": "Orchidaceae",
        "description": "Orchids are diverse and widespread flowering plants, with blooms that are often colourful and fragrant.",
        "habitat": "Varies greatly depending on species, found on every continent except Antarctica.",
        "uses": "Ornamental, medicinal, culinary (vanilla orchid)."
    },
    "lily": {
        "scientific_name": "Lilium",
        "description": "Lilies are tall perennials ranging in height from 2 to 6 feet.",
        "habitat": "Temperate northern hemisphere regions.",
        "uses": "Ornamental, medicinal (some species)."
    },
    "lotus": {
        "scientific_name": "Nelumbo nucifera",
        "description": "Lotus is a genus of aquatic plants with large, showy flowers.",
        "habitat": "Found in various parts of Asia, Australia, and North America.",
        "uses": "Cultural and religious significance, ornamental."
    },
    "sunflower": {
        "scientific_name": "Helianthus annuus",
        "description": "Sunflowers are tall, annual plants with large flower heads.",
        "habitat": "Native to the Americas, now cultivated worldwide.",
        "uses": "Oil production, ornamental, birdseed."
    },
    "rose": {
        "scientific_name": "Rosa",
        "description": "Roses are woody perennial flowering plants of the genus Rosa, in the family Rosaceae.",
        "habitat": "Various habitats depending on species, often in gardens.",
        "uses": "Ornamental, medicinal, culinary (rose hips)."
    }
}

# Function to extract features from an image file
def extract_features(image_path):

    image = cv2.imread(image_path)
    resized_image = cv2.resize(image, (256, 256))  # Resize image if needed
    hist = cv2.calcHist([resized_image], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
    hist = cv2.normalize(hist, hist).flatten()
    return hist

# Function to read and process uploaded image data
def read_files(data):
    try:
        image = Image.open(BytesIO(data))
        cv_image = np.array(image)
        
        cv_image= cv2.cvtColor(cv_image, cv2.COLOR_RGB2BGR)
        # Save and process the image for feature extraction
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as temp_file:
            cv2.imwrite(temp_file.name, cv_image)
            temp_file_path = temp_file.name
        
        # Extract features from the processed image
        features = extract_features(temp_file_path)
        
        return features
    
    except Exception as e:
        print(f"Error in reading image: {str(e)}")
        raise HTTPException(status_code=400, detail="Error: Unable to process image data")

# Function to predict flower class from extracted features
def predict_flower_class(features):
    try:
        predicted_class= MODEL.predict(features.reshape(1, -1))[0]
        probabilities = MODEL.predict_proba(features.reshape(1, -1))[0]
        class_labels = MODEL.classes_
        # print(MODEL.classes_)
        # print(predicted_class)
        predicted_class_index = np.where(class_labels == predicted_class)[0][0]
        confidence = probabilities[predicted_class_index]
        predicted_class = class_labels[predicted_class_index]
        return predicted_class, round(confidence*100,2)
    
    except Exception as e:
        print(f"Error in prediction: {str(e)}")
        raise HTTPException(status_code=500, detail="Error: Unable to make predictions")

# Route to handle image upload and prediction
@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        features = read_files(await file.read())
        predicted_class, confidence = predict_flower_class(features)
        
        details = flower_details.get(predicted_class.lower(), {})
        print(f"Predicted class: {predicted_class}, Confidence: {confidence}")
        print(f"Details: {details}")
        
        return {
            "predicted_class": predicted_class,
            "Confidence": confidence,
            "details": details
        }
    
    except Exception as e:
        print(f"Error in prediction: {str(e)}")
        raise HTTPException(status_code=500, detail="Error: Unable to process image and make predictions")

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)

