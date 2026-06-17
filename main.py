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

def stat_to_color(value, min_val=20, max_val=360):
    stops = [
        (220, 20, 60),    # red
        (255, 140, 0),    # orange
        (255, 215, 0),    # yellow
        (50, 180, 50),    # green
        (90, 170, 255),   # light blue
        (20, 30, 150),    # dark blue
    ]
    t = (value - min_val) / (max_val - min_val)
    t = max(0, min(1, t))

    n_segments = len(stops) - 1
    segment = t * n_segments
    idx = int(segment)
    if idx >= n_segments:
        idx = n_segments - 1
    local_t = segment - idx

    c1, c2 = stops[idx], stops[idx + 1]
    r = round(c1[0] + (c2[0] - c1[0]) * local_t)
    g = round(c1[1] + (c2[1] - c1[1]) * local_t)
    b = round(c1[2] + (c2[2] - c1[2]) * local_t)
    return f"rgb({r}, {g}, {b})"

app.jinja_env.filters["stat_color"] = stat_to_color

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