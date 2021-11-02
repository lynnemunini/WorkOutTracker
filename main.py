import requests
import os
from datetime import datetime
today = datetime.now()
date = today.strftime("%d/%m/%y")
now_time = today.time()
time = now_time.strftime("%H:%M:%S")
nutritionix_id = os.environ["APP_ID"]
apikey = os.environ["API_KEY"]
nutritionix_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
sheety_endpoint = os.environ["SHEETY_ENDPOINT"]
token = os.environ["TOKEN"]
headers = {
    "x-app-id": nutritionix_id,
    "x-app-key": apikey,

}
do = input("Hey Lynne, what did you do today? ")

nutritionix_config = {
     "query": do,
     "gender": "female",
     "weight_kg": 50.5,
     "height_cm": 163,
     "age": 20
    }
response = requests.post(url=nutritionix_endpoint, json=nutritionix_config, headers=headers)
result = response.json()
print(result)

authorization_header = {

    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"

}

for exercise in result["exercises"]:
    sheety_params = {
        "workout": {
            "date": date,
            "time": time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }
    new_response = requests.post(url=sheety_endpoint, json=sheety_params, headers=authorization_header)

    print(new_response.text)
