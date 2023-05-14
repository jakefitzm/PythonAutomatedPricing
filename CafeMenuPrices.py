import requests
import tkinter as tk
import datetime
import time
from geopy.geocoders import Nominatim

API_KEY = '4e0a54400095f9ac754a93f4849fa008'

def get_weather_data(api_key, city):
    try:    
        geolocator = Nominatim(user_agent="CafeMenuPrices")
        location = geolocator.geocode(city)
        lat, lon = location.latitude, location.longitude
        
        weather_url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
        response = requests.get(weather_url)
        data = response.json()
        temperature = data['main']['temp']
        condition = data['weather'][0]['description']    
        
        return temperature, condition
    
    except:
        print("Error: Unable to retrieve weather data. Please check your input and try again.")
        return None, None
api_key = '4e0a54400095f9ac754a93f4849fa008'
city = 'Dublin'
temperature, condition = get_weather_data(api_key, city)
if temperature and condition:
    print(f'The current temperature in {city} is {temperature}°C and the condition is {condition}.')

def adjust_price(price, temperature, condition, drink_type):
    if drink_type == "hot":
        if temperature < 0:
            price *= 1.4
        elif temperature < 12:
            if condition == 'Rain':
                price *= 1.075
            price *= 1.02 ** (12 - temperature)
        else:
            price /= 1.02 ** (temperature - 12) * (1 + 0.02 * (temperature - 12))
            if condition == 'Rain':
                price *= 1.075
        return round(price, 2)
    
    elif drink_type == "cold":
        if temperature < 0:
            price *= 0.7
        elif temperature < 12:
            if condition == 'Rain':
                price *= 0.925
            price /= 1.02 ** (12 - temperature)
        else:
            price *= 1 + 0.02 * (temperature - 12)
            if condition == 'Rain':
                price *= 1.075
        return round(price, 2)
    
    else:
        return price

def display_menu(root, api_key, city):
    hot_drinks = {'Tea': 2.5, 'Coffee': 3.0, 'Hot Chocolate': 3.5}
    cold_drinks = {'Iced Tea': 2.0, 'Iced Coffee': 2.5, 'Smoothie': 4.0}

    # Get the current timestamp and temperature
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    temperature, condition = get_weather_data(api_key, city)

    root.title("Python Cafe")
    root.geometry("800x480")
    root.attributes("-fullscreen", True)

    title_label = tk.Label(root, text="Python Cafe", font=("Arial", 50), fg="red")
    title_label.pack(pady=(20, 50))

    weather_label = tk.Label(root, text="Today's temperature in " + city + " is " + str(temperature) + " degrees Celsius\nand the weather condition is " + condition, font=("Arial", 20))
    weather_label.pack()

    menu_label = tk.Label(root, text="Menu", font=("Arial", 30))
    menu_label.pack(pady=(50, 20))

    hot_drinks_label = tk.Label(root, text="Hot Drinks:", font=("Arial", 20))
    hot_drinks_label.pack()

    for drink, price in hot_drinks.items():
        new_price = adjust_price(price, temperature, condition, "hot")
        drink_label = tk.Label(root, text=drink + " - €" + str(new_price), font=("Arial", 15))
        drink_label.pack()

    cold_drinks_label = tk.Label(root, text="Cold Drinks:", font=("Arial", 20))
    cold_drinks_label.pack()

    for drink, price in cold_drinks.items():
        new_price = adjust_price(price, temperature, condition, "cold")
        drink_label = tk.Label(root, text=drink + " - €" + str(new_price), font=("Arial", 15))
        drink_label.pack()

    menu_timestamp = tk.Label(root, text="Last updated: " + timestamp, font=("Arial", 10))
    menu_timestamp.pack(side="bottom", pady=(0, 20))

    exit_button = tk.Button(root, text="Exit", command=root.destroy)
    exit_button.pack(side="bottom", pady=(20, 0))

def update_menu(root):
    # get the current time
    now = datetime.datetime.now()

    # check if the current time is between 9am and 6pm
    if now.hour >= 9 and now.hour < 18:
    # update the menu display, show in the console that it is updating
        print("menu closed.")
        display_menu(root, '4e0a54400095f9ac754a93f4849fa008', 'Dublin')
        print(f"Updating menu...")

    # Destroy the previous Toplevel window
    for widget in root.winfo_children():
        if isinstance(widget, tk.Toplevel):
            widget.destroy()

    # Create a new Toplevel window
    top = tk.Toplevel(root)

    # populate the new window with the updated menu
    display_menu(top, '4e0a54400095f9ac754a93f4849fa008', 'Dublin')

    # schedule the update_menu function to be called again after 30 minutes
    root.after(180000, update_menu, root)
    
# create the first window
root = tk.Tk()

# populate the first window with the menu
display_menu(root, '4e0a54400095f9ac754a93f4849fa008', 'Dublin')

# schedule the update_menu function to be called after a delay of 30 minutes
root.after(180000, update_menu, root)

# start the main event loop
root.mainloop()