import streamlit as st
import moviepy.editor as mp
import speech_recognition as sr
from googletrans import Translator
from pydub import AudioSegment
import os
from deep_translator import GoogleTranslator

def translate_text(text, src_lang='en', dest_lang='mr'):
    translator = GoogleTranslator(source=src_lang, target=dest_lang)
    translated_text = translator.translate(text)
    return translated_text


def video_to_text_translation(video_file):
    # Save the video file temporarily
    video_path = 'temp_video.mp4'
    with open(video_path, 'wb') as f:
        f.write(video_file.getbuffer())

    # Extract audio from the video
    video = mp.VideoFileClip(video_path)
    audio_file = "extracted_audio.wav"

    # Extract audio and write to file
    video.audio.write_audiofile(audio_file)

    # Close the video file to release it
    video.close()  # Ensures the video file is properly closed before removing it

    # Speech recognition
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(audio_file) as source:
            audio_data = recognizer.record(source)  # Read the entire audio file
            recognized_text = recognizer.recognize_google(audio_data)  # Recognize speech in English
    except sr.UnknownValueError:
        recognized_text = "Could not understand the audio"
    except sr.RequestError as e:
        recognized_text = f"Could not request results from Google Speech Recognition service; {e}"

    # Translate text using deep-translator
    try:
        translated_text = translate_text(recognized_text, src_lang='en', dest_lang='mr')
    except Exception as e:
        translated_text = f"Translation error: {e}"

    # Cleanup temporary files
    os.remove(video_path)  # Now it is safe to remove the video file
    os.remove(audio_file)

    return recognized_text, translated_text


# Streamlit app layout
def main():
    st.title("Video-to-Text Translator (English to Marathi)")

    # Upload video file
    video_file = st.file_uploader("Upload a video file", type=['mp4', 'mov', 'avi', 'mkv'])

    if video_file is not None:
        st.success("Video uploaded successfully!")

        # Process the video to extract and translate text
        with st.spinner("Processing the video..."):
            original_text, translated_text = video_to_text_translation(video_file)

        # Display the recognized and translated text
        st.subheader("Recognized Text (in English):")
        st.write(original_text)

        st.subheader("Translated Text (in Marathi):")
        st.write(translated_text)

# Run the Streamlit app
if __name__ == "__main__":
    main()
