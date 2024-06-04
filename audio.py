import requests

def generate_audio(text, filename, api_key):

    url = "https://api.elevenlabs.io/v1/text-to-speech/29vD33N1CtxCmqQRPOHJ"

    payload = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5
        }
    }
    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json",
        "Accept": "audio/mpeg"
    }
    
    response = requests.request("POST", url, json=payload, headers=headers)
    
    with open('audio/' + filename, 'wb') as f:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                
    print(response)
    
def split_whisper(arr): # Take an array of whisper transcrptions and splits each into 2 transcrptions
    new_arr = []
    for i in arr:
        # Calculate sentances
        sentance = i[0]
        sentance = sentance.split()
        split_index = int(len(sentance) / 2)
        first_part = sentance[:split_index]
        last_part = sentance[split_index:]
        
        # Calculate timestamps
        offset = (i[2] - i[1]) / 2
        first_timestamp_s = i[1]
        first_timestamp_e = i[1] + offset
        last_timestamp_s = i[1] + offset
        last_timestamp_e = i[2]
        
        # Append new sentances
        empty = " "
        new_arr.append([empty.join(first_part), round(first_timestamp_s, 3), round(first_timestamp_e, 3)])
        new_arr.append([empty.join(last_part), round(last_timestamp_s, 3), round(last_timestamp_e, 3)])
    return new_arr