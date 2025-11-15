import random
import telebot
from random import randint, choice
from datetime import datetime, timedelta
import config  

bot = telebot.TeleBot(config.token)


class Pokemon:
    pokemons = {}

    def __init__(self, name, trainer):
        self.name = name
        self.pokemon_trainer = trainer
        self.hp = random.randint(50, 100)
        self.power = random.randint(10, 30)
        self.max_hp = 120
        self.pokemon_class = "Обычный"
        self.last_feed_time = datetime.min  # время последнего кормления

    def info(self):
        return f"Класс: {self.pokemon_class}\nПокемон: {self.name}, HP: {self.hp}, Сила: {self.power}"

    def win_bonus(self):
        hp_bonus = 15
        power_bonus = 10
        self.hp = min(self.hp + hp_bonus, self.max_hp)
        self.power = min(self.power + power_bonus, 50)
        return f"🏅 {self.name} получает бонус: +{hp_bonus} HP и +{power_bonus} силы!"

    def heal(self):
        heal_points = random.randint(10, 30)
        old_hp = self.hp
        self.hp = min(self.hp + heal_points, self.max_hp)
        restored = self.hp - old_hp
        return f"💚 {self.name} восстановил {restored} HP (текущее HP: {self.hp})"

    
    def feed(self, feed_interval=20, hp_increase=10):
        current_time = datetime.now()
        delta_time = timedelta(seconds=feed_interval)

        if (current_time - self.last_feed_time) >= delta_time:
            self.hp = min(self.hp + hp_increase, self.max_hp)
            self.last_feed_time = current_time
            return f"🍎 {self.name} поел и восстановил {hp_increase} HP! Текущее HP: {self.hp}"
        else:
            next_feed_time = self.last_feed_time + delta_time
            return f"⏳ Рано! Следующее кормление в: {next_feed_time.strftime('%H:%M:%S')}"

    def attack(self, enemy):
        if isinstance(enemy, Wizard) and random.randint(1, 5) == 1:
            return f"🪄 Волшебник {enemy.name} применил магический щит и избежал атаки!"

        if enemy.hp > self.power:
            enemy.hp -= self.power
            return f"⚔️ @{self.pokemon_trainer} атакует @{enemy.pokemon_trainer}. У {enemy.name} осталось {enemy.hp} HP."
        else:
            enemy.hp = 0
            bonus_text = self.win_bonus()
            del Pokemon.pokemons[enemy.pokemon_trainer]
            return f"🏆 Победа @{self.pokemon_trainer} над @{enemy.pokemon_trainer}!\n{bonus_text}\n❌ {enemy.name} был побежден."



class Wizard(Pokemon):
    def __init__(self, trainer_name):
        super().__init__("Wizard", trainer_name)
        self.pokemon_class = "Волшебник"

    
    def feed(self, feed_interval=20, hp_increase=20):
        return super().feed(feed_interval, hp_increase)

    def attack(self, enemy):
        return super().attack(enemy)


class Fighter(Pokemon):
    def __init__(self, trainer_name):
        super().__init__("Fighter", trainer_name)
        self.pokemon_class = "Боец"

    
    def feed(self, feed_interval=10, hp_increase=10):
        return super().feed(feed_interval, hp_increase)

    def attack(self, enemy):
        super_power = random.randint(5, 15)
        self.power += super_power
        result = super().attack(enemy)
        self.power -= super_power
        return f"{result}\n💥 Боец применил супер-атаку силой: {super_power}!"


class SuperFighter(Fighter):
    def __init__(self, trainer_name):
        super().__init__(trainer_name)
        self.name = "Super Fighter"

    def attack(self, enemy):
        if random.randint(1, 3) == 1:
            bonus = random.randint(10, 25)
            self.power += bonus
            result = super().attack(enemy)
            self.power -= bonus
            return f"💥 {self.name} использует супер-удар (+{bonus} силы)!\n" + result
        else:
            return super().attack(enemy)


class ShieldWizard(Wizard):
    def __init__(self, trainer_name):
        super().__init__(trainer_name)
        self.name = "Shield Wizard"

    def attack(self, enemy):
        if random.randint(1, 4) == 1:
            return f"🛡 {self.name} активировал магический щит и защитился!"
        return super().attack(enemy)






@bot.message_handler(commands=['go'])
def start(message):
    username = message.from_user.username
    if username not in Pokemon.pokemons:
        chance = randint(1, 10)
        if chance == 1:
            pokemon = ShieldWizard(username)
        elif chance == 2:
            pokemon = SuperFighter(username)
        elif chance == 3:
            pokemon = Wizard(username)
        elif chance == 4:
            pokemon = Fighter(username)
        else:
            pokemon = Pokemon(username, username)
        Pokemon.pokemons[username] = pokemon
        bot.send_message(message.chat.id,
                         f"🎉 Поздравляю, {username}!\nТвой покемон — класс {pokemon.pokemon_class}!\n{pokemon.info()}")
    else:
        bot.reply_to(message, "Ты уже создал себе покемона!")


@bot.message_handler(commands=['attack'])
def attack_pok(message):
    if message.reply_to_message:
        attacker_name = message.from_user.username
        defender_name = message.reply_to_message.from_user.username
        if attacker_name in Pokemon.pokemons and defender_name in Pokemon.pokemons:
            attacker = Pokemon.pokemons[attacker_name]
            defender = Pokemon.pokemons[defender_name]
            result = attacker.attack(defender)
            bot.send_message(message.chat.id, result)
        else:
            bot.send_message(message.chat.id, "⚠️ Сражаться можно только с игроками с покемонами!")
    else:
        bot.send_message(message.chat.id, "Ответь на сообщение того, кого хочешь атаковать!")






@bot.message_handler(commands=['feed'])
def feed_pok(message):
    username = message.from_user.username
    if username in Pokemon.pokemons:
        pok = Pokemon.pokemons[username]
        bot.send_message(message.chat.id, pok.feed())
    else:
        bot.send_message(message.chat.id, "У тебя нет покемона. Создай его командой /go")


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот-помощник и покемон-бот. 🐾\nКоманды:\n/go - создать покемона\n/attack - атаковать\n/heal - восстановить здоровье\n/feed - накормить покемона\n/coin - монета\n/info - информация о боте")


@bot.message_handler(commands=['coin'])
def coin_handler(message):
    bot.reply_to(message, choice(["ОРЕЛ", "РЕШКА"]))


@bot.message_handler(commands=['info'])
def send_info(message):
    bot.reply_to(message, "Я дружелюбный бот, который может кидать монетку и играть с покемонами!")


bot.infinity_polling()
