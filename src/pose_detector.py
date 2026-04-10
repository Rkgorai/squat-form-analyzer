import cv2
import numpy as np
import mediapipe as mp
import os
import urllib.request

from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe.tasks.python.vision import drawing_utils
from mediapipe.tasks.python.vision import drawing_styles

class PoseDetector:
    # FIX 1: Set the default to 'pose_landmarker_lite.task'
    def __init__(self, model_asset_path='pose_landmarker_lite.task'):
        
        # Pure Python fallback to download the correct model if missing
        if not os.path.exists(model_asset_path):
            if model_asset_path == 'pose_landmarker_heavy.task':
                print(f"Model not found. Downloading to {model_asset_path}...")
                url = "https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_heavy/float16/1/pose_landmarker_heavy.task"
                urllib.request.urlretrieve(url, model_asset_path)
                print("✅ Heavy Model Download complete!")
                
            elif model_asset_path == 'pose_landmarker_lite.task':
                print(f"Downloading Lite model to {model_asset_path}...")
                url = "https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_lite/float16/1/pose_landmarker_lite.task"
                urllib.request.urlretrieve(url, model_asset_path)
                print("✅ Lite Model Download complete!")

        base_options = python.BaseOptions(model_asset_path=model_asset_path)
        options = vision.PoseLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.VIDEO,
            min_pose_detection_confidence=0.5,
            min_pose_presence_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.detector = vision.PoseLandmarker.create_from_options(options)

    def find_pose(self, img, timestamp_ms, draw=True):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=img_rgb)

        self.results = self.detector.detect_for_video(mp_image, int(timestamp_ms))

        if self.results.pose_landmarks and draw:
            annotated_rgb = self._draw_landmarks_on_image(img_rgb, self.results)
            return cv2.cvtColor(annotated_rgb, cv2.COLOR_RGB2BGR)
            
        return img

    def _draw_landmarks_on_image(self, rgb_image, detection_result):
        pose_landmarks_list = detection_result.pose_landmarks
        annotated_image = np.copy(rgb_image)

        pose_landmark_style = drawing_styles.get_default_pose_landmarks_style()
        pose_connection_style = drawing_utils.DrawingSpec(color=(0, 255, 0), thickness=2)

        for pose_landmarks in pose_landmarks_list:
            drawing_utils.draw_landmarks(
                image=annotated_image,
                landmark_list=pose_landmarks,
                connections=vision.PoseLandmarksConnections.POSE_LANDMARKS,
                landmark_drawing_spec=pose_landmark_style,
                connection_drawing_spec=pose_connection_style)

        return annotated_image