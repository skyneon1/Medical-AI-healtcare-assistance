import gradio as gr
from voice_of_the_patient import record_audio

def simple_process(audio_filepath):
    # Just return the audio filepath to confirm it was received
    return f"Received audio file: {audio_filepath}"

# Create a simplified interface
iface = gr.Interface(
    fn=simple_process,
    inputs=[
        gr.Audio(sources=["microphone"], type="filepath")
    ],
    outputs=[
        gr.Textbox(label="Result")
    ],
    title="Simple Audio Test"
)

iface.launch(debug=True)
