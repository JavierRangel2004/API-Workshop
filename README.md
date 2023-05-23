# API-Workshop


<h1 align="center">🔥 PokémonGo - A Pokémon Analyzer and Tracker 🔥</h1>

<div align="center">
  <img src="https://upload.wikimedia.org/wikipedia/commons/9/98/International_Pokémon_logo.svg" width="300" height="150">
</div>

<div align="center">
    <p>
    PokémonGo is a Python-based web application that uses the <a href="https://pokeapi.co/">PokéAPI</a> to fetch data about different Pokémon and store it locally for future use and analysis. The tool is also capable of displaying the fetched data in different ways including graphically.
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
   git clone https://github.com/JavierRangel2004/API-Workshop.git
   ```
2. Navigate into the cloned directory:
   ```bash
   cd API-Workshop
   ```
3. Make sure you have the required Python packages installed. You can install them via pip:
   ```bash
   pip install flask pandas plotly requests
   ```

<h2 id="usage"> ⚙️ Usage ⚙️ </h2>

To start using PokémonGo, run the `flask run` command in the root directory of the project:

```bash
flask run
```

This will start the web application and provide a link to access the web interface (usually `http://127.0.0.1:5000` or `http://localhost:5000`).

<h2 id="features"> 🌟 Features 🌟 </h2>

Here are the main functionalities of PokémonGo:

1. **Register Pokémon**: By entering the name of the Pokémon, it fetches its data from the PokéAPI, shows basic information such as type, resistance, weakness, advantage and saves it in a local CSV file. It also retrieves the Pokémon's stats, saves them, and presents them in a bar graph.

2. **View all Pokémon**: Displays all the Pokémon that you have registered so far, reading from the local CSV file.

3. **Stats of all Pokémon**: Shows a bar graph of the statistics of all registered Pokémon, sorted by highest total stats.

4. **Clear files**: Deletes all the locally stored CSV files containing Pokémon data.

<h2 id="future-enhancements"> 💡 Future Enhancements 💡 </h2>

- Add a function to compare two or more Pokémon.
- Improve error handling and user input validation.

<h2 id="contribution"> 🤝 Contribution 🤝 </h2>

Contributions are always welcome! Please feel free to submit a Pull Request. If you find any bugs/issues, please create an issue to discuss it.

---
**NOTE:** This application is a fan-made project and is not affiliated with the official Pokémon franchise. All Pokémon information and data are retrieved from [PokéAPI](https://pokeapi.co/).
```
