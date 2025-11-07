import requests

class Pokemon:
    def __init__(self, pokemon_number):
        self.pokemon_number = pokemon_number
        self.name = None
        self.image = None
        self.height = None
        self.weight = None
        self.types = []
        self.update_data()  # сразу загружаем данные при создании

    def update_data(self):
        """Обновляет данные покемона через API"""
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            self.name = data['forms'][0]['name']
            self.image = data['sprites']['front_default']
            self.height = data['height']
            self.weight = data['weight']
            self.types = [t['type']['name'] for t in data['types']]
        else:
            # Данные по умолчанию, если API недоступен
            self.name = "pikachu"
            self.image = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/25.png"
            self.height = 4
            self.weight = 60
            self.types = ["electric"]

    def get_name(self):
        return self.name

    def get_img(self):
        return self.image

    def get_height(self):
        return self.height

    def get_weight(self):
        return self.weight

    def get_types(self):
        return self.types

    def update_pokemon(self, new_number):
        """Изменяет номер покемона и обновляет все данные"""
        self.pokemon_number = new_number
        self.update_data()