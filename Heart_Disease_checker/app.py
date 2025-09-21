import streamlit as st
import pandas as pd
import pickle

st.set_page_config(page_title="Heart Disease Predictor", page_icon="❤️", layout="wide")

# --- Custom CSS for Light Gradient and Reduced Top Space ---
st.markdown("""
<style>
:root {
  --mint: #E6FFF7;
  --blue: #E6F7FF;
  --green: #F0FFF0;
  --ivory: #FDFDFC;
  --pink: #F4C2DF;
  --card-bg: rgba(255,255,255,0.76);
  --card-border: rgba(240,240,240,0.46);
  --shadow: 0 10px 28px rgba(0,0,0,0.11);
}
.stApp {
  background: linear-gradient(115deg, var(--mint) 0%, var(--ivory) 50%, var(--blue) 100%);
  background-attachment: fixed;
  background-size: cover;
}
.card {
  background: var(--card-bg);
  border: 1px solid var(--card-border);
  border-radius: 18px;
  padding: 24px;
  box-shadow: var(--shadow);
  backdrop-filter: blur(12px);
  margin-bottom: 26px;
}
h1, h2, h3 {
  color: #359da0;
  letter-spacing: 0.3px;
}
div.block-container {padding-top:1.5rem;}
/* Buttons: pastel blue gradient with mint border */
div.stButton > button:first-child {
  background: linear-gradient(120deg, var(--blue) 0%, var(--mint) 100%);
  color: #339993;
  font-size: 18px;
  font-weight: 700;
  padding: 12px 28px;
  border-radius: 12px;
  border: 2px solid #d0f8ee;
  box-shadow: 0 6px 16px rgba(53,157,160,0.14);
  transition: transform .11s, box-shadow .11s;
  width: 100%;
}
div.stButton > button:first-child:hover {
  background: linear-gradient(120deg, var(--mint) 0%, var(--blue) 100%);
  box-shadow: 0 12px 20px rgba(53,157,160,0.18);
}
[data-testid="stSuccess"], [data-testid="stError"], [data-testid="stWarning"], [data-testid="stInfo"] {
  border-radius: 15px;
  border: 1px solid rgba(200,230,216,0.15);
  box-shadow: 0 6px 14px rgba(53,157,160,0.08);
}
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR: Feature Explanations in Easy Language ---
st.sidebar.title("🩺 Feature Information")
st.sidebar.markdown("""
**Chest Pain Type (cp):**  
Type of chest pain – can be typical angina (heart-related), pain not related to heart, or no symptoms.

**Resting Blood Pressure (trestbps):**  
Blood pressure measured when resting (in mm Hg).

**Serum Cholesterol (chol):**  
Amount of cholesterol in your blood (mg/dL).

**Fasting Blood Sugar (fbs):**  
Is fasting blood sugar above 120 mg/dl? (True/False).

**Resting ECG (restecg):**  
Result of basic heart electrical test (normal or showing changes).

**Max Heart Rate Achieved (thalach):**  
Highest heart rate recorded during exercise.

**Exercise Induced Angina (exang):**  
Chest pain triggered by exercise (Yes/No).

**ST Depression (oldpeak):**  
A dip in a specific ECG line during exercise, showing possible heart stress.

**Slope:**  
Pattern of the ECG line during exercise (upwards, flat, or downwards).

**Number of Vessels Colored by Fluoroscopy (ca):**  
Major blood vessels shown by X-ray dye (0 means none, up to 4).

**Thalassemia (thal):**  
A blood-related health condition; options are normal, fixed defect, or reversible defect.
""")

# --- Helper Functions for Selectbox Formatting ---
def format_sex(option):
    return "Male" if option == 1 else "Female"
def format_fbs(option):
    return "True (> 120 mg/dl)" if option == 1 else "False (<= 120 mg/dl)"
def format_exang(option):
    return "Yes" if option == 1 else "No"
def format_cp(option):
    cp_dict = {0: "Typical Angina", 1: "Atypical Angina", 2: "Non-anginal Pain", 3: "Asymptomatic"}
    return f"{option}: {cp_dict[option]}"
def format_restecg(option):
    restecg_dict = {0: "Normal", 1: "ST-T Wave Abnormality", 2: "Probable or Definite Left Ventricular Hypertrophy"}
    return f"{option}: {restecg_dict[option]}"
def format_slope(option):
    slope_dict = {0: "Upsloping", 1: "Flat", 2: "Downsloping"}
    return f"{option}: {slope_dict[option]}"
def format_thal(option):
    thal_dict = {1: "Normal", 2: "Fixed Defect", 3: "Reversible Defect"}
    return f"{option}: {thal_dict[option]}"

# --- Main App Function ---
def main():
    st.title("❤️ Heart Disease Prediction")
    st.markdown("<p style='text-align: center; color: #0d2a4c;'>This app uses a machine learning model to predict the likelihood of heart disease based on patient data.<br>Please fill in the patient's details below to get a prediction.</p>", unsafe_allow_html=True)
    st.markdown("---")

    # --- Input Form within styled cards ---
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.header("Patient Information")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("Demographics")
        age = st.slider("Age", 1, 100, 50, help="Patient's age in years.")
        sex = st.selectbox("Sex", options=[0, 1], format_func=format_sex, help="0 for Female, 1 for Male.")
    with col2:
        st.subheader("Symptoms & Vitals")
        cp = st.selectbox("Chest Pain Type (cp)", options=[0, 1, 2, 3], format_func=format_cp)
        trestbps = st.number_input("Resting Blood Pressure (trestbps)", 50, 200, 120, help="In mm Hg on admission.")
    with col3:
        st.subheader("Lab Results")
        chol = st.number_input("Serum Cholesterol (chol)", 100, 600, 250, help="In mg/dl.")
        fbs = st.selectbox("Fasting Blood Sugar > 120 mg/dl (fbs)", options=[0, 1], format_func=format_fbs)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.header("Clinical Measurements")
    col4, col5, col6 = st.columns(3)
    with col4:
        st.subheader("ECG & Heart Rate")
        restecg = st.selectbox("Resting ECG Results (restecg)", options=[0, 1, 2], format_func=format_restecg)
        thalach = st.number_input("Max Heart Rate Achieved (thalach)", 50, 220, 150)
    with col5:
        st.subheader("Exercise-Induced Data")
        exang = st.selectbox("Exercise Induced Angina (exang)", options=[0, 1], format_func=format_exang)
        oldpeak = st.number_input("ST Depression (oldpeak)", 0.0, 6.2, 1.0, step=0.1, help="ST depression induced by exercise relative to rest.")
    with col6:
        st.subheader("Fluoroscopy & Thalassemia")
        slope = st.selectbox("Slope of Peak Exercise ST Segment", options=[0, 1, 2], format_func=format_slope)
        ca = st.selectbox("Major Vessels Colored by Fluoroscopy (ca)", options=[0, 1, 2, 3, 4], help="Number of major vessels (0-4).")
        thal = st.selectbox("Thalassemia (thal)", options=[1, 2, 3], format_func=format_thal)
    st.markdown('</div>', unsafe_allow_html=True)

    # --- Prediction Logic ---
    if st.button("Predict Likelihood of Heart Disease"):
        input_data = pd.DataFrame([[age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]],
                                  columns=['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal'])

        try:
            with open('model.pkl', 'rb') as model_file:
                model = pickle.load(model_file)
            prediction = model.predict(input_data)
            prediction_proba = model.predict_proba(input_data)

            st.header("Prediction Result")
            if prediction[0] == 1:
                st.error("High Risk of Heart Disease Detected", icon="⚠️")
                st.write(f"**Confidence:** {prediction_proba[0][1]*100:.2f}%")
                st.warning("""
                **Disclaimer:** This prediction is based on a machine learning model and is not a substitute for a professional medical diagnosis.
                The model indicates a high likelihood of heart disease. Please consult a healthcare professional for an accurate diagnosis and treatment plan.
                """)
            else:
                st.success("Low Risk of Heart Disease Detected", icon="✅")
                st.write(f"**Confidence:** {prediction_proba[0][0]*100:.2f}%")
                st.info("""
                **Disclaimer:** This prediction is based on a machine learning model and is not a substitute for a professional medical diagnosis.
                While the model indicates a low risk, it's always best to consult with a healthcare provider for any health concerns.
                """)

        except FileNotFoundError:
            st.error("Error: 'model.pkl' not found. Please ensure the model file is in the same directory as the app.")
        except Exception as e:
            st.error(f"An error occurred during prediction: {e}")

if __name__ == "__main__":
    main()
