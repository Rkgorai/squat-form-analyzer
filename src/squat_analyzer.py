import math
import cv2

class SquatAnalyzer:
    def __init__(self):
        self.is_squatting = False
        
    def calculate_angle(self, p1, p2, p3):
        radians = math.atan2(p3.y - p2.y, p3.x - p2.x) - math.atan2(p1.y - p2.y, p1.x - p2.x)
        angle = abs(radians * 180.0 / math.pi)
        if angle > 180.0:
            angle = 360.0 - angle
        return angle

    def analyze_pose(self, pose_landmarks):
        if not pose_landmarks:
            return "No person detected.", False

        # ---------------------------------------------------------
        # 1. DYNAMIC PROFILE DETECTION (Left vs. Right Side)
        # ---------------------------------------------------------
        # Compare visibility of the hips to determine which side is facing the camera
        left_hip_vis = pose_landmarks[23].visibility
        right_hip_vis = pose_landmarks[24].visibility

        if right_hip_vis > left_hip_vis:
            # Right side of the body is facing the camera
            shoulder = pose_landmarks[12]
            hip = pose_landmarks[24]
            knee = pose_landmarks[26]
            ankle = pose_landmarks[28]
            toe = pose_landmarks[32]
        else:
            # Left side of the body is facing the camera
            shoulder = pose_landmarks[11]
            hip = pose_landmarks[23]
            knee = pose_landmarks[25]
            ankle = pose_landmarks[27]
            toe = pose_landmarks[31]

        feedback = []
        is_correct = True

        # ---------------------------------------------------------
        # 2. EVALUATION RULES
        # ---------------------------------------------------------
        
        # RULE 1: Hip Depth (Y-axis is universal regardless of orientation)
        if hip.y < knee.y:
            feedback.append("Lower your hips further")
            is_correct = False

        # RULE 2: Knee Extension (X-axis depends on facing direction)
        # In OpenCV, X increases from left to right.
        # If toe.x > ankle.x, they are facing Right. If toe.x < ankle.x, they are facing Left.
        is_facing_right = toe.x > ankle.x
        
        if is_facing_right:
            # Facing Right: Knee violation occurs if knee is further right than toe
            if knee.x > (toe.x + 0.02):
                feedback.append("Maintain knees behind toes")
                is_correct = False
        else:
            # Facing Left: Knee violation occurs if knee is further left than toe
            if knee.x < (toe.x - 0.02):
                feedback.append("Maintain knees behind toes")
                is_correct = False

        # RULE 3: Back Angle (Calculated relative to a vertical drop from the hip)
        vertical_ref = type('Point', (), {'x': hip.x, 'y': 0})() 
        back_angle = self.calculate_angle(shoulder, hip, vertical_ref)
        
        if back_angle > 45.0:
            feedback.append("Straighten your back")
            is_correct = False

        # ---------------------------------------------------------
        # 3. COMPILE FEEDBACK
        # ---------------------------------------------------------
        if is_correct:
            final_feedback = "✅ Correct Posture"
        else:
            final_feedback = "❌ " + " | ".join(feedback)

        return final_feedback, is_correct

    def draw_feedback(self, img, feedback_text, is_correct):
        color = (0, 255, 0) if is_correct else (0, 0, 255)
        
        # Get dynamic image dimensions
        h, w, _ = img.shape
        
        # Draw the background rectangle across the full dynamic width
        overlay = img.copy()
        cv2.rectangle(overlay, (0, 0), (w, 60), (0, 0, 0), cv2.FILLED)
        cv2.addWeighted(overlay, 0.6, img, 0.4, 0, img)
        
        clean_text = feedback_text.replace("❌ ", "Error: ").replace("✅ ", "")
        
        # Reduce font scale from 1 to 0.7 so long compound errors fit on smaller screens
        cv2.putText(img, clean_text, (15, 40), cv2.FONT_HERSHEY_SIMPLEX, 
                    0.7, color, 2, cv2.LINE_AA)
        return img