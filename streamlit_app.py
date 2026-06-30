import streamlit as st
import requests
import pandas as pd

# ----------------- CONFIG -----------------
API_URL = "https://house-price-api-ekwk.onrender.com"

st.set_page_config(
    page_title="House Price Prediction",
    page_icon="🏠",
    layout="wide"
)

st.title("🏠 California House Price Prediction")
st.markdown("Predict house prices using a Random Forest model.")

# ----------------- SIDEBAR -----------------

st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Choose Page",
    ["Single Prediction", "Batch Prediction"]
)

# ==========================================================
# SINGLE PREDICTION
# ==========================================================

if page == "Single Prediction":

    st.header("🏡 Predict Single House Price")

    col1, col2 = st.columns(2)

    with col1:
        MedInc = st.number_input("Median Income", value=8.32)
        HouseAge = st.number_input("House Age", value=41.0)
        AveRooms = st.number_input("Average Rooms", value=6.98)
        AveBedrms = st.number_input("Average Bedrooms", value=1.02)

    with col2:
        Population = st.number_input("Population", value=322.0)
        AveOccup = st.number_input("Average Occupancy", value=2.55)
        Latitude = st.number_input("Latitude", value=37.88)
        Longitude = st.number_input("Longitude", value=-122.23)

    if st.button("🚀 Predict"):

        payload = {
            "MedInc": MedInc,
            "HouseAge": HouseAge,
            "AveRooms": AveRooms,
            "AveBedrms": AveBedrms,
            "Population": Population,
            "AveOccup": AveOccup,
            "Latitude": Latitude,
            "Longitude": Longitude
        }

        with st.spinner("Predicting..."):

            response = requests.post(
                f"{API_URL}/predict",
                json=payload
            )

        if response.status_code == 200:

            result = response.json()

            st.success("Prediction Successful!")

            st.metric(
                "Predicted Price",
                result["predicted_price"]
            )

            st.info(result["predicted_price_short"])

            st.warning(
                f"Confidence Range: {result['fidence_range']}"
            )

        else:
            st.error(response.json()["detail"])

# ==========================================================
# BATCH PREDICTION
# ==========================================================

else:

    st.header("📂 Batch Prediction")

    uploaded_file = st.file_uploader(
        "Upload CSV File",
        type="csv"
    )

    if uploaded_file is not None:

        df = pd.read_csv(uploaded_file)

        st.subheader("Preview")

        st.dataframe(df)

        uploaded_file.seek(0)

        if st.button("Predict CSV"):

            files = {
                "file": (
                    uploaded_file.name,
                    uploaded_file,
                    "text/csv"
                )
            }

            with st.spinner("Processing..."):

                response = requests.post(
                    f"{API_URL}/predict-file",
                    files=files
                )

            if response.status_code == 200:

                st.success("Prediction Completed!")

                st.download_button(
                    label="⬇ Download Predictions",
                    data=response.content,
                    file_name="predictions.csv",
                    mime="text/csv"
                )

            else:
                st.error(response.json()["detail"])