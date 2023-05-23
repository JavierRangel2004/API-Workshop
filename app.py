from flask import Flask, render_template, request, redirect, url_for
from pokemon import PokemonGo
import pandas as pd
import os
import plotly.graph_objects as go
import plotly.offline as pyo
from plotly.subplots import make_subplots

app = Flask(__name__)
pokedex = PokemonGo()

@app.route('/')
def home():
    message = ""
    return render_template('home.html', message=message)

@app.route('/add', methods=['POST'])
def add():
    name = request.form.get('pokemon').lower()
    basic_info = pokedex.basic_info(name)
    messages=[]
    if basic_info["notFound"]:
        messages.append("The Pokémon was not found.")
    else:
        messages.append(f'{name.capitalize()} is of type {" ".join(basic_info["type"])}')
        messages.append(f'{name.capitalize()} is resistant to {", ".join(basic_info["resistant"])}')
        messages.append(f'{name.capitalize()} is weak against {", ".join(basic_info["weaknesses"])}')
        messages.append(f'{name.capitalize()} has advantage against {", ".join(basic_info["advantages"])}')

        message = f'{name.capitalize()} is of type {" ".join(basic_info["type"])}\n' + \
                             f'{name.capitalize()} is resistant to {", ".join(basic_info["resistant"])}\n' + \
                             f'{name.capitalize()} is weak against {", ".join(basic_info["weaknesses"])}\n' + \
                             f'{name.capitalize()} has advantage against {", ".join(basic_info["advantages"])}'
    
    if not basic_info["notFound"] and not pokedex.pokemon_already_saved(name) :
        pokedex.save_pokemon(name)
        pokedex.get_pokemon_stats(name)
    
    return render_template('home.html', messages=messages)

@app.route('/show_all')
def show_all():
    try:
        df = pd.read_csv('pokemons.csv')
        table = go.Figure(data=[go.Table(
            header=dict(values=list(df.columns),
                        fill_color='paleturquoise',
                        align='left'),
            cells=dict(values=[df.name, df.type, df.weakness, df.resistance, df.advantage],
                       fill_color='lavender',
                       align='left'))
        ])
        table_div = pyo.plot(table, output_type='div', include_plotlyjs=False)
    except FileNotFoundError:
        table_div = ""
    return render_template('show_all.html', table_div=table_div)

# @app.route('/show_stats')
# def show_stats():
#     try:
#         pokemons_stats = df.to_dict(orient='records')
#         df= pd.read_csv('pokemons_stats.csv')  # Try to read the Pokémon data from the CSV file
#         total = df['hp'] + df['attack'] + df['defense'] + df['special_attack'] + df['special_defense'] + df['speed']  # Calculate the total stats of each Pokémon
#         df['total'] = total
#         df = df.sort_values(by=['total'], ascending=False)#sort the total stats from highest to lowest
#         df.to_csv('pokemons_stats.csv', index=False)  # Save the DataFrame to the CSV file
#         df = pd.read_csv('pokemons_stats.csv')  # Try to read the Pokémon data from the CSV file
#         total = df['total']#Get the total stats
#         stats_fig = go.Figure(data=[go.Bar(x=df['name'], y=total)])  # Create a bar graph using plotly
#         stats_fig.update_layout(title="Your Pokémon team Statistics",#set the title and axis labels
#                                     xaxis_title="Pokémon",
#                                     yaxis_title="Total Stats")
#         plot_div = pyo.plot(stats_fig, output_type='div', include_plotlyjs=False)

#     except FileNotFoundError:
#         pokemons_stats = []
#         plot_div = ""
#     return render_template('show_stats.html', pokemons_stats=pokemons_stats, plot_div=plot_div)

@app.route('/show_stats')
def show_stats():
    try:
        df = pd.read_csv('pokemons_stats.csv')  # Try to read the Pokémon data from the CSV file
        total = df['hp'] + df['attack'] + df['defense'] + df['special_attack'] + df['special_defense'] + df['speed']  # Calculate the total stats of each Pokémon
        df['total'] = total
        df = df.sort_values(by=['total'], ascending=False)  # Sort the total stats from highest to lowest
        df.to_csv('pokemons_stats.csv', index=False)  # Save the DataFrame to the CSV file
        df = pd.read_csv('pokemons_stats.csv')  # Try to read the Pokémon data from the CSV file
        total = df['total']  # Get the total stats
        pokemons_stats = df.to_dict(orient='records')

        # Add a new field to each dictionary in pokemons_stats with the Pokémon's image URL
        for pokemon in pokemons_stats:
            pokemon['image'] = pokedex.get_pokemon_image(pokemon['name'])

        stats_fig = go.Figure(data=[go.Bar(x=df['name'], y=total)])  # Create a bar graph using plotly
        stats_fig.update_layout(title="Your Pokémon team Statistics",  # Set the title and axis labels
                                    xaxis_title="Pokémon",
                                    yaxis_title="Total Stats")
        plot_div = pyo.plot(stats_fig, output_type='div', include_plotlyjs=False)

    except FileNotFoundError:
        pokemons_stats = []
        plot_div = ""

    return render_template('show_stats.html', pokemons_stats=pokemons_stats, plot_div=plot_div)



@app.route('/clear')
def clear():
    try:
        messages = []
        os.remove('log.txt')
        os.remove('pokemons.csv')
        os.remove('pokemons_stats.csv')
        messages.append("The files were cleared successfully.")
    except FileNotFoundError:
        messages.append("There are no files to clear.")
    return render_template('home.html', messages=messages)

if __name__ == "__main__":
    app.run(debug=True)