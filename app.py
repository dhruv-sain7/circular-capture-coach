import streamlit as st
from google import genai
from PIL import Image
import pandas as pd
import json
import os
import time

# 1. Page Configuration
st.set_page_config(page_title="Circular Capture Coach — Complete Suite", page_icon="📸", layout="wide")

st.title("📸 Circular Capture Coach — Integrated Compliance Suite")
st.subheader("Official Live Prototype for the American Circular Challenge")
st.write("---")
# Force browser webcam layouts to disable mirroring properties so right matches right
st.markdown("""
    <style>
    /* Un-mirror the live view video feed element */
    div[data-testid="stCameraInput"] video, 
    .stCameraInput video, 
    video {
        transform: scaleX(-1) !important;
        -webkit-transform: scaleX(-1) !important;
    }
    </style>
""", unsafe_allow_html=True)


# 2. Sidebar Configuration Setup
with st.sidebar:
    st.header("⚙️ Core Engine Settings")
    api_key = st.text_input("Enter Gemini API Key", type="password")
    st.caption("Engine: Gemini 3.6 Flash Active")
    st.write("---")
    
    # Navigation mode selector to bridge batch checking and live capture bonus paths
    app_mode = st.radio(
        "Select Operational Interface Mode:",
        ["📁 Challenge Dataset Batch Mode", "🎥 Real-Time Live Camera Mode"]
    )
    st.write("---")
    st.markdown("""
    ### 🛡️ Challenge Guidelines Met:
    - [x] Multi-Photo Set Parsing Matrix
    - [x] Custom Semicolon Schema Flags
    - [x] Retake vs Variance Segregation
    - [x] Bonus Live Capture Pipeline
    """)

# Helper Core Quality Inspection Engine Function
def audit_single_photo_sync(client, image, view_name):
    prompt = f"""
    Analyze this equipment photo for structural sorting compliance.
    The operational intent states this image explicitly represents the '{view_name}' view perspective.

    Evaluate against these criteria:
    1. Does the image content match the intended view name? If not, flag as mismatch.
    2. Blur: Is the subject clear or out of focus?
    3. Lighting: Check if it is 'underexposed' (too dark) or 'glare_or_overexposed' (too bright/reflections).
    4. Framing: Is the required hardware area cut off or misaligned?
    5. Label Obstruction: If the view is 'label', is the temporary orange DEMO label covered? Ignore black privacy masks entirely.

    You must respond ONLY with a raw JSON object containing these keys:
    "status": "usable" or "retake" or "needs_review",
    "issue_codes": "semicolon-separated list among: blur, underexposed, glare_or_overexposed, framing, label_obstructed. Leave blank '' if none apply",
    "reason": "short explanation statement",
    "retake_guidance": "step-by-step camera position correction instructions for the worker. If usable, write 'No action required.'"
    """
    response = client.models.generate_content(model='gemini-3.6-flash', contents=[image, prompt])
    clean_text = response.text.strip().strip('`').replace('json\n', '')
    return json.loads(clean_text)


# =========================================================================
# MODE 1: CHALLENGE DATASET BATCH MODE
# =========================================================================
if app_mode == "📁 Challenge Dataset Batch Mode":
    
    @st.cache_data
    def load_challenge_data():
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            csv_path = os.path.join(current_dir, "photo_sets.csv")
            photo_sets = pd.read_csv(csv_path)
            return photo_sets, None
        except Exception as e:
            return None, str(e)

    photo_sets_df, error_msg = load_challenge_data()

    if error_msg:
        st.error(f"⚠️ Dataset Data Tables Not Detected. Details: {error_msg}")
    else:
        st.markdown("### 📥 Step 1: Select Challenge Photo Set Target")
        available_sets = sorted(photo_sets_df['set_id'].unique().tolist())
        selected_set = st.selectbox("Choose an official Evaluation/Practice Photo Set ID from the dataset:", options=available_sets)
        
        set_records = photo_sets_df[photo_sets_df['set_id'] == selected_set]
        target_device = set_records['device_id'].iloc[0] if not set_records.empty else "UNKNOWN"
        
        st.info(f"Targeting Grouping Identifier: **{target_device}** | Contains **{len(set_records)}** associated entries.")
        st.write("---")

        st.markdown("### 🖼️ Step 2: Loaded Manifest Assets & Auto-Mapped View Intents")
        photo_set_pipeline = []
        columns_layout = st.columns(max(len(set_records), 1))
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        for idx, row in set_records.reset_index().iterrows():
            img_id = row['image_id']
            intended_view = row['intended_view']
            
            possible_paths = [
                os.path.join(current_dir, "images", f"{img_id}.jpg"),
                os.path.join(current_dir, "images", f"{img_id}.png"),
                os.path.join(current_dir, "images", f"{img_id}.jpeg"),
                os.path.join(current_dir, "images", f"{img_id}.JPEG"),
                os.path.join(current_dir, "images", f"{img_id}.JPG"),
                os.path.join(current_dir, "images", f"{img_id}.PNG")
            ]
            
            actual_path = None
            for path in possible_paths:
                if os.path.exists(path):
                    actual_path = path
                    break
                    
            with columns_layout[idx]:
                if actual_path:
                    img = Image.open(actual_path)
                    st.image(img, use_container_width=True, caption=f"ID: {img_id}")
                    st.caption(f"Intended View: **{intended_view}**")
                    photo_set_pipeline.append({"image": img, "name": img_id, "intended_view": intended_view})
                else:
                    st.warning(f"Missing image file: {img_id}")

        st.write("---")

        if photo_set_pipeline:
            st.markdown("### 🚀 Step 3: Run Automation Pipeline Validation Matrix")
            if st.button("Execute Multi-Photo Set Compliance Validation"):
                if not api_key:
                    st.error("Please configure your Gemini API key in the left configuration sidebar menu!")
                else:
                    with st.spinner("Executing rate-limit protected quality audits across images..."):
                        try:
                            client = genai.Client(api_key=api_key)
                            captured_views = {p["intended_view"] for p in photo_set_pipeline}
                            
                            photo_reports = []
                            for photo in photo_set_pipeline:
                                st.caption(f"Analyzing asset: {photo['name']}...")
                                data = audit_single_photo_sync(client, photo["image"], photo["intended_view"])
                                photo_reports.append({
                                    "name": photo["name"], "intended_view": photo["intended_view"],
                                    "status": data.get("status", "needs_review"), "issue_codes": data.get("issue_codes", ""),
                                    "reason": data.get("reason", "No reason."), "retake_guidance": data.get("retake_guidance", "No guidance.")
                                })
                                time.sleep(1.5) # Protect token ceiling allocations

                            required_views = {"front", "rear_ports", "label"}
                            missing_views = list(required_views - captured_views)
                            
                            st.write("## 📊 Live Audit Assessment Report Dashboard")
                            st.markdown("### 📋 Set-Level Required View Verification Status")
                            if not missing_views:
                                st.success("✅ Complete Set Integrity Confirmed! All 3 required perspectives ('front', 'rear_ports', 'label') are present.")
                            else:
                                st.error(f"❌ Missing Required Views: {'; '.join(missing_views)}")

                            st.markdown("### 🔍 Individual Image Quality Inspection Matrix")
                            for rep in photo_reports:
                                with st.expander(f"📷 Asset ID: {rep['name']} — Intended View: {rep['intended_view'].upper()}", expanded=True):
                                    if rep["status"] == "usable": st.success("STATUS: USABLE")
                                    elif rep["status"] == "retake": st.error(f"STATUS: RETAKE REQUIRED — Codes: [{rep['issue_codes']}]")
                                    else: st.warning("STATUS: HUMAN REVIEW REQUIRED")
                                    st.write(f"**Feedback:** {rep['reason']}")
                                    st.info(f"💡 **Retake Guidance:** {rep['retake_guidance']}")
                        except Exception as e:
                            st.error(f"Validation Engine Failure: {e}")

# =========================================================================
# MODE 2: REAL-TIME LIVE CAMERA EXPERIENCE (BONUS)
# =========================================================================
else:
    st.markdown("### 🎥 Bonus Feature: Live Camera Quality Coach Workspace")
    st.write("Simulate a worker on the sorting floor capturing equipment live using their active workspace device.")
    
    col_cam, col_feed = st.columns(2, gap="large")
    
    with col_cam:
        st.markdown("#### 📷 Viewport Capture Feed")
        live_view_target = st.selectbox("Specify the view angle you are about to photograph live:", options=["front", "rear_ports", "label"])
        
        # Deploy a native browser webcam interface access link widget inside the app container
        picture_stream = st.camera_input("Position the asset and snap a validation photo:")
        
    with col_feed:
        st.markdown("#### 🧠 Live Coach Real-Time Audit Metrics")
        if picture_stream is not None:
            st.image(picture_stream, caption="Live Captured Sample frame", width=250)
            
            if st.button("🚀 Process Live Image Compliance"):
                if not api_key:
                    st.error("Configure your Gemini API key inside the sidebar config menu first!")
