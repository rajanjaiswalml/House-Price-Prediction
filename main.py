from importlib.resources import contents
import io
import joblib
import pandas as pd
from fastapi import FastAPI , HTTPException, UploadFile, File
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field


app = FastAPI()


model = joblib.load("house_model.joblib")
features = joblib.load("house_features.joblib")

#input Schema
class HouseFeatures(BaseModel):
    MedInc: float = Field(gt=0, description="Median income of Neighbourhood")
    HouseAge: float = Field(gt=0, description="Average age of houses in the block")
    AveRooms: float = Field(gt=0, description="Average number of rooms per household")
    AveBedrms: float = Field(gt=0, description="Average number of bedrooms per household")
    Population: float = Field(gt=0, description="Block group population")
    AveOccup: float = Field(gt=0, description="Average number of household members")
    Latitude: float = Field(ge=32, le=42, description="Block group latitude")
    Longitude: float = Field(ge=-125, le=114, description="Block group longitude")
    
@app.get("/")
def home():
    return {"message": "Welcome to the California Housing Price Prediction API",
            "status": "API is running successfully",
            "endpoints":"send POST request to predict"
        }
    
@app.get("/health")
def health():
    return {"status": "API is running successfully",
            "model": "Random Forest Regressor",
            "features": features,
            "avg_error": "average error: $33,000"
        }
    
#schema for prediction

@app.post("/predict")
def predict(house: HouseFeatures):
    try:
        input_data = pd.DataFrame([{
            "MedInc": house.MedInc,
            "HouseAge": house.HouseAge,
            "AveRooms": house.AveRooms,
            "AveBedrms": house.AveBedrms,
            "Population": house.Population,
            "AveOccup": house.AveOccup,
            "Latitude": house.Latitude,
            "Longitude": house.Longitude
        }])
        
        predicted = model.predict(input_data)[0]
        price_usd = predicted * 100000
        
        return {"predicted_price": f"${price_usd:,.0f}",
                "predicted_price_short": f"${predicted:.2f} hundred thousand dollars",
                "fidence_range": f"${price_usd - 33000:,.0f}to ${price_usd + 33000:,.0f}"
                
            }
        
    except Exception as e:
        raise HTTPException(
            status_code=400, 
            detail=f"prediction failed: {str(e)}")
        
        
@app.post("/predict-file")
async def predict_file(file: UploadFile = File(...)):
    
    if not file.filename.endswith('.csv'):
        raise HTTPException(
            status_code=400, 
            detail="Invalid file format. Please upload a CSV file."
        )
        
    contents = await file.read()

    df = pd.read_csv(io.BytesIO(contents))
    df.columns = df.columns.str.strip()
    
    required_columns = [
        'MedInc', 'HouseAge', 'AveRooms', 'AveBedrms',
        'Population', 'AveOccup', 'Latitude', 'Longitude'
    ]
    
    missing_columns = [
        col for col in required_columns 
        if col not in df.columns
    ]
    
    if missing_columns:
        raise HTTPException(
            status_code=400, 
            detail=f"Missing required columns: {missing_columns}"
        )
        
    if len(df) == 0:
        raise HTTPException(
            status_code=400, 
            detail="The uploaded CSV file is empty."
        )
        
    try:
        predictions = model.predict(df[required_columns])

        df["PredictedPriceUSD"] = [
            f"${x * 100000:,.0f}"
            for x in predictions
        ]

        output = df.to_csv(index=False)

        return StreamingResponse(
            io.StringIO(output),
            media_type="text/csv",
            headers={
                "Content-Disposition":
                "attachment; filename=predictions.csv"
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=400, 
            detail=f"Prediction failed: {str(e)}"
        )
        