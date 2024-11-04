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
img_url = "https://instagram.fjai14-1.fna.fbcdn.net/v/t51.29350-15/447344148_468137552438569_5416229813738446488_n.webp?stp=dst-jpg_e35&_nc_ht=instagram.fjai14-1.fna.fbcdn.net&_nc_cat=101&_nc_ohc=w9mTJa-Nrg0Q7kNvgGGTcqM&_nc_gid=7a33792191eb482fad74c22d4d307231&edm=ANTKIIoBAAAA&ccb=7-5&oh=00_AYBt7aAxYvlB0bPFusnIP_4PwYnGaFRoDoURYh_1bPVF1w&oe=672EF810&_nc_sid=d885a2"
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