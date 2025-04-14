# if you dont use pipenv uncomment the following:
# from dotenv import load_dotenv
# load_dotenv()

# VoiceBot UI with Gradio
import os
import gradio as gr
import logging

from brain_of_the_doctor import encode_image, analyze_image_with_query
from voice_of_the_patient import transcribe_with_groq
from voice_of_the_doctor import text_to_speech_with_elevenlabs

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# System prompt for the doctor
system_prompt = """You have to act as a professional doctor, i know you are not but this is for learning purpose. 
            What's in this image?. Do you find anything wrong with it medically? 
            If you make a differential, suggest some remedies for them. Donot add any numbers or special characters in 
            your response. Your response should be in one long paragraph. Also always answer as if you are answering to a real person.
            Donot say 'In the image I see' but say 'With what I see, I think you have ....'
            Dont respond as an AI model in markdown, your answer should mimic that of an actual doctor not an AI bot, 
            Keep your answer concise (max 2 sentences). No preamble, start your answer right away please"""

def process_inputs(audio_filepath, image_filepath):
    """
    Process the audio and image inputs to generate the doctor's response.
    
    Args:
        audio_filepath: Path to the recorded audio file
        image_filepath: Path to the uploaded image file
        
    Returns:
        Tuple containing:
        - Transcribed text from the audio
        - Doctor's response to the query
        - Path to the audio file of the doctor's response
    """
    try:
        # Check if audio file exists
        if not audio_filepath:
            return "No audio recorded. Please record your question.", "I need to hear your question to help you.", None
        
        logging.info(f"Processing audio file: {audio_filepath}")
        speech_to_text_output = transcribe_with_groq(
            GROQ_API_KEY=os.environ.get("GROQ_API_KEY"), 
            audio_filepath=audio_filepath,
            stt_model="whisper-large-v3"
        )
        logging.info(f"Transcription: {speech_to_text_output}")

        # Handle the image input
        if image_filepath:
            logging.info(f"Processing image file: {image_filepath}")
            doctor_response = analyze_image_with_query(
                query=system_prompt + speech_to_text_output, 
                encoded_image=encode_image(image_filepath), 
                model="llama-3.2-11b-vision-preview"
            )
        else:
            doctor_response = "No image provided for me to analyze. Please upload an image for me to examine."
            logging.info("No image provided")

        # Generate audio response
        logging.info("Generating audio response")
        voice_of_doctor = text_to_speech_with_elevenlabs(
            input_text=doctor_response, 
            output_filepath="final.mp3"
        ) 
        
        return speech_to_text_output, doctor_response, voice_of_doctor
        
    except Exception as e:
        logging.error(f"Error in process_inputs: {str(e)}")
        import traceback
        logging.error(traceback.format_exc())
        return f"Error: {str(e)}", "I encountered an error while processing your request. Please try again.", None

# Create the interface
with gr.Blocks(title="AI Doctor with Vision and Voice") as iface:
    gr.Markdown("# AI Doctor with Vision and Voice")
    gr.Markdown("Record your question about a medical image, then upload the image for analysis.")
    
    with gr.Row():
        with gr.Column():
            audio_input = gr.Audio(sources=["microphone"], type="filepath", label="Record Your Question")
            image_input = gr.Image(type="filepath", label="Upload Medical Image")
            submit_btn = gr.Button("Get Doctor's Analysis", variant="primary")
        
        with gr.Column():
            text_output = gr.Textbox(label="Your Question (Transcribed)")
            response_output = gr.Textbox(label="Doctor's Response")
            audio_output = gr.Audio(label="Doctor's Voice")
    
    submit_btn.click(
        fn=process_inputs,
        inputs=[audio_input, image_input],
        outputs=[text_output, response_output, audio_output]
    )

# Launch the app
if __name__ == "__main__":
    try:
        logging.info("Starting AI Doctor application...")
        # Use a different server option and port
        iface.launch(debug=True, server_name="0.0.0.0", server_port=7862)
    except Exception as e:
        logging.error(f"Error launching application: {str(e)}")
        import traceback
        logging.error(traceback.format_exc())
