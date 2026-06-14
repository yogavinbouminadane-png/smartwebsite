

from flask import Flask, render_template, request
from deep_translator import GoogleTranslator
import requests

app = Flask(__name__)

# Get ALL supported languages automatically
languages = GoogleTranslator().get_supported_languages(as_dict=True)

@app.route("/", methods=["GET", "POST"])
def home():

    meaning = ""
    temperature = ""
    recipe = ""
    translation = ""

    if request.method == "POST":

        # WORD MEANING
        if request.form.get("word"):
            word = request.form.get("word")

            try:
                url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
                data = requests.get(url, timeout=10).json()

                meaning = data[0]["meanings"][0]["definitions"][0]["definition"]

            except:
                meaning = "Meaning not found."

        # TEMPERATURE
        elif request.form.get("city"):
            city = request.form.get("city")

            try:
                url = f"https://wttr.in/{city}?format=%t"
                temperature = requests.get(url, timeout=10).text

            except:
                temperature = "Temperature not found."

        # RECIPE
        elif request.form.get("food"):
            food = request.form.get("food")

            try:
                url = f"https://www.themealdb.com/api/json/v1/1/search.php?s={food}"
                data = requests.get(url, timeout=10).json()

                if data["meals"]:
                    meal = data["meals"][0]

                    recipe = f"""Recipe: {meal['strMeal']}

Category: {meal['strCategory']}

Instructions:
{meal['strInstructions']}"""
                else:
                    recipe = "Recipe not found in database."

            except:
                recipe = "Error fetching recipe."

        # TRANSLATOR (ALL LANGUAGES)
        elif request.form.get("text"):
            text = request.form.get("text")
            language = request.form.get("language")

            try:
                translation = GoogleTranslator(
                    source="auto",
                    target=language
                ).translate(text)

            except:
                translation = "Translation failed."

    return render_template(
        "home.html",
        meaning=meaning,
        temperature=temperature,
        recipe=recipe,
        translation=translation,
        languages=languages
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

