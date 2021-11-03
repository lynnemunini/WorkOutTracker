import requests
import os
from tkinter import *
from datetime import datetime
window = Tk()
window.geometry("500x600")
window.title("WorkOut Tracker")
window.config(bg="white")
do = None
# Add workout function


def add_workout():
    global do
    do = today_workout.get("1.0", END)
    window.destroy()


canvas = Canvas(width=256, height=256, bg="white", highlightthickness=0)
logo = PhotoImage(file="meditation.png")
canvas.create_image(128, 128, image=logo)
canvas.grid(column=0, row=0, pady=30)


do_label = Label(text="\nHey Lynne, what did you do today?\n", font=("courier", 13, "normal"))
do_label.grid(column=0, row=2,  padx=100)
do_label.config(bg="white")
today_workout = Text(bg="#F8F7DE", borderwidth=0, highlightthickness=0, width=48, height=4, insertbackground="#39A2DB",
                     selectbackground="#FFEAC9", fg="black")
today_workout.grid(column=0, row=3, columnspan=2, pady=5)

add_image = PhotoImage(file="plus.png")
add_image_button = Button(image=add_image, bg="white", highlightthickness=0, border=0, command=add_workout)
add_image_button.grid(column=0, row=4, pady=30)
window.mainloop()
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
