import requests
import os
from requests.auth import HTTPBasicAuth
from datetime import datetime

USERNAME = os.environ["ENV_SHEETY_USERNAME"]
PASSWORD = os.environ["ENV_SHEETY_PASSWORD"]

APP_ID = os.environ["ENV_NIX_APP_ID"]
APP_KEY = os.environ["ENV_NIX_API_KEY"]


EXERCISE_API_ENDPOINT = "https://trackapi.nutritionix.com/v2/natural/exercise"
SHEETY_API_ENDPOINT = os.environ["ENV_SHEETY_ENDPOINT"]

headers = {
    "x-app-id":APP_ID,
    "x-app-key":APP_KEY
}

exercise_params = {
    "query":input("Tell me which exercise you did: "),
    "gender":"male",
    "weight_kg":80,
    "height_cm":191,
    "age":20
}

exercise_data = requests.post(url=EXERCISE_API_ENDPOINT, json=exercise_params, headers=headers)
exercise_data = exercise_data.json()

today_date = datetime.now().strftime("%d/%m/%Y")
now_time = datetime.now().strftime("%X")

for exercise in exercise_data["exercises"]:
    sheet_inputs = {
        "workout": {
            "date": today_date,
            "time": now_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }
    sheet_response = requests.post(url=SHEETY_API_ENDPOINT, json=sheet_inputs, auth=HTTPBasicAuth(USERNAME, PASSWORD))
    print(sheet_response.text)

