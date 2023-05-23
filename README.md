# API-Workshop


<h1 align="center">🔥 PokémonGo - A Pokémon Analyzer and Tracker 🔥</h1>

<div align="center">
  <img src="https://upload.wikimedia.org/wikipedia/commons/9/98/International_Pokémon_logo.svg" width="300" height="150">
</div>

<div align="center">
    <p>
    PokémonGo is a Python-based application that uses the <a href="https://pokeapi.co/">PokéAPI</a> to fetch data about different Pokémon and store it locally for future use and analysis. The tool is also capable of displaying the fetched data in different ways including graphically.
    </p>
</div>

## 🚀 Table of Contents 🚀

- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Future Enhancements](#future-enhancements)
- [Contribution](#contribution)

<h2 id="installation"> 🎈 Installation 🎈 </h2>

1. Clone the repository to your local machine using:
   ```bash
   git clone https://github.com/username/pokemongo.git
   ```
2. Navigate into the cloned directory:
   ```bash
   cd pokemongo
   ```
3. Make sure you have the required Python packages installed. You can install them via pip:
   ```bash
   pip install pandas plotly requests
   ```

<h2 id="usage"> ⚙️ Usage ⚙️ </h2>

To start using PokémonGo, run the `pokedex.py` script:

```bash
python pokedex.py
```

This will start the application and display the main menu with several options to interact with the Pokémon data.

Here is an example of what the menu looks like:

```
Welcome to the Pokedex
1. Register Pokémon
2. View all Pokémon
3. Stats of all Pokémon
4. Clear files
5. Exit
Enter an option:
```

<h2 id="features"> 🌟 Features 🌟 </h2>

Here are the main functionalities of PokémonGo:

1. **Register Pokémon**: By entering the name of the Pokémon, it fetches its data from the PokéAPI, shows basic information such as type, resistance, weakness, advantage and saves it in a local CSV file. It also retrieves the Pokémon's stats, saves them, and presents them in a bar graph.

2. **View all Pokémon**: Displays all the Pokémon that you have registered so far, reading from the local CSV file.

3. **Stats of all Pokémon**: Shows a bar graph of the statistics of all registered Pokémon, sorted by highest total stats.

4. **Clear files**: Deletes all the locally stored CSV files containing Pokémon data.

5. **Exit**: Quits the application.

<h2 id="future-enhancements"> 💡 Future Enhancements 💡 </h2>

- Integrate a GUI for easier interaction and better user experience.
- Add a function to compare two or more Pokémon.
- Improve error handling and user input validation.

<h2 id="contribution"> 🤝 Contribution 🤝 </h2>

Contributions are always welcome! Please feel free to submit a Pull Request. If you find any bugs/issues, please create an issue to discuss it.

---
**NOTE:** This application is a fan-made project and is not affiliated with the official Pokémon franchise. All Pokémon information and data are retrieved from [PokéAPI](https://pokeapi.co/).
```
