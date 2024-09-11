import hashlib
import os

import openai
from openai import OpenAI
from dotenv import load_dotenv
from IPython.display import display, Image, Audio

load_dotenv()
client = OpenAI()
client.api_key = os.getenv("OPENAI_API_KEY")

import cv2  # We're using OpenCV to read video, to install !pip install opencv-python
import base64
import time
import requests
from pytube import YouTube

# Get user input YouTube video URL
video_url = input("Enter the YouTube video URL: ")

#
# # Download the YouTube video
youtube = YouTube(video_url)
video_stream = youtube.streams.filter(file_extension="mp4").first()
# Specify the output path where you want to save the video
hash_object = hashlib.md5()
hash_object.update(str(time.time()).encode('utf-8'))
hash_value = hash_object.hexdigest()
hash_value = hash_value[:5]
output_path = os.path.join("./videos/", hash_value)
output_image_path = os.path.join(output_path, "images")
os.makedirs(output_image_path, exist_ok=True)

# Download the video to the specified output path
video_stream.download(output_path=output_path, filename=hash_value + ".mp4")
video_name = output_path + "/" + hash_value + ".mp4"
print("Video downloaded successfully to:", video_name)
video = cv2.VideoCapture(video_name)

base64Frames = []
frame_count = 0
while video.isOpened():
    success, frame = video.read()
    if not success:
        break

    # Encode the frame to JPEG
    _, buffer = cv2.imencode(".jpg", frame)
    base64_image = base64.b64encode(buffer).decode("utf-8")
    base64Frames.append(base64_image)

    # Save the every 10th frame locally
    if frame_count % 100 == 0:
        frame_filename = os.path.join(output_image_path, f"frame_{frame_count}.jpg")
        success_write=cv2.imwrite(frame_filename, frame)
        if not success_write:
            print("Failed to save frame:", frame_filename)

    frame_count += 1

video.release()
print(len(base64Frames), "frames read.")

TPM_LIMIT = 600  # Adjust this based on your organization's TPM limit
frames_per_request = max(1, len(base64Frames) // (TPM_LIMIT // 60))

PROMPT_MESSAGES = [
    {
        "role": "user",
        "content": [
            "These are frames of a video. Create a short voiceover script in the style of David Attenborough. Only include the narration.",
            *map(lambda x: {"image": x, "resize": 768}, base64Frames[0::frames_per_request]),
        ],
    },
]
params = {
    "model": "gpt-4-vision-preview",
    "messages": PROMPT_MESSAGES,
    "max_tokens": 500,
}

result = client.chat.completions.create(**params)
print(result.choices[0].message.content)
# write transcript to file
text_file_path = os.path.join(output_path, hash_value + ".txt")
with open(text_file_path, "w") as f:
    f.write(result.choices[0].message.content)

response = openai.audio.speech.create(
  model="tts-1",
  voice="alloy",
  input=result.choices[0].message.content,
)

speech_file_path = os.path.join(output_path, hash_value + ".mp3")
response.stream_to_file(speech_file_path)
print("Audio file saved to:", speech_file_path)

