from . import bp as pokemon
from flask import render_template, request, flash, redirect, url_for
import requests

@pokemon.route('/search', methods=['GET', 'POST'])
def search():
    if request.method =='POST':
        poke = request.form.get("search")
        url = f'https://pokeapi.co/api/v2/pokemon/{poke}'
        response = requests.get(url)
        if not response.ok:
            error_string = "We had an Unexpected Error"
            return render_template('pokemon.html.j2', error = error_string)
        if not response.json():
            error_string = "That's Not A Pokmeon. Please Try Again"
            return render_template('pokemon.html.j2', error = error_string)
        data = response.json()
        poke_dict={
            "name":data['name'],
            "ability":data['abilities'][0]['ability']['name'],
            "defense":data['stats'][2]['base_stat'],
            "attack":data['stats'][1]['base_stat'],
            "HP":data['stats'][0]['base_stat'],
            "sprite":data['sprites']['front_shiny']
        }
        return render_template('pokemon.html.j2', poke=poke_dict)

    return render_template('pokemon.html.j2')

@pokemon.route('/my_pokemon')
def my_pokemon():
    return render_template('my_pokemon.html.j2')