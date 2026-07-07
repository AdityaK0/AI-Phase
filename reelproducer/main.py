import json
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types
from tmdb import search_movie, download_poster

load_dotenv()

client = genai.Client(api_key=os.getenv("API_KEY"))


SYSTEM_PROMPT = """
...

Schema:

{
    "title":"",
    "hook":"",
    "script":"",

    "movies":[
        {
            "rank":5,
            "title":"",
            "worldwide_box_office_inr_crore":0,
            "year":0
        }
    ],

    "hashtags":[],
    "captions":[]
}

Rules:

- Return exactly 5 movies.
- Use official worldwide box office collections.
- Use integer values in INR crore.
- Sort from rank 5 to rank 1.
- Movie titles must be official.
- Return JSON only.
"""
celebrity = input("Celebrity: ")

response = client.models.generate_content(
    model="gemini-2.5-flash",
    config=types.GenerateContentConfig(
        system_instruction=SYSTEM_PROMPT,
        temperature=0.8,
        response_mime_type="application/json",
    ),
    contents=f"""
    Create an Instagram Reel about the Top 5 Highest Grossing Movies of {celebrity}.

    Return the movie list ordered from rank 5 to rank 1.
    """,
)

data = json.loads(response.text)
print(json.dumps(data, indent=4))

os.makedirs("output", exist_ok=True)

with open("output/metadata.json", "w") as f:
    json.dump(data, f, indent=4)

with open("output/script.txt", "w") as f:
    f.write(data["script"])

with open("output/captions.srt", "w") as f:

    for i, caption in enumerate(data["captions"], start=1):

        start = caption["start"] + ":00"
        end = caption["end"] + ":00"

        f.write(f"{i}\n")
        f.write(f"{start.replace('.',',')} --> {end.replace('.',',')}\n")
        f.write(caption["text"] + "\n\n")

print("Files generated successfully!")


for movie in data["movies"]:

    result = search_movie(movie["title"])

    if result:
        download_poster(result)