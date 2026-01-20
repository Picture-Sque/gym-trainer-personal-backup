import pyttsx3
import threading

def speak_thread(text):
    """
    This function runs in a separate thread.
    It initializes a temporary engine for each command to avoid freezing the video.
    """
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 150) # Speed of speech
        engine.say(text)
        engine.runAndWait()
    except:
        pass

def speak(text):
    """
    Call this function from main.py.
    It starts the speaking process in the background.
    """
    # We use a Thread so the camera doesn't freeze while the AI talks
    t = threading.Thread(target=speak_thread, args=(text,))
    t.start()