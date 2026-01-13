import time
from logic import RepCounter
from feedback import speak

def main():
    print("--- AI GYM TRAINER (V2: FATIGUE EDITION) ---")
    print("Type angles to simulate. Try waiting between inputs!")
    print("Type 'q' to quit.\n")

    counter = RepCounter()
    speak("System Ready. Let's workout.")

    while True:
        user_input = input("\nEnter Knee Angle: ")
        
        if user_input.lower() == 'q':
            break
            
        try:
            angle = float(user_input)
            
            # Pass data to KD's Brain
            # Now captures TWO values: rep_complete (True/False) AND message (String)
            is_complete, message = counter.process_angle(angle)
            
            # If there is a message (either a number or a warning), speak it
            if is_complete and message:
                speak(message)
                
                # Visual Feedback in Console
                if "slow" in message:
                    print(f"⚠️  WARNING: {message}")
                else:
                    print(f"✅ Count: {message}")
                
        except ValueError:
            print("Please enter a valid number.")

if __name__ == "__main__":
    main()