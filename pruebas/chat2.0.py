import os
import requests
import pandas as pd
import plotly.graph_objects as go
from typing import List, Dict, Union

class PokemonGo:
    """
    Class to interact with the Pokémon API and provide information about different Pokémon.
    """
    def __init__(self):
        self.url = "https://pokeapi.co/api/v2/"
        self.data_cache = {}  # Cache for API responses
        self.file_cache = {}  # Cache for CSV dataframes

    def log_requests(self, response):
        """
        Method to log the requests to the API.
        """
        print(f"Request to {response.url} returned status code {response.status_code}")

    def get_request(self, endpoint: str) -> Dict:
        """
        Method to send a GET request to the Pokémon API.
        Handles caching of requests to avoid repeated calls to the API.
        """
        # If the data is in cache, return it
        if endpoint in self.data_cache:
            return self.data_cache[endpoint]

        # Send a GET request
        response = requests.get(self.url + endpoint)

        # Log the request
        self.log_requests(response)

        # If the request is successful, cache and return the data
        if response.status_code == 200:
            data = response.json()
            self.data_cache[endpoint] = data
            return data

        print(f"No information was found for the endpoint: {endpoint}")
        return None

    def read_csv(self, file_name: str) -> pd.DataFrame:
        """
        Method to read data from a CSV file.
        Handles caching of dataframes to avoid repeated file operations.
        """
        # If the DataFrame is in cache, return it
        if file_name in self.file_cache:
            return self.file_cache[file_name]

        # Try to read the CSV file
        try:
            df = pd.read_csv(file_name)
            self.file_cache[file_name] = df
            return df
        except FileNotFoundError:
            # If the file doesn't exist, return an empty DataFrame
            return pd.DataFrame()

    def write_csv(self, file_name: str, df: pd.DataFrame) -> None:
        """
        Method to write a DataFrame to a CSV file.
        Updates the cache after writing to the file.
        """
        df.to_csv(file_name, index=False)
        self.file_cache[file_name] = df

    def get_pokemon_type(self, pokemon: str) -> List[str]:
        """
        Method to get the type(s) of a specific Pokémon.
        """
        data = self.get_request(f"pokemon/{pokemon}")
        if data:
            return [type_info['type']['name'] for type_info in data['types']]
        return None

    def get_resistance(self, pokemon: str) -> List[str]:
        """
        Method to get the resistance types of a specific Pokémon.
        """
        types = self.get_pokemon_type(pokemon)
        if types:
            resistance = []
            for type_ in types:
                data = self.get_request(f"type/{type_}")
                if data:
                    resistance.extend([type_info['type']['name'] for type_info in data['damage_relations']['half_damage_from']])
            return list(set(resistance))
        return None

    def get_weakness(self, pokemon: str) -> List[str]:
        """
        Method to get the weakness types of a specific Pokémon.
        """
        types = self.get_pokemon_type(pokemon)
        if types:
            weakness = []
            for type_ in types:
                data = self.get_request(f"type/{type_}")
                if data:
                    weakness.extend([type_info['type']['name'] for type_info in data['damage_relations']['double_damage_from']])
            return list(set(weakness))
        return None

    def get_advantage(self, pokemon: str) -> List[str]:
        """
        Method to get the advantage types of a specific Pokémon.
        """
        types = self.get_pokemon_type(pokemon)
        if types:
            advantage = []
            for type_ in types:
                data = self.get_request(f"type/{type_}")
                if data:
                    advantage.extend([type_info['type']['name'] for type_info in data['damage_relations']['double_damage_to']])
            return list(set(advantage))
        return None

    def basic_info(self, pokemon: str) -> int:
        """
        Method to display basic information about a specific Pokémon.
        """
        types = self.get_pokemon_type(pokemon)  # Get the type(s) of the Pokémon
        if types:
            print(f"{pokemon.capitalize()} is of type {', '.join(types)}")  # Print the Pokémon's type(s)
            print(f"{pokemon.capitalize()} is resistant to {', '.join(self.get_resistance(pokemon))}")  # Print the Pokémon's resistance types
            print(f"{pokemon.capitalize()} is weak against {', '.join(self.get_weakness(pokemon))}")  # Print the Pokémon's weakness types
            print(f"{pokemon.capitalize()} has advantage against {', '.join(self.get_advantage(pokemon))}")  # Print the Pokémon's advantage types
            return 1
        else:
            print("The Pokémon was not found.")
            return 0

    def save_pokemon(self, pokemon: str) -> None:
        """
        Method to save a Pokémon's details to a CSV file.
        """
        # Get the DataFrame from cache or file
        df = self.read_csv('pokemons.csv')

        # Create a dictionary with the Pokémon details
        data = [{
            'name': pokemon, 
            'type': ', '.join(self.get_pokemon_type(pokemon)), 
            'weakness': ', '.join(self.get_weakness(pokemon)), 
            'resistance': ', '.join(self.get_resistance(pokemon)), 
            'advantage': ', '.join(self.get_advantage(pokemon))
        }]

        # Append the dictionary to the DataFrame and save to file
        df = df.append(data, ignore_index=True)
        self.write_csv('pokemons.csv', df)

    def get_pokemon_stats(self, name: str) -> None:
        """
        Method to create a csv file with the pokemon stats.
        """
        # Get the detailed information of the Pokémon
        data = self.get_request(f"pokemon/{name.lower()}")

        if data:
            # Get the DataFrame from cache or file
            df = self.read_csv('pokemons_stats.csv')

            # Create a dictionary with the Pokémon details
            data = [{
                'name': name, 
                'hp': data['stats'][0]['base_stat'], 
                'attack': data['stats'][1]['base_stat'], 
                'defense': data['stats'][2]['base_stat'], 
                'special_attack': data['stats'][3]['base_stat'], 
                'special_defense': data['stats'][4]['base_stat'], 
                'speed': data['stats'][5]['base_stat']
            }]

            # Append the dictionary to the DataFrame and save to file
            df = df.append(data, ignore_index=True)
            self.write_csv('pokemons_stats.csv', df)
        else:
            print("The Pokémon was not found.")

    def plot_pokemon_stats(self, name: str) -> None:
        """
        Method to plot the stats of a Pokémon.
        """
        # Get the DataFrame from cache or file
        df = self.read_csv('pokemons_stats.csv')

        if name in df['name'].values:
            # Select the Pokémon's data
            pokemon_data = df[df['name'] == name]

            # Plot the stats
            fig = go.Figure(data=[
                go.Bar(name=name, x=list(pokemon_data.columns[1:]), y=pokemon_data.values[0, 1:])
            ])
            fig.update_layout(barmode='group')
            fig.show()
        else:
            print("The Pokémon was not found.")

def clear_csv():
    """
    Function to delete the CSV file.
    """
    try:
        os.remove('pokemons.csv')#Remove the file
        os.remove('pokemons_stats.csv')#Remove the file
        os.remove('types.csv')#Remove the file

        print("The CSV file was cleared successfully.")#Print a message
    except FileNotFoundError:#If the file was not found
        print("The CSV file does not exist.")#Print a message
        return None

def clear():
    """
    Function to clear the console screen.
    """
    input("Press enter to continue...")  # Wait for user input
    os.system('cls')  # Clear the console screen    

def menu():
    """
    Function to display the main menu of the Pokedex application.
    """
    print("Welcome to the Pokedex")
    print("1. Register Pokémon")
    print("2. View all Pokémon")
    print("3. Stats of all Pokémon")
    print("4. Clear files")
    print("5. Exit")
    option = input("Enter an option: ")  # Prompt the user to enter an option
    return option

Api = PokemonGo()  # Create an instance of the PokemonGo class

while True:
    Api.createtypesdata()  # Create the types data if it doesn't exist
    option = menu()  # Display the main menu and get the user's option
    if option == "1":  # If the user selects option 1
        pokemon = input("Enter the Pokémon's name: ").lower()  # Prompt the user to enter a Pokémon name
        clear()  # Clear the console screen
        control = Api.basic_info(pokemon)  # Display basic information about the Pokémon
        if control == 1:  # If the Pokémon was not found
            Api.save_pokemon(pokemon)  # Save the Pokémon's details to the CSV file
            Api.get_pokemon_stats(pokemon)  # Get the Pokémon's detailed information
            Api.show_pokemon_stats_graph(pokemon)  # Show the bar graph of the Pokémon's statistics
        else:
            pass
        clear()  # Clear the console screen

    elif option == "2":  # If the user selects option 2
        try:
            os.system('cls')  # Clear the console screen
            df = pd.read_csv('pokemons.csv')  # Read the Pokémon data from the CSV file
            print(df)  # Print the DataFrame
            clear()  # Clear the console screen
        except FileNotFoundError:
            print("You have not registered pokemons yet.")
            clear()  # Clear the console screen

    elif option == "3":  # If the user selects option 3
        Api.all_pokemon_stats()  # Show the bar graph of the statistics of all Pokémon
        clear()  # Clear the console screen

    elif option == "4":  # If the user selects option 4
        clear_csv()  # Clear the CSV file
        clear()  # Clear the console screen

    elif option == "5":  # If the user selects option 3
        break  # Exit the program

    else:
        print("Invalid option")  # If the user enters an invalid option
        clear()  # Clear the console screen