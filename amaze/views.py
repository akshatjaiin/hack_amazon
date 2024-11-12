from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import  render, get_object_or_404

import os
from . import  extract,ais
from .amazon_product_search import amazon_product_search
import json
import base64
from PIL import Image
from io import BytesIO

def is_valid_base64_image(data_url):
    try:
        # Check if the URL starts with the required prefix
        if not data_url.startswith("data:image/"):
            return False
        
        # Extract base64 string (remove the "data:image/type;base64," part)
        base64_data = data_url.split(",")[1]
        
        # Decode the base64 string
        image_data = base64.b64decode(base64_data)
        
        # Check if it can be opened as an image
        image = Image.open(BytesIO(image_data))
        image.verify()  # Verify that it's a valid image
        return True
    except Exception as e:
        # Handle exceptions which indicate invalid base64 or image data
        print("Invalid base64 image:", e)
        return False

def index(request):
    if request.method == "POST":
        try:
            print("Post Request receive")
            post_url = request.POST.get("post_url")  # Use request.POST to get the URL
            post_info = {}
            post_info = extract.extract_post_info(post_url)
            media = extract.extract_media_base64(post_info.get('images',[]),post_info.get('video',None));

            # Define default values for None objects
            default_values = {
                'content': "No Post Description Found",
                'images': "No Images Found",
                'platform': "Unknown",
                'author': "Unknown"
            }
            print("asking the ai ...")
            response=ais.ask_ai(media["images"],media.get("video",None),post_info["content"],media.get("audio",None));
            if response==None:raise Exception("Error in ai response")
            queries = json.loads(response.choices[0].message.content.replace("```","").replace("json","").replace("\n",""))
            print("queries:",queries)
            print("Searchingbon amazon ...")
            amazon_search_results:list = [];
            if type(queries)==list:
                for query in queries:
                    amazon_search_results.extend(amazon_product_search(query["query"])[:5]);
            else:
                amazon_search_results.extend(amazon_product_search(queries["query"])[:5]);


            return render(request, "amaze/index.html", {
                'images': post_info.get('images',None),
                'video':post_info.get('video'),
                # 'ai_res': response.choices[0].message.content,
                'heading': "Extracted Post Information:",  # Use quotes around keys
                'Platform': post_info['platform'],  # Remove curly braces and quotes
                'Author': post_info['author'],
                'Content': post_info['content'],
                # 'products':amazon_search_results
            })
        except Exception as e:
            return render(request, "amaze/index.html", {'message': e})
    return render(request, "amaze/index.html")  # Handle GET request

def new(request):
    return render(request, "amaze/new.html")

def custom_error(request, exception=None, status_code=404):
   print("custom error get called ?")
   url = f'http://http.cat/{status_code}'
   return render(request, "amaze/error.html", {
        'content': url,
    })
