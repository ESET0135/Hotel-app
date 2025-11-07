from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import numpy as np
import pandas as pd
import joblib
from tensorflow import keras

# Load preprocessing pipeline and trained model
preprocessor = joblib.load("preprocessor.pkl")
model = keras.models.load_model("Hotel_model.keras")

app = FastAPI()
templates = Jinja2Templates(directory="templetes")

# Your original 32 raw features (in correct order!)
features_num = [
    "lead_time", "arrival_date_week_number", "arrival_date_day_of_month",
    "stays_in_weekend_nights", "stays_in_week_nights", "adults", "children",
    "babies", "is_repeated_guest", "previous_cancellations",
    "previous_bookings_not_canceled", "required_car_parking_spaces",
    "total_of_special_requests", "adr",
]
features_cat = [
    "hotel", "arrival_date_month", "meal", "market_segment",
    "distribution_channel", "reserved_room_type", "deposit_type", "customer_type"
]
all_features = features_num + features_cat

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/predict", response_class=HTMLResponse)
async def predict(
    request: Request,
    lead_time: float = Form(...),
    arrival_date_week_number: float = Form(...),
    arrival_date_day_of_month: float = Form(...),
    stays_in_weekend_nights: float = Form(...),
    stays_in_week_nights: float = Form(...),
    adults: float = Form(...),
    children: float = Form(...),
    babies: float = Form(...),
    is_repeated_guest: float = Form(...),
    previous_cancellations: float = Form(...),
    previous_bookings_not_canceled: float = Form(...),
    required_car_parking_spaces: float = Form(...),
    total_of_special_requests: float = Form(...),
    adr: float = Form(...),
    hotel: str = Form(...),
    arrival_date_month: str = Form(...),
    meal: str = Form(...),
    market_segment: str = Form(...),
    distribution_channel: str = Form(...),
    reserved_room_type: str = Form(...),
    deposit_type: str = Form(...),
    customer_type: str = Form(...),
):
    # Create DataFrame with one row
    input_dict = {
        "lead_time": lead_time,
        "arrival_date_week_number": arrival_date_week_number,
        "arrival_date_day_of_month": arrival_date_day_of_month,
        "stays_in_weekend_nights": stays_in_weekend_nights,
        "stays_in_week_nights": stays_in_week_nights,
        "adults": adults,
        "children": children,
        "babies": babies,
        "is_repeated_guest": is_repeated_guest,
        "previous_cancellations": previous_cancellations,
        "previous_bookings_not_canceled": previous_bookings_not_canceled,
        "required_car_parking_spaces": required_car_parking_spaces,
        "total_of_special_requests": total_of_special_requests,
        "adr": adr,
        "hotel": hotel,
        "arrival_date_month": arrival_date_month,
        "meal": meal,
        "market_segment": market_segment,
        "distribution_channel": distribution_channel,
        "reserved_room_type": reserved_room_type,
        "deposit_type": deposit_type,
        "customer_type": customer_type,
    }

    df = pd.DataFrame([input_dict])

    # Apply same preprocessing
    df_processed = preprocessor.transform(df)

    # Predict
    pred_prob = model.predict(df_processed)[0][0]
    pred_class = int(pred_prob >= 0.5)

    return templates.TemplateResponse(
        "result.html",
        {
            "request": request,
            "prediction": pred_class,
            "probability": float(pred_prob),
            "features": input_dict,
        },
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
