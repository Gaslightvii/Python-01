from classes.game import Person, bcolors, slowprint
from classes.magic import Spell
from classes.inventory import Item
import random

# Create Black Magic
fire = Spell("Fire", 10, 150, "black")
thunder = Spell("Thunder", 10, 170, "black")
blizzard = Spell("Blizzard", 10, 140, "black")
meteor = Spell("Meteor", 20, 250, "black")
quake = Spell("Quake", 14, 150, "black")

#Create White Magic
cure = Spell("Cure", 11, -120, "white")
cura = Spell("Cura", 15, -250, "white")


# Create some items
potion = Item("Potion", "potion", "Heals 50 HP", -50)
hipotion = Item("Hi-Potion", "potion", "Heals 100 HP", -100)
superpotion = Item("Super potion", "potion", "Heals 500 HP", -500)
elixer = Item("Elixer", "elixer", "Fully restores HP/MP of one party member", -99999)
hielexier = Item("MegaElixer", "elixer", "Fully restores party's HP/MP", -99999)

grenade = Item("Grenade", "attack", "Deals 500 damage", 500)

player_spells = [fire, thunder, blizzard, meteor, quake, cure, cura]
player_items = [{"item": potion, "quantity": 15}, {"item": hipotion, "quantity": 5},
                {"item": superpotion, "quantity": 5}, {"item": elixer, "quantity": 15},
                {"item": hielexier, "quantity": 5}, {"item": grenade, "quantity": 15},]

#Instantiate People
player1 = Person("Valos", 3460, 165, 90, 134, player_spells, player_items)
player2 = Person("Smith", 3460, 145, 70, 104, player_spells, player_items)
player3 = Person("Tayah", 3460, 165, 60, 94, player_spells, player_items)

enemy1 = Person("Goblin", 1200, 65, 845, 25, [], [])
enemy2 = Person("Kobold", 800, 45, 145, 20, [], [])
enemy3 = Person("Kobold", 800, 45, 145, 20, [], [])

players = [player1, player2, player3]
enemies = [enemy1, enemy2, enemy3]
running = True
i = 0

print("\n")
slowprint("As you and your friends leave the inn feeling rather inebriated, the dusk sky dwindles in the distance.")
slowprint("A crow squawks noisily in the shadow of the tree, blocking out the last of the day's light but it is the ")
slowprint("howl of the lone wolf that sends a shiver down your spine.")
slowprint('"Let\'s get moving, don\'t wanna be out here after dark."')
input("Press enter to continue...")
print("\n")
slowprint(bcolors.FAIL + bcolors.BOLD + "An enemy emerges from the shadows and attacks your party!" + bcolors.ENDC)
input("Press enter to continue...")

while running:
    print("===================================")

    for player in players:
        if enemy1.get_hp() == 0:
            running = False
            break

        print("Your enemy:")
        enemy1.get_enemy_stats()

        enemy_choice = 1
        target = random.randrange(0, 3)
        enemy_dmg = enemy1.generate_damage()
        players[target].take_damage(enemy_dmg)
        slowprint(bcolors.FAIL + enemy1.name + bcolors.ENDC + " attacks " + bcolors.OKGREEN + players[target].name +
                  bcolors.ENDC + " for " + bcolors.BOLD + str(enemy_dmg) + bcolors.ENDC + " points of damage."
                  + bcolors.ENDC)
        print("===================================")
        print("Your party:")
        player1.get_stats()
        player2.get_stats()
        player3.get_stats()

        player.choose_action()
        choice = input("    Choose action: ")
        index = int(choice) - 1

        if index == 0:
            dmg = player.generate_damage()
            enemy1.take_damage(dmg)
            slowprint(player.name + " attacked " + enemy1.name + " for " + bcolors.BOLD + str(dmg) + bcolors.ENDC +
                      " points of damage. Enemy HP: " + bcolors.FAIL + str(enemy1.get_hp()) + bcolors.ENDC)


        elif index == 1:
            player.choose_magic()
            magic_choice = int(input("    Choose Magic: ")) - 1

            if magic_choice == -1:
                continue

            spell = player.magic[magic_choice]
            magic_dmg = player.magic[magic_choice].generate_damage()

            current_mp = player.get_mp()

            if spell.cost > current_mp:
                slowprint(bcolors.FAIL + "\nNot enough MP\n" + bcolors.ENDC)
                continue

            player.reduce_mp(spell.cost)

            if spell.type == "white":
                player.heal(magic_dmg)
                slowprint(bcolors.OKBLUE + "\n" + spell.name + " heals for " + str(magic_dmg) + " HP." + bcolors.ENDC)
            elif spell.type == "black":
                enemy1.take_damage(magic_dmg)
                slowprint(
                    bcolors.OKBLUE + "\n" + spell.name + " deals " + str(magic_dmg) + " points of damage." + bcolors.ENDC)
            if enemy1.get_hp() == 0:
                running = False


        elif index == 2:
            player.choose_item()
            item_choice = int(input("    Choose Item: ")) - 1

            if item_choice == -1:
                continue

            item = player.items[item_choice]["item"]
            if player.items[item_choice]["quantity"] == 0:
                slowprint(bcolors.FAIL + "\n" + "...none left." + bcolors.ENDC)
                continue

            player.items[item_choice]["quantity"] -= 1

            if item.type == "potion":
                player.heal(item.prop)
                slowprint(bcolors.OKGREEN + "\n" + item.name + " heals for " + str(item.prop) + " HP" + bcolors.ENDC)
            elif item.type == "elixer":

                if item.name == "MegaElixer":
                    for i in players:
                        i.hp = i.maxhp
                        i.mp = i.maxmp
                else:
                    player.hp = player.maxhp
                    player.mp = player.maxmp
                slowprint(bcolors.OKGREEN + "\n" + item.name + " fully restores HP/MP" + bcolors.ENDC)
            elif item.type == "attack":
                enemy1.take_damage(item.prop)
                slowprint(
                    bcolors.FAIL + "\n" + item.name + " deals " + str(item.prop) + " points of damage" + bcolors.ENDC)
            if enemy1.get_hp() == 0:
                running = False
                break



    if player.get_hp() == 0:
        slowprint(
            bcolors.FAIL + "Your enemy has defeated you! You limp back to the inn, to fight another day." + bcolors.ENDC)
        running = False
        break

slowprint(bcolors.FAIL + enemy1.name + " has died.")
slowprint(bcolors.OKGREEN + "You win!" + bcolors.ENDC)
input("Press enter to continue...")
slowprint(
        "With blood trickling into your boots, you slowly venture on down the road. It isn't long before ")
slowprint(
        "your weary eyes start to deceive you again. A gust of wind shakes the leaves around you as if a ")
slowprint("wave of darkness has come crashing down around you. ")
slowprint(
        "As the wind dies down, a nearby bush continues to rustle. The squeaking sound alerts you to the ")
slowprint("presence of another beast before you.")
input("Press enter to continue...")


print("===================================")
running = True
i = 0
while running:
    for player in players:
            if enemy2.get_hp() == 0:
                running = False


            print("Your enemy:")
            enemy2.get_enemy_stats()

            enemy_choice = 1
            target = random.randrange(0, 3)
            enemy_dmg = enemy2.generate_damage()
            players[target].take_damage(enemy_dmg)
            slowprint(bcolors.FAIL + enemy2.name + bcolors.ENDC + " attacks " + bcolors.OKGREEN + players[target].name +
                      bcolors.ENDC + " for " + bcolors.BOLD + str(enemy_dmg) + bcolors.ENDC + " points of damage."
                      + bcolors.ENDC)
            print("===================================")
            print("Your party:")
            player1.get_stats()
            player2.get_stats()
            player3.get_stats()

            player.choose_action()
            choice = input("    Choose action: ")
            index = int(choice) - 1

            if index == 0:
                dmg = player.generate_damage()
                enemy2.take_damage(dmg)
                slowprint(player.name + " attacked " + enemy2.name + " for " + bcolors.BOLD + str(dmg) + bcolors.ENDC +
                          " points of damage. Enemy HP: " + bcolors.FAIL + str(enemy2.get_hp()) + bcolors.ENDC)

            elif index == 1:
                player.choose_magic()
                magic_choice = int(input("    Choose Magic: ")) - 1

                if magic_choice == -1:
                    continue

                spell = player.magic[magic_choice]
                magic_dmg = player.magic[magic_choice].generate_damage()

                current_mp = player.get_mp()

                if spell.cost > current_mp:
                    slowprint(bcolors.FAIL + "\nNot enough MP\n" + bcolors.ENDC)
                    continue

                player.reduce_mp(spell.cost)

                if spell.type == "white":
                    player.heal(magic_dmg)
                    slowprint(bcolors.OKBLUE + "\n" + spell.name + " heals for " + str(magic_dmg) + "HP." + bcolors.ENDC)
                elif spell.type == "black":
                    enemy2.take_damage(magic_dmg)
                    slowprint(bcolors.OKBLUE + "\n" + spell.name + " deals " + str(
                        magic_dmg) + " points of damage." + bcolors.ENDC)
                if enemy2.get_hp() == 0:
                     running = False

            elif index == 2:
                player.choose_item()
                item_choice = int(input("    Choose Item: ")) - 1

                if item_choice == -1:
                    continue

                item = player.items[item_choice]["item"]
                if player.items[item_choice]["quantity"] == 0:
                    slowprint(bcolors.FAIL + "\n" + "...none left." + bcolors.ENDC)
                    continue

                player.items[item_choice]["quantity"] -= 1

                if item.type == "potion":
                    player.heal(item.prop)
                    slowprint(bcolors.OKGREEN + "\n" + item.name + " heals for " + str(item.prop) + "HP" + bcolors.ENDC)
                elif item.type == "elixer":

                    if item.name == "MegaElixer":
                        for i in players:
                            i.hp = i.maxhp
                            i.mp = i.maxmp
                    else:
                        player.hp = player.maxhp
                        player.mp = player.maxmp
                    slowprint(bcolors.OKGREEN + "\n" + item.name + " fully restores HP/MP" + bcolors.ENDC)
                elif item.type == "attack":
                    enemy2.take_damage(item.prop)
                    slowprint(
                        bcolors.FAIL + "\n" + item.name + " deals " + str(item.prop) + " points of damage" + bcolors.ENDC)

            if enemy2.get_hp() == 0:
                slowprint(bcolors.OKGREEN + "You win!" + bcolors.ENDC)
                input("Press enter to continue...")
                slowprint("You make it back to the safety of your house with but flesh wounds. You shall live to fight "
                          "another day.")
                input("Press enter to continue...")
                slowprint('"Oh woops, I left my wife at the inn, back I go..."')
                running = False
                break