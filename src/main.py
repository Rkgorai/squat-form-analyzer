import cv2
import sys
from tqdm import tqdm

# Import our custom modules
from src.pose_detector import PoseDetector
from src.squat_analyzer import SquatAnalyzer

def process_video(input_path, output_path, model_asset_path='pose_landmarker_heavy.task'):
    cap = cv2.VideoCapture(input_path)

    if not cap.isOpened():
        print(f"❌ Error: Could not open video at {input_path}")
        return

    # Initialize modules
    detector = PoseDetector(model_asset_path=model_asset_path)
    analyzer = SquatAnalyzer()

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

    progress_bar = tqdm(
        total=total_frames, 
        desc="Evaluating Squat Form", 
        unit="frames",
        file=sys.stdout, 
        position=0, 
        leave=True
    )

    while cap.isOpened():
        success, img = cap.read()
        if not success:
            break 
            
        timestamp_ms = cap.get(cv2.CAP_PROP_POS_MSEC)
        if timestamp_ms < 0: timestamp_ms = 0

        # 1. Get Pose
        img = detector.find_pose(img, timestamp_ms, draw=True)
        
        # 2. Evaluate
        if hasattr(detector, 'results') and detector.results.pose_landmarks:
            landmarks = detector.results.pose_landmarks[0]
            feedback_text, is_correct = analyzer.analyze_pose(landmarks)
            img = analyzer.draw_feedback(img, feedback_text, is_correct)
        else:
            img = analyzer.draw_feedback(img, "Waiting for subject...", False)

        # 3. Write Frame
        out.write(img)
        progress_bar.update(1)

    progress_bar.close()
    cap.release()
    out.release()
    print(f"✅ Done! Analyzed video saved to: {output_path}")