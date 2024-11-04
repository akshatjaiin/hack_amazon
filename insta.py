import instaloader
from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)
prompt = "explain the image"

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

# Example usage:
url = 'https://www.instagram.com/p/DBS3usJNsMx/?img_index=1'
post_info = extract_instagram_post_info(url)
print(post_info['images'])

# Path to the image file you want to send
img_url = post_info['images']
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {
                    "type": "image_url",
                    "image_url": {"url": f"{img_url}"},
                },
            ],
        }
    ],
)
print(response)