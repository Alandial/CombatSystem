init python:



    def DiceRoll(sides=6):
        return renpy.random.randint(1, sides)

    class enemy:
        def __init__(self, name, level = 1, max_hp = 0, hp = 0, initiative = 0, atk = 0, defense = 0, img = 0, weapon = 0, to_hit = 0):
            self.name = name
            self.level = 1
            self.max_hp = max_hp
            self.hp = hp
            self.initiative = initiative
            self.atk = atk
            self.defense = defense
            self.img = img
            self.weapon = weapon
            self.to_hit = to_hit

    # Function to initiate combat
    def initiate_combat(player, enemies):
        combat = CombatSystem(person=player, enemies=enemies)
        combat.fight()

        
    class CombatSystem:
        def __init__(self, person, enemies):
            self.person = person
            self.enemies = enemies

        
        def show_vbox_screen(self):
            show_custom_screen()

        def create_enemy_list():
            enemy_list = []
            return enemy_list
        
        def fight(self):
            self.person.hp = self.person.max_hp

            for enemy in self.enemies:
                enemy.hp = enemy.max_hp

            current_enemy_index = 0

            while self.person.hp > 0 and self.enemies:
                enemy = self.enemies[current_enemy_index]
                if enemy.hp <= 0:
                    renpy.say("", f"You have slain the {enemy.name}!")
                    renpy.hide(enemy.img)
                    self.enemies.remove(enemy)
                    current_enemy_index %= len(self.enemies)
                    if not self.enemies:  # Check if all enemies are defeated
                        break
                    enemy = self.enemies[current_enemy_index]

                renpy.show(enemy.img)

                #Player's turn
                result = renpy.display_menu([("Attack", "attack")]) #todo modify this to look better. (add heavy attack?)
                roll = DiceRoll(100)
                if roll > self.person.to_hit:
                    renpy.say("","Your attack missed")
                else:
                    renpy.say("",f"You strike at the {enemy.name} with your sword!")
                    player_attack_value = round(max(DiceRoll(self.person.atk) - enemy.defense, self.person.atk*0.5)) #dmg calc
                    renpy.say("",f"You strike the {enemy.name} for {player_attack_value} damage!")
                    enemy.hp -= player_attack_value #actual hp reduction
                    

                if enemy.hp <= 0:
                    renpy.say("",f"You have slain the {enemy.name}!")
                    renpy.hide(enemy.img)
                    self.enemies.remove(enemy) #Remove defeated enemy

                if enemy.hp <= 0: #checks if current enemy is dead, and replaces with next enemy if it is.
                    continue
                    current_enemy_index += 1
                    current_enemy_index %= len(self.enemies)
            
                    

                #Enemy's turn
                renpy.pause(1)                        
                
                if any(enemy.hp > 0 for enemy in self.enemies): #Checks to see if any enemies are alive
                    renpy.say("",f"The {enemy.name} strikes at you with his {enemy.weapon}!")
                    roll = DiceRoll(100)
                    if roll < enemy.to_hit:
                        enemy_attack_value = max(DiceRoll(enemy.atk) - self.person.defense, 1) #dmg calc
                        renpy.say("",f"The {enemy.name} hits you for {enemy_attack_value} dmg!")
                        self.person.hp -= enemy_attack_value #actual hp reduction
                        if self.person.hp <= 0:
                            renpy.jump ("endGame")
                    else:
                        renpy.say("",f"You block the attack!")

                
            
