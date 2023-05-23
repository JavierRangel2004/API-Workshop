from flask import Flask, render_template, request, redirect, url_for
from pokemon import PokemonGo
import pandas as pd
import os

app = Flask(__name__)
pokedex = PokemonGo()

basic_info_message = ""  # Initialize a global variable to store the basic info message

@app.route('/')
def home():
    global basic_info_message  # Access the global variable inside the function
    return render_template('home.html', message=basic_info_message)  # Pass the message to the template

@app.route('/add', methods=['POST'])
def add():
    global basic_info_message  # Access the global variable inside the function
    name = request.form.get('pokemon')
    basic_info = pokedex.basic_info(name)  # Update to return a dictionary

    if basic_info["notFound"]:
        basic_info_message = "The Pokémon was not found."
    else:
        basic_info_message = f'{name.capitalize()} is of type {basic_info["type"]}\n' + \
                             f'{name.capitalize()} is resistant to {", ".join(basic_info["resistant"])}\n' + \
                             f'{name.capitalize()} is weak against {", ".join(basic_info["weaknesses"])}\n' + \
                             f'{name.capitalize()} has advantage against {", ".join(basic_info["advantages"])}'
    
    if basic_info["notFound"]==False:
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
    global basic_info_message  # Access the global variable inside the function
    try:
        os.remove('log.txt')
        os.remove('pokemons.csv')
        os.remove('pokemons_stats.csv')
        message = "The CSV file was cleared successfully."
    except FileNotFoundError:
        message = "The CSV file does not exist."
    basic_info_message = ""  # Clear the basic info message when the files are cleared
    return render_template('home.html', message=message)

if __name__ == "__main__":
    app.run(debug=True)
