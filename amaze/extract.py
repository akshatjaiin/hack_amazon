from PIL import Image
import numpy as np
from dotenv import load_dotenv
import requests
import instaloader
from bs4 import BeautifulSoup
from moviepy.editor import VideoFileClip
import time
import base64
from .ais import audio_transcription
from io import BytesIO
import tempfile
import os

def extract_media_base64(image_urls:list[str],video_url:str|None):
    media_base64 = {}
    try:
        if video_url:
            media_base64 = get_video_base64(video_url,fps=1)
            media_base64["audio"] = audio_transcription(media_base64["audio"])
        media_base64["images"] = [get_image_base64(image) for image in image_urls if image!=None];
        print("media extraction done")
    except Exception as e:
        print(f"Error extracting Facebook post: {e}")
    finally:
        return media_base64;

def get_image_base64(url:str):
    try:
        res = requests.get(url);
        if res.status_code != 200:raise Exception("Failed to fetvh the image");
        img_base64 = base64.b64encode(res.content).decode("utf-8")
        return img_base64
    except Exception as e:
        print("Error: ",e);
        return None;
def download_video(url,video_folder):
    video_path:str = os.path.join(video_folder,"video.mp4")
    with requests.get(url, stream=True) as r:
        r.raise_for_status()  # Check for errors in fetching the video
        with open(video_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return video_path;

def get_video_base64(url:str,fps:int=10,output_folder="public"):
    print("Extracting video")
    if(url==""):raise Exception("Invelid video url");
    # read the video fromm the url
    video_path = download_video(url,output_folder)
    video = VideoFileClip(video_path)
    os.remove(video_path)
    audio_path = os.path.join(output_folder,"audio.wav")
    if not os.path.exists(output_folder):os.makedirs(frames_output_folder)
    video.audio.write_audiofile(audio_path);
    with open(audio_path,"rb") as saved_audio_file:
        audio_base64 = base64.b64encode(saved_audio_file.read()).decode('utf-8')

    print("Extracting video frames")
    video_frames_base64 = [];
    buffered = BytesIO();
    for frame_index,frame in enumerate(video.iter_frames(fps=min(video.fps,fps), dtype="uint8")):
        print("extracting the frame",frame_index);
        frame_img = Image.fromarray(frame);
        frame_img.save(buffered,format="PNG");
        video_frames_base64.append(base64.b64encode(buffered.getvalue()).decode('utf-8'))
        buffered.truncate(0)
        buffered.seek(0)
    del buffered
    video.reader.close()
    video.audio.close()
    del video
    os.remove(audio_path);
    print("Video extraction done")
    return {"video":video_frames_base64,"audio":audio_base64};

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
        post = instaloader.Post.from_shortcode(loader.context, shortcode);
        # Extracting post details
        post_info = {
            'platform': 'Instagram',
            'author': post.owner_username,
            'content': post.caption,  # Caption of the post
            'images': [node.display_url for node in post.get_sidecar_nodes()],  # Handle video posts
            'video':post.video_url
        };
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
