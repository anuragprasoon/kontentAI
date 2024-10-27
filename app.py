import os
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi
from pytube import YouTube
import google.generativeai as genai
import requests
from bs4 import BeautifulSoup
from newspaper import Article
import streamlit as st

load_dotenv()

genai.configure(api_key=os.getenv("API"))
model = genai.GenerativeModel("gemini-1.5-flash")


def extract_blog(url):
    try:
        # First, try to use newspaper3k, which is designed for content extraction
        article = Article(url)
        article.download()
        article.parse()
        return article.text  # Returns the main text content of the article

    except Exception as e:
        print("Newspaper3k failed; attempting manual extraction.")
        
        # If newspaper3k fails, use requests and BeautifulSoup
        try:
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Custom extraction using common blog post structures
                # Look for common HTML tags or classes used in blog content
                content = ''
                for tag in ['p', 'article', 'div']:
                    paragraphs = soup.find_all(tag)
                    if paragraphs:
                        content += '\n'.join([p.get_text() for p in paragraphs])
                        break
                
                return content.strip()
            else:
                return f"Failed to retrieve the page, status code: {response.status_code}"
                
        except Exception as e:
            return f"Error during manual extraction: {e}"

def extract_yt(url):
    yt=YouTube(url)
    subtitle=''
    try:
        transcript = YouTubeTranscriptApi.get_transcript(yt.video_id)
        for entry in transcript:
            subtitle+=entry['text']+'\n' 
    except Exception as e:
        print(f"Error: {e}")
    return subtitle

form1=st.form("form")
form1.write("Welcome to Kontent-AI")
url=form1.text_input("Enter Any Youtube Link or Blog/Article Link")
twittersubmit=form1.form_submit_button("Generate Twitter Threads")
linkedinsubmit=form1.form_submit_button("Generate Linkedin Content")

if twittersubmit:
    if "youtube" in url or "youtu.be" in url:
        content=extract_yt(url)
    else:
        content=extract_blog(url)
    newcontent=model.generate_content("Convert the following content into a humanized written twiiter thread : "+content)
    form1.write(newcontent.text)

if linkedinsubmit:
    if "youtube" in url or "youtu.be" in url:
        content=extract_yt(url)
    else:
        content=extract_blog(url)
    newcontent=model.generate_content("Convert the following content into a humanized written linkedin content of 1200 character : "+content)
    form1.write(newcontent.text)
