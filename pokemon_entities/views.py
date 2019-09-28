import folium
import json

from django.http import HttpResponseNotFound
from django.shortcuts import render
from .models import PokemonEntity
from .models import Pokemon

MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = 'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832&fill=transparent'


def add_pokemon(folium_map, lat, lon, name, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        tooltip=name,
        icon=icon,
    ).add_to(folium_map)

def get_image_url_or_default(request, path_to_search_image):
    try:
        img_url = request.build_absolute_uri(path_to_search_image.url)
    except Exception:
        img_url = DEFAULT_IMAGE_URL
    return img_url

def show_all_pokemons(request):
    pokemon_entities = PokemonEntity.objects.all().select_related('pokemon')

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemon_entities:
        img_url = get_image_url_or_default(request, pokemon_entity.pokemon.image)
        add_pokemon(
            folium_map, pokemon_entity.lat, pokemon_entity.lon,
            pokemon_entity.pokemon.title, img_url)

    pokemons_on_page = []
    pokemons = Pokemon.objects.all()
    for pokemon in pokemons:
        img_url  = get_image_url_or_default(request, pokemon.image)
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': img_url,
            'title_ru': pokemon.title,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })

def show_pokemon(request, pokemon_id):
    requested_pokemon = Pokemon.objects.get(id=int(pokemon_id))
    if not requested_pokemon:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')
        
    img_url = get_image_url_or_default(request, requested_pokemon.image)
    requested_pokemon_entities = PokemonEntity.objects.filter(pokemon=requested_pokemon)
    
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in requested_pokemon_entities:
        add_pokemon(
            folium_map, pokemon_entity.lat, pokemon_entity.lon,
            requested_pokemon.title, img_url)  

    pokemon = {
        'title_ru': requested_pokemon.title,
        'title_en': requested_pokemon.title_en,
        'title_jp': requested_pokemon.title_jp,
        'description': requested_pokemon.description,
        'img_url': img_url,
    }
    if requested_pokemon.next_evolution:
        pokemon['next_evolution'] = {
                'title_ru': requested_pokemon.next_evolution.title,
                'pokemon_id': requested_pokemon.next_evolution.id,
                'img_url': get_image_url_or_default(request, requested_pokemon.next_evolution.image),
        }
    if requested_pokemon.previous_evolution:
        pokemon['previous_evolution'] = {
                'title_ru': requested_pokemon.previous_evolution.title,
                'pokemon_id': requested_pokemon.previous_evolution.id,
                'img_url': get_image_url_or_default(request, requested_pokemon.previous_evolution.image),
        }

    return render(request, 'pokemon.html', context={'map': folium_map._repr_html_(),
                                                    'pokemon': pokemon})
