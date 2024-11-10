# django modules
from django.urls import reverse
from django.db import IntegrityError
from django.contrib.sessions.models import Session
from django.shortcuts import  render, get_object_or_404
from django.http import HttpResponse, JsonResponse  

# import
import os
import json
from dotenv import load_dotenv
import requests
import instaloader
from . import constant 
from . import extract
from openai import OpenAI
from .amazon_product_search import amazon_product_search 
from json import loads
import cv2
from moviepy.editor import VideoFileClip
import time
import base64
load_dotenv()
client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)


def process_video(video_path, seconds_per_frame=2):
    base64Frames = []   
    base_video_path, _ = os.path.splitext(video_path)

    video = cv2.VideoCapture(video_path)
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = video.get(cv2.CAP_PROP_FPS)
    frames_to_skip = int(fps * seconds_per_frame)
    curr_frame=0

    # Loop through the video and extract frames at specified sampling rate
    while curr_frame < total_frames - 1:
        video.set(cv2.CAP_PROP_POS_FRAMES, curr_frame)
        success, frame = video.read()
        if not success:
            break
        _, buffer = cv2.imencode(".jpg", frame)
        base64Frames.append(base64.b64encode(buffer).decode("utf-8"))
        curr_frame += frames_to_skip
    video.release()

    # Extract audio from video
    audio_path = f"{base_video_path}.mp3"
    clip = VideoFileClip(video_path)
    clip.audio.write_audiofile(audio_path, bitrate="32k")
    clip.audio.close()
    clip.close()

    print(f"Extracted {len(base64Frames)} frames")
    print(f"Extracted audio to {audio_path}")
    return base64Frames, audio_path



def ask_ai(base64Frames,transcription):
    try:
        prompt = constant.prompt
        print("post text inside function: "+transcription.text)

            ## Generate a summary with visual and audio
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
            {"role": "system", "content":constant.prompt},
            {"role": "user", "content": [
                "These are the frames from the video.",
                *map(lambda x: {"type": "image_url", 
                                "image_url": {"url": f'data:image/jpg;base64,{x}', "detail": "low"}}, base64Frames),
                {"type": "text", "text": f"The audio transcription is: {transcription.text}"}
                ],
            }
        ],
            temperature=0,
        )
        print(response.choices[0].message.content)
        return response
    except Exception as error:
        print("Error, while ai response:",error)
        return None

def index(request):
    post_info = {}
    if request.method == "POST":
        print("Post Request receive")
        post_url = request.POST.get("post_url")  # Use request.POST to get the URL
        post_info = extract.extract_post_info(post_url)
        print(f"Post Info. {post_info}")
        # Define default values for None objects
        default_values = {
            'content': "No Post Description Found",
            'images': "No Images Found",
            'platform': "Unknown",
            'author': "Unknown"
        }

        if post_info['images']:
              # Replace None values with default values for any missing or None fields
            for key, default_value in default_values.items():
                post_info[key] = post_info.get(key, default_value) or default_value
            response = ask_ai(post_info['images'],post_info['content'])
        else:
            print("missing video")


        # # Create a folder to save images
        # folder_name = "down_image"
        # save_images(post_info['images'], folder_name)

           
        if(response == None):
            return HttpResponse("<p>Error, while asking gpt about product</p>")
        print(response.choices[0].message.content.split("```"))
        ai_response= response.choices[0].message.content.replace("```","").replace("json","").replace("\n","")
        ai_response = loads(ai_response)
        print(ai_response)
        amazon_search_result= amazon_product_search(f'{ai_response.get("query")},' + ai_response.get("brand"))
        print(amazon_search_result)

        return render(request, "amaze/index.html", {
            'images': post_info['images'],
            'ai_res': response.choices[0].message.content,
            'heading': "Extracted Post Information:",  # Use quotes around keys
            'Platform': post_info['platform'],  # Remove curly braces and quotes
            'Author': post_info['author'],
            'Content': post_info['content'],
            'products':amazon_search_result
        })

    return render(request, "amaze/index.html")  # Handle GET request

def new(request):
    return render(request, "amaze/new.html")
