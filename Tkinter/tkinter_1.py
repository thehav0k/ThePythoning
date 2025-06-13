## Weather Displayer (City) widget using Tkinter

import tkinter as tk
from tkinter import ttk # themed widgets
import requests
import os
from dotenv import load_dotenv

# Colors and fonts
# this part was hard in macOS
BG_COLOR = "#1e1e2f"
BTN_COLOR = "#2563eb"
BTN_HOVER_COLOR = "#1e40af"
BTN_TEXT_COLOR = "#ffffff"
TEXT_COLOR = "#e5e7eb"
ENTRY_BG = "#2d2d3c"
ENTRY_FG = "#ffffff"

FONT = ("Segoe UI", 12)
TITLE_FONT = ("Segoe UI", 14, "bold")
TITLE_COLOR = "#ffffff"

# Weather fetching logic
def get_weather(city):
    load_dotenv()
    API_KEY = os.getenv("OPENWEATHER_API_KEY")  # for security, store API key in a .env file
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()
        if data.get("cod") != 200:
            return f"❌ {data.get('message', 'City not found').capitalize()}"
        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"].capitalize()
        city = data.get("name", city.title())
        return f"📍 {city}\n🌡️ {temp}°C\n☁️ {desc}"
    except Exception as e:
        return f"❌ Error: {e}"

def show_weather():
    city = city_entry.get().strip()
    if not city:
        weather_label.config(text="Please enter a city name.", fg="red")
        return
    weather_label.config(text="Fetching weather...", fg=TEXT_COLOR)
    root.after(100, lambda: weather_label.config(text=get_weather(city), fg=TEXT_COLOR))

def clear_fields():
    city_entry.delete(0, tk.END)
    weather_label.config(text="", fg=TEXT_COLOR)

root = tk.Tk()
root.title("Weather Displayer (City)")
root.geometry("400x220")
root.configure(bg=BG_COLOR)
root.resizable(False, False)

# Style configuration for ttk buttons
style = ttk.Style(root)
style.theme_use("clam")  # Use a clean theme that allows color override

style.configure("Custom.TButton",
                font=FONT,
                foreground=BTN_TEXT_COLOR,
                background=BTN_COLOR,
                borderwidth=1,
                focusthickness=3,
                focuscolor="none",
                padding=6)

style.map("Custom.TButton",
          background=[('active', BTN_HOVER_COLOR)],
          foreground=[('disabled', '#888'), ('!disabled', BTN_TEXT_COLOR)])

### UI Setup

# Title
title_label = tk.Label(root, text="Weather Displayer", font=TITLE_FONT, bg=BG_COLOR, fg=TITLE_COLOR)
title_label.pack(pady=(15, 5))

# City
city_frame = tk.Frame(root, bg=BG_COLOR)
city_frame.pack(pady=10)
city_label = tk.Label(city_frame, text="City:", font=FONT, bg=BG_COLOR, fg=TEXT_COLOR)
city_label.pack(side=tk.LEFT, padx=(0, 5))

city_entry = tk.Entry(city_frame, font=FONT, width=22, bg=ENTRY_BG, fg=ENTRY_FG, insertbackground=ENTRY_FG, relief=tk.FLAT)
city_entry.pack(side=tk.LEFT)

# Buttons (ttk)
btn_frame = tk.Frame(root, bg=BG_COLOR)
btn_frame.pack(pady=10)

get_btn = ttk.Button(btn_frame, text="Get Weather", command=show_weather, style="Custom.TButton")
get_btn.pack(side=tk.LEFT, padx=5)

clear_btn = ttk.Button(btn_frame, text="Clear", command=clear_fields, style="Custom.TButton")
clear_btn.pack(side=tk.LEFT, padx=5)

# Weather result
weather_label = tk.Label(root, text="", font=FONT, bg=BG_COLOR, fg=TEXT_COLOR, justify=tk.LEFT)
weather_label.pack(pady=15)

root.mainloop()