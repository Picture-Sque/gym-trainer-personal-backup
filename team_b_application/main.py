import cv2
import time
import numpy as np

# IMPORT THE MODULES
from vision_engine import VisionEngine  # The Eyes
from logic import Squat, BicepCurl      # The Brain
from feedback import speak              # <--- NEW: The Voice 🔊

def main():
    # 1. SETUP
    cap = cv2.VideoCapture(0)
    vision = VisionEngine()

    print("\n--- AI PERSONAL TRAINER ---")
    print("1. Squat (Tracks Knee & Back)")
    print("2. Bicep Curl (Tracks Elbow)")
    choice = input("Select Exercise: ")

    if choice == '1':
        trainer = Squat()
    else:
        trainer = BicepCurl()
    
    print(f"Starting {trainer.name}...")
    speak(f"Starting {trainer.name} session") # <--- Say Hello
    
    # 2. MAIN LOOP
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: break

        # --- VISION ---
        image, landmarks = vision.process_frame(frame)
        
        # --- LOGIC ---
        feedback_text = ""
        
        if landmarks:
            # Process Reps
            rep_complete, feedback_text, angle = trainer.process(landmarks)

            # --- UI DRAWING ---
            cv2.rectangle(image, (0,0), (350, 120), (245, 117, 16), -1)
            cv2.putText(image, trainer.name.upper(), (15, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,0), 1, cv2.LINE_AA)
            cv2.putText(image, str(trainer.reps), (20, 100), 
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
            cv2.putText(image, "REPS", (20, 115), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
            cv2.putText(image, trainer.stage, (150, 100), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255,255,255), 2, cv2.LINE_AA)
            cv2.putText(image, f"Angle: {int(angle)}", (15, 145), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 1, cv2.LINE_AA)

            # --- AUDIO & TEXT FEEDBACK ---
            if feedback_text:
                # 1. DRAW IT (Visual)
                cv2.rectangle(image, (0, 420), (640, 480), (0,0,0), -1)
                
                text_color = (0, 255, 0) # Green
                if "Rest" in feedback_text or "Straighten" in feedback_text:
                    text_color = (0, 0, 255) # Red
                    
                cv2.putText(image, feedback_text, (10, 460), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, text_color, 2, cv2.LINE_AA)
                
                # 2. SPEAK IT (Audio) <--- NEW! 🔊
                print(f"Trainer Says: {feedback_text}")
                speak(feedback_text)
            
            # --- GAME OVER CHECK ---
            if trainer.game_over:
                cv2.putText(image, "GAME OVER", (180, 250), 
                            cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 5, cv2.LINE_AA)
                cv2.imshow('AI Trainer', image)
                
                speak("Session finished.") # Say goodbye
                cv2.waitKey(4000) 
                break

        cv2.imshow('AI Trainer', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()