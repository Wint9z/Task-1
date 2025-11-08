import random
import telebot
from random import randint

# -----------------------------
# Классы покемонов
# -----------------------------
class Pokemon:
    pokemons = {}  # общий словарь для всех покемонов

    def __init__(self, name, trainer):
        self.name = name
        self.pokemon_trainer = trainer
        self.hp = random.randint(50, 100)
        self.power = random.randint(10, 30)
        self.max_hp = 120

    def info(self):
        return f"Покемон: {self.name}, HP: {self.hp}, Сила: {self.power}"

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

    def attack(self, enemy):
        if isinstance(enemy, Wizard) and random.randint(1, 5) == 1:
            return f"🪄 Волшебник {enemy.name} применил магический щит и избежал атаки!"
        
        if enemy.hp > self.power:
            enemy.hp -= self.power
            return f"⚔️ @{self.pokemon_trainer} атакует @{enemy.pokemon_trainer}. У {enemy.name} осталось {enemy.hp} HP."
        else:
            enemy.hp = 0
            bonus_text = self.win_bonus()
            return f"🏆 Победа @{self.pokemon_trainer} над @{enemy.pokemon_trainer}!\n{bonus_text}"


class Fighter(Pokemon):
    def info(self):
        return "💪 У тебя покемон-боец!\n" + super().info()

    def attack(self, enemy):
        super_power = random.randint(5, 15)
        self.power += super_power
        result = super().attack(enemy)
        self.power -= super_power
        return result + f"\n💥 Боец применил супер-атаку силой: {super_power}!"


class Wizard(Pokemon):
    def info(self):
        return "🪄 У тебя покемон-волшебник!\n" + super().info()

    def attack(self, enemy):
        return super().attack(enemy)


# -----------------------------
# Бот
# -----------------------------
bot = telebot.TeleBot("8203604330:AAGGqXL3w8VJU9uAa7jFaF5m5TZtv1lqHnY")

# команды /go, /attack, /heal
@bot.message_handler(commands=['go'])
def start(message):
    username = message.from_user.username
    if username not in Pokemon.pokemons:
        chance = randint(1, 5)
        if chance == 1:
            pokemon = Wizard(username)
        elif chance == 2:
            pokemon = Fighter(username)
        else:
            pokemon = Pokemon(username, username)
        Pokemon.pokemons[username] = pokemon
        bot.send_message(message.chat.id, f"🎉 Поздравляю, {username}!\n{pokemon.info()}")
    else:
        bot.reply_to(message, "Ты уже создал себе покемона!")

# ... остальные команды аналогично

bot.polling(none_stop=True)
