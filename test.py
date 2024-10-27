from youtube_transcript_api import YouTubeTranscriptApi

# Replace 'video_id' with the ID of the YouTube video
video_id = 'N87jEVBfkE0'
subtitle=''
try:
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    for entry in transcript:
        #print(f"{entry['text']}")
        subtitle+=entry['text']+'\n' 
    
except Exception as e:
    print(f"Error: {e}")

print(subtitle)