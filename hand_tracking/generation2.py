import openai
import pygame
import os
from gtts import gTTS

file1 = open("test.txt", "w")

from pydantic import BaseModel
import json
from openai import OpenAI
client = OpenAI(
    api_key= "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"
)

def generate_recipe(transcript):
    """
    Takes a transcript of a person's speech and generates a recipe that fits it.
    Saves the recipe to response.txt in the specified format.
    """
    # Define the prompt
    prompt = f"""
    Analyze the following transcript of a person speaking:
    \"\"\"{transcript}\"\"\"

    Based on the content, mood, and implied preferences of the speaker, 
    suggest the best recipe that suits the transcript. Keep the number of 
    ingredients under 8. Always keep the number of recipe steps above, 
    but make each step concise.
    SAY NOTHING EXCEPT THE LIST OF INGREDIENTS AND RECIPE STEPS, 
    NO ADDITIONAL COMMENTS SHALL BE TOLERATED.
    Format the recipe in this structure:

    **Ingredients**  
    - List ingredients with quantities in a clear and organized manner.  

    **Recipe**  
    1. Write steps concisely and clearly for making the dish.  
    
    Save only the recipe in the file.
    """

    # Call the OpenAI API
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a culinary expert and creative recipe developer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
    recipe = response.choices[0].message.content.strip()

    # Save to a file
    with open("response.txt", "w") as file:
        file.write(recipe)


def read_response_file(file_path):
    """
    Reads the content of the response file.
    """
    with open(file_path, "r") as file:
        return file.read()

def generate_tts(text, output_audio_file):
    """
    Generates TTS audio for the given text and saves it as an MP3 file.
    """
    # Use gTTS to convert text to speech
    tts = gTTS(text, lang="en")
    tts.save(output_audio_file)

def play_audio(audio_file):
    """
    Plays the given audio file using pygame.
    """
    pygame.mixer.init()
    pygame.mixer.music.load(audio_file)
    pygame.mixer.music.play()
    print("Playing audio...")

    while pygame.mixer.music.get_busy():  # Wait for the audio to finish
        continue

# Extract the recipe
