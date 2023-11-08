import subprocess
import time
import tkinter as tk
from datetime import datetime
from tkinter import ttk, messagebox
import pyodbc
import requests
import webbrowser
from PIL import Image, ImageTk

# Create a Tkinter window
root = tk.Tk()
root.title("Agri~Drone")
LABEL_COLOR = "#333333"
BUTTON_COLOR = "#D2B48C"
BG_COLOR = "#D2B48C"
FONT_STYLE = ("Arial ", 16)
TEXT_COLOR = "#000000"
# Replace with your own Power BI report URL and embed token
report_url = "https://app.powerbi.com/groups/me/reports/5d657c9d-0c5f-45d1-866c-f5fcfa233402/ReportSection?experience=power-bi"
ico_image1 = Image.open("drone_icon_191447.ico")
photo = ImageTk.PhotoImage(ico_image1)
ico_image2 = Image.open("data_icon_154537.ico")
photo1 = ImageTk.PhotoImage(ico_image2)
ico_image3 = Image.open("Weather_31085.ico")
photo2 = ImageTk.PhotoImage(ico_image3)
warning_message = """
Please Note:
- Enter accurate data for the most optimal assessment.
- Use the application responsibly and follow ethical guidelines.
"""
# Set the window size to fullscreen
root.geometry("450x400")
root.config(bg=BG_COLOR)

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
                messagebox.showwarning("Drone Connection",
                                       "Please Change your wifi connection! Connect to Drone Wifi e.g.'Tello-ABC123' ")
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
    time.sleep(5)
    root.destroy()


def open_powerbi():
    # Open the Power BI report in a new window or tab
    webbrowser.open(report_url)


top_crops = ["Maize", "Sugarcane", "Wheat", "Sunflower", "Citrus"]
# Create a welcome label
welcome_label = ttk.Label(root, text="Welcome to AgriDrone", font=("Times New Roman", 18, "bold"), background=BG_COLOR,
                          foreground=TEXT_COLOR)
welcome_label.pack()

# Create a label to display the current date and time
date_time_label = ttk.Label(root, text="", font=FONT_STYLE, background=BG_COLOR, foreground=TEXT_COLOR)
date_time_label.pack()

farm_name_label = ttk.Label(root, text="Farm Name:", font=FONT_STYLE, background=BG_COLOR, foreground=TEXT_COLOR)
farm_name_label.pack()
farm_name_combobox = ttk.Combobox(root, values=farm_names_list, state="readonly")
farm_name_combobox.set("Select Farm Name")
farm_name_combobox.pack(padx=10)

city_label = ttk.Label(root, text="City", font=FONT_STYLE, background=BG_COLOR, foreground=TEXT_COLOR)
city_combobox = ttk.Combobox(root, values=cities, state="readonly")
city_combobox.set("Please select city")
city_label.pack()
city_combobox.pack(padx=10)
# Create a crop type dropdown (combobox)
crop_label = ttk.Label(root, text="Crop Type", font=FONT_STYLE, background=BG_COLOR, foreground=TEXT_COLOR)
crop_combobox = ttk.Combobox(root, values=top_crops, state="readonly")
crop_combobox.set("Select Crop Type")
crop_label.pack()
crop_combobox.pack(padx=10)

logout_button = tk.Button(root, text="LogOut", command=root.destroy, background="#D3D3D3", font=FONT_STYLE)
logout_button.pack(pady=5, padx=20)

copyright_label = ttk.Label(root, text="Copyright Reserved @ Agri~Drone 2023",
                            font=("Times New Roman", 14, "bold italic"), background=BG_COLOR, foreground=TEXT_COLOR)
copyright_label.pack()
# Create a button to fetch and display weather forecast
weather_button = tk.Button(root, image=photo2, text="Check Weather Forecast", command=display_weather_forecast,
                           background="#D2B48C",
                           font=FONT_STYLE)
weather_button.pack(side=tk.LEFT, pady=5, padx=20)

data_button = tk.Button(root, image=photo1, text="Data Insights", command=open_powerbi, background="#D2B48C",
                        font=FONT_STYLE)
data_button.pack(side=tk.LEFT, pady=5, padx=20)

crop_assessment_button = tk.Button(root, image=photo, text="Start Drone", command=close_application, state="disabled",
                                   background=BUTTON_COLOR, font=FONT_STYLE)
crop_assessment_button.pack(side=tk.LEFT, pady=5, padx=20)

# Start the GUI main loop
update_date_time()
show_warning()
root.mainloop()
