from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
import json
import re
import random_responses

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Load JSON data
def load_json(file):
    with open(file) as bot_responses:
        print(f"Loaded '{file}' successfully!")
        return json.load(bot_responses)

# Store JSON data
response_data = load_json("bot.json")

def get_response(input_string):
    split_message = re.split(r'\s+|[,;?!.-]\s*', input_string.lower())
    score_list = []

    # Check all the responses
    for response in response_data:
        response_score = 0
        required_score = 0
        required_words = response["required_words"]

        # Check if there are any required words
        if required_words:
            for word in split_message:
                if word in required_words:
                    required_score += 1

        # Amount of required words should match the required score
        if required_score == len(required_words):
            for word in split_message:
                if word in response["user_input"]:
                    response_score += 1

        score_list.append(response_score)

    best_response = max(score_list)
    response_index = score_list.index(best_response)

    if input_string == "":
        return "Please type something so we can chat :("

    if best_response != 0:
        return response_data[response_index]["bot_response"]

    return random_responses.random_string()

@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/process_input")
async def process_input(request: Request):
    data = await request.json()
    user_input = data.get("user_input")
    response = get_response(user_input)
    return {"message": response}
