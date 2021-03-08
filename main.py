import json
import random
import time
import sys


class House:

    def __init__(self, house_name, name, slogan, starting_gold, starting_health, damage, gold_won, gold=0, health=0):
        self.house_name = house_name
        self.name = name
        self.slogan = slogan
        self.starting_gold = starting_gold
        self.starting_health = starting_health
        self.damage = damage
        self.gold_won = gold_won
        self.gold = starting_gold
        self.health = starting_health

    def __repr__(self):
        return f"<{self.house_name}>"

    def get_damage(self, damage):
        self.health -= damage
        printc(Colors.CYAN, f"{self.name} get {damage} point damage. Remaining HP: {0 if self.health < 0 else self.health}")


class Player(House):
    def __repr__(self):
        return f"<Player '{self.name}' hp:{self.health} gold:{self.gold}>"

    def make_move(self):
        if self.health > 1:
            printc(Colors.BLUE, "What is your move?")
            printc(Colors.BLUE, "Fight: f")
            printc(Colors.BLUE, "Retreat: r")
            move = input('>')
            if move == "f":
                if random.randint(0, 4) > 0:
                    time.sleep(random.randint(1, 3))
                    printc(Colors.GREEN, "You hit your enemy")
                    enemy.get_damage(self.damage)
                    enemy.make_move()
                else:
                    time.sleep(random.randint(1, 3))
                    printc(Colors.WARNING, "You miss. Enemy's turn.")
                    enemy.make_move()
            elif move == "r":
                player.retreat()
            else:
                printc(Colors.FAIL, "Wrong move.")
                player.make_move()
        else:
            printc(Colors.FAIL, "You defeated by your enemy.")
            printc(Colors.BOLD, f"{enemy.name} said: {enemy.slogan}")

    def retreat(self):
        printc(Colors.FAIL, f"You choose to retreat.\nHealth: {self.health}. Total reward: {self.gold}")
        printc(Colors.BOLD, f"{enemy.name} said: {enemy.slogan}")
        sys.exit()


class Enemy(House):
    def __repr__(self):
        return f"<Enemy '{self.name}' hp:{self.health} gold:{self.gold}>"

    def make_move(self):
        if self.health > 1:
            if random.randint(0, 5) < 3:
                time.sleep(random.randint(1, 3))
                player.get_damage(self.damage)
                player.make_move()
            else:
                time.sleep(random.randint(1, 3))
                printc(Colors.GREEN, "Enemy missed. Your turn.")
                player.make_move()
        else:
            printc(Colors.GREEN, f"You defeated your enemy {self.name}. {len(house_list)} enemies left.")
            printc(Colors.BOLD, f"You said: {player.slogan}")
            player.gold += player.gold_won
            if player.gold > player.starting_gold:
                player.gold = player.starting_gold


class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def printc(color, *text):
    print(*map(lambda t: f"{color}{t}{Colors.END}", text))


def select_char(t, house):
    return t(**house.__dict__)


def generate_house_list():
    _house_list = []

    with open("house_data.json") as house_data:
        house_data = json.loads(house_data.read())

    return [House(data['name'], data['hero'], data['slogan'], data['starting_gold'], data['starting_health'],
                  data['damage'], data['gold_won']) for data in house_data]


def get_selected_house():
    for i, house in enumerate(house_list):
        printc(Colors.BLUE, i + 1, house.house_name)
    try:
        s = int(input('Which house you are belong to? :'))
        if 1 > s > 11:
            raise ValueError
        selected = house_list[s - 1]
        house_list.remove(selected)
        return selected
    except ValueError:
        printc(Colors.FAIL, "Wrong answer! You have to enter valid number.")
        get_selected_house()


def make_first_attack():
    if random.randint(0, 1) == 0:
        player.make_move()
    else:
        enemy.make_move()


def ask_for_health():
    printc(Colors.CYAN, f"Your remaining HP: {player.health} Gold: {player.gold}")
    printc(Colors.BLUE, "How much HP you want to buy? (0 for none)")
    try:
        amount = int(input(">"))
        if -1 < amount < player.starting_health and amount + player.health <= player.starting_health and amount <= player.gold:
            player.gold -= amount
            player.health += amount
            printc(Colors.CYAN, f"You bought {amount} HP.")
        else:
            raise ValueError
    except ValueError:
        printc(Colors.FAIL, "You cannot buy this amount of health")
        ask_for_health()


if __name__ == '__main__':

    logo = """\
    
                                   '...............................,    
       @   @                          @                            `    
      @        '   #      +:'         @ @   @ @,@   +;'` @   .. @;@ # # 
     +`        @   @   '` ;    .` .`  @ @   @ @  ; @ ; ' @@     @   +   
     #        #.   +@  :+ ;`, @` .:   @ @;;;@ @   `` ;  :@ @    @`' ';  
     +,    @  +'@  ',`; @ ;   #` ;:   @ @   @ @,@ `. ;  '@  @   @ `  :' 
      @    @ .  @  . @: @ ;    ., ;   @ @   @ @  + @ ; . @  `+  @     @ 
      ;@   @ @  .@`; `  @.##;         @ @`  @ @. .+ #';  @`  `  @:@ ';  
        #@@,                         ';;             		
    
    
    """
    print(logo)

    house_list = generate_house_list()

    selected_house = get_selected_house()

    player = select_char(Player, selected_house)

    printc(Colors.CYAN, f"You're {player.name}. You have {player.health} health points and {player.gold} golds.")
    printc(Colors.CYAN, "You must defeat your 10 enemies to reach Iron Throne.")
    printc(Colors.CYAN, "You can buy health point with your golds after each round. 1 HP = 1 GOLD")
    printc(Colors.CYAN, "Good luck...")
    print()

    time.sleep(2)

    random.shuffle(house_list)

    while len(house_list) > 0 and player.health > 1:
        enemy = select_char(Enemy, house_list.pop())
        time.sleep(1)
        if len(house_list) <= 8:
            ask_for_health()
        printc(Colors.CYAN, f"You're facing your enemy {enemy.name} right now.")
        make_first_attack()

    if len(house_list) == 0:
        printc(Colors.GREEN, "† You reach the Iron throne †")
