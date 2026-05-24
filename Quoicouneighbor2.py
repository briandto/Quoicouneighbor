#########################################################
# VALEURS PAR DEFAUT
#########################################################
# Importations
import pyxel, random
from decimal import Decimal
# Fenetre
WIDTH = 128
HEIGHT = 128
TITLE = "Quoicouneighbor 2"
INTERFACE_SIZE_Y = 18
FPS = 60
MARGE_INTERACTION = 2
SCREEN_CENTER_X = WIDTH//2
SCREEN_CENTER_Y = (HEIGHT+INTERFACE_SIZE_Y)//2
# Definition des couleurs
COLOR_BLACK = 0
COLOR_DARKBLUE = 1
COLOR_PURPLE = 2
COLOR_GREEN = 3
COLOR_BROWN = 4
COLOR_BLUE = 5
COLOR_LIGHTBLUE = 6
COLOR_WHITE = 7
COLOR_RED = 8
COLOR_ORANGE = 9
COLOR_YELLOW = 10
COLOR_LIGHTGREEN = 11
COLOR_CYAN = 12
COLOR_GREY = 13
COLOR_LIGHTROSE = 14
COLOR_ROSE = 15

#########################################################
# CLASSES
#########################################################
class Player:
    def __init__(self, collisions, x, y, stamina, direction, lives, ability, default_ability_uses, default_ability_duration, default_ability_cooldown):
        self.collisions = collisions
        self.interface_x = 0
        self.interface_y = 0 + INTERFACE_SIZE_Y
        self.default_speed = 0.5
        self.speed = self.default_speed
        self.x = x
        self.y = y
        self.default_lives = lives
        self.lives = self.default_lives
        self.default_stamina = stamina
        self.stamina = self.default_stamina
        self.stamina_statut = True
        self.stamina_regen = 0.2
        self.stamina_inprogress = False
        self.stamina_full = True
        self.stamina_low = False
        self.lives_inprogress = False
        self.lives_full = False
        self.lives_low = False
        self.direction = direction
        self.ability = ability
        self.default_ability_duration = default_ability_duration
        self.ability_duration = self.default_ability_duration
        self.ability_inprogress = False
        self.default_ability_uses = default_ability_uses
        self.ability_uses = self.default_ability_uses
        self.default_ability_cooldown = default_ability_cooldown
        self.ability_cooldown = self.default_ability_cooldown
        self.index_statut = False
        self.index_x = 0
        self.index_y = 0
        self.visibility_statut = True
        self.detector_statut = False
        self.detector_x = 0
        self.detector_y = 0
        self.horizontal_res_x = 0
        self.horizontal_res_y = 0
        self.vertical_res_x = 0
        self.vertical_res_y = 0
        self.size_x = 0
        self.size_y = 0
        self.isjumping = False
        self.KEY_UP = pyxel.KEY_Z
        self.KEY_DOWN = pyxel.KEY_S
        self.KEY_RIGHT = pyxel.KEY_D
        self.KEY_LEFT = pyxel.KEY_Q
        self.KEY_SPRINT = pyxel.KEY_SHIFT
        self.KEY_ABILITY = pyxel.KEY_A
        self.KEY_JUMP = pyxel.KEY_SPACE

    # Revoir conditions pour être considéré dans une collision à sa gauche
    def fcollision(self, pre_x, pre_y, x, y): 
        confirmed = True
        self.isjumping = False

        for x1, y1, x2, y2, type in self.collisions:
            if x1 <= x + self.size_x and y1 <= y + self.size_y and x2 >= x and y2 >= y:
                if type == "Meuble":
                    if pyxel.btn(self.KEY_JUMP):
                        self.isjumping = True
                    else:
                        confirmed = False
                else:
                    confirmed = False
                break

        if confirmed:
            self.x = x
            self.y = y
        else:
            self.x = pre_x
            self.y = pre_y

    def fstamina(self, pre_x, pre_y):
        # Endurance en cours d'utilisation
        if pyxel.btn(self.KEY_SPRINT) and self.x != pre_x or pyxel.btn(self.KEY_SPRINT) and self.y != pre_y:
            self.stamina_inprogress = True
            if self.stamina <= 0:
                self.stamina = -5
                self.stamina_inprogress = False
            elif self.stamina > 0:
                self.stamina -= (self.default_speed + self.stamina_regen)
                self.stamina_inprogress = True
        else:
            self.stamina_inprogress = False
        # Endurance pleine
        self.stamina_full = False
        if self.stamina >= self.default_stamina:
            self.stamina = self.default_stamina
            self.stamina_full = True
        else:
            self.stamina += self.stamina_regen
        # Endurance faible
        self.stamina_low = False
        if self.stamina <= 20:
            self.stamina_low = True

    def fmovement(self):
        ##### VITESSE #####
        if pyxel.btn(self.KEY_SPRINT) and self.stamina > 0:
            self.speed = self.default_speed * 2
        else:
            self.speed = self.default_speed
        if self.isjumping:
            self.speed = self.speed / 2
        ##### DEPLACEMENTS #####
        pre_x = self.x
        pre_y = self.y
        if pyxel.btn(self.KEY_UP):
            self.direction = 1
            # if pyxel.btn(pyxel.KEY_Q):
            #     self.direction = 8
            # if pyxel.btn(pyxel.KEY_D):
            #     self.direction = 2
            self.y -= self.speed
        if pyxel.btn(self.KEY_RIGHT):
            self.direction = 3
            # if pyxel.btn(pyxel.KEY_Z):
            #     self.direction = 2
            # if pyxel.btn(pyxel.KEY_S):
            #     self.direction = 4
            self.x += self.speed
        if pyxel.btn(self.KEY_LEFT):
            self.direction = 7
            # if pyxel.btn(pyxel.KEY_Z):
            #     self.direction = 8
            # if pyxel.btn(pyxel.KEY_S):
            #     self.direction = 6
            self.x -= self.speed
        if pyxel.btn(self.KEY_DOWN):
            self.direction = 5
            # if pyxel.btn(pyxel.KEY_Q) and not pyxel.btn(pyxel.KEY_D):
            #     self.direction = 6
            # if pyxel.btn(pyxel.KEY_D) and not pyxel.btn(pyxel.KEY_Q):
            #     self.direction = 4
            self.y += self.speed
        ##### COLLISIONS #####
        self.fcollision(pre_x, pre_y, self.x, self.y)
        ##### ENDURANCE #####
        if not self.stamina_statut:
            self.stamina = self.default_stamina
        self.fstamina(pre_x, pre_y)

    def fcamera(self):
        ##### CAMERA #####
        # Coin haut gauche
        if self.x <= WIDTH//2 and self.y <= HEIGHT//2:
            self.interface_x = 0
            self.interface_y = 0
        # Coin bas droite
        elif self.x >= 255-WIDTH//2 and self.y >= 255-HEIGHT//2:
            self.interface_x = 255-WIDTH
            self.interface_y = 255-HEIGHT
        # Longueur droite
        elif self.x >= 255-WIDTH//2 and self.y >= HEIGHT//2 and self.y <= 255-HEIGHT//2:
            self.interface_x = 255-WIDTH
            self.interface_y = self.y-HEIGHT//2
        # Longueur basse
        elif self.y >= 255-HEIGHT//2 and self.x >= WIDTH//2 and self.x <= 255-WIDTH//2:
            self.interface_x = self.x-WIDTH//2
            self.interface_y = 255-HEIGHT
        # Coin bas gauche
        elif self.x <= 255-WIDTH//2 and self.y >= 255-HEIGHT//2:
            self.interface_x = 0
            self.interface_y = 255-HEIGHT
        # Coin haut droite
        elif self.x >= 255-WIDTH//2 and self.y <= 255-HEIGHT//2:
            self.interface_x = 255-WIDTH
            self.interface_y = 0
        # longueur gauche
        elif self.x <= WIDTH//2:
            self.interface_x = 0
            self.interface_y = self.y - HEIGHT//2
        # Longueur haute
        elif self.y <= WIDTH//2:
            self.interface_x = self.x - WIDTH//2
            self.interface_y = 0
        # Autre
        else:
           self.interface_x = self.x - WIDTH//2
           self.interface_y = self.y - HEIGHT//2
        pyxel.camera(self.interface_x, self.interface_y)
        self.interface_y += INTERFACE_SIZE_Y

    def fhealth(self):
        if self.lives == self.default_lives:
            self.lives_full = True
        else:
            self.lives_full = False
        if self.lives < self.default_lives:
            self.lives_low = True
        else:
            self.lives_low = False

    def fability(self):
        # Cooldown
        if self.ability_cooldown > 0:
            self.ability_cooldown -= 1/FPS
        elif self.ability_cooldown < 0:
            self.ability_cooldown = 0
        # Activation
        if self.ability_cooldown <= 0 and pyxel.btn(self.KEY_ABILITY) and self.ability_uses > 0 and not self.ability_inprogress:
            self.ability_inprogress = True
        # Activée
        if self.ability_inprogress:
            if self.ability_duration > 0:
                self.ability_duration -= 1/FPS
                if self.ability == "Stamina": # Endurance illimitée pendant 5 secondes
                    self.stamina_statut = False
                elif self.ability == "Index": # Affiche la location de la prochaine cle
                    self.index_statut = True
                elif self.ability == "Detector": # Affiche la location de la prochaine cle
                    self.detector_statut = True
                elif self.ability == "Invisibility": # Affiche la location de la prochaine cle
                    self.visibility_statut = False
            else:
                self.ability_inprogress = False
                self.ability_cooldown = self.default_ability_cooldown
                self.ability_uses -= 1
                self.detector_statut = False
                self.stamina_statut = True
                self.index_statut = False
                self.ability_duration = self.default_ability_duration
                self.visibility_statut = True

    def update(self):
        self.fmovement()
        self.fcamera()
        self.fhealth()
        if self.ability != "":
            self.fability()

    # Effets quand vie/stam low
    def draw(self):
        ##### PERSONNAGE #####
        if self.visibility_statut:
            if self.direction == 1:
                pyxel.blt(self.x, self.y, 0, self.horizontal_res_x, self.horizontal_res_y, self.size_x, self.size_y, COLOR_WHITE)
            elif self.direction == 3:
                pyxel.blt(self.x, self.y, 0, self.vertical_res_x, self.vertical_res_y, self.size_x, self.size_y, COLOR_WHITE)
            elif self.direction == 5:
                pyxel.blt(self.x, self.y, 0, self.horizontal_res_x, self.horizontal_res_y, -self.size_x, -self.size_y, COLOR_WHITE)
            elif self.direction == 7:
                pyxel.blt(self.x, self.y, 0, self.vertical_res_x, self.vertical_res_y, -self.size_x, -self.size_y, COLOR_WHITE)
        ##### ENDURANCE ####
        # Indicateurs
        if self.stamina_full:
            pass
        if self.stamina_inprogress:
            pass
        if self.stamina_low:
            pass
        # Compteur
        pyxel.rectb(self.interface_x + 3, self.interface_y + 119, 40, 5, COLOR_BLACK)
        pyxel.rect(self.interface_x + 4, self.interface_y + 120, 100*(self.stamina/self.default_stamina) // 2.6, 3, COLOR_YELLOW)
        pyxel.blt(self.interface_x + 1, self.interface_y + 115, 0, 44, 66, 12, 12, COLOR_WHITE)
        ##### VIES #####
        # Indicateurs
        if self.lives_full:
            pass
        if self.lives_inprogress:
            pass
        if self.lives_low:
            pass
        # Compteur
        pyxel.rectb(self.interface_x + 85, self.interface_y + 119, 40, 5, COLOR_BLACK)
        pyxel.rect(self.interface_x + 86, self.interface_y + 120, (100 * (self.lives / self.default_lives)) // 2.6, 3, COLOR_RED)
        pyxel.blt(self.interface_x + 79, self.interface_y + 117, 0, 42, 84, 12, 12, COLOR_WHITE)
        ##### ABILITEES #####
        if self.ability != "":
            if self.index_statut:
                pyxel.line(self.x, self.y, self.index_x, self.index_y, COLOR_GREEN)
            if self.detector_statut:
                pyxel.line(self.x, self.y, self.detector_x, self.detector_y, COLOR_GREEN)
            if not self.stamina_statut:
                pyxel.rectb(self.interface_x + 3, self.interface_y + 119, 40, 5, COLOR_GREEN)
                pyxel.rect(self.interface_x + 4, self.interface_y + 120, 100*(self.stamina/self.default_stamina) // 2.6, 3, COLOR_LIGHTGREEN)
                pyxel.blt(self.interface_x + 1, self.interface_y + 115, 0, 44+16, 66, 12, 12, COLOR_WHITE)
            if self.ability_uses > 0:
                if round(self.ability_cooldown) > 0:
                    if round(self.ability_cooldown) <= 9:
                        pyxel.text(self.interface_x + 110, self.interface_y + 113, str(round(self.ability_cooldown)), COLOR_WHITE)
                    else:
                        pyxel.text(self.interface_x + 106, self.interface_y + 113, str(round(self.ability_cooldown)), COLOR_WHITE)
                if self.ability_inprogress:
                    color = COLOR_ORANGE
                else:
                    color = COLOR_GREEN
                for i in range(self.ability_uses):
                    pyxel.circ(self.interface_x + 116 + i*6, self.interface_y + 115, 2, color)

class Neighbor:
    def __init__(self, neighbor_x, neighbor_y, size_x, size_y, collisions):
        self.x = neighbor_x
        self.y = neighbor_y
        self.size_x = size_x
        self.size_y = size_y
        self.vertical_res_x = 195
        self.horizontal_res_x = 211
        self.collisions = collisions
        self.direction = 7
        self.trajectory = Decimal('1')
        self.player_x = 0
        self.player_y = 0
        self.player_size_x = 0
        self.player_size_y = 0
        self.player_visibility = True
        self.default_speed = 0.25
        self.speed = self.default_speed
        self.player_catched = False
        self.pause = 0
        self.islost_time = 0
        self.islost = False
        self.returning = False
        self.movements = []
        self.player_room = 10
        self.room = 8
        self.house_turn_count = 0

    def froom(self, x, y):
        if 220 < x < 255 and 24 < y < 59:
            return 0 # SALLE 0 - ARMOIRE
        elif 24 < x < 83 and 24 < y < 107:
            return 1 # SALLE 1 - BUREAU
        elif 112 < x < 175 and 24 < y < 107:
            return 2 # SALLE 2 - CAVE A VAIN
        elif 0 < x < 27 and 56 < y < 107:
            return 3 # SALLE 3 - WC
        elif 0 < x < 59 and 176 < y < 255:
            return 4 # SALLE 4 - SALLE CONTROLE
        elif 0 < x < 59 and 104 < y < 179:
            return 5 # SALLE 5 - CELLULE
        elif 56 < x < 147 and 136 < y < 223:
            return 6 # SALLE 6 - SALON
        elif 172 < x < 223 and 24 < y < 107:
            return 7 # SALLE 7 - LABORATOIRE
        elif 144 < x < 223 and 136 < y < 223:
            return 8 # SALLE 8 - ARMURERIE
        elif 80 < x < 115 and 52 < y < 107:
            return 9 # SALLE 9 - TELEPHONE
        elif x > 255 or x < 0 or y < 0 or y > 255:
            return -1 # SALLE INEXISTANTE
        else:
            if y < 56:
                return 10 # COULOIR 1
            elif y < 180:
                return 11 # Couloir 2 haut
            else:
                return 12 # COULOIR 2 bas
    
    def check_collision(self, x, y):
        for x1, y1, x2, y2, type in self.collisions:
            if x1 < x + self.size_x and y1 < y + self.size_y and x2 >= x and y2 >= y:
                if type == "Mur" or type == "Armoire":
                    return True
                elif type == "Meuble":
                    self.speed = self.speed / 2
                break
        return False
    
    def following_player(self):
        player_center_x = self.player_x + self.player_size_x // 2
        player_center_y = self.player_y + self.player_size_y // 2
        neighbor_center_x = self.x + self.size_x // 2
        neighbor_center_y = self.y + self.size_y // 2
        dx = player_center_x - neighbor_center_x
        dy = player_center_y - neighbor_center_y
        self.movements.append((self.x, self.y, self.direction))
        new_direction = self.direction
        moved = False

        directions = [(dx, 3, 7), (dy, 5, 1)]  # (delta, positive direction, negative direction)
        # Sort by the absolute value of delta to prioritize the largest move
        directions.sort(key=lambda d: abs(d[0]), reverse=True)

        for delta, pos_dir, neg_dir in directions:
            if not moved:
                if delta > 0:
                    new_direction = pos_dir
                    if pos_dir in [3, 7]:  # droite or gauche
                        if not self.check_collision(self.x + self.speed, self.y):
                            self.x += self.speed
                            moved = True
                    else:  # bas or haut
                        if not self.check_collision(self.x, self.y + self.speed):
                            self.y += self.speed
                            moved = True
                else:
                    new_direction = neg_dir
                    if neg_dir in [3, 7]:  # droite or gauche
                        if not self.check_collision(self.x - self.speed, self.y):
                            self.x -= self.speed
                            moved = True
                    else:  # bas or haut
                        if not self.check_collision(self.x, self.y - self.speed):
                            self.y -= self.speed
                            moved = True

        # Update direction based on movement direction
        if moved:
            self.direction = new_direction

    def unfollowing_player(self):
        if not self.islost:
            if self.movements == []:
                self.returning = False
            else:
                self.returning = True
                direction = self.movements[-1][2]
                if direction == 1:
                    self.direction = 5
                elif direction == 5:
                    self.direction = 1
                elif direction == 7:
                    self.direction = 3
                elif direction == 3:
                    self.direction = 7
                self.x = self.movements[-1][0]
                self.y = self.movements[-1][1]
                del self.movements[-1]
        else:
            self.islost_time += 1
            if self.islost_time >= 4*FPS:
                self.islost = False
                self.islost_time = 0
            elif self.islost_time >= 3*FPS:
                self.direction = 5
            elif self.islost_time >= 2*FPS:
                self.direction = 1
            elif self.islost_time >= 1*FPS:
                self.direction = 3
            elif self.islost_time >= 0:
                self.direction = 7

    # + de trajectoires secondaires/terciaires/inverses
    # Modifier trajectoires dans prison
    # Modifier random trajectoires
    def following_trajectory(self):
        if self.pause <= 0:

            ### ALLER ###

            if self.trajectory == Decimal('1'):
                self.direction = 7
                if self.x <= 129:
                    if random.randint(1, 1) > 1:
                        self.trajectory += Decimal('1')
                    else:
                        self.trajectory += Decimal('0.1')
            elif self.trajectory == Decimal('1.1'):
                self.direction = 1
                if self.y <= 152:
                    self.trajectory += Decimal('0.1')
                    self.direction = 1
                    self.pause = random.randint(1, 3)*FPS
            elif self.trajectory == Decimal('1.2'):
                self.direction = 5
                if self.y >= 171:
                    self.trajectory += Decimal('0.8')
            elif self.trajectory == Decimal('2'):
                self.direction = 5
                if self.y >= 191:
                    self.trajectory += Decimal('1')
            elif self.trajectory == Decimal('3'):
                self.direction = 7
                if self.x <= 69:
                    if random.randint(1, 1) > 1:
                        self.trajectory += Decimal('1')
                    else:
                        self.trajectory += Decimal('0.1')
            elif self.trajectory == Decimal('3.1'):
                self.direction = 1
                if self.y <= 152:
                    self.trajectory += Decimal('0.1')
                    self.direction = 1
                    self.pause = random.randint(1, 3)*FPS
            elif self.trajectory == Decimal('3.2'):
                self.direction = 5
                if self.y >= 191:
                    self.trajectory += Decimal('0.8')
            elif self.trajectory == Decimal('4'):
                self.direction = 5
                if self.y >= 201:
                    self.trajectory += Decimal('1')
            elif self.trajectory == Decimal('5'):
                self.direction = 7
                if self.x <= 38:
                    if random.randint(1, 1) > 1:
                        self.trajectory += Decimal('1')
                    else:
                        self.trajectory += Decimal('0.1')
            elif self.trajectory == Decimal('5.1'):
                self.direction = 1
                if self.y <= 198:
                    self.trajectory += Decimal('0.1')
            elif self.trajectory == Decimal('5.2'):
                self.direction = 7
                if self.x <= 17:
                    self.trajectory += Decimal('0.1')
                    self.direction = 7
                    self.pause = random.randint(4, 6)*FPS
            elif self.trajectory == Decimal('5.3'):
                self.direction = 3
                if self.x >= 38:
                    self.trajectory += Decimal('0.1')
            elif self.trajectory == Decimal('5.4'):
                self.direction = 5
                if self.y >= 201:
                    self.trajectory += Decimal('0.6')
            elif self.trajectory == Decimal('6'):
                self.direction = 5
                if self.y >= 233:
                    if random.randint(1, 1) > 1:
                        self.trajectory += Decimal('1')
                    else:
                        self.trajectory += Decimal('0.1')
            elif self.trajectory == Decimal('6.1'):
                self.direction = 5
                if self.y >= 235:
                    self.trajectory += Decimal('0.1')
            elif self.trajectory == Decimal('6.2'):
                self.direction = 7
                if self.x <= 17:
                    self.trajectory += Decimal('0.1')
                    self.direction = 7
                    self.pause = random.randint(1, 3)*FPS
            elif self.trajectory == Decimal('6.3'):
                self.direction = 3
                if self.x >= 38:
                    self.trajectory += Decimal('0.1')
            elif self.trajectory == Decimal('6.4'):
                self.direction = 1
                if self.y <= 233:
                    self.trajectory += Decimal('0.6')
            elif self.trajectory == Decimal('7'):
                self.direction = 3
                if self.x >= 233:
                    if random.randint(1, 1) > 1:
                        self.trajectory += Decimal('1')
                    else:
                        self.trajectory += Decimal('0.1')
            elif self.trajectory == Decimal('7.1'):
                self.direction = 3
                if self.x >= 256:
                    self.trajectory += Decimal('0.1')
                    self.direction = 3
                    self.pause = random.randint(1, 3)*FPS
            elif self.trajectory == Decimal('7.2'):
                self.direction = 7
                if self.x <= 233:
                    self.trajectory += Decimal('0.8')
            elif self.trajectory == Decimal('8'):
                self.direction = 1
                if self.y <= 117:
                    if random.randint(1, 1) > 1:
                        self.trajectory += Decimal('1')
                    else:
                        self.trajectory += Decimal('0.1')
            elif self.trajectory == Decimal('8.1'):
                self.direction = 1
                if self.y <= 77:
                    self.trajectory += Decimal('0.1')
                    self.direction = 1
                    self.pause = random.randint(1, 3)*FPS
            elif self.trajectory == Decimal('8.2'):
                self.direction = 5
                if self.y >= 117:
                    self.trajectory += Decimal('0.8')
            elif self.trajectory == Decimal('9'):
                self.direction = 7
                if self.x <= 137:
                    if random.randint(1, 1) > 1:
                        self.trajectory += Decimal('1')
                    else:
                        self.trajectory += Decimal('0.1')
            elif self.trajectory == Decimal('9.1'):
                self.direction = 7
                if self.x <= 93:
                    self.trajectory += Decimal('0.1')
            elif self.trajectory == Decimal('9.2'):
                self.direction = 1
                if self.y <= 82:
                    self.direction = 1
                    self.pause = random.randint(1, 3)*FPS
                    self.trajectory += Decimal('0.1')
            elif self.trajectory == Decimal('9.3'):
                self.direction = 5
                if self.y >= 117:
                    self.trajectory += Decimal('0.1')
            elif self.trajectory == Decimal('9.4'):
                self.direction = 7
                if self.x <= 77:
                    self.trajectory += Decimal('0.1')
                    self.direction = 7
                    self.pause = random.randint(1, 3)*FPS
            elif self.trajectory == Decimal('9.5'):
                self.direction = 3
                if self.x >= 137:
                    self.trajectory += Decimal('0.5')
            elif self.trajectory == Decimal('10'):
                self.direction = 1
                if self.y <= 91:
                    self.trajectory += Decimal('1')
            elif self.trajectory == Decimal('11'):
                self.direction = 3
                if self.x >= 149:
                    self.trajectory += Decimal('1')
            elif self.trajectory == Decimal('12'):
                self.direction = 1
                if self.y <= 37:
                    self.trajectory += Decimal('1')
            elif self.trajectory == Decimal('13'):
                self.direction = 7
                if self.x <= 137:
                    self.trajectory += Decimal('1')
            elif self.trajectory == Decimal('14'):
                self.direction = 1
                if self.y <= 9:
                    self.trajectory += Decimal('1')
            elif self.trajectory == Decimal('15'):
                self.direction = 3
                if self.x >= 193:
                    if random.randint(1, 1) > 1:
                        self.trajectory += Decimal('1')
                    else:
                        self.trajectory += Decimal('0.1')
            elif self.trajectory == Decimal('15.1'):
                self.direction = 5
                if self.y >= 31:
                    self.trajectory += Decimal('0.1')
            elif self.trajectory == Decimal('15.2'):
                self.direction = 3
                if self.x >= 208-self.size_x:
                    self.trajectory += Decimal('0.1')
                    self.direction = 3
                    self.pause = random.randint(1, 3)*FPS
            elif self.trajectory == Decimal('15.3'):
                self.direction = 5
                if self.y >= 45:
                    self.trajectory += Decimal('0.1')
                    self.direction = 3
                    self.pause = random.randint(1, 3)*FPS
            elif self.trajectory == Decimal('15.4'):
                self.direction = 7
                if self.x <= 179:
                    self.trajectory += Decimal('0.1')
            elif self.trajectory == Decimal('15.5'):
                self.direction = 5
                if self.y >= 73:
                    if random.randint(1, 1) > 1:
                        self.trajectory += Decimal('0.1')
                    else:
                        self.trajectory += Decimal('0.01')
            elif self.trajectory == Decimal('15.51'):
                self.direction = 3
                if self.x >= 204:
                    self.trajectory += Decimal('0.01')
                    self.direction = 1
                    self.pause = random.randint(1, 3)*FPS
            elif self.trajectory == Decimal('15.52'):
                self.direction = 7
                if self.x <= 179:
                    self.trajectory += Decimal('0.08')
            elif self.trajectory == Decimal('15.6'):
                self.direction = 1
                if self.y <= 37:
                    self.trajectory += Decimal('0.1')
            elif self.trajectory == Decimal('15.7'):
                self.direction = 3
                if self.x >= 193:
                    self.trajectory += Decimal('0.1')
            elif self.trajectory == Decimal('15.8'):
                self.direction = 1
                if self.y <= 9:
                    self.trajectory += Decimal('0.2')
            elif self.trajectory == Decimal('16'):
                self.direction = 3
                if self.x >= 233:
                    if random.randint(1, 1) > 1:
                        self.trajectory += Decimal('1')
                    else:
                        self.trajectory += Decimal('0.1')
            elif self.trajectory == Decimal('16.1'):
                self.direction = 5
                if self.y >= 31:
                    self.trajectory += Decimal('0.1')
                    self.direction = 5
                    self.pause = random.randint(1, 3)*FPS
            elif self.trajectory == Decimal('16.2'):
                self.direction = 1
                if self.y <= 9:
                    self.trajectory += Decimal('0.8')
            elif self.trajectory == Decimal('17'):
                self.direction = 7
                if self.x <= 9:
                    self.trajectory += Decimal('1')
            elif self.trajectory == Decimal('18'):
                self.direction = 5
                if self.y >= 37:
                    self.trajectory += Decimal('1')
            elif self.trajectory == Decimal('19'):
                self.direction = 3
                if self.x >= 31:
                    self.trajectory += Decimal('1')
            elif self.trajectory == Decimal('20'):
                self.direction = 5
                if self.y >= 69:
                    if random.randint(1, 1) > 1:
                        self.trajectory += Decimal('1')
                    else:
                        self.trajectory += Decimal('0.1')
            elif self.trajectory == Decimal('20.1'):
                self.direction = 7
                if self.x <= 9:
                    if random.randint(1, 1) > 1:
                        self.trajectory += Decimal('0.02')
                    else:
                        self.trajectory += Decimal('0.01')
            elif self.trajectory == Decimal('20.11'):
                self.direction = 5
                if self.y >= 87-self.size_y:
                    self.trajectory += Decimal('0.01')
                    self.direction = 5
                    self.pause = random.randint(1, 3)*FPS
            elif self.trajectory == Decimal('20.12'):
                self.direction = 1
                if self.y <= 66:
                    self.trajectory += Decimal('0.01')
                    self.direction = 1
                    self.pause = random.randint(1, 3)*FPS
            elif self.trajectory == Decimal('20.13'):
                self.direction = 5
                if self.y >= 69:
                    self.trajectory += Decimal('0.07')
            elif self.trajectory == Decimal('20.2'):
                self.direction = 3
                if self.x >= 31:
                    self.trajectory += Decimal('0.8')
            elif self.trajectory == Decimal('21'):
                self.direction = 5
                if self.y >= 91:
                    self.trajectory += Decimal('1')
            elif self.trajectory == Decimal('22'):
                self.direction = 3
                if self.x >= 37:
                    if random.randint(1, 1) > 1:
                        self.trajectory += Decimal('1')
                    else:
                        self.trajectory += Decimal('0.1')
            elif self.trajectory == Decimal('22.1'):
                self.direction = 5
                if self.y >= 115:
                    self.trajectory += Decimal('0.1')
            elif self.trajectory == Decimal('22.2'):
                self.direction = 7
                if self.x <= 22:
                    self.trajectory += Decimal('0.1')
            elif self.trajectory == Decimal('22.3'):
                self.direction = 5
                if self.y >= 159-self.size_y:
                    if random.randint(1, 1) > 1:
                        self.trajectory += Decimal('0.1')
                    else:
                        self.trajectory += Decimal('0.01')
            elif self.trajectory == Decimal('22.31'):
                self.direction = 3
                if self.x >= 43-self.size_x:
                    self.trajectory += Decimal('0.01')
                    self.direction = 3
                    self.pause = random.randint(1, 3)*FPS
            elif self.trajectory == Decimal('22.32'):
                self.direction = 7
                if self.x <= 22:
                    self.trajectory += Decimal('0.08')
            elif self.trajectory == Decimal('22.4'):
                self.direction = 1
                if self.y <= 115:
                    self.trajectory += Decimal('0.1')
            elif self.trajectory == Decimal('22.5'):
                self.direction = 3
                if self.x >= 37:
                    self.trajectory += Decimal('0.1')
            elif self.trajectory == Decimal('22.6'):
                self.direction = 1
                if self.y <= 91:
                    self.trajectory += Decimal('0.4')
            elif self.trajectory == Decimal('23'):
                self.direction = 3
                if self.x >= 67:
                    self.trajectory += Decimal('1')
            elif self.trajectory == Decimal('24'):
                self.direction = 1
                if self.y <= 64:
                    self.trajectory = Decimal('-24')
                    self.house_turn_count += 1
                    self.direction = 7
                    self.pause = random.randint(1, 3)*FPS

            ### RETOUR ###
            
            elif self.trajectory == Decimal('-24'):
                self.direction = 5
                if self.y >= 91:
                    self.trajectory += Decimal('1')
            elif self.trajectory == Decimal('-23'):
                self.direction = 7
                if self.x <= 37:
                    if random.randint(1, 1) > 1:
                        self.trajectory += Decimal('1')
                    else:
                        self.trajectory += Decimal('-0.1')
            elif self.trajectory == Decimal('-23.1'):
                self.direction = 5
                if self.y >= 115:
                    self.trajectory += Decimal('-0.1')
            elif self.trajectory == Decimal('-23.2'):
                self.direction = 7
                if self.x <= 22:
                    self.trajectory += Decimal('-0.1')
            elif self.trajectory == Decimal('-23.3'):
                self.direction = 5
                if self.y >= 159-self.size_y:
                    if random.randint(1, 1) > 1:
                        self.trajectory += Decimal('-0.1')
                    else:
                        self.trajectory += Decimal('-0.01')
            elif self.trajectory == Decimal('-23.31'):
                self.direction = 3
                if self.x >= 43-self.size_x:
                    self.trajectory += Decimal('-0.01')
                    self.direction = 3
                    self.pause = random.randint(1, 3)*FPS
            elif self.trajectory == Decimal('-23.32'):
                self.direction = 7
                if self.x <= 22:
                    self.trajectory += Decimal('-0.08')
            elif self.trajectory == Decimal('-23.4'):
                self.direction = 1
                if self.y <= 115:
                    self.trajectory += Decimal('-0.1')
            elif self.trajectory == Decimal('-23.5'):
                self.direction = 3
                if self.x >= 37:
                    self.trajectory += Decimal('-0.1')
            elif self.trajectory == Decimal('-23.6'):
                self.direction = 1
                if self.y <= 91:
                    self.trajectory += Decimal('1.6')
            elif self.trajectory == Decimal('-22'):
                self.direction = 7
                if self.x <= 31:
                    self.trajectory += Decimal('1')
            elif self.trajectory == Decimal('-21'):
                self.direction = 1
                if self.y <= 69:
                    if random.randint(1, 1) > 1:
                        self.trajectory += Decimal('1')
                    else:
                        self.trajectory += Decimal('-0.1')
            elif self.trajectory == Decimal('-21.1'):
                self.direction = 7
                if self.x <= 9:
                    if random.randint(1, 1) > 1:
                        self.trajectory += Decimal('-0.02')
                    else:
                        self.trajectory += Decimal('-0.01')
            elif self.trajectory == Decimal('-21.11'):
                self.direction = 5
                if self.y >= 87-self.size_y:
                    self.trajectory += Decimal('-0.01')
                    self.direction = 5
                    self.pause = random.randint(1, 3)*FPS
            elif self.trajectory == Decimal('-21.12'):
                self.direction = 1
                if self.y <= 66:
                    self.trajectory += Decimal('-0.01')
                    self.direction = 1
                    self.pause = random.randint(1, 3)*FPS
            elif self.trajectory == Decimal('-21.13'):
                self.direction = 5
                if self.y >= 69:
                    self.trajectory += Decimal('-0.07')
            elif self.trajectory == Decimal('-21.2'):
                self.direction = 3
                if self.x >= 31:
                    self.trajectory += Decimal('1.2')
            elif self.trajectory == Decimal('-20'):
                self.direction = 1
                if self.y <= 37:
                    self.trajectory += Decimal('1')
            elif self.trajectory == Decimal('-19'):
                self.direction = 7
                if self.x <= 9:
                    self.trajectory += Decimal('1')
            elif self.trajectory == Decimal('-18'):
                self.direction = 1
                if self.y <= 9:
                    self.trajectory += Decimal('1')
            elif self.trajectory == Decimal('-17'):
                self.direction = 3
                if self.x >= 193:
                    if random.randint(1, 1) > 1:
                        self.trajectory += Decimal('1')
                    else:
                        self.trajectory += Decimal('-0.1')
            elif self.trajectory == Decimal('-17.1'):
                self.direction = 5
                if self.y >= 31:
                    self.trajectory += Decimal('-0.1')
            elif self.trajectory == Decimal('-17.2'):
                self.direction = 3
                if self.x >= 208-self.size_x:
                    self.trajectory += Decimal('-0.1')
                    self.direction = 3
                    self.pause = random.randint(1, 3)*FPS
            elif self.trajectory == Decimal('-17.3'):
                self.direction = 5
                if self.y >= 45:
                    self.trajectory += Decimal('-0.1')
                    self.direction = 3
                    self.pause = random.randint(1, 3)*FPS
            elif self.trajectory == Decimal('-17.4'):
                self.direction = 7
                if self.x <= 179:
                    self.trajectory += Decimal('-0.1')
            elif self.trajectory == Decimal('-17.5'):
                self.direction = 5
                if self.y >= 73:
                    if random.randint(1, 1) > 1:
                        self.trajectory += Decimal('-0.1')
                    else:
                        self.trajectory += Decimal('-0.01')
            elif self.trajectory == Decimal('-17.51'):
                self.direction = 3
                if self.x >= 204:
                    self.trajectory += Decimal('-0.01')
                    self.direction = 1
                    self.pause = random.randint(1, 3)*FPS
            elif self.trajectory == Decimal('-17.52'):
                self.direction = 7
                if self.x <= 179:
                    self.trajectory += Decimal('-0.08')
            elif self.trajectory == Decimal('-17.6'):
                self.direction = 1
                if self.y <= 37:
                    self.trajectory += Decimal('-0.1')
            elif self.trajectory == Decimal('-17.7'):
                self.direction = 3
                if self.x >= 193:
                    self.trajectory += Decimal('-0.1')
            elif self.trajectory == Decimal('-17.8'):
                self.direction = 1
                if self.y <= 9:
                    self.trajectory += Decimal('1.8')
            elif self.trajectory == Decimal('-16'):
                self.direction = 3
                if self.x >= 233:
                    if random.randint(1, 1) > 1:
                        self.trajectory += Decimal('1')
                    else:
                        self.trajectory += Decimal('-0.1')
            elif self.trajectory == Decimal('-16.1'):
                self.direction = 5
                if self.y >= 31:
                    self.trajectory += Decimal('-0.1')
                    self.direction = 5
                    self.pause = random.randint(1, 3)*FPS
            elif self.trajectory == Decimal('-16.2'):
                self.direction = 1
                if self.y <= 9:
                    self.trajectory += Decimal('1.2')
            elif self.trajectory == Decimal('-15'):
                self.direction = 7
                if self.x <= 137:
                    self.trajectory += Decimal('1')
            elif self.trajectory == Decimal('-14'):
                self.direction = 5
                if self.y >= 37:
                    self.trajectory += Decimal('1')
            elif self.trajectory == Decimal('-13'):
                self.direction = 3
                if self.x >= 149:
                    self.trajectory += Decimal('1')
            elif self.trajectory == Decimal('-12'):
                self.direction = 5
                if self.y >= 91:
                    self.trajectory += Decimal('1')
            elif self.trajectory == Decimal('-11'):
                self.direction = 7
                if self.x <= 137:
                    self.trajectory += Decimal('1')
            elif self.trajectory == Decimal('-10'):
                self.direction = 5
                if self.y >= 117:
                    if random.randint(1, 1) > 1:
                        self.trajectory += Decimal('1')
                    else:
                        self.trajectory += Decimal('-0.1')
            elif self.trajectory == Decimal('-10.1'):
                self.direction = 7
                if self.x <= 93:
                    self.trajectory += Decimal('-0.1')
            elif self.trajectory == Decimal('-10.2'):
                self.direction = 1
                if self.y <= 82:
                    self.direction = 1
                    self.pause = random.randint(1, 3)*FPS
                    self.trajectory += Decimal('-0.1')
            elif self.trajectory == Decimal('-10.3'):
                self.direction = 5
                if self.y >= 117:
                    self.trajectory += Decimal('-0.1')
            elif self.trajectory == Decimal('-10.4'):
                self.direction = 7
                if self.x <= 77:
                    self.trajectory += Decimal('-0.1')
                    self.direction = 7
                    self.pause = random.randint(1, 3)*FPS
            elif self.trajectory == Decimal('-10.5'):
                self.direction = 3
                if self.x >= 137:
                    self.trajectory += Decimal('1.5')
            elif self.trajectory == Decimal('-9'):
                self.direction = 3
                if self.x >= 233:
                    if random.randint(1, 1) > 1:
                        self.trajectory += Decimal('1')
                    else:
                        self.trajectory += Decimal('-0.1')
            elif self.trajectory == Decimal('-9.1'):
                self.direction = 1
                if self.y <= 77:
                    self.trajectory += Decimal('-0.1')
                    self.direction = 1
                    self.pause = random.randint(1, 3)*FPS
            elif self.trajectory == Decimal('-9.2'):
                self.direction = 5
                if self.y >= 117:
                    self.trajectory += Decimal('1.2')
            elif self.trajectory == Decimal('-8'):
                self.direction = 5
                if self.y >= 233:
                    if random.randint(1, 1) > 1:
                        self.trajectory += Decimal('1')
                    else:
                        self.trajectory += Decimal('-0.1')
            elif self.trajectory == Decimal('-8.1'):
                self.direction = 3
                if self.x >= 260:
                    self.trajectory += Decimal('-0.1')
                    self.direction = 3
                    self.pause = random.randint(1, 3)*FPS
            elif self.trajectory == Decimal('-8.2'):
                self.direction = 7
                if self.x <= 233:
                    self.trajectory += Decimal('1.2')
            elif self.trajectory == Decimal('-7'):
                self.direction = 7
                if self.x <= 38:
                    if random.randint(1, 1) > 1:
                        self.trajectory += Decimal('1')
                    else:
                        self.trajectory += Decimal('-0.1')
            elif self.trajectory == Decimal('-7.1'):
                self.direction = 5
                if self.y >= 235:
                    self.trajectory += Decimal('-0.1')
            elif self.trajectory == Decimal('-7.2'):
                self.direction = 7
                if self.x <= 17:
                    self.trajectory += Decimal('-0.1')
                    self.direction = 7
                    self.pause = random.randint(1, 3)*FPS
            elif self.trajectory == Decimal('-7.3'):
                self.direction = 3
                if self.x >= 38:
                    self.trajectory += Decimal('-0.1')
            elif self.trajectory == Decimal('-7.4'):
                self.direction = 1
                if self.y <= 233:
                    self.trajectory += Decimal('1.4')             
            elif self.trajectory == Decimal('-6'):
                self.direction = 1
                if self.y <= 201:
                    if random.randint(1, 1) > 1:
                        self.trajectory += Decimal('1')
                    else:
                        self.trajectory += Decimal('-0.1')
            elif self.trajectory == Decimal('-6.1'):
                self.direction = 1
                if self.y <= 198:
                    self.trajectory += Decimal('-0.1')
            elif self.trajectory == Decimal('-6.2'):
                self.direction = 7
                if self.x <= 17:
                    self.trajectory += Decimal('-0.1')
                    self.direction = 7
                    self.pause = random.randint(1, 3)*FPS
            elif self.trajectory == Decimal('-6.3'):
                self.direction = 3
                if self.x >= 38:
                    self.trajectory += Decimal('-0.1')
            elif self.trajectory == Decimal('-6.4'):
                self.direction = 5
                if self.y >= 201:
                    self.trajectory += Decimal('1.4')
            elif self.trajectory == Decimal('-5'):
                self.direction = 3
                if self.x >= 69:
                    self.trajectory += Decimal('1')
            elif self.trajectory == Decimal('-4'):
                self.direction = 1
                if self.y <= 191:
                    if random.randint(1, 1) > 1:
                        self.trajectory += Decimal('1')
                    else:
                        self.trajectory += Decimal('-0.1')
            elif self.trajectory == Decimal('-4.1'):
                self.direction = 1
                if self.y <= 152:
                    self.trajectory += Decimal('-0.1')
                    self.direction = 1
                    self.pause = random.randint(1, 3)*FPS
            elif self.trajectory == Decimal('-4.2'):
                self.direction = 5
                if self.y >= 191:
                    self.trajectory += Decimal('1.2')
            elif self.trajectory == Decimal('-3'):
                self.direction = 3
                if self.x >= 129:
                    self.trajectory += Decimal('1')
            elif self.trajectory == Decimal('-2'):
                self.direction = 1
                if self.y <= 171:
                    if random.randint(1, 1) > 1:
                        self.trajectory += Decimal('1')
                    else:
                        self.trajectory += Decimal('-0.1')
            elif self.trajectory == Decimal('-2.1'):
                self.direction = 1
                if self.y <= 152:
                    self.trajectory += Decimal('-0.1')
                    self.direction = 1
                    self.pause = random.randint(1, 3)*FPS
            elif self.trajectory == Decimal('-2.2'):
                self.direction = 5
                if self.y >= 171:
                    self.trajectory += Decimal('1.2')
            elif self.trajectory == Decimal('-1'):
                self.direction = 3
                if self.x >= 206:
                    self.direction = 1
                    self.pause = random.randint(1, 3)*FPS
                    self.trajectory = Decimal('1')

            # Avancement
            if self.direction == 1:
                self.y -= self.speed
            elif self.direction == 3:
                self.x += self.speed
            elif self.direction == 5:
                self.y += self.speed
            elif self.direction == 7:
                self.x -= self.speed
        else:
            self.pause -= 1

    def catch_player(self):
        if self.x < self.player_x + self.player_size_x and self.x + self.size_x > self.player_x and self.y < self.player_y + self.player_size_y and self.y + self.size_y > self.player_y:
            self.player_catched = True

    # Voisin suit à des moments inappropriés (couloirs)
    # Voisin bete (arrête de suivre en changeant de salle/armoire)
    def update(self):
        self.speed = self.default_speed
        self.player_room = self.froom(self.player_x, self.player_y)
        self.room = self.froom(self.x, self.y)
        self.catch_player()
        if self.room == self.player_room and self.player_visibility and self.direction == 1 and self.player_y < self.y \
        or self.room == self.player_room and self.player_visibility and self.direction == 3 and self.player_x > self.x \
        or self.room == self.player_room and self.player_visibility and self.direction == 5 and self.player_y > self.y \
        or self.room == self.player_room and self.player_visibility and self.direction == 7 and self.player_x < self.x \
        or self.player_visibility and 220 < self.x and 220 < self.player_x and 56 < self.y and 56 < self.player_y and self.direction == 5 and self.player_y > self.y \
        or self.player_visibility and 220 < self.x and 220 < self.player_x and 56 < self.y and 56 < self.player_y and self.direction == 1 and self.player_y < self.y :
            self.returning = True
            self.islost = True
            self.speed = self.default_speed*3
            self.following_player()
        elif self.returning:
            self.speed = self.default_speed*2
            self.unfollowing_player()
        else:
            self.following_trajectory()

    def draw(self):
        if self.direction == 1:
            pyxel.blt(self.x, self.y, 0, self.vertical_res_x, 3, self.size_x, self.size_y, COLOR_WHITE)
        elif self.direction == 3:
            pyxel.blt(self.x, self.y, 0, self.horizontal_res_x, 3, self.size_x, self.size_y, COLOR_WHITE)
        elif self.direction == 5:
            pyxel.blt(self.x, self.y, 0, self.vertical_res_x, 3, -self.size_x, -self.size_y, COLOR_WHITE)
        elif self.direction == 7:
            pyxel.blt(self.x, self.y, 0, self.horizontal_res_x, 3, -self.size_x, -self.size_y, COLOR_WHITE)

class Interactive:
    def __init__(self, x, y, res_x, res_y, size_x, size_y, key):
        self.x = x
        self.y = y
        self.res_x = res_x
        self.res_y = res_y
        self.size_x = size_x
        self.size_y = size_y
        self.player_x = 0
        self.player_y = 0
        self.player_size_x = 0
        self.player_size_y = 0
        self.key = key
        self.isopen = False
        self.isnear = False
        self.KEY_INTERACT = pyxel.KEY_E
        self.key_isdisplay = 0
    
    def fisnear(self):
        h = abs(self.player_x - self.x)
        v = abs(self.player_y - self.y)
        self.isnear = False
        if h <= MARGE_INTERACTION + self.size_x and v <= MARGE_INTERACTION + self.size_y:
            self.isnear = True
            
    def update(self):
        self.fisnear()
        if self.isnear and pyxel.btnr(self.KEY_INTERACT):
            self.isopen = not self.isopen
            self.key_isdisplay = 1

    def draw(self):
        if self.isopen:
            pyxel.blt(self.x, self.y, 0, self.res_x, self.res_y, self.size_x, self.size_y, COLOR_WHITE)
        if self.isnear:
            pyxel.text(self.player_x+self.player_size_x+1, self.y+6, "!!", COLOR_RED)

class Hideouts:
    def __init__(self, x, y, res_x, res_y, size_x, size_y):
        self.x = x
        self.y = y
        self.res_x = res_x
        self.res_y = res_y
        self.size_x = size_x
        self.size_y = size_y
        self.player_x = 0
        self.player_y = 0
        self.player_size_x = 0
        self.player_size_y = 0
        self.isinside = False
    
    def finside(self):
        self.isinside = False
        if self.player_x >= self.x and self.player_x <= self.x + self.size_x and self.player_y + self.player_size_y >= self.y and self.player_y <= self.y + self.size_y:
            self.isinside = True

    def update(self):
        self.finside()

    def draw(self):
        if self.isinside:
            pyxel.blt(self.x, self.y, 0, self.res_x, self.res_y, self.size_x, self.size_y, COLOR_WHITE)
    
class Passages:
    def __init__(self, door_x, door_y, door_res_x, door_res_y, door_size_x, door_size_y, key_x, key_y, key_res_x, key_res_y, key_size_x, key_size_y):
        self.player_x = 0
        self.player_y = 0
        self.player_size_x = 0
        self.player_size_y = 0
        self.player_direction = 0
        self.door_statut = False
        self.door_x = door_x
        self.door_y = door_y
        self.door_res_x = door_res_x
        self.door_res_y = door_res_y
        self.door_size_x = door_size_x
        self.door_size_y = door_size_y
        self.key_statut = False
        self.key_x = key_x
        self.key_y = key_y
        self.key_res_x = key_res_x
        self.key_res_y = key_res_y
        self.key_size_x = key_size_x
        self.key_size_y = key_size_y
        self.key_display = 0
        self.key_isdisplay = True
        self.key_ishidden = False
        self.KEY_INTERACT = pyxel.KEY_E
    
    def frecovery(self):
        h = self.player_x - self.key_x
        v = self.player_y - self.key_y

        if pyxel.btn(self.KEY_INTERACT) and h >= -MARGE_INTERACTION - self.player_size_x and h <= MARGE_INTERACTION + self.key_size_x and v >= -MARGE_INTERACTION - self.player_size_y and v <= MARGE_INTERACTION + self.key_size_y:
            self.key_statut = True
    
    def foppening(self):
        h = abs(self.key_x - self.door_x)
        v = abs(self.key_y - self.door_y)
        
        if pyxel.btn(self.KEY_INTERACT) and h <= MARGE_INTERACTION + self.door_size_x and v <= MARGE_INTERACTION + self.door_size_y:
            self.door_statut = True

    def update(self):
        if self.key_statut:
            if not self.door_statut:
                self.foppening()
            if self.player_direction == 1:
                self.key_x = self.player_x-self.key_size_x//2
                self.key_y = self.player_y
            elif self.player_direction == 3:
                self.key_x = self.player_x+self.player_size_x//2
                self.key_y = self.player_y
            elif self.player_direction == 5:
                self.key_x = self.player_x+self.player_size_x//2
                self.key_y = self.player_y+self.key_size_y//2+self.player_size_y//2
            elif self.player_direction == 7:
                self.key_x = self.player_x-self.key_size_x//2
                self.key_y = self.player_y+self.key_size_y//2+self.player_size_y//2
        elif not self.key_ishidden:
            self.frecovery()
    
    def draw(self):
        if not self.door_statut:
            pyxel.blt(self.door_x, self.door_y, 0, self.door_res_x, self.door_res_y, self.door_size_x, self.door_size_y, COLOR_BLACK)
            if self.key_statut:
                pyxel.blt(self.key_x, self.key_y, 0, self.key_res_x, self.key_res_y, self.key_size_x, self.key_size_y, COLOR_BLACK)
            elif not self.key_ishidden:
                if self.key_display >= 1:
                    self.key_isdisplay = True
                elif self.key_display <= 0:
                    self.key_isdisplay = False
                if self.key_isdisplay:
                    pyxel.blt(self.key_x, self.key_y, 0, self.key_res_x, self.key_res_y, self.key_size_x, self.key_size_y, COLOR_BLACK)
                    self.key_display -= 1/(FPS*2)
                else:
                    self.key_display += 1/FPS

class Game:
    def __init__(self):
        
        ### ECRAN ###
        pyxel.init(WIDTH, HEIGHT+INTERFACE_SIZE_Y, title=TITLE, fps=FPS)
        self.screen = "Tutorial"
        self.settings_res_x = 43
        self.settings_res_y = 35
        self.settings_x = 59
        self.settings_size_x = 10
        self.settings_y = 5
        self.settings_size_y = 10
        self.onarrow_left = False
        self.onarrow_right = False
        self.onconfirm = False
        self.arrow1_res_x = 44
        self.arrow1_res_y = 50
        self.arrow1_size_x = 9
        self.arrow1_size_y = 12
        self.arrow2_res_x = 59
        self.arrow2_res_y = 49
        self.arrow2_size_x = 11
        self.arrow2_size_y = 14
        self.tutorial_page = 0
        self.tutorial_ended = False
        self.end_timer = 60*FPS

        ### COLLISIONS ###
        self.collisions = [
            ### Portes ###
            (228, 24, 247, 27, "Porte"), # 0
            (24, 32, 27, 51, "Porte"), # 1
            (132, 24, 151, 27, "Porte"), # 2
            (24, 64, 27, 83, "Porte"), # 3
            (132, 104, 151, 107, "Porte"), # 4
            (56, 228, 59, 247, "Porte"), # 5
            (32, 104, 51, 107, "Porte"), # 6
            (56, 196, 59, 215, "Porte"), # 7
            (188, 24, 207, 27, "Porte"), # 8
            (144, 166, 147, 185, "Porte"), # 9
            (88, 104, 107, 107, "Porte"), # 10
            ### Couloir 0 ###
            (4, 0, 16, 7, "Mur"), # Etagere
            ### Couloir 1 ###
            (224, 60, 251, 74, "Meuble"), # Bureau Droite
            (60, 108, 75, 135, "Meuble"), # Bureau Gauche
            ### Murs contours ###
            (0, 0, 255, 3, "Mur"), # Haut
            (0, 0, 3, 255, "Mur"), # Gauche
            (0, 252, 255, 255, "Mur"), # Bas
            (252, 0, 255, 255, "Mur"), # Droite
            ### SALLE 0 - ARMOIRE ###
            # Murs
            (208, 24, 227, 27, "Mur"), # Haut Gauche
            (248, 24, 255, 27, "Mur"), # Haut Droite
            (220, 24, 223, 107, "Mur"), # Gauche
            (220, 55, 255, 59, "Mur"), # Bas
            # Armoire
            (225, 44, 228, 46, "Armoire"), # Haut Gauche
            (225, 44, 225, 55, "Armoire"), # Gauche
            (225, 55, 250, 55, "Armoire"), # Bas
            (250, 44, 250, 55, "Armoire"), # Droite
            (247, 44, 250, 46, "Armoire"), # Haut Droite
            ### SALLE 1 - BUREAU ###
            # Murs
            (24, 24, 27, 31, "Mur"), # Gauche Haut
            (24, 52, 27, 63, "Mur"), # Gauche Milieu
            (24, 24, 131, 27, "Mur"), # Haut
            (80, 24, 83, 107, "Mur"), # Droite
            (52, 104, 87, 107, "Mur"), # Bas Droite
            (24, 84, 27, 107, "Mur"), # Gauche Bas
            (24, 104, 31, 107, "Mur"), # Bas Gauche
            # Bureau
            (56, 28, 63, 86, "Meuble"),
            (57, 32, 65, 46, "Meuble"), # Ordinateur
            # Chaises
            (45, 60, 55, 67, "Meuble"), # Gauche
            (69, 36, 76, 43, "Meuble"), # Droite
            ### SALLE 2 - CAVE A VAIN ###
            # Murs
            (152, 24, 187, 27, "Mur"), # Haut Droite
            (112, 24, 115, 107, "Mur"), # Gauche
            (112, 104, 131, 107, "Mur"), # Bas Gauche
            (152, 104, 223, 107, "Mur"), # Bas Droite
            (172, 24, 175, 107, "Mur"), # Droite
            # Casiers à bouteilles 
            (116, 28, 127, 103, "Mur"), # Gauche
            (160, 28, 171, 103, "Mur"), # Droite
            # Tonneaux 
            (126, 57, 139, 69, "Meuble"), # Haut
            (129, 66, 142, 79, "Meuble"), # Milieu
            (132, 73, 146, 86, "Meuble"), # Bas
            ### SALLE 3 - WC ###
            # Murs
            (0, 56, 27, 59, "Mur"), # Haut
            (0, 104, 31, 107, "Mur"), # Bas
            # Etagere
            (4, 60, 23, 63, "Meuble"), # Gauche
            # Toilettes
            (4, 90, 23, 103, "Meuble"),
            ### SALLE 4 - SALLE DE CONTROLE ###
            # Murs
            (0, 179, 59, 179, "Mur"), # Haut
            (56, 104, 59, 195, "Mur"), # Droite Haut
            (56, 216, 59, 227, "Mur"), # Droite Milieu
            (56, 248, 59, 255, "Mur"), # Droite Bas
            # Fauteuil
            (18, 217, 30, 230, "Meuble"),
            # Armoire
            (17, 180, 54, 180, "Armoire"), # Haut
            (17, 180, 17, 191, "Armoire"), # Droite
            (54, 180, 54, 191, "Armoire"), # Gauche
            (17, 189, 20, 191, "Armoire"), # Bas Gauche
            (51, 189, 54, 191, "Armoire"), # Bas Droite
            # Panneau de commandes
            (4, 180, 14, 251, "Meuble"),
            # Souris
            (16, 211, 20, 213, "Meuble"),
            ### SALLE 5 - CELLULE ###
            # Murs
            (0, 56, 27, 59, "Mur"), # Haut
            (10, 112, 17, 117, "Mur"), # Bas
            # Table
            (46, 129, 55, 175, "Meuble"),
            # Toilettes
            (8, 108, 19, 110, "Meuble"),            
            (8, 108, 19, 110, "Meuble"),            
            # Lit
            (6, 162, 41, 173, "Meuble"),
            # Chaise
            (35, 134, 42, 141, "Meuble"),            
            # Robinet
            (23, 108, 30, 111, "Meuble"),
            ### SALLE 6 - SALON ###
            # Murs
            (56, 136, 223, 139, "Mur"), # Haut
            (56, 220, 223, 223, "Mur"), # Bas
            (144, 136, 147, 165, "Mur"), # Droite Haut
            (144, 186, 147, 223, "Mur"), # Droite Bas
            # Table
            (90, 156, 122, 162, "Meuble"),
            # Fauteuil
            (90, 169, 122, 182, "Meuble"),            
            # Meubles
            (97, 209, 141, 217, "Meuble"), # Bas
            (62, 142, 141, 149, "Meuble"), # Haut
            ### SALLE 7 - LABORATOIRE ###
            # Murs
            (192, 56, 223, 59, "Mur"), # Centre
            # Paillasse
            (211, 28, 219, 55, "Meuble"),
            # Jardin
            (201, 60, 219, 70, "Meuble"),
            # Armoire
            (177, 90, 183, 92, "Armoire"), # Haut Gauche
            (177, 90, 177, 102, "Armoire"), # Gauche
            (177, 102, 218, 102, "Armoire"), # Bas
            (218, 90, 218, 102, "Armoire"), # Droite
            (212, 90, 218, 92, "Armoire"), # Haut Droite
            ### SALLE 7 - ARMURERIE ###
            # Murs + Etageres
            (144, 136, 223, 150, "Mur"), # Haut
            (144, 209, 223, 223, "Mur"), # Bas
            (209, 136, 223, 223, "Mur"), # Droite
            ### SALLE 8 - TELEPHONE ###
            # Murs
            (80, 52, 115, 55, "Mur"), # Haut
            # Meuble
            (89, 65, 106, 79, "Meuble"),
        ]
        
        ### PASSAGES ###
        #
        self.door_opened = 0
        self.key2_position = random.randint(1,2)
        self.key4_position = random.randint(1,2)
        self.key5_position = random.randint(1,4)
        self.key7_position = random.randint(1,2)
        self.key8_position = random.randint(1,2)
        # 0
        self.door0_x = 228
        self.door0_y = 22
        self.door0_res_x = 2
        self.door0_res_y = 36
        self.door0_size_x = 20
        self.door0_size_y = 8
        self.key0_x = 7
        self.key0_y = 5
        self.key0_res_x = 27
        self.key0_res_y = 38
        self.key0_size_x = 8
        self.key0_size_y = 3
        # 1
        self.door1_x = 22
        self.door1_y = 32
        self.door1_res_x = 4
        self.door1_res_y = 50
        self.door1_size_x = 6
        self.door1_size_y = 20
        self.key1_x = 234
        self.key1_y = 50
        self.key1_res_x = 22
        self.key1_res_y = 54
        self.key1_size_x = 6
        self.key1_size_y = 4
        # 2
        self.door2_x = 132
        self.door2_y = 22
        self.door2_res_x = 2
        self.door2_res_y = 76
        self.door2_size_x = 20
        self.door2_size_y = 8
        self.key2_x = 66
        if self.key2_position == 1: # Tiroir haut
            self.key2_y = 56
        else: # Tiroir bas
            self.key2_y = 77
        self.key2_res_x = 27
        self.key2_res_y = 78
        self.key2_size_x = 8
        self.key2_size_y = 3
        # 3
        self.door3_x = 22
        self.door3_y = 64
        self.door3_res_x = 4
        self.door3_res_y = 90
        self.door3_size_x = 8
        self.door3_size_y = 20
        self.key3_x = 121
        self.key3_y = 97
        self.key3_res_x = 22
        self.key3_res_y = 95
        self.key3_size_x = 8
        self.key3_size_y = 3
        # 4
        self.door4_x = 132
        self.door4_y = 101
        self.door4_res_x = 2
        self.door4_res_y = 115
        self.door4_size_x = 20
        self.door4_size_y = 10
        if self.key4_position == 1: # Etagere
            self.key4_x = 17
            self.key4_y = 60
        else: # Wc
            self.key4_x = 11
            self.key4_y = 90
        self.key4_res_x = 29
        self.key4_res_y = 118
        self.key4_size_x = 6
        self.key4_size_y = 4
        # 5
        self.door5_x = 54
        self.door5_y = 228
        self.door5_res_x = 4
        self.door5_res_y = 130
        self.door5_size_x = 8
        self.door5_size_y = 20
        if self.key5_position == 1: # Tiroir droite gauche
            self.key5_x = 228
            self.key5_y = 77
            self.key5_res_x = 19
            self.key5_res_y = 135
            self.key5_size_x = 3
            self.key5_size_y = 8
        elif self.key5_position == 2: # Tiroir droite droite
            self.key5_x = 245
            self.key5_y = 77
            self.key5_res_x = 19
            self.key5_res_y = 135
            self.key5_size_x = 3
            self.key5_size_y = 8
        elif self.key5_position == 3: # Tiroir gauche haut
            self.key5_x = 77
            self.key5_y = 112
            self.key5_res_x = 17
            self.key5_res_y = 129
            self.key5_size_x = 8
            self.key5_size_y = 3
        elif self.key5_position == 4: # Tiroir gauche bas
            self.key5_x = 77
            self.key5_y = 129
            self.key5_res_x = 17
            self.key5_res_y = 129
            self.key5_size_x = 8
            self.key5_size_y = 3
        # 6
        self.door6_x = 32
        self.door6_y = 102
        self.door6_res_x = 3
        self.door6_res_y = 156
        self.door6_size_x = 20
        self.door6_size_y = 6
        self.key6_x = 16
        self.key6_y = 242
        self.key6_res_x = 29
        self.key6_res_y = 158
        self.key6_size_x = 7
        self.key6_size_y = 3
        # 7
        self.door7_x = 54
        self.door7_y = 196
        self.door7_res_x = 4
        self.door7_res_y = 170
        self.door7_size_x = 6
        self.door7_size_y = 20
        if self.key7_position == 1: # Tiroir
            self.key7_x = 34
            self.key7_y = 151
            self.key7_res_x = 17
            self.key7_res_y = 169
            self.key7_size_x = 11
            self.key7_size_y = 3
        else: # Poster
            self.key7_x = 1
            self.key7_y = 132
            self.key7_res_x = 22
            self.key7_res_y = 172
            self.key7_size_x = 3
            self.key7_size_y = 11
        # 8
        self.door8_x = 188
        self.door8_y = 22
        self.door8_res_x = 2
        self.door8_res_y = 196
        self.door8_size_x = 20
        self.door8_size_y = 8
        if self.key8_position == 1: # Meuble
            self.key8_x = 134
            self.key8_y = 210
        else: # Tiroir
            self.key8_x = 72
            self.key8_y = 152
        self.key8_res_x = 29
        self.key8_res_y = 197
        self.key8_size_x = 6
        self.key8_size_y = 8
        # 9
        self.door9_x = 143
        self.door9_y = 166
        self.door9_res_x = 5
        self.door9_res_y = 210
        self.door9_size_x = 6
        self.door9_size_y = 20
        self.key9_x = 210
        self.key9_y = 73
        self.key9_res_x = 20
        self.key9_res_y = 214
        self.key9_size_x = 7
        self.key9_size_y = 4
        # 10
        self.door10_x = 88
        self.door10_y = 103
        self.door10_res_x = 1
        self.door10_res_y = 238
        self.door10_size_x = 20
        self.door10_size_y = 6
        self.key10_x = 158
        self.key10_y = 209
        self.key10_res_x = 25
        self.key10_res_y = 239
        self.key10_size_x = 19
        self.key10_size_y = 5
        # Initialisation
        self.passages = []
        self.passages.append(Passages(self.door0_x, self.door0_y, self.door0_res_x, self.door0_res_y, self.door0_size_x, self.door0_size_y, self.key0_x, self.key0_y, self.key0_res_x, self.key0_res_y, self.key0_size_x, self.key0_size_y))
        self.passages.append(Passages(self.door1_x, self.door1_y, self.door1_res_x, self.door1_res_y, self.door1_size_x, self.door1_size_y, self.key1_x, self.key1_y, self.key1_res_x, self.key1_res_y, self.key1_size_x, self.key1_size_y))
        self.passages.append(Passages(self.door2_x, self.door2_y, self.door2_res_x, self.door2_res_y, self.door2_size_x, self.door2_size_y, self.key2_x, self.key2_y, self.key2_res_x, self.key2_res_y, self.key2_size_x, self.key2_size_y))
        self.passages.append(Passages(self.door3_x, self.door3_y, self.door3_res_x, self.door3_res_y, self.door3_size_x, self.door3_size_y, self.key3_x, self.key3_y, self.key3_res_x, self.key3_res_y, self.key3_size_x, self.key3_size_y))
        self.passages.append(Passages(self.door4_x, self.door4_y, self.door4_res_x, self.door4_res_y, self.door4_size_x, self.door4_size_y, self.key4_x, self.key4_y, self.key4_res_x, self.key4_res_y, self.key4_size_x, self.key4_size_y))
        self.passages.append(Passages(self.door5_x, self.door5_y, self.door5_res_x, self.door5_res_y, self.door5_size_x, self.door5_size_y, self.key5_x, self.key5_y, self.key5_res_x, self.key5_res_y, self.key5_size_x, self.key5_size_y))
        self.passages.append(Passages(self.door6_x, self.door6_y, self.door6_res_x, self.door6_res_y, self.door6_size_x, self.door6_size_y, self.key6_x, self.key6_y, self.key6_res_x, self.key6_res_y, self.key6_size_x, self.key6_size_y))
        self.passages.append(Passages(self.door7_x, self.door7_y, self.door7_res_x, self.door7_res_y, self.door7_size_x, self.door7_size_y, self.key7_x, self.key7_y, self.key7_res_x, self.key7_res_y, self.key7_size_x, self.key7_size_y))
        self.passages.append(Passages(self.door8_x, self.door8_y, self.door8_res_x, self.door8_res_y, self.door8_size_x, self.door8_size_y, self.key8_x, self.key8_y, self.key8_res_x, self.key8_res_y, self.key8_size_x, self.key8_size_y))
        self.passages.append(Passages(self.door9_x, self.door9_y, self.door9_res_x, self.door9_res_y, self.door9_size_x, self.door9_size_y, self.key9_x, self.key9_y, self.key9_res_x, self.key9_res_y, self.key9_size_x, self.key9_size_y))
        self.passages.append(Passages(self.door10_x, self.door10_y, self.door10_res_x, self.door10_res_y, self.door10_size_x, self.door10_size_y, self.key10_x, self.key10_y, self.key10_res_x, self.key10_res_y, self.key10_size_x, self.key10_size_y))
        
        ### INTERACTIFS ###
        # COULOIR 1 :
        # Tiroir
        self.interactive0_x = 4
        self.interactive0_y = 0
        self.interactive0_res_x = 41
        self.interactive0_res_y = 100
        self.interactive0_size_x = 14
        self.interactive0_size_y = 10
        self.interactive0_key = 0
        # COULOIR 2 :
        # Tiroir gauche haut
        self.interactive1_x = 75
        self.interactive1_y = 109
        self.interactive1_res_x = 40
        self.interactive1_res_y = 132
        self.interactive1_size_x = 13
        self.interactive1_size_y = 9
        if self.key5_position == 3:
            self.interactive1_key = 5
        else:
            self.interactive1_key = -1        
        # Tiroir gauche bas
        self.interactive2_x = 75
        self.interactive2_y = 126
        self.interactive2_res_x = 40
        self.interactive2_res_y = 132
        self.interactive2_size_x = 13
        self.interactive2_size_y = 9
        if self.key5_position == 4:
            self.interactive2_key = 5
        else:
            self.interactive2_key = -1 
        # Tiroir droite gauche
        self.interactive3_x = 225
        self.interactive3_y = 75
        self.interactive3_res_x = 44
        self.interactive3_res_y = 144
        self.interactive3_size_x = 9
        self.interactive3_size_y = 13
        if self.key5_position == 1:
            self.interactive3_key = 5
        else:
            self.interactive3_key = -1 
        # Tiroir droite droite
        self.interactive4_x = 242
        self.interactive4_y = 75
        self.interactive4_res_x = 44
        self.interactive4_res_y = 144
        self.interactive4_size_x = 9
        self.interactive4_size_y = 13
        if self.key5_position == 2:
            self.interactive4_key = 5
        else:
            self.interactive4_key = -1 
        # BUREAU
        # Tiroir haut
        self.interactive5_x = 64
        self.interactive5_y = 53
        self.interactive5_res_x = 40
        self.interactive5_res_y = 116
        self.interactive5_size_x = 13
        self.interactive5_size_y = 9
        if self.key2_position == 1:
            self.interactive5_key = 2
        else:
            self.interactive5_key = -1
        # Tiroir bas
        self.interactive6_x = 64
        self.interactive6_y = 74
        self.interactive6_res_x = 40
        self.interactive6_res_y = 116
        self.interactive6_size_x = 13
        self.interactive6_size_y = 9
        if self.key2_position == 2:
            self.interactive6_key = 2
        else:
            self.interactive6_key = -1
        # # SALLE DE BAIN : 
        # # Wc
        # self.interactive7_x = 64
        # self.interactive7_y = 74
        # self.interactive7_res_x = 40
        # self.interactive7_res_y = 116
        # self.interactive7_size_x = 13
        # self.interactive7_size_y = 9
        # self.interactive7_key = -1
        # # Robinet
        # self.interactive8_x = 64
        # self.interactive8_y = 74
        # self.interactive8_res_x = 40
        # self.interactive8_res_y = 116
        # self.interactive8_size_x = 13
        # self.interactive8_size_y = 9
        # self.interactive8_key = -1
        # SALLE DE COMMANDE :
        # # Ecran
        # self.interactive9_x = 64
        # self.interactive9_y = 74
        # self.interactive9_res_x = 40
        # self.interactive9_res_y = 116
        # self.interactive9_size_x = 13
        # self.interactive9_size_y = 9
        # self.interactive9_key = -1
        # Tiroir
        self.interactive10_x = 16
        self.interactive10_y = 239
        self.interactive10_res_x = 40
        self.interactive10_res_y = 163
        self.interactive10_size_x = 13
        self.interactive10_size_y = 10
        self.interactive10_key = 6
        # # PRISON :
        # Tiroir
        self.interactive11_x = 45-13
        self.interactive11_y = 148
        self.interactive11_res_x = 40
        self.interactive11_res_y = 179
        self.interactive11_size_x = 13
        self.interactive11_size_y = 10
        if self.key7_position == 1:
            self.interactive11_key = 7
        else:
            self.interactive11_key = -1
        # Poster
        self.interactive12_x = 4
        self.interactive12_y = 128
        self.interactive12_res_x = 40
        self.interactive12_res_y = 208
        self.interactive12_size_x = 1
        self.interactive12_size_y = 16
        if self.key7_position == 2:
            self.interactive12_key = 7
        else:
            self.interactive12_key = -1
        # # Toilettes
        # self.interactive13_x = 64
        # self.interactive13_y = 74
        # self.interactive13_res_x = 40
        # self.interactive13_res_y = 116
        # self.interactive13_size_x = 13
        # self.interactive13_size_y = 9
        # self.interactive13_key = -1
        # # Robinet
        # self.interactive14_x = 64
        # self.interactive14_y = 74
        # self.interactive14_res_x = 40
        # self.interactive14_res_y = 116
        # self.interactive14_size_x = 13
        # self.interactive14_size_y = 9
        # self.interactive14_key = -1
        # # SALON :
        # Tiroir
        self.interactive15_x = 70
        self.interactive15_y = 150
        self.interactive15_res_x = 43
        self.interactive15_res_y = 192
        self.interactive15_size_x = 10
        self.interactive15_size_y = 13
        if self.key8_position == 2:
            self.interactive15_key = 8
        else:
            self.interactive15_key = -1
        
        # # SALLE FINALE :
        # # Telephone
        
        # Initialisation
        self.interactives = []
        self.interactives.append(Interactive(self.interactive0_x, self.interactive0_y, self.interactive0_res_x, self.interactive0_res_y, self.interactive0_size_x, self.interactive0_size_y, self.interactive0_key))
        self.interactives.append(Interactive(self.interactive1_x, self.interactive1_y, self.interactive1_res_x, self.interactive1_res_y, self.interactive1_size_x, self.interactive1_size_y, self.interactive1_key))
        self.interactives.append(Interactive(self.interactive2_x, self.interactive2_y, self.interactive2_res_x, self.interactive2_res_y, self.interactive2_size_x, self.interactive2_size_y, self.interactive2_key))
        self.interactives.append(Interactive(self.interactive3_x, self.interactive3_y, self.interactive3_res_x, self.interactive3_res_y, self.interactive3_size_x, self.interactive3_size_y, self.interactive3_key))
        self.interactives.append(Interactive(self.interactive4_x, self.interactive4_y, self.interactive4_res_x, self.interactive4_res_y, self.interactive4_size_x, self.interactive4_size_y, self.interactive4_key))
        self.interactives.append(Interactive(self.interactive5_x, self.interactive5_y, self.interactive5_res_x, self.interactive5_res_y, self.interactive5_size_x, self.interactive5_size_y, self.interactive5_key))
        self.interactives.append(Interactive(self.interactive6_x, self.interactive6_y, self.interactive6_res_x, self.interactive6_res_y, self.interactive6_size_x, self.interactive6_size_y, self.interactive6_key))
        # self.interactives.append(Interactive(self.interactive7_x, self.interactive7_y, self.interactive7_res_x, self.interactive7_res_y, self.interactive7_size_x, self.interactive7_size_y, self.interactive7_key))
        # self.interactives.append(Interactive(self.interactive8_x, self.interactive8_y, self.interactive8_res_x, self.interactive8_res_y, self.interactive8_size_x, self.interactive8_size_y, self.interactive8_key))
        # self.interactives.append(Interactive(self.interactive9_x, self.interactive9_y, self.interactive9_res_x, self.interactive9_res_y, self.interactive9_size_x, self.interactive9_size_y, self.interactive9_key))
        self.interactives.append(Interactive(self.interactive10_x, self.interactive10_y, self.interactive10_res_x, self.interactive10_res_y, self.interactive10_size_x, self.interactive10_size_y, self.interactive10_key))
        self.interactives.append(Interactive(self.interactive11_x, self.interactive11_y, self.interactive11_res_x, self.interactive11_res_y, self.interactive11_size_x, self.interactive11_size_y, self.interactive11_key))
        self.interactives.append(Interactive(self.interactive12_x, self.interactive12_y, self.interactive12_res_x, self.interactive12_res_y, self.interactive12_size_x, self.interactive12_size_y, self.interactive12_key))
        # self.interactives.append(Interactive(self.interactive13_x, self.interactive13_y, self.interactive13_res_x, self.interactive13_res_y, self.interactive13_size_x, self.interactive13_size_y, self.interactive13_key))
        # self.interactives.append(Interactive(self.interactive14_x, self.interactive14_y, self.interactive14_res_x, self.interactive14_res_y, self.interactive14_size_x, self.interactive14_size_y, self.interactive14_key))
        self.interactives.append(Interactive(self.interactive15_x, self.interactive15_y, self.interactive15_res_x, self.interactive15_res_y, self.interactive15_size_x, self.interactive15_size_y, self.interactive15_key))
        
        ### CACHETTES ###
        # 0
        self.hideout0_x = 225
        self.hideout0_y = 44
        self.hideout0_res_x = 33
        self.hideout0_res_y = 20
        self.hideout0_size_x = 25
        self.hideout0_size_y = 11
        # 1
        self.hideout1_x = 17
        self.hideout1_y = 180
        self.hideout1_res_x = 65
        self.hideout1_res_y = 20
        self.hideout1_size_x = 38
        self.hideout1_size_y = 11
        # 2
        self.hideout2_x = 177
        self.hideout2_y = 90
        self.hideout2_res_x = 105
        self.hideout2_res_y = 19
        self.hideout2_size_x = 41
        self.hideout2_size_y = 12
        # Initialisation
        self.hideouts = []
        self.hideouts.append(Hideouts(self.hideout0_x, self.hideout0_y, self.hideout0_res_x, self.hideout0_res_y, self.hideout0_size_x, self.hideout0_size_y))
        self.hideouts.append(Hideouts(self.hideout1_x, self.hideout1_y, self.hideout1_res_x, self.hideout1_res_y, self.hideout1_size_x, self.hideout1_size_y))
        self.hideouts.append(Hideouts(self.hideout2_x, self.hideout2_y, self.hideout2_res_x, self.hideout2_res_y, self.hideout2_size_x, self.hideout2_size_y))
        
        ### PERSONNAGES ###
        #
        self.default_player_x = 232
        self.default_player_y = 10
        self.player_stamina = 75
        self.player_direction = 1
        self.player_lives = 3
        self.player_ability_duration = 5
        self.player_ability_uses = 2
        self.player_ability_cooldown = 20
        self.selection_skin = 1
        self.skin_selected = 0
        #1
        self.player1_horizontal_res_x = 3
        self.player1_horizontal_res_y = 3
        self.player1_vertical_res_x = self.player1_horizontal_res_x+16
        self.player1_vertical_res_y = 3
        self.player1_size_x = 10
        self.player1_size_y = 10
        self.player1_ability = "Stamina"
        self.player1_ability_duration = 4
        #2
        self.player2_lives = self.player_lives+1
        self.player2_horizontal_res_x = self.player1_vertical_res_x+16
        self.player2_horizontal_res_y = 3
        self.player2_vertical_res_x = self.player2_horizontal_res_x+16
        self.player2_vertical_res_y = 3
        self.player2_size_x = 10
        self.player2_size_y = 10
        self.player2_ability = "Index"
        self.player2_ability_duration = 6
        #3
        self.player3_horizontal_res_x = self.player2_vertical_res_x+16
        self.player3_horizontal_res_y = 3
        self.player3_vertical_res_x = self.player3_horizontal_res_x+16
        self.player3_vertical_res_y = 3
        self.player3_size_x = 10
        self.player3_size_y = 10
        self.player3_ability = "Detector"
        self.player3_ability_duration = 6
        self.player3_default_stamina = self.player_stamina+25
        #4
        self.player4_horizontal_res_x = self.player3_vertical_res_x+16
        self.player4_horizontal_res_y = 3
        self.player4_vertical_res_x = self.player4_horizontal_res_x+16
        self.player4_vertical_res_y = 3
        self.player4_size_x = 10
        self.player4_size_y = 10
        self.player4_ability = "Invisibility"
        self.player4_ability_duration = 8
        #5
        self.player5_horizontal_res_x = 132
        self.player5_horizontal_res_y = 4
        self.player5_vertical_res_x = self.player5_horizontal_res_x+16
        self.player5_vertical_res_y = 4
        self.player5_size_x = 8
        self.player5_size_y = 8
        self.player5_ability = ""
        self.player5_ability_duration = 0
        self.player5_default_speed = 1
        self.player5_default_stamina = self.player_stamina-25
        # Initialisation
        self.player = Player(self.collisions, self.default_player_x, self.default_player_y, self.player_stamina, self.player_direction, self.player_lives, self.player1_ability, self.player_ability_uses, self.player_ability_duration, self.player_ability_cooldown)
        
        ### VOISIN ###
        #
        self.neighbor_size_x = 10
        self.neighbor_size_y = 10
        self.default_neighbor_x = 206-self.neighbor_size_x
        self.default_neighbor_y = 171
        # Initialisation
        self.neighbor = Neighbor(self.default_neighbor_x, self.default_neighbor_y, self.neighbor_size_x, self.neighbor_size_y, self.collisions)

        ### TOUCHES ###
        #
        self.KEYS = [
            pyxel.KEY_RETURN,
            pyxel.KEY_ESCAPE,
            pyxel.KEY_BACKSPACE,
            pyxel.KEY_TAB,
            pyxel.KEY_SPACE,
            pyxel.KEY_EXCLAIM,
            pyxel.KEY_QUOTEDBL,
            pyxel.KEY_HASH,
            pyxel.KEY_PERCENT,
            pyxel.KEY_DOLLAR,
            pyxel.KEY_AMPERSAND,
            pyxel.KEY_QUOTE,
            pyxel.KEY_LEFTPAREN,
            pyxel.KEY_RIGHTPAREN,
            pyxel.KEY_ASTERISK,
            pyxel.KEY_PLUS,
            pyxel.KEY_COMMA,
            pyxel.KEY_MINUS,
            pyxel.KEY_PERIOD,
            pyxel.KEY_SLASH,
            pyxel.KEY_0,
            pyxel.KEY_1,
            pyxel.KEY_2,
            pyxel.KEY_3,
            pyxel.KEY_4,
            pyxel.KEY_5,
            pyxel.KEY_6,
            pyxel.KEY_7,
            pyxel.KEY_8,
            pyxel.KEY_9,
            pyxel.KEY_COLON,
            pyxel.KEY_SEMICOLON,
            pyxel.KEY_LESS,
            pyxel.KEY_EQUALS,
            pyxel.KEY_GREATER,
            pyxel.KEY_QUESTION,
            pyxel.KEY_AT,
            pyxel.KEY_LEFTBRACKET,
            pyxel.KEY_BACKSLASH,
            pyxel.KEY_RIGHTBRACKET,
            pyxel.KEY_CARET,
            pyxel.KEY_UNDERSCORE,
            pyxel.KEY_BACKQUOTE,
            pyxel.KEY_A,
            pyxel.KEY_B,
            pyxel.KEY_C,
            pyxel.KEY_D,
            pyxel.KEY_E,
            pyxel.KEY_F,
            pyxel.KEY_G,
            pyxel.KEY_H,
            pyxel.KEY_I,
            pyxel.KEY_J,
            pyxel.KEY_K,
            pyxel.KEY_L,
            pyxel.KEY_M,
            pyxel.KEY_N,
            pyxel.KEY_O,
            pyxel.KEY_P,
            pyxel.KEY_Q,
            pyxel.KEY_R,
            pyxel.KEY_S,
            pyxel.KEY_T,
            pyxel.KEY_U,
            pyxel.KEY_V,
            pyxel.KEY_W,
            pyxel.KEY_X,
            pyxel.KEY_Y,
            pyxel.KEY_Z,
            pyxel.KEY_CAPSLOCK,
            pyxel.KEY_F1,
            pyxel.KEY_F2,
            pyxel.KEY_F3,
            pyxel.KEY_F4,
            pyxel.KEY_F5,
            pyxel.KEY_F6,
            pyxel.KEY_F7,
            pyxel.KEY_F8,
            pyxel.KEY_F9,
            pyxel.KEY_F10,
            pyxel.KEY_F11,
            pyxel.KEY_F12,
            pyxel.KEY_PRINTSCREEN,
            pyxel.KEY_SCROLLLOCK,
            pyxel.KEY_PAUSE,
            pyxel.KEY_INSERT,
            pyxel.KEY_HOME,
            pyxel.KEY_PAGEUP,
            pyxel.KEY_DELETE,
            pyxel.KEY_END,
            pyxel.KEY_PAGEDOWN,
            pyxel.KEY_RIGHT,
            pyxel.KEY_LEFT,
            pyxel.KEY_DOWN,
            pyxel.KEY_UP,
            pyxel.KEY_NUMLOCKCLEAR,
            pyxel.KEY_KP_DIVIDE,
            pyxel.KEY_KP_MULTIPLY,
            pyxel.KEY_KP_MINUS,
            pyxel.KEY_KP_PLUS,
            pyxel.KEY_KP_ENTER,
            pyxel.KEY_KP_1,
            pyxel.KEY_KP_2,
            pyxel.KEY_KP_3,
            pyxel.KEY_KP_4,
            pyxel.KEY_KP_5,
            pyxel.KEY_KP_6,
            pyxel.KEY_KP_7,
            pyxel.KEY_KP_8,
            pyxel.KEY_KP_9,
            pyxel.KEY_KP_0,
            pyxel.KEY_KP_PERIOD,
            pyxel.KEY_APPLICATION,
            pyxel.KEY_POWER,
            pyxel.KEY_KP_EQUALS,
            pyxel.KEY_F13,
            pyxel.KEY_F14,
            pyxel.KEY_F15,
            pyxel.KEY_F16,
            pyxel.KEY_F17,
            pyxel.KEY_F18,
            pyxel.KEY_F19,
            pyxel.KEY_F20,
            pyxel.KEY_F21,
            pyxel.KEY_F22,
            pyxel.KEY_F23,
            pyxel.KEY_F24,
            pyxel.KEY_EXECUTE,
            pyxel.KEY_HELP,
            pyxel.KEY_MENU,
            pyxel.KEY_SELECT,
            pyxel.KEY_STOP,
            pyxel.KEY_AGAIN,
            pyxel.KEY_UNDO,
            pyxel.KEY_CUT,
            pyxel.KEY_COPY,
            pyxel.KEY_PASTE,
            pyxel.KEY_FIND,
            pyxel.KEY_MUTE,
            pyxel.KEY_VOLUMEUP,
            pyxel.KEY_VOLUMEDOWN,
            pyxel.KEY_KP_EQUALSAS400,
            pyxel.KEY_ALTERASE,
            pyxel.KEY_SYSREQ,
            pyxel.KEY_CANCEL,
            pyxel.KEY_CLEAR,
            pyxel.KEY_PRIOR,
            pyxel.KEY_RETURN2,
            pyxel.KEY_SEPARATOR,
            pyxel.KEY_OUT,
            pyxel.KEY_OPER,
            pyxel.KEY_CLEARAGAIN,
            pyxel.KEY_CRSEL,
            pyxel.KEY_EXSEL,
            pyxel.KEY_KP_00,
            pyxel.KEY_KP_000,
            pyxel.KEY_THOUSANDSSEPARATOR,
            pyxel.KEY_DECIMALSEPARATOR,
            pyxel.KEY_CURRENCYUNIT,
            pyxel.KEY_CURRENCYSUBUNIT,
            pyxel.KEY_KP_LEFTPAREN,
            pyxel.KEY_KP_RIGHTPAREN,
            pyxel.KEY_KP_LEFTBRACE,
            pyxel.KEY_KP_RIGHTBRACE,
            pyxel.KEY_KP_TAB,
            pyxel.KEY_KP_BACKSPACE,
            pyxel.KEY_KP_A,
            pyxel.KEY_KP_B,
            pyxel.KEY_KP_C,
            pyxel.KEY_KP_D,
            pyxel.KEY_KP_E,
            pyxel.KEY_KP_F,
            pyxel.KEY_KP_XOR,
            pyxel.KEY_KP_POWER,
            pyxel.KEY_KP_PERCENT,
            pyxel.KEY_KP_LESS,
            pyxel.KEY_KP_GREATER,
            pyxel.KEY_KP_AMPERSAND,
            pyxel.KEY_KP_DBLAMPERSAND,
            pyxel.KEY_KP_VERTICALBAR,
            pyxel.KEY_KP_DBLVERTICALBAR,
            pyxel.KEY_KP_COLON,
            pyxel.KEY_KP_HASH,
            pyxel.KEY_KP_SPACE,
            pyxel.KEY_KP_AT,
            pyxel.KEY_KP_EXCLAM,
            pyxel.KEY_KP_MEMSTORE,
            pyxel.KEY_KP_MEMRECALL,
            pyxel.KEY_KP_MEMCLEAR,
            pyxel.KEY_KP_MEMADD,
            pyxel.KEY_KP_MEMSUBTRACT,
            pyxel.KEY_KP_MEMMULTIPLY,
            pyxel.KEY_KP_MEMDIVIDE,
            pyxel.KEY_KP_PLUSMINUS,
            pyxel.KEY_KP_CLEAR,
            pyxel.KEY_KP_CLEARENTRY,
            pyxel.KEY_KP_BINARY,
            pyxel.KEY_KP_OCTAL,
            pyxel.KEY_KP_DECIMAL,
            pyxel.KEY_KP_HEXADECIMAL,
            pyxel.KEY_LCTRL,
            pyxel.KEY_LSHIFT,
            pyxel.KEY_LALT,
            pyxel.KEY_LGUI,
            pyxel.KEY_RCTRL,
            pyxel.KEY_RSHIFT,
            pyxel.KEY_RALT,
            pyxel.KEY_RGUI,
            pyxel.KEY_SHIFT,
            pyxel.KEY_CTRL,
            pyxel.KEY_ALT,
            pyxel.KEY_GUI
        ]
        self.key_ismodify = False
        self.ismodify_ABILITY = False
        self.ismodify_SPRINT = False
        self.ismodify_INTERACT = False
        self.ismodify_UP = False
        self.ismodify_RIGHT = False
        self.ismodify_DOWN = False
        self.ismodify_LEFT = False
        self.ismodify_JUMP = False
        
        ### LANCEMENT ###
        pyxel.load("res.pyxres")
        pyxel.mouse(True)
        pyxel.run(self.update, self.draw)

    def tutorial_update(self):
        
        if pyxel.mouse_x >= WIDTH-20-self.arrow1_size_x and pyxel.mouse_x <= WIDTH-20-self.arrow1_size_x + self.arrow1_size_x and pyxel.mouse_y >= (HEIGHT+INTERFACE_SIZE_Y-self.arrow1_size_y)//2 and pyxel.mouse_y <= (HEIGHT+INTERFACE_SIZE_Y-self.arrow1_size_y)//2 + self.arrow1_size_y and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) or pyxel.btnp(pyxel.KEY_RIGHT):
            self.onarrow_right = True
            if self.tutorial_page != 5:
                self.tutorial_page += 1
            else:
                self.tutorial_ended = True
        elif pyxel.mouse_x >= 20 and pyxel.mouse_x <= 20 + self.arrow1_size_x and pyxel.mouse_y >= (HEIGHT+INTERFACE_SIZE_Y-self.arrow1_size_y)//2 and pyxel.mouse_y <= (HEIGHT+INTERFACE_SIZE_Y-self.arrow1_size_y)//2 + self.arrow1_size_y and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) or pyxel.btnp(pyxel.KEY_LEFT):
            if self.tutorial_page != 0:
                self.onarrow_left = True
                self.tutorial_page -= 1
        elif pyxel.mouse_x > 54 and pyxel.mouse_x < 54+20 and pyxel.mouse_y > (HEIGHT+INTERFACE_SIZE_Y)//2+17 and pyxel.mouse_y < (HEIGHT+INTERFACE_SIZE_Y)//2+17+9 and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) or pyxel.btnp(pyxel.KEY_E) or pyxel.btnp(pyxel.KEY_SPACE):
            self.onconfirm = True
        if pyxel.mouse_x > 54 and pyxel.mouse_x < 54+20 and pyxel.mouse_y > (HEIGHT+INTERFACE_SIZE_Y)//2+17 and pyxel.mouse_y < (HEIGHT+INTERFACE_SIZE_Y)//2+17+9 and pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT) or pyxel.btnr(pyxel.KEY_E) or pyxel.btnr(pyxel.KEY_SPACE):
            self.tutorial_ended = True

        if pyxel.btnr(pyxel.KEY_LEFT) or pyxel.btnr(pyxel.KEY_RIGHT) or pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT) or pyxel.btnr(pyxel.KEY_E) or pyxel.btnr(pyxel.KEY_SPACE):
            self.onconfirm = False
            self.onarrow_left = False
            self.onarrow_right = False

        if self.tutorial_ended:
            self.screen = "Selection"

    def tutorial_draw(self):

        pyxel.text(46, 20, "TUTORIEL :", COLOR_ORANGE)
        pyxel.blt(20, (HEIGHT+INTERFACE_SIZE_Y-self.arrow1_size_y)//2, 0, self.arrow1_res_x, self.arrow1_res_y, -self.arrow1_size_x, self.arrow1_size_y)
        if self.onarrow_left:
            pyxel.blt(20-1, (HEIGHT+INTERFACE_SIZE_Y-self.arrow2_size_y)//2-1, 0, self.arrow2_res_x, self.arrow2_res_y, -self.arrow2_size_x, self.arrow2_size_y)
        pyxel.blt(WIDTH-20-self.arrow1_size_x, (HEIGHT+INTERFACE_SIZE_Y-self.arrow1_size_y)//2, 0, self.arrow1_res_x, self.arrow1_res_y, self.arrow1_size_x, self.arrow1_size_y)
        if self.onarrow_right:
            pyxel.blt(WIDTH-20-self.arrow2_size_x, (HEIGHT+INTERFACE_SIZE_Y-self.arrow2_size_y)//2, 0, self.arrow2_res_x, self.arrow2_res_y, self.arrow2_size_x, self.arrow2_size_y)
        pyxel.rectb(54, (HEIGHT+INTERFACE_SIZE_Y)//2+17, 20, 9, COLOR_ORANGE)
        pyxel.text(56, (HEIGHT+INTERFACE_SIZE_Y)//2+19, "SKIP", COLOR_YELLOW)
        if self.onconfirm:
            pyxel.rectb(54-1, (HEIGHT+INTERFACE_SIZE_Y)//2+17-1, 20+2, 9+2, COLOR_RED)
            pyxel.text(56, (HEIGHT+INTERFACE_SIZE_Y)//2+19, "SKIP", COLOR_RED)
        if self.tutorial_page == 0:
            pyxel.text(SCREEN_CENTER_X-len("But : Appeler police")*2+1, SCREEN_CENTER_Y-40, "But : Appeler police", COLOR_YELLOW)
            pyxel.blt(SCREEN_CENTER_X-22//2, SCREEN_CENTER_Y-32//2, 1, 87, 62, 22, 32, 0)
        elif self.tutorial_page == 1:
            pyxel.text(SCREEN_CENTER_X-len("Vous pouvez")*2+1, SCREEN_CENTER_Y-40, "Vous pouvez", COLOR_YELLOW)
            pyxel.text(SCREEN_CENTER_X-len("Ramasser cles / Ouvrir portes")*2+1, SCREEN_CENTER_Y-30, "Ramasser cles / Ouvrir portes", COLOR_YELLOW)
            pyxel.blt(SCREEN_CENTER_X-35//2, SCREEN_CENTER_Y-9//2, 0, 1, 35, 35, 9, 0)
        elif self.tutorial_page == 2:
            pyxel.text(SCREEN_CENTER_X-len("Attention !")*2+1, SCREEN_CENTER_Y-40, "Attention !", COLOR_YELLOW)
            pyxel.text(SCREEN_CENTER_X-len("Ne vous faites pas attraper")*2+1, SCREEN_CENTER_Y-30, "Ne vous faites pas attraper", COLOR_YELLOW)
            pyxel.text(SCREEN_CENTER_X-len("par le voisin")*2+1, SCREEN_CENTER_Y-20, "par le voisin", COLOR_YELLOW)
            pyxel.blt(SCREEN_CENTER_X-11//2, SCREEN_CENTER_Y-11//2, 0, self.neighbor.vertical_res_x, 3, 11, 11, COLOR_WHITE)
        elif self.tutorial_page == 3:
            pyxel.text(SCREEN_CENTER_X-len("Vous pouvez vous cacher")*2+1, SCREEN_CENTER_Y-40, "Vous pouvez vous cacher", COLOR_YELLOW)
            pyxel.text(SCREEN_CENTER_X-len("dans ces armoires :")*2+1, SCREEN_CENTER_Y-30, "dans ces armoires :", COLOR_YELLOW)
            pyxel.blt(SCREEN_CENTER_X-29//2, SCREEN_CENTER_Y-15//2, 0, 31, 18, 29, 15, COLOR_WHITE)
        elif self.tutorial_page == 4:
            pyxel.text(SCREEN_CENTER_X-len("Vous pouvez actionner le decor")*2+1, SCREEN_CENTER_Y-40, "Vous pouvez actionner le decor", COLOR_YELLOW)
            pyxel.text(SCREEN_CENTER_X-len("lorsque vous voyez : '!!'")*2+1, SCREEN_CENTER_Y-30, "lorsque vous voyez : '!!'", COLOR_YELLOW)
            pyxel.text(SCREEN_CENTER_X-len("a cote de votre personnage")*2+1, SCREEN_CENTER_Y-20, "a cote de votre personnage", COLOR_YELLOW)
            # pyxel.text(SCREEN_CENTER_X-len("(en developpement)")*2+1, SCREEN_CENTER_Y-10, "(en developpement)", COLOR_YELLOW)
        elif self.tutorial_page == 5:
            pyxel.text(SCREEN_CENTER_X-len("Touches :")*2+1, SCREEN_CENTER_Y-40, "Touches :", COLOR_YELLOW)
            pyxel.text(SCREEN_CENTER_X-len("(Toutes sont modifiables)")*2+1, SCREEN_CENTER_Y-30, "(Toutes sont modifiables)", COLOR_YELLOW)
            pyxel.text(SCREEN_CENTER_X-len("Movements = ZQSD")*2+1, SCREEN_CENTER_Y-20, "Movements: ZQSD", COLOR_YELLOW)
            pyxel.text(SCREEN_CENTER_X-len("Ability = A")*2+1, SCREEN_CENTER_Y-10, "Ability: A", COLOR_YELLOW)
            pyxel.text(SCREEN_CENTER_X-len("Interact = E")*2+1, SCREEN_CENTER_Y, "Interact: E", COLOR_YELLOW)
            pyxel.text(SCREEN_CENTER_X-len("Climb: ESPACE (maintenir)")*2+1, SCREEN_CENTER_Y+10, "Climb: ESPACE (maintenir)", COLOR_YELLOW)
        elif self.tutorial_page == 6:
            pyxel.text(SCREEN_CENTER_X-len("Bonne chance !")*2+1, SCREEN_CENTER_Y, "Bonne chance !", COLOR_YELLOW)
            
    def selection_update(self):
        
        
        if pyxel.mouse_x >= WIDTH-35-self.arrow1_size_x and pyxel.mouse_x <= WIDTH-35-self.arrow1_size_x + self.arrow1_size_x and pyxel.mouse_y >= (HEIGHT+INTERFACE_SIZE_Y-self.arrow1_size_y)//2 and pyxel.mouse_y <= (HEIGHT+INTERFACE_SIZE_Y-self.arrow1_size_y)//2 + self.arrow1_size_y and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) or pyxel.btnp(pyxel.KEY_RIGHT):
            self.onarrow_right = True
            if self.selection_skin != 5:
                self.selection_skin += 1
            else:
                self.onarrow_right = False
        elif pyxel.mouse_x >= 35 and pyxel.mouse_x <= 35 + self.arrow1_size_x and pyxel.mouse_y >= (HEIGHT+INTERFACE_SIZE_Y-self.arrow1_size_y)//2 and pyxel.mouse_y <= (HEIGHT+INTERFACE_SIZE_Y-self.arrow1_size_y)//2 + self.arrow1_size_y and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) or pyxel.btnp(pyxel.KEY_LEFT):
            self.onarrow_left = True
            if self.selection_skin != 1:
                self.selection_skin -= 1
            else:
                self.onarrow_left = False

        elif pyxel.mouse_x > 48 and pyxel.mouse_x < 48+32 and pyxel.mouse_y > (HEIGHT+INTERFACE_SIZE_Y)//2+17 and pyxel.mouse_y < (HEIGHT+INTERFACE_SIZE_Y)//2+17+9 and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) or pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.KEY_E):
            self.onconfirm = True
        if pyxel.mouse_x > 48 and pyxel.mouse_x < 48+32 and pyxel.mouse_y > (HEIGHT+INTERFACE_SIZE_Y)//2+17 and pyxel.mouse_y < (HEIGHT+INTERFACE_SIZE_Y)//2+17+9 and pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT) or pyxel.btnr(pyxel.KEY_SPACE) or pyxel.btnr(pyxel.KEY_E):
            self.skin_selected = self.selection_skin

        if pyxel.btnr(pyxel.KEY_LEFT) or pyxel.btnr(pyxel.KEY_RIGHT) or pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT) or pyxel.btnr(pyxel.KEY_E) or pyxel.btnr(pyxel.KEY_SPACE):
            self.onconfirm = False
            self.onarrow_left = False
            self.onarrow_right = False

        if self.skin_selected == 1:
            self.player.horizontal_res_x = self.player1_horizontal_res_x
            self.player.horizontal_res_y = self.player1_horizontal_res_y
            self.player.vertical_res_x = self.player1_vertical_res_x
            self.player.vertical_res_y = self.player1_vertical_res_y
            self.player.size_x = self.player1_size_x
            self.player.size_y = self.player1_size_y
            self.player.ability =  self.player1_ability
            self.player.default_ability_duration = self.player1_ability_duration
            self.player.ability_duration = self.player1_ability_duration
        elif self.skin_selected == 2:
            self.player.horizontal_res_x = self.player2_horizontal_res_x
            self.player.horizontal_res_y = self.player2_horizontal_res_y
            self.player.vertical_res_x = self.player2_vertical_res_x
            self.player.vertical_res_y = self.player2_vertical_res_y
            self.player.size_x = self.player2_size_x
            self.player.size_y = self.player2_size_y
            self.player.ability =  self.player2_ability
            self.player.default_ability_duration = self.player2_ability_duration
            self.player.ability_duration = self.player2_ability_duration
            self.player.default_lives = self.player2_lives
            self.player.lives = self.player2_lives
        elif self.skin_selected == 3:
            self.player.horizontal_res_x = self.player3_horizontal_res_x
            self.player.horizontal_res_y = self.player3_horizontal_res_y
            self.player.vertical_res_x = self.player3_vertical_res_x
            self.player.vertical_res_y = self.player3_vertical_res_y
            self.player.size_x = self.player3_size_x
            self.player.size_y = self.player3_size_y
            self.player.ability =  self.player3_ability
            self.player.default_ability_duration = self.player3_ability_duration
            self.player.ability_duration = self.player3_ability_duration
            self.player.default_stamina = self.player3_default_stamina
            self.player.stamina = self.player3_default_stamina
        elif self.skin_selected == 4:
            self.player.horizontal_res_x = self.player4_horizontal_res_x
            self.player.horizontal_res_y = self.player4_horizontal_res_y
            self.player.vertical_res_x = self.player4_vertical_res_x
            self.player.vertical_res_y = self.player4_vertical_res_y
            self.player.size_x = self.player4_size_x
            self.player.size_y = self.player4_size_y
            self.player.ability =  self.player4_ability
            self.player.default_ability_duration = self.player4_ability_duration
            self.player.ability_duration = self.player4_ability_duration
        elif self.skin_selected == 5:
            self.player.horizontal_res_x = self.player5_horizontal_res_x
            self.player.horizontal_res_y = self.player5_horizontal_res_y
            self.player.vertical_res_x = self.player5_vertical_res_x
            self.player.vertical_res_y = self.player5_vertical_res_y
            self.player.size_x = self.player5_size_x
            self.player.size_y = self.player5_size_y
            self.player.ability =  self.player5_ability
            self.player.default_ability_duration = self.player5_ability_duration
            self.player.ability_duration = self.player5_ability_duration
            self.player.default_speed = self.player5_default_speed
            self.player.default_stamina = self.player5_default_stamina
            self.player.stamina = self.player5_default_stamina
        
        if self.skin_selected != 0:
            self.screen = "Game"

    def selection_draw(self):
        
        
        pyxel.text(30, 20, "Player selection :", COLOR_ORANGE)
        pyxel.blt(35, (HEIGHT+INTERFACE_SIZE_Y-self.arrow1_size_y)//2, 0, self.arrow1_res_x, self.arrow1_res_y, -self.arrow1_size_x, self.arrow1_size_y)
        if self.onarrow_left:
            pyxel.blt(35-1, (HEIGHT+INTERFACE_SIZE_Y-self.arrow2_size_y)//2-1, 0, self.arrow2_res_x, self.arrow2_res_y, -self.arrow2_size_x, self.arrow2_size_y)
        pyxel.blt(WIDTH-35-self.arrow1_size_x, (HEIGHT+INTERFACE_SIZE_Y-self.arrow1_size_y)//2, 0, self.arrow1_res_x, self.arrow1_res_y, self.arrow1_size_x, self.arrow1_size_y)
        if self.onarrow_right:
            pyxel.blt(WIDTH-35-self.arrow2_size_x, (HEIGHT+INTERFACE_SIZE_Y-self.arrow2_size_y)//2, 0, self.arrow2_res_x, self.arrow2_res_y, self.arrow2_size_x, self.arrow2_size_y)
        pyxel.rectb(48, (HEIGHT+INTERFACE_SIZE_Y)//2+17, 32, 9, COLOR_ORANGE)
        pyxel.text(52, (HEIGHT+INTERFACE_SIZE_Y)//2+19, "SELECT", COLOR_YELLOW)
        if self.onconfirm:
            pyxel.rectb(48-1, (HEIGHT+INTERFACE_SIZE_Y)//2+17-1, 32+2, 9+2, COLOR_RED)
            pyxel.text(52, (HEIGHT+INTERFACE_SIZE_Y)//2+19, "SELECT", COLOR_RED)
        if self.selection_skin == 1:
            pyxel.blt(60, (HEIGHT+INTERFACE_SIZE_Y-self.player1_size_y)//2, 0, self.player1_horizontal_res_x, self.player1_horizontal_res_y, self.player1_size_x, self.player1_size_y, COLOR_WHITE)
            pyxel.text(5, 110, "Abilitee : Endurance illimitee", COLOR_WHITE)
            pyxel.text(5, 120, "Duree : " + str(self.player1_ability_duration) + " secondes", COLOR_WHITE)
            pyxel.text(5, 130, "Passif : Aucun", COLOR_WHITE)
        elif self.selection_skin == 2:
            pyxel.blt(60, (HEIGHT+INTERFACE_SIZE_Y-self.player2_size_y)//2, 0, self.player2_horizontal_res_x, self.player2_horizontal_res_y, self.player2_size_x, self.player2_size_y, COLOR_WHITE)
            pyxel.text(5, 110, "Abilitee : Indice", COLOR_WHITE)
            pyxel.text(5, 120, "Duree : " + str(self.player2_ability_duration) + " secondes", COLOR_WHITE)
            pyxel.text(5, 130, "Passif : +1 Vie", COLOR_WHITE)
        elif self.selection_skin == 3:
            pyxel.blt(60, (HEIGHT+INTERFACE_SIZE_Y-self.player3_size_y)//2, 0, self.player3_horizontal_res_x, self.player3_horizontal_res_y, self.player3_size_x, self.player3_size_y, COLOR_WHITE)
            pyxel.text(5, 110, "Abilitee : Localise le voisin", COLOR_WHITE)
            pyxel.text(5, 120, "Duree : " + str(self.player3_ability_duration) + " secondes", COLOR_WHITE)
            pyxel.text(5, 130, "Passif : +25 endurance max", COLOR_WHITE)
        elif self.selection_skin == 4:
            pyxel.blt(60, (HEIGHT+INTERFACE_SIZE_Y-self.player4_size_y)//2, 0, self.player4_horizontal_res_x, self.player4_horizontal_res_y, self.player4_size_x, self.player4_size_y, COLOR_WHITE)
            pyxel.text(5, 110, "Abilitee : Invisibilitee", COLOR_WHITE)
            pyxel.text(5, 120, "Duree : " + str(self.player4_ability_duration) + " secondes", COLOR_WHITE)
            pyxel.text(5, 130, "Passif : Aucun", COLOR_WHITE)
        elif self.selection_skin == 5:
            pyxel.blt(60, (HEIGHT+INTERFACE_SIZE_Y-self.player5_size_y)//2, 0, self.player5_horizontal_res_x, self.player5_horizontal_res_y, self.player5_size_x, self.player5_size_y, COLOR_WHITE)
            pyxel.text(5, 110, "Abilitee : Aucune", COLOR_WHITE)
            pyxel.text(5, 120, "Duree : 0 secondes", COLOR_WHITE)
            pyxel.text(5, 130, "Passif : Petit", COLOR_WHITE)

    def game_update(self):
        # Changements d'écran
        if self.player.x >= 88 and self.player.y >= 81 and self.player.x <= 107 and self.player.y <= 93 and pyxel.btnp(self.interactives[0].KEY_INTERACT):
            self.player.collisions.append((228, 44, 247, 44, "Meuble"))
            self.player.collisions.append((20, 191, 51, 191, "Meuble"))
            self.player.collisions.append((184, 90, 211, 90, "Meuble"))
            self.screen = "End"
        elif pyxel.mouse_x >= self.settings_x and pyxel.mouse_x <= self.settings_x + self.settings_size_x and pyxel.mouse_y >= HEIGHT + self.settings_y and pyxel.mouse_y <= HEIGHT + self.settings_y + self.settings_size_y and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            self.screen = "Settings"
        # Interactifs
        for interactive in self.interactives:
            interactive.player_x = self.player.x
            interactive.player_y = self.player.y
            interactive.player_size_x = self.player.size_x
            interactive.player_size_y = self.player.size_y
            if interactive.key_isdisplay == 1:
                interactive.key_isdisplay = 0
                self.passages[0].key_display = 1
            if interactive.key != -1:
                self.passages[interactive.key - self.door_opened].key_ishidden = True
                if interactive.isopen:
                    self.passages[interactive.key - self.door_opened].key_ishidden = False
                    if self.passages[interactive.key - self.door_opened].key_statut:
                        interactive.key = -1
            interactive.update()
        # Portes
        for passage in self.passages:
            passage.player_x = self.player.x
            passage.player_y = self.player.y
            passage.player_size_x = self.player.size_x
            passage.player_size_y = self.player.size_y
            passage.player_direction = self.player.direction
            passage.update()
            if passage.door_statut:
                self.door_opened += 1
                del self.passages[0]
                if self.player.collisions != []:
                    del self.player.collisions[0]
        # Cachettes
        for hideout in self.hideouts:
            hideout.player_x = self.player.x
            hideout.player_y = self.player.y
            hideout.player_size_x = self.player.size_x
            hideout.player_size_y = self.player.size_y
            hideout.update()
        # Personnage
        self.player.update()
        if self.player.lives == 0:
            self.screen = "Lost"
        if self.player.ability == "Detector":
            self.player.detector_x = self.neighbor.x
            self.player.detector_y = self.neighbor.y
        elif self.player.ability == "Index":
            if len(self.passages) > 0:
                if not self.passages[0].key_statut:
                    self.player.index_x = self.passages[0].key_x
                    self.player.index_y = self.passages[0].key_y
                else:
                    self.player.index_x = self.passages[0].door_x
                    self.player.index_y = self.passages[0].door_y
            else:
                self.player.ability_uses = 0
        # Voisin
        self.neighbor.update()
        visibility = []
        for hideout in self.hideouts:
            visibility.append(hideout.isinside)
        if True in visibility or not self.player.visibility_statut:
            self.neighbor.player_visibility = False
        else:
            self.neighbor.player_visibility = True
        self.neighbor.player_x = self.player.x
        self.neighbor.player_y = self.player.y
        self.neighbor.player_size_x = self.player.size_x
        self.neighbor.player_size_y = self.player.size_y
        if self.neighbor.player_catched:
            self.neighbor = Neighbor(self.default_neighbor_x, self.default_neighbor_y, self.neighbor_size_x, self.neighbor_size_y, self.collisions)
            self.player.x = self.default_player_x
            self.player.y = self.default_player_y
            self.player.lives -= 1
            if self.passages[0].key_statut:
                self.passages[0].key_statut = False
    
    def game_draw(self):
        # Tilemap
        pyxel.blt(0, 0, 1, 0, 0, 256, 256)
        # Interactions
        if self.player.x >= 88 and self.player.y >= 81 and self.player.x <= 107 and self.player.y <= 93:
            pyxel.text(85, 85, "!!", COLOR_RED)
        for interactive in self.interactives:
            interactive.draw()
        # Cachettes
        for hideout in self.hideouts:
            hideout.draw()
        # Passages
        for passage in self.passages:
            passage.draw()
        # Interface
        pyxel.rect(self.player.interface_x, self.player.interface_y+HEIGHT-INTERFACE_SIZE_Y, WIDTH, 2, COLOR_ROSE)
        pyxel.rect(self.player.interface_x, self.player.interface_y+HEIGHT-INTERFACE_SIZE_Y+1, WIDTH, INTERFACE_SIZE_Y, COLOR_LIGHTBLUE)
        pyxel.blt(self.player.interface_x+self.settings_x, self.player.interface_y+HEIGHT-INTERFACE_SIZE_Y+self.settings_y, 0, self.settings_res_x, self.settings_res_y, self.settings_size_x, self.settings_size_y, 0)
        # Player
        self.player.draw()
        # Voisin
        self.neighbor.draw()

    def settings_update(self):
        if self.key_ismodify:
            key = 0
            for i in self.KEYS:
                if pyxel.btnp(i):
                    key = i
                    break
            if key != 0:
                if self.ismodify_JUMP:
                    self.ismodify_JUMP = False
                    self.player.KEY_JUMP = key
                elif self.ismodify_LEFT:
                    self.ismodify_LEFT = False
                    self.player.KEY_LEFT = key
                elif self.ismodify_RIGHT:
                    self.ismodify_RIGHT = False
                    self.player.KEY_RIGHT = key
                elif self.ismodify_UP:
                    self.ismodify_UP = False
                    self.player.KEY_UP = key
                elif self.ismodify_DOWN:
                    self.ismodify_DOWN = False
                    self.player.KEY_DOWN = key
                elif self.ismodify_ABILITY:
                    self.ismodify_ABILITY = False
                    self.player.KEY_ABILITY = key
                elif self.ismodify_SPRINT:
                    self.ismodify_SPRINT = False
                    self.player.KEY_SPRINT = key
                elif self.ismodify_INTERACT:
                    self.ismodify_INTERACT = False
                    for passage in self.passages:
                        passage.KEY_INTERACT = key
                    for interactive in self.interactives:
                        interactive.KEY_INTERACT = key
                self.key_ismodify = False
        
        else:
            if pyxel.mouse_x > 5 and pyxel.mouse_x < 5+118 and pyxel.mouse_y > 4+INTERFACE_SIZE_Y and pyxel.mouse_y < 4+11+INTERFACE_SIZE_Y and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                self.key_ismodify = True
                self.ismodify_JUMP = True
            elif pyxel.mouse_x > 5 and pyxel.mouse_x < 5+118 and pyxel.mouse_y > 15+INTERFACE_SIZE_Y and pyxel.mouse_y < 15+11+INTERFACE_SIZE_Y and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                self.key_ismodify = True
                self.ismodify_LEFT = True
            elif pyxel.mouse_x > 5 and pyxel.mouse_x < 5+118 and pyxel.mouse_y > 26+INTERFACE_SIZE_Y and pyxel.mouse_y < 26+11+INTERFACE_SIZE_Y and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                self.key_ismodify = True
                self.ismodify_RIGHT = True
            elif pyxel.mouse_x > 5 and pyxel.mouse_x < 5+118 and pyxel.mouse_y > 37+INTERFACE_SIZE_Y and pyxel.mouse_y < 37+11+INTERFACE_SIZE_Y and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                self.key_ismodify = True
                self.ismodify_UP = True
            elif pyxel.mouse_x > 5 and pyxel.mouse_x < 5+118 and pyxel.mouse_y > 48+INTERFACE_SIZE_Y and pyxel.mouse_y < 48+11+INTERFACE_SIZE_Y and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                self.key_ismodify = True
                self.ismodify_DOWN = True
            elif pyxel.mouse_x > 5 and pyxel.mouse_x < 5+118 and pyxel.mouse_y > 59+INTERFACE_SIZE_Y and pyxel.mouse_y < 59+11+INTERFACE_SIZE_Y and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                self.key_ismodify = True
                self.ismodify_ABILITY = True
            elif pyxel.mouse_x > 5 and pyxel.mouse_x < 5+118 and pyxel.mouse_y > 70+INTERFACE_SIZE_Y and pyxel.mouse_y < 70+11+INTERFACE_SIZE_Y and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                self.key_ismodify = True
                self.ismodify_SPRINT = True
            elif pyxel.mouse_x > 5 and pyxel.mouse_x < 5+118 and pyxel.mouse_y > 81+INTERFACE_SIZE_Y and pyxel.mouse_y < 81+11+INTERFACE_SIZE_Y and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                self.key_ismodify = True
                self.ismodify_INTERACT = True
                
            if pyxel.mouse_x >= 16 and pyxel.mouse_x <= 102 and pyxel.mouse_y >= 97+INTERFACE_SIZE_Y and pyxel.mouse_y <= 108+INTERFACE_SIZE_Y and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                self.player.KEY_UP = pyxel.KEY_Z
                self.player.KEY_DOWN = pyxel.KEY_S
                self.player.KEY_RIGHT = pyxel.KEY_D
                self.player.KEY_LEFT = pyxel.KEY_Q
                self.player.KEY_ABILITY = pyxel.KEY_A
                self.player.KEY_SPRINT = pyxel.KEY_SHIFT
                self.player.KEY_JUMP = pyxel.KEY_SPACE
                for passage in self.passages:
                    passage.KEY_INTERACT = pyxel.KEY_E
                for interactive in self.interactives:
                    interactive.KEY_INTERACT = pyxel.KEY_E
    
            if pyxel.mouse_x >= 16 and pyxel.mouse_x <= 102 and pyxel.mouse_y >= 110+INTERFACE_SIZE_Y and pyxel.mouse_y <= 121+INTERFACE_SIZE_Y and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                self.screen = "Game"

    def settings_draw(self):
        if self.key_ismodify:
            pyxel.text(self.player.interface_x+20, self.player.interface_y+25, "APPUYEZ SUR UNE TOUCHE", COLOR_ORANGE)
        else:
            pyxel.text(self.player.interface_x+40, self.player.interface_y-15, "PARAMETRES :", COLOR_ORANGE)
            pyxel.text(self.player.interface_x+20, self.player.interface_y-6, "(cliquer pour modifier)", COLOR_ORANGE)
            #
            pyxel.rectb(self.player.interface_x+5, self.player.interface_y+4, 118, 11, COLOR_WHITE)
            pyxel.text(self.player.interface_x+8, self.player.interface_y+7, "SAUTER : " + str(self.player.KEY_JUMP), COLOR_WHITE)
            pyxel.rectb(self.player.interface_x+5, self.player.interface_y+15, 118, 11, COLOR_WHITE)
            pyxel.text(self.player.interface_x+8, self.player.interface_y+18, "GAUCHE : " + str(self.player.KEY_LEFT), COLOR_WHITE)
            pyxel.rectb(self.player.interface_x+5, self.player.interface_y+26, 118, 11, COLOR_WHITE)
            pyxel.text(self.player.interface_x+8, self.player.interface_y+29, "DROITE : " + str(self.player.KEY_RIGHT), COLOR_WHITE)
            pyxel.rectb(self.player.interface_x+5, self.player.interface_y+37, 118, 11, COLOR_WHITE)
            pyxel.text(self.player.interface_x+8, self.player.interface_y+40, "HAUT : " + str(self.player.KEY_UP), COLOR_WHITE)
            pyxel.rectb(self.player.interface_x+5, self.player.interface_y+48, 118, 11, COLOR_WHITE)
            pyxel.text(self.player.interface_x+8, self.player.interface_y+51, "BAS : " + str(self.player.KEY_DOWN), COLOR_WHITE)
            pyxel.rectb(self.player.interface_x+5, self.player.interface_y+59, 118, 11, COLOR_WHITE)
            pyxel.text(self.player.interface_x+8, self.player.interface_y+62, "ABILITEE : " + str(self.player.KEY_ABILITY), COLOR_WHITE)
            pyxel.rectb(self.player.interface_x+5, self.player.interface_y+70, 118, 11, COLOR_WHITE)
            pyxel.text(self.player.interface_x+8, self.player.interface_y+73, "SPRINTER : " + str(self.player.KEY_SPRINT), COLOR_WHITE)
            pyxel.rectb(self.player.interface_x+5, self.player.interface_y+81, 118, 11, COLOR_WHITE)
            pyxel.text(self.player.interface_x+8, self.player.interface_y+84, "INTERAGIR : " + str(self.passages[0].KEY_INTERACT), COLOR_WHITE)
            pyxel.rectb(self.player.interface_x+13, self.player.interface_y+110, 102, 11, COLOR_ORANGE)
            pyxel.text(self.player.interface_x+21, self.player.interface_y+113, "SAUVEGARDER ET QUITTER", COLOR_YELLOW)
            pyxel.rectb(self.player.interface_x+13, self.player.interface_y+97, 102, 11, COLOR_ORANGE)
            pyxel.text(self.player.interface_x+38, self.player.interface_y+100, "REINITIALISER", COLOR_YELLOW)

    def end_update(self):
        if self.end_timer <= 0:
            self.screen = "Won"
        else:
            self.end_timer -= 1
        # Changement d'écran
        if pyxel.mouse_x >= self.settings_x and pyxel.mouse_x <= self.settings_x + self.settings_size_x and pyxel.mouse_y >= HEIGHT + self.settings_y and pyxel.mouse_y <= HEIGHT + self.settings_y + self.settings_size_y and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            self.screen = "Settings"
        # Personnage
        self.player.update()
        self.player_ability_uses = 0
        if self.player.ability == "Detector":
            self.player.detector_x = self.neighbor.x
            self.player.detector_y = self.neighbor.y
        elif self.player.ability == "Index":
            if len(self.passages) > 0:
                if not self.passages[0].key_statut:
                    self.player.index_x = self.passages[0].key_x
                    self.player.index_y = self.passages[0].key_y
                else:
                    self.player.index_x = self.passages[0].door_x
                    self.player.index_y = self.passages[0].door_y
            else:
                self.player.ability_uses = 0
        # Voisin
        self.neighbor.update()
        self.neighbor.horizontal_res_x = 243
        self.neighbor.vertical_res_x = 227
        self.neighbor.player_visibility = True
        self.neighbor.default_speed = 0.75
        self.neighbor.pause //= 1.25
        self.neighbor.player_x = self.player.x
        self.neighbor.player_y = self.player.y
        self.neighbor.player_size_x = self.player.size_x
        self.neighbor.player_size_y = self.player.size_y
        if self.neighbor.player_catched:
            self.screen = "Lost"

    def end_draw(self):
        
        
        # Tilemap
        pyxel.blt(0, 0, 1, 0, 0, 256, 256)
        # Interface
        pyxel.text(self.player.interface_x+2, self.player.interface_y-16, "Temps restant :", COLOR_RED)
        pyxel.text(self.player.interface_x+62, self.player.interface_y-16, str(self.end_timer//FPS), COLOR_RED)
        pyxel.rect(self.player.interface_x, self.player.interface_y+HEIGHT-INTERFACE_SIZE_Y, WIDTH, 2, COLOR_GREEN)
        pyxel.rect(self.player.interface_x, self.player.interface_y+HEIGHT-INTERFACE_SIZE_Y+1, WIDTH, INTERFACE_SIZE_Y, COLOR_LIGHTBLUE)
        pyxel.blt(self.player.interface_x+self.settings_x, self.player.interface_y+HEIGHT-INTERFACE_SIZE_Y+self.settings_y, 0, self.settings_res_x, self.settings_res_y, self.settings_size_x, self.settings_size_y, 0)
        # Player
        self.player.draw()
        # Voisin
        self.neighbor.draw()

    def finished_update(self):
        pass

    def finished_draw(self):
            pyxel.camera(0, 0)
            if self.screen == "Lost":
                pyxel.text(48, 4, "PERDU...", random.randint(0, 15))
            elif self.screen == "Won":
                pyxel.text(48, 4, "GAGNE!!!", random.randint(0, 15))
    
    def update(self):
        # Tutoriel
        if self.screen == "Tutorial":
            self.tutorial_update()
        # Sélection
        elif self.screen == "Selection":
            self.selection_update()
        # Jeu
        elif self.screen == "Game":
            self.game_update()
        # Paramètres
        elif self.screen == "Settings":
            self.settings_update()
        # Fin
        elif self.screen == "End":
            self.end_update()
        # Gagné/Perdu
        elif self.screen == "Lost" or self.screen == "Won":
            self.finished_update()
            
    def draw(self):
        # Ecran
        pyxel.cls(COLOR_BLACK)
        # Tutoriel
        if self.screen == "Tutorial":
            self.tutorial_draw()
        # Sélection
        elif self.screen == "Selection":
            self.selection_draw()
        # Jeu
        elif self.screen == "Game":
            self.game_draw()
        # Paramètres  
        elif self.screen == "Settings":
            self.settings_draw()
        # Fin
        elif self.screen == "End":
            self.end_draw()
        # Gagné/Perdu
        elif self.screen == "Lost" or self.screen == "Won":
            self.finished_draw()

#########################################################
# DEMARRAGE
#########################################################
Game()