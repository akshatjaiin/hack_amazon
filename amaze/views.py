from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import  render, get_object_or_404

import os
from . import  extract,ais
from .amazon_product_search import amazon_product_search
import json
def index(request):
    if request.method == "POST":
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
        response=ais.ask_ai(media["images"],media.get("video",None),post_info["content"],media.get("audio",None));
        queries = json.loads(response.choices[0].message.content.replace("```","").replace("json","").replace("\n",""))
        print("queries:",queries)
        amazon_search_results:list = [];
        if type(queries)==list:
            for query in queries:
                amazon_search_results.extend(amazon_product_search(query["query"])[:5]);
        else:
            amazon_search_results.extend(amazon_product_search(queries["query"])[:5]);


        return render(request, "amaze/index.html", {
            'images': post_info.get('images',None),
            'video':post_info.get('video'),
            'ai_res': response.choices[0].message.content,
            'heading': "Extracted Post Information:",  # Use quotes around keys
            'Platform': post_info['platform'],  # Remove curly braces and quotes
            'Author': post_info['author'],
            'Content': post_info['content'],
            'products':amazon_search_results
        })

    return render(request, "amaze/index.html")  # Handle GET request

def new(request):
    return render(request, "amaze/new.html")
