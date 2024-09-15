import numpy as np
import pickle
import streamlit as st
from mappings import weather_mappings,direction_mapping,reversedict

# Load model
model = pickle.load(open("conditions_model.pkl", "rb"))

# Mapping dictionaries
weather_conditions = weather_mappings
wind_directions = direction_mapping

# Streamlit app
def main():
    st.title("Weather Prediction App")

    # Form to input data
    with st.form(key='prediction_form'):
        st.header("Enter the weather details:")

        
        # Sliders for numerical inputs
        temperature = st.slider("Temperature (°C)", -10, 50, 0)
        pressure = st.slider("Pressure (hPa)", 900, 1050, 1013)
        humidity = st.slider("Humidity (%)", 0, 100, 50)
        dew = st.slider("Dew Point (°C)", -10, 30, 0)
        vism = st.text_input("Visibility (in km)")
        
        fog = st.checkbox("Fog", value=False)
        
        # Dropdown for wind direction
        wind_direction = st.selectbox(
            "Wind Direction",
            list(wind_directions.keys())
        )

        wind_direction_value = wind_directions[wind_direction]
        wind_speed = st.text_input("Wind Speed")

        # Convert checkbox inputs to 0 or 1
        fog = int(fog)
        
        # Convert selected wind direction to corresponding integer value
        wind_direction_value = wind_directions[wind_direction]

        submit_button = st.form_submit_button("Predict")

    if submit_button:
        #Convert to integer values
        try:
            input_features = [
                int(dew),
                int(fog),
                int(humidity),
                int(pressure),
                int(temperature),
                int(vism),
                int(wind_direction_value),
                int(wind_speed) 
            ]
        except:
            st.error("Invalid input. Please enter a valid value for each field.")
            return
        
        features = [np.array(input_features)]
        probabilities = model.predict_proba(features)[0]
        sorted_indices = np.argsort(probabilities)[:-4:-1]
        probabilities = sorted(probabilities)[::-1]
        dict1 = {}
        for index in range(3):
            class_label = reversedict[sorted_indices[index]]
            probability = probabilities[index] * 100
            dict1[class_label] = round(probability,2)
        

        st.markdown(
        """
        <style>
            .centered-header {
                text-align: center;
            }
        </style>
        <h1 class="centered-header">Predicted weather conditions : </h1>
        """,
        unsafe_allow_html=True
        )
        
        # Result box styling
        try:
            label1 = reversedict[sorted_indices[0]]
            label2= reversedict[sorted_indices[1]]
            label3 = reversedict[sorted_indices[2]]
            pred1 = round((probabilities[0] * 100),2)
            pred2 = round((probabilities[1] * 100),2)
            pred3 = round((probabilities[2] * 100),2)
            st.markdown(f"""
                <style>
                .weather-box-wrapper {{
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                }}
                .weather-box {{
                    padding: 10px;
                    color: white;
                    border-radius: 5px;
                    display: inline-block;
                    font-size: 20px;
                    font-weight: bold;
                    margin: 5px;
                    width: 200px; /* Adjust width as needed */
                }}
                .weather-box-1 {{
                    background-color: #4CAF50; /* Green background */
                    font-size: 24px; /* Largest size */
                    width: 250px; /* Adjust size as needed */
                }}
                .weather-box-2 {{
                    background-color: #FFEB3B; /* Yellow background */
                    font-size: 22px; /* Medium size */
                    width: 220px; /* Adjust size as needed */
                }}
                .weather-box-3 {{
                    background-color: #F44336; /* Red background */
                    font-size: 20px; /* Smallest size */
                    width: 200px; /* Adjust size as needed */
                }}
                .weather-label {{
                    font-size: 18px;
                    font-weight: normal;
                }}
                </style>
                <div class="weather-box-wrapper">
                    <div class="weather-box weather-box-1">
                        <div>Weather conditions:</div>
                        <div class="weather-label">1. {label1}: {pred1}%</div>
                    </div>
                    <div class="weather-box weather-box-2">
                        <div class="weather-label">2. {label2}: {pred2}%</div>
                    </div>
                    <div class="weather-box weather-box-3">
                        <div class="weather-label">3. {label3}: {pred3}%</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)        

        except:
            st.error("Error occurred during prediction. Please check inputs and try again.")
if __name__ == "__main__":
    main()
