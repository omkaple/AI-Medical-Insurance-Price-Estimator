import streamlit as st
import pandas as pd
import numpy as np
import pickle
from PIL import Image
import os

# ==========================================
# 1. PAGE CONFIGURATION & THEME
# ==========================================
st.set_page_config(
    page_title="MedSure AI • Precision Insurance",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==========================================
# 2. Advanced UI/UX: Custom CSS

# ==========================================
# This completely rewrites the visuals.
CUSTOM_CSS = """
<style>
/* 2a. Global styling */
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700;900&display=swap');
html, body, [class*="css"] {
    font-family: 'Roboto', sans-serif;
}

/* 2b. Main App Area (Dark-Tech Theme) */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0f1c30 0%, #000000 100%);
    color: #e6f1f3;
}

/* Remove default padding from st.info/st.warning to use our cards */
div[data-testid="stNotification"] {
    background: transparent;
    border: none;
    color: inherit;
    padding: 0px;
}

/* 2c. Sidebar Area (Clean, Light Theme for contrast) */
[data-testid="stSidebar"] {
    background-color: #ffffff;
    border-right: 1px solid #ddd;
    padding: 1rem;
    
}
[data-testid="stSidebar"] hr {
    border-top: 2px solid #ddd;
}


/* 2d. Main Heading Styling */
h1.main-heading {
    color: #4da3ff;
    font-weight: 900;
    font-size: 3.5rem;
    margin-bottom: 0px;
}
p.main-subheading {
    color: #bbccdd;
    font-size: 1.3rem;
    font-weight: 300;
    margin-top: 5px;
    margin-bottom: 25px;
}

/* 2e. Result Display (The Big Number) */
.result-card {
    background-color: #0c1421;
    border: 3px solid #4da3ff;
    border-radius: 20px;
    padding: 30px;
    text-align: center;
    box-shadow: 0 10px 20px rgba(0,0,0,0.5);
    margin-top: 20px;
}
.result-currency {
    font-size: 2.5rem;
    color: #bbf0ff;
    vertical-align: top;
    margin-right: 10px;
}
.result-amount {
    font-size: 6.5rem;
    color: #4da3ff;
    font-weight: 900;
    line-height: 1;
}
.result-label {
    color: #bbccdd;
    font-size: 1.1rem;
    font-weight: 400;
    margin-top: 10px;
}

/* 2f. Sidebar Form Styling */
.stSlider>div {
    margin-bottom: 10px;
}
.stNumberInput, .stSelectbox {
    margin-bottom: 15px;
}

/* Button style */
.stButton>button {
    background: linear-gradient(135deg, #4da3ff 0%, #0066cc 100%);
    color: white !important;
    font-weight: bold !important;
    border-radius: 12px !important;
    padding: 12px 30px !important;
    border: none !important;
    width: 100%;
    font-size: 1.1rem !important;
    transition: all 0.2s ease;
}
.stButton>button:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(77, 163, 255, 0.4);
}

</style>




"""

# ==========================================
# 2. Advanced UI/UX: Custom CSS
# ==========================================
CUSTOM_CSS = """
<style>
/* ... keep your other global/main styles ... */

/* 2c. Sidebar Area (Clean, Light Theme) */
[data-testid="stSidebar"] {
    background-color: #ffffff;
    border-right: 1px solid #ddd;
    padding: 1rem;
}

/* TARGET SIDEBAR TEXT TO BE BLACK */

[data-testid="stSidebar"] label, 

[data-testid="stSidebar"] .stSlider div {
    color: #000000 !important;
    font-weight: 500; /* Makes it slightly bolder for better readability */
}

/* Horizontal rule in sidebar */
[data-testid="stSidebar"] hr {
    border-top: 2px solid #000000;
}

/* ... keep the rest of your styles ... */
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# ==========================================
# 3. CORE LOGIC (Model Prediction)
# ==========================================
@st.cache_resource
def load_prediction_model(model_path):
    """
    Optimized function to load the model and cache it in memory.
    """
    if not os.path.exists(model_path):
        st.error(f"⚠️ Model file '{model_path}' not found. Ensure it is in the same directory as app.py.")
        st.stop()
    with open(model_path, "rb") as f:
        model = pickle.load(f)
    return model

def MyPrediction_Optimized(age, bmi, smoker, children, Gender, region, model):
    """
    Converts raw UI input into the exact DataFrame format the ML model expects.
    """
    # Create the single-row DataFrame required by the prediction function.
    input_data = pd.DataFrame({
        "age" : [age],
        "bmi" : [bmi],
        "smoker" : 1 if smoker.lower() == "yes" else 0,
        "children" : [children],
        "Gender" : 1 if Gender.lower() == "male" else 0,
        # Region handling - Ensure these match your training data column names!
        "northeast" : [True if region == "northeast" else False],
        "northwest" : [True if region == "northwest" else False],
        "southeast" : [True if region == "southeast" else False],
        "southwest" : [True if region == "southwest" else False]
    })
    
    # Run prediction and extract the single value
    charges = model.predict(input_data)
    
    # Round to 2 decimal places and return
    return np.round(charges[0], 2)


# # Load the model
model_filename = "FinalModel_Med.pkl"
final_model = load_prediction_model(model_filename)


# ==========================================
# 4. MAIN LAYOUT (Interactive & Aesthetic)
# ==========================================

# -- Sidebar: Input Form --
# 1. Branding
st.sidebar.markdown("""
    <div style="text-align: center;">
        <h1 style="color: #0066cc; font-size: 2.5rem; margin-bottom: 0;">MedSure</h1>
        <p style="color: #555; font-size: 1rem; margin-top: 0;">PRECISION AI ESTIMATOR</p>
    </div>
    """, unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.markdown("### Profile Details")

# 2. The Input Form for Optimized Interaction
with st.sidebar.form(key="input_form"):
    
    # Using a slider for Age (more interactive)
    
    age_input = st.slider("Age", min_value=18, max_value=100, value=25, step=1)
    
    # Standard number input for Children
    children_input = st.number_input("Children", min_value=0, max_value=10, value=0, step=1)
        
    # Standard input for BMI
    bmi_input = st.number_input("BMI (Body Mass Index)", min_value=10.0, max_value=60.0, value=22.0, step=0.1)
    
    # Direct selection (prevents user typing errors)
    gender_input = st.selectbox("Gender", ("Male", "Female"))
    smoker_input = st.selectbox("Do you smoke?", ("No", "Yes"))
    
    # Region selection
    region_input = st.selectbox("Region", ("northeast", "northwest", "southeast", "southwest"))

    # Crucial UI Element: The Submit Button
    st.markdown("<br>", unsafe_allow_html=True)
    submit_button = st.form_submit_button(label="CALCULATE CHARGES")


# -- Main Area: Header & Background --
# Create the structure (two columns)
m_col1, m_col2 = st.columns([1, 1])

with m_col1:
    st.markdown('<h1 class="main-heading">🩺 AI Medical Insurance Price Estimator</h1>', unsafe_allow_html=True)
    st.markdown('<p class="main-subheading">A data-driven prediction model to help you understand estimated annual medical insurance charges.</p>', unsafe_allow_html=True)

with m_col2:
    # 5. UX Fix: Use modern st.image with use_container_width
    image_path = os.path.join("images", "image.png")
    try:
        main_image = Image.open(image_path)
        # use_container_width is the replacement for use_column_width
        st.image(main_image, use_container_width=True) 
    except FileNotFoundError:
        # Fallback if the user hasn't downloaded the image.
        st.warning(f"Image not found at '{image_path}'. Ensure you create the 'images' folder and add 'medical_tech_banner.jpg'.")


# -- Results Area: Conditional Display --
st.write("---")

if submit_button:
    # Get the calculation
    predicted_charges = MyPrediction_Optimized(
        age_input, bmi_input, smoker_input, children_input, gender_input, region_input, final_model
    )
    
    # 6. UI Fix: The "Invisible" (Yellow) Content issue.
    # Instead of st.info (which had invisible text against the dark theme),
    # we use a dedicated result display card.
    
    st.balloons() # Immediate interactive feedback
    
    # Clear visual indicators
    c1, c2, c3 = st.columns([1, 2, 1])
    
    with c1:
        st.markdown(f"**Age:** {age_input}")
        st.markdown(f"**BMI:** {bmi_input}")
        if smoker_input == "Yes":
             st.warning("Smoking status increases insurance premium.")
        else:
             st.success("Non-smoking status helps reduce premium.")

    with c2:
        # The impactful result card
        # Using a structured format to create the massive number
        result_html = f"""
        <div class="result-card">
            <span class="result-currency">Rs.</span>
            <span class="result-amount">{predicted_charges:,.2f}</span>
            <p class="result-label">Personalized annual charge estimate</p>
        </div>
        """
        st.markdown(result_html, unsafe_allow_html=True)
        
    with c3:
        st.markdown(f"**Gender:** {gender_input}")
        st.markdown(f"**Children:** {children_input}")
        st.markdown(f"**Region:** {region_input}")
        
    # Crucial UX element: The Disclaimer (managing ethical AI expectations)
    st.write("<br><br>", unsafe_allow_html=True)
    st.markdown("""
        <div style="background-color:rgba(77, 163, 255, 0.1); padding:15px; border-radius:10px; border:1px solid rgba(77, 163, 255, 0.3); color:#bbccdd;">
            <p style="font-size:0.9rem;">
            <b>Disclaimer:</b> This calculation is an estimate based on your profile inputs and a machine learning model. It is not a guarantee of actual pricing from any insurance provider. Premiums are influenced by many factors including carrier-specific underwriting and policy features not captured here.
            </p>
        </div>
        """, unsafe_allow_html=True)

else:
    # Initial instructive message
    st.markdown("""
        <div style="background-color:rgba(77, 163, 255, 0.1); padding:15px; border-radius:10px; border:1px solid rgba(77, 163, 255, 0.3); color:#bbccdd;">
            <p style="font-size:1.1rem; text-align:center; font-weight: 300;">
            ⬅️ To generate your estimate, please complete your profile details on the left sidebar and click "CALCULATE CHARGES."
            </p>
        </div>
        """, unsafe_allow_html=True)
    

    # ==========================================
# 2. Advanced UI/UX: Custom CSS
# ==========================================
CUSTOM_CSS = """
<style>
/* ... keep your other global/main styles ... */

/* 2c. Sidebar Area (Clean, Light Theme) */
[data-testid="stSidebar"] {
    background-color: #ffffff;
    border-right: 1px solid #ddd;
    padding: 1rem;
}

/* TARGET SIDEBAR TEXT TO BE BLACK */
[data-testid="stSidebar"] .stMarkdown p, 
[data-testid="stSidebar"] label, 
[data-testid="stSidebar"] .stSelectbox div, 
[data-testid="stSidebar"] .stSlider div {
    color: #000000 !important;
    font-weight: 500; /* Makes it slightly bolder for better readability */
}

/* Horizontal rule in sidebar */
[data-testid="stSidebar"] hr {
    border-top: 2px solid #000000;
}

/* ... keep the rest of your styles ... */
</style>
"""