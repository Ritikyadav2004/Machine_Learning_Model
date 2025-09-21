import streamlit as st
import pickle
import time

# --- Page Configuration (No changes here) ---
st.set_page_config(
    page_title="Spam Shield AI",
    page_icon="🛡️",
    layout="centered",
    initial_sidebar_state="auto"
)

# --- Custom CSS for ADVANCED Styling ---
# The .toml file now handles base colors and fonts.
# We only need CSS for things the theme can't do, like gradients and glassmorphism.
st.markdown("""
<style>
/* Main app background gradient */
.stApp {
    background-image: linear-gradient(to right top, #051937, #004d7a, #008793, #00bf72, #a8eb12);
    background-size: cover;
    background-repeat: no-repeat;
    background-attachment: fixed;
}

/* Main content block with glassmorphism */
.main .block-container {
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border-radius: 20px;
    padding: 2rem;
    border: 1px solid rgba(255, 255, 255, 0.18);
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
}

/* Make instruction text a bit lighter */
.stMarkdown p {
    color: #E0E0E0;
    text-align: center;
}

/* Text Area styling - textColor is from theme, but we can add more */
.stTextArea textarea {
    border-radius: 10px;
    border: 2px solid rgba(255, 255, 255, 0.2);
    background-color: rgba(0, 0, 0, 0.2);
}

/* Button styling - primaryColor is from theme, but we style the hover effect */
.stButton>button {
    width: 100%;
    border-radius: 10px;
    border: 2px solid #a8eb12; /* Match primaryColor */
    font-weight: bold;
    padding: 10px 0;
    transition: all 0.3s ease-in-out;
}

.stButton>button:hover {
    background-color: #FFFFFF;
    color: #008793;
    border-color: #FFFFFF;
}

/* Result messages (Success/Error) */
.stAlert {
    border-radius: 10px;
    text-align: center;
    font-size: 1.2rem;
}
</style>
""", unsafe_allow_html=True)


# --- Load Model and Vectorizer (No changes here) ---
try:
    model = pickle.load(open("E:/ToBeArrenged/Ml Project/Sms_detecter/Indian_Spam_Model.pkl", "rb"))
    vectorizer = pickle.load(open("E:/ToBeArrenged/Ml Project/Sms_detecter/vectorizer.pkl", "rb"))
except FileNotFoundError:
    st.error("Model or vectorizer file not found. Please check the file paths.")
    st.stop()

# --- Sidebar Content (No changes here) ---
with st.sidebar:
    st.image("https://www.gstatic.com/images/branding/product/2x/gemini_48dp.png", width=60)
    st.header("About Spam Shield AI")
    st.write("""
        This application uses a Machine Learning model to classify messages as either **Spam** or **Not Spam**.
        
        The model was trained on a dataset of Indian SMS messages and uses a `TfidfVectorizer` to process the text.
    """)
    st.write("**Model:** Naive Bayes Classifier")
    st.write("**Made with:** Streamlit & Scikit-learn")


# --- Main App Interface (No changes here) ---
st.title("🛡️ Spam Shield AI")
st.markdown("<p>Enter a message below and I'll tell you if it's Spam or Not Spam.</p>", unsafe_allow_html=True)

message = st.text_area("✏️ Type your message here:", height=150, placeholder="e.g., Congratulations you've won a lottery...")

if st.button("Check Message"):
    if not message.strip():
        st.warning("🧐 Please enter a message to check.")
    else:
        with st.spinner('Analyzing your message...'):
            time.sleep(1)
            
            message_vector = vectorizer.transform([message])
            prediction = model.predict(message_vector)[0]
            
            if prediction == 1:
                st.error("🚨 This message is **SPAM**!")
            else:
                st.success("✅ This message is **NOT Spam**.")
                # st.balloons()