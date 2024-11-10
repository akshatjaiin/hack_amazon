# django modules
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import  render, get_object_or_404

import os
from json import loads
from openai import OpenAI
from dotenv import load_dotenv
from . import constant, extract
from .amazon_product_search import amazon_product_search
import json
load_dotenv()
client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)

def ask_ai(frames,transcription,content):
    try:
        prompt = constant.prompt
        content = json.dumps(content)
        print("post text inside function: "+content)

            ## Generate a summary with visual and audio
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
            {"role": "system", "content":constant.prompt+"i m feeding you few post related content " + content},
            {"role": "user", "content": [
                "These are the frames from the post.",
                *map(lambda x: {"type": "image_url", 
                                "image_url": {"url": f'data:image/jpg;base64,{x}', "detail": "low"}}, frames),
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

              # Replace None values with default values for any missing or None fields
        
        response = ["empty list"]
        
        # response = ask_ai(base64Frames,transcription)
        media = extract.process_media("download")

        if media['audio_path'] != None:
            # Transcribe the audio
            transcription = client.audio.transcriptions.create(
                model="whisper-1",
                file=open(media['audio_path'], "rb"),
            )
        else:
            transcription = {'text': 'post has no transcription'}

        response=ask_ai(frames=media['frames'], transcription=transcription, content=post_info)
        query = response.choices[0].message.content
        print(query)
        amazon_search_result= amazon_product_search(query)
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
