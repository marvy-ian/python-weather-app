import tkinter as tk
from tkinter import ttk, messagebox
import threading
import requests

API_URL = "https://wttr.in/{city}?format=j1"

WEATHER_ICONS = {
    "sunny": "☀️",
    "clear": "🌤️",
    "partly cloudy": "⛅",
    "cloudy": "☁️",
    "overcast": "☁️",
    "mist": "🌫️",
    "fog": "🌫️",
    "rain": "🌧️",
    "drizzle": "🌦️",
    "thunder": "⛈️",
    "snow": "❄️",
    "sleet": "🌨️",
}


def get_icon(description: str) -> str:
    description = description.lower()
    for key, icon in WEATHER_ICONS.items():
        if key in description:
            return icon
    return "🌡️"


class WeatherApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Weather App")
        self.geometry("420x480")
        self.resizable(False, False)
        self.configure(bg="#1e2a38")

        self._build_ui()

    def _build_ui(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TButton", font=("Segoe UI", 11), padding=6)
        style.configure("TEntry", font=("Segoe UI", 12))

        header = tk.Label(
            self, text="Weather Now", font=("Segoe UI", 20, "bold"),
            bg="#1e2a38", fg="white"
        )
        header.pack(pady=(20, 10))

        search_frame = tk.Frame(self, bg="#1e2a38")
        search_frame.pack(pady=5)

        self.city_entry = ttk.Entry(search_frame, width=24, font=("Segoe UI", 12))
        self.city_entry.grid(row=0, column=0, padx=(0, 8))
        self.city_entry.insert(0, "Quezon City")
        self.city_entry.bind("<Return>", lambda e: self.search_weather())

        search_btn = ttk.Button(search_frame, text="Search", command=self.search_weather)
        search_btn.grid(row=0, column=1)

        self.status_label = tk.Label(
            self, text="", font=("Segoe UI", 10), bg="#1e2a38", fg="#9fb3c8"
        )
        self.status_label.pack(pady=(4, 0))

        self.card = tk.Frame(self, bg="#28394d", bd=0)
        self.card.pack(pady=20, padx=30, fill="both", expand=True)

        self.icon_label = tk.Label(self.card, text="🌍", font=("Segoe UI", 48), bg="#28394d", fg="white")
        self.icon_label.pack(pady=(20, 5))

        self.city_label = tk.Label(self.card, text="", font=("Segoe UI", 16, "bold"), bg="#28394d", fg="white")
        self.city_label.pack()

        self.temp_label = tk.Label(self.card, text="", font=("Segoe UI", 36, "bold"), bg="#28394d", fg="white")
        self.temp_label.pack(pady=(5, 0))

        self.desc_label = tk.Label(self.card, text="", font=("Segoe UI", 13), bg="#28394d", fg="#c3d3e0")
        self.desc_label.pack(pady=(0, 15))

        details_frame = tk.Frame(self.card, bg="#28394d")
        details_frame.pack(pady=(0, 20))

        self.feels_label = self._detail_row(details_frame, "Feels like", 0)
        self.humidity_label = self._detail_row(details_frame, "Humidity", 1)
        self.wind_label = self._detail_row(details_frame, "Wind", 2)

        footer = tk.Label(
            self, text="Data: wttr.in", font=("Segoe UI", 8),
            bg="#1e2a38", fg="#5f7387"
        )
        footer.pack(side="bottom", pady=8)

        self.search_weather()

    def _detail_row(self, parent, label_text, row):
        tk.Label(parent, text=label_text, font=("Segoe UI", 10), bg="#28394d", fg="#9fb3c8") \
            .grid(row=row, column=0, sticky="w", padx=10, pady=3)
        value_label = tk.Label(parent, text="--", font=("Segoe UI", 10, "bold"), bg="#28394d", fg="white")
        value_label.grid(row=row, column=1, sticky="e", padx=10, pady=3)
        return value_label

    def search_weather(self):
        city = self.city_entry.get().strip()
        if not city:
            messagebox.showwarning("Input needed", "Please enter a city name.")
            return

        self.status_label.config(text="Loading...")
        self.icon_label.config(text="⏳")
        threading.Thread(target=self._fetch_weather, args=(city,), daemon=True).start()

    def _fetch_weather(self, city):
        try:
            response = requests.get(API_URL.format(city=city), timeout=10)
            response.raise_for_status()
            data = response.json()

            current = data["current_condition"][0]
            area = data["nearest_area"][0]

            city_name = area["areaName"][0]["value"]
            country = area["country"][0]["value"]
            temp_c = current["temp_C"]
            feels_c = current["FeelsLikeC"]
            humidity = current["humidity"]
            wind_kmph = current["windspeedKmph"]
            description = current["weatherDesc"][0]["value"]

            self.after(0, self._update_ui, {
                "city": f"{city_name}, {country}",
                "temp": f"{temp_c}°C",
                "feels": f"{feels_c}°C",
                "humidity": f"{humidity}%",
                "wind": f"{wind_kmph} km/h",
                "desc": description,
                "icon": get_icon(description),
            })
        except requests.exceptions.RequestException:
            self.after(0, self._show_error, "Network error. Check your connection and try again.")
        except (KeyError, IndexError, ValueError):
            self.after(0, self._show_error, "City not found. Try a different name.")

    def _update_ui(self, info):
        self.status_label.config(text="")
        self.icon_label.config(text=info["icon"])
        self.city_label.config(text=info["city"])
        self.temp_label.config(text=info["temp"])
        self.desc_label.config(text=info["desc"])
        self.feels_label.config(text=info["feels"])
        self.humidity_label.config(text=info["humidity"])
        self.wind_label.config(text=info["wind"])

    def _show_error(self, message):
        self.status_label.config(text="")
        self.icon_label.config(text="⚠️")
        self.city_label.config(text="")
        self.temp_label.config(text="")
        self.desc_label.config(text="")
        self.feels_label.config(text="--")
        self.humidity_label.config(text="--")
        self.wind_label.config(text="--")
        messagebox.showerror("Error", message)


if __name__ == "__main__":
    app = WeatherApp()
    app.mainloop()