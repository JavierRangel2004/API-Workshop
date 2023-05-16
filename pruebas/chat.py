import requests
import pandas as pd
import datetime
import os

def clear():
    input("Presione enter para continuar...")
    os.system('clear')

class PokemonGo():
    def __init__(self):
        self.url = 'https://pokeapi.co/api/v2/'

    def createtypesdata(self):
        try:
            pd.read_csv('tipos.csv')
            return
        except FileNotFoundError:
            pass

        response = requests.get(self.url + 'type')
        self.log_requests(response)
        
        if response.status_code == 200:
            data = response.json()
            tipos = []
            
            for tipo in data['results']:
                tipo_url = tipo['url']
                tipo_response = requests.get(tipo_url)
                self.log_requests(tipo_response)
                tipo_data = tipo_response.json()

                debilidades = [d['name'] for d in tipo_data['damage_relations']['double_damage_from']]
                resistencias = [r['name'] for r in tipo_data['damage_relations']['half_damage_from']]
                ventaja = [v['name'] for v in tipo_data['damage_relations']['double_damage_to']]
                
                if tipo['name'] == "unknown" or tipo['name'] == "shadow":
                    continue
                else:
                    tipos.append({'Tipo': tipo['name'], 'Debilidades': debilidades, 'Resistencias': resistencias, 'Ventaja': ventaja})
                    
            df = pd.DataFrame(tipos)
            df.to_csv('tipos.csv', index=False)
        else:
            return None

    def log_requests(self, response):
        with open('log.txt', 'a') as f:
            f.write(f"{datetime.datetime.now()} - {response.url} - {response.status_code}\n")

    def get_pokemon(self, pokemon):
        url = self.url + 'pokemon/' + pokemon
        response = requests.get(url)
        self.log_requests(response)
        
        if response.status_code == 200:
            return response.json()
        else:
            return None
        
    def get_pokemon_type(self, pokemon):
        url = self.url + 'pokemon/' + pokemon
        response = requests.get(url)
        self.log_requests(response)
        
        if response.status_code == 200:
            return response.json()['types'][0]['type']['name']
        else:
            return None
        
    def get_pokemon_data(self, pokemon):
        tipo = self.get_pokemon_type(pokemon)
        df = pd.read_csv('tipos.csv')
        df = df[df['Tipo'] == tipo]
        return df

    def get_weakness(self, pokemon):
        
        df = self.get_pokemon_data(pokemon)
        return df['Debilidades'].values[0]

    def get_resistance(self, pokemon):
        df = self.get_pokemon_data(pokemon)
        return df['Resistencias'].values[0]

    def get_advantage(self, pokemon):
        df = self.get_pokemon_data(pokemon)
        return df['Ventaja'].values[0]

    def basic_info(self, pokemon):
        tipo = self.get_pokemon_type(pokemon)
        df = self.get_pokemon_data(pokemon)
        if df.empty:
            print("No se encontro el pokemon")
            return
        print(f"{pokemon} es de tipo {tipo}")
        print(f"{pokemon} es resistente a {df['Resistencias'].values[0]}")
        print(f"{pokemon} es debil contra {df['Debilidades'].values[0]}")
        print(f"{pokemon} tiene ventaja contra {df['Ventaja'].values[0]}")

    def save_pokemon(self, pokemon):
        df = pd.DataFrame(columns=['nombre', 'tipo', 'debilidad', 'resistencia', 'ventaja'])
        try:
            pd.read_csv('pokemons.csv')
            data = [{'nombre': pokemon, 'tipo': self.get_pokemon_type(pokemon), 'debilidad': self.get_weakness(pokemon), 'resistencia': self.get_resistance(pokemon), 'ventaja': self.get_advantage(pokemon)}]
            df = pd.DataFrame(data)
            df.to_csv('pokemons.csv', mode='a', header=False, index=False)
        except FileNotFoundError:
            df = pd.DataFrame(columns=['nombre', 'tipo', 'debilidad', 'resistencia', 'ventaja'])
            df.to_csv('pokemons.csv', index=False)
            data = [{'nombre': pokemon, 'tipo': self.get_pokemon_type(pokemon), 'debilidad': self.get_weakness(pokemon), 'resistencia': self.get_resistance(pokemon), 'ventaja': self.get_advantage(pokemon)}]
            df = pd.DataFrame(data)
            df.to_csv('pokemons.csv', mode='a', header=False, index=False)


Api = PokemonGo()

def menu():
    print("Bienvenido a la Pokedex")
    print("1. Buscar Pokemon")
    print("2. Ver todos los pokemons")
    print("3. Salir")
    opcion = input("Ingrese una opcion: ")
    return opcion

while True:
    Api.createtypesdata()
    opcion = menu()
    if opcion == "1":
        pokemon = input("Ingrese el nombre del pokemon: ")
        clear()
        Api.basic_info(pokemon)
        Api.save_pokemon(pokemon)
    elif opcion == "2":
        df = pd.read_csv('pokemons.csv')
        print(df)
        clear()
    elif opcion == "3":
        break
    else:
        print("Opcion invalida")
        continue