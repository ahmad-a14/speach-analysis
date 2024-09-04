import streamlit as st
from pathlib import Path
import os
from streamlit_mic_recorder import mic_recorder
from main import get_transcript, analyze_text, create_sharp_donut_sentiment_pie_chart

def print_data(json_resp):
    with st.spinner('Processing...'):
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("<h2 style='color: red;'>Sentiment</h2>", unsafe_allow_html=True)
            st.write(json_resp["sentiment"])

            st.markdown("<h2 style='color: red;'>Summary</h2>", unsafe_allow_html=True)
            st.write(json_resp["summary"])

        with col2:
            st.markdown("<h2 style='color: red;'>Topics</h2>", unsafe_allow_html=True)
            st.write(", ".join(json_resp["topics"]))

            st.markdown("<h2 style='color: red;'>Sentiment Distribution</h2>", unsafe_allow_html=True)
            sentiment_dist = json_resp["sentiment_distribution"]
            st.write(f"**Positive:** {sentiment_dist['positive']}%")
            st.write(f"**Negative:** {sentiment_dist['negative']}%")
            st.write(f"**Neutral:** {sentiment_dist['neutral']}%")
        fig = create_sharp_donut_sentiment_pie_chart(json_resp['sentiment_distribution'])
        st.pyplot(fig)



def main():
    st.title("Nayatel Sentiment Analysis Assistant")

    # Add radio buttons for selecting the model type
    # model_type = st.radio("Select Whisper model:", ("Whisper en to en", "Whisper many to en"))
    # model_type = st.selectbox("Select Whisper model:", ("Whisper English to English", "Whisper Multi-lingual"))


    # Add radio buttons for selecting recording method
    recording_method = st.radio("Select recording method:", ("Upload file", "Record from microphone"))

    if recording_method == "Upload file":
        uploaded_file = st.file_uploader("Choose a voice file", type=["wav", "mp3", "flac", "mp4"])

        if uploaded_file is not None:
            # Read the contents of the file
            file_contents = uploaded_file.read()
            # Save the file
            file_name = uploaded_file.name
            with open(f"temp_audio_{file_name}", "wb") as f:
                f.write(file_contents)
            
            text = get_transcript(f"temp_audio_{file_name}")
            # st.write(text)
            json_resp = analyze_text(text)
            
            st.json(json_resp)
            # Create columns for organized display
            # Create columns for organized display

            print_data(json_resp)
            

    elif recording_method == "Record from microphone":
        # Hide file uploader
        st.info("Speak into the microphone...")

        audio = mic_recorder(
            start_prompt="Start recording",
            stop_prompt="Stop recording",
            just_once=False,
            use_container_width=False,
            callback=None,
            args=(),
            kwargs={},
            key=None
        )
        if audio is not None:
            
            # Save the recorded audio to file
            file_name = "recorded_audio.wav"
            file_contents = audio['bytes']
            audio_path = Path(file_name)
            
            with open(audio_path, "wb") as f:
                f.write(file_contents)
                
            text = get_transcript(audio_path)
            # st.write(text)
            json_resp = analyze_text(text)
            
            st.json(json_resp)
            # Create columns for organized display
            # Create columns for organized display

            print_data(json_resp)
            
            
            

if __name__ == "__main__":
    main()