from voice_of_the_patient import record_audio
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

try:
    print("Starting audio recording test...")
    record_audio(file_path="test_recording.mp3", timeout=5, phrase_time_limit=3)
    print("Test completed successfully!")
except Exception as e:
    print(f"Error: {str(e)}")
    print(f"Error type: {type(e).__name__}")
    import traceback
    print(traceback.format_exc())
