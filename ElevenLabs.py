import os
from dotenv import load_dotenv

load_dotenv()

from elevenlabs import play
from elevenlabs.client import ElevenLabs


client = ElevenLabs(
  api_key= os.environ.get("ELEVENLABS_API_KEY")
)

audio = client.generate(
  text="SKRA MOTHERFUCKER",
  voice="Adam",
  model="eleven_multilingual_v2"
# audio = client.text_to_sound_effects.convert(
#     text= input(""),
#     duration_seconds=1.0,
#     prompt_influence=1.0,
)
play(audio)