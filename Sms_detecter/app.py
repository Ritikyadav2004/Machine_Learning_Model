import streamlit as st
import pickle
import time
import pandas as pd
from datetime import datetime

# --- Page Configuration ---
st.set_page_config(
    page_title="SpamShield Pro v3",
    page_icon="🛡️",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- Advanced Custom CSS for a clean, dark, card-based UI ---
st.markdown("""
<style>
/* Import a different, clean font */
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');

:root {
    --primary-color: #5C67F2;
    --secondary-color: #E6E8F2;
    --background-color: #1A1A2E;
    --card-bg-color: #2E2E4A;
    --text-color: #F8F8F2;
    --success-color: #4CAF50;
    --error-color: #FF6B6B;
    --warning-color: #FFC107;
}

/* Main app background */
.stApp {
    background-color: var(--background-color);
    font-family: 'Roboto', sans-serif;
    color: var(--text-color);
}

/* Main container card */
.main .block-container {
    background-color: var(--card-bg-color);
    border-radius: 20px;
    padding: 3rem;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
    margin-top: 3rem;
    max-width: 800px;
}

/* Title styling */
h1 {
    color: var(--primary-color);
    text-align: center;
    font-weight: 700;
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
}

/* Subtitle styling */
.subtitle {
    text-align: center;
    color: var(--secondary-color);
    font-size: 1.1rem;
    margin-bottom: 2rem;
    font-weight: 300;
}

/* Enhanced text area */
.stTextArea textarea {
    border-radius: 12px;
    border: 1px solid rgba(255, 255, 255, 0.2);
    background-color: #1A1A2E;
    color: var(--text-color);
    font-size: 1rem;
    padding: 15px;
    transition: all 0.3s ease;
}

.stTextArea textarea:focus {
    border-color: var(--primary-color);
    box-shadow: 0 0 15px rgba(92, 103, 242, 0.5);
    background-color: #1A1A2E;
}

/* Animated button */
.stButton > button {
    width: 100%;
    border-radius: 12px;
    border: none;
    background-color: var(--primary-color);
    color: white;
    font-weight: 500;
    font-size: 1.1rem;
    padding: 15px 0;
    transition: all 0.2s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(92, 103, 242, 0.4);
}

.stButton > button:active {
    transform: translateY(0);
    box-shadow: none;
}

/* Results container */
.results-container {
    padding: 20px;
    border-radius: 12px;
    margin-top: 2rem;
    text-align: center;
    animation: fadeIn 0.5s ease-out;
}

/* Spam result styling */
.spam {
    background-color: rgba(255, 107, 107, 0.1);
    border: 1px solid var(--error-color);
}

/* Legit result styling */
.legit {
    background-color: rgba(76, 175, 80, 0.1);
    border: 1px solid var(--success-color);
}

.results-container h3 {
    margin: 0;
    font-weight: 500;
}

.results-container p {
    margin-top: 10px;
    font-size: 0.9rem;
    color: var(--secondary-color);
}

/* Progress bar styling */
.stProgress > div > div {
    height: 10px;
    border-radius: 5px;
    background-color: rgba(255, 255, 255, 0.1);
}

.stProgress > div > div > div {
    background-color: var(--primary-color);
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

/* Sidebar styling */
.css-1d391kg {
    background-color: #2A2A3A;
    border-radius: 0 20px 20px 0;
}

.stat-card {
    background-color: #3B3B5B;
    border-radius: 10px;
    padding: 15px;
    margin-bottom: 10px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    text-align: center;
}

.stat-card h4 {
    font-size: 1rem;
    color: var(--primary-color);
    margin-bottom: 5px;
}

.stat-card p {
    font-size: 0.9rem;
    color: var(--secondary-color);
}
</style>
""", unsafe_allow_html=True)

# --- Load Model and Vectorizer ---
@st.cache_resource
def load_models():
    """Loads the pre-trained model and vectorizer from pickle files."""
    try:
        model = pickle.load(open("D:/Ml Project/Sms_detecter/Indian_Spam_Model.pkl", "rb"))
        vectorizer = pickle.load(open("D:/Ml Project/Sms_detecter/vectorizer.pkl", "rb"))
        return model, vectorizer
    except FileNotFoundError:
        st.error("🚨 Model files not found! Please check the file paths.")
        st.stop()

model, vectorizer = load_models()

# --- Sidebar Content ---
with st.sidebar:
    st.markdown("""
    <div style='text-align: center; padding: 20px;'>
        <h2 style='color: var(--primary-color);'>🛡️ SpamShield Pro</h2>
        <p style='color: var(--secondary-color); font-size: 0.9rem;'>Powered by Machine Learning</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Model Information
    st.markdown("### 📊 Model Info")
    st.markdown("""
    <div class='stat-card'>
        <h4>Algorithm</h4>
        <p>Naive Bayes Classifier</p>
    </div>
    <div class='stat-card'>
        <h4>Processing</h4>
        <p>TF-IDF Vectorization</p>
    </div>
    <div class='stat-card'>
        <h4>Dataset</h4>
        <p>Indian SMS Corpus</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Features
    st.markdown("### ✨ Key Features")
    st.markdown("""
    - **Real-time** message analysis
    - **High-accuracy** prediction
    - **Privacy-focused** (data is not stored)
    """)
    
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: var(--secondary-color); font-size: 0.8rem;'>
        Made with ❤️ using Streamlit
    </div>
    """, unsafe_allow_html=True)

# --- Main App Interface ---
# Header
st.markdown("# SpamShield Pro")
st.markdown('<p class="subtitle">A minimalist tool for real-time spam detection</p>', unsafe_allow_html=True)

# Main content area
with st.container():
    # Message input
    st.markdown("### 📝 Enter Your Message")
    message = st.text_area(
        "",
        height=150,
        placeholder="Type or paste your message here...\n\ne.g., 'Congratulations! You've won a lottery of ₹1,00,000. Click here to claim your prize!'",
        help="Enter any text message to check if it's spam or legitimate"
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Check button
    if st.button("🔍 Analyze Message"):
        if not message.strip():
            st.warning("⚠ Please enter a message to analyze!")
        else:
            # Create a spinner and simulate analysis
            with st.spinner('Analyzing...'):
                time.sleep(1) # Simulating a processing delay
            
            # Make prediction
            try:
                message_vector = vectorizer.transform([message])
                prediction = model.predict(message_vector)[0]
                confidence = model.predict_proba(message_vector)[0]
                
                # Display results with enhanced styling
                st.markdown("---")
                
                if prediction == 1:
                    st.markdown(f"""
                    <div class='results-container spam'>
                        <h3>🚨 SPAM DETECTED!</h3>
                        <p>This message appears to be spam with a confidence of {confidence[1]*100:.2f}%</p>
                    </div>
                    """, unsafe_allow_html=True)
                    with st.expander("🛡️ Safety Tips"):
                        st.markdown("""
                        - **Do not click** on any links.
                        - **Do not reply** or share personal information.
                        - **Delete** the message immediately.
                        """)
                else:
                    st.markdown(f"""
                    <div class='results-container legit'>
                        <h3>✅ LEGITIMATE MESSAGE</h3>
                        <p>This message appears to be genuine with a confidence of {confidence[0]*100:.2f}%</p>
                    </div>
                    """, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"An error occurred during analysis: {e}")

# --- Footer ---
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: var(--secondary-color); padding: 20px;'>
    <p>🔒 Your privacy is important. Messages are not stored or logged.</p>
</div>
""", unsafe_allow_html=True)

