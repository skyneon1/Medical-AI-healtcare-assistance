# if you dont use pipenv uncomment the following:
# from dotenv import load_dotenv
# load_dotenv()

#VoiceBot UI with Gradio
import os
import gradio as gr

from brain_of_the_doctor import encode_image, analyze_image_with_query
from voice_of_the_patient import transcribe_with_groq

#load_dotenv()

system_prompt="""You have to act as a professional doctor, i know you are not but this is for learning purpose.
            What's in this image?. Do you find anything wrong with it medically?
            If you make a differential, suggest some remedies for them. Donot add any numbers or special characters in
            your response. Your response should be in one long paragraph. Also always answer as if you are answering to a real person.
            Donot say 'In the image I see' but say 'With what I see, I think you have ....'
            Dont respond as an AI model in markdown, your answer should mimic that of an actual doctor not an AI bot,
            Keep your answer concise (max 2 sentences). No preamble, start your answer right away please"""


def process_inputs(audio_filepath, image_filepath, text_input):
    # Process text input or audio input
    if text_input:
        query_text = text_input
    elif audio_filepath:
        query_text = transcribe_with_groq(GROQ_API_KEY=os.environ.get("GROQ_API_KEY"),
                                         audio_filepath=audio_filepath,
                                         stt_model="whisper-large-v3")
    else:
        query_text = ""

    # Handle the image input
    if image_filepath:
        doctor_response = analyze_image_with_query(query=system_prompt+query_text, encoded_image=encode_image(image_filepath), model="llama-3.2-11b-vision-preview")
    else:
        doctor_response = "No image provided for me to analyze"

    return query_text, doctor_response


# Create the interface
iface = gr.Interface(
    fn=process_inputs,
    inputs=[
        gr.Audio(sources=["microphone"], type="filepath", label="Voice Input (Optional)"),
        gr.Image(type="filepath", label="Medical Image"),
        gr.Textbox(label="Text Input (Optional)")
    ],
    outputs=[
        gr.Textbox(label="Your Question"),
        gr.Textbox(label="Doctor's Response")
    ],
    title="AI Doctor with Vision, Voice, and Text"
)

iface.launch(debug=True)

#http://127.0.0.1:7860