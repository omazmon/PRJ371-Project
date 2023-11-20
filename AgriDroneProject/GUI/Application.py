import subprocess
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import PhotoImage
from PIL import Image, ImageTk
import pyodbc
import requests

# Create a Tkinter window
root = tk.Tk()
root.title("Agri~Drone")

# Set the window size to fullscreen
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
root.configure(bg="#008080")  # Use the color code for green
BUTTON_COLOR = "#4CAF50"



# Define the button color, font style, and border width
BUTTON_COLOR = "#4CAF50"  # Darker green
FONT_STYLE = "Arial 12"
BUTTON_BORDER_WIDTH = 1

# Load your start icon image
start_icon = PhotoImage(file="C:/Users/mo/Downloads/play.png")  # Replace with your icon's file path
start_icon_resized= start_icon.subsample(16,16)

weather_icon= PhotoImage(file="C:/Users/mo/Downloads/cloudy.png")
weather_icon_resized= weather_icon.subsample(16,16)
# Create a connection to the database
conn_str ="DRIVER={SQL Server};SERVER=LAPTOP-CPS3S6O0\SQLEXPRESS;DATABASE=AgriDrone;Trusted_Connection=yes;"



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
welcome_label = tk.Label(root, text="Welcome to AgriDrone", font=("Arial", 18, "bold"), bg="white", bd=1, relief="solid", fg="#008080")
welcome_label.pack(fill="x")  # Set the label to fill the x-axis

farm_name_label = ttk.Label(root, text="Farm Name:")
farm_name_label.pack()
farm_name_combobox = ttk.Combobox(root, values=farm_names_list, state="readonly", font=FONT_STYLE)
farm_name_combobox.pack(padx=30, pady=20)
farm_name_combobox.set("Select farm name")

# Create a location dropdown (combobox)
location_label = ttk.Label(root, text="Location")
location_label.pack()
location_combobox = ttk.Combobox(root, values=provinces, state="readonly", font=FONT_STYLE)
location_combobox.pack(padx=30, pady=20)
location_combobox.set("Please select province")



# Create a crop type dropdown (combobox)
crop_label = ttk.Label(root, text="Crop Type")
crop_combobox = ttk.Combobox(root, values=top_crops, state="readonly", font=FONT_STYLE)
crop_combobox.set("Select Crop Type")
crop_label.pack()
crop_combobox.pack(padx=30, pady=20)


crop_assessment_button = tk.Button(root, text="Start Drone", command=close_application, bg=BUTTON_COLOR, font=FONT_STYLE, borderwidth=BUTTON_BORDER_WIDTH,image=start_icon_resized, compound=tk.LEFT)
crop_assessment_button.pack(pady=20, side="top", anchor="n")
# Create a button to fetch and display weather forecast
weather_button = tk.Button(root, text="Check Weather Forecast", command=display_weather_forecast, bg=BUTTON_COLOR, font=FONT_STYLE, borderwidth=BUTTON_BORDER_WIDTH,image=weather_icon_resized, compound=tk.LEFT)
weather_button.pack(pady=20, side="top", anchor="n")
copyright_label = ttk.Label(root, text="Copy Right Reserved @ Agri~Drone 2023",
                            font=("Times New Roman", 14, "bold italic"))



# Start the GUI main loop
root.mainloop()


