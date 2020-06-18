import urllib.request
import json

# TODO make an object mapping cities to their lat and lon so that city names can be typed in instead
# locationDict = { "LA": { "lat": 0, "lon": 0}}


def printweather(lat, lon):
  # ...with TODO above. if lat in locationDict.keys(): locationDict[lat] etc...
  # rename lat to latOrCity?
    try:
        data = urllib.request.urlopen(
            f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=hourly,daily,minutely&units=imperial&appid=4ba6a408966bcec7ac3ae7026c9ab365")
        wData = json.loads(data.read())
        # print(readableData) #prints very poorly
        # below is human readable
        # print(json.dumps(wData, indent=4, sort_keys=True))
        return f"{wData['current']['temp']} fahrenheit. {wData['current']['humidity']}% humidity. Feels like {wData['current']['feels_like']} fahrenheit. Generally: {wData['current']['weather'][0]['description']}."
    except:
        return "Something went wrong."
