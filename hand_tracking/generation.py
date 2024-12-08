
file1 = open("test.txt", "w")

from pydantic import BaseModel
import json
from openai import OpenAI
client = OpenAI(
    api_key= "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"
)



def piga(mode, modeType=None):


    match mode:
        case 1:
            modeType = "Generate 1 SINGLE SPORT ACTIVITY, ONE TIME, ONLY ONCE, that can be done indoors, like dancing or doing body-weight exercises"
        case 2:
            modeType = "Generate 1 SINGLE ACTIVITY, ONE TIME, ONLY ONCE one simple and tasy recipe that can be prepared by a normal person in their home. Start the Lists of ingredients with the caption 'ingredients' and the list of recipe steps with caption 'recipe'"
        case 3:
            modeType = "Generate 1 single freaky and silly card game that can be played alone or with friends"
        case 4:
            modeType = "Generate a youtube link to a video of JamilaCuisine, based on recipe description provided as input:"




    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a perfect machine made to generate A SPECIFIED WELL BEING ACTIVITY"},
            {
                "role": "system",
                "content": f"{modeType}",

            }
        ]
    )
    response = completion.choices[0].message.content

    with open ("response.txt", "w") as file:
        file.write(response)


piga(2)