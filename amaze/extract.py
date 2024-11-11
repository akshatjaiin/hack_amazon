# import
import os
import json
from dotenv import load_dotenv
import requests
import instaloader
from bs4 import BeautifulSoup
import cv2
from moviepy.editor import VideoFileClip
import time
import base64

def download_image(url, folder_path, image_name):
    """Downloads an image from a URL and saves it to a specified folder."""
    try:
        # Create the folder if it doesn't exist
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        # Download the image
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful

        # Save the image to the specified folder
        image_path = os.path.join(folder_path, image_name)
        with open(image_path, 'wb') as file:
            file.write(response.content)
        
        print(f"Downloaded: {image_name}")
    except Exception as e:
        print(f"Error downloading image {image_name}: {e}")


def process_media(folder_path, seconds_per_frame=2):
    print("process media called")
    base64Frames = []   
    # Iterate over each file in the download folder
    for file_name in os.listdir(folder_path):
        print(f"file name: {file_name}")
        file_path = os.path.join(folder_path, file_name)
        # handling image
        if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            with open(file_path, "rb") as image_file:
                base64Frames.append(base64.b64encode(image_file.read()).decode("utf-8"))

        elif file_name.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
        
            base_file_path, _ = os.path.splitext(file_path)

            video = cv2.VideoCapture(file_path)
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
            audio_path = f"{base_file_path}.mp3"
            clip = VideoFileClip(file_path)
            clip.audio.write_audiofile(audio_path, bitrate="32k")
            clip.audio.close()
            clip.close()

            print(f"Extracted {len(base64Frames)} frames")
            print(f"Extracted audio to {audio_path}")

    try:
        media = {
            'frames': base64Frames,
            'audio_path': audio_path
        }
        return media
    except NameError or UnboundLocalError:
        media = {
            'frames': base64Frames,
            'audio_path': None
        }
        return media

def extract_instagram_post_info(url):
    """Extracts information from an Instagram post and downloads images using instaloader."""
    loader = instaloader.Instaloader(
        download_comments=False,
        download_geotags=True,
        download_pictures=True,
        download_video_thumbnails=True,
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
        folder_name = "download"
        loader.download_post(post, target=folder_name)
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
