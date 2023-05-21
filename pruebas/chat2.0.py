import requests
import pandas as pd
import datetime
import os
import plotly.graph_objects as go

def clear():#Function to clear the console
    input("Press enter to continue...")#Wait for the user to press enter
    os.system('cls')#Clear the console

class PokemonGo():#Class to manage the pokemon api
    def __init__(self):
        self.url = 'https://pokeapi.co/api/v2/'#Url of the api

    def createtypesdata(self):#Function to create the types data
        try:
            pd.read_csv('types.csv')#Try to read the types data
        except FileNotFoundError:#If the file is not found
            self.fetch_and_save_types_data()#Call the function to create the types data

    def fetch_and_save_types_data(self):#Function to create the types data
        try:
            response = requests.get(self.url + 'type')#Get the types data
            self.log_requests(response)#Log the request

            if response.status_code == 200:#If the request was successful
                data = response.json()#Get the data
                types = []#Create a list to store the types data
                for type in data['results']:#For each type
                    type_url = type['url']#Get the url of the type
                    type_response = requests.get(type_url)#Get the type data
                    self.log_requests(type_response)#Log the request
                    type_data = type_response.json()#Get the data of the type

                    weaknesses = [d['name'] for d in type_data['damage_relations']['double_damage_from']]#Get the weaknesses of the type
                    resistances = [r['name'] for r in type_data['damage_relations']['half_damage_from']]#Get the resistances of the type
                    advantages = [v['name'] for v in type_data['damage_relations']['double_damage_to']]#Get the advantages of the type

                    if type['name'] not in ["unknown", "shadow"]:#If the type is not unknown or shadow
                        types.append({'Type': type['name'], 'Weaknesses': weaknesses, 'Resistances': resistances, 'Advantages': advantages})#Add the type to the list

                df = pd.DataFrame(types)#Create a dataframe with the types data
                df.to_csv('types.csv', index=False)#Save the types data in a csv file
        except requests.exceptions.RequestException as e:#If there was an error
            print(f"There was a problem obtaining the data: {e}")#Print the error
            return None#Return None

    def log_requests(self, response):#Function to log the requests
        with open('log.txt', 'a') as f:#Open the log file
            f.write(f"{datetime.datetime.now()} - {response.url} - {response.status_code}\n")#Write the request in the log file

    def get_pokemon(self, pokemon):#Function to get the pokemon
        try:#Try to get the pokemon data
            url = self.url + 'pokemon/' + pokemon#Get the url of the pokemon
            response = requests.get(url)#Get the pokemon data
            self.log_requests(response)#Log the request

            if response.status_code == 200:
                return response.json()#Return the pokemon data in json format
            else:
                print("The pokemon was not found.")#Print a message if the pokemon was not found
                return None
        except requests.exceptions.RequestException as e:#If there was an error
            print(f"There was a problem obtaining the data: {e}")#Print the error
            return None

    def get_pokemon_type(self, pokemon):#Function to get the pokemon type
        data = self.get_pokemon(pokemon)#Get the pokemon data

        return data['types'][0]['type']['name'] if data else None#Return the pokemon type

    def get_pokemon_data(self, pokemon):#Function to get the pokemon data
        try:
            type = self.get_pokemon_type(pokemon)#Get the pokemon type
            df = pd.read_csv('types.csv')#Read the types data
            df = df[df['Type'] == type]#Get the data of the pokemon type
            return df#Return the pokemon data
        except FileNotFoundError:#If the file types is not found
            print("The file 'types.csv' was not found.")#Print a message
            return pd.DataFrame()#Return an empty dataframe

    def get_weakness(self, pokemon):#Function to get the pokemon weakness
        df = self.get_pokemon_data(pokemon)#Get the pokemon data
        return df['Weaknesses'].values[0] if not df.empty else None#Return the pokemon weakness

    def get_resistance(self, pokemon):#Function to get the pokemon resistance
        df = self.get_pokemon_data(pokemon)
        return df['Resistances'].values[0] if not df.empty else None

    def get_advantage(self, pokemon):#Function to get the pokemon advantage
        df = self.get_pokemon_data(pokemon)
        return df['Advantages'].values[0] if not df.empty else None

    def basic_info(self, pokemon):#Function to get the basic info of the pokemon
        type = self.get_pokemon_type(pokemon)#Get the pokemon type
        df = self.get_pokemon_data(pokemon)#Get the pokemon data
        if df.empty: #If the pokemon data is empty
            print("The Pokémon was not found.")#Print that the pokemon was not found
            return  #Return None
        print(f"{pokemon} is of type {type}")#Print the pokemon type
        print(f"{pokemon} is resistant to {df['Resistances'].values[0]}")#Print the pokemon resistance
        print(f"{pokemon} is weak against {df['Weaknesses'].values[0]}")#Print the pokemon weakness
        print(f"{pokemon} has advantage against {df['Advantages'].values[0]}")#Print the pokemon advantage

    def save_pokemon(self, pokemon):#Function to save the pokemon in the csv file
        df = pd.DataFrame(columns=['name', 'type', 'weakness', 'resistance', 'advantage'])#Create a dataframe to store the pokemon data
        try:
            df = pd.read_csv('pokemons.csv')#Read the csv file
        except FileNotFoundError:#If the file is not found
            df.to_csv('pokemons.csv', index=False)#Create the file
        
        data = [{'name': pokemon, 'type': self.get_pokemon_type(pokemon), 'weakness': self.get_weakness(pokemon), 'resistance': self.get_resistance(pokemon), 'advantage': self.get_advantage(pokemon)}]#Create a dictionary with the pokemon data
        df = df.append(data, ignore_index=True)#Add the pokemon data to the dataframe
        df.to_csv('pokemons.csv', index=False)#Save the dataframe in the csv file
    
    def get_pokemon_info(self, name):#Function to get the pokemon info
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

    def show_pokemon_stats_graph(self, name):#Function to show the pokemon stats graph
        pokemon_info = self.get_pokemon_info(name)#Get the pokemon info
        if pokemon_info:#If the pokemon info is not None
            stats = pokemon_info#Get the pokemon stats

            # Plot stats
            stats_fig = go.Figure(data=[go.Bar(x=list(stats.keys()), y=list(stats.values()))])#Create the graph
            stats_fig.update_layout(title=f"{name.capitalize()}'s Statistics",
                                    xaxis_title="Statistic",
                                    yaxis_title="Value")#Add the title and labels
            stats_fig.show()#Show the graph
        else:
            print(f"No information was found for the Pokémon {name.capitalize()}.")#Print a message if the pokemon was not found

Api = PokemonGo()#Create an instance of the class

def menu():#Function to show the menu
    print("Welcome to the Pokedex")
    print("1. Search Pokémon")
    print("2. View all Pokémon")
    print("3. Exit")
    option = input("Enter an option: ")#Get the option
    return option#Return the option

while True:#While the user does not exit
    Api.createtypesdata()#Create the types data
    option = menu()#Show the menu
    if option == "1":#If the user wants to search a pokemon
        pokemon = input("Enter the Pokémon's name: ").lower()#Get the pokemon name
        clear()#Clear the console
        Api.basic_info(pokemon)#Show the pokemon info
        Api.save_pokemon(pokemon)#Save the pokemon in the csv file
        Api.show_pokemon_stats_graph(pokemon)#Show the pokemon stats graph
    elif option == "2":#If the user wants to see all the pokemons
        try:#Try to read the csv file
            df = pd.read_csv('pokemons.csv')#Read the csv file
            print(df)#Print the dataframe
            clear()#Clear the console
        except FileNotFoundError:#If the file is not found
            print("The file 'pokemons.csv' was not found.")#Print a message
            clear()#Clear the console
    elif option == "3":#If the user wants to exit
        break#Exit the program
    else:#If the user enters an invalid option
        print("Invalid option")#Tell the user that the option is invalid
        clear()#Clear the console