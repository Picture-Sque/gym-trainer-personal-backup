import time
import random
import numpy as np
from utils import calculate_angle

# ==========================================
# PARENT CLASS: THE BRAIN 🧠
# ==========================================
class Exercise:
    def __init__(self, name):
        self.name = name
        self.reps = 0
        self.game_over = False 
        
        # TIMER VARIABLES
        self.start_time = 0
        self.rep_durations = [] 
        self.baseline_speed = 0
        
        # FATIGUE SETTINGS
        self.fatigue_warning = 1.3  # Yellow
        self.fatigue_failure = 1.8  # Red

    def start_rep_timer(self):
        self.start_time = time.time()

    def stop_rep_timer(self):
        end_time = time.time()
        duration = end_time - self.start_time
        if duration < 0.1: duration = 0.1
        self.rep_durations.append(duration)
        return duration

    def get_fatigue_level(self, current_duration):
        # 1. Calibration
        if self.reps <= 3:
            self.baseline_speed = sum(self.rep_durations) / len(self.rep_durations)
            print(f"   [System] Calibration. Baseline: {round(self.baseline_speed, 2)}s")
            return 0 
            
        # 2. Monitoring
        else:
            yellow_limit = self.baseline_speed * self.fatigue_warning
            red_limit = self.baseline_speed * self.fatigue_failure
            
            if current_duration > red_limit:
                print(f"   [System] RED LIGHT 🔴")
                return 2 # FAILURE
            elif current_duration > yellow_limit:
                print(f"   [System] YELLOW LIGHT 🟡")
                return 1 # WARNING
            else:
                return 0 # GOOD

# ==========================================
# CHILD CLASS 1: SQUAT 🏋️
# ==========================================
class Squat(Exercise):
    def __init__(self):
        super().__init__("Squat")
        self.stage = "UP"
        self.last_speech_time = 0
        self.speech_cooldown = 5.0 # Increased cooldown so long sentences finish
        
        # --- NEW LONG & NATURAL VOCABULARY ---
        
        # 1. Bad Form (Back) - Clear Instructions
        self.phrases_bad_back = [
            "You are leaning too far forward. Please straighten your back.",
            "Your chest is dropping down. Keep your chest lifted up.",
            "Watch your posture. Keep your spine straight to avoid injury."
        ]
        
        # 2. Yellow Light (Motivation) - Encouraging Sentences
        self.phrases_push = [
            "You are slowing down. Come on, push through the pain!",
            "Don't give up now. Maintain your speed!",
            "I know it is hard, but keep moving. You can do this."
        ]
        
        # 3. Red Light (Failure) - Professional Safety Message
        self.phrases_stop = "Fatigue detected. You should take a rest now."

    def process(self, landmarks):
        feedback = None
        rep_complete = False
        
        # 1. GET ANGLES
        if isinstance(landmarks, list):
            knee_angle = landmarks[0]
            back_angle = landmarks[1]
        elif isinstance(landmarks, (int, float)):
            knee_angle = landmarks
            back_angle = 100 
        else:
            shoulder = landmarks['LEFT_SHOULDER']
            hip = landmarks['LEFT_HIP']
            knee = landmarks['LEFT_KNEE']
            ankle = landmarks['LEFT_ANKLE']
            knee_angle = calculate_angle(hip, knee, ankle)
            back_angle = calculate_angle(shoulder, hip, knee)

        current_time = time.time()

        # 2. FORM CHECK (Bad Back Logic)
        if knee_angle < 120 and back_angle < 60:
            if (current_time - self.last_speech_time) > self.speech_cooldown:
                feedback = random.choice(self.phrases_bad_back)
                self.last_speech_time = current_time
                print(f" -> COACH: {feedback}")

        # 3. REP LOGIC
        if knee_angle < 90:
            if self.stage == "UP":
                self.stage = "DOWN"
                self.start_rep_timer()
                print(f" -> {self.name} DOWN")
        
        if knee_angle > 160:
            if self.stage == "DOWN":
                self.stage = "UP"
                
                duration = self.stop_rep_timer()
                fatigue_level = self.get_fatigue_level(duration)
                
                # FAIL (Red Light)
                if fatigue_level == 2:
                    feedback = self.phrases_stop
                    self.game_over = True
                    print(f" -> FAIL (Too Slow)")
                
                # SUCCESS (Green/Yellow)
                else:
                    self.reps += 1
                    
                    # Yellow Light: Count + Long Motivation
                    if fatigue_level == 1:
                        phrase = random.choice(self.phrases_push)
                        feedback = f"{self.reps}. {phrase}"
                    
                    # Green Light: Just the Number (As you requested)
                    else:
                        feedback = str(self.reps)
                        
                    print(f" -> UP (Rep {self.reps})")
                
                rep_complete = True

        return rep_complete, feedback, knee_angle

# ==========================================
# CHILD CLASS 2: BICEP CURL 💪
# ==========================================
class BicepCurl(Exercise):
    def __init__(self):
        super().__init__("Bicep Curl")
        self.stage = "DOWN"
        
        # --- VOCABULARY ---
        # 1. Motivation (Yellow Light)
        self.phrases_push = [
            "Lift it all the way up. Don't stop now!",
            "You are getting tired, but stay strong. Keep curling!",
            "Focus on the squeeze. Do not let the weight drop."
        ]
        
        # 2. Form Correction (Swinging) - NEW!
        self.phrases_swing = [
            "Do not swing your elbow. Keep it fixed at your side.",
            "You are using your shoulder. Focus only on the bicep.",
            "Stop moving your upper arm. Lock your elbow in place."
        ]
        
        self.phrases_stop = "Fatigue detected. You should take a rest now."
        
        self.last_speech_time = 0
        self.speech_cooldown = 4.0

    def process(self, landmarks):
        feedback = None
        rep_complete = False
        current_time = time.time()
        
        # 1. GET COORDINATES
        # We need extra points for the cheat detector
        if isinstance(landmarks, (int, float)):
            # Manual Mode (Testing)
            elbow_angle = landmarks
            shoulder_angle = 10 # Assume perfect form
        else:
            # Camera Mode
            shoulder = landmarks['LEFT_SHOULDER']
            elbow = landmarks['LEFT_ELBOW']
            wrist = landmarks['LEFT_WRIST']
            hip = landmarks['LEFT_HIP'] # Needed for sway check
            
            # Angle 1: Rep Progress (Shoulder-Elbow-Wrist)
            elbow_angle = calculate_angle(shoulder, elbow, wrist)
            
            # Angle 2: Cheat Detector (Hip-Shoulder-Elbow)
            # This measures how far the elbow is from the torso
            shoulder_angle = calculate_angle(hip, shoulder, elbow)
            
        # 2. CHEAT DETECTION (The Swing Check)
        # If the arm moves forward > 30 degrees, it's a swing
        if shoulder_angle > 30:
            if (current_time - self.last_speech_time) > self.speech_cooldown:
                feedback = random.choice(self.phrases_swing)
                self.last_speech_time = current_time
                print(f" -> COACH: {feedback}")

        # 3. REP LOGIC
        # START TIMER (Going UP)
        if elbow_angle < 30:
            if self.stage == "DOWN":
                self.stage = "UP"
                self.start_rep_timer()
                print(f" -> {self.name} UP")
                
        # STOP TIMER (Going DOWN)
        if elbow_angle > 160:
            if self.stage == "UP":
                self.stage = "DOWN"
                
                duration = self.stop_rep_timer()
                fatigue_level = self.get_fatigue_level(duration)
                
                if fatigue_level == 2:
                    feedback = self.phrases_stop
                    self.game_over = True
                    print(f" -> FAIL")
                else:
                    self.reps += 1
                    if fatigue_level == 1:
                        phrase = random.choice(self.phrases_push)
                        feedback = f"{self.reps}. {phrase}"
                    else:
                        feedback = str(self.reps)
                    print(f" -> DOWN (Rep {self.reps})")
                
                rep_complete = True

        return rep_complete, feedback, elbow_angle