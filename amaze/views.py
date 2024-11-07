# django modules
from django.urls import reverse
from django.db import IntegrityError
from django.contrib.sessions.models import Session
from django.shortcuts import  render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse  

# import
import os
import json
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import instaloader
from * import constant 
from openai import OpenAI
load_dotenv()
client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)
def download_image(url, folder_path, image_name):
    """Downloads an image from a URL and saves it to a specified folder."""
    try:
        print(f"url: {url}")
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
        image_path = os.path.join(folder_path, image_name)
        with open(image_path, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded: {image_name}")
    except Exception as e:
        print(f"Error downloading image {image_name}: {e}")

def extract_instagram_post_info(url):
    """Extracts information from an Instagram post and downloads images using instaloader."""
    loader = instaloader.Instaloader(
        download_comments=False,
        download_geotags=True,
        download_pictures=True,
        download_video_thumbnails=False,
        save_metadata=True
    )
    shortcode = url.split('/')[-2]
    try:
        post = instaloader.Post.from_shortcode(loader.context, shortcode)       
        # Extracting post details
        post_info = {
            'platform': 'Instagram',
            'author': post.owner_username,
            'content': post.caption,  # Caption of the post
            'images': [node.display_url for node in post.get_sidecar_nodes()] if post.is_video else [post.url]  # Handle video posts
        }
        # Download the post to a folder named after the shortcode
        loader.download_post(post, target=shortcode)
        return post_info
    except Exception as e:
        print(f"Error extracting Instagram post: {e}")
        return None

def extract_twitter_post_info(url):
    """Extracts information from a Twitter post and downloads images."""
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extracting post details
    try:
        post_content = soup.find('meta', property='og:description')['content']
        post_images = [img['content'] for img in soup.find_all('meta', property='og:image')]
        post_author = soup.find('meta', property='og:title')['content'].split(' ')[0]  # Assuming the first word is the username

        return {
            'platform': 'Twitter',
            'author': post_author,
            'content': post_content,
            'images': post_images
        }
    except Exception as e:
        print(f"Error extracting Twitter post: {e}")
        return None

def extract_facebook_post_info(url):
    """Extracts information from a Facebook post and downloads images."""
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extracting post details
    try:
        post_content = soup.find('meta', property='og:description')['content']
        post_images = [img['content'] for img in soup.find_all('meta', property='og:image')]
        post_author = soup.find('meta', property='og:title')['content'].split(' ')[0]  # Assuming the first word is the username

        return {
            'platform': 'Facebook',
            'author': post_author,
            'content': post_content,
            'images': post_images
        }
    except Exception as e:
        print(f"Error extracting Facebook post: {e}")
        return None

def extract_post_info(url):
    """Extracts post information based on the social media platform."""
    if 'instagram.com' in url:
        return extract_instagram_post_info(url)
    elif 'twitter.com' in url:
        return extract_twitter_post_info(url)
    elif 'facebook.com' in url:
        return extract_facebook_post_info(url)
    else:
        print("Unsupported platform.")
        return None

def save_images(images, folder_path):
    """Saves images to the specified folder."""
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    for index, image_url in enumerate(images):
        image_name = f"image_{index + 1}.jpg"  # Naming images sequentially
        download_image(image_url, folder_path, image_name)

def askAi(post_images,post_text):
    prompt = constant.prompt
    print("post text inside function: "+post_text)

    response = client.chat.completions.create(
        model="gpt-4o-mini",

        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt+"The Text: "+post_text},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"{post_images[0]}"},
                    },
                ],
            }
        ],
    )
    return response

def index(request):
    if request.method == "POST":
        print("Post Request receive")
        post_url = request.POST.get("post_url")  # Use request.POST to get the URL
        post_info = extract_post_info(post_url)

        # Define default values for None objects
    default_values = {
      'content': "No Post Description Found",
      'images': "No Images Found",
      'platform': "Unknown",
      'author': "Unknown"
    }

# Replace None values with default values for any missing or None fields
  for key, default_value in default_values.items():
      post_info[key] = post_info.get(key, default_value) or default_value
 
        # Create a folder to save images
        folder_name = "down_image"
        save_images(post_info['images'], folder_name)
        print("\nExtracted Post Information:")
        print(f"Platform: {post_info['platform']}")
        print(f"Author: {post_info['author']}")
        print(f"Content: {post_info['content']}")
        print(f"Image: {post_info['images']}")
        response = askAi(post_info['images'],post_info['content'])
        print(response.choices[0].message.content)

        return render(request, "amaze/index.html", {
            'images': post_info['images'],
            'ai_res': response.choices[0].message.content,
            'heading': "Extracted Post Information:",  # Use quotes around keys
            'Platform': post_info['platform'],  # Remove curly braces and quotes
            'Author': post_info['author'],
            'Content': post_info['content'],
        })
        

    return render(request, "amaze/index.html")  # Handle GET request

def new(request):
    return render(request, "amaze/new.html")
