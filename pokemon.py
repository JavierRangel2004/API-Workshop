import requests  # Importing the requests library for making HTTP requests
import pandas as pd  # Importing the pandas library for data manipulation and analysis
import datetime  # Importing the datetime module for working with dates and times
import plotly.graph_objects as go  # Importing the graph_objects module from the plotly library for creating interactive visualizations

class PokemonGo():
    """
    Class representing the PokemonGo application.
    """

    def __init__(self):
        """
        Constructor method to initialize the PokemonGo object.
        """
        self.url = 'https://pokeapi.co/api/v2/'  # Base URL for the Pokemon API

    def log_requests(self, response):
        """
        Method to log the HTTP requests made by the application.
        """
        with open('log.txt', 'a') as f:  # Open the log.txt file in append mode
            f.write(f"{datetime.datetime.now()} - {response.url} - {response.status_code}\n")  # Write the request details to the log file

    def fetch_and_save_types_data(self):
        """
        Method to fetch and save the Pokemon type data from the API.
        """
        try:
            response = requests.get(self.url + 'type')  # Send a GET request to the API to fetch the type data
            self.log_requests(response)  # Log the request

            if response.status_code == 200:  # If the request is successful
                data = response.json()  # Convert the response to JSON format
                types = []
                for type in data['results']:
                    type_url = type['url']
                    type_response = requests.get(type_url)  # Send a GET request to fetch the details of a specific type
                    self.log_requests(type_response)  # Log the request
                    type_data = type_response.json()  # Convert the response to JSON format

                    weaknesses = [d['name'] for d in type_data['damage_relations']['double_damage_from']]  # Extract the weakness types
                    resistances = [r['name'] for r in type_data['damage_relations']['half_damage_from']]  # Extract the resistance types
                    advantages = [v['name'] for v in type_data['damage_relations']['double_damage_to']]  # Extract the advantage types

                    if type['name'] not in ["unknown", "shadow"]:
                        types.append({'Type': type['name'], 'Weaknesses': weaknesses, 'Resistances': resistances, 'Advantages': advantages})  # Append the type data to the list

                df = pd.DataFrame(types)  # Create a DataFrame from the type data
                df.to_csv('types.csv', index=False)  # Save the DataFrame to a CSV file
        except requests.exceptions.RequestException as e:
            print(f"There was a problem obtaining the data: {e}")
            return None

    def createtypesdata(self):
        """
        Method to create the types data if it doesn't already exist.
        """
        try:
            pd.read_csv('types.csv')  # Try to read the types data from the CSV file
        except FileNotFoundError:
            self.fetch_and_save_types_data()  # Fetch and save the types data if the file doesn't exist

    def get_pokemon(self, pokemon):
        """
        Method to get the details of a specific Pokémon from the API.
        """
        try:
            url = self.url + 'pokemon/' + pokemon
            response = requests.get(url)  # Send a GET request to fetch the details of the Pokémon
            self.log_requests(response)  # Log the request

            if response.status_code == 200:  # If the request is successful
                return response.json()  # Convert the response to JSON format and return it
            else:
                return None
        except requests.exceptions.RequestException as e:
            print(f"There was a problem obtaining the data: {e}")
            return None

    def get_pokemon_image(self, pokemon):
        """
        Method to get the image of a specific Pokémon.
        """
        try:
            data = self.get_pokemon(pokemon)  # Get the Pokémon data
            try:
                image = data['sprites']['front_default'] if data else None  # Extract the image URL from the data if it exists, otherwise return None
                return image
            except KeyError:
                return None
        except TypeError:
            return None

    def get_pokemon_type(self, pokemon):
        """
        Method to get the type(s) of a specific Pokémon.
        """
        try:
            data = self.get_pokemon(pokemon)  # Get the Pokémon data
            try:
                types = [type_info['type']['name'] for type_info in data['types']] if data else None  # Extract the type(s) from the data if it exists, otherwise return None
                return types
            except KeyError:
                return None
        except TypeError:
            return None
        
    def get_pokemon_data(self, pokemon):
        """
        Method to get the data of a specific Pokémon from the CSV file.
        """
        try:
            types = self.get_pokemon_type(pokemon)  # Get the type(s) of the Pokémon
            df = pd.read_csv('types.csv')  # Read the types data from the CSV file

            if len(types)==1:  # If the Pokémon has only one type
                df = df[df['Type'] == types[0]]  # Filter the DataFrame to include only the rows with the matching type
            else:  # If the Pokémon has two types
                df1 = df[df['Type'] == types[0]]  # Filter the DataFrame to include only the rows with the first type
                df2 = df[df['Type'] == types[1]]  # Filter the DataFrame to include only the rows with the second type
                df = pd.concat([df1, df2])  # Concatenate the two DataFrames
            return df  # Return the filtered DataFrame
        except FileNotFoundError:
            print("The file 'types.csv' was not found.")
            return pd.DataFrame()  # Return an empty DataFrame if the file doesn't exist

    def get_weakness_and_resistance(self, pokemon):
        """
        Method to get the weakness and resistance types of a specific Pokémon.
        """
        df = self.get_pokemon_data(pokemon)  # Get the Pokémon data
        if not df.empty:  # If the DataFrame is not empty
            # Concatenate and deduplicate weakness and resistance lists
            weakness = set()
            resistance = set()
            for w, r in zip(df['Weaknesses'].values, df['Resistances'].values):
                # convert string representation of list to actual list
                w = w.strip("[]").replace("'", "").split(", ")
                r = r.strip("[]").replace("'", "").split(", ")
                weakness.update(w)
                resistance.update(r)
            # Remove any weaknesses that are also resistances
            neutral_weakness = weakness.intersection(resistance)
            weakness = weakness.difference(neutral_weakness)
            resistance = resistance.difference(neutral_weakness)
            return sorted(list(weakness)), sorted(list(resistance))  # Return sorted weakness and resistance lists
        else:
            return None, None

    def get_weakness(self, pokemon):
        """
        Method to get the weakness types of a specific Pokémon.
        """
        weakness, _ = self.get_weakness_and_resistance(pokemon)  # Get the weakness and resistance types
        return weakness

    def get_resistance(self, pokemon):
        """
        Method to get the resistance types of a specific Pokémon.
        """
        _, resistance = self.get_weakness_and_resistance(pokemon)  # Get the weakness and resistance types
        return resistance

    def get_advantage(self, pokemon):
        """
        Method to get the advantage types of a specific Pokémon.
        """
        df = self.get_pokemon_data(pokemon)  # Get the Pokémon data
        if not df.empty:  # If the DataFrame is not empty
            # Concatenate and deduplicate advantage lists
            advantage = set()
            for a in df['Advantages'].values:
                # convert string representation of list to actual list
                a = a.strip("[]").replace("'", "").split(", ")
                advantage.update(a)
            return sorted(list(advantage))  # Return sorted advantage list
        else:
            return None

    def basic_info(self, pokemon):
        """
        Method to display basic information about a specific Pokémon.
        """
        types = self.get_pokemon_type(pokemon)  # Get the type(s) of the Pokémon
        if types:
            return {
                "notFound": False,
                "type": types,
                "resistant": self.get_resistance(pokemon),
                "weaknesses": self.get_weakness(pokemon),
                "advantages": self.get_advantage(pokemon)
            }
        else:
            return {
                "notFound": True
            }

    def pokemon_already_saved(self, pokemon):
        """
        Method to check if a Pokémon's details are already saved in the CSV file.
        """
        df = pd.DataFrame(columns=['name', 'type', 'weakness', 'resistance', 'advantage'])
        try:
            df = pd.read_csv('pokemons.csv')  # Try to read the Pokémon data from the CSV file
        except FileNotFoundError:
            pass
        return pokemon in df['name'].values  # Return True if the Pokémon is already saved, otherwise return False

    def save_pokemon(self, pokemon):
        """
        Method to save a Pokémon's details to a CSV file.
        """
        df = pd.DataFrame(columns=['name', 'type', 'weakness', 'resistance', 'advantage'])  # Create an empty DataFrame with the specified columns
        try:
            df = pd.read_csv('pokemons.csv')  # Try to read the Pokémon data from the CSV file
        except FileNotFoundError:
            df.to_csv('pokemons.csv', index=False)  # If the file doesn't exist, create a new CSV file with the DataFrame structure
        try:
            data = [{'name': pokemon, 'type': ', '.join(self.get_pokemon_type(pokemon)), 'weakness': ', '.join(self.get_weakness(pokemon)), 'resistance': ', '.join(self.get_resistance(pokemon)), 'advantage': ', '.join(self.get_advantage(pokemon))}]  # Create a dictionary with the Pokémon details
            df = df.append(data, ignore_index=True)  # Append the dictionary to the DataFrame
            df.to_csv('pokemons.csv', index=False)  # Save the DataFrame to the CSV file
        except:
            print("The Pokémon was not found.")

    def get_pokemon_stats(self, name):
        """
        Method to create a csv file with the pokemon stats.
        """
        try:
            url = f"{self.url}pokemon/{name.lower()}"
            response = requests.get(url)  # Send a GET request to fetch the detailed information of the Pokémon
            self.log_requests(response)  # Log the request
            if response.status_code == 200:  # If the request is successful 
                df = pd.DataFrame(columns=['name', 'hp', 'attack', 'defense', 'special_attack', 'special_defense', 'speed'])  # Create an empty DataFrame with the specified columns
                try:
                    df = pd.read_csv('pokemons_stats.csv')  # Try to read the Pokémon data from the CSV file
                except FileNotFoundError:
                    df.to_csv('pokemons_stats.csv', index=False)
                data = [{'name': name, 'hp': response.json()['stats'][0]['base_stat'], 'attack': response.json()['stats'][1]['base_stat'], 'defense': response.json()['stats'][2]['base_stat'], 'special_attack': response.json()['stats'][3]['base_stat'], 'special_defense': response.json()['stats'][4]['base_stat'], 'speed': response.json()['stats'][5]['base_stat']}]  # Create a dictionary with the Pokémon details
                df = df.append(data, ignore_index=True)  # Append the dictionary to the DataFrame
                df.to_csv('pokemons_stats.csv', index=False)  # Save the DataFrame to the CSV file

            else:
                print(f"No information was found for the Pokémon {name.capitalize()}.")
                return None
        except requests.exceptions.RequestException as e:
            print(f"There was a problem obtaining the data: {e}")
            return None
        
    def get_pokemon_info(self, name):
        """
        Method to get the pokemon stats.
        """
        try:
            url = f"{self.url}pokemon/{name.lower()}"#Get the url of the pokemon
            response = requests.get(url)#Get the pokemon data
            self.log_requests(response)#Log the request
            if response.status_code == 200:#If the pokemon was found
                data = response.json()#Get the pokemon data
                stats = {stat['stat']['name']: stat['base_stat'] for stat in data['stats']}#Get the pokemon stats
                return stats#Return the pokemon stats
            else:
                print(f"No information was found for the Pokémon {name.capitalize()}.")#Print a message if the pokemon was not found
                return None#Return None
        except requests.exceptions.RequestException as e:#If there was an error
            print(f"There was a problem obtaining the data: {e}")#Print the error
            return None#Return None

    def show_pokemon_stats_graph(self, name):
        """
        Method to show a bar graph of the statistics of a specific Pokémon.
        """
        pokemon_info = self.get_pokemon_info(name)  # Get the detailed information of the Pokémon
        if pokemon_info:
            stats = pokemon_info  # Get the stats of the Pokémon
            # Plot stats
            stats_fig = go.Figure(data=[go.Bar(x=list(stats.keys()), y=list(stats.values()))])  # Create a bar graph using plotly
            stats_fig.update_layout(title=f"{name.capitalize()}'s Statistics",
                                    xaxis_title="Statistic",
                                    yaxis_title="Value")
            stats_fig.show()  # Show the bar graph
        else:
            print(f"No information was found for the Pokémon {name.capitalize()}.")
    
    def all_pokemon_stats(self):
        """
        Method to show a bar graph of the statistics of all Pokémon sort by highest total stats.
        """
        try:
            df= pd.read_csv('pokemons_stats.csv')  # Try to read the Pokémon data from the CSV file
            total = df['hp'] + df['attack'] + df['defense'] + df['special_attack'] + df['special_defense'] + df['speed']  # Calculate the total stats of each Pokémon
            df['total'] = total
            df = df.sort_values(by=['total'], ascending=False)#sort the total stats from highest to lowest
            df.to_csv('pokemons_stats.csv', index=False)  # Save the DataFrame to the CSV file
            df = pd.read_csv('pokemons_stats.csv')  # Try to read the Pokémon data from the CSV file
            total = df['total']#Get the total stats
            stats_fig = go.Figure(data=[go.Bar(x=df['name'], y=total)])  # Create a bar graph using plotly
            stats_fig.update_layout(title="Your Pokémon team Statistics",#set the title and axis labels
                                    xaxis_title="Pokémon",
                                    yaxis_title="Total Stats")
            stats_fig.show()  # Show the bar graph
        except FileNotFoundError:#If the file was not found
            print("No Pokémon data was found.")#Print a message
            return None

Api = PokemonGo()
Api.createtypesdata()  # Create the types data if it doesn't exist