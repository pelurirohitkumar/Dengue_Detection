import streamlit as st
import pandas as pd
import pickle
import os

# =========================
# Page Config (FIRST)
# =========================
st.set_page_config(
    page_title="Dengue Prediction System",
    page_icon="🦟",
    layout="centered"
)

# =========================
# Simple Clean CSS
# =========================
st.markdown("""
<style>
.stApp {
    background-color: #f5f7fa;
}
h1 {
    color: #2c3e50;
    text-align: center;
}
h3 {
    color: #34495e;
}
.stButton>button {
    background-color: #3498db;
    color: white;
    border-radius: 8px;
    height: 3em;
    font-weight: bold;
}
.stButton>button:hover {
    background-color: #2980b9;
}
input {
    border-radius: 6px !important;
}
section[data-testid="stSidebar"] {
    background-color: #ecf0f1;
}
</style>
""", unsafe_allow_html=True)

# =========================
# Load Model (SAFE)
# =========================
@st.cache_resource
def load_model():
    try:
<<<<<<< HEAD
        with open("best_logistic_model.pkl", "rb") as f:
=======
        base = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(base, "../best_logistic_model.pkl")
        with open(path, "rb") as f:
>>>>>>> c91fd36cbb11fe60870ffe8af66d418dcc14eb84
            return pickle.load(f)
    except Exception as e:
        st.error(f"❌ Model loading failed: {e}")
        return None

model = load_model()

# =========================
# Model Info (SAFE)
# =========================
if model is not None:
    model_name = list(model.named_steps.keys())[-1]
    model_type = type(model.named_steps[model_name]).__name__
else:
    model_name = "Not Loaded"
    model_type = "Error"

# =========================
# Sidebar
# =========================
st.sidebar.title("🤖 Model Info")
st.sidebar.write(f"Model: {model_type}")
st.sidebar.write(f"Pipeline Step: {model_name}")

st.sidebar.markdown("### 📊 Performance")
st.sidebar.metric("Accuracy", "0.90")
st.sidebar.metric("F1 Score", "0.89")

st.sidebar.info("⚠️ Not a medical diagnosis")

# =========================
# Header
# =========================
st.title("🦟 Dengue Prediction System")
st.markdown("### AI-based dengue risk prediction")

st.divider()

# =========================
# Input Section
# =========================
st.subheader("🧪 Blood Test Parameters")

col1, col2 = st.columns(2)

with col1:
    wbc_count = st.number_input("WBC Count", min_value=0.0)
    rbc_count = st.number_input("RBC Count", min_value=0.0)
    platelet_wbc_ratio = st.number_input("Platelet-to-WBC Ratio", min_value=0.0)
    age = st.number_input("Age", min_value=0)

with col2:
    differential_count = st.number_input("Differential Count", min_value=0.0)
    platelet_distribution_width = st.number_input("Platelet Distribution Width", min_value=0.0)
    platelet_count = st.number_input("Platelet Count", min_value=0.0)
    hemoglobin = st.number_input("Hemoglobin (g/dL)", min_value=0.0)

gender = st.selectbox("Gender", ["Male", "Female"])

st.divider()

# =========================
# Prediction
# =========================
if st.button("🔍 Predict Dengue Risk", use_container_width=True):

    if model is None:
        st.error("❌ Model not loaded. Please check file path.")
    else:
        input_data = pd.DataFrame({
            'wbc_count': [wbc_count],
            'differential_count': [differential_count],
            'rbc_count': [rbc_count],
            'platelet_distribution_width': [platelet_distribution_width],
            'Platelet-to-WBC Ratio': [platelet_wbc_ratio],
            'age': [age],
            'platelet_count': [platelet_count],
            'hemoglobin_g_dl': [hemoglobin],
            'gender': [gender]
        })

        try:
            prediction = model.predict(input_data)[0]

            st.subheader("📊 Prediction Result")

            # Score handling
            if hasattr(model, "predict_proba"):
                prob = model.predict_proba(input_data)[0][1]
                st.progress(float(prob))
                st.write(f"Risk Probability: {prob:.2%}")

            elif hasattr(model, "decision_function"):
                score = model.decision_function(input_data)[0]
                st.write(f"Model Score: {score:.2f}")

            # Prediction result
            if prediction == 0:
                st.error("⚠️ High Dengue Risk Detected")
                st.warning("Please consult a doctor immediately")
            else:
                st.success("✅ Low Dengue Risk")
                st.info("Continue monitoring symptoms")

        except Exception as e:
            st.error(f"❌ Prediction Error: {e}")

# =========================
# Footer
# =========================
st.divider()
st.caption("Built with Machine Learning & Streamlit")
