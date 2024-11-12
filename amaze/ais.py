from dotenv import load_dotenv
import os
from openai import OpenAI
import base64
from io import BytesIO
from . import constant

load_dotenv()
client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)

def ask_ai(images:list=[],video:list|None=None,content:str="",transcription=None):
    try:
        prompt = constant.prompt
        messages = [
            {"role": "system", "content":constant.prompt+"i m feeding you few post related content " + content},
            {"role": "user", "content": [
                ]
            }
        ];
        if len(images)>0:
            for image in images:
                messages[1]["content"].append({"type": "image_url", "image_url": {"url": f'data:image/jpg;base64,{image}', "detail": "low"}});
        if video!=None:
            for frame in video:
                messages[1]["content"].append({"type": "image_url", "image_url": {"url": f'data:image/jpg;base64,{frame}', "detail": "low"}});

        if transcription!=None:
            messages[1]["content"].append({"type": "text", "text": f"The audio transcription is: {transcription.text}"});

        ## Generate a summary with visual and audio
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0,
        )
        return response
    except Exception as error:
        print("Error, while ai response:",error)
        return None

def audio_transcription(audio_base64:list):
    print("transcripting the audio")
    audio_data = base64.b64decode(audio_base64)
    # Convert the byte data into a file-like object using BytesIO
    audio_file = BytesIO(audio_data)
    audio_file.name = "audio.wav"  # Set a name to simulate a real file (optional but helps with clarity)

    transcriptions = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file,
    )
    print(transcriptions)
    audio_file.truncate(0)
    audio_file.seek(0)
    del audio_file
    return transcriptions;
