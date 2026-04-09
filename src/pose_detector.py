# import cv2
# import numpy as np
# import mediapipe as mp
# import matplotlib.pyplot as plt
# import os
# import urllib.request

# # Imports strictly from the new Tasks API
# from mediapipe.tasks import python
# from mediapipe.tasks.python import vision
# from mediapipe.tasks.python.vision import drawing_utils
# from mediapipe.tasks.python.vision import drawing_styles

# from tqdm import tqdm  # For progress bars in loops

# class PoseDetector:
#     def __init__(self, model_asset_path='pose_landmarker_heavy.task'):
#         # Pure Python fallback to download the model if missing
#         if not os.path.exists(model_asset_path):
#             if model_asset_path=='pose_landmarker_heavy.task':
#                 print(f"Model not found. Downloading to {model_asset_path}...")
#                 url = "https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_heavy/float16/1/pose_landmarker_heavy.task"
#                 urllib.request.urlretrieve(url, model_asset_path)
#                 print("✅ Download complete!")
#             elif model_asset_path == 'pose_landmarker_lite.task':
#                 print(f"Downloading Lite model to {model_asset_path}...")
#                 # NOTICE THE URL CHANGE TO 'lite'
#                 url = "https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_lite/float16/1/pose_landmarker_lite.task"
#                 urllib.request.urlretrieve(url, model_asset_path)
#                 print("✅ Download complete!")



#         # Create the PoseLandmarker object for VIDEO
#         base_options = python.BaseOptions(model_asset_path=model_asset_path)
#         options = vision.PoseLandmarkerOptions(
#             base_options=base_options,
#             running_mode=vision.RunningMode.VIDEO,
#             min_pose_detection_confidence=0.5,
#             min_pose_presence_confidence=0.5,
#             min_tracking_confidence=0.5
#         )
#         self.detector = vision.PoseLandmarker.create_from_options(options)
        
#         # Dictionary mapping MediaPipe indices to human-readable names (Excluding Face 0-10)
#         self.keypoint_names = {
#             11: 'L_Shoulder', 12: 'R_Shoulder', 13: 'L_Elbow', 14: 'R_Elbow',
#             15: 'L_Wrist', 16: 'R_Wrist', 17: 'L_Pinky', 18: 'R_Pinky',
#             19: 'L_Index', 20: 'R_Index', 21: 'L_Thumb', 22: 'R_Thumb',
#             23: 'L_Hip', 24: 'R_Hip', 25: 'L_Knee', 26: 'R_Knee',
#             27: 'L_Ankle', 28: 'R_Ankle', 29: 'L_Heel', 30: 'R_Heel',
#             31: 'L_Foot', 32: 'R_Foot'
#         }

#     def find_pose(self, img, timestamp_ms, draw=True):
#         """Processes the image and draws landmarks using the new API utilities."""
#         img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#         mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=img_rgb)

#         self.results = self.detector.detect_for_video(mp_image, int(timestamp_ms))

#         if self.results.pose_landmarks and draw:
#             annotated_rgb = self._draw_landmarks_on_image(img_rgb, self.results)
#             return cv2.cvtColor(annotated_rgb, cv2.COLOR_RGB2BGR)
            
#         return img

#     def _draw_landmarks_on_image(self, rgb_image, detection_result):
#         """Draws the skeleton and overlays text labels for the body joints."""
#         pose_landmarks_list = detection_result.pose_landmarks
#         annotated_image = np.copy(rgb_image)
        
#         # Get image dimensions to calculate pixel coordinates
#         h, w, _ = annotated_image.shape

#         pose_landmark_style = drawing_styles.get_default_pose_landmarks_style()
#         pose_connection_style = drawing_utils.DrawingSpec(color=(0, 255, 0), thickness=2)

#         for pose_landmarks in pose_landmarks_list:
#             # 1. Draw the default dots and lines
#             drawing_utils.draw_landmarks(
#                 image=annotated_image,
#                 landmark_list=pose_landmarks,
#                 connections=vision.PoseLandmarksConnections.POSE_LANDMARKS,
#                 landmark_drawing_spec=pose_landmark_style,
#                 connection_drawing_spec=pose_connection_style)
                
#             # 2. Iterate through the coordinates and add text labels
#             for idx, landmark in enumerate(pose_landmarks):
#                 # If the point is in our dictionary (11-32)
#                 if idx in self.keypoint_names:
#                     # Convert normalized 0.0-1.0 coordinate to actual X, Y pixels
#                     x, y = int(landmark.x * w), int(landmark.y * h)
                    
#                     # Put the text slightly offset (+5px) so it doesn't cover the green dot
#                     cv2.putText(
#                         annotated_image, 
#                         self.keypoint_names[idx], 
#                         (x + 5, y - 5), 
#                         cv2.FONT_HERSHEY_SIMPLEX, 
#                         0.4,           # Font scale
#                         (255, 0, 0),   # Color (Red in RGB space)
#                         1,             # Line thickness
#                         cv2.LINE_AA
#                     )

#         return annotated_image

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