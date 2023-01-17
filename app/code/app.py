import requests

from flask import Flask

app = Flask(__name__)

API_KEY = "45581b696ab5c0011abd67e94508b64c"

@app.route('/')
def index():
    return 'Wilson API - Works fine!'

@app.route('/<string:city>/<string:country>/')
def weather_by_city(country, city):

    url = 'http://api.openweathermap.org/data/2.5/weather'
    params = dict(
        q=city + "," + country,
        appid= API_KEY,
    )

    response = requests.get(url=url, params=params)
    data = response.json()
    return data

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)