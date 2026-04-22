import streamlit as st
import requests

import streamlit as st
import requests

# Set Streamlit theme to light and wide mode
st.set_page_config(
    page_title="Leaf Disease Detection",
    layout="wide",
    initial_sidebar_state="collapsed"
)
<!--New_Code-->
# Language Toggle
if "lang" not in st.session_state:
    st.session_state.lang = "English"

c1, c2, c3 = st.columns([1,1,1])

with c1:
    if st.button("English"):
        st.session_state.lang = "English"

with c2:
    if st.button("বাংলা"):
        st.session_state.lang = "বাংলা"

with c3:
    if st.button("हिन्दी"):
        st.session_state.lang = "हिन्दी"

translations = {
    "English": {
        "title": "Leaf Disease Detection",
        "desc": "Upload a leaf image and instantly find out if your plant is healthy or affected, along with expert care tips.",
        "upload": "Upload Leaf Image",
        "detect": "🔍 Detect Disease"
    },

    "বাংলা": {
        "title": "পাতার রোগ শনাক্তকরণ",
        "desc": "পাতার ছবি আপলোড করুন এবং রোগ আছে কিনা সাথে সাথে জানুন।",
        "upload": "পাতার ছবি আপলোড করুন",
        "detect": "🔍 পরীক্ষা করুন"
    },

    "हिन्दी": {
        "title": "पत्ती रोग पहचान",
        "desc": "पत्ती की फोटो अपलोड करें और तुरंत जानें पौधा स्वस्थ है या नहीं।",
        "upload": "पत्ती की फोटो अपलोड करें",
        "detect": "🔍 जांच करें"
    }
}

t = translations[st.session_state.lang]
<!--New_Code_ENd-->

# Enhanced modern CSS
st.markdown("""
    <style>

/* Background */
.stApp {
 
    font-family: 'Segoe UI', sans-serif;
    background: url("https://images.unsplash.com/photo-1501004318641-b39e6451bec6");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
}

.stApp::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(135deg, #9fddae45 0%, #f1f8e9d4 50%, #e3f2fd42 100%);    
    z-index: 0;
}


/* Main title area */
h1 {
    font-weight: 800;
    letter-spacing: 0.5px;
}

/* Hero container feel */
div[data-testid="stMarkdownContainer"] {
    line-height: 1.6;
}

/* Upload box */
[data-testid="stFileUploader"] {
    background: white;
    padding: 20px;
    border-radius: 18px;
    box-shadow: 0 8px 25px rgba(0,0,0,0.08);
    border: 1px solid #e0e0e0;
}

/* Button styling */
.stButton > button {
    background: linear-gradient(135deg, #c0f1cafc, #46e51e7a);
    color: #000000;
    border: 1px solid hsl(107.44deg 100% 83.15%);
    padding: 0.75em 1.2em;
    border-radius: 12px;
    font-weight: 600;
    transition: all 0.3s ease;
    box-shadow: 0 6px 15px rgba(0,0,0,0.15);
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 25px rgba(0,0,0,0.2);
}

/* Result card */
.result-card {
    background: rgba(255,255,255,0.95);
    border-radius: 24px;
    box-shadow: 0 12px 35px rgba(0,0,0,0.12);
    padding: 2.2em;
    margin-top: 1.5em;
    margin-bottom: 1.5em;
    border: 1px solid rgba(0,0,0,0.05);
    backdrop-filter: blur(10px);
}

/* Title */
.disease-title {
    color: #1b5e20;
    font-size: 2em;
    font-weight: 800;
    margin-bottom: 0.5em;
}

/* Section headings */
.section-title {
    color: #1b5e20
    font-size: 1.2em;
    font-weight: 700;
    margin-top: 1.2em;
    margin-bottom: 0.5em;
}

/* Info badges */
.info-badge {
    display: inline-block;
    background: linear-gradient(135deg, #e3f2fd, #e8f5e9);
    color: #1b5e20
    border-radius: 20px;
    padding: 0.4em 0.9em;
    font-size: 0.95em;
    margin-right: 0.5em;
    margin-bottom: 0.4em;
    font-weight: 500;
    border: 1px solid #d0e3ff;
}

/* Lists */
.symptom-list li,
.cause-list li,
.treatment-list li {
    margin-bottom: 6px;
    color: #424242;
}

/* Timestamp */
.timestamp {
    color: #757575;
    font-size: 0.9em;
    text-align: right;
    margin-top: 1em;
}

/* Hover effect for cards */
.result-card:hover {
    transform: translateY(-3px);
    transition: 0.3s ease;
    box-shadow: 0 18px 45px rgba(0,0,0,0.15);
}

/* Image preview */
img {
    border-radius: 12px;
}

</style>
""", unsafe_allow_html=True)


st.markdown("""
    <div style='text-align: center; margin-top: 1em;'>
        <span style='font-size:3em;'>🪴</span>
        <h1 style='color: #3b631d; margin-bottom:0;'>Leaf Disease Detection</h1>
        <p style='color: #000; font-size:1.15em;'>Upload a leaf image and instantly find out if your plant is healthy or affected, along with expert care tips.</p>
    </div>
""", unsafe_allow_html=True)

api_url = "http://leaf-diseases-detect.vercel.app"

col1, col2 = st.columns([1, 2])
with col1:
    uploaded_file = st.file_uploader(
        "Upload Leaf Image", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        st.image(uploaded_file, caption="Preview")

with col2:
    if uploaded_file is not None:
        if st.button("🔍 Detect Disease", use_container_width=True):
            with st.spinner("Analyzing image and contacting API..."):
                try:
                    files = {
                        "file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                    response = requests.post(
                        f"{api_url}/disease-detection-file", files=files)
                    if response.status_code == 200:
                        result = response.json()

                        # Check if it's an invalid image
                        if result.get("disease_type") == "invalid_image":
                            st.markdown("<div class='result-card'>",
                                        unsafe_allow_html=True)
                            st.markdown(
                                "<div class='disease-title'>⚠️ Invalid Image</div>", unsafe_allow_html=True)
                            st.markdown(
                                "<div style='color: #ff5722; font-size: 1.1em; margin-bottom: 1em;'>Please upload a clear image of a plant leaf for accurate disease detection.</div>", unsafe_allow_html=True)

                            # Show the symptoms (which contain the error message)
                            if result.get("symptoms"):
                                st.markdown(
                                    "<div class='section-title'>Issue</div>", unsafe_allow_html=True)
                                st.markdown("<ul class='symptom-list'>",
                                            unsafe_allow_html=True)
                                for symptom in result.get("symptoms", []):
                                    st.markdown(
                                        f"<li>{symptom}</li>", unsafe_allow_html=True)
                                st.markdown("</ul>", unsafe_allow_html=True)

                            # Show treatment recommendations
                            if result.get("treatment"):
                                st.markdown(
                                    "<div class='section-title'>What to do</div>", unsafe_allow_html=True)
                                st.markdown("<ul class='treatment-list'>",
                                            unsafe_allow_html=True)
                                for treat in result.get("treatment", []):
                                    st.markdown(
                                        f"<li>{treat}</li>", unsafe_allow_html=True)
                                st.markdown("</ul>", unsafe_allow_html=True)

                            st.markdown("</div>", unsafe_allow_html=True)

                        elif result.get("disease_detected"):
                            st.markdown("<div class='result-card'>",
                                        unsafe_allow_html=True)
                            st.markdown(
                                f"<div class='disease-title'>🦠 {result.get('disease_name', 'N/A')}</div>", unsafe_allow_html=True)
                            st.markdown(
                                f"<span class='info-badge'>Type: {result.get('disease_type', 'N/A')}</span>", unsafe_allow_html=True)
                            st.markdown(
                                f"<span class='info-badge'>Severity: {result.get('severity', 'N/A')}</span>", unsafe_allow_html=True)
                            st.markdown(
                                f"<span class='info-badge'>Confidence: {result.get('confidence', 'N/A')}%</span>", unsafe_allow_html=True)
                            st.markdown(
                                "<div class='section-title'>Symptoms</div>", unsafe_allow_html=True)
                            st.markdown("<ul class='symptom-list'>",
                                        unsafe_allow_html=True)
                            for symptom in result.get("symptoms", []):
                                st.markdown(
                                    f"<li>{symptom}</li>", unsafe_allow_html=True)
                            st.markdown("</ul>", unsafe_allow_html=True)
                            st.markdown(
                                "<div class='section-title'>Possible Causes</div>", unsafe_allow_html=True)
                            st.markdown("<ul class='cause-list'>",
                                        unsafe_allow_html=True)
                            for cause in result.get("possible_causes", []):
                                st.markdown(
                                    f"<li>{cause}</li>", unsafe_allow_html=True)
                            st.markdown("</ul>", unsafe_allow_html=True)
                            st.markdown(
                                "<div class='section-title'>Treatment</div>", unsafe_allow_html=True)
                            st.markdown("<ul class='treatment-list'>",
                                        unsafe_allow_html=True)
                            for treat in result.get("treatment", []):
                                st.markdown(
                                    f"<li>{treat}</li>", unsafe_allow_html=True)
                            st.markdown("</ul>", unsafe_allow_html=True)
                            st.markdown(
                                f"<div class='timestamp'>🕒 {result.get('analysis_timestamp', 'N/A')}</div>", unsafe_allow_html=True)
                            st.markdown("</div>", unsafe_allow_html=True)
                        else:
                            # Healthy leaf case
                            st.markdown("<div class='result-card'>",
                                        unsafe_allow_html=True)
                            st.markdown(
                                "<div class='disease-title'>✅ Healthy Leaf</div>", unsafe_allow_html=True)
                            st.markdown(
                                "<div style='color: #4caf50; font-size: 1.1em; margin-bottom: 1em;'>No disease detected in this leaf. The plant appears to be healthy!</div>", unsafe_allow_html=True)
                            st.markdown(
                                f"<span class='info-badge'>Status: {result.get('disease_type', 'healthy')}</span>", unsafe_allow_html=True)
                            st.markdown(
                                f"<span class='info-badge'>Confidence: {result.get('confidence', 'N/A')}%</span>", unsafe_allow_html=True)
                            st.markdown(
                                f"<div class='timestamp'>🕒 {result.get('analysis_timestamp', 'N/A')}</div>", unsafe_allow_html=True)
                            st.markdown("</div>", unsafe_allow_html=True)
                    else:
                        st.error(f"API Error: {response.status_code}")
                        st.write(response.text)
                except Exception as e:
                    st.error(f"Error: {str(e)}")
