from flask import Flask, render_template, request
import requests

app = Flask(__name__)

STAT_NAMES = {
    "hp": "HP",
    "attack": "Atk",
    "defense": "Def",
    "special-attack": "Sp.Atk",
    "special-defense": "Sp.Def",
    "speed": "Speed"
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search", methods=["POST"])
def search():
    pokemon_name = request.form["pokemon"].lower()
    response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}")
    
    if response.status_code == 200:
        data = response.json()
        pokemon = {
            "name": data["name"].capitalize(),
            "id": data["id"],
            "height": data["height"],
            "weight": data["weight"],
            "types": [t["type"]["name"] for t in data["types"]],
            "stats": {STAT_NAMES[s["stat"]["name"]]: s["base_stat"] for s in data["stats"]},
            "image": data["sprites"]["front_default"]
        }
        return render_template("pokemon.html", pokemon=pokemon)
    else:
        return render_template("index.html", error="Pokémon not found!")
    
@app.route("/pokemon-list")
def pokemon_list():
    response = requests.get("https://pokeapi.co/api/v2/pokemon?limit=1500")
    data = response.json()
    names = [p["name"] for p in data["results"]]
    return {"pokemon": names}

@app.route("/pokemon/<name>")
def pokemon(name):
    response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{name}")
    if response.status_code == 200:
        data = response.json()
        pokemon = {
            "name": data["name"].capitalize(),
            "id": data["id"],
            "height": data["height"],
            "weight": data["weight"],
            "types": [t["type"]["name"] for t in data["types"]],
            "stats": {STAT_NAMES[s["stat"]["name"]]: s["base_stat"] for s in data["stats"]},
            "image": data["sprites"]["front_default"]
        }
        return render_template("pokemon.html", pokemon=pokemon)
    else:
        return render_template("index.html", error="Pokémon not found!")

if __name__ == "__main__":
    app.run(debug=True)