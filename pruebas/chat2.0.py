import requests
import pandas as pd
import datetime
import os
import plotly.graph_objects as go

def clear():
    input("Presione enter para continuar...")
    os.system('clear')

class PokemonGo():
    def __init__(self):
        self.url = 'https://pokeapi.co/api/v2/'

    def createtypesdata(self):
        try:
            pd.read_csv('tipos.csv')
        except FileNotFoundError:
            self.fetch_and_save_types_data()

    def fetch_and_save_types_data(self):
        try:
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

                    if tipo['name'] not in ["unknown", "shadow"]:
                        tipos.append({'Tipo': tipo['name'], 'Debilidades': debilidades, 'Resistencias': resistencias, 'Ventaja': ventaja})

                df = pd.DataFrame(tipos)
                df.to_csv('tipos.csv', index=False)
        except requests.exceptions.RequestException as e:
            print(f"Hubo un problema al obtener los datos: {e}")
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
                print("El pokemon no se encontró.")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Hubo un problema al obtener los datos: {e}")
            return None

    def get_pokemon_type(self, pokemon):
        data = self.get_pokemon(pokemon)
        return data['types'][0]['type']['name'] if data else None

    def get_pokemon_data(self, pokemon):
        try:
            tipo = self.get_pokemon_type(pokemon)
            df = pd.read_csv('tipos.csv')
            df = df[df['Tipo'] == tipo]
            return df
        except FileNotFoundError:
            print("No se encontró el archivo 'tipos.csv'")
            return pd.DataFrame()

    def get_weakness(self, pokemon):
        df = self.get_pokemon_data(pokemon)
        return df['Debilidades'].values[0] if not df.empty else None

    def get_resistance(self, pokemon):
        df = self.get_pokemon_data(pokemon)
        return df['Resistencias'].values[0] if not df.empty else None

    def get_advantage(self, pokemon):
        df = self.get_pokemon_data(pokemon)
        return df['Ventaja'].values[0] if not df.empty else None

    def basic_info(self, pokemon):
        tipo = self.get_pokemon_type(pokemon)
        df = self.get_pokemon_data(pokemon)
        if df.empty:
            print("No se encontró el Pokémon.")
            return
        print(f"{pokemon} es de tipo {tipo}")
        print(f"{pokemon} es resistente a {df['Resistencias'].values[0]}")
        print(f"{pokemon} es débil contra {df['Debilidades'].values[0]}")
        print(f"{pokemon} tiene ventaja contra {df['Ventaja'].values[0]}")

    def save_pokemon(self, pokemon):
        df = pd.DataFrame(columns=['nombre', 'tipo', 'debilidad', 'resistencia', 'ventaja'])
        try:
            df = pd.read_csv('pokemons.csv')
        except FileNotFoundError:
            df.to_csv('pokemons.csv', index=False)
        
        data = [{'nombre': pokemon, 'tipo': self.get_pokemon_type(pokemon), 'debilidad': self.get_weakness(pokemon), 'resistencia': self.get_resistance(pokemon), 'ventaja': self.get_advantage(pokemon)}]
        df = df.append(data, ignore_index=True)
        df.to_csv('pokemons.csv', index=False)
    
    def obtener_info_pokemon(self, nombre):
        try:
            url = f"{self.url}pokemon/{nombre.lower()}"
            response = requests.get(url)
            self.log_requests(response)
            if response.status_code == 200:
                data = response.json()
                stats = {stat['stat']['name']: stat['base_stat'] for stat in data['stats']}
                return stats
            else:
                print(f"No se encontró información para el Pokémon {nombre.capitalize()}.")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Hubo un problema al obtener los datos: {e}")
            return None

    def mostrar_grafica_estadisticas_pokemon(self, nombre):
        info_pokemon = self.obtener_info_pokemon(nombre)
        if info_pokemon:
            stats = info_pokemon

            # Graficar estadísticas
            stats_fig = go.Figure(data=[go.Bar(x=list(stats.keys()), y=list(stats.values()))])
            stats_fig.update_layout(title=f"Estadísticas de {nombre.capitalize()}",
                                    xaxis_title="Estadística",
                                    yaxis_title="Valor")
            stats_fig.show()
        else:
            print(f"No se encontró información para el Pokémon {nombre.capitalize()}.")

Api = PokemonGo()

def menu():
    print("Bienvenido a la Pokedex")
    print("1. Buscar Pokémon")
    print("2. Ver todos los Pokémon")
    print("3. Salir")
    opcion = input("Ingrese una opción: ")
    return opcion

while True:
    Api.createtypesdata()
    opcion = menu()
    if opcion == "1":
        pokemon = input("Ingrese el nombre del Pokémon: ")
        clear()
        Api.basic_info(pokemon)
        Api.save_pokemon(pokemon)
        Api.mostrar_grafica_estadisticas_pokemon(pokemon)
    elif opcion == "2":
        try:
            df = pd.read_csv('pokemons.csv')
            print(df)
            clear()
        except FileNotFoundError:
            print("No se encontró el archivo 'pokemons.csv'.")
            clear()
    elif opcion == "3":
        break
    else:
        print("Opción inválida")
