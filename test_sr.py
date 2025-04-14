import speech_recognition as sr

# Create a recognizer instance
r = sr.Recognizer()

# Try to initialize the microphone
try:
    with sr.Microphone() as source:
        print("Microphone initialized successfully!")
        print(f"Using audio device: {source.device_index}")
except Exception as e:
    print(f"Error initializing microphone: {str(e)}")
    print(f"Error type: {type(e).__name__}")
