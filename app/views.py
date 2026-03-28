from django.shortcuts import render
import datetime
import json
from urllib.parse import urlencode
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

# Create your views here.
def home(request):
    if "city" in request.POST:
        city = request.POST["city"]
    else:
        city = "kathmandu"

    params = {
        "q": city,
        "appid": "36c7399f052f12cd0c33171d5b9bd164",
        "units": "metric",
    }
    url = "https://api.openweathermap.org/data/2.5/weather?" + urlencode(params)

    try:
        with urlopen(url) as response:
            data = json.load(response)
    except (HTTPError, URLError, TimeoutError):
        data = {"cod": "error"}

    if data.get("cod") != 200:
        description = "Unable to fetch weather"
        icon = "01d"
        temp = "N/A"
        feels_like = "N/A"
        humidity = "N/A"
        wind_speed = "N/A"
        country = ""
        weather_label = "Weather Unavailable"
        theme = "day"
    else:
        description = data["weather"][0]["description"]
        icon = data["weather"][0]["icon"]
        temp = round(data["main"]["temp"])
        feels_like = round(data["main"]["feels_like"])
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        country = data["sys"].get("country", "")
        weather_label = data["weather"][0]["main"]
        theme = "night" if icon.endswith("n") else "day"

    day = datetime.date.today()
    formatted_day = day.strftime("%A, %d %B %Y")

    return render(
        request,
        "app/index.html",
        {
            "city": city,
            "country": country,
            "description": description,
            "weather_label": weather_label,
            "icon": icon,
            "temp": temp,
            "feels_like": feels_like,
            "humidity": humidity,
            "wind_speed": wind_speed,
            "day": formatted_day,
            "theme": theme,
        },
    )
