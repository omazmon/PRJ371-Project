import subprocess
import tkinter as tk
from tkinter import ttk, messagebox
import pyodbc
import requests

# Create a Tkinter window
root = tk.Tk()
root.title("Agri~Drone")

# Set the window size to fullscreen
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
BUTTON_COLOR = "#4CAF50"
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


# Create a farm name label and combobox


def open_dronedata():
    selected_province = location_combobox.get()
    farm_name = farm_name_combobox.get()  # Get the farm name from the combobox
    selected_crop = crop_combobox.get()  # Get the selected crop type
    if selected_province != "Please select province" and farm_name and selected_crop:

        api_key = '06e1969da55a4b51d0b4447dcd9c92eb'
        weather_api_url = f'http://api.openweathermap.org/data/2.5/weather?q={selected_province}&appid={api_key}&units=metric'
        response = requests.get(weather_api_url)
        if response.status_code == 200:
            weather_data = response.json()
            temperature = weather_data['main']['temp']
            humidity = weather_data['main']['humidity']
            description = weather_data['weather'][0]['description']
            return f"Temperature: {temperature}°C, Humidity: {humidity}%, Description: {description}"
        else:
            return "Failed to fetch weather data"
    else:
        messagebox.showerror("Error", "Please select a province, enter a farm name, and select a crop type.")


# Function to display weather forecast
def display_weather_forecast():
    weather_forecast = open_dronedata()
    messagebox.showinfo("Weather Forecast", weather_forecast)


def close_application():
    subprocess.Popen(["python", "Assesment.py"])
    root.destroy()


# Create a list of provinces in South Africa
provinces = ["Please select province", "Eastern Cape", "Free State", "Gauteng", "KwaZulu-Natal", "Limpopo",
             "Mpumalanga", "North West", "Northern Cape", "Western Cape"]

# Create a list of top 5 farming crops in South Africa
top_crops = ["Maize", "Sugarcane", "Wheat", "Sunflower", "Citrus"]
# Create a welcome label
welcome_label = ttk.Label(root, text="Welcome to AgriDrone", font=("Times New Roman", 14, "bold"))
welcome_label.pack()

farm_name_label = ttk.Label(root, text="Farm Name:")
farm_name_label.pack()
farm_name_combobox = ttk.Combobox(root, values=farm_names_list, state="readonly")
farm_name_combobox.set("Select Farm Name")
farm_name_combobox.pack()
# Create a location dropdown (combobox)
location_label = ttk.Label(root, text="Location")
location_combobox = ttk.Combobox(root, values=provinces, state="readonly")
location_combobox.set("Please select province")
location_label.pack()
location_combobox.pack()

# Create a crop type dropdown (combobox)
crop_label = ttk.Label(root, text="Crop Type")
crop_combobox = ttk.Combobox(root, values=top_crops, state="readonly")
crop_combobox.set("Select Crop Type")
crop_label.pack()
crop_combobox.pack()

crop_assessment_button = ttk.Button(root, text="Start Drone", command=close_application)
crop_assessment_button.pack()
# Create a button to fetch and display weather forecast
weather_button = ttk.Button(root, text="Check Weather Forecast", command=display_weather_forecast)
weather_button.pack()
copyright_label = ttk.Label(root, text="Copy Right Reserved @ Agri~Drone 2023",
                            font=("Times New Roman", 14, "bold italic"))
# Start the GUI main loop
root.mainloop()
