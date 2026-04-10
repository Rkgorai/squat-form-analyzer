import cv2
import streamlit as st
import time
import tempfile
import os

# Import our custom modules
from src.pose_detector import PoseDetector
from src.squat_analyzer import SquatAnalyzer

# ---------------------------------------------------------
# UI Configuration & CSS fixes
# ---------------------------------------------------------
st.set_page_config(page_title="Squat Form Analyzer", page_icon="🏋️", layout="wide")

st.markdown(
    """
    <style>
    /* 1. Target the Streamlit image container */
    [data-testid="stImage"] {
        max-height: 70vh !important;
        display: flex !important;
        justify-content: center !important;
        overflow: hidden !important;
    }
    
    /* 2. Target the actual image inside */
    [data-testid="stImage"] img {
        max-height: 70vh !important;
        width: auto !important; /* This stops Streamlit from forcing 100% width */
        object-fit: contain !important;
    }
    
    /* 3. Make the metrics on the right side stick to the top */
    [data-testid="column"]:nth-of-type(2) {
        position: sticky;
        top: 3rem;
    }

    /* 4. Custom Button Colors (Grey for Start, Red for Stop) */
    div.stButton > button[kind="secondary"] {
        background-color: #6c757d !important;
        color: white !important;
        border: none !important;
        width: 100%;
    }
    div.stButton > button[kind="secondary"]:hover {
        background-color: #5a6268 !important;
    }
    
    div.stButton > button[kind="primary"] {
        background-color: #dc3545 !important;
        color: white !important;
        border: none !important;
        width: 100%;
    }
    div.stButton > button[kind="primary"]:hover {
        background-color: #c82333 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🏋️ Real-Time Squat Form Analyzer")
st.markdown("Upload a video or use your webcam to analyze squat form in real-time.")

# ---------------------------------------------------------
# Sidebar Controls
# ---------------------------------------------------------
st.sidebar.header("Input Controls")

# Source Selection
input_source = st.sidebar.radio("Select Input Source:", ("Webcam", "Upload Video"))

uploaded_file = None
if input_source == "Upload Video":
    uploaded_file = st.sidebar.file_uploader("Choose a video file", type=["mp4", "mov", "avi"])

st.sidebar.markdown("---")
st.sidebar.header("Performance Settings")

# Model Selection
model_choice = st.sidebar.selectbox(
    "Select AI Model:", 
    ("Lite (Fastest, CPU-friendly)", "Heavy (Most Accurate)")
)
model_path = 'pose_landmarker_lite.task' if "Lite" in model_choice else 'pose_landmarker_heavy.task'

# Resolution Control
use_original_res = st.sidebar.checkbox(
    "Run at Original Resolution", 
    value=False, 
    help="If unchecked, video is downscaled width to 640px to vastly improve FPS."
)

st.sidebar.markdown("---")

# ---------------------------------------------------------
# State Management & Dynamic Button
# ---------------------------------------------------------
# Initialize the session state variable if it doesn't exist yet
if 'analyze_running' not in st.session_state:
    st.session_state.analyze_running = False

# Function to flip the state when the button is clicked
def toggle_analysis():
    st.session_state.analyze_running = not st.session_state.analyze_running

# Render the dynamic button based on the current state
if st.session_state.analyze_running:
    # If running, show the RED Stop button
    st.sidebar.button("Stop Analysis", type="primary", on_click=toggle_analysis)
else:
    # If stopped, show the GREY Start button
    st.sidebar.button("Start Analysis", type="secondary", on_click=toggle_analysis)

st.sidebar.info("💡 **Tip:** Face left or right. The system will automatically detect your orientation.")

# ---------------------------------------------------------
# Main Dashboard Layout
# ---------------------------------------------------------
col1, col2 = st.columns([2, 1])

with col1:
    stframe = st.empty()

with col2:
    st.subheader("Live Feedback")
    status_placeholder = st.empty()
    feedback_placeholder = st.empty()

# ---------------------------------------------------------
# Application Logic
# ---------------------------------------------------------
# Check the session state memory instead of a standard variable
if st.session_state.analyze_running:
    # Determine Video Source
    if input_source == "Webcam":
        cap = cv2.VideoCapture(0)
    else:
        if uploaded_file is not None:
            tfile = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
            tfile.write(uploaded_file.read())
            cap = cv2.VideoCapture(tfile.name)
        else:
            st.warning("Please upload a video file first.")
            st.stop()
    
    # Initialize our AI modules
    detector = PoseDetector(model_asset_path=model_path)
    analyzer = SquatAnalyzer()
    
    # Setup Frame Skipper
    frame_counter = 0
    skip_rate = 2 
    last_timestamp_ms = 0
    
    while cap.isOpened():
        success, img = cap.read()
        if not success:
            st.info("End of video stream.")
            # Automatically flip the button back to grey when the video ends
            st.session_state.analyze_running = False
            st.rerun()
            break
            
        # Conditionally resize the image while maintaining aspect ratio
        if not use_original_res:
            target_width = 640
            h, w, _ = img.shape
            target_height = int(target_width * (h / w))
            img = cv2.resize(img, (target_width, target_height))
        
        frame_counter += 1
        
        # Frame skip logic
        if frame_counter % skip_rate != 0:
            continue
            
        # Get timestamp safely
        if input_source == "Webcam":
            timestamp_ms = int(time.time() * 1000)
            # Prevent MediaPipe crash if CPU processes frames faster than 1ms
            if timestamp_ms <= last_timestamp_ms:
                timestamp_ms = last_timestamp_ms + 1
            last_timestamp_ms = timestamp_ms
        else:
            timestamp_ms = int(cap.get(cv2.CAP_PROP_POS_MSEC))
            if timestamp_ms <= 0: timestamp_ms = 1
        
        # A. Process Pose
        img = detector.find_pose(img, timestamp_ms, draw=True)
        
        # B. Evaluate Form
        if hasattr(detector, 'results') and detector.results.pose_landmarks:
            landmarks = detector.results.pose_landmarks[0]
            feedback_text, is_correct = analyzer.analyze_pose(landmarks)
            
            if is_correct:
                status_placeholder.success("Form is Perfect!")
                feedback_placeholder.info("✅ Keep going!")
            else:
                status_placeholder.error("Form Correction Needed")
                feedback_placeholder.warning(feedback_text.replace("❌ ", ""))
                
            img = analyzer.draw_feedback(img, feedback_text, is_correct)
        else:
            status_placeholder.warning("Waiting for subject...")
            feedback_placeholder.empty()

        # C. Render to Streamlit UI
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        stframe.image(img_rgb, channels="RGB", use_container_width=True)
        
    cap.release()
    if input_source == "Upload Video" and uploaded_file is not None:
        os.unlink(tfile.name)