# House Price Prediction System

A Machine Learning web application that predicts California house prices using a Random Forest Regressor. The project includes a FastAPI backend for serving predictions and a Streamlit frontend for an interactive user experience.

---

## Live Demo

**Application**

https://house-price-prediction0007.streamlit.app/

**API Documentation**

Local Development

```
http://127.0.0.1:8000/docs
```

ReDoc

```
http://127.0.0.1:8000/redoc
```

---

## Features

- Predict house prices for a single property
- Batch prediction using CSV files
- REST API built with FastAPI
- Interactive Streamlit dashboard
- CSV download after batch prediction
- Input validation using Pydantic
- Trained Random Forest Regression model
- Health check endpoint
- Automatic Swagger API documentation

---

## Tech Stack

- Python
- Scikit-learn
- FastAPI
- Streamlit
- Pandas
- Joblib
- Pydantic
- Uvicorn

---

## Machine Learning Model

Model: Random Forest Regressor

Dataset:
California Housing Dataset from Scikit-learn

Evaluation Metrics

- Mean Absolute Error (MAE)
- R² Score

The trained model is saved using Joblib and loaded into the FastAPI application for real-time inference.

---

## Project Structure

```
House-Price-Prediction/
│
├── main.py
├── train.py
├── streamlit_app.py
├── house_model.joblib
├── house_features.joblib
├── requirements.txt
├── test_houses.csv
├── .gitignore
└── README.md
```

---

## API Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | / | Home Endpoint |
| GET | /health | Health Check |
| POST | /predict | Predict a single house price |
| POST | /predict-file | Batch prediction using CSV |

---

## Installation

Clone the repository

```bash
git clone https://github.com/rajanjaiswalml/House-Price-Prediction.git
```

Move into the project directory

```bash
cd House-Price-Prediction
```

Create a virtual environment

```bash
python -m venv venv
```

Activate the virtual environment

Windows

```bash
venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## Run the Backend

```bash
uvicorn main:app --reload
```

The API will be available at

```
http://127.0.0.1:8000
```

Swagger Documentation

```
http://127.0.0.1:8000/docs
```

ReDoc Documentation

```
http://127.0.0.1:8000/redoc
```

---

## Run the Frontend

```bash
streamlit run streamlit_app.py
```

The application will be available at

```
http://localhost:8501
```

---

## Input Features

| Feature | Description |
|---------|-------------|
| MedInc | Median Income |
| HouseAge | Average House Age |
| AveRooms | Average Rooms |
| AveBedrms | Average Bedrooms |
| Population | Population |
| AveOccup | Average Occupancy |
| Latitude | Latitude |
| Longitude | Longitude |

---

## Screenshots

### Streamlit Dashboard

_Add Screenshot Here_

### Prediction Result

_Add Screenshot Here_

### Swagger API Documentation

_Add Screenshot Here_

---

## Future Improvements

- Deploy FastAPI on Render or Railway
- Docker Support
- User Authentication
- Database Integration
- Prediction History
- Model Comparison
- Feature Importance Visualization
- CI/CD Pipeline

---

## Author

**Rajan Jaiswal**

GitHub

https://github.com/rajanjaiswalml

LinkedIn

Add your LinkedIn profile here.

---

## License

This project is licensed under the MIT License.
