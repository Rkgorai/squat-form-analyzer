# 🏋️ Squat Form Analyzer

A real-time computer vision system utilizing **MediaPipe** to track human kinematics, analyze squat posture, and provide automated, corrective feedback on form accuracy. This project offers both an interactive **Streamlit web app** for real-time analysis and a **command-line interface** for batch processing videos.

## 📋 Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
  - [Streamlit App (Real-Time Analysis)](#streamlit-app-real-time-analysis)
  - [Command-Line Inference (Batch Processing)](#command-line-inference-batch-processing)
- [Model Options](#model-options)
- [Configuration & Performance](#configuration--performance)
- [Technical Approach](#-technical-approach)
- [Assumptions](#-assumptions)
- [Limitations](#️-limitations)
- [Workarounds & Recommendations](#-workarounds--recommendations)
- [Notes](#-notes)
- [Troubleshooting](#️-troubleshooting)

## ✨ Features

- **Real-Time Squat Form Analysis**: Analyze squat form using your webcam with instant feedback
- **Video Upload Support**: Upload pre-recorded videos for analysis
- **Dual Model Options**:
  - **Lite Model**: Fast, CPU-friendly (recommended for real-time webcam)
  - **Heavy Model**: More accurate pose detection (recommended for offline analysis)
- **Automatic Orientation Detection**: Works whether you face left or right
- **Live Feedback**: Visual indicators and corrective suggestions during analysis
- **Performance Optimization**: Adjustable resolution for better FPS
- **Batch Processing**: Analyze multiple videos using the command-line interface
- **Pose Visualization**: Annotated skeleton overlays with confidence indicators

## 📁 Project Structure

```
squat-form-analyzer/
├── app.py                          # Streamlit web application
├── run.py                          # Command-line inference script
├── requirements.txt                # Python dependencies
├── pose_landmarker_lite.task       # Lite pose detection model
├── pose_landmarker_heavy.task      # Heavy pose detection model
├── src/
│   ├── main.py                     # Video processing pipeline
│   ├── pose_detector.py            # MediaPipe pose detection wrapper
│   └── squat_analyzer.py           # Squat form evaluation logic
├── notebook/
│   └── main2.ipynb                 # Jupyter notebook for experimentation
├── demo/                           # Sample videos directory
└── sample_vids/                    # Additional sample videos
```

## 📦 Prerequisites

- **Python 3.8+**
- **pip** package manager
- **Webcam** (for real-time analysis in Streamlit app)
- **4GB+ RAM** recommended (8GB+ for heavy model)

## 🔧 Installation

### 1. Clone or Navigate to the Repository

```bash
cd /path/to/squat-form-analyzer
```

### 2. Create a Virtual Environment (Recommended)

```bash
python3 -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

The project requires:
- **opencv-python**: Video processing and frame manipulation
- **mediapipe**: Pose estimation and landmark detection
- **numpy**: Numerical computations
- **streamlit**: Web application framework
- **matplotlib**: Visualization (optional)
- **tqdm**: Progress bars for batch processing

### 4. Download Pose Models (Automatic)

Models are downloaded automatically on first use from Google's MediaPipe repository. You can also manually download them:

- **Lite Model**: Used for real-time analysis
- **Heavy Model**: Used for offline batch processing (higher accuracy)

Models will be placed in the project root directory.

## 🚀 Usage

### Streamlit App (Real-Time Analysis)

The interactive web app allows you to analyze squat form in real-time using your webcam or upload a video.

#### Run the Application

```bash
streamlit run app.py
```

The app will open in your default browser at `http://localhost:8501`

#### Using the App

1. **Select Input Source**:
   - **Webcam**: Real-time analysis from your camera
   - **Upload Video**: Analyze a pre-recorded video file (MP4, MOV, AVI)

2. **Configure Settings**:
   - **Model Selection**: Choose between Lite (fast) or Heavy (accurate)
   - **Resolution**: 
     - Unchecked (default): 640px width for optimal FPS
     - Checked: Original resolution for higher accuracy

3. **Start Analysis**:
   - Click **"Start Analysis"** to begin
   - The system will detect your pose and provide real-time feedback
   - Click **"Stop Analysis"** to end the session

4. **View Feedback**:
   - Live video feed with pose skeleton overlay on the left
   - Real-time status and corrective feedback on the right
   - Visual indicators for proper vs. improper form

#### Tips

- Face directly left or right for best detection
- Ensure adequate lighting and clear background
- Stand at a distance where your full body is visible
- The system works best with 1-2 people in frame

---

### Command-Line Inference (Batch Processing)

Use `run.py` to analyze videos from the command line and save annotated output videos.

#### Basic Usage

```bash
python run.py -i <input_video> -o <output_video>
```

#### Arguments

| Argument | Short | Required | Description |
|----------|-------|----------|-------------|
| `--input` | `-i` | ✅ Yes | Path to the input video file |
| `--output` | `-o` | ✅ Yes | Path where the analyzed video will be saved |
| `--model` | `-m` | ❌ No | Model to use: `pose_landmarker_lite.task` or `pose_landmarker_heavy.task` (default: `pose_landmarker_lite.task`) |

#### Examples

**Analyze a video with the Lite model:**
```bash
python run.py -i sample_vids/my_squat.mp4 -o output/analyzed_squat.mp4
```

**Analyze with the Heavy model for higher accuracy:**
```bash
python run.py -i sample_vids/my_squat.mp4 -o output/analyzed_squat.mp4 -m pose_landmarker_heavy.task
```

**Batch process multiple videos:**
```bash
for video in sample_vids/*.mp4; do
    python run.py -i "$video" -o "output/$(basename $video)"
done
```

#### Output

- An annotated video with:
  - Pose skeleton overlay
  - Landmark points with confidence scores
  - Real-time form feedback and corrections
- Same frame rate and resolution as input video
- MP4 format with H.264 codec

---

## 🤖 Model Options

### Lite Model (`pose_landmarker_lite.task`)

**Best for**: Real-time analysis, webcam streaming, CPU-only systems

- ⚡ Fast inference (~30+ FPS on CPU)
- 💾 Lightweight (~13 MB)
- 📱 CPU-friendly
- ⚠️ Slightly lower accuracy on complex poses

### Heavy Model (`pose_landmarker_heavy.task`)

**Best for**: Offline batch processing, high-accuracy requirements, machines with GPU

- 🎯 Higher accuracy and robustness
- 🚀 Better for complex or ambiguous poses
- 💪 Optimized for GPU acceleration
- 📦 Larger model (~75 MB)
- ⏱️ Slower inference (~5-15 FPS on CPU, 30+ FPS on GPU)

### Model Selection Guide

| Use Case | Recommended Model | Reason |
|----------|-------------------|--------|
| Real-time webcam | **Lite** | Smooth FPS, responsive feedback |
| Video analysis | **Heavy** | Higher accuracy |
| Limited hardware | **Lite** | Lower resource usage |
| Production quality | **Heavy** | Best accuracy |

---

## ⚙️ Configuration & Performance

### Performance Optimization

#### For Faster Performance:

1. **Use Lite Model** in Streamlit app
2. **Downscale Resolution**: Keep "Run at Original Resolution" unchecked (default)
3. **Reduce Frame Rate**: Process every 2nd or 3rd frame
4. **Lower Lighting**: Better in well-lit environments

#### For Higher Accuracy:

1. **Use Heavy Model** with offline processing
2. **Enable Original Resolution**: Check "Run at Original Resolution" in Streamlit app
3. **Ensure Proper Lighting**: Avoid shadows and glare
4. **Better Camera Quality**: Higher resolution input improves detection

### Hardware Requirements

| Component | Lite Model | Heavy Model |
|-----------|-----------|------------|
| RAM | 2-4 GB | 4-8 GB |
| CPU | Dual-core | Quad-core+ |
| GPU | Optional | Recommended |
| Disk Space | ~50 MB | ~150 MB |

---

## � Technical Approach

### Overall Architecture

The system follows a **frame-by-frame pose estimation and analysis pipeline**:

```
Input Video/Stream
       ↓
[Frame Extraction]
       ↓
[Pose Detector - MediaPipe Lite/Heavy]
       ↓
[33 Landmark Point Extraction]
       ↓
[Dynamic Profile Detection (Left/Right)]
       ↓
[Form Rule Evaluation Engine]
       ↓
[Real-time Feedback Generation & Visualization]
       ↓
Output (Streamlit Display or Annotated Video File)
```

### Core Technologies

1. **MediaPipe Pose Estimation**
   - Uses deep learning models to detect 33 body landmarks in real-time
   - Each landmark includes X, Y coordinates and confidence visibility score
   - Models: TFLite-based (FP16 precision) for edge device optimization

2. **OpenCV (cv2)**
   - Frame extraction and manipulation
   - Image resizing for performance optimization
   - Skeleton rendering and annotation
   - Video encoding (H.264 MP4v codec)

3. **Streamlit Framework**
   - Rapid prototyping of interactive web interface
   - Real-time video rendering with state management
   - Session-based state for UI control (start/stop button)
   - File upload and webcam integration

### Technical Implementation Details

#### Pose Estimation Pipeline

**MediaPipe Configuration:**
```
- Running Mode: VIDEO (optimized for sequential frame processing)
- Min Pose Detection Confidence: 0.5 (triggers pose detection if confidence ≥ 50%)
- Min Pose Presence Confidence: 0.5 (minimum confidence to include pose in results)
- Min Tracking Confidence: 0.5 (temporal smoothing threshold)
```

**Landmark Index Reference:**
```
Key Points Used:
- Shoulder: Left (11) / Right (12)
- Hip: Left (23) / Right (24)
- Knee: Left (25) / Right (26)
- Ankle: Left (27) / Right (28)
- Toe: Left (31) / Right (32)
```

#### Dynamic Orientation Detection

The system automatically detects which side of the body faces the camera:
```python
if right_hip_visibility > left_hip_visibility:
    # Use right-side landmarks (shoulder 12, hip 24, knee 26, etc.)
else:
    # Use left-side landmarks (shoulder 11, hip 23, knee 25, etc.)
```

This enables the same form validation logic to work for both left-facing and right-facing users without requiring manual configuration.

#### Form Validation Engine

Three-rule evaluation system:

1. **Hip Depth Rule**: 
   - Validates that hip Y-coordinate < knee Y-coordinate (hips below knees)
   - Indicates proper squat depth

2. **Knee Position Rule**:
   - Validates knee does not extend beyond toe position
   - Prevents excessive forward knee translation
   - Accounts for user orientation (right-facing vs. left-facing) via X-coordinate comparison

3. **Back Angle Rule**:
   - Calculates angle between shoulder-hip-vertical line
   - Threshold: Back angle ≤ 45° from vertical
   - Prevents excessive forward lean

#### Feedback Generation

- Real-time text overlay on video frames
- Color coding: Green (✅ correct) or Red (❌ error)
- Multiple simultaneous feedback messages joined by "|" separator
- Automatic text truncation for small screen compatibility

### Key Components

#### 1. **PoseDetector** (`src/pose_detector.py`)
- Wraps MediaPipe Pose estimation SDK
- Automatic model download from Google's CDN on first run
- Detects 33 body landmarks with confidence scores
- Handles both webcam and video file inputs via OpenCV
- Performs skeleton visualization with MediaPipe drawing utilities
- Stores detection results for subsequent form analysis

#### 2. **SquatAnalyzer** (`src/squat_analyzer.py`)
- Analyzes detected pose landmarks using geometric calculations
- `calculate_angle()`: Uses atan2 to compute angles between three points
- `analyze_pose()`: Implements three-rule evaluation engine
- Auto-detects person's orientation via hip visibility comparison
- Generates multi-line corrective feedback
- `draw_feedback()`: Renders overlay text with transparency

#### 3. **Streamlit App** (`app.py`)
- Interactive web UI built with Streamlit framework
- Two input modes: Webcam or video file upload
- Sidebar controls for model selection and resolution
- Session state management for start/stop analysis button
- Real-time frame visualization with feedback dashboard
- Automatic resource cleanup (temporary file deletion)
- CSS styling for custom button colors and layout optimization

#### 4. **Main Processing Pipeline** (`src/main.py`)
- Batch video processing for offline analysis
- Frame-by-frame iteration with timestamp tracking
- VideoWriter for H.264 MP4 encoding
- Progress bar with TQDM showing ETA
- Maintains original video properties (FPS, resolution, codec)

---

## � Assumptions

The system operates under the following assumptions:

### Input Assumptions

1. **Video Format & Codec**
   - Input videos are in common formats (MP4, MOV, AVI, etc.)
   - H.264 or similar widely-supported codec
   - Frame rate ≥ 20 FPS for smooth analysis
   - Valid video file accessible on disk or streamed from webcam

2. **User Position & Orientation**
   - User faces directly **left or right** (not angled or at 45°)
   - Full body is visible in frame (head to feet)
   - User stands upright between squats (for proper reference baseline)
   - Single person per frame (system focuses on first detected person)

3. **Environment & Lighting**
   - **Adequate lighting**: No dark shadows obscuring body
   - **Clear background**: High contrast between person and background (not black-on-black)
   - **Stable camera**: Minimal camera shake or movement
   - **Sufficient space**: User has room to perform full squat motion

4. **MediaPipe Landmark Availability**
   - All 33 pose landmarks are detectable (confidence ≥ 0.5)
   - Camera angle permits full visibility of hip, knee, ankle, toe landmarks
   - Body proportions are typical human morphology (not extreme body compositions)

### Processing Assumptions

1. **Timestamp Validity** (Webcam-specific)
   - System time advances monotonically (no system clock resets during session)
   - MediaPipe library requires strictly increasing timestamps in VIDEO mode
   - Fallback: Increments timestamp by 1ms if processed too quickly

2. **Frame-by-Frame Analysis**
   - No temporal memory between frames (stateless, per-frame evaluation)
   - Each frame is evaluated independently for form correctness
   - Rapid feedback without tracking squat rep state

3. **Model Availability**
   - Internet connection available on first run for model downloads
   - Models cached in project root after initial download
   - Model file integrity (no corruption)

4. **System Resources**
   - Sufficient RAM for frame buffering and model inference
   - CPU/GPU capable of processing at target FPS
   - Temporary file system available for video uploads

### User Behavior Assumptions

1. **Intentional Squat Motion**
   - User performs squat deliberately (not walking, jumping, or casual movement)
   - User understands proper squat form concepts (hip depth, knee alignment, back angle)
   - User reads and acts on feedback in real-time

2. **Compliance with Guidelines**
   - User faces left or right (not front-on or angled)
   - User stands at appropriate distance (full body visible)
   - User wears form-fitting clothing (not loose baggy clothes that obscure landmarks)

---

## ⚠️ Limitations

### Technical Limitations

1. **Single-Person Detection**
   - System only analyzes first detected person in frame
   - Multiple people in frame may cause landmark confusion
   - No multi-person tracking capability

2. **Orientation Constraints**
   - **Only left/right facing supported** (cardinal directions)
   - Angled positions (45°, 90°) not supported
   - Front-facing or back-facing poses not supported
   - Side-profile essential for proper landmark detection

3. **Lighting Sensitivity**
   - Poor lighting → decreased pose detection accuracy
   - Shadows and backlighting degrade landmark visibility
   - Reflective surfaces may cause over-exposure issues
   - Dark clothing on dark background → landmarks not detected

4. **Clothing & Body Coverage**
   - Loose/baggy clothing obscures body shape and joint positions
   - Covered joints (e.g., full-length winter gear) reduce detection confidence
   - Long hair, hats, or accessories may interfere with landmark detection
   - Extreme body types (very tall, very short, obese, muscular) may have reduced accuracy

5. **Camera Quality**
   - Low-resolution cameras (<1080p) reduce landmark precision
   - Webcams with high latency impact real-time feedback responsiveness
   - Frame rate <20 FPS creates perception of jittery feedback
   - Rolling shutter cameras may distort pose estimates

### Algorithm Limitations

1. **Form Evaluation Rigidity**
   - Fixed angle thresholds (45° back angle, knee-toe X-distance) work for typical users only
   - No personalization for individual biomechanics or limb proportions
   - Cannot distinguish between different squat styles (ATG, parallel, high-bar, low-bar)
   - All feedback rules apply equally regardless of fitness level

2. **No Rep Counting**
   - System evaluates individual frames, not continuous squat cycles
   - Cannot detect squat start/end or rep boundaries
   - No ability to count total reps performed
   - Cannot measure rest periods between sets

3. **No Temporal Tracking**
   - Feedback is per-frame, not per-rep or per-set
   - Cannot identify if errors are consistent or occasional
   - No motion smoothing across frames
   - Rapid feedback may appear jittery due to per-frame evaluation

4. **Back Angle Calculation Simplification**
   - Back angle calculated relative to vertical line through hip only
   - Does not account for hip flexion angle or knee angle
   - May give misleading results for very deep squats
   - "Vertical drop" reference point is 2D approximation

5. **No Depth Validation Personalization**
   - Hip-below-knee rule is absolute (no adjustment for femur length)
   - Short-limbed users may struggle to achieve this naturally
   - Tall users may have different biomechanical optimal depths

### Performance Limitations

1. **Inference Speed**
   - **Lite model**: ~30+ FPS on CPU-only systems
   - **Heavy model**: ~5-15 FPS on CPU, requires GPU for real-time performance
   - Webcam latency: typically 100-300ms depending on hardware
   - Video processing: slower than real-time on older machines

2. **Memory Usage**
   - Heavy model requires 4-6GB RAM peak usage
   - Large video files loaded entirely for processing (no streaming)
   - Multiple concurrent analyses not supported
   - Frame buffering for web display uses RAM

3. **Real-Time Constraints**
   - Streamlit page redraws on each frame (network/rendering overhead)
   - Resolution downscaling necessary for smooth performance on CPU
   - Frame skipping (2x drop) in Streamlit app to maintain responsiveness
   - Browser refresh lag adds to perceived latency

4. **Video Output Limitations**
   - Output codec fixed to H.264 MP4 (no custom codec selection)
   - Output resolution matches input (no resizing option in batch mode)
   - Frame rate matches input video (cannot reduce for file size)
   - No quality/bitrate control parameter

### Usability Limitations

1. **No User Feedback History**
   - No persistent storage of analysis results
   - Cannot review historical trends or improvements
   - Session data lost when page refreshed (Streamlit design)
   - No export of performance metrics or statistics

2. **Limited Error Detection**
   - Only three form rules evaluated (not comprehensive squat biomechanics)
   - No detection of equipment use (belt, knee wraps) affecting judgment
   - Cannot identify pain/injury-induced form deviations
   - Fatigue-induced form breakdown not tracked

3. **No Advanced Features**
   - No slow-motion analysis option
   - No frame-by-frame stepping (Streamlit continuous stream only)
   - No side-by-side comparison with reference form
   - No joint angle numerical display (only visual feedback)
   - No personalized form goals or objective targets

### Dependency & Compatibility

1. **Python Version**: Requires Python 3.8+ (not tested on Python 2.x)
2. **OS Compatibility**: Tested on Linux; Windows/macOS support depends on OpenCV & MediaPipe
3. **Webcam Driver**: Requires OpenCV to correctly enumerate and access webcams
4. **Browser Support**: Streamlit requires modern browser (Chrome, Firefox, Edge); not IE-compatible
5. **Model Licensing**: MediaPipe Lite/Heavy models pre-converted to FP16 (no double-precision option)

---

## 🎯 Workarounds & Recommendations

### For Better Accuracy

- **Improve Lighting**: Use natural light from front/side; avoid backlighting
- **Wear Fitted Clothing**: Compression gear or form-fitting clothes improve detection
- **Increase Distance**: Stand further back so full body occupies more frame pixels
- **Use Heavy Model**: For offline analysis where speed is not critical
- **Add GPU**: NVIDIA CUDA-compatible GPU speeds up Heavy model 5-10x

### For Multi-User Scenarios

- Process users sequentially (one at a time)
- Use wider camera angle and position users far apart
- Accept that only closest person gets analyzed
- Consider multi-person pose estimation (outside scope of this project)

### For Different Squat Styles

- Current rules assume parallel squat (hip at knee level)
- ATG (ass-to-grass) users will trigger false "hip depth correct" earlier
- High-bar squats may show higher back angle due to posture differences
- Recommend documenting expected feedback for your squat style

---

## �📝 Notes

- Models are automatically downloaded from Google's MediaPipe repository on first use
- Ensure you have internet connection for initial model downloads
- For best results, face directly left or right (avoid angled positions)
- The system supports single-person detection per frame
- Keep the environment well-lit for optimal pose detection

---

## 🛠️ Troubleshooting

### Webcam Not Working
- Grant permissions to the application
- Check if another app is using the camera
- Try a different camera (if available)

### Low FPS
- Use Lite model instead of Heavy
- Uncheck "Run at Original Resolution"
- Close background applications
- Ensure adequate lighting

### Poor Pose Detection
- Use Heavy model for better accuracy
- Ensure full body is visible in frame
- Improve lighting conditions
- Stand further back so full body fits in frame

---

## 📄 License

This project uses MediaPipe, which is licensed under the Apache License 2.0.

---

**Ready to analyze your squat form? Start with the Streamlit app or process videos in batch!** 🏋️
