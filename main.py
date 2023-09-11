import tkinter as tk
from tkinter import ttk
import requests
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from datetime import datetime
from weatherApp.WeatherApp.key import api


def get_weather():
    city = city_entry.get()
    api_key = api

    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
    response = requests.get(url, timeout=10)
    weather_data = response.json()

    if weather_data["cod"] != "404":
        hourly_data = weather_data["list"]

        # Clear previous plot
        plt.clf()

        temperatures = []
        timestamps = []
        humidities = []
        pressures = []
        feels_like = []
        weather_now = []

        for data in hourly_data:
            temperature = data["main"]["temp"]
            timestamp = datetime.fromtimestamp(data["dt"])
            humidity = data['main']['humidity']
            pressure = data['main']['pressure']
            feels_liked = data['main']['feels_like']
            weath = data['weather'][0]['main']
            temperatures.append(temperature)
            timestamps.append(timestamp)
            humidities.append(humidity)
            pressures.append(pressure)
            feels_like.append(feels_liked)
            weather_now.append(weath)

        # Update the temperature label
        temperature_label.config(text=f"Temperature: {temperatures[0]}°C")

        feels_like_label= tk.Label(root, text=f"Feeling temperature is {feels_like[0]}°C ", font=("Helvetica", 20))
        feels_like_label.pack()
        humid_label = tk.Label(root, text=f"Humidity is {humidities[0]}%", font=("Helvetica", 20))
        humid_label.pack()
        pressure_label= tk.Label(root, text=f"Pessure is {pressures[0]} hPa", font=("Helvetica", 20))
        pressure_label.pack()
        weather_label= tk.Label(root, text=f"Weather now: {weather_now[0]}", font=("Helvetica", 20))
        weather_label.pack()

        # Create a figure and plot
        fig = plt.figure(figsize=(8, 4))
        plt.plot(timestamps, temperatures, marker='o', linestyle='-', color='blue')
        plt.gcf().autofmt_xdate()
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
        plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=12))
        plt.xlabel("Time")
        plt.ylabel("Temperature (°C)")
        plt.title(f"Hourly Temperature Forecast for {city}")
        plt.grid(True)

        # Create a Tkinter canvas and embed the plot
        canvas = FigureCanvasTkAgg(fig, master=plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

        # Create a navigation toolbar for the plot
        toolbar = NavigationToolbar2Tk(canvas, plot_frame)
        toolbar.update()
        toolbar.pack()

    else:
        temperature_label.config(text="Weather information not found")


root = tk.Tk()
root.title("Weather App")

# Create the input section
input_frame = ttk.Frame(root)
input_frame.pack(pady=20)

city_entry = ttk.Entry(input_frame, font=("Helvetica", 20))
city_entry.pack(side=tk.LEFT, padx=10)

get_weather_button = ttk.Button(
    input_frame, text="Get Weather", command=get_weather
    )
get_weather_button.pack(side=tk.LEFT)

# Create the weather information section
weather_frame = ttk.Frame(root)
weather_frame.pack(pady=20)

temperature_label = ttk.Label(weather_frame, font=("Helvetica", 20))
temperature_label.pack()

# Create the plot section
plot_frame = ttk.Frame(root)
plot_frame.pack(pady=20)

root.mainloop()
