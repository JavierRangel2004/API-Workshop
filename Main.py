import requests
import pandas as pd

class PokeAPi():
    def __init__(self):
        self.url = 'https://pokeapi.co/api/v2/'

    def get_pokemon(self, pokemon):
        url = self.url + 'pokemon/' + pokemon
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return None
        
    def get_pokemon_evolution(self, pokemon):
        url = self.url + 'pokemon-species/' + pokemon
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return None
        
    def get_pokemon_evolution_chain(self, pokemon):
        url = self.url + 'evolution-chain/' + pokemon
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return None
        
    def get_pokemon_habitat(self, pokemon):
        url = self.url + 'pokemon-habitat/' + pokemon
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return None

Api= PokeAPi()
Api.get_pokemon('pikachu')
Api.get_pokemon_evolution('pikachu')
Api.get_pokemon_evolution_chain('pikachu')
Api.get_pokemon_habitat('pikachu')
