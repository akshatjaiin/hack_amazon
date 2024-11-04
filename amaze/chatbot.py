from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()
client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)
prompt = "explain the image"
# Path to the image file you want to send
img_url = "https://scontent.cdninstagram.com/v/t51.29350-15/463824545_568189195783303_4805163012266105423_n.heic?stp=c288.0.864.864a_dst-jpg_s640x640&_nc_cat=1&ccb=1-7&_nc_sid=18de74&_nc_ohc=d5rPwtEH4eoQ7kNvgFevzgW&_nc_zt=23&_nc_ht=scontent.cdninstagram.com&_nc_gid=AAI4Hw2LAqoUKtY1x9rgMZq&oh=00_AYClM9BkC2n8csptSVM-T85i-vif74AvdmYS4kutM2UmRA&oe=672EDB31"
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