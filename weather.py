import requests
import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime  
import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


# API Key and Base URL
API_KEY = "5d894bd74a30064c0ba6d40972c788fd"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# Function to fetch and display weather data
def fetch_weather():
    city = city_entry.get()
    if not city:
        messagebox.showerror("Input Error", "Please enter a city name.")
        return

    api_url = f"{BASE_URL}?q={city}&appid={API_KEY}&units=metric"
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Check for HTTP errors
        data = response.json()
        
        if response.status_code == 200:
            display_weather_info(data)
            city_entry.delete(0, ctk.END)  # Clear the input field after successful data retrieval
        else:
            messagebox.showerror("API Error", f"Unable to fetch data for {city}. HTTP Status Code: {response.status_code}")
    
    except requests.exceptions.HTTPError as http_error:
        messagebox.showerror("HTTP Error", f"HTTP error occurred: {http_error}")
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Request Error", f"An error occurred while fetching data: {e}")

# Function to assign emoji based on weather condition (using weather_id)
def assign_emoji_by_weatherID(weather_id):
    if 200 <= weather_id <= 232:
        return "⚡"  # Thunderstorm
    elif 300 <= weather_id <= 321:
        return "⛅"  # Drizzle
    elif 500 <= weather_id <= 531:
        return "🌧️"  # Rain
    elif 600 <= weather_id <= 622:
        return "❄️"  # Snow
    elif 701 <= weather_id <= 741:
        return "🌫️"  # Fog
    elif weather_id == 762:
        return "🌋"  # Volcanic ash
    elif weather_id == 771:
        return "💨"  # Wind
    elif weather_id == 781:
        return "🌪️"  # Tornado
    elif weather_id == 800:
        return "☀️"  # Clear sky
    elif 801 <= weather_id <= 804:
        return "☁️"  # Clouds
    else:
        return ""  # Unknown condition

def display_weather_info(data):
    # Extract necessary data
    city_name = data["name"]
    weather_id = data["weather"][0]["id"]
    weather_description = data["weather"][0]["description"]
    current_temperature = data["main"]["temp"]
    wind_speed = data["wind"]["speed"]
    humidity = data["main"]["humidity"]

    # Get the weather emoji based on the weather_id
    weather_icon = assign_emoji_by_weatherID(weather_id)

    # Get the current time and format it
    current_time = datetime.now().strftime("%Y.%m.%d  %H:%M:%S")

    # Update Labels with relevant information
    city_label.configure(text=f"🚩{city_name}", font=("Arial", 28, "bold"))
    time_label.configure(text=f"📅 {current_time}", font=("Comic Sans MS", 12))  
    temp_label.configure(text=f"Temperature: {current_temperature if current_temperature != 0 else 0:.1f}°C", font=("Comic Sans MS", 14))
    wind_label.configure(text=f"Wind Speed: {wind_speed} m/s", font=("Comic Sans MS", 14))
    humidity_label.configure(text=f"Humidity: {humidity}%", font=("Comic Sans MS", 14))
    description_label.configure(text=f"Condition: {weather_description.capitalize()} {weather_icon}", font=("Comic Sans MS", 16))

# Initialize CustomTkinter
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("dark-blue")

# Create the main application window
root = ctk.CTk()
root.title("Weather App")
root.geometry("500x500")
root.iconbitmap(resource_path("meteorology.ico"))
root.resizable(False, False)

# Input Section
frame_top = ctk.CTkFrame(root, corner_radius=10, width=400, height=60)
frame_top.pack(pady=20, padx=20)

city_entry = ctk.CTkEntry(frame_top, placeholder_text="Enter a city name...", width=280, font=("Arial", 14))
city_entry.pack(side="left", padx=(10, 5), pady=10)

fetch_button = ctk.CTkButton(frame_top, text="Get Weather", command=fetch_weather, width=100)
fetch_button.pack(side="left", padx=(5, 10))

# Display Section (Updated look with icons for conditions)
frame_display = ctk.CTkFrame(root, corner_radius=10, width=350, height=200)  
frame_display.pack(pady=20, padx=20, fill="both", expand=True)

city_label = ctk.CTkLabel(frame_display, text="", font=("Arial", 28, "bold"))
city_label.pack(pady=(20, 10))

time_label = ctk.CTkLabel(frame_display, text="", font=("Comic Sans MS", 12))
time_label.pack(pady=5)

temp_label = ctk.CTkLabel(frame_display, text="", font=("Comic Sans MS", 14))  
temp_label.pack(pady=5)

wind_label = ctk.CTkLabel(frame_display, text="", font=("Comic Sans MS", 14))  
wind_label.pack(pady=5)

humidity_label = ctk.CTkLabel(frame_display, text="", font=("Comic Sans MS", 14))  
humidity_label.pack(pady=5)

description_label = ctk.CTkLabel(frame_display, text="", font=("Comic Sans MS", 16))  
description_label.pack(pady=(20, 10))

# Footer Section
footer = ctk.CTkLabel(root, text="Weather App © 2025", font=("Arial", 10))
footer.pack(side="bottom", pady=10)

# Run the Application
root.mainloop()