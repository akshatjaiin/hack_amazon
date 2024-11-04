# django modules
from django.urls import reverse
from django.db import IntegrityError
from django.contrib.sessions.models import Session
from django.shortcuts import  render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse  

# import
import os
import json
from datetime import date
from dotenv import load_dotenv
from datetime import date
 
def get_date():
    # return current date
    return date.today() 

load_dotenv() # load env
api_key=os.getenv('CHATGPT_API') # cofiguring model api 


import os
import requests
from bs4 import BeautifulSoup

def download_image(url, folder_path, image_name):
    """Downloads an image from a URL and saves it to a specified folder."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
        image_path = os.path.join(folder_path, image_name)
        with open(image_path, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded: {image_name}")
    except Exception as e:
        print(f"Error downloading image {image_name}: {e}")

def extract_instagram_post_info(url):
    """Extracts information from an Instagram post and downloads images."""
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extracting post details
    try:
        post_content = soup.find('meta', property='og:description')['content']
        post_images = [img['content'] for img in soup.find_all('meta', property='og:image')]
        post_author = soup.find('meta', property='og:title')['content'].split(' ')[0]  # Assuming the first word is the username

        return {
            'platform': 'Instagram',
            'author': post_author,
            'content': post_content,
            'images': post_images
        }
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



def index(request):
    if request.method == "POST":
        print("Post Request receive")
        post_url = request.POST.get("post_url")  # Use request.POST to get the URL
        post_info = extract_post_info(post_url)

        # Create a folder to save images
        folder_name = "down_image"
        save_images(post_info['images'], folder_name)
        print("\nExtracted Post Information:")
        print(f"Platform: {post_info['platform']}")
        print(f"Author: {post_info['author']}")
        print(f"Content: {post_info['content']}")
        return render(request, "amaze/index.html", {
            'images': post_info['images'],
            'heading': "Extracted Post Information:",  # Use quotes around keys
            'Platform': post_info['platform'],  # Remove curly braces and quotes
            'Author': post_info['author'],
            'Content': post_info['content'],
        })

    return render(request, "amaze/index.html")  # Handle GET request

def new(request):
    return render(request, "amaze/new.html")