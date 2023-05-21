import requests
import pandas as pd
import datetime
import os
import plotly.graph_objects as go

def clear():
    input("Press enter to continue...")
    os.system('cls')

class PokemonGo():
    def __init__(self):
        self.url = 'https://pokeapi.co/api/v2/'

    def createtypesdata(self):
        try:
            pd.read_csv('types.csv')
        except FileNotFoundError:
            self.fetch_and_save_types_data()

    def fetch_and_save_types_data(self):
        try:
            response = requests.get(self.url + 'type')
            self.log_requests(response)

            if response.status_code == 200:
                data = response.json()
                types = []
                for type in data['results']:
                    type_url = type['url']
                    type_response = requests.get(type_url)
                    self.log_requests(type_response)
                    type_data = type_response.json()

                    weaknesses = [d['name'] for d in type_data['damage_relations']['double_damage_from']]
                    resistances = [r['name'] for r in type_data['damage_relations']['half_damage_from']]
                    advantages = [v['name'] for v in type_data['damage_relations']['double_damage_to']]

                    if type['name'] not in ["unknown", "shadow"]:
                        types.append({'Type': type['name'], 'Weaknesses': weaknesses, 'Resistances': resistances, 'Advantages': advantages})

                df = pd.DataFrame(types)
                df.to_csv('types.csv', index=False)
        except requests.exceptions.RequestException as e:
            print(f"There was a problem obtaining the data: {e}")
            return None

    def log_requests(self, response):
        with open('log.txt', 'a') as f:
            f.write(f"{datetime.datetime.now()} - {response.url} - {response.status_code}\n")

    def get_pokemon(self, pokemon):
        try:
            url = self.url + 'pokemon/' + pokemon
            response = requests.get(url)
            self.log_requests(response)

            if response.status_code == 200:
                return response.json()
            else:
                print("The pokemon was not found.")
                return None
        except requests.exceptions.RequestException as e:
            print(f"There was a problem obtaining the data: {e}")
            return None

    def get_pokemon_type(self, pokemon):
        data = self.get_pokemon(pokemon)
        return data['types'][0]['type']['name'] if data else None

    def get_pokemon_data(self, pokemon):
        try:
            type = self.get_pokemon_type(pokemon)
            df = pd.read_csv('types.csv')
            df = df[df['Type'] == type]
            return df
        except FileNotFoundError:
            print("The file 'types.csv' was not found.")
            return pd.DataFrame()

    def get_weakness(self, pokemon):
        df = self.get_pokemon_data(pokemon)
        return df['Weaknesses'].values[0] if not df.empty else None

    def get_resistance(self, pokemon):
        df = self.get_pokemon_data(pokemon)
        return df['Resistances'].values[0] if not df.empty else None

    def get_advantage(self, pokemon):
        df = self.get_pokemon_data(pokemon)
        return df['Advantages'].values[0] if not df.empty else None

    def basic_info(self, pokemon):
        type = self.get_pokemon_type(pokemon)
        df = self.get_pokemon_data(pokemon)
        if df.empty:
            print("The Pokémon was not found.")
            return
        print(f"{pokemon} is of type {type}")
        print(f"{pokemon} is resistant to {df['Resistances'].values[0]}")
        print(f"{pokemon} is weak against {df['Weaknesses'].values[0]}")
        print(f"{pokemon} has advantage against {df['Advantages'].values[0]}")

    def save_pokemon(self, pokemon):
        df = pd.DataFrame(columns=['name', 'type', 'weakness', 'resistance', 'advantage'])
        try:
            df = pd.read_csv('pokemons.csv')
        except FileNotFoundError:
            df.to_csv('pokemons.csv', index=False)
        
        data = [{'name': pokemon, 'type': self.get_pokemon_type(pokemon), 'weakness': self.get_weakness(pokemon), 'resistance': self.get_resistance(pokemon), 'advantage': self.get_advantage(pokemon)}]
        df = df.append(data, ignore_index=True)
        df.to_csv('pokemons.csv', index=False)
    
    def get_pokemon_info(self, name):
        try:
            url = f"{self.url}pokemon/{name.lower()}"
            response = requests.get(url)
            self.log_requests(response)
            if response.status_code == 200:
                data = response.json()
                stats = {stat['stat']['name']: stat['base_stat'] for stat in data['stats']}
                return stats
            else:
                print(f"No information was found for the Pokémon {name.capitalize()}.")
                return None
        except requests.exceptions.RequestException as e:
            print(f"There was a problem obtaining the data: {e}")
            return None

    def show_pokemon_stats_graph(self, name):
        pokemon_info = self.get_pokemon_info(name)
        if pokemon_info:
            stats = pokemon_info

            # Plot stats
            stats_fig = go.Figure(data=[go.Bar(x=list(stats.keys()), y=list(stats.values()))])
            stats_fig.update_layout(title=f"{name.capitalize()}'s Statistics",
                                    xaxis_title="Statistic",
                                    yaxis_title="Value")
            stats_fig.show()
        else:
            print(f"No information was found for the Pokémon {name.capitalize()}.")

Api = PokemonGo()

def menu():
    print("Welcome to the Pokedex")
    print("1. Search Pokémon")
    print("2. View all Pokémon")
    print("3. Exit")
    option = input("Enter an option: ")
    return option

while True:
    Api.createtypesdata()
    option = menu()
    if option == "1":
        pokemon = input("Enter the Pokémon's name: ").lower()
        clear()
        Api.basic_info(pokemon)
        Api.save_pokemon(pokemon)
        Api.show_pokemon_stats_graph(pokemon)
    elif option == "2":
        try:
            df = pd.read_csv('pokemons.csv')
            print(df)
            clear()
        except FileNotFoundError:
            print("The file 'pokemons.csv' was not found.")
            clear()
    elif option == "3":
        break
    else:
        print("Invalid option")
        clear()