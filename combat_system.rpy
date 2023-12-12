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


    def show_health_bars(player, enemies):
        renpy.show_screen("hp_bar_person", person=player)
        for enemy in enemies:
            renpy.show_screen("hp_bar_enemy", enemy=enemy)

    # Function to hide health bars for the player and enemies
    def hide_health_bars(player, enemies):
        renpy.hide_screen("hp_bar_person")
        for enemy in enemies:
            renpy.hide_screen("hp_bar_enemy", enemy=enemy)

    # Function to initiate combat
    def initiate_combat(player, enemies):
        show_health_bars(player, enemies)
    
        combat = CombatSystem(person=player, enemies=enemies)
        combat.fight()

        if all(enemy.hp <= 0 for enemy in enemies):
            hide_health_bars(player, enemies)

    class CombatSystem:
        def __init__(self, person, enemies):
            self.person = person
            self.enemies = enemies

        def show_hp_bar_person(self):
            renpy.show_screen("hp_bar_person", person = self.person)

        def show_hp_bar_enemy(self, enemy_index):
            renpy.show_screen("hp_bar_enemy", enemy=self.enemies[enemy_index])

        def hide_hp_bar_person(self):
            renpy.hide_screen("hp_bar_person")

        def hide_hp_bar_enemy(self, enemy_index):
            renpy.hide_screen("hp_bar_enemy")

        def show_vbox_screen(self):
            show_custom_screen()

        def create_enemy_list():
            enemy_list = []
            return enemy_list
        
        def fight(self):

            self.person.hp = self.person.max_hp
            
            for enemy in self.enemies:
                enemy.hp = enemy.max_hp
                renpy.show(enemy.img)
        
            while self.person.hp > 0 and any(enemy.hp > 0 for enemy in self.enemies):
                for enemy in self.enemies:
                    if enemy.hp <= 0:
                        continue # This skips defeeated enemies
                #Player's turn
                result = renpy.display_menu([("Attack", "attack")])
                roll = DiceRoll(100)
                if roll > self.person.to_hit:
                    renpy.say("","Your attack missed")
                else:
                    renpy.say("",f"You strike at the {enemy.name} with your sword!")
                    player_attack_value = round(max(DiceRoll(self.person.atk) - enemy.defense, self.person.atk*0.5))
                    renpy.say("",f"You strike the {enemy.name} for {player_attack_value} damage!")
                    enemy.hp -= player_attack_value
                    

                if enemy.hp <= 0:
                    renpy.say("",f"You have slain the {enemy.name}!")
                    renpy.hide(enemy.img)
                    self.enemies.remove(enemy) #Remove defeated enemy
                    

                #Enemy's turn
                renpy.pause(1)                        
                
                if any(enemy.hp > 0 for enemy in self.enemies): #Checks to see if any enemies are alive
                    renpy.say("",f"The {enemy.name} strikes at you with his {enemy.weapon}!")
                    roll = DiceRoll(100)
                    if roll < enemy.to_hit:
                        enemy_attack_value = max(DiceRoll(enemy.atk) - self.person.defense, 1)
                        renpy.say("",f"The {enemy.name} hits you for {enemy_attack_value} dmg!")
                        self.person.hp -= enemy_attack_value
                    else:
                        renpy.say("",f"You block the attack!") 
            
            if all(enemy.hp <= 0 for enemy in self.enemies):
                self.hide_hp_bar_enemy(enemy)