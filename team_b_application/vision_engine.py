import cv2
import mediapipe as mp
import numpy as np

class VisionEngine:
    def __init__(self):
        # 1. SETUP MEDIAPIPE (From Team A's Code)
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_pose = mp.solutions.pose
        
        # Initialize Pose with Team A's confidence settings
        self.pose = self.mp_pose.Pose(
            min_detection_confidence=0.5, 
            min_tracking_confidence=0.5
        )

    def process_frame(self, frame):
        """
        Takes a raw camera frame, finds the skeleton, 
        and returns a clean Dictionary of coordinates.
        """
        # 1. Recolor to RGB (Team A's Step 1)
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
      
        # 2. Make detection (Team A's Step 2)
        results = self.pose.process(image)
      
        # 3. Recolor back to BGR (Team A's Step 3)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        landmark_dict = {}

        # 4. Extract Landmarks (Team A's Step 4 - Simplified)
        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark
            
            # Helper to get [x, y] easily
            def get_point(landmark_name):
                return [
                    landmarks[landmark_name.value].x,
                    landmarks[landmark_name.value].y
                ]

            # --- PACKAGING DATA FOR TEAM B LOGIC ---
            # We convert MediaPipe data into your simple Dictionary format
            try:
                landmark_dict = {
                    'LEFT_SHOULDER': get_point(self.mp_pose.PoseLandmark.LEFT_SHOULDER),
                    'LEFT_ELBOW':    get_point(self.mp_pose.PoseLandmark.LEFT_ELBOW),
                    'LEFT_WRIST':    get_point(self.mp_pose.PoseLandmark.LEFT_WRIST),
                    'LEFT_HIP':      get_point(self.mp_pose.PoseLandmark.LEFT_HIP),
                    'LEFT_KNEE':     get_point(self.mp_pose.PoseLandmark.LEFT_KNEE),
                    'LEFT_ANKLE':    get_point(self.mp_pose.PoseLandmark.LEFT_ANKLE),
                    # Add Right side if needed later
                    'RIGHT_SHOULDER': get_point(self.mp_pose.PoseLandmark.RIGHT_SHOULDER),
                    'RIGHT_ELBOW':    get_point(self.mp_pose.PoseLandmark.RIGHT_ELBOW),
                    'RIGHT_WRIST':    get_point(self.mp_pose.PoseLandmark.RIGHT_WRIST),
                }
            except:
                pass # Handle cases where body is partially out of frame
            
            # Draw the Skeleton (Team A's Visuals)
            self.mp_drawing.draw_landmarks(
                image, 
                results.pose_landmarks, 
                self.mp_pose.POSE_CONNECTIONS
            )
            
        return image, landmark_dict