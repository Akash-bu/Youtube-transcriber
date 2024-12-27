import streamlit as st
from dotenv import load_dotenv
load_dotenv()

import os
import google.generativeai as genai

from youtube_transcript_api import YouTubeTranscriptApi

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

prompt = """You are Youtube video summarizer. You will be taking the transcript text
and summarizing the entire video and providing the important summary in points
within 250 words. Please provide the summary of the text given here:  """

def extract_transcript_details(youtube_url):
    try:
        video_id = youtube_url.split("=")[1]
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)

        transcript = ""
        for i in transcript_text:
            transcript += i['text']

        return transcript

    except Exception as e:
        raise e 
    

def generate_gemini_content(transcript_text, prompt):

    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content(prompt+transcript_text)
    return response.text

st.title("Youtube Video Summarizer")

youtube_link = st.text_input("Enter the Youtube URL: ")

if youtube_link:
    video_id = youtube_link.split("=")[1]
    print(video_id)
    st.image(f"https://img.youtube.com/vi/{video_id}/0.jpg", width=300)


if st.button("Summarize"):
    transcript_text = extract_transcript_details(youtube_link)

    if transcript_text:
        summary = generate_gemini_content(transcript_text, prompt)
        st.markdown(summary)
        st.write(summary)



        