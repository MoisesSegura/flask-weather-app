from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Claves de API
WEATHER_API_KEY = "c7f6fe0e714d246a873756ffa2bcbf70"
UNSPLASH_ACCESS_KEY = "Bmh136ZSOF-of1U33xvmVvz2twKBbnGq_Pz8Gif3HPE"

# Página principal
@app.route("/", methods=["GET", "POST"])
def home():
    weather_data = None
    city_image = None

    if request.method == "POST":
        city = request.form.get("city")

        #  datos del clima desde OpenWeatherMap
        weather_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric&lang=es"
        weather_response = requests.get(weather_url)

        if weather_response.status_code == 200:
            weather_data = weather_response.json()

            # imagen de la ciudad desde Unsplash
            unsplash_url = f"https://api.unsplash.com/search/photos?query={city}&client_id={UNSPLASH_ACCESS_KEY}&per_page=1"
            unsplash_response = requests.get(unsplash_url)

            if unsplash_response.status_code == 200 and unsplash_response.json()["results"]:
                city_image = unsplash_response.json()["results"][0]["urls"]["regular"]

    return render_template("index.html", weather=weather_data, city_image=city_image)

# 🔹 Nueva ruta para autocompletar ciudades
@app.route("/autocomplete")
def autocomplete():
    query = request.args.get("q")
    if not query:
        return jsonify([])

    geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={query}&limit=5&appid={WEATHER_API_KEY}"
    response = requests.get(geo_url)

    if response.status_code == 200:
        cities = response.json()
        suggestions = [f"{city['name']}, {city['country']}" for city in cities]
        return jsonify(suggestions)

    return jsonify([])

if __name__ == "__main__":
    app.run(debug=True)
