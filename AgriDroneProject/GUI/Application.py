import time
from datetime import datetime
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox
import pyodbc
import requests
from PIL import Image, ImageTk
import random
from nltk.chat.util import Chat, reflections

# Define patterns and responses for the chatbot
patterns = [
    (r'(.*)agricultural drone(.*)',
     [
         "Agricultural drones are used in farming to monitor crop health, optimize irrigation, and assess crop yield. They use various sensors and cameras to collect data."]),
    (r'(.*)work(.*)drone(.*)',
     [
         "Agricultural drones work by flying over farmland and capturing data using sensors and cameras. This data is then used by farmers to make informed decisions about their crops."]),
    (r'(.*)benefits(.*)agricultural drone(.*)',
     [
         "The benefits of agricultural drones include increased efficiency, better crop management, reduced costs, and improved yields due to data-driven decision-making."]),
    (r'(.*)sensors(.*)agricultural drone(.*)',
     [
         "Agricultural drones are equipped with various sensors such as multispectral cameras, thermal cameras, and LiDAR sensors. These sensors help in capturing different types of data related to crops."]),
    (r'(.*)future(.*)agricultural drone(.*)',
     [
         "The future of agricultural drones looks promising, with advancements in AI and machine learning. Drones will continue to play a vital role in precision agriculture and sustainable farming practices."]),
    (r'(.*)thank you(.*)',
     ["You're welcome! If you have more questions, feel free to ask."]),
]

# Create a chatbot using the patterns and reflections
chatbot = Chat(patterns, reflections)


# Function to start the chatbot when the checkbox is checked
def start_chat():
    if checkbox_var.get() == 1:
        get_response()
    else:
        messagebox.showinfo("Error", "Please check the checkbox to start the chatbot.")


# Create a Tkinter window
root = tk.Tk()
root.title("Agri~Drone")
warning_message = """
Please Note:
- Enter accurate data for the most optimal assessment.
- Use the application responsibly and follow ethical guidelines.
"""
# Set the window size to fullscreen
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
BUTTON_COLOR = "#4CAF50"
# Load the background image
background_image = Image.open("background-image.jpg")
background_photo = ImageTk.PhotoImage(background_image)
background_label = tk.Label(root, image=background_photo)
background_label.place(relwidth=1, relheight=1)

# Create a connection to the database
conn_str = "DRIVER={SQL Server};SERVER=Mthokozisi-2\SQLEXPRESS;DATABASE=AgriDrone;Trusted_Connection=yes;"
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()
# Execute the query to fetch farm names
farm_names_query = "SELECT FarmName FROM farm"
cursor.execute(farm_names_query)
# Fetch all the farm names
farm_names = cursor.fetchall()
# Extract farm names from the result and convert them to a list
farm_names_list = [row[0] for row in farm_names]
cities = [
    "Please select city",
    "Johannesburg",
    "Cape Town",
    "Durban",
    "Pretoria",
    "Port Elizabeth",
    "Bloemfontein",
    "East London",
    "Polokwane",
    "Nelspruit",
    "Pietermaritzburg",
    "Kimberley",
    "Rustenburg",
    "Mahikeng",
    "Middelburg",
    "Vryheid",
    "Witbank",
    "Grahamstown",
    "Stellenbosch",
    "Paarl",
    "Franschhoek",
    "George",
    "Upington",
    "Springbok",
    "Vredendal",
    "Thohoyandou",
    "Musina",
    "Mafikeng",
    "Richards Bay",
    "Welkom",
    # Add more South African cities as needed
]


def show_warning():
    messagebox.showwarning("Warning", warning_message)


def open_dronedata():
    selected_city = city_combobox.get()
    farm_name = farm_name_combobox.get()
    selected_crop = crop_combobox.get()
    if selected_city != "Please select city" and farm_name and selected_crop:
        api_key = '06e1969da55a4b51d0b4447dcd9c92eb'
        weather_api_url = f'http://api.openweathermap.org/data/2.5/weather?q={selected_city},ZA&appid={api_key}&units=metric'
        response = requests.get(weather_api_url)
        if response.status_code == 200:
            weather_data = response.json()
            temperature = weather_data['main']['temp']
            humidity = weather_data['main']['humidity']
            wind_speed = weather_data['wind']['speed']
            description = weather_data['weather'][0]['description']

            def predict_pest_outbreak(temperature):
                if 20 <= temperature <= 30:
                    return "Low risk of pest and disease outbreak."
                elif 30 < temperature <= 35:
                    return "Moderate risk of pest and disease outbreak. Monitor the crops closely."
                elif temperature > 35:
                    return "High risk of pest and disease outbreak. Take immediate action to prevent damage. Consider the following:\n" \
                           "- Increase irrigation to keep plants hydrated.\n" \
                           "- Apply appropriate pesticides or natural remedies recommended for the specific pests in your area.\n" \
                           "- Remove and destroy affected plants to prevent the spread of diseases.\n" \
                           "- Seek advice from local agricultural experts or extension services for specific recommendations."

                else:
                    return "Temperature too low for significant pest and disease activity."

            pest_outbreak_prediction = predict_pest_outbreak(temperature)
            messagebox.showinfo("Pest and Disease Prediction", pest_outbreak_prediction)
            if 'rain' in description.lower() or 'drizzle' in description.lower() or 'shower' in description.lower():
                messagebox.showwarning("Weather Warning", "It's raining! Drone operation is not allowed.")
                return f"Temperature: {temperature}°C, Humidity: {humidity}%, Wind Speed: {wind_speed} m/s\nIt's raining can not operate the drone in these conditions!"
            elif wind_speed > 13:
                messagebox.showwarning("Caution",
                                       f"Wind speed is {wind_speed} m/s. Exercise caution while operating the drone.")
                crop_assessment_button.config(state="normal")  # Enable the button despite caution
                return f"Temperature: {temperature}°C, Humidity: {humidity}%, Wind Speed: {wind_speed} m/s\nExercise caution."
            else:
                crop_assessment_button.config(
                    state="normal")  # Enable the button if it's not raining and wind speed is safe
                return f"Temperature: {temperature}°C, Humidity: {humidity}%, Wind Speed: {wind_speed} m/s\nThe drone is safe to operate."
        else:
            return "Failed to fetch weather data"
    else:
        messagebox.showerror("Error", "Please select a city, enter a farm name, and select a crop type.")


# Function to display weather forecast
def display_weather_forecast():
    weather_forecast = open_dronedata()
    messagebox.showinfo("Weather Forecast", weather_forecast)


def update_date_time():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    date_time_label.config(text=f"{current_time}")
    root.after(1000, update_date_time)


def close_application():
    subprocess.Popen(["python", "Assesment.py"])
    time.sleep(7)
    root.destroy()


# Function to handle user input and get chatbot response
def get_response():
    if checkbox_var.get() == 1:
        user_input = input_box.get()
        response = chatbot.respond(user_input)
        messagebox.showinfo("Chatbot Response", random.choice(response))
    else:
        messagebox.showinfo("Error", "Please check the checkbox to start the chatbot.")


# Create a list of provinces in South Africa
provinces = ["Please select province", "Eastern Cape", "Free State", "Gauteng", "KwaZulu-Natal", "Limpopo",
             "Mpumalanga", "North West", "Northern Cape", "Western Cape"]

top_crops = ["Maize", "Sugarcane", "Wheat", "Sunflower", "Citrus"]
# Create a welcome label
welcome_label = ttk.Label(root, text="Welcome to AgriDrone", font=("Times New Roman", 18, "bold"))
welcome_label.pack()

# Create a label to display the current date and time
date_time_label = ttk.Label(root, text="")
date_time_label.pack()

farm_name_label = ttk.Label(root, text="Farm Name:")
farm_name_label.pack()
farm_name_combobox = ttk.Combobox(root, values=farm_names_list, state="readonly")
farm_name_combobox.set("Select Farm Name")
farm_name_combobox.pack()
# Create a location dropdown (combobox)
location_label = ttk.Label(root, text="Province")
location_combobox = ttk.Combobox(root, values=provinces, state="readonly")
location_combobox.set("Please select province")
location_label.pack()
location_combobox.pack()

city_label = ttk.Label(root, text="City")
city_combobox = ttk.Combobox(root, values=cities, state="readonly")
city_combobox.set("Please select city")
city_label.pack()
city_combobox.pack()
# Create a crop type dropdown (combobox)
crop_label = ttk.Label(root, text="Crop Type")
crop_combobox = ttk.Combobox(root, values=top_crops, state="readonly")
crop_combobox.set("Select Crop Type")
crop_label.pack()
crop_combobox.pack()

# Create a button to fetch and display weather forecast
weather_button = ttk.Button(root, text="Check Weather Forecast", command=display_weather_forecast)
weather_button.pack()

crop_assessment_button = ttk.Button(root, text="Start Drone", command=close_application, state="disabled")
crop_assessment_button.pack()

checkbox_var = tk.IntVar()
checkbox = tk.Checkbutton(root, text="Start Chatbot", variable=checkbox_var)
checkbox.pack()

input_box = tk.Entry(root, width=50)
input_box.pack(pady=20)

# Bind the Enter key to get_response function
input_box.bind("<Return>", lambda event=None: get_response())

copyright_label = ttk.Label(root, text="Copy Right Reserved @ Agri~Drone 2023",
                            font=("Times New Roman", 14, "bold italic"))
copyright_label.pack()
# Start the GUI main loop
update_date_time()
show_warning()
root.mainloop()
