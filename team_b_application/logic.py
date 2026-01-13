import time
import numpy as np # KD, you might need to 'pip install numpy' if you haven't yet

class RepCounter:
    def __init__(self):
        self.reps = 0
        self.stage = "UP"
        
        # Time Tracking
        self.start_time = 0
        self.rep_durations = [] # List to store history of ALL reps
        self.baseline_speed = 0 # Average of the first 3 "Fresh" reps
        self.is_fatigued = False

    def process_angle(self, knee_angle):
        feedback = None
        rep_complete = False

        # 1. Detect Going DOWN (Start Timer)
        if knee_angle < 90:
            if self.stage == "UP":
                self.stage = "DOWN"
                self.start_time = time.time()
                print(" -> Logic: DOWN (Timer Started)")

        # 2. Detect Coming UP (End Timer)
        if knee_angle > 160:
            if self.stage == "DOWN":
                self.stage = "UP"
                self.reps += 1
                
                # Calculate Duration
                current_duration = time.time() - self.start_time
                self.rep_durations.append(current_duration)
                
                rep_complete = True
                
                # --- NEW GRADUAL FATIGUE LOGIC ---
                
                # Phase 1: Establish Baseline (First 3 Reps)
                if self.reps <= 3:
                    feedback = str(self.reps)
                    # Recalculate baseline average constantly for the first 3
                    self.baseline_speed = sum(self.rep_durations) / len(self.rep_durations)
                    print(f" -> Calibration: Baseline Speed is now {round(self.baseline_speed, 2)}s")

                # Phase 2: Monitor for Gradual Drop-off (Rep 4+)
                else:
                    # Logic: If current rep is 30% slower (takes 1.3x longer) than baseline
                    threshold = self.baseline_speed * 1.5
                    
                    if current_duration > threshold:
                        self.is_fatigued = True
                        feedback = "Fatigue Detected! Take a rest."
                        print(f" -> FATIGUE! Current: {round(current_duration, 2)}s vs Baseline: {round(self.baseline_speed, 2)}s")
                    else:
                        feedback = str(self.reps)
                        
        return rep_complete, feedback