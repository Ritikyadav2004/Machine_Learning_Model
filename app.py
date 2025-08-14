# import streamlit as st
# import pickle
# import time
# import pandas as pd
# from datetime import datetime

# # --- Page Configuration ---
# st.set_page_config(
#     page_title="SpamShield Pro",
#     page_icon="🛡",
#     layout="centered",
#     initial_sidebar_state="expanded"
# )

# # --- Advanced Custom CSS ---
# st.markdown("""
# <style>
# @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

# /* Main app background with animated gradient */
# .stApp {
#     background: linear-gradient(-45deg, #0F0C29, #24243e, #302B63, #0F0C29);
#     background-size: 400% 400%;
#     animation: gradientShift 15s ease infinite;
#     font-family: 'Poppins', sans-serif;
# }

# @keyframes gradientShift {
#     0% { background-position: 0% 50%; }
#     50% { background-position: 100% 50%; }
#     100% { background-position: 0% 50%; }
# }

# /* Glassmorphism container */
# .main .block-container {
#     background: rgba(255, 255, 255, 0.08);
#     backdrop-filter: blur(20px);
#     -webkit-backdrop-filter: blur(20px);
#     border-radius: 20px;
#     padding: 2.5rem;
#     border: 1px solid rgba(255, 255, 255, 0.1);
#     box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
#     margin-top: 2rem;
# }

# /* Title styling */
# h1 {
#     background: linear-gradient(45deg, #00D4AA, #7B68EE, #FF6B6B);
#     background-size: 200% auto;
#     color: transparent;
#     background-clip: text;
#     -webkit-background-clip: text;
#     animation: shine 3s ease-in-out infinite alternate;
#     text-align: center;
#     font-weight: 700;
#     margin-bottom: 0.5rem;
# }

# @keyframes shine {
#     to { background-position: 200% center; }
# }

# /* Subtitle styling */
# .subtitle {
#     text-align: center;
#     color: #B8BCC8;
#     font-size: 1.1rem;
#     margin-bottom: 2rem;
#     font-weight: 300;
# }

# /* Enhanced text area */
# .stTextArea textarea {
#     border-radius: 15px;
#     border: 2px solid rgba(0, 212, 170, 0.3);
#     background: rgba(255, 255, 255, 0.05);
#     color: #FAFAFA;
#     font-size: 1rem;
#     padding: 15px;
#     transition: all 0.3s ease;
# }

# .stTextArea textarea:focus {
#     border-color: #00D4AA;
#     box-shadow: 0 0 20px rgba(0, 212, 170, 0.3);
#     background: rgba(255, 255, 255, 0.1);
# }

# /* Animated button */
# .stButton > button {
#     width: 100%;
#     border-radius: 15px;
#     border: none;
#     background: linear-gradient(45deg, #00D4AA, #7B68EE);
#     color: white;
#     font-weight: 600;
#     font-size: 1.1rem;
#     padding: 15px 0;
#     transition: all 0.3s ease;
#     position: relative;
#     overflow: hidden;
# }

# .stButton > button:hover {
#     transform: translateY(-2px);
#     box-shadow: 0 10px 25px rgba(0, 212, 170, 0.4);
# }

# .stButton > button:active {
#     transform: translateY(0);
# }

# /* Enhanced alerts */
# .stAlert {
#     border-radius: 15px;
#     border: none;
#     font-size: 1.2rem;
#     font-weight: 500;
#     text-align: center;
#     padding: 20px;
#     animation: fadeInUp 0.5s ease;
# }

# @keyframes fadeInUp {
#     from {
#         opacity: 0;
#         transform: translateY(30px);
#     }
#     to {
#         opacity: 1;
#         transform: translateY(0);
#     }
# }

# /* Success message enhancement */
# .stSuccess {
#     background: linear-gradient(45deg, #00D4AA, #4CAF50);
#     color: white;
#     border: 2px solid rgba(255, 255, 255, 0.2);
# }

# /* Error message enhancement */
# .stError {
#     background: linear-gradient(45deg, #FF6B6B, #FF4757);
#     color: white;
#     border: 2px solid rgba(255, 255, 255, 0.2);
# }

# /* Warning message enhancement */
# .stWarning {
#     background: linear-gradient(45deg, #FFA726, #FF9800);
#     color: white;
#     border: 2px solid rgba(255, 255, 255, 0.2);
# }

# /* Sidebar styling */
# .css-1d391kg {
#     background: rgba(255, 255, 255, 0.05);
#     backdrop-filter: blur(10px);
#     border-radius: 0 20px 20px 0;
# }

# /* Stats cards */
# .stat-card {
#     background: rgba(255, 255, 255, 0.1);
#     border-radius: 15px;
#     padding: 20px;
#     margin: 10px 0;
#     border: 1px solid rgba(255, 255, 255, 0.1);
#     text-align: center;
# }

# /* Loading spinner customization */
# .stSpinner > div {
#     border-top-color: #00D4AA !important;
# }

# /* Custom metrics styling */
# .metric-container {
#     background: rgba(255, 255, 255, 0.05);
#     border-radius: 15px;
#     padding: 20px;
#     margin: 10px 0;
#     border: 1px solid rgba(0, 212, 170, 0.2);
# }
# </style>
# """, unsafe_allow_html=True)

# # --- Load Model and Vectorizer ---
# @st.cache_resource
# def load_models():
#     try:
#         model = pickle.load(open("D:/Ml Project/Sms_detecter/Indian_Spam_Model.pkl", "rb"))
#         vectorizer = pickle.load(open("D:/Ml Project/Sms_detecter/vectorizer.pkl", "rb"))
#         return model, vectorizer
#     except FileNotFoundError:
#         st.error("🚨 Model files not found! Please check the file paths.")
#         st.stop()

# model, vectorizer = load_models()

# # --- Sidebar Content ---
# with st.sidebar:
#     st.markdown("""
#     <div style='text-align: center; padding: 20px;'>
#         <h2 style='color: #00D4AA;'>🛡 SpamShield Pro</h2>
#         <p style='color: #B8BCC8; font-size: 0.9rem;'>Advanced AI-Powered Spam Detection</p>
#     </div>
#     """, unsafe_allow_html=True)
    
#     st.markdown("---")
    
#     # Model Information
#     st.markdown("### 📊 Model Info")
#     with st.container():
#         st.markdown("""
#         <div class='stat-card'>
#             <h4>🧠 Algorithm</h4>
#             <p>Naive Bayes Classifier</p>
#         </div>
#         <div class='stat-card'>
#             <h4>📝 Training Data</h4>
#             <p>Indian SMS Dataset</p>
#         </div>
#         <div class='stat-card'>
#             <h4>⚡ Processing</h4>
#             <p>TF-IDF Vectorization</p>
#         </div>
#         """, unsafe_allow_html=True)
    
#     st.markdown("---")
    
#     # Features
#     st.markdown("### ✨ Features")
#     st.markdown("""
#     - 🚀 *Real-time Detection*
#     - 🎯 *High Accuracy*
#     - 🌐 *Indian Context Aware*
#     - 🔒 *Privacy Focused*
#     - 📱 *Mobile Friendly*
#     """)
    
#     st.markdown("---")
#     st.markdown("""
#     <div style='text-align: center; color: #B8BCC8; font-size: 0.8rem;'>
#         Made with ❤ using Streamlit<br>
#         & Machine Learning
#     </div>
#     """, unsafe_allow_html=True)

# # --- Main App Interface ---
# # Header
# st.markdown("# 🛡 SpamShield Pro")
# st.markdown('<p class="subtitle">Advanced AI-powered spam detection for your messages</p>', unsafe_allow_html=True)

# # Add some spacing
# st.markdown("<br>", unsafe_allow_html=True)

# # Create columns for better layout
# col1, col2, col3 = st.columns([1, 3, 1])

# with col2:
#     # Message input
#     st.markdown("### 📝 Enter Your Message")
#     message = st.text_area(
#         "",
#         height=150,
#         placeholder="Type or paste your message here...\n\ne.g., 'Congratulations! You've won a lottery of ₹1,00,000. Click here to claim your prize!'",
#         help="Enter any text message to check if it's spam or legitimate"
#     )
    
#     # Add some spacing
#     st.markdown("<br>", unsafe_allow_html=True)
    
#     # Check button
#     if st.button("🔍 Analyze Message", type="primary"):
#         if not message.strip():
#             st.warning("⚠ Please enter a message to analyze!")
#         else:
#             # Create progress bar
#             progress_bar = st.progress(0)
#             status_text = st.empty()
            
#             # Simulate analysis steps
#             steps = [
#                 "Preprocessing text...",
#                 "Extracting features...",
#                 "Running AI model...",
#                 "Generating results..."
#             ]
            
#             for i, step in enumerate(steps):
#                 status_text.text(step)
#                 progress_bar.progress((i + 1) * 25)
#                 time.sleep(0.3)
            
#             # Clear progress indicators
#             progress_bar.empty()
#             status_text.empty()
            
#             # Make prediction
#             message_vector = vectorizer.transform([message])
#             prediction = model.predict(message_vector)[0]
#             confidence = model.predict_proba(message_vector)[0]
            
#             # Display results with enhanced styling
#             st.markdown("---")
#             st.markdown("### 📊 Analysis Results")
            
#             if prediction == 1:
#                 st.error("🚨 *SPAM DETECTED!* This message appears to be spam.")
#                 spam_confidence = max(confidence) * 100
#                 st.markdown(f"""
#                 <div class='metric-container'>
#                     <h4 style='color: #FF6B6B;'>Spam Confidence: {spam_confidence:.1f}%</h4>
#                     <p>This message contains patterns commonly found in spam messages.</p>
#                 </div>
#                 """, unsafe_allow_html=True)
                
#                 # Safety tips
#                 with st.expander("🛡 Safety Tips"):
#                     st.markdown("""
#                     - *Don't click* on suspicious links
#                     - *Don't share* personal information
#                     - *Report* spam messages to authorities
#                     - *Delete* the message immediately
#                     """)
                    
#             else:
#                 st.success("✅ *LEGITIMATE MESSAGE* This appears to be a genuine message.")
#                 legit_confidence = max(confidence) * 100
#                 st.markdown(f"""
#                 <div class='metric-container'>
#                     <h4 style='color: #00D4AA;'>Legitimacy Confidence: {legit_confidence:.1f}%</h4>
#                     <p>This message appears to be genuine and safe.</p>
#                 </div>
#                 """, unsafe_allow_html=True)
#                 st.balloons()

# # --- Footer ---
# st.markdown("---")
# st.markdown("""
# <div style='text-align: center; color: #B8BCC8; padding: 20px;'>
#     <p>🔒 Your privacy is protected. Messages are not stored or logged.</p>
#     <p style='font-size: 0.8rem;'>SpamShield Pro v2.0 | Powered by Machine Learning</p>
# </div>
# """, unsafe_allow_html=True)

# # --- Additional Features (Optional) ---
# # You can uncomment these for extra functionality

# # with st.expander("📈 View Detection Statistics"):
# #     col1, col2, col3 = st.columns(3)
# #     with col1:
# #         st.metric("Messages Checked", "1,234", "12")
# #     with col2:
# #         st.metric("Spam Detected", "456", "3")
# #     with col3:
# #         st.metric("Accuracy Rate", "94.2%", "0.5%")

# # with st.expander("🎯 How It Works"):
# #     st.markdown("""
# #     1. *Text Preprocessing*: Your message is cleaned and normalized
# #     2. *Feature Extraction*: TF-IDF vectorization converts text to numbers
# #     3. *AI Classification*: Naive Bayes model analyzes the features
# #     4. *Result Generation*: Confidence score and classification provided
# #     """)





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

