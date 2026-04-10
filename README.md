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
- [How It Works](#how-it-works)

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

## 🔍 How It Works

### Architecture Overview

```
Input Video/Stream
       ↓
[Frame Extraction]
       ↓
[Pose Detector - MediaPipe]
       ↓
[Landmark Extraction]
       ↓
[Squat Form Analyzer]
       ↓
[Real-time Feedback & Visualization]
       ↓
Output (Display or Video File)
```

### Key Components

#### 1. **PoseDetector** (`src/pose_detector.py`)
- Wraps MediaPipe Pose estimation
- Automatically downloads models on first run
- Detects 33 body landmarks with confidence scores
- Handles both webcam and video file inputs
- Performs pose visualization with annotations

#### 2. **SquatAnalyzer** (`src/squat_analyzer.py`)
- Analyzes detected pose landmarks
- Calculates angles between body joints
- Auto-detects person's orientation (left/right facing)
- Validates squat depth and form
- Generates corrective feedback
- Provides real-time visual feedback overlays

#### 3. **Streamlit App** (`app.py`)
- Interactive web interface
- Real-time video streaming and display
- Live feedback dashboard
- Model and resolution selection
- Webcam and video file support

#### 4. **Main Processing Pipeline** (`src/main.py`)
- Processes entire videos frame-by-frame
- Applies pose detection to each frame
- Evaluates squat form
- Writes annotated output video
- Shows progress bar with ETA

---

## 📝 Notes

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
