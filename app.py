from flask import Flask, request, make_response
import os, json
import pyowm
import os
from flask_cors import CORS,cross_origin

app = Flask(__name__)
# owmapikey=os.environ.get('119242c426975bc98ee4f259b9551823') #or provide your key here
#owmapikey = '119242c426975bc98ee4f259b9551823'
owmapikey = 'c235e087f66450ccd468cf92507f97fd'
owm = pyowm.OWM(owmapikey)

'''import requests
url = "https://weatherbit-v1-mashape.p.rapidapi.com/current"
querystring = {"lang":"en","lon":"<required>","lat":"<required>"}
headers = {
    'x-rapidapi-host': "weatherbit-v1-mashape.p.rapidapi.com",
    'x-rapidapi-key': "15263c1e77msh408ed2560d9f1c9p123c23jsn0fc0b44e64ea"
    }
response = requests.request("GET", url, headers=headers, params=querystring)
print(response.text)'''

# geting and sending response to dialogflow
@app.route('/webhook', methods=['POST'])
@cross_origin()
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


# processing the request from dialogflow
def processRequest(req):
    result = req.get("queryResult")
    parameters = result.get("parameters")
    city = parameters.get("geo-city")
    date = parameters.get("Date")
    observation = owm.weather_at_place(city)
    w = observation.get_weather()
    latlon_res = observation.get_location()
    lat = str(latlon_res.get_lat())
    lon = str(latlon_res.get_lon())

    wind_res = w.get_wind()
    wind_speed = str(wind_res.get('speed'))

    humidity = str(w.get_humidity())

    celsius_result = w.get_temperature('celsius')
    temp_min_celsius = str(celsius_result.get('temp_min'))
    temp_max_celsius = str(celsius_result.get('temp_max'))

    fahrenheit_result = w.get_temperature('fahrenheit')
    temp_min_fahrenheit = str(fahrenheit_result.get('temp_min'))
    temp_max_fahrenheit = str(fahrenheit_result.get('temp_max'))
    fulfillmentText = "The weather in " + city +   "for"  + date + ": \n" + "Temperature in Celsius:\nMax temp :" + temp_max_celsius + ".\nMin Temp :" + temp_min_celsius + ".\nTemperature in Fahrenheit:\nMax temp :" + temp_max_fahrenheit + ".\nMin Temp :" + temp_min_fahrenheit + ".\nHumidity :" + humidity + ".\nWind Speed :" + wind_speed + "\nLatitude :" + lat + ".\n  Longitude :" + lon

    return {
        "fulfillmentText": fulfillmentText,
        "displayText": fulfillmentText,
        "source": "dialogflow-weather-by-satheshrgs"
    }


if __name__ == '__main__':
 port = int(os.getenv('PORT', 5000))
 print("Starting app on port %d" % port)
 app.run(debug=True, port=port, host='0.0.0.0')
 ##app.run(debug=True, port = 5000)