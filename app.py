from flask import Flask, render_template, request, redirect, url_for
from pokemon import PokemonGo
import pandas as pd
import os

app = Flask(__name__)
pokedex = PokemonGo()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/add', methods=['POST'])
def add():
    name = request.form.get('pokemon')
    pokedex.basic_info(name)
    pokedex.save_pokemon(name)
    pokedex.get_pokemon_stats(name)
    return redirect(url_for('home'))

@app.route('/show_all')
def show_all():
    try:
        df = pd.read_csv('pokemons.csv')
        pokemons = df.to_dict(orient='records')
    except FileNotFoundError:
        pokemons = []
    return render_template('show_all.html', pokemons=pokemons)

@app.route('/show_stats')
def show_stats():
    try:
        df = pd.read_csv('pokemons_stats.csv')
        pokemons_stats = df.to_dict(orient='records')
    except FileNotFoundError:
        pokemons_stats = []
    return render_template('show_stats.html', pokemons_stats=pokemons_stats)

@app.route('/clear')
def clear():
    try:
        os.remove('pokemons.csv')
        os.remove('pokemons_stats.csv')
        os.remove('types.csv')
        message = "The CSV file was cleared successfully."
    except FileNotFoundError:
        message = "The CSV file does not exist."
    return render_template('home.html', message=message)

if __name__ == "__main__":
    app.run(debug=True)
