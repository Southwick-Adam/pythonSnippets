#This game is a text based RPG based on the characters of Lord of the Rings
#you play as a wizard with various spells
#you and your team of fighters, archers and more face off against creatures
#with there own sets of specialized skills
#Good luck and have fun!

import random
import time


class Creature:
    def __init__(self, name, maxHP=10):
        self.name = name
        self.hp = maxHP
        self.maxHP = maxHP
        self.abilities = [1, 5, 5]  # attack, defense, speed

    def check_life(self):
        if self.hp <= 0:
            self.hp = 0
            print(f"{self.name} fainted.")
        return self.hp

    def attack(self, target):
        print(f"{self.name} attacks {target.name}.")
        roll = random.randrange(1, 20)
        if roll < (target.abilities[1] + target.abilities[2]):
            print("Attack missed...")
            return
        attackMod = random.randrange(1, 4)
        damage = self.abilities[0] + attackMod
        target.hp -= damage
        print(f"Attack hits for {damage} damage!")
        target.check_life()

    def auto_select(self, target_list):
        randTarget = random.randint(0, len(target_list) - 1)
        return target_list[randTarget]

    def turn(self, round_num, target_list):
        targ = self.auto_select(target_list)
        if targ != None:
            self.attack(targ)

    def targetStrongWeak(self, target_list, mode):
        targ = None
        for t in target_list:
            if t.hp <= 0:  # needed for multi strike attacks from Fighter and Orc General
                continue
            if targ == None:
                targ = t
                continue
            if mode == "strong":
                if t.hp > targ.hp:
                    targ = t
            else:
                if t.hp < targ.hp:
                    targ = t
        return targ

    def healHP(self, val):
        healAmmount = val
        if self.hp + val > self.maxHP:
            healAmmount = (self.maxHP - self.hp)
            self.hp = self.maxHP
        else:
            self.hp += val
        return healAmmount

    def __gt__(self, other):
        return self.abilities[2] > other.abilities[2]  # speed


class Goblin(Creature):
    def __init__(self, name, maxHP=15):
        Creature.__init__(self, name, maxHP)
        self.abilities = [3, 6, 6]  # attack, defense, speed


class Orc(Creature):
    def __init__(self, name, maxHP=50):
        Creature.__init__(self, name, maxHP)
        self.abilities = [5, 8, 3]  # attack, defense, speed
        self.abilitiesMod = False

    def heavy_attack(self, target):
        if not self.abilitiesMod:
            self.abilitiesMod = True
            self.abilities = [10, 5, 5]  # attack, defense, speed
            print(f"{self.name} is in a rage!")
        Creature.attack(self, target)

    def attack(self, target):
        if self.abilitiesMod:
            self.abilitiesMod = False
            self.abilities = [5, 8, 3]  # attack, defense, speed
            print(f"{self.name} has cooled down.")
        Creature.attack(self, target)

    def turn(self, round_num, target_list):
        targ = self.auto_select(target_list)
        if targ == None:
            return
        if round_num % 4 == 0:
            self.heavy_attack(targ)
        else:
            self.attack(targ)


class Warrior(Creature):
    def __init__(self, name, maxHP=50):
        Creature.__init__(self, name, maxHP)
        self.abilities = [5, 10, 4]  # attack, defense, speed
        self.shield = False

    def shield_up(self):
        if not self.shield:
            self.shield = True
            self.abilities[0] -= 4
            self.abilities[1] += 4
            print(f"{self.name} takes a defensive stance.")

    def shield_down(self):
        if self.shield:
            self.shield = False
            self.abilities = [5, 10, 4]  # attack, defense, speed
            print(f"{self.name}'s stance returns to normal.")

    def turn(self, round_num, target_list):
        targ = self.auto_select(target_list)
        if targ == None:
            return
        if round_num % 4 == 1:
            self.attack(targ)
            self.shield_up()
        elif round_num % 4 == 0:
            self.shield_down()
            self.attack(targ)
        else:
            self.attack(targ)


class Archer(Creature):
    def __init__(self, name, maxHP=30):
        Creature.__init__(self, name, maxHP)
        self.abilities = [7, 9, 8]  # attack, defense, speed
        self.abilitiesMod = False

    def power_shot(self, target):
        roll1 = random.randrange(1, 20)
        roll2 = random.randrange(1, 20)
        roll = max(roll1, roll2)
        speedDif = self.abilities[2] - target.abilities[2]
        if speedDif > 0:
            roll += speedDif
        if not self.abilitiesMod:
            self.abilitiesMod = True
            self.abilities[0] += 3
            print(f"{self.name}'s attack rises")
            self.abilities[1] -= 3
            print(f"{self.name}'s defence reduced")
        print(f"{self.name} shoots at {target.name}.")
        if roll < (target.abilities[1] + target.abilities[2]):
            print("Power Shot missed...")
            return
        attackMod = random.randrange(1, 8)
        damage = self.abilities[0] + attackMod
        target.hp -= damage
        print(f"Attack hits for {damage} damage!")
        target.check_life()

    def attack(self, target):
        if self.abilitiesMod:
            self.abilitiesMod = False
            self.abilities = [7, 9, 8]  # attack, defense, speed
            print(f"{self.name}'s abilities return to normal.")
        Creature.attack(self, target)

    def auto_select(self, target_list):
        return self.targetStrongWeak(target_list, "weak")

    def turn(self, round_num, target_list):
        targ = self.auto_select(target_list)
        if targ == None:
            return
        if round_num % 4 == 1:
            self.attack(targ)
        else:
            self.power_shot(targ)


class Fighter(Creature):
    def __init__(self, name, maxHP=50):
        Creature.__init__(self, name, maxHP)
        self.abilities = [5, 8, 5]  # attack, defense, speed
        self.abilitiesMod = False

    def auto_select(self, target_list):
        return self.targetStrongWeak(target_list, "strong")

    def turn(self, round_num, target_list):
        self.abilities[0] = 5
        targ = None
        for i in range(3):
            if targ == None:
                targ = self.auto_select(target_list)
            if targ == None:
                return  # other team is wiped out
            if i == 1:
                print(f"{self.name} unleashes a flurry of strikes.")
                self.abilities[0] = 2
            self.attack(targ)
            if targ.hp <= 0:
                targ = None

# ENEMIES


class OrcGeneral(Orc, Warrior):
    def __init__(self, name, maxHP=80):
        Orc.__init__(self, name, maxHP)
        self.shield = False

    def turn(self, round_num, target_list):
        targ = self.auto_select(target_list)
        if targ == None:
            return
        if round_num % 4 == 1:
            self.attack(targ)
            self.shield_up()
        elif round_num % 4 == 2:
            self.attack(targ)
        elif round_num % 4 == 3:
            self.shield_down()
            self.attack(targ)
        else:
            self.heavy_attack(targ)


class GoblinKing(Goblin, Archer):
    def __init__(self, name, maxHP=50):
        Goblin.__init__(self, name, maxHP)
        self.abilitiesMod = False


class Boss(Orc):
    def __init__(self, name, maxHP=200):
        Orc.__init__(self, name, maxHP)
        self.abilities[2] = 5  # other stats are correct on Orc class

    def auto_select(self, target_list, mode):
        if mode == "random":
            rand = random.randint(0, 2)
            if rand == 0:
                mode = "weak"
            else:
                mode = "strong"
        return self.targetStrongWeak(target_list, mode)

    def turn(self, round_num, target_list):
        if round_num % 4 == 1:
            targ = self.auto_select(target_list, "weak")
            if targ == None:
                return  # other team is wiped out
            self.attack(targ)
            if targ.hp <= 0:
                targ = None
            for i in range(2):  # Flurry of strikes
                if targ == None:
                    targ = self.auto_select(target_list, "random")
                if targ == None:
                    return  # other team is wiped out
                if i == 0:
                    print(f"{self.name} unleashes a flurry of strikes.")
                self.abilities[0] -= 3
                self.attack(targ)
                self.abilities[0] += 3
                if targ.hp <= 0:
                    targ = None
        else:
            targ = self.auto_select(target_list, "strong")
            if targ == None:
                return  # other team is wiped out
            self.heavy_attack(targ)

# WIZARD


class Wizard(Creature):
    def __init__(self, name, maxHP=20):
        Creature.__init__(self, name, maxHP)
        self.abilities = [3, 5, 5, 10]  # attack, defense, speed, arcana
        self.__mana = 100

    def use_mana(self, val):
        if self.__mana - val < 0:
            print("Not enough Mana.")
            return False
        print(f"-{val} Mana")
        self.__mana -= val
        return True

    def add_mana(self, val):
        self.__mana += val
        if self.__mana >= 100:
            print("Mana is full.")
            self.__mana = 100
        else:
            print(f"Mana +{val}!")

    def attack(self, target):
        Creature.attack(self, target)
        self.add_mana(20)

    def recharge(self):
        print(f"{self.name} channels magical energy...")
        self.add_mana(30)

    def fire_bolt(self, target):
        # self.abilities[3] = Arcana
        print(f"{self.name} hurls a fireball at {target.name}.")
        roll = random.randrange(1, 20)
        roll += (self.abilities[3] // 2)
        if roll < (target.abilities[1] + target.abilities[2]):
            print("Fireball missed...")
            return
        damage = random.randrange(1, self.abilities[3])
        target.hp -= damage
        print(f"Fireball hits for {damage} damage!")
        self.add_mana(10)
        target.check_life()

    def heal(self, target):
        if self.use_mana(20):
            healVal = random.randrange(0, 8)
            healVal += (self.abilities[3] // 2)
            print(f"{self.name} heals {target.name} for {target.healHP(healVal)} HP!")
        else:
            print("Heal Failed.")

    def mass_heal(self, allies):
        if self.use_mana(30):
            for a in allies:
                healVal = random.randrange(0, 10)
                healVal += (self.abilities[3])
                print(f"{self.name} heals {a.name} for {a.healHP(healVal)} HP!")
        else:
            print("Mass heal Failed.")

    def fire_storm(self, enemies):
        if self.use_mana(50):
            for e in enemies:
                roll = random.randrange(1, 20)
                roll += e.abilities[2]  # speed
                attackMod = 1
                if roll >= self.abilities[3]:  # arcana
                    attackMod = 2
                damage = (random.randrange(5, 20) +
                          self.abilities[3]) // attackMod
                e.hp -= damage
                print(f"Fire Storm deals {damage} fire damage to {e.name}!")
                e.check_life()
        else:
            print("Fire Storm Failed.")

    def select_target(self, target_list):
        print("Select target:")
        n = 1
        for t in target_list:
            print(f"{n}: {t.name}, HP: {t.hp}/{t.maxHP}")
            n += 1
        choice = int(input("Enter choice: "))
        while True:
            if choice <= len(target_list) and choice > 0:
                return target_list[choice - 1]
            print("That is not a valid choice. Please choose again.")
            choice = int(input("Enter choice: "))

    def player_turn(self, allies, enemies):
        print(
            f"Player: {self.name} HP:{self.hp}/{self.maxHP} Mana: {self.__mana}/100")
        print("Allies:")
        for a in allies:
            print(f"\t {a.name} HP:{a.hp}/{a.maxHP}")
        line()
        print("Actions: F: Attack, R: Recharge Mana")
        print("Spells: 1: Heal, 2: Firebolt, 3: Mass Heal, 4: Fire Storm")
        print("To Quit game type: Quit")
        line()
        action = None
        while True:
            action = input("Enter Action: ").lower()
            if action == 'quit':
                print("Quitting game.")
                return 'QUIT'
            if action in 'fr1234':
                break
            print("invalid action.")
        # RESOLVE ACTIONS
        if action == 'r':  # recharge
            self.recharge()
            return
        if action == '3':  # mass heal
            wholeAllyTeam = allies.copy()
            wholeAllyTeam.append(self)
            self.mass_heal(wholeAllyTeam)
            return
        if action == '4':
            self.fire_storm(enemies)
            return
        if action in 'f12':  # single target actions
            targ_list = enemies
            if action == '1':  # only action that can target allies
                targ_list = allies.copy()
                targ_list.append(self)
            targ = self.select_target(targ_list)
            if action == 'f':
                self.attack(targ)
                return
            if action == '1':
                self.heal(targ)
                return
            if action == '2':
                self.fire_bolt(targ)
                return


class Battle:
    def __init__(self):
        self.enemies = [GoblinKing("Goblin King"), OrcGeneral(
            "Orc General"), Orc("Orc"), Goblin("Goblin")]
        self.allies = [Fighter("Aragorn"), Archer(
            "Legolas"), Warrior("Borimir"), Creature("Frodo")]
        self.boss = Boss("Balrog")
        self.player = Wizard("Gandalf")
        self.bossSpawned = False

    def removeDead(self, team):
        for t in team:
            if t.hp <= 0:
                team.remove(t)
                self.turn_order.remove(t)
        if len(team) == 0:
            self.gameOver(team)
            return True
        return False

    def check_for_boss(self):
        if self.bossSpawned:
            return
        if len(self.enemies) < 2:
            self.bossSpawned = True
            self.spawnBoss()

    def spawnBoss(self):
        print(
            f"A strong enemy has apeared. {self.boss.name} has joined the battle.")
        self.enemies.append(self.boss)
        self.turn_order.append(self.boss)
        self.turn_order.sort()
        self.turn_order.reverse()
        line()

    def start(self):
        self.turn_order = self.enemies.copy()
        self.turn_order.extend(self.allies)
        self.turn_order.append(self.player)
        self.turn_order.sort()
        self.turn_order.reverse()
        print("THE BATTLE BEGINS")
        line()
        r = 1
        while True:
            print(f"Round {r}.")
            line()
            for t in self.turn_order:
                if t == self.player:
                    if t.player_turn(self.allies, self.enemies) == 'QUIT':
                        return
                    line()
                    self.removeDead(self.enemies)
                    self.check_for_boss()
                elif t in self.allies:  # on allies team
                    t.turn(r, self.enemies)
                    line()
                    if self.removeDead(self.enemies):
                        return
                    self.check_for_boss()
                else:  # on enemy team
                    allies_plus_player = self.allies.copy()
                    allies_plus_player.append(self.player)
                    t.turn(r, allies_plus_player)
                    line()
                    if self.removeDead(self.allies):
                        return
                    if self.player.hp <= 0:
                        print("Game Over. Player has been defeated.")
                        return
            print(f"End of Round {r}.")
            line()
            r += 1

    def gameOver(self, team):
        if team == self.enemies:
            print("Congratulations! All enemies defeated.")
        else:
            print("Game Over. All allies defeated.")
# END OF BATTLE CLASS


def line():
    print("=======================================================")
    time.sleep(1)  # adjust for speed of game


# game
battle = Battle()
battle.start()
