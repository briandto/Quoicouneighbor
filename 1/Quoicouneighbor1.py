# Importation des fonctions
import pyxel, random

##### SELECTION DU JEU #####
game = "partie 1"
# Dans un futur ou le jeu 2 sera sorti

if game == "partie 1":

    #####
    # Bugs :
    #   + : Voisin qui traverse le lit dans la chambre + n'accélère pas dans certaines salles, Permettre au voisin de s'arrêter et de faire demi-tour aléatoirement
    #   - : Inventaire à une seule voire deux cases
    # Ajouts : 
    #   + : Fenetres, Cachettes, Ajouter une clef et une salle (ou on trouvera le lance-pierre = salle bonus)
    #   - : Menu de sélection de langue, Afficher les touches au démarrage, afficher crédits à la fin, Easter egg sur écran de lancement
    #####

    # Précisions de ce qui peut être considéré comme un bug mais qui ne l'est pas !
    # Le voisin et les clefs sont visibles à travers le carré noir en bas
    # Sur certains meubles il est possible de voir le bras du personnage dépasser (logique comme le jeu est en vue du dessus mais nécessaire à préciser)
    # Dans le programme on retrouve souvent " + 64 ", il est souvent présent car les coordonnées de la tilemap sont exactement les mêmes que celles de l'éditeur avec 64 de plus (en x et y), et donc évite de longs calculs faisant perdre du temps...
    
    # =========================================================
    #  FONCTIONS DE JEU
    # =========================================================

    def reset():
        """
        Réinitialise toutes les variables
        Entrée : 
        Sortie : Toutes les variables du jeu
        """
        
        ##### FEUNETRE #####
        TITLE = "Quoicouneighbor"
        WIDTH = 128
        HEIGHT = 128
        FPS = 30 # JEU FAIT POUR 30 UNIQUEMENT
        ##### JEU #####
        jeu_statut = False
        jeu_perdu = False
        jeu_gagne = False
        jeu_niveau = 0
        jeu_page = 1
        jeu_timer = 0
        gamemod_statut = False
        collisions_statut = True
        endurance_statut = True
        ##### PERSONNAGE #####
        personnage_defaut_x = 156
        personnage_defaut_y = 300
        personnage_x = personnage_defaut_x
        personnage_y = personnage_defaut_y
        personnage_direction = 0
        personnage_vitesse = 0
        personnage_vies_max = 0
        personnage_vies = 0
        personnage_endurance = 100
        endurance_pleine_statut = False
        endurance_inprogress_statut = False
        endurance_faible_statut = False
        personnage_selectionne = 0
        personnage_selectionne1_res_x = 0
        personnage_selectionne2_res_x = 0
        personnage_selectionne1_res_y = 0
        personnage_selectionne2_res_y = 0
        personnage_size_x = 10
        personnage_size_y = 10
        # 1
        personnage11_res_x = 3
        personnage11_res_y = 51
        personnage12_res_x = personnage11_res_x + 16
        personnage12_res_y = personnage11_res_y
        # 2
        personnage21_res_x = 3
        personnage21_res_y = 67
        personnage22_res_x = personnage21_res_x + 16
        personnage22_res_y = personnage21_res_y
        # 3
        personnage31_res_x = 3
        personnage31_res_y = 83
        personnage32_res_x = personnage31_res_x + 16
        personnage32_res_y = personnage31_res_y
        # 4
        personnage41_res_x = 3
        personnage41_res_y = 99
        personnage42_res_x = personnage41_res_x + 16
        personnage42_res_y = personnage41_res_y
        ##### VOISIN #####
        voisin_defaut_x = 7 + 64
        voisin_defaut_y = 55 + 64
        voisin_v = 0
        voisin_trajectoire = 0
        voisin_direction = 2
        voisin_x = voisin_defaut_x
        voisin_y = voisin_defaut_y
        voisin_res1_x = 3
        voisin_res1_y = 115
        voisin_res2_x = 19
        voisin_res2_y = 115
        voisin_size_x = 10
        voisin_size_y = 10
        voisin_touchee = False
        voisin_endormi_temps = 0
        voisin_endormi_max = 0
        voisin_trajectoire_pause = 0
        voisin_trajectoire_pause_max = 0
        voisin_trajectoire_changement_max = 0
        ##### INVENTAIRE #####
        inventaire_objet_selectionne = 0
        inventaire_objet_selectionne_x = 0
        inventaire_objet_selectionne_y = 0
        inventaire_munition_slot_x = 73
        inventaire_munition_slot_y = 118
        marge_interaction = 4
        marge_px = personnage_size_x
        marge_py = personnage_size_y
        ##### ARME #####
        # Arme
        arme_defaut_x = 212 + 64
        arme_defaut_y = 203 + 64
        arme_x = arme_defaut_x
        arme_y = arme_defaut_y
        arme_size_x = 8
        arme_size_y = 8
        arme_bar_color = 0
        arme_statut = False
        arme_tir_avancement = 0
        arme_cooldown = 0
        arme_munition = 1
        arme_direction = personnage_direction
        # Tir
        arme_tir_x = arme_x
        arme_tir_y = arme_y
        arme_tir_size_x = 6
        arme_tir_size_y = 6
        arme_tir_statut = False
        arme_res_x = 40
        arme_res_y = 16
        ##### MUNITIONS #####
        arme_munition_count = 0
        arme_munition_size_x = 5
        arme_munition_size_y = 5
        # 1
        arme_munition1_statut = False
        arme_munition1_defaut_x = 79 + 64
        arme_munition1_defaut_y = 176 + 64
        arme_munition1_x = arme_munition1_defaut_x
        arme_munition1_y = arme_munition1_defaut_y
        arme_munition1_res_x = 0
        arme_munition1_res_y = 16
        # 2
        arme_munition2_statut = False
        arme_munition2_defaut_x = 30 + 64
        arme_munition2_defaut_y = 163 + 64
        arme_munition2_x = arme_munition2_defaut_x
        arme_munition2_y = arme_munition2_defaut_y
        arme_munition2_res_x = 8
        arme_munition2_res_y = 16
        # 3
        arme_munition3_statut = False
        arme_munition3_defaut_x = 195 + 64
        arme_munition3_defaut_y = 130 + 64
        arme_munition3_x = arme_munition3_defaut_x
        arme_munition3_y = arme_munition3_defaut_y
        arme_munition3_res_x = 0
        arme_munition3_res_y = 24
        # 4
        arme_munition4_statut = False
        arme_munition4_defaut_x = 129 + 64
        arme_munition4_defaut_y = 59 + 64
        arme_munition4_x = arme_munition4_defaut_x
        arme_munition4_y = arme_munition4_defaut_y
        arme_munition4_res_x = 8
        arme_munition4_res_y = 24
        ##### CLEFS #####
        # 0 -> Pince = Dans le jardin
        clef0_defaut_x = 29 + 64
        clef0_defaut_y = 144 + 64
        clef0_x = clef0_defaut_x
        clef0_y = clef0_defaut_y
        clef0_statut = False
        clef0_size_x = 5
        clef0_size_y = 7
        clef0_res_x = 72
        clef0_res_y = 64
        clef0_utilise = False
        # 1 -> Jaune = Dans le garage
        clef1_defaut_x = 79 + 64
        clef1_defaut_y = 166 + 64
        clef1_x = clef1_defaut_x
        clef1_y = clef1_defaut_y
        clef1_statut = False
        clef1_size_x = 4
        clef1_size_y = 7
        clef1_res_x = 48
        clef1_res_y = 48
        clef1_utilise = False
        # 2 -> Rose = Dans la salle de bain
        clef2_defaut_x = 87 + 64
        clef2_defaut_y = 6 + 64
        clef2_x = clef2_defaut_x
        clef2_y = clef2_defaut_y
        clef2_statut = False
        clef2_size_x = 4
        clef2_size_y = 7
        clef2_res_x = 48
        clef2_res_y = 64
        clef2_utilise = False
        # 3 -> Vert = Dans la salle de caméra
        clef3_defaut_x = 197 + 64
        clef3_defaut_y = 86 + 64
        clef3_x = clef3_defaut_x
        clef3_y = clef3_defaut_y
        clef3_statut = False
        clef3_size_x = 4
        clef3_size_y = 7
        clef3_res_x = 48
        clef3_res_y = 80
        clef3_utilise = False
        # 4 -> Bleue = Dans la chambre
        clef4_defaut_x = 193 + 64
        clef4_defaut_y = 172 + 64
        clef4_x = clef4_defaut_x
        clef4_y = clef4_defaut_y
        clef4_statut = False
        clef4_size_x = 4
        clef4_size_y = 7
        clef4_res_x = 48
        clef4_res_y = 96
        clef4_utilise = False
        # 5 -> Ciseaux = Dans le salon
        clef5_defaut_x = 48 + 64
        clef5_defaut_y = 200 + 64
        clef5_x = clef5_defaut_x
        clef5_y = clef5_defaut_y
        clef5_statut = False
        clef5_size_x = 7
        clef5_size_y = 7
        clef5_res_x = 72
        clef5_res_y = 80
        clef5_utilise = False
        # 6 -> Marteau = Dans la cuisine
        clef6_defaut_x = 115 + 64
        clef6_defaut_y = 59 + 64
        clef6_x = clef6_defaut_x
        clef6_y = clef6_defaut_y
        clef6_statut = False
        clef6_size_x = 4
        clef6_size_y = 7
        clef6_res_x = 72
        clef6_res_y = 96
        clef6_utilise = False
        ##### PORTES #####
        # 0 -> Planches à clous = Garage
        porte0_defaut_x = 152 + 64
        porte0_defaut_y = 212 + 64
        porte0_x = porte0_defaut_x
        porte0_y = porte0_defaut_y
        porte0_statut = False
        porte0_size_x = 16
        porte0_size_y = 6
        porte0_res_x = 56
        porte0_res_y = 69
        # 1 -> Jaune = Salle de bain
        porte1_defaut_x = 8 + 64
        porte1_defaut_y = 42 + 64
        porte1_x = porte1_defaut_x
        porte1_y = porte1_defaut_y
        porte1_statut = False
        porte1_size_x = 16
        porte1_size_y = 8
        porte1_res_x = 32
        porte1_res_y = 52
        # 2 -> Rose = Salle de caméra
        porte2_defaut_x = 180 + 64
        porte2_defaut_y = 140 + 64
        porte2_x = porte2_defaut_x
        porte2_y = porte2_defaut_y
        porte2_statut = False
        porte2_size_x = 8
        porte2_size_y = 16
        porte2_res_x = 36
        porte2_res_y = 64
        # 3 -> Verte = Salon
        porte3_defaut_x = 40 + 64
        porte3_defaut_y = 154 + 64
        porte3_x = porte3_defaut_x
        porte3_y = porte3_defaut_y
        porte3_statut = False
        porte3_size_x = 16
        porte3_size_y = 8
        porte3_res_x = 32
        porte3_res_y = 84
        # 4 -> Bleue = Cuisine
        porte4_defaut_x = 92 + 64
        porte4_defaut_y = 134 + 64
        porte4_x = porte4_defaut_x
        porte4_y = porte4_defaut_y
        porte4_statut = False
        porte4_size_x = 16
        porte4_size_y = 8
        porte4_res_x = 32
        porte4_res_y = 100
        # 5 -> Bande = Chambre
        porte5_defaut_x = 208 + 64
        porte5_defaut_y = 155 + 64
        porte5_x = porte5_defaut_x
        porte5_y = porte5_defaut_y
        porte5_statut = False
        porte5_size_x = 16
        porte5_size_y = 6
        porte5_res_x = 56
        porte5_res_y = 85
        # 6 -> Mur = Escalier sous-sol (fin)
        porte6_defaut_x = 16 + 64
        porte6_defaut_y = 72 + 64
        porte6_x = porte6_defaut_x
        porte6_y = porte6_defaut_y
        porte6_statut = False
        porte6_size_x = 16
        porte6_size_y = 4
        porte6_res_x = 56
        porte6_res_y = 102

        return TITLE, WIDTH, HEIGHT, FPS, jeu_statut, jeu_perdu, jeu_gagne, jeu_niveau, jeu_page, jeu_timer, gamemod_statut, collisions_statut, endurance_statut, personnage_defaut_x, personnage_defaut_y, personnage_x, personnage_y, personnage_direction, personnage_vitesse, personnage_vies_max, personnage_vies, personnage_endurance, endurance_pleine_statut, endurance_inprogress_statut, endurance_faible_statut, personnage_selectionne, personnage_selectionne1_res_x, personnage_selectionne2_res_x, personnage_selectionne1_res_y, personnage_selectionne2_res_y, personnage_size_x, personnage_size_y, personnage11_res_x, personnage11_res_y, personnage12_res_x, personnage12_res_y, personnage21_res_x, personnage21_res_y, personnage22_res_x, personnage22_res_y, personnage31_res_x, personnage31_res_y, personnage32_res_x, personnage32_res_y, personnage41_res_x, personnage41_res_y, personnage42_res_x, personnage42_res_y, voisin_defaut_x, voisin_defaut_y, voisin_v, voisin_trajectoire, voisin_direction, voisin_x, voisin_y, voisin_res1_x, voisin_res1_y, voisin_res2_x, voisin_res2_y, voisin_size_x, voisin_size_y, voisin_touchee, voisin_endormi_temps, voisin_endormi_max, voisin_trajectoire_pause, voisin_trajectoire_pause_max, voisin_trajectoire_changement_max, inventaire_objet_selectionne, inventaire_objet_selectionne_x, inventaire_objet_selectionne_y, inventaire_munition_slot_x, inventaire_munition_slot_y, marge_interaction, marge_px, marge_py, arme_defaut_x, arme_defaut_y, arme_x, arme_y, arme_size_x, arme_size_y, arme_bar_color, arme_statut, arme_tir_avancement, arme_cooldown, arme_munition, arme_direction, arme_tir_x, arme_tir_y, arme_tir_size_x, arme_tir_size_y, arme_tir_statut, arme_res_x, arme_res_y, arme_munition_count, arme_munition_size_x, arme_munition_size_y, arme_munition1_statut, arme_munition1_defaut_x, arme_munition1_defaut_y, arme_munition1_x, arme_munition1_y, arme_munition1_res_x, arme_munition1_res_y, arme_munition2_statut, arme_munition2_defaut_x, arme_munition2_defaut_y, arme_munition2_x, arme_munition2_y, arme_munition2_res_x, arme_munition2_res_y, arme_munition3_statut, arme_munition3_defaut_x, arme_munition3_defaut_y, arme_munition3_x, arme_munition3_y, arme_munition3_res_x, arme_munition3_res_y, arme_munition4_statut, arme_munition4_defaut_x, arme_munition4_defaut_y, arme_munition4_x, arme_munition4_y, arme_munition4_res_x, arme_munition4_res_y, clef0_defaut_x, clef0_defaut_y, clef0_x, clef0_y, clef0_statut, clef0_size_x, clef0_size_y, clef0_res_x, clef0_res_y, clef0_utilise, clef1_defaut_x, clef1_defaut_y, clef1_x, clef1_y, clef1_statut, clef1_size_x, clef1_size_y, clef1_res_x, clef1_res_y, clef1_utilise, clef2_defaut_x, clef2_defaut_y, clef2_x, clef2_y, clef2_statut, clef2_size_x, clef2_size_y, clef2_res_x, clef2_res_y, clef2_utilise, clef3_defaut_x, clef3_defaut_y, clef3_x, clef3_y, clef3_statut, clef3_size_x, clef3_size_y, clef3_res_x, clef3_res_y, clef3_utilise, clef4_defaut_x, clef4_defaut_y, clef4_x, clef4_y, clef4_statut, clef4_size_x, clef4_size_y, clef4_res_x, clef4_res_y, clef4_utilise, clef5_defaut_x, clef5_defaut_y, clef5_x, clef5_y, clef5_defaut_y, clef5_statut, clef5_size_x, clef5_size_y, clef5_res_x, clef5_res_y, clef5_utilise, clef6_defaut_x, clef6_defaut_y, clef6_x, clef6_y, clef6_statut, clef6_size_x, clef6_size_y, clef6_res_x, clef6_res_y, clef6_utilise, porte0_defaut_x, porte0_defaut_y, porte0_x, porte0_y, porte0_statut, porte0_size_x, porte0_size_y, porte0_res_x, porte0_res_y, porte1_defaut_x, porte1_defaut_y, porte1_x, porte1_y, porte1_statut, porte1_size_x, porte1_size_y, porte1_res_x, porte1_res_y, porte2_defaut_x, porte2_defaut_y, porte2_x, porte2_y, porte2_statut, porte2_size_x, porte2_size_y, porte2_res_x, porte2_res_y, porte3_defaut_x, porte3_defaut_y, porte3_x, porte3_y, porte3_statut, porte3_size_x, porte3_size_y, porte3_res_x, porte3_res_y, porte4_defaut_x, porte4_defaut_y, porte4_x, porte4_y, porte4_statut, porte4_size_x, porte4_size_y, porte4_res_x, porte4_res_y, porte5_defaut_x, porte5_defaut_y, porte5_x, porte5_y, porte5_statut, porte5_size_x, porte5_size_y, porte5_res_x, porte5_res_y, porte6_defaut_x, porte6_defaut_y, porte6_x, porte6_y, porte6_statut, porte6_size_x, porte6_size_y, porte6_res_x, porte6_res_y

    def fonction_selection_personnage():
        """
        Sélectionner son personnage (4 modèles disponibles)
        Entrée :
        Sortie : Le personnage sélectionne
        """
        selectionne = 0

        if pyxel.btnp(pyxel.KEY_A):
            selectionne = 1
        elif pyxel.btnp(pyxel.KEY_B):
            selectionne = 2
        elif pyxel.btnp(pyxel.KEY_C):
            selectionne = 3
        elif pyxel.btnp(pyxel.KEY_D):
            selectionne = 4

        return selectionne

    def fonction_godmode(gamemod, gagne, perdu, collisions, endurance, arme, munitions, p0, p1, p2, p3, p4, p5, p6):
        """
        Le joueur peut faire ce qu'il veut grâce à des combinaisons de touches
        Entrée : Statut du gamemod, Statut de toutes les portes, Statut et Nombre de munitions de l'arme, Statut des collisions, Statut du jeu gagne ou perdu
        Sortie : Statut du gamemod, Statut de toutes les portes, Statut et Nombre de munitions de l'arme, Statut des collisions, Statut du jeu gagne ou perdu
        """

        if gamemod == True:

            # Statut du jeu
            if pyxel.btnr(pyxel.KEY_L):
                perdu = True
            if pyxel.btnr(pyxel.KEY_W):
                gagne = True

            # Collisions
            if pyxel.btnr(pyxel.KEY_C) and collisions == True:
                collisions = False
            elif pyxel.btnr(pyxel.KEY_C) and collisions == False:
                collisions = True

            # Endurance
            elif pyxel.btnr(pyxel.KEY_E) and endurance == True:
                endurance = False
            elif pyxel.btnr(pyxel.KEY_E) and endurance == False:
                endurance = True

            # Arme
            if pyxel.btnr(pyxel.KEY_A) and arme == False:
                arme = True
                munitions = 9
            
            # Portes
            if pyxel.btnr(pyxel.KEY_P):
                p0 = True
                p1 = True
                p2 = True
                p3 = True
                p4 = True
                p5 = True
                p6 = True

            # Désactiver gamemod
            if pyxel.btnr(pyxel.KEY_G):

                gamemod = False
                collisions = True
                endurance = True
                p0 = False
                p1 = False
                p2 = False
                p3 = False
                p4 = False
                p5 = False
                p6 = False
                arme = False
                munitions = 0

        else:

            if pyxel.btnr(pyxel.KEY_G):
                gamemod = True

        return gamemod, gagne, perdu, collisions, endurance, arme, munitions, p0, p1, p2, p3, p4, p5, p6
        
    # =========================================================
    #  FONCTIONS DE DEPLACEMENT
    # =========================================================

    def fonction_collisions(type, pre_x, pre_y, x, y, p0, p1, p2, p3, p4, p5, p6):
        """
        Détermine si le joueur/munition peut avancer
        Entrée : Type, Coordonnées du type avant et après avoir bougé, le Statut des portes
        Sortie : Coordonnées du type, statut de la victoire
        """

        ##### COLLISIONS #####
        # Initialisation des variables par défaut
        valid = True
        if type == "personnage":
            type_size_x = personnage_size_x
            type_size_y = personnage_size_y
        elif type == "tir":
            type_size_x = arme_munition_size_x
            type_size_y = arme_munition_size_y
        # Détermine les collisions
        # Contour map
        # droite
        if x > 255 + 64 - type_size_x:
            valid = False
        # gauche
        elif x < 10:
            valid = False
        # bas
        elif y > 255 + 64 - type_size_y:
            valid = False
        # haut
        elif y < 10:
            valid = False

        # CONTOURS DE LA MAISON
        # haut
        elif x >= 0 + 64 - type_size_x and y >= 0 + 64 - type_size_y and x <= 255 + 64 and y <= 3 + 64:
            valid = False
        # droite
        elif x >= 252 + 64 - type_size_x and y >= 0 + 64 - type_size_y and x <= 255 + 64 and y <= 215 + 64:
            valid = False
        # bas 1
        elif x >= 0 + 64 - type_size_x and y >= 212 + 64 - type_size_y and x <= 151 + 64 and y <= 215 + 64:
            valid = False
        # bas 2
        elif x >= 168 + 64 - type_size_x and y >= 212 + 64 - type_size_y and x <= 255 + 64 and y <= 215 + 64:
            valid = False
        # gauche 1
        elif x >= 0 + 64 - type_size_x and y >= 0 + 64 - type_size_y and x <= 3 + 64 and y <= 139 + 64:
            valid = False
        # gauche 2
        elif x >= 0 + 64 - type_size_x and y >= 156 + 64 - type_size_y and x <= 3 + 64 and y <= 215 + 64:
            valid = False
        # Obstacles (jardin)
        # Etagère
        elif x >= 27 + 64 - type_size_x and y >= 142 + 64 - type_size_y and x <= 35 + 64 and y <= 153 + 64:
            if type == "personnage": # Si c'est le personnage qui se trouve ici:
                valid = False

        # SALLE DE BAIN
        # Murs
        # haut
        elif x >= 0 + 64 - type_size_x and y >= 0 + 64 - type_size_y and x <= 95 + 64 and y <= 3 + 64:
            valid = False
        # droite
        elif x >= 92 + 64 - type_size_x and y >= 0 + 64 - type_size_y and x <= 95 + 64 and y <= 39 + 64:
            valid = False
        # bas 1
        elif x >= 0 + 64 - type_size_x and y >= 44 + 64 - type_size_y and x <= 7 + 64 and y <= 47 + 64:
            valid = False
        # porte 1
        elif x >= 8 + 64 - type_size_x and y >= 44 + 64 - type_size_y and x <= 23 + 64 and y <= 47 + 64:
            if p1 == False:
                valid = False
        # bas 2
        elif x >= 24 + 64 - type_size_x and y >= 44 + 64 - type_size_y and x <= 59 + 64 and y <= 47 + 64:
            valid = False
        # bas 3
        elif x >= 52 + 64 - type_size_x and y >= 36 + 64 - type_size_y and x <= 95 + 64 and y <= 39 + 64:
            valid = False
        # milieu
        elif x >= 52 + 64 - type_size_x and y >= 17 + 64 - type_size_y and x <= 55 + 64 and y <= 47 + 64:
            valid = False
        # gauche = déjà initialisé
        # Obstacles
        # toilette
        elif x >= 6 + 64 - type_size_x and y >= 4 + 64 - type_size_y and x <= 16 + 64 and y <= 17 + 64:
            if type == "personnage": # Si c'est le personnage qui se trouve ici:
                valid = False
        # lavabo
        elif x >= 21 + 64 - type_size_x and y >= 4 + 64 - type_size_y and x <= 29 + 64 and y <= 11 + 64:
            if type == "personnage": # Si c'est le personnage qui se trouve ici:
                valid = False
        # meuble 1 (bas)
        elif x >= 28 + 64 - type_size_x and y >= 38 + 64 - type_size_y and x <= 50 + 64 and y <= 42 + 64:
            if type == "personnage": # Si c'est le personnage qui se trouve ici:
                valid = False
        # meuble 1 (haut)
        elif x >= 46 + 64 - type_size_x and y >= 27 + 64 - type_size_y and x <= 50 + 64 and y <= 42 + 64:
            if type == "personnage": # Si c'est le personnage qui se trouve ici:
                valid = False
        # baignoire
        elif x >= 56 + 64 - type_size_x and y >= 21 + 64 - type_size_y and x <= 91 + 64 and y <= 35 + 64:
            if type == "personnage": # Si c'est le personnage qui se trouve ici:
                valid = False
        # meuble 2
        elif x >= 85 + 64 - type_size_x and y >= 4 + 64 - type_size_y and x <= 91 + 64 and y <= 18 + 64:
            if type == "personnage": # Si c'est le personnage qui se trouve ici:
                valid = False

        # SALLE DE LA CAVE
        # Murs
        # haut 1
        elif x >= 0 + 64 - type_size_x and y >= 72 + 64 - type_size_y and x <= 15 + 64 and y <= 75 + 64:
            valid = False
        # porte 6
        elif x >= 16 + 64 - type_size_x and y >= 72 + 64 - type_size_y and x <= 31 + 64 and y <= 75 + 64:
            if p6 == False:
                valid = False
        # haut 2
        elif x >= 32 + 64 - type_size_x and y >= 72 + 64 - type_size_y and x <= 39 + 64 and y <= 75 + 64:
            valid = False
        # droite
        elif x >= 36 + 64 - type_size_x and y >= 72 + 64 - type_size_y and x <= 39 + 64 and y <= 159 + 64:
            valid = False
        # bas
        elif x >= 0 + 64 - type_size_x and y >= 136 + 64 - type_size_y and x <= 39 + 64 and y <= 139 + 64:
            valid = False
        # gauche
        elif x >= 32 + 64 - type_size_x and y >= 72 + 64 - type_size_y and x <= 39 + 64 and y <= 75 + 64:
            valid = False
        # droite = déjà initialisé
        # Obstacles
        # Aucun

        # SALON
        # Murs
        # haut 1
        elif x >= 0 + 64 - type_size_x and y >= 156 + 64 - type_size_y and x <= 39 + 64 and y <= 159 + 64:
            valid = False
        # porte 3
        elif x >= 40 + 64 - type_size_x and y >= 156 + 64 - type_size_y and x <= 55 + 64 and y <= 159 + 64:
            if p3 == False:
                valid = False
        # haut 2
        elif x >= 56 + 64 - type_size_x and y >= 156 + 64 - type_size_y and x <= 75 + 64 and y <= 159 + 64:
            valid = False
        # bas
        elif x >= 0 + 64 - type_size_x and y >= 212 + 64 - type_size_y and x <= 59 + 64 and y <= 215 + 64:
            valid = False
        # droite
        elif x >= 56 + 64 - type_size_x and y >= 156 + 64 - type_size_y and x <= 75 + 64 and y <= 215 + 64:
            valid = False
        # gauche = déjà initialisé
        # Obstacles
        # meuble
        elif x >= 5 + 64 - type_size_x and y >= 161 + 64 - type_size_y and x <= 36 + 64 and y <= 168 + 64:
            if type == "personnage": # Si c'est le personnage qui se trouve ici:
                valid = False
        # fauteuil
        elif x >= 8 + 64 - type_size_x and y >= 174 + 64 - type_size_y and x <= 35 + 64 and y <= 198 + 64:
            if type == "personnage": # Si c'est le personnage qui se trouve ici:
                valid = False
        # meuble tv
        elif x >= 6 + 64 - type_size_x and y >= 203 + 64 - type_size_y and x <= 45 + 64 and y <= 210 + 64:
            if type == "personnage": # Si c'est le personnage qui se trouve ici:
                valid = False

        # GARAGE
        # Murs
        # gauche
        elif x >= 72 + 64 - type_size_x and y >= 156 + 64 - type_size_y and x <= 75 + 64 and y <= 215 + 64:
            valid = False
        # haut 1
        elif x >= 72 + 64 - type_size_x and y >= 156 + 64 - type_size_y and x <= 91 + 64 and y <= 159 + 64:
            valid = False
        # écart de non-porte
        # haut 2
        elif x >= 108 + 64 - type_size_x and y >= 156 + 64 - type_size_y and x <= 191 + 64 and y <= 159 + 64:
            valid = False
        # droite
        elif x >= 188 + 64 - type_size_x and y >= 156 + 64 - type_size_y and x <= 191 + 64 and y <= 215 + 64:
            valid = False
        # bas 1
        elif x >= 59 + 64 - type_size_x and y >= 212 + 64 - type_size_y and x <= 151 + 64 and y <= 215 + 64:
            valid = False
        # porte 0
        elif x >= 152 + 64 - type_size_x and y >= 212 + 64 - type_size_y and x <= 167 + 64 and y <= 215 + 64:
            if p0 == False:
                valid = False
        # bas 2
        elif x >= 168 + 64 - type_size_x and y >= 212 + 64 - type_size_y and x <= 191 + 64 and y <= 215 + 64:
            valid = False
        # Obstacles
        # boite à outils
        elif x >= 122 + 64 - type_size_x and y >= 208 + 64 - type_size_y and x <= 133 + 64 and y <= 211 + 64:
            if type == "personnage": # Si c'est le personnage qui se trouve ici:
                valid = False
        # voiture
        elif x >= 127 + 64 - type_size_x and y >= 167 + 64 - type_size_y and x <= 179 + 64 and y <= 188 + 64:
            valid = False
        # étagère
        elif x >= 76 + 64 - type_size_x and y >= 162 + 64 - type_size_y and x <= 84 + 64 and y <= 181 + 64:
            if type == "personnage": # Si c'est le personnage qui se trouve ici:
                valid = False

        # Chambre
        # haut 1
        elif x >= 188 + 64 - type_size_x and y >= 156 + 64 - type_size_y and x <= 207 + 64 and y <= 159 + 64:
            valid = False
        # porte 5
        elif x >= 208 + 64 - type_size_x and y >= 156 + 64 - type_size_y and x <= 223 + 64 and y <= 159 + 64:
            if p5 == False:
                valid = False
        # haut 2
        elif x >= 224 + 64 - type_size_x and y >= 156 + 64 - type_size_y and x <= 255 + 64 and y <= 159 + 64:
            valid = False
        # droite = déjà initialisé
        # bas = déjà initialisé
        # gauche = déjà initialisé
        # Obstacles
        # meuble 1
        elif x >= 192 + 64 - type_size_x and y >= 171 + 64 - type_size_y and x <= 197 + 64 and y <= 181 + 64:
            if type == "personnage": # Si c'est le personnage qui se trouve ici:
                valid = False
        # meuble 2
        elif x >= 201 + 64 - type_size_x and y >= 201 + 64 - type_size_y and x <= 230 + 64 and y <= 211 + 64:
            if type == "personnage": # Si c'est le personnage qui se trouve ici:
                valid = False
        # lit
        elif x >= 233 + 64 - type_size_x and y >= 162 + 64 - type_size_y and x <= 249 + 64 and y <= 189 + 64:
            if type == "personnage": # Si c'est le personnage qui se trouve ici:
                valid = False

        # Salle de caméra
        # Murs
        # haut
        elif x >= 188 + 64 - type_size_x and y >= 40 + 64 - type_size_y and x <= 255 + 64 and y <= 43 + 64:
            valid = False
        # gauche
        elif x >= 188 + 64 - type_size_x and y >= 0 + 64 - type_size_y and x <= 191 + 64 and y <= 139 + 64:
            valid = False
        # bas 1
        elif x >= 188 + 64 - type_size_x and y >= 136 + 64 - type_size_y and x <= 207 + 64 and y <= 139 + 64:
            valid = False
        # écart de non-porte
        # bas 2
        elif x >= 224 + 64 - type_size_x and y >= 136 + 64 - type_size_y and x <= 255 + 64 and y <= 139 + 64:
            valid = False
        # droite = déjà initialisé
        # Obstacles
        # meuble 1 (nosignal) gauche
        elif x >= 193 + 64 - type_size_x and y >= 45 + 64 - type_size_y and x <= 204 + 64 and y <= 94 + 64:
            if type == "personnage": # Si c'est le personnage qui se trouve ici:
                valid = False
        # meuble 1 (nosignal) droite
        elif x >= 239 + 64 - type_size_x and y >= 45 + 64 - type_size_y and x <= 250 + 64 and y <= 94 + 64:
            if type == "personnage": # Si c'est le personnage qui se trouve ici:
                valid = False
        # canapé meuble nosignal
        elif x >= 210 + 64 - type_size_x and y >= 68 + 64 - type_size_y and x <= 233 + 64 and y <= 91 + 64:
            if type == "personnage": # Si c'est le personnage qui se trouve ici:
                valid = False
        # meuble 2 gauche
        elif x >= 228 + 64 - type_size_x and y >= 129 + 64 - type_size_y and x <= 252 + 64 and y <= 135 + 64:
            if type == "personnage": # Si c'est le personnage qui se trouve ici:
                valid = False
        # meuble 2 droite
        elif x >= 245 + 64 - type_size_x and y >= 100 + 64 - type_size_y and x <= 252 + 64 and y <= 135 + 64:
            if type == "personnage": # Si c'est le personnage qui se trouve ici:
                valid = False
        # fauteuil
        elif x >= 234 + 64 - type_size_x and y >= 103 + 64 - type_size_y and x <= 241 + 64 and y <= 110 + 64:
            if type == "personnage": # Si c'est le personnage qui se trouve ici:
                valid = False
        # meuble 3
        elif x >= 192 + 64 - type_size_x and y >= 129 + 64 - type_size_y and x <= 203 + 64 and y <= 135 + 64:
            if type == "personnage": # Si c'est le personnage qui se trouve ici:
                valid = False

        # CUISINE
        # Murs
        # haut
        elif x >= 72 + 64 - type_size_x and y >= 52 + 64 - type_size_y and x <= 143 + 64 and y <= 55 + 64:
            valid = False
        # gauche
        elif x >= 72 + 64 - type_size_x and y >= 52 + 64 - type_size_y and x <= 75 + 64 and y <= 139 + 64:
            valid = False
        # droite
        elif x >= 140 + 64 - type_size_x and y >= 52 + 64 - type_size_y and x <= 143 + 64 and y <= 139 + 64:
            valid = False
        # bas 1
        elif x >= 56 + 64 - type_size_x and y >= 136 + 64 - type_size_y and x <= 91 + 64 and y <= 139 + 64:
            valid = False
        # porte 4
        elif x >= 92 + 64 - type_size_x and y >= 136 + 64 - type_size_y and x <= 107 + 64 and y <= 139 + 64:
            if p4 == False:
                valid = False
        # bas 2
        elif x >= 108 + 64 - type_size_x and y >= 136 + 64 - type_size_y and x <= 191 + 64 and y <= 139 + 64:
            valid = False
        # droite = déjà initialisé
        # Obstacles
        # meubles haut
        elif x >= 76 + 64 - type_size_x and y >= 56 + 64 - type_size_y and x <= 139 + 64 and y <= 67 + 64:
            if type == "personnage": # Si c'est le personnage qui se trouve ici:
                valid = False
        # table
        elif x >= 76 + 64 - type_size_x and y >= 89 + 64 - type_size_y and x <= 118 + 64 and y <= 110 + 64:
            if type == "personnage": # Si c'est le personnage qui se trouve ici:
                valid = False
        # chaise haut gauche
        elif x >= 80 + 64 - type_size_x and y >= 80 + 64 - type_size_y and x <= 86 + 64 and y <= 86 + 64:
            if type == "personnage": # Si c'est le personnage qui se trouve ici:
                valid = False
        # chaise haut droite
        elif x >= 95 + 64 - type_size_x and y >= 80 + 64 - type_size_y and x <= 101 + 64 and y <= 86 + 64:
            if type == "personnage": # Si c'est le personnage qui se trouve ici:
                valid = False
        # chaise bas gauche
        elif x >= 79 + 64 - type_size_x and y >= 113 + 64 - type_size_y and x <= 85 + 64 and y <= 119 + 64:
            if type == "personnage": # Si c'est le personnage qui se trouve ici:
                valid = False
        # chaise bas droite
        elif x >= 95 + 64 - type_size_x and y >= 113 + 64 - type_size_y and x <= 101 + 64 and y <= 119 + 64:
            if type == "personnage": # Si c'est le personnage qui se trouve ici:
                valid = False
        # poubelle
        elif x >= 132 + 64 - type_size_x and y >= 128 + 64 - type_size_y and x <= 136 + 64 and y <= 133 + 64:
            if type == "personnage": # Si c'est le personnage qui se trouve ici:
                valid = False

        # COULOIRS
        # Murs
        # salle de la cave / cuisine
        elif x >= 56 + 64 - type_size_x and y >= 44 + 64 - type_size_y and x <= 59 + 64 and y <= 139 + 64:
            valid = False
        # salle de la cave / cuisine
        elif x >= 180 + 64 - type_size_x and y >= 140 + 64 - type_size_y and x <= 184 + 64 and y <= 155 + 64:
            if p2 == False:
                valid = False
        # Obstacles
        # Aucun

        # Si le personnage touche la porte de fin du jeu
        if x >= 6 + 64 - type_size_x and y >= 100 + 64 - type_size_y and x <= 33 + 64 and y <= 133 + 64:
            if type == "personnage": # Si c'est le personnage qui se trouve ici:
                gagne = True
            else:
                gagne = False
        else:
            gagne = False

        if valid == False:
            return pre_x, pre_y, gagne
        else:
            return x, y, gagne

    def fonction_personnage_endurance(pre_x, pre_y, x, y, endurance, endurance_inprogress, endurance_faible, endurance_pleine):
        """
        Augmenter ou diminue l'endurance du personnage en fonction des actions du joueur
        Entrée : Les coordonnées et les pré-coordonnées et l'endurance restante du personnage, Le statut de l'endurance au max, de l'endurance en régénération et de l'endurance faible
        Sortie : L'endurance restante du personnage, Le statut de l'endurance au max, de l'endurance en régénération et de l'endurance faible
        """

        # Met à jour l'endurance ainsi que si la barre d'endurance actionnée et d'endurance max
        if pyxel.btn(pyxel.KEY_SHIFT) and x != pre_x or pyxel.btn(pyxel.KEY_SHIFT) and y != pre_y: # Si il s'est déplacé en appuyant sur MAJ:
            endurance_inprogress = True
            if endurance < 0: # Si l'endurance est vide:
                endurance = - 5
                endurance_inprogress = False
            if endurance > 0: # Si l'endurance n'est pas vide:
                endurance = endurance - (0.75 + 0.20) # L'endurance diminue
                endurance_inprogress = True
        else:
            endurance_inprogress = False

        if endurance >= 100: # Si l'endurance est pleine
            endurance = 100
            endurance_pleine = True
        else:
            endurance_pleine = False
            endurance = endurance + 0.20 # L'endurance augmente

        if endurance <= 20: # Si l'endurance est faible
            endurance_faible = True
        else:
            endurance_faible = False

        # Renvoie les nouvelles valeurs des variables
        return endurance, endurance_pleine, endurance_inprogress, endurance_faible

    def fonction_personnage_deplacement(x, y, v, direction, p0, p1, p2, p3, p4, p5, p6, collisions, endurance, personnage_endurance, endurance_pleine_statut, endurance_inprogress_statut, endurance_faible_statut):
        """
        Déplace le joueur en fonctions des touches entrées par le joueur :
        - Maj = Accélérer (Endurance limitée)
        - Z / ↑ = Avancer
        - Q / ← = Aller à gauche
        - S / ↓ = Reculer
        - D / → = Aller à droite
        Entrée : Les coordonnées, la direction et la vitesse du personnage, Le statut des portes, Le statut des collisions et Le statut de l'endurance
        Sortie : Les coordonnées, l'endurance et la direction du personnage, Statut de la barre d'endurance max/faible/enutilisation
        """


        ##### VITESSE #####
        # Initialise les valeurs par défaut
        v = 0.5
        if pyxel.btn(pyxel.KEY_LSHIFT) and personnage_endurance > 0: # Si la touche LSHIFT est pressée et que l'endurance est supérieure à 0:
            v = v * 2 # Accélère la vitesse du personnage par 2

        ##### DEPLACEMENT #####
        # Initialise les valeurs par défaut
        pre_x = x
        pre_y = y
        # Vérifie les actions du joueur
        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_D): # Si → ou d est préssé :

            direction = 2 # Change sa direction
            x = x + v  # v pixel vers la droite

        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_Q): # Si ← ou q est préssé :

            direction = 4 # Change sa direction
            x = x - v  # v pixel vers la droite

        if pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.KEY_S): # Si ↓ ou s est préssé :

            direction = 3 # Change sa direction
            y = y + v  # v pixel vers la droite

        if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.KEY_Z): # Si ↑ ou z est préssé :

            direction = 1 # Change sa direction
            y = y - v  # v pixel vers la droite

        ##### COLLISIONS #####
        if collisions == True:
            x, y, gagne = fonction_collisions("personnage", pre_x, pre_y, x, y, p0, p1, p2, p3, p4, p5, p6)
        else:
            gagne = False
        
        ##### ENDURANCE #####
        if endurance == True:
            personnage_endurance, endurance_pleine_statut, endurance_inprogress_statut, endurance_faible_statut = fonction_personnage_endurance(pre_x, pre_y, x, y, personnage_endurance, endurance_inprogress_statut, endurance_faible_statut, endurance_pleine_statut)
        else:
            personnage_endurance = 100

        # Renvoie les nouvelles valeurs des variables
        return x, y, personnage_endurance, direction, endurance_pleine_statut, endurance_inprogress_statut, endurance_faible_statut, gagne

    def fonction_voisin(x, y, v, trajectoire, trajectoire_changement_max, pause_max, pause, direction, touchee, endormi, endormi_max, personnage_x, personnage_y, personnage_vies, tir_x, tir_y, tir_avancement):
        """
        Déplace le voisin vers le personnage pour l'attraper
        Entrée : Coordonnées, Trajectoire, Vitesse et Statut de touche/endormi, Le temps de pause maximum, Le taux de changement de trajectoire, la direction, Le temps de pause de l'ia, Coordonnées du personnage et ses vies
        Sortie : Coordonnées, Trajectoire, et Statut de touche/endormi de l'ia, Coordonnées du personnage et ses vies
        """

        # Endort le voisin si elle est touchée et la réveille si elle dort le temps prédéfini en fonction du niveau
        if touchee == True:
            endormi = endormi + 1
            v = 0
            if endormi >= endormi_max:
                touchee = False
                endormi = 0
        # Si le voisin est à un endroit ou elle doit s'arrêter et qu'elle a fini d'attendre on réinitialise le timer (prédéfini en fonction du niveau)
        if pause <= 0:
            pause = pause_max
        # Le voisin a une chance sur ... (en fonction du niveau) de bifurquer
        if random.randint(1,trajectoire_changement_max) <= 25:
            trajectoire_changement = True
        else:
            trajectoire_changement = False

        ##### DEPLACEMENTS #####
        # Le voisin va à chacune de ces trajectoires prédéfinies en fonction de si le joueur, il a une chance sur 2/3/4 (en fonction du niveau) d'aller dans une salle (sauf le garage ou la aslle de la cave), si le joueur passe devant lui il accélère
        # .1 = aller / .2 = retour /+ en cas de double changement +/ .3 = aller / .4 = retour
        # Des sous-trajectoires ont elles-aussi des sous-trajectoires d'ou les .11, etc

        # COULOIR
        # Position de départ : x=7; y=55 -> Position d'arrivée : x=11; y=55
        if trajectoire == 0:

            # Accélération
            if personnage_x < 59 + 64 and personnage_y < 75 + 64 and personnage_x > 0 + 64 and personnage_x > 0 + 64 or trajectoire_changement == False: # s'il voit le joueur:
                v = v * 1.5
            # Avancement
            x = x + v
            # Changement
            if x >= 11 + 64: # s'il arrive à destination:
                x = 11 + 64
                if personnage_x < 59 + 64 and personnage_y < 75 + 64 and personnage_x > 0 + 64 and personnage_x > 0 + 64 or trajectoire_changement == False: # s'il voit le joueur:
                    trajectoire = 1 # Change sa trajectoire
                else:
                    trajectoire = 0.11 # Change sa trajectoire
                    direction = 1 # Change la direction dans laquelle il regarde

        # SALLE DE BAIN
        # Position de départ : x=11; y=55 -> Position d'arrivée : x=11; y=27
        elif trajectoire == 0.11:

            # Accélération
            # Pas d'accélération
            # Avancement
            y = y - v
            # Changement
            if y <= 27 + 64: # s'il arrive à destination:
                y = 27 + 64
                direction = 2 # Change sa direction
                if personnage_x > 0 + 64 and personnage_y > 0 + 64 and personnage_x < 55 + 64 and personnage_y < 47 + 64: # s'il voit le joueur
                    trajectoire = 0.13 # Change sa trajectoire
                else:
                    trajectoire = 0.12 # Change sa trajectoire
        
        # Position de départ : x=11; y=27 -> Position d'arrivée : x=31; y=27
        elif trajectoire == 0.12:

            # Accélération
            # Pas d'accélération
            # Avancement
            x = x + v
            # Changement
            if x >= 31 + 64: # s'il arrive à destination:
                x = 31 + 64
                # Pause
                pause = pause - 1
                direction = 3 # Change sa direction
                if pause <= 0:
                    trajectoire = 0.21 # Change sa trajectoire
                    direction = 4 # Change sa direction
        
        # Position de départ : x=11; y=27 -> Position d'arrivée : x=52; y=6
        elif trajectoire == 0.13:
            
            # Accélération
            v = v * 2
            # Avancement
            if x < 52 + 64:
                x = x + v
            if y > 6 + 64:
                y = y - v / 1.5
            # Changement
            if x >= 52 + 64 and y <= 6 + 64: # S'il arrive à destination
                x = 52 + 64
                y = 6 + 64
                trajectoire = 0.14 # Change sa trajectoire
        
        # Position de départ : x=52; y=6 -> Position d'arrivée : x=77; y=6
        elif trajectoire == 0.14:
            
            # Accélération
            v = v * 2
            # Avancement
            x = x + v
            # Changement
            if x >= 77 + 64: # s'il arrive à destination:
                x = 77 + 64
                # Pause
                pause = pause - 1
                direction = 2 # Change sa direction
                if pause <= 0:
                    trajectoire = 0.23 # Change sa trajectoire
                    direction = 4 # Change sa direction
        
        # Position de départ : x=32; y=27 -> Position d'arrivée : x=11; y=27
        elif trajectoire == 0.21:
            
            # Accélération
            # Pas d'accélération
            # Avancement
            x = x - v
            # Changement
            if x <= 11 + 64: # s'il arrive à destination:
                x = 11 + 64
                trajectoire = 0.22 #  # Change sa trajectoire
                direction = 3  # Change sa direction
        
        # Position de départ : x=11; y=27 -> Position d'arrivée : x=11; y=55
        elif trajectoire == 0.22:
            
            # Accélération
            if personnage_x > 0 + 64 and personnage_y > 44 + 64 and personnage_x < 39 + 64 and personnage_y < 75 + 64: # S'il voit le joueur:
                v = v * 2
            # Avancement
            y = y + v
            # Changement
            if y >= 55 + 64: # s'il arrive à destination:
                y = 55 + 64
                if personnage_x > 0 + 64 and personnage_y > 44 + 64 and personnage_x < x and personnage_y < 75 + 64:
                    trajectoire = 11 # Change sa trajectoire
                    direction = 4 # Change sa direction
                else:
                    trajectoire = 11 # Change sa trajectoire
                    direction = 2 # Change sa direction
        
        # Position de départ : x=77; y=6 -> Position d'arrivée : x=45; y=6
        elif trajectoire == 0.23:
            
            # Accélération
            if personnage_x > 0 + 64 and personnage_y > 0 + 64 and personnage_x < 90 + 64 and personnage_y < 47 + 64: # s'il voit le joueur:
                v = v * 2
            # Avancement
            x = x - v
            # Changement
            if x <= 45 + 64: # s'il arrive à destination:
                x = 45 + 64
                trajectoire = 0.24 # Change sa trajectoire

        # Position de départ : x=45; y=6 -> Position d'arrivée : x=11; y=27
        elif trajectoire == 0.24:
            
            # Accélération
            if personnage_x > 0 + 64 and personnage_y > 0 + 64 and personnage_x < 55 + 64 and personnage_y < 47 + 64: # S'il voit le joueur:
                v = v * 2
            # Avancement
            if x > 11 + 64:
                x = x - v
            if y < 27 + 64:
                y = y + v / 1.5
            # Changement
            if x <= 11 + 64 and y >= 27 + 64:
                x = 11 + 64
                y = 27 + 64
                trajectoire = 0.22 # Change sa trajectoire
                direction = 3 # Change sa direction
        
        # COULOIR
        # Position de départ : x=11; y=55 -> Position d'arrivée : x=43; y=55
        elif trajectoire == 1:

            # Accélération
            if personnage_x > 0 + 64 and personnage_y > 44 + 64 and personnage_x < 59 + 64 and personnage_y < 75 + 64: # s'il voit le joueur:
                v = v * 2
            # Avancement
            x = x + v
            # Changement
            if x >= 43 + 64: # s'il arrive à destination:
                x = 43 + 64
                if personnage_x > 0 + 64 and personnage_y > 44 + 64 and personnage_x < x and personnage_y < 75 + 64: # s'il voit le joueur:
                    trajectoire = 10 # Change sa trajectoire
                    direction = 4 # Change sa direction
                else:
                    trajectoire = 2 # Change sa trajectoire
                    direction = 3 # Change sa direction
        
        # Position de départ : x=43; y=55 -> Position d'arrivée : x=43; y=143
        elif trajectoire == 2:

            # Accélération
            if personnage_y > y and x >= personnage_x - 2 and x <= personnage_x + personnage_size_x + 2 and personnage_y < 145 + 64: # s'il voit le joueur:
                v = v * 2
            # Avancement
            y = y + v
            # Changement
            if y >= 143 + 64: # s'il arrive à destination:
                y = 143 + 64
                if personnage_x > x and personnage_y > 136 + 64 and personnage_x < 108 + 64 and personnage_y < 156 + 64: # s'il voit le joueur:
                    trajectoire = 3 # Change sa trajectoire
                    direction = 2 # Change sa direction
                elif trajectoire_changement == True:
                    trajectoire = 2.11 # Change sa trajectoire
                else:
                    trajectoire = 3 # Change sa trajectoire
                    direction = 2 # Change sa direction
        
        # SALON
        # Position de départ : x=43; y=143 -> Position d'arrivée : x=43; y=188
        elif trajectoire == 2.11:

            # Accélération
            if personnage_x > 0 + 64 and personnage_y > 156 + 64 and personnage_x < 59 + 64 and personnage_y < 215 + 64: # S'il voit le joueur:
                v = v * 2
            # Avancement
            y = y + v
            # Changement
            if y >= 188 + 64: # s'il arrive à destination:
                y = 188 + 64
                if personnage_y > y and personnage_y < 215 + 64: # S'il voit le joueur:
                    trajectoire = 2.12 #  Change sa trajectoire
                else:
                    trajectoire = 2.13 #  Change sa trajectoire
                    direction = 4 # Change sa direction
        
        # Position de départ : x=43; y=188 -> Position d'arrivée : x=43; y=193
        elif trajectoire == 2.12:

            # Accélération
            if personnage_x > 34 + 64 and personnage_y > 184 + 64 and personnage_x < 59 + 64 and personnage_y < 215 + 64: # S'il voit le joueur:
                v = v * 2
            # Avancement
            y = y + v
            # Changement
            if y >= 193 + 64: # s'il arrive à destination:
                y = 193 + 64
                trajectoire = 2.22 #  Change sa trajectoire
                direction = 1 # Change sa direction

        # Position de départ : x=43; y=188 -> Position d'arrivée : x=36; y=188
        elif trajectoire == 2.13:

            # Accélération
            if personnage_x > 0 + 64 and personnage_y > 156 + 64 and personnage_x < 59 + 64 and personnage_y < 215 + 64: # S'il voit le joueur:
                v = v * 2
            # Avancement
            x = x - v
            # Changement
            if x <= 36 + 64: # s'il arrive à destination:
                x = 36 + 64
                # Pause
                pause = pause - 1
                direction = 4 # Change sa direction
                if pause <= 0:
                    trajectoire = 2.21 # Change sa trajectoire
                    direction = 2 # Change sa direction
        
        # Position de départ : x=36; y=188 -> Position d'arrivée : x=43; y=188
        elif trajectoire == 2.21:

            # Accélération
            # Pas d'accélération
            # Avancement
            x = x + v
            # Changement
            if x >= 43 + 64: # s'il arrive à destination:
                x = 43 + 64
                trajectoire = 2.22 # Change sa trajectoire
                direction = 1 # Change sa direction
        
        # Position de départ : x=43; y=188/y=193 -> Position d'arrivée : x=43; y=143
        elif trajectoire == 2.22:

            # Accélération
            if personnage_x > 0 + 64 and personnage_y > 156 + 64 and personnage_x < 59 + 64 and personnage_y < 215 + 64: # S'il voit le joueur:
                v = v * 2
            # Avancement
            y = y - v
            # Changement
            if y <= 143 + 64: # s'il arrive à destination:
                y = 143 + 64
                if personnage_x > 36 + 64 and personnage_y > 44 + 64 and personnage_x < 56 + 64 and personnage_y < y: # s'il voit le joueur:
                    trajectoire = 9 # Change sa trajectoire
                    direction = 1 # Change sa direction
                elif personnage_x > x and personnage_y > 136 + 64 and personnage_x < 108 + 64 and personnage_y < 159 + 64: # s'il voit le joueur:
                        trajectoire = 3 # Change sa trajectoire
                        direction = 2 # Change sa direction
                else:
                    if random.randint(1,4) == 1:
                        trajectoire = 9 # Change sa trajectoire
                        direction = 1 # Change sa direction
                    else:
                        trajectoire = 3 # Change sa trajectoire
                        direction = 2 # Change sa direction
        
        # COULOIR
        # Position de départ : x=43; y=143 -> Position d'arrivée : x=95; y=143
        elif trajectoire == 3:

            # Accélération
            if personnage_x > x and y >= personnage_y - 2 and y <= personnage_y + personnage_size_y + 2 and personnage_x < 180 + 64: # s'il voit le joueur:
                v = v * 2
            # Avancement
            x = x + v
            # Changement
            if x >= 95 + 64: # s'il arrive à destination:
                x = 95 + 64
                if trajectoire_changement == False or personnage_x > 91 + 64 and personnage_y > 136 + 64 and personnage_x < 180 + 64 and personnage_y < 159 + 64: # S'il voit le personnage
                    trajectoire = 4 # Change sa trajectoire
                else:
                    trajectoire = 3.11 # Change sa trajectoire (cuisine)
                    direction = 1 # Change sa direction

        # CUISINE
        # Position de départ : x=95; y=143 -> Position d'arrivée : x=95; y=123
        elif trajectoire == 3.11:

            # Accélération
            if personnage_x > 83 + 64 and personnage_y > 110 + 64 and personnage_x < 116 + 64 and personnage_y < 139 + 64: # S'il voit le joueur:
                v = v * 2
            # Avancement
            y = y - v
            # Changement
            if y <= 123 + 64: # s'il arrive à destination:
                y = 123 + 64
                if personnage_x > 72 + 64 and personnage_y > 103 + 64 and personnage_x < x and personnage_y < 139 + 64:  # S'il voit le joueur:
                    trajectoire = 3.12 # Change sa trajectoire
                    direction = 4 # Change sa direction
                else:
                    trajectoire = 3.13 # Change sa trajectoire
                    direction = 2 # Change sa direction
        
        # Position de départ : x=95; y=123 -> Position d'arrivée : x=80; y=123
        elif trajectoire == 3.12:

            # Accélération
            v = v * 2
            # Avancement
            x = x - v
            # Changement
            if x <= 80 + 64: # s'il arrive à destination:
                x = 80 + 64
                trajectoire = 3.24 # Change sa trajectoire
                direction = 2 # Change sa direction

        # Position de départ : x=95; y=123 -> Position d'arrivée : x=120; y=123
        elif trajectoire == 3.13:

            # Accélération
            if personnage_x > 95 + 64 and personnage_y > 103 + 64 and personnage_x < 143 + 64 and personnage_y < 139 + 64: # S'il voit le joueur:
                v = v * 2
            # Avancement
            x = x + v
            # Changement
            if x >= 120 + 64: # s'il arrive à destination:
                x = 120 + 64
                trajectoire = 3.14 #  Change sa trajectoire
                direction = 1 # Change la direction dans laquelle il regarde

        # Position de départ : x=120; y=123 -> Position d'arrivée : x=120; y=68
        elif trajectoire == 3.14:

            # Accélération
            if personnage_x > 111 + 64 and personnage_y > 52 + 64 and personnage_x < 143 + 64 and personnage_y < 139 + 64: # S'il voit le joueur:
                v = v * 2
            # Avancement
            y = y - v
            # Changement
            if y <= 68 + 64: # s'il arrive à destination:
                y = 68 + 64
                if personnage_x > 72 + 64 and personnage_y > 52 + 64 and personnage_x < 143 + 64 and personnage_y < 99 + 64: # S'il voit le joueur:
                    trajectoire = 3.15 #  Change sa trajectoire
                    direction = 4 # Change sa direction
                else:
                    # Pause
                    pause = pause - 1
                    if pause <= 0:
                        trajectoire = 3.22 # Change sa trajectoire
                        direction = 3 # Change sa direction
        
        # Position de départ : x=120; y=68 -> Position d'arrivée : x=80; y=68
        elif trajectoire == 3.15:

            # Accélération
            v = v * 2
            # Avancement
            x = x - v
            # Changement
            if x <= 80 + 64: # s'il arrive à destination:
                x = 80 + 64
                trajectoire = 3.21 #  Change sa trajectoire
                direction = 2 # Change sa direction

        # Position de départ : x=80; y=68 -> Position d'arrivée : x=120; y=68
        elif trajectoire == 3.21:

            # Accélération
            if personnage_x > x + 64 and personnage_y > 52 + 64 and personnage_x < 143 + 64 and personnage_y < 95 + 64: # S'il voit le joueur:
                v = v * 2
            # Avancement
            x = x + v
            # Changement
            if x >= 120 + 64: # s'il arrive à destination:
                x = 120 + 64
                trajectoire = 3.22 #  Change sa trajectoire
                direction = 3 # Change sa direction

        # Position de départ : x=120; y=68 -> Position d'arrivée : x=120; y=123
        elif trajectoire == 3.22:

            # Accélération
            if personnage_x > 111 + 64 and personnage_y > 55 + 64 and personnage_x < 143 + 64 and personnage_y < 139 + 64: # S'il voit le joueur:
                v = v * 2
            # Avancement
            y = y + v
            # Changement
            if y >= 123 + 64: # s'il arrive à destination:
                y = 123 + 64
                trajectoire = 3.23 # Change sa trajectoire
                direction = 4 # Change sa direction

        # Position de départ : x=120; y=123 -> Position d'arrivée : x=95; y=123
        elif trajectoire == 3.23:

            # Accélération
            if personnage_x > 72 + 64 and personnage_y > 103 + 64 and personnage_x < 143 + 64 and personnage_y < 139 + 64: # S'il voit le joueur:
                v = v * 2
            # Avancement
            x = x - v
            # Changement
            if x <= 95 + 64: # s'il arrive à destination:
                x = 95 + 64
                if personnage_x > 72 + 64 and personnage_y > 103 + 64 and personnage_x < 96 + 64 and personnage_y < 136 + 64: # S'il voit le joueur:
                    trajectoire = 3.12 #  Change sa trajectoire
                else:
                    trajectoire = 3.25 #  Change sa trajectoire
                    direction = 3 # Change sa direction

        # Position de départ : x=80; y=123 -> Position d'arrivée : x=95; y=123
        elif trajectoire == 3.24:

            # Accélération
            if personnage_x > 95 + 64 and personnage_y > 103 + 64 and personnage_x < 143 + 64 and personnage_y < 139 + 64: # S'il voit le joueur:
                v = v * 2
            # Avancement
            x = x + v
            # Changement
            if x >= 95 + 64: # s'il arrive à destination:
                x = 95 + 64
                if personnage_x > 95 + 64 and personnage_y > 103 + 64 and personnage_x < 143 + 64 and personnage_y < 139 + 64: # S'il voit le joueur:
                    trajectoire = 3.13 # Change sa trajectoire
                else:
                    trajectoire = 3.25 #  Change sa trajectoire
                    direction = 3 # Change sa direction

        # Position de départ : x=95; y=123 -> Position d'arrivée : x=95; y=143
        elif trajectoire == 3.25:

            # Accélération
            v = v * 2
            # Avancement
            y = y + v
            # Changement
            if y >= 143 + 64: # s'il arrive à destination:
                y = 143 + 64
                if personnage_x > 36 + 64 and personnage_y > 139 + 64 and personnage_x < x and personnage_y < 159 + 64: # s'il voit le joueur:
                    trajectoire = 8 # Change sa trajectoire
                    direction = 4 # Change sa direction
                elif personnage_x > x and personnage_y > 139 + 64 and personnage_x < 184 + 64 and personnage_y < 159 + 64: # s'il voit le joueur:
                        trajectoire = 4 # Change sa trajectoire
                        direction = 2 # Change sa direction
                else:
                    if random.randint(1,4) == 1:
                        trajectoire = 8 # Change sa trajectoire
                        direction = 4 # Change sa direction
                    else:
                        trajectoire = 4 #  Change sa trajectoire
                        direction = 2 # Change sa direction
        
        # COULOIR
        # Position de départ : x=95; y=143 -> Position d'arrivée : x=211; y=143
        elif trajectoire == 4:

            # Accélération
            if personnage_x > x and y >= personnage_y - 2 and y <= personnage_y + personnage_size_y + 2 and personnage_x < 252 + 64: # S'il voit le joueur:
                v = v * 2            
            # Avancement
            x = x + v
            # Changement
            if x >= 211 + 64: # S'il arrive à destination:
                x = 211 + 64
                if trajectoire_changement == False or personnage_x > 207 + 64 and personnage_y > 136 + 64 and personnage_x < 255 + 64 and personnage_y < 259 + 64: # S 'il voit le personnage:
                    trajectoire = 5
                else:
                    if random.randint(1,2) == 1:
                        trajectoire = 4.11 # Change sa trajectoire (salle des caméras)
                        direction = 1 # Change sa direction
                    else:
                        trajectoire = 4.31 # Change sa trajectoire (chambre)
                        direction = 3 # Change sa direction

        # Position de départ : x=211; y=143 -> Position d'arrivée : x=211; y=114
        elif trajectoire == 4.11:

            # Accélération
            if personnage_x > 188 + 64 and personnage_y > 40 + 64 and personnage_x < 255 + 64 and personnage_y < 139 + 64: # S 'il voit le personnage:
                v = v * 2
            # Avancement
            y = y - v
            # Changement
            if y <= 114 + 64: # s'il arrive à destination:
                y = 114 + 64
                if personnage_x > 188 + 64 and personnage_y > 40 + 64 and personnage_x < 255 + 64 and personnage_y < 139 + 64: # S 'il voit le personnage:
                    trajectoire = 4.13 # Cahnge sa trajectoire
                else:
                    trajectoire = 4.12 #  Change sa trajectoire
                    direction = 2 # Change sa direction

        # Position de départ : x=211; y=114 -> Position d'arrivée : x=236; y=114
        elif trajectoire == 4.12:

            # Accélération
            # Pas d'accélération
            # Avancement
            x = x + v
            # Changement
            if x >= 236 + 64: # s'il arrive à destination:
                x = 236 + 64
                # Pause
                pause = pause - 1
                if pause <= 0:
                    trajectoire = 4.21 # Change sa trajectoire
                    direction = 4 # Change sa direction

        # Position de départ : x=211; y=114 -> Position d'arrivée : x=211; y=114
        elif trajectoire == 4.13:

            # Spécial (poursuit le personnage au lieu d'aller à un enroit prédéfini)
            if personnage_x > 188 + 64 and personnage_y > 40 + 64 and personnage_x < 255 + 64 and personnage_y < 139 + 64: #S 'il voit le personnage:
                # Accélération
                v = v * 2
                # Avancement
                if x < personnage_x:
                    x = x + 1
                elif x > personnage_x:
                    x = x - 1
                if y < personnage_y:
                    y = y + 1
                elif y > personnage_y:
                    y = y - 1
            else:
                if x < 211 + 64:
                    x = x + v
                elif x > 211 + 64:
                    x = x - v
                if y < 114 + 64:
                    y = y + v
                elif y > 114 + 64:
                    y = y - v
                # Changement
                if x >= 210 + 64 and y >= 113 + 64 and x <= 212 + 64 and y <= 115 + 64:
                    x = 211 + 64
                    y = 112 + 64
                    trajectoire = 4.22 # Change sa trajectoire
                    direction = 3 # Change sa direction

        # Position de départ : x=236; y=114 -> Position d'arrivée : x=211; y=114
        elif trajectoire == 4.21:

            # Accélération
            # Pas d'accélération
            # Avancement
            x = x - v
            # Changement
            if x <= 211 + 64: # s'il arrive à destination:
                x = 211 + 64
                if personnage_x > 188 + 64 and personnage_y > 40 + 64 and personnage_x < 155 + 64 and personnage_y < 139 + 64: # S 'il voit le personnage:
                    trajectoire = 4.13 # Change sa trajectoire
                else:
                    trajectoire = 4.22 # Change sa trajectoire
                    direction = 3 # Change sa direction

        # Position de départ : x=211; y=114 -> Position d'arrivée : x=211; y=143
        elif trajectoire == 4.22:

            # Accélération
            # Pas d'accélération
            # Avancement
            y = y + v
            # Changement
            if y >= 143 + 64: # s'il arrive à destination:
                y = 143 + 64
                if personnage_x > 140 + 64 and personnage_y > 136 + 64 and personnage_x < x and personnage_y < 159 + 64: # s'il voit le joueur:
                    trajectoire = 5 # Change sa trajectoire
                    direction = 2 # Change sa direction
                else:
                    trajectoire = 7 # Change sa trajectoire
                    direction = 4 # Change sa direction

        # Position de départ : x=211; y=143 -> Position d'arrivée : x=211; y=164
        elif trajectoire == 4.31:

            # Accélération
            # Pas d'accélération
            # Avancement
            y = y + v
            # Changement
            if y >= 164 + 64: # S'il arrive à destination:
                y = 164 + 64
                if personnage_x > 188 + 64 and personnage_y > 156 + 64 and personnage_x < 255 + 64 and personnage_y < 215 + 64: # S'il voit le joueur:
                    trajectoire = 4.32 # Change sa trajectoire
                else:
                    trajectoire = 4.33 # Change sa trajectoire

        # Position de départ : x=211; y=164 -> Position d'arrivée : x=211; y=192
        elif trajectoire == 4.32:
            
            # Spécial (poursuit le personnage au lieu d'aller à un enroit prédéfini)
            if personnage_x > 188 + 64 and personnage_y > 156 + 64 and personnage_x < 255 + 64 and personnage_y < 215 + 64: #S 'il voit le personnage:
                # Accélération
                v = v * 2
                # Avancement
                if x < personnage_x:
                    x = x + 1
                elif x > personnage_x:
                    x = x - 1
                if y < personnage_y:
                    y = y + 1
                elif y > personnage_y:
                    y = y - 1
            else:
                if x < 211 + 64:
                    x = x + v
                elif x > 211 + 64:
                    x = x - v
                if y < 192 + 64:
                    y = y + v
                elif y > 192 + 64:
                    y = y - v
                # Changement
                if x >= 210 + 64 and y >= 191 + 64 and x <= 212 + 64 and y <= 193 + 64:
                    x = 211 + 64
                    y = 192 + 64
                    trajectoire = 4.33 # Change sa trajectoire
        
        # Position de départ : x=211; y=164 -> Position d'arrivée : x=211; y=192
        elif trajectoire == 4.33:

            # Accélération
            if personnage_x > 188 + 64 and personnage_y > 156 + 64 and personnage_x < 255 + 64 and personnage_y < 215 + 64: # S'il voit le joueur:
                v = v * 2
            # Avancement
            y = y + v
            # Changement
            if y >= 192 + 64: # S'il arrive à destination:
                y = 192 + 64
                # Pause
                pause = pause - 1
                if pause <= 0:
                    trajectoire = 4.41 # Change sa trajectoire
                    direction = 1 # Change sa direction
            
        # Position de départ : x=211; y=192 -> Position d'arrivée : x=211; y=143
        elif trajectoire == 4.41:

            # Accélération
            if personnage_x > 204 + 64 and personnage_y > 136 + 64 and personnage_x < 227 + 64 and personnage_y < 159 + 64: # S'il voit le joueur:
                v = v * 2
            # Avancement
            y = y - v
            # Changement
            if y <= 143 + 64: # S'il arrive à destination:
                y = 143 + 64
                if personnage_x > 140 + 64 and personnage_y > 136 + 64 and personnage_x < x and personnage_y < 159 + 64: # s'il voit le joueur:
                    trajectoire = 5 # Change sa trajectoire
                    direction = 2 # Change sa direction
                else:
                    trajectoire = 7 # Change sa trajectoire
                    direction = 4 # Change sa direction

        # Position de départ : x=211; y=143 -> Position d'arrivée : x=243; y=143
        elif trajectoire == 5:

            # Accélération
            if personnage_x > 224 + 64 and personnage_y > 136 + 64 and personnage_x < 255 + 64 and personnage_y < 159 + 64: # S'il voit le joueur:
                v = v * 2
            # Avancement
            x = x + v
            # Changement
            if x >= 243 + 64: # S'il arrive à destination:
                x = 243 + 64
                trajectoire = 6 # Change sa trajectoire
                direction = 4 # Change sa direction
        
        # Position de départ : x=243; y=143 -> Position d'arrivée : x=211; y=143
        elif trajectoire == 6:

            # Accélération
            if personnage_x > 188 + 64 and personnage_y > 136 + 64 and personnage_x < 255 + 64 and personnage_y < 159 + 64: # S'il voit le joueur:
                v = v * 2
            # Avancement
            x = x - v
            # Changement
            if x <= 211 + 64: # S'il arrive à destination:
                x = 211 + 64
                if trajectoire_changement == False or personnage_x > 188 + 64 and personnage_y > 136 + 64 and personnage_x < 255 + 64 and personnage_y < 159 + 64: # S'il voit le joueur:
                    trajectoire = 7 # Change sa trajectoire
                else:
                    if random.randint(1,2) == 1:
                        trajectoire = 4.11 # Change sa trajectoire (salle des caméras)
                        direction = 1 # Change sa direction
                    else:
                        trajectoire = 4.31 # Change sa trajectoire (chambre)
                        direction = 3 # Change sa direction
        
        # Position de départ : x=211; y=143 -> Position d'arrivée : x=95; y=143
        elif trajectoire == 7:

            # Accélération
            if personnage_x > 59 + 64 and personnage_y > 136 + 64 and personnage_x < x and personnage_y < 159 + 64: # S'il voit le joueur:
                v = v * 2
            # Avancement
            x = x - v
            # Changement
            if x <= 95 + 64: # S'il arrive à destination:
                x = 95 + 64
                if trajectoire_changement == False or personnage_x > 59 + 64 and personnage_y > 136 + 64 and personnage_x < x and personnage_y < 159 + 64: # S'il voit le joueur:
                    trajectoire = 8 # Change sa trajectoire
                else:
                    trajectoire = 3.11 # Change sa trajectoire (cuisine)
                    direction = 1 # Change sa direction

        # Position de départ : x=95; y=143 -> Position d'arrivée : x=43; y=143
        elif trajectoire == 8:

            # Accélération
            if personnage_x > 188 + 64 and personnage_y > 136 + 64 and personnage_x < 255 + 64 and personnage_y < 139 + 64: # S'il voit le joueur:
                v = v * 2
            # Avancement
            x = x - v
            # Changement
            if x <= 43 + 64: # S'il arrive à destination:
                x = 43 + 64
                if trajectoire_changement == False or personnage_x > 36 + 64 and personnage_y > 44 + 64 and personnage_x < 59 + 64 and personnage_y < 159 + 64: # S'il voit le joueur:
                    trajectoire = 9 # Change sa trajectoire
                    direction = 1 # Change sa direction
                else:
                    trajectoire = 2.11 # Change sa trajectoire (salon)
                    direction = 3 # Change sa direction

        # Position de départ : x=43; y=143 -> Position d'arrivée : x=43; y=55
        elif trajectoire == 9:

            # Accélération
            if personnage_x > 36 + 64 and personnage_y > 44 + 64 and personnage_x < 59 + 64 and personnage_y < y: # S'il voit le joueur:
                v = v * 2
            # Avancement
            y = y - v
            # Changement
            if y <= 55 + 64: # S'il arrive à destination:
                y = 55 + 64
                trajectoire = 10 # Change sa trajectoire
                direction = 4 # Change sa direction

        # Position de départ : x=95; y=143 -> Position d'arrivée : x=43; y=143
        elif trajectoire == 10:

            # Accélération
            if personnage_x > 0 + 64 and personnage_y > 44 + 64 and personnage_x < x and personnage_y < 75 + 64: # S'il voit le joueur:
                v = v * 2
            # Avancement
            x = x - v
            # Changement
            if x <= 11 + 64: # S'il arrive à destination:
                x = 11 + 64
                if trajectoire_changement == False or personnage_x > 0 + 64 and personnage_y > 44 + 64 and personnage_x < x and personnage_y < 75 + 64: # S'il voit le joueur:
                    trajectoire = 11 # Change sa trajectoire
                    direction = 4 # Change sa direction
                else:
                    trajectoire = 0.11 # Change sa trajectoire (salle de bain)
                    direction = 1 # Change sa direction
            
        # Position de départ : x=95; y=143 -> Position d'arrivée : x=43; y=143
        elif trajectoire == 11:

            # Accélération
            if personnage_x > 0 + 64 and personnage_y > 44 + 64 and personnage_x < x and personnage_y < 75 + 64: # S'il voit le joueur:
                v = v * 2
            # Avancement
            x = x - v
            # Changement
            if x <= 7 + 64: # S'il arrive à destination:
                x = 7 + 64
                trajectoire = 0 # Change sa trajectoire (salle de bain)
                direction = 2 # Change sa direction

        
        ##### COLLISIONS #####
        if touchee == False:


            # NE MARCHE PAS Vérifie si le voisin est touchée et arrête le projectile si oui
            # if personnage_direction == 1:
            #     if x + voisin_size_x >= tir_x and x <= tir_x + arme_tir_size_x and y >= tir_y:
            #         touchee = True
            #         tir_avancement = 0
            #         tir_x = 0
            #         tir_y = 0
            # elif personnage_direction == 2:
            #     if y + voisin_size_y >= tir_y and y <= tir_y + arme_tir_size_y and x >= tir_x:
            #         touchee = True
            #         tir_avancement = 0
            #         tir_x = 0
            #         tir_y = 0
            # if personnage_direction == 3:
            #     if x + voisin_size_x >= tir_x and x <= tir_x + arme_tir_size_x and y <= tir_y:
            #         touchee = True
            #         tir_avancement = 0
            #         tir_x = 0
            #         tir_y = 0
            # elif personnage_direction == 4:
            #     if y + voisin_size_y >= tir_y and y <= tir_y + arme_tir_size_y and x <= tir_x:
            #         touchee = True
            #         tir_avancement = 0
            #         tir_x = 0
            #         tir_y = 0

            # Initialise la marge de toucher entre le joueur et l'ia
            h = personnage_x - x # h = Horizontal
            v = personnage_y - y # v = Vertical
                
            # Vérifie les actions du joueur pour déterminer s'il touche l'ia
            if h >= - marge_px and h <= + voisin_size_x and v >= - marge_py and v <= + voisin_size_y: # Si le personnage est trop proche de l'ia et qu'il appuie sur E:
                personnage_vies = personnage_vies - 1
                personnage_x = personnage_defaut_x
                personnage_y = personnage_defaut_y

        # Renvoie les nouvelles valeurs des variables
        return x, y, trajectoire, pause, direction, touchee, endormi, personnage_x, personnage_y, personnage_vies, tir_avancement, tir_x, tir_y

    # =========================================================
    #  FONCTIONS D'INVENTAIRE
    # =========================================================

    def fonction_inventaire_selection_objet(objet_selectionne):
        """
        Affiche au joueur quel objet il sélectionne dans l'inventaire :
        - 1, 2, 3, 4 = Objet à l'emplacement ... de l'inventaire
        - 5 = Prendre pistolet
        - 0 = Ranger l'objet
        Entrée : L'objet sélectionné par le joueur
        Sortie : L'objet sélectionné par le joueur
        """

        ##### CONTROLES INVENTAIRE #####
        if pyxel.btn(pyxel.KEY_T): # Si le joueur presse T ou que l'objet sélectionné est le 5 :
            objet_selectionne = 5 # L'objet sélectionné est le 5 
        elif pyxel.btn(pyxel.KEY_W): # Si le joueur presse W :
            objet_selectionne = 0 # L'objet sélectionné est le 0
        elif pyxel.btn(pyxel.KEY_X): # Si le joueur presse X :
            objet_selectionne = 1 # L'objet sélectionné est le 1 et ses coordonnées sont attribuées à :
        elif pyxel.btn(pyxel.KEY_C): # Si le joueur presse C :
            objet_selectionne = 2 # L'objet sélectionné est le 2 et ses coordonnées sont attribuées à :
        elif pyxel.btn(pyxel.KEY_V): # Si le joueur presse V :
            objet_selectionne = 3 # L'objet sélectionné est le 3 et ses coordonnées sont attribuées à :
        elif pyxel.btn(pyxel.KEY_B): # Si le joueur presse B :
            objet_selectionne = 4 # L'objet sélectionné est le 4 et ses coordonnées sont attribuées à :
            
        # Renvoie les nouvelles valeurs des variables
        return objet_selectionne

    # =========================================================
    #  FONCTIONS DE L'ARME
    # =========================================================

    def fonction_arme(x, y, statut, personnage_x, personnage_y):
        """
        L'arme est un objet qui permet d'endormir le voisin pendant 2 secondes
        Il existe au total 2 munitions (+1 dans l'arme à son obtention) dans la map, et nécessite 30 secondes pour la recharger
        Entrée : Les coordonnées, le statut, le nombre de munitions et le cooldown de l'arme, Les coordonnées du personnage, L'objet sélectionné
        Sortie : Le statut de l'arme
        """
        
        # Eviter de relancer le programme si l'arme est déjà trouvée
        if statut == False: # Si l'arme n'est pas encore utilisée:

            # Initialise la marge de récupération de la clef
            h = personnage_x - x # h = Horizontal
            v = personnage_y - y # v = Vertical

            # Vérifie les actions du joueur pour sélectionner la bonne position de la clef
            if pyxel.btn(pyxel.KEY_E) and h >= - marge_interaction - marge_px and h <= + marge_interaction + arme_size_x and v >= - marge_interaction - marge_py and v <= + marge_interaction + arme_size_y: # Si le personnage est proche de l'arme et qu'il appuie sur E:
                statut = True # La clef est désormais récupérée
        
        # Renvoie les nouvelles valeurs des variables
        return statut

    def fonction_arme_tir(tir, munition, cooldown, x, y, direction, personnage_x, personnage_y, objet_selectionne, personnage_direction, voisin_x, voisin_y, touchee, p0, p1, p2, p3, p4, p5, p6):
        """
        Création du tir de l'objet : arme
        Entrée : Le statut, le nombre de munitions et le cooldown de l'arme, L'objet sélectionné
        Sortie : Le nombre de munitions et le cooldown de l'arme, Le statut du tir
        """

        if tir == False:

            # Réinitialise les valeurs par défaut:
            # ??
            # Actionne le tir ou non
            if cooldown > 0: # Si le cooldown n'est pas égal à 0
                cooldown = cooldown - 1 # Le cooldown diminue
            if pyxel.btn(pyxel.KEY_E) and munition >= 1 and cooldown <= 0 and objet_selectionne == 5: # Si le joueur appuie sur espace et que l'arme est bien chargée (cooldown à 0, munitions à 1 ou plus) et que l'objet sélectionné est le 0 (arme):
                munition = munition - 1 # Le nombre de munitions diminue
                cooldown = 450 # Le cooldown recommence à 30 secondes
                tir = True # Change le statut du tir
                x = personnage_x
                y = personnage_y
                direction = personnage_direction

        else:

            # Initialise les valeurs par défaut:
            pre_x = x
            pre_y = y
            # Avance la munition
            if direction == 1:
                y = y - 1.40
            elif direction == 2:
                x = x + 1.40
            elif direction == 3:
                y = y + 1.40
            elif direction == 4:
                x = x - 1.40
            # Détecte les collisions (mur/meubles/voisin) NE MARCHE PAS !!
            x, y, nothing = fonction_collisions("tir", pre_x, pre_y, x, y, p0, p1, p2, p3, p4, p5, p6)
            if x >= voisin_x - 2 and y >= voisin_y - 2 and x <= voisin_x + voisin_size_x + 2 and y <= voisin_y + voisin_size_y + 2:
                touchee = True
                tir = False
            elif x == pre_x and y == pre_y:
                tir = False

        # Renvoie les nouvelles valeurs des variables
        return tir, cooldown, munition, x, y, direction, touchee

    def fonction_arme_munition1(x, y, statut, personnage_x, personnage_y, munition):
        """
        Munitions n°1 pour l'arbalère, 5 sont trouvables sur la map
        Entrée : Les coordonnées et le statut de la munition, Le nombre de munitions de l'arme, Les coordonnées du personnage
        Sortie : Le statut de la munition, Le nombre de munitions de l'arme
        """

        # Initialise la marge de récupération de l'objet
        h = personnage_x - x
        v = personnage_y - y

        # Vérifie si le joueur peut récupérer la munition
        if pyxel.btn(pyxel.KEY_E) and h >= - marge_interaction - marge_px and h <= + marge_interaction + arme_munition_size_x and v >= - marge_interaction - marge_py and v <= + marge_interaction + arme_munition_size_y: # Si le joueur est assez proche de l'objet et qu'il appuie sur E:
            # pyxel.play(0, 0) # Joue le son d'objet récupéré
            munition = munition + 1 # Le nombre de munition augmente de 1
            statut = True # La munition est désormais récupéré
        
        # Renvoie les nouvelles valeurs des variables
        return statut, munition

    def fonction_arme_munition2(x, y, statut, personnage_x, personnage_y, munition):
        """
        Munitions n°2 pour l'arbalère, 5 sont trouvables sur la map
        Entrée : Les coordonnées et le statut de la munition, Le nombre de munitions de l'arme, Les coordonnées du personnage
        Sortie : Le statut de la munition, Le nombre de munitions de l'arme
        """

        # Initialise la marge de récupération de l'objet
        h = personnage_x - x
        v = personnage_y - y

        # Vérifie si le joueur peut récupérer la munition
        if pyxel.btn(pyxel.KEY_E) and h >= - marge_interaction - marge_px and h <= + marge_interaction + arme_munition_size_x and v >= - marge_interaction - marge_py and v <= + marge_interaction + arme_munition_size_y: # Si le joueur est assez proche de l'objet et qu'il appuie sur E:
            # pyxel.play(0, 0) # Joue le son d'objet récupéré
            munition = munition + 1 # Le nombre de munition augmente de 1
            statut = True # La munition est désormais récupéré
        
        # Renvoie les nouvelles valeurs des variables
        return statut, munition

    def fonction_arme_munition3(x, y, statut, personnage_x, personnage_y, munition):
        """
        Munitions n°3 pour l'arbalère, 5 sont trouvables sur la map
        Entrée : Les coordonnées et le statut de la munition, Le nombre de munitions de l'arme, Les coordonnées du personnage
        Sortie : Le statut de la munition, Le nombre de munitions de l'arme
        """
        
        # Initialise la marge de récupération de l'objet
        h = personnage_x - x
        v = personnage_y - y

        # Vérifie si le joueur peut récupérer la munition
        if pyxel.btn(pyxel.KEY_E) and h >= - marge_interaction - marge_px and h <= + marge_interaction + arme_munition_size_x and v >= - marge_interaction - marge_py and v <= + marge_interaction + arme_munition_size_y: # Si le joueur est assez proche de l'objet et qu'il appuie sur E:
            # pyxel.play(0, 0) # Joue le son d'objet récupéré
            munition = munition + 1 # Le nombre de munition augmente de 1
            statut = True # La munition est désormais récupéré
        
        # Renvoie les nouvelles valeurs des variables
        return statut, munition

    def fonction_arme_munition4(x, y, statut, personnage_x, personnage_y, munition):
        """
        Munitions n°4 pour l'arbalère, 5 sont trouvables sur la map
        Entrée : Les coordonnées et le statut de la munition, Le nombre de munitions de l'arme, Les coordonnées du personnage
        Sortie : Le statut de la munition, Le nombre de munitions de l'arme
        """

        # Initialise la marge de récupération de l'objet
        h = personnage_x - x
        v = personnage_y - y

        # Vérifie si le joueur peut récupérer la munition
        if pyxel.btn(pyxel.KEY_E) and h >= - marge_interaction - marge_px and h <= + marge_interaction + arme_munition_size_x and v >= - marge_interaction - marge_py and v <= + marge_interaction + arme_munition_size_y: # Si le joueur est assez proche de l'objet et qu'il appuie sur E:
            # pyxel.play(0, 0) # Joue le son d'objet récupéré
            munition = munition + 1 # Le nombre de munition augmente de 1
            statut = True # La munition est désormais récupéré
        
        # Renvoie les nouvelles valeurs des variables
        return statut, munition

    # =========================================================
    #  FONCTIONS DES CLEFS/PORTES
    # =========================================================

    # 0
    def fonction_clef0(x, y, statut, utilise, porte, personnage_x, personnage_y):
        """
        Clef n°0 associé à la porte n°0 (plusieures sont trouvables sur la map)
        Entrée : Coordonnées et Statut de la clef, Statut de la porte associée, Coordonnées du personnage, Objet sélectionné
        Sortie : Coordonnées et Statut de la clef
        """

        # Eviter de relancer le programme si la clef est déjà utilisée:
        if utilise == False: # Si le clef n'est pas encore utilisée:

            # Initialise la marge de récupération de la clef
            h = personnage_x - x # h = Horizontal
            v = personnage_y - y # v = Vertical

            # Vérifie les actions du joueur pour sélectionner la bonne position de la clef
            if statut == False: # Ne relance la vérification que si la clef n'est pas encore récupéré
                if pyxel.btn(pyxel.KEY_E) and h >= - marge_interaction - marge_px and h <= + marge_interaction + clef0_size_x and v >= - marge_interaction - marge_py and v <= + marge_interaction + clef0_size_y: # Si le personnage est proche de la clef et qu'il appuie sur E:
                    statut = True # La clef est désormais récupérée

            # Initialise la position de la clef
            if porte == True: # Si la porte associée à la clef est ouverte:
                utilise = True # La clef disparait

        # Renvoie les nouvelles valeurs des variables
        return statut, utilise

    def fonction_porte0(x, y, personnage_x, personnage_y, clef, objet_selectionne):
        """
        Porte n°0 associé à la clef n°0 (plusieures sont trouvables sur la map)
        Entrée : Coordonnées et Statut de la porte, Coordonnées et Statut de la clef associée, Objet sélectionné
        Sortie : Statut de la porte
        """

        # Eviter de relancer le programme si la clef n'est pas encore récupérée
        if clef == True: # Si la clef est récupérée:

            # Initialise la marge de récupération de la porte
            h = personnage_x - x # h = Horizontal
            v = personnage_y - y # v = Vertical

            # Vérifie que le personnage puisse ouvrir la porte
            if pyxel.btn(pyxel.KEY_E) and objet_selectionne == 4 and h >= - marge_interaction - marge_px and h <= + marge_interaction + porte0_size_x and v >= - marge_interaction - marge_py and v <= + marge_interaction + porte0_size_y: # Si le personnage est assez proche de la porte avec la clef en main et qu'il appuie sur E:
                return True # La porte est désormais ouverte

        # Renvoie les nouvelles valeurs des variables
        return False

    # 1
    def fonction_clef1(x, y, statut, utilise, porte, personnage_x, personnage_y):
        """
        Clef n°1 associé à la porte n°1 (plusieures sont trouvables sur la map)
        Entrée : Coordonnées et Statut de la clef, Statut de la porte associée, Coordonnées du personnage, Objet sélectionné
        Sortie : Coordonnées et Statut de la clef
        """

        # Eviter de relancer le programme si la clef est déjà utilisée:
        if utilise == False: # Si le clef n'est pas encore utilisée:

            # Initialise la marge de récupération de la clef
            h = personnage_x - x # h = Horizontal
            v = personnage_y - y # v = Vertical

            # Vérifie les actions du joueur pour sélectionner la bonne position de la clef
            if statut == False: # Ne relance la vérification que si la clef n'est pas encore récupéré
                if pyxel.btn(pyxel.KEY_E) and h >= - marge_interaction - marge_px and h <= + marge_interaction + clef1_size_x and v >= - marge_interaction - marge_py and v <= + marge_interaction + clef1_size_y: # Si le personnage est proche de la clef et qu'il appuie sur E:
                    statut = True # La clef est désormais récupérée

            # Initialise la position de la clef
            if porte == True: # Si la porte associée à la clef est ouverte:
                utilise = True # La clef disparait

        # Renvoie les nouvelles valeurs des variables
        return statut, utilise

    def fonction_porte1(x, y, personnage_x, personnage_y, clef, objet_selectionne):
        """
        Porte n°1 associé à la clef n°1 (plusieures sont trouvables sur la map)
        Entrée : Coordonnées et Statut de la porte, Coordonnées et Statut de la clef associée, Objet sélectionné
        Sortie : Statut de la porte
        """

        # Eviter de relancer le programme si la clef n'est pas encore récupérée
        if clef == True: # Si la clef est récupérée:

            # Initialise la marge de récupération de la porte
            h = personnage_x - x # h = Horizontal
            v = personnage_y - y # v = Vertical

            # Vérifie que le personnage puisse ouvrir la porte
            if pyxel.btn(pyxel.KEY_E) and objet_selectionne == 1 and h >= - marge_interaction - marge_px and h <= + marge_interaction + porte1_size_x and v >= - marge_interaction - marge_py and v <= + marge_interaction + porte1_size_y: # Si le personnage est assez proche de la porte avec la clef en main et qu'il appuie sur E:
                return True # La porte est désormais ouverte

        # Renvoie les nouvelles valeurs des variables
        return False

    # 2
    def fonction_clef2(x, y, statut, utilise, porte, personnage_x, personnage_y):
        """
        Clef n°2 associé à la porte n°2 (plusieures sont trouvables sur la map)
        Entrée : Coordonnées et Statut de la clef, Statut de la porte associée, Coordonnées du personnage, Objet sélectionné
        Sortie : Coordonnées et Statut de la clef
        """

        # Eviter de relancer le programme si la clef est déjà utilisée:
        if utilise == False: # Si le clef n'est pas encore utilisée:

            # Initialise la marge de récupération de la clef
            h = personnage_x - x # h = Horizontal
            v = personnage_y - y # v = Vertical

            # Vérifie les actions du joueur pour sélectionner la bonne position de la clef
            if statut == False: # Ne relance la vérification que si la clef n'est pas encore récupéré
                if pyxel.btn(pyxel.KEY_E) and h >= - marge_interaction - marge_px and h <= + marge_interaction + clef2_size_x and v >= - marge_interaction - marge_py and v <= + marge_interaction + clef2_size_y: # Si le personnage est proche de la clef et qu'il appuie sur E:
                    statut = True # La clef est désormais récupérée

            # Initialise la position de la clef
            if porte == True: # Si la porte associée à la clef est ouverte:
                utilise = True # L'clef disparait

        # Renvoie les nouvelles valeurs des variables
        return statut, utilise

    def fonction_porte2(x, y, personnage_x, personnage_y, clef, objet_selectionne):
        """
        Porte n°2 associé à la clef n°2 (plusieures sont trouvables sur la map)
        Entrée : Coordonnées et Statut de la porte, Coordonnées et Statut de la clef associée, Objet sélectionné
        Sortie : Statut de la porte
        """

        # Eviter de relancer le programme si la clef n'est pas encore récupérée
        if clef == True: # Si la clef est récupérée:

            # Initialise la marge de récupération de la porte
            h = personnage_x - x # h = Horizontal
            v = personnage_y - y # v = Vertical

            # Vérifie que le personnage puisse ouvrir la porte
            if pyxel.btn(pyxel.KEY_E) and objet_selectionne == 2 and h >= - marge_interaction - marge_px and h <= + marge_interaction + porte2_size_x and v >= - marge_interaction - marge_py and v <= + marge_interaction + porte2_size_y: # Si le personnage est assez proche de la porte avec la clef en main et qu'il appuie sur E:
                return True # La porte est désormais ouverte

        # Renvoie les nouvelles valeurs des variables
        return False

    # 3
    def fonction_clef3(x, y, statut, utilise, porte, personnage_x, personnage_y):
        """
        Clef n°3 associé à la porte n°3 (plusieures sont trouvables sur la map)
        Entrée : Coordonnées et Statut de la clef, Statut de la porte associée, Coordonnées du personnage, Objet sélectionné
        Sortie : Coordonnées et Statut de la clef
        """

        # Eviter de relancer le programme si la clef est déjà utilisée:
        if utilise == False: # Si le clef n'est pas encore utilisée:

            # Initialise la marge de récupération de la clef
            h = personnage_x - x # h = Horizontal
            v = personnage_y - y # v = Vertical

            # Vérifie les actions du joueur pour sélectionner la bonne position de la clef
            if statut == False: # Ne relance la vérification que si la clef n'est pas encore récupéré
                if pyxel.btn(pyxel.KEY_E) and h >= - marge_interaction - marge_px and h <= + marge_interaction + clef3_size_x and v >= - marge_interaction - marge_py and v <= + marge_interaction + clef3_size_y: # Si le personnage est proche de la clef et qu'il appuie sur E:
                    statut = True # La clef est désormais récupérée

            # Initialise la position de la clef
            if porte == True: # Si la porte associée à la clef est ouverte:
                utilise = True # L'clef disparait

        # Renvoie les nouvelles valeurs des variables
        return statut, utilise

    def fonction_porte3(x, y, personnage_x, personnage_y, clef, objet_selectionne):
        """
        Porte n°3 associé à la clef n°3 (plusieures sont trouvables sur la map)
        Entrée : Coordonnées et Statut de la porte, Coordonnées et Statut de la clef associée, Objet sélectionné
        Sortie : Statut de la porte
        """

        # Eviter de relancer le programme si la clef n'est pas encore récupérée
        if clef == True: # Si la clef est récupérée:

            # Initialise la marge de récupération de la porte
            h = personnage_x - x # h = Horizontal
            v = personnage_y - y # v = Vertical

            # Vérifie que le personnage puisse ouvrir la porte
            if pyxel.btn(pyxel.KEY_E) and objet_selectionne == 3 and h >= - marge_interaction - marge_px and h <= + marge_interaction + porte3_size_x and v >= - marge_interaction - marge_py and v <= + marge_interaction + porte3_size_y: # Si le personnage est assez proche de la porte avec la clef en main et qu'il appuie sur E:
                return True # La porte est désormais ouverte

        # Renvoie les nouvelles valeurs des variables
        return False

    # 4
    def fonction_clef4(x, y, statut, utilise, porte, personnage_x, personnage_y):
        """
        Clef n°4 associé à la porte n°4 (plusieures sont trouvables sur la map)
        Entrée : Coordonnées et Statut de la clef, Statut de la porte associée, Coordonnées du personnage, Objet sélectionné
        Sortie : Coordonnées et Statut de la clef
        """

        # Eviter de relancer le programme si la clef est déjà utilisée:
        if utilise == False: # Si le clef n'est pas encore utilisée:

            # Initialise la marge de récupération de la clef
            h = personnage_x - x # h = Horizontal
            v = personnage_y - y # v = Vertical

            # Vérifie les actions du joueur pour sélectionner la bonne position de la clef
            if statut == False: # Ne relance la vérification que si la clef n'est pas encore récupérée
                if pyxel.btn(pyxel.KEY_E) and h >= - marge_interaction - marge_px and h <= + marge_interaction + clef4_size_x and v >= - marge_interaction - marge_py and v <= + marge_interaction + clef4_size_y: # Si le personnage est proche de la clef et qu'il appuie sur E:
                    statut = True # La clef est désormais récupérée

            # Initialise la position de la clef
            if porte == True: # Si la porte associée à la clef est ouverte:
                utilise = True # L'clef disparait

        # Renvoie les nouvelles valeurs des variables
        return statut, utilise

    def fonction_porte4(x, y, personnage_x, personnage_y, clef, objet_selectionne):
        """
        Porte n°4 associé à la clef n°4 (plusieures sont trouvables sur la map)
        Entrée : Coordonnées et Statut de la porte, Coordonnées et Statut de la clef associée, Objet sélectionné
        Sortie : Statut de la porte
        """

        # Eviter de relancer le programme si la clef n'est pas encore récupérée
        if clef == True: # Si la clef est récupérée:

            # Initialise la marge de récupération de la porte
            h = personnage_x - x # h = Horizontal
            v = personnage_y - y # v = Vertical

            # Vérifie que le personnage puisse ouvrir la porte
            if pyxel.btn(pyxel.KEY_E) and objet_selectionne == 1 and h >= - marge_interaction - marge_px and h <= + marge_interaction + porte4_size_x and v >= - marge_interaction - marge_py and v <= + marge_interaction + porte4_size_y: # Si le personnage est assez proche de la porte avec la clef en main et qu'il appuie sur E:
                return True # La porte est désormais ouverte

        # Renvoie les nouvelles valeurs des variables
        return False

    # 5
    def fonction_clef5(x, y, statut, utilise, porte, personnage_x, personnage_y):
        """
        Clef n°5 associé à la porte n°5 (plusieures sont trouvables sur la map)
        Entrée : Coordonnées et Statut de la clef, Statut de la porte associée, Coordonnées du personnage, Objet sélectionné
        Sortie : Coordonnées et Statut de la clef
        """


        # Eviter de relancer le programme si la clef est déjà utilisée:
        if utilise == False: # Si le clef n'est pas encore utilisée:

            # Initialise la marge de récupération de la clef
            h = personnage_x - x # h = Horizontal
            v = personnage_y - y # v = Vertical

            # Vérifie les actions du joueur pour sélectionner la bonne position de la clef
            if statut == False: # Ne relance la vérification que si la clef n'est pas encore récupéré
                if pyxel.btn(pyxel.KEY_E) and h >= - marge_interaction - marge_px and h <= + marge_interaction + clef5_size_x and v >= - marge_interaction - marge_py and v <= + marge_interaction + clef5_size_y: # Si le personnage est proche de la clef et qu'il appuie sur E:
                    statut = True # La clef est désormais récupérée

            # Initialise la position de la clef
            if porte == True: # Si la porte associée à la clef est ouverte:
                utilise = True # L'clef disparait

        # Renvoie les nouvelles valeurs des variables
        return statut, utilise

    def fonction_porte5(x, y, personnage_x, personnage_y, clef, objet_selectionne):
        """
        Porte n°5 associé à la clef n°5 (plusieures sont trouvables sur la map)
        Entrée : Coordonnées et Statut de la porte, Coordonnées et Statut de la clef associée, Objet sélectionné
        Sortie : Statut de la porte
        """

        # Eviter de relancer le programme si la clef n'est pas encore récupérée
        if clef == True: # Si la clef est récupérée:

            # Initialise la marge de récupération de la porte
            h = personnage_x - x # h = Horizontal
            v = personnage_y - y # v = Vertical

            # Vérifie que le personnage puisse ouvrir la porte
            if pyxel.btn(pyxel.KEY_E) and objet_selectionne == 2 and h >= - marge_interaction - marge_px and h <= + marge_interaction + porte5_size_x and v >= - marge_interaction - marge_py and v <= + marge_interaction + porte5_size_y: # Si le personnage est assez proche de la porte avec la clef en main et qu'il appuie sur E:
                return True # La porte est désormais ouverte

        # Renvoie les nouvelles valeurs des variables
        return False

    # 6
    def fonction_clef6(x, y, statut, utilise, porte, personnage_x, personnage_y):
        """
        Clef n°6 associée à la porte n°6 (plusieures sont trouvables sur la map)
        Entrée : Coordonnées et Statut de la clef, Statut de la porte associée, Coordonnées du personnage, Objet sélectionné
        Sortie : Coordonnées et Statut de la clef
        """

        # Eviter de relancer le programme si la clef est déjà utilisée:
        if utilise == False: # Si le clef n'est pas encore utilisée:

            # Initialise la marge de récupération de la clef
            h = personnage_x - x # h = Horizontal
            v = personnage_y - y # v = Vertical

            # Vérifie les actions du joueur pour sélectionner la bonne position de la clef
            if statut == False: # Ne relance la vérification que si la clef n'est pas encore récupéré
                if pyxel.btn(pyxel.KEY_E) and h >= - marge_interaction - marge_px and h <= + marge_interaction + clef6_size_x and v >= - marge_interaction - marge_py and v <= + marge_interaction + clef6_size_y: # Si le personnage est proche de la clef et qu'il appuie sur E:
                    statut = True # La clef est désormais récupérée

            # Initialise la position de la clef
            if porte == True: # Si la porte associée à la clef est ouverte:
                utilise = True # L'clef disparait

        # Renvoie les nouvelles valeurs des variables
        return statut, utilise

    def fonction_porte6(x, y, personnage_x, personnage_y, clef, objet_selectionne):
        """
        Porte n°6 associé à la clef n°6 (plusieures sont trouvables sur la map)
        Entrée : Coordonnées et Statut de la porte, Coordonnées et Statut de la clef associée, Objet sélectionné
        Sortie : Statut de la porte
        """

        # Eviter de relancer le programme si la clef n'est pas encore récupérée
        if clef == True: # Si la clef est récupérée:

            # Initialise la marge de récupération de la porte
            h = personnage_x - x # h = Horizontal
            v = personnage_y - y # v = Vertical

            # Vérifie que le personnage puisse ouvrir la porte
            if pyxel.btn(pyxel.KEY_E) and objet_selectionne == 3 and h >= - marge_interaction - marge_px and h <= + marge_interaction + porte6_size_x and v >= - marge_interaction - marge_py and v <= + marge_interaction + porte6_size_y: # Si le personnage est assez proche de la porte avec la clef en main et qu'il appuie sur E:
                return True # La porte est désormais ouverte

        # Renvoie les nouvelles valeurs des variables
        return False

    # =========================================================
    #  FONCTIONS UPDATE
    # =========================================================
        
    def update0(page, niveau):
        """
        Update pour sélectionner le niveau
        Entrée : La page affichée et le niveau sélectionné
        Sortie : La page à afficher et Le niveau sélectionné
        """
        
        # Soit le joueur va vers le niveau au dessus et la page change vers le dessus etc
        if pyxel.btnr(pyxel.KEY_UP) or pyxel.btnr(pyxel.KEY_Z):
            if page == 2:
                page = 4
            elif page == 4:
                page = 3
            elif page == 3:
                page = 2

        elif pyxel.btnr(pyxel.KEY_DOWN) or pyxel.btnr(pyxel.KEY_S):
            if page == 2:
                page = 3
            elif page == 3:
                page = 4
            elif page == 4:
                page = 2

        elif pyxel.btnr(pyxel.KEY_SPACE):
            if page == 2:
                niveau = 1
            if page == 3:
                niveau = 2
            if page == 4:
                niveau = 3
            if page == 1:
                page = 2
        else:
            niveau = 0

        return page, niveau

    def update1(personnage_vies):
        """
        Update si le jeu est en cours, appelle toutes les fonctions du jeu
        Entrée : Le nombre de vies du personnage, 
        Sortie : Jeu gagné ou perdu et Le nombre de vies du personnage
        """
        ##### GLOBAL #####
        # Met en global les variables : JEU
        global jeu_gagne, jeu_perdu, jeu_timer, gamemod_statut
        # Met en global les variables de : PERSONNAGE
        global personnage_y, personnage_x, personnage_direction, personnage_vitesse
        global personnage_endurance, endurance_pleine_statut, endurance_inprogress_statut, endurance_faible_statut, collisions_statut, endurance_statut
        global personnage_selectionne1_res_x, personnage_selectionne1_res_y, personnage_selectionne2_res_x, personnage_selectionne2_res_y
        # Initialisation du personnage
        if personnage_selectionne == 1:
            personnage_selectionne1_res_x = personnage11_res_x
            personnage_selectionne2_res_x = personnage12_res_x
            personnage_selectionne1_res_y = personnage11_res_y
            personnage_selectionne2_res_y = personnage12_res_y
        elif personnage_selectionne == 2:
            personnage_selectionne1_res_x = personnage21_res_x
            personnage_selectionne2_res_x = personnage22_res_x
            personnage_selectionne1_res_y = personnage21_res_y
            personnage_selectionne2_res_y = personnage22_res_y
        elif personnage_selectionne == 3:
            personnage_selectionne1_res_x = personnage31_res_x
            personnage_selectionne2_res_x = personnage32_res_x
            personnage_selectionne1_res_y = personnage31_res_y
            personnage_selectionne2_res_y = personnage32_res_y
        elif personnage_selectionne == 4:
            personnage_selectionne1_res_x = personnage41_res_x
            personnage_selectionne2_res_x = personnage42_res_x
            personnage_selectionne1_res_y = personnage41_res_y
            personnage_selectionne2_res_y = personnage42_res_y
        # Met en global les variables de : INVENTAIRE
        global inventaire_objet_selectionne
        # Met en global les variables de : ARME
        global arme_x, arme_y, arme_size_x, arme_size_y, arme_statut, arme_cooldown, arme_munition, arme_direction
        global arme_tir_x, arme_tir_y, arme_tir_size_x, arme_tir_size_y, arme_tir_statut, arme_tir_avancement
        # Met en global les variables de : MUNITIONS
        global arme_munition1_x, arme_munition1_y, arme_munition1_statut
        global arme_munition2_x, arme_munition2_y, arme_munition2_statut
        global arme_munition3_x, arme_munition3_y, arme_munition3_statut
        global arme_munition4_x, arme_munition4_y, arme_munition4_statut
        # Met en global les variables de : CLEFS
        global clef0_x, clef0_y, clef0_statut, clef0_utilise
        global clef1_x, clef1_y, clef1_statut, clef1_utilise
        global clef2_x, clef2_y, clef2_statut, clef2_utilise
        global clef3_x, clef3_y, clef3_statut, clef3_utilise
        global clef4_x, clef4_y, clef4_statut, clef4_utilise
        global clef5_x, clef5_y, clef5_statut, clef5_utilise
        global clef6_x, clef6_y, clef6_statut, clef6_utilise
        # Met en global les variables de : PORTES
        global porte0_x, porte0_y, porte0_statut
        global porte1_x, porte1_y, porte1_statut
        global porte2_x, porte2_y, porte2_statut
        global porte3_x, porte3_y, porte3_statut
        global porte4_x, porte4_y, porte4_statut
        global porte5_x, porte5_y, porte5_statut
        global porte6_x, porte6_y, porte6_statut
        # Met en global les variables de : VOISIN
        global voisin_y, voisin_x, voisin_v, voisin_trajectoire, voisin_direction, voisin_touchee, voisin_endormi_temps, voisin_trajectoire_pause, voisin_trajectoire_changement_max, voisin_endormi_max, voisin_trajectoire_pause_max
        # Met en marche un chronomètre
        jeu_timer = jeu_timer + 1
        # Change les variables en fonction de la difficulté
        if jeu_niveau == 1:
            voisin_v = 0.4
            voisin_endormi_max = random.randint(4,5) * FPS - random.randint(1,30)
            voisin_trajectoire_changement_max = 85
            voisin_trajectoire_pause_max = random.randint(5,6) * FPS - random.randint(1,25)
        elif jeu_niveau == 2:
            voisin_v = 0.6
            voisin_endormi_max = random.randint(3,4) * FPS - random.randint(1,20)
            voisin_trajectoire_changement_max = 65
            voisin_trajectoire_pause_max = random.randint(4,5) * FPS - random.randint(1,25)
        elif jeu_niveau == 3:
            voisin_v = 0.8
            voisin_endormi_max = random.randint(2,3) * FPS - random.randint(1,10)
            voisin_trajectoire_changement_max = 45
            voisin_trajectoire_pause_max = random.randint(3,4) * FPS - random.randint(1,25)

        ##### DEPLACEMENTS #####
        personnage_x, personnage_y, personnage_endurance, personnage_direction, endurance_pleine_statut, endurance_inprogress_statut, endurance_faible_statut, jeu_gagne = fonction_personnage_deplacement(personnage_x, personnage_y, personnage_vitesse, personnage_direction, porte0_statut, porte1_statut, porte2_statut, porte3_statut, porte4_statut, porte5_statut, porte6_statut, collisions_statut, endurance_statut, personnage_endurance, endurance_pleine_statut, endurance_inprogress_statut, endurance_faible_statut)

        ##### VOISIN #####
        voisin_x, voisin_y, voisin_trajectoire, voisin_trajectoire_pause, voisin_direction, voisin_touchee, voisin_endormi_temps, personnage_x, personnage_y, personnage_vies, arme_tir_avancement, arme_tir_x, arme_tir_y = fonction_voisin(voisin_x, voisin_y, voisin_v, voisin_trajectoire, voisin_trajectoire_changement_max, voisin_trajectoire_pause_max, voisin_trajectoire_pause, voisin_direction, voisin_touchee, voisin_endormi_temps, voisin_endormi_max, personnage_x, personnage_y, personnage_vies, arme_tir_x, arme_tir_y, arme_tir_avancement)

        ##### INVENTAIRE #####
        inventaire_objet_selectionne = fonction_inventaire_selection_objet(inventaire_objet_selectionne)

        ##### ARME #####
        # Arme
        arme_statut = fonction_arme(arme_x, arme_y, arme_statut, personnage_x, personnage_y)
        if arme_statut == True:
            arme_tir_statut, arme_cooldown, arme_munition, arme_tir_x, arme_tir_y, arme_direction, voisin_touchee = fonction_arme_tir(arme_tir_statut, arme_munition, arme_cooldown, arme_tir_x, arme_tir_y, arme_direction, personnage_x, personnage_y, inventaire_objet_selectionne, personnage_direction, voisin_x, voisin_y, voisin_touchee, porte0_statut, porte1_statut, porte2_statut, porte3_statut, porte4_statut, porte5_statut, porte6_statut)
        # Munitions
        if jeu_niveau == 1:
            if arme_munition1_statut == False:
                arme_munition1_statut, arme_munition = fonction_arme_munition1(arme_munition1_x, arme_munition1_y, arme_munition1_statut, personnage_x, personnage_y, arme_munition)
            if arme_munition2_statut == False:
                arme_munition2_statut, arme_munition = fonction_arme_munition2(arme_munition2_x, arme_munition2_y, arme_munition2_statut, personnage_x, personnage_y, arme_munition)
            if arme_munition3_statut == False:
                arme_munition3_statut, arme_munition = fonction_arme_munition3(arme_munition3_x, arme_munition3_y, arme_munition3_statut, personnage_x, personnage_y, arme_munition)
            if arme_munition4_statut == False:
                arme_munition4_statut, arme_munition = fonction_arme_munition4(arme_munition4_x, arme_munition4_y, arme_munition4_statut, personnage_x, personnage_y, arme_munition)
        elif jeu_niveau == 2:
            if arme_munition1_statut == False:
                arme_munition1_statut, arme_munition = fonction_arme_munition1(arme_munition1_x, arme_munition1_y, arme_munition1_statut, personnage_x, personnage_y, arme_munition)
            if arme_munition2_statut == False:
                arme_munition2_statut, arme_munition = fonction_arme_munition2(arme_munition2_x, arme_munition2_y, arme_munition2_statut, personnage_x, personnage_y, arme_munition)
            if arme_munition3_statut == False:
                arme_munition3_statut, arme_munition = fonction_arme_munition3(arme_munition3_x, arme_munition3_y, arme_munition3_statut, personnage_x, personnage_y, arme_munition)
        elif jeu_niveau == 3:
            if arme_munition1_statut == False:
                arme_munition1_statut, arme_munition = fonction_arme_munition1(arme_munition1_x, arme_munition1_y, arme_munition1_statut, personnage_x, personnage_y, arme_munition)
            if arme_munition2_statut == False:
                arme_munition2_statut, arme_munition = fonction_arme_munition2(arme_munition2_x, arme_munition2_y, arme_munition2_statut, personnage_x, personnage_y, arme_munition)

        ##### CLEFS/PORTES #####
        # 0
        clef0_statut, clef0_utilise = fonction_clef0(clef0_x, clef0_y, clef0_statut, clef0_utilise, porte0_statut, personnage_x, personnage_y)
        if porte0_statut == False:
            porte0_statut = fonction_porte0(porte0_x, porte0_y, personnage_x, personnage_y, clef0_statut, inventaire_objet_selectionne)
        # 1
        clef1_statut, clef1_utilise = fonction_clef1(clef1_x, clef1_y, clef1_statut, clef1_utilise, porte1_statut, personnage_x, personnage_y)
        if porte1_statut == False:
            porte1_statut = fonction_porte1(porte1_x, porte1_y, personnage_x, personnage_y, clef1_statut, inventaire_objet_selectionne)
        # 2
        clef2_statut, clef2_utilise = fonction_clef2(clef2_x, clef2_y, clef2_statut, clef2_utilise, porte2_statut, personnage_x, personnage_y)
        if porte2_statut == False:
            porte2_statut = fonction_porte2(porte2_x, porte2_y, personnage_x, personnage_y, clef2_statut, inventaire_objet_selectionne)
        # 3
        clef3_statut, clef3_utilise = fonction_clef3(clef3_x, clef3_y, clef3_statut, clef3_utilise, porte3_statut, personnage_x, personnage_y)
        if porte3_statut == False:
            porte3_statut = fonction_porte3(porte3_x, porte3_y, personnage_x, personnage_y, clef3_statut, inventaire_objet_selectionne)
        # 4
        clef4_statut, clef4_utilise = fonction_clef4(clef4_x, clef4_y, clef4_statut, clef4_utilise, porte4_statut, personnage_x, personnage_y)
        if porte4_statut == False:
            porte4_statut = fonction_porte4(porte4_x, porte4_y, personnage_x, personnage_y, clef4_statut, inventaire_objet_selectionne)
        # 5
        clef5_statut, clef5_utilise = fonction_clef5(clef5_x, clef5_y, clef5_statut, clef5_utilise, porte5_statut, personnage_x, personnage_y)
        if porte5_statut == False:
            porte5_statut = fonction_porte5(porte5_x, porte5_y, personnage_x, personnage_y, clef5_statut, inventaire_objet_selectionne)
        # 6
        clef6_statut, clef6_utilise = fonction_clef6(clef6_x, clef6_y, clef6_statut, clef6_utilise, porte6_statut, personnage_x, personnage_y)
        if porte6_statut == False:
            porte6_statut = fonction_porte6(porte6_x, porte6_y, personnage_x, personnage_y, clef6_statut, inventaire_objet_selectionne)

        ##### DEVELOPPEMENT #####
        gamemod_statut, jeu_gagne, jeu_perdu, collisions_statut, endurance_statut, arme_statut, arme_munition, porte0_statut, porte1_statut, porte2_statut, porte3_statut, porte4_statut, porte5_statut, porte6_statut = fonction_godmode(gamemod_statut, jeu_gagne, jeu_perdu, collisions_statut, endurance_statut, arme_statut, arme_munition, porte0_statut, porte1_statut, porte2_statut, porte3_statut, porte4_statut, porte5_statut, porte6_statut)
        
        return jeu_gagne, jeu_perdu, personnage_vies

    def update():
        """
        Mise à jour des variables 30 fois par seconde
        """

        ##### GLOBAL #####
        # Met en global les variables : FEUNETRE
        global jeu_gagne, jeu_niveau, jeu_perdu, jeu_statut, personnage_selectionne, jeu_page, personnage_vies

        if jeu_gagne == True and jeu_statut == False or jeu_perdu == True and jeu_statut == False:

            # Si le joueur appuie sur espace tout recommence depuis le départ
            if pyxel.btnr(pyxel.KEY_SPACE):
                # Réinitialise toutes les variables du jeu
                global TITLE, WIDTH, HEIGHT, FPS, jeu_timer, gamemod_statut, collisions_statut, endurance_statut, personnage_defaut_x, personnage_defaut_y, personnage_x, personnage_y, personnage_direction, personnage_vitesse, personnage_vies_max, personnage_endurance, endurance_pleine_statut, endurance_inprogress_statut, endurance_faible_statut, personnage_selectionne1_res_x, personnage_selectionne2_res_x, personnage_selectionne1_res_y, personnage_selectionne2_res_y, personnage_size_x, personnage_size_y, personnage11_res_x, personnage11_res_y, personnage12_res_x, personnage12_res_y, personnage21_res_x, personnage21_res_y, personnage22_res_x, personnage22_res_y, personnage31_res_x, personnage31_res_y, personnage32_res_x, personnage32_res_y, personnage41_res_x, personnage41_res_y, personnage42_res_x, personnage42_res_y, voisin_defaut_x, voisin_defaut_y, voisin_v, voisin_trajectoire, voisin_direction, voisin_x, voisin_y, voisin_res1_x, voisin_res1_y, voisin_res2_x, voisin_res2_y, voisin_size_x, voisin_size_y, voisin_touchee, voisin_endormi_temps, voisin_endormi_max, voisin_trajectoire_pause, voisin_trajectoire_pause_max, voisin_trajectoire_changement_max, inventaire_objet_selectionne, inventaire_objet_selectionne_x, inventaire_objet_selectionne_y, inventaire_munition_slot_x, inventaire_munition_slot_y, marge_interaction, marge_px, marge_py, arme_defaut_x, arme_defaut_y, arme_x, arme_y, arme_size_x, arme_size_y, arme_bar_color, arme_statut, arme_tir_avancement, arme_cooldown, arme_munition, arme_direction, arme_tir_x, arme_tir_y, arme_tir_size_x, arme_tir_size_y, arme_tir_statut, arme_res_x, arme_res_y, arme_munition_count, arme_munition_size_x, arme_munition_size_y, arme_munition1_statut, arme_munition1_defaut_x, arme_munition1_defaut_y, arme_munition1_x, arme_munition1_y, arme_munition1_res_x, arme_munition1_res_y, arme_munition2_statut, arme_munition2_defaut_x, arme_munition2_defaut_y, arme_munition2_x, arme_munition2_y, arme_munition2_res_x, arme_munition2_res_y, arme_munition3_statut, arme_munition3_defaut_x, arme_munition3_defaut_y, arme_munition3_x, arme_munition3_y, arme_munition3_res_x, arme_munition3_res_y, arme_munition4_statut, arme_munition4_defaut_x, arme_munition4_defaut_y, arme_munition4_x, arme_munition4_y, arme_munition4_res_x, arme_munition4_res_y, clef0_defaut_x, clef0_defaut_y, clef0_x, clef0_y, clef0_statut, clef0_size_x, clef0_size_y, clef0_res_x, clef0_res_y, clef0_utilise, clef1_defaut_x, clef1_defaut_y, clef1_x, clef1_y, clef1_statut, clef1_size_x, clef1_size_y, clef1_res_x, clef1_res_y, clef1_utilise, clef2_defaut_x, clef2_defaut_y, clef2_x, clef2_y, clef2_statut, clef2_size_x, clef2_size_y, clef2_res_x, clef2_res_y, clef2_utilise, clef3_defaut_x, clef3_defaut_y, clef3_x, clef3_y, clef3_statut, clef3_size_x, clef3_size_y, clef3_res_x, clef3_res_y, clef3_utilise, clef4_defaut_x, clef4_defaut_y, clef4_x, clef4_y, clef4_statut, clef4_size_x, clef4_size_y, clef4_res_x, clef4_res_y, clef4_utilise, clef5_defaut_x, clef5_defaut_y, clef5_x, clef5_y, clef5_defaut_y, clef5_statut, clef5_size_x, clef5_size_y, clef5_res_x, clef5_res_y, clef5_utilise, clef6_defaut_x, clef6_defaut_y, clef6_x, clef6_y, clef6_statut, clef6_size_x, clef6_size_y, clef6_res_x, clef6_res_y, clef6_utilise, porte0_defaut_x, porte0_defaut_y, porte0_x, porte0_y, porte0_statut, porte0_size_x, porte0_size_y, porte0_res_x, porte0_res_y, porte1_defaut_x, porte1_defaut_y, porte1_x, porte1_y, porte1_statut, porte1_size_x, porte1_size_y, porte1_res_x, porte1_res_y, porte2_defaut_x, porte2_defaut_y, porte2_x, porte2_y, porte2_statut, porte2_size_x, porte2_size_y, porte2_res_x, porte2_res_y, porte3_defaut_x, porte3_defaut_y, porte3_x, porte3_y, porte3_statut, porte3_size_x, porte3_size_y, porte3_res_x, porte3_res_y, porte4_defaut_x, porte4_defaut_y, porte4_x, porte4_y, porte4_statut, porte4_size_x, porte4_size_y, porte4_res_x, porte4_res_y, porte5_defaut_x, porte5_defaut_y, porte5_x, porte5_y, porte5_statut, porte5_size_x, porte5_size_y, porte5_res_x, porte5_res_y, porte6_defaut_x, porte6_defaut_y, porte6_x, porte6_y, porte6_statut, porte6_size_x, porte6_size_y, porte6_res_x, porte6_res_y
                TITLE, WIDTH, HEIGHT, FPS, jeu_statut, jeu_perdu, jeu_gagne, jeu_niveau, jeu_page, jeu_timer, gamemod_statut, collisions_statut, endurance_statut, personnage_defaut_x, personnage_defaut_y, personnage_x, personnage_y, personnage_direction, personnage_vitesse, personnage_vies_max, personnage_vies, personnage_endurance, endurance_pleine_statut, endurance_inprogress_statut, endurance_faible_statut, personnage_selectionne, personnage_selectionne1_res_x, personnage_selectionne2_res_x, personnage_selectionne1_res_y, personnage_selectionne2_res_y, personnage_size_x, personnage_size_y, personnage11_res_x, personnage11_res_y, personnage12_res_x, personnage12_res_y, personnage21_res_x, personnage21_res_y, personnage22_res_x, personnage22_res_y, personnage31_res_x, personnage31_res_y, personnage32_res_x, personnage32_res_y, personnage41_res_x, personnage41_res_y, personnage42_res_x, personnage42_res_y, voisin_defaut_x, voisin_defaut_y, voisin_v, voisin_trajectoire, voisin_direction, voisin_x, voisin_y, voisin_res1_x, voisin_res1_y, voisin_res2_x, voisin_res2_y, voisin_size_x, voisin_size_y, voisin_touchee, voisin_endormi_temps, voisin_endormi_max, voisin_trajectoire_pause, voisin_trajectoire_pause_max, voisin_trajectoire_changement_max, inventaire_objet_selectionne, inventaire_objet_selectionne_x, inventaire_objet_selectionne_y, inventaire_munition_slot_x, inventaire_munition_slot_y, marge_interaction, marge_px, marge_py, arme_defaut_x, arme_defaut_y, arme_x, arme_y, arme_size_x, arme_size_y, arme_bar_color, arme_statut, arme_tir_avancement, arme_cooldown, arme_munition, arme_direction, arme_tir_x, arme_tir_y, arme_tir_size_x, arme_tir_size_y, arme_tir_statut, arme_res_x, arme_res_y, arme_munition_count, arme_munition_size_x, arme_munition_size_y, arme_munition1_statut, arme_munition1_defaut_x, arme_munition1_defaut_y, arme_munition1_x, arme_munition1_y, arme_munition1_res_x, arme_munition1_res_y, arme_munition2_statut, arme_munition2_defaut_x, arme_munition2_defaut_y, arme_munition2_x, arme_munition2_y, arme_munition2_res_x, arme_munition2_res_y, arme_munition3_statut, arme_munition3_defaut_x, arme_munition3_defaut_y, arme_munition3_x, arme_munition3_y, arme_munition3_res_x, arme_munition3_res_y, arme_munition4_statut, arme_munition4_defaut_x, arme_munition4_defaut_y, arme_munition4_x, arme_munition4_y, arme_munition4_res_x, arme_munition4_res_y, clef0_defaut_x, clef0_defaut_y, clef0_x, clef0_y, clef0_statut, clef0_size_x, clef0_size_y, clef0_res_x, clef0_res_y, clef0_utilise, clef1_defaut_x, clef1_defaut_y, clef1_x, clef1_y, clef1_statut, clef1_size_x, clef1_size_y, clef1_res_x, clef1_res_y, clef1_utilise, clef2_defaut_x, clef2_defaut_y, clef2_x, clef2_y, clef2_statut, clef2_size_x, clef2_size_y, clef2_res_x, clef2_res_y, clef2_utilise, clef3_defaut_x, clef3_defaut_y, clef3_x, clef3_y, clef3_statut, clef3_size_x, clef3_size_y, clef3_res_x, clef3_res_y, clef3_utilise, clef4_defaut_x, clef4_defaut_y, clef4_x, clef4_y, clef4_statut, clef4_size_x, clef4_size_y, clef4_res_x, clef4_res_y, clef4_utilise, clef5_defaut_x, clef5_defaut_y, clef5_x, clef5_y, clef5_defaut_y, clef5_statut, clef5_size_x, clef5_size_y, clef5_res_x, clef5_res_y, clef5_utilise, clef6_defaut_x, clef6_defaut_y, clef6_x, clef6_y, clef6_statut, clef6_size_x, clef6_size_y, clef6_res_x, clef6_res_y, clef6_utilise, porte0_defaut_x, porte0_defaut_y, porte0_x, porte0_y, porte0_statut, porte0_size_x, porte0_size_y, porte0_res_x, porte0_res_y, porte1_defaut_x, porte1_defaut_y, porte1_x, porte1_y, porte1_statut, porte1_size_x, porte1_size_y, porte1_res_x, porte1_res_y, porte2_defaut_x, porte2_defaut_y, porte2_x, porte2_y, porte2_statut, porte2_size_x, porte2_size_y, porte2_res_x, porte2_res_y, porte3_defaut_x, porte3_defaut_y, porte3_x, porte3_y, porte3_statut, porte3_size_x, porte3_size_y, porte3_res_x, porte3_res_y, porte4_defaut_x, porte4_defaut_y, porte4_x, porte4_y, porte4_statut, porte4_size_x, porte4_size_y, porte4_res_x, porte4_res_y, porte5_defaut_x, porte5_defaut_y, porte5_x, porte5_y, porte5_statut, porte5_size_x, porte5_size_y, porte5_res_x, porte5_res_y, porte6_defaut_x, porte6_defaut_y, porte6_x, porte6_y, porte6_statut, porte6_size_x, porte6_size_y, porte6_res_x, porte6_res_y = reset()

        elif jeu_statut == False and jeu_gagne == False and jeu_perdu == False:
                
            # Change les pages du menu jusqu'à la sélection d'un niveau
            jeu_page, jeu_niveau = update0(jeu_page, jeu_niveau)
            if jeu_niveau != 0:
                # Lance le jeu
                jeu_statut = True
                if jeu_niveau == 1:
                    personnage_vies_max = 3
                elif jeu_niveau == 2:
                    personnage_vies_max = 2
                elif jeu_niveau == 3:
                    personnage_vies_max = 1
                personnage_vies = personnage_vies_max

        elif jeu_statut == True and personnage_selectionne == 0:

            # Après avoir sélectionné le niveau le joueur sélectionne son personnage
            personnage_selectionne = fonction_selection_personnage()

        else:

            # Si le joueur a fini de choisir le niveau et son personnage le jeu commence
            jeu_gagne, jeu_perdu, personnage_vies = update1(personnage_vies)
            # Si le personnage n'a plus aucune vie ou s'il a finit par descendre dans la cave le jeu se finit (puis l'écran en question se lance)
            if personnage_vies == 0:
                jeu_perdu = True
            if jeu_perdu == True or jeu_gagne == True:
                jeu_statut = False

    # =========================================================
    #  FONCTION DRAW
    # =========================================================

    def draw():
        """
        Affichage des objets 30 fois par seconde
        """

        # Efface l'écran
        pyxel.cls(0)
        global arme_tir_avancement, FPS, WIDTH, HEIGHT

        if jeu_gagne == True:

            # Affiche au joueur qu'il a perdu avec l'écran des stats
            pyxel.camera(0, 0)
            pyxel.text(48, 4, "GAGNE!!!", random.randint(0, 15))
            pyxel.text(2, 18, "STATS:", 7)
            pyxel.text(2, 30, "Difficultee :", 7)
            pyxel.text(2, 36, str(jeu_niveau), 2)
            pyxel.text(2, 48, "Vies restantes :", 7)
            pyxel.text(2, 54, str(personnage_vies) + " / " + str(personnage_vies_max), 2)
            pyxel.text(2, 66, "Temps :", 7)
            pyxel.text(2, 72, str(jeu_timer//FPS) + " secondes", 2)
            pyxel.text(2, 100, "Suite dans la seconde partie...", 7)
            pyxel.text(22, 120, "PRESS SPACE TO RESTART", random.randint(0, 15))
        
        elif jeu_perdu == True:

            # Affiche au joueur qu'il a perdu avec l'écran des stats
            pyxel.camera(0, 0)
            pyxel.text(48, 4, "PERDU...", random.randint(0, 15))
            pyxel.text(2, 18, "STATS:", 7)
            pyxel.text(2, 30, "Difficultee :", 7)
            pyxel.text(2, 36, str(jeu_niveau), 2)
            pyxel.text(2, 48, "Vies restantes :", 7)
            pyxel.text(2, 54, str(personnage_vies) + " / " + str(personnage_vies_max), 2)
            pyxel.text(2, 66, "Temps :", 7)
            pyxel.text(2, 72, str(jeu_timer//FPS) + " secondes", 2)
            pyxel.text(22, 120, "PRESS SPACE TO RESTART", random.randint(0, 15))
            
        elif jeu_statut == False and jeu_perdu == False and jeu_gagne == False:

            # CHANGEMENT DE PAGE (sélection de niveau)
            if jeu_page == 1:
                pyxel.blt(0, 0, 2, 0, 0, 128, 128)
            elif jeu_page == 2:
                pyxel.blt(0, 0, 2, 128, 0, 128, 128)
            elif jeu_page == 3:
                pyxel.blt(0, 0, 2, 0, 128, 128, 128)
            elif jeu_page == 4:
                pyxel.blt(0, 0, 2, 128, 128, 128, 128)
            
        elif jeu_statut == True and personnage_selectionne == 0:

            # CHANGEMENT DE PAGE (sélection de personnage)
            # 1
            pyxel.blt(12, 20, 0, 0, 48, 32, 16, 7)
            pyxel.text(11, 20+18, "Press : 1", 7)
            # 2
            pyxel.blt(76, 20, 0, 0, 64, 32, 16, 7)
            pyxel.text(75, 20+18, "Press : 2", 7)
            # 3
            pyxel.blt(12, 84, 0, 0, 80, 32, 16, 7)
            pyxel.text(11, 84+18, "Press : 3", 7)
            # 4
            pyxel.blt(76, 84, 0, 0, 96, 32, 16, 7)
            pyxel.text(75, 84+18, "Press : 4", 7)

        else:

            # Réinitialise les coordonnées des slots
            slot_y = 117
            slot1_x = 4
            slot2_x = 14
            slot3_x = 24
            slot4_x = 34
            arme_slot_x = 58
            arme_slot_y = 116

            ##### TILEMAP #####
            # AFffiche la tilemap et change la camera en fonction de l'emplacement du personnage et des salles
            pyxel.bltm(0, 0, 0, 0, 0, 512, 512)
            # Y1
            if personnage_y >= 100*0 and personnage_y <= 100*1:
                interface_y = 100 * 0
                if personnage_x >= WIDTH * 0 and personnage_x <= WIDTH * 1:
                    pyxel.camera(WIDTH * 0, 100*0)
                    interface_x = WIDTH * 0
                elif personnage_x > WIDTH * 1 - 4 and personnage_x <= WIDTH * 2 - 4:
                    pyxel.camera(WIDTH * 1 - 4, 100*0)
                    interface_x = WIDTH * 1 - 4
                elif personnage_x > WIDTH * 2 - 4 and personnage_x <= WIDTH * 3 - 4:
                    pyxel.camera(WIDTH * 2 - 4, 100*0)
                    interface_x = WIDTH * 2 - 4
                elif personnage_x > WIDTH * 3 - 4 and personnage_x <= WIDTH * 4 - 4:
                    pyxel.camera(WIDTH * 3 - 4, 100*0)
                    interface_x = WIDTH * 3 - 4
            # Y2
            elif personnage_y >= 100*1 and personnage_y <= 100*2:
                interface_y = 100 * 1
                if personnage_x > WIDTH * 0 and personnage_x <= WIDTH * 1:
                    pyxel.camera(WIDTH * 0, 100*1)
                    interface_x = WIDTH * 0
                elif personnage_x > WIDTH * 1 - 4 and personnage_x <= WIDTH * 2 - 4:
                    pyxel.camera(WIDTH * 1 - 4, 100*1)
                    interface_x = WIDTH * 1 - 4
                elif personnage_x > WIDTH * 2 - 4 and personnage_x <= WIDTH * 3 - 4:
                    pyxel.camera(WIDTH * 2 - 4, 100*1)
                    interface_x = WIDTH * 2 - 4
                elif personnage_x > WIDTH * 3 - 4 and personnage_x <= WIDTH * 4 - 4:
                    pyxel.camera(WIDTH * 3 - 4, 100*1)
                    interface_x = WIDTH * 3 - 4
            # Y3
            elif personnage_y >= 100*2 and personnage_y <= 100*3:
                interface_y = 100 * 2
                if personnage_x > WIDTH * 0 and personnage_x <= WIDTH * 1:
                    pyxel.camera(WIDTH * 0, 100*2)
                    interface_x = WIDTH * 0
                elif personnage_x > WIDTH * 1 - 4 and personnage_x <= WIDTH * 2 - 4:
                    pyxel.camera(WIDTH * 1 - 4, 100*2)
                    interface_x = WIDTH * 1 - 4
                elif personnage_x > WIDTH * 2 - 4 and personnage_x <= WIDTH * 3 - 4:
                    pyxel.camera(WIDTH * 2 - 4, 100*2)
                    interface_x = WIDTH * 2 - 4
                elif personnage_x > WIDTH * 3 and personnage_x <= WIDTH * 4 - 4:
                    pyxel.camera(WIDTH * 3 - 4, 100*2)
                    interface_x = WIDTH * 3 - 4
            # Y4
            elif personnage_y >= 100*3 and personnage_y <= 100*4:
                interface_y = 100 * 3
                if personnage_x > WIDTH * 0 and personnage_x <= WIDTH * 1:
                    pyxel.camera(WIDTH * 0, 100*3)
                    interface_x = WIDTH * 0
                elif personnage_x > WIDTH * 1 - 4 and personnage_x <= WIDTH * 2 - 4:
                    pyxel.camera(WIDTH * 1 - 4, 100*3)
                    interface_x = WIDTH * 1 - 4
                elif personnage_x > WIDTH * 2 - 4 and personnage_x <= WIDTH * 3 - 4:
                    pyxel.camera(WIDTH * 2 - 4, 100*3)
                    interface_x = WIDTH * 2 - 4
                elif personnage_x > WIDTH * 3 - 4 and personnage_x <= WIDTH * 4 - 4:
                    pyxel.camera(WIDTH * 3 - 4, 100*3)
                    interface_x = WIDTH * 3 - 4

            ##### MUNITIONS #####
            # Affiche chaque munitions si elle n'est pas récupérée
            if jeu_niveau == 1:
                if arme_munition1_statut == False: # Si la munition 1 n'est pas récupérée:
                    pyxel.blt(arme_munition1_defaut_x, arme_munition1_defaut_y, 0, arme_munition1_res_x, arme_munition1_res_y, arme_munition_size_x, arme_munition_size_y, 0) # Munition 1
                if arme_munition2_statut == False: # Si la munition 2 n'est pas récupérée:
                    pyxel.blt(arme_munition2_defaut_x, arme_munition2_defaut_y, 0, arme_munition2_res_x, arme_munition2_res_y, arme_munition_size_x, arme_munition_size_y, 0) # Munition 2
                if arme_munition3_statut == False: # Si la munition 3 n'est pas récupérée:
                    pyxel.blt(arme_munition3_defaut_x, arme_munition3_defaut_y, 0, arme_munition3_res_x, arme_munition3_res_y, arme_munition_size_x, arme_munition_size_y, 0) # Munition 3
                if arme_munition4_statut == False: # Si la munition 4 n'est pas récupérée:
                    pyxel.blt(arme_munition4_defaut_x, arme_munition4_defaut_y, 0, arme_munition4_res_x, arme_munition4_res_y, arme_munition_size_x, arme_munition_size_y, 0) # Munition 4            
            if jeu_niveau == 2:
                if arme_munition1_statut == False: # Si la munition 1 n'est pas récupérée:
                    pyxel.blt(arme_munition1_defaut_x, arme_munition1_defaut_y, 0, arme_munition1_res_x, arme_munition1_res_y, arme_munition_size_x, arme_munition_size_y, 0) # Munition 1
                if arme_munition2_statut == False: # Si la munition 2 n'est pas récupérée:
                    pyxel.blt(arme_munition2_defaut_x, arme_munition2_defaut_y, 0, arme_munition2_res_x, arme_munition2_res_y, arme_munition_size_x, arme_munition_size_y, 0) # Munition 2
                if arme_munition3_statut == False: # Si la munition 3 n'est pas récupérée:
                    pyxel.blt(arme_munition3_defaut_x, arme_munition3_defaut_y, 0, arme_munition3_res_x, arme_munition3_res_y, arme_munition_size_x, arme_munition_size_y, 0) # Munition 3           
            if jeu_niveau == 3:
                if arme_munition1_statut == False: # Si la munition 1 n'est pas récupérée:
                    pyxel.blt(arme_munition1_defaut_x, arme_munition1_defaut_y, 0, arme_munition1_res_x, arme_munition1_res_y, arme_munition_size_x, arme_munition_size_y, 0) # Munition 1
                if arme_munition2_statut == False: # Si la munition 2 n'est pas récupérée:
                    pyxel.blt(arme_munition2_defaut_x, arme_munition2_defaut_y, 0, arme_munition2_res_x, arme_munition2_res_y, arme_munition_size_x, arme_munition_size_y, 0) # Munition 2

            ##### PORTES #####
            # Affiche chaque porte si elle n'est pas ouverte
            if porte0_statut == False: # Si la porte 0 est fermée:
                pyxel.blt(porte0_defaut_x, porte0_defaut_y, 0, porte0_res_x, porte0_res_y, porte0_size_x, porte0_size_y, 0) # Porte 0
            if porte1_statut == False: # Si la porte 1 est fermée:
                pyxel.blt(porte1_defaut_x, porte1_defaut_y, 0, porte1_res_x, porte1_res_y, porte1_size_x, porte1_size_y, 0) # Porte 1
            if porte2_statut == False: # Si la porte 2 est fermée:
                pyxel.blt(porte2_defaut_x, porte2_defaut_y, 0, porte2_res_x, porte2_res_y, porte2_size_x, porte2_size_y, 0) # Porte 2
            if porte3_statut == False: # Si la porte 3 est fermée:
                pyxel.blt(porte3_defaut_x, porte3_defaut_y, 0, porte3_res_x, porte3_res_y, porte3_size_x, porte3_size_y, 0) # Porte 3
            if porte4_statut == False: # Si la porte 4 est fermée:
                pyxel.blt(porte4_defaut_x, porte4_defaut_y, 0, porte4_res_x, porte4_res_y, porte4_size_x, porte4_size_y, 0) # Porte 4
            if porte5_statut == False: # Si la porte 5 est fermée:
                pyxel.blt(porte5_defaut_x, porte5_defaut_y, 0, porte5_res_x, porte5_res_y, porte5_size_x, porte5_size_y, 0) # Porte 5
            if porte6_statut == False: # Si la porte 6 est fermée:
                pyxel.blt(porte6_defaut_x, porte6_defaut_y, 0, porte6_res_x, porte6_res_y, porte6_size_x, porte6_size_y, 0) # Porte 6

            # Change les valeurs des emplacements inventaire en fonction de la camera
            slot_y = slot_y + interface_y
            slot1_x = slot1_x + interface_x
            slot2_x = slot2_x + interface_x
            slot3_x = slot3_x + interface_x
            slot4_x = slot4_x + interface_x
            arme_slot_x = arme_slot_x + interface_x
            arme_slot_y = arme_slot_y + interface_y
            # Dessine un carré noir en bas (le carré noir laisse visible les choses importantes comme voisin, clefs, ...)
            pyxel.rect(0, interface_y + 105, 512, 512, 7)
            pyxel.rect(0, interface_y + 106, 512, 512, 0)
            
            ##### INVENTAIRE #####
            # Affiche la barre d'objet du joueur
            pyxel.text(interface_x + 2, interface_y + 108, "INVENTAIRE:", 7)
            pyxel.blt(interface_x + 2, interface_y + 115, 0, 0, 0, 41, 11, 0)
            if inventaire_objet_selectionne == 1: # Si l'objet sélectionné est le 1 :
                inventaire_objet_selectionne_x = 1
                inventaire_objet_selectionne_y = 114
            elif inventaire_objet_selectionne == 2: # Si l'objet sélectionné est le 2 :
                inventaire_objet_selectionne_x = 11
                inventaire_objet_selectionne_y = 114
            elif inventaire_objet_selectionne == 3: # Si l'objet sélectionné est le 3 :
                inventaire_objet_selectionne_x = 21
                inventaire_objet_selectionne_y = 114
            elif inventaire_objet_selectionne == 4: # Si l'objet sélectionné est le 4 :
                inventaire_objet_selectionne_x = 31
                inventaire_objet_selectionne_y = 114
            if inventaire_objet_selectionne > 0 and inventaire_objet_selectionne < 5:
                pyxel.blt(interface_x + inventaire_objet_selectionne_x, interface_y + inventaire_objet_selectionne_y, 0, 40, 0, 13, 13, 2)

            ##### ENDURANCE #####
            # Affiche la barre d'endurance du joueur
            pyxel.text(interface_x + 86, interface_y + 108, "ENDURANCE:", 7)
            pyxel.rectb(interface_x + 83, interface_y + 115, 43, 11, 7)
            pyxel.rect(interface_x + 84, interface_y + 116, personnage_endurance / 2.5 + 1, 9, 10)
            if endurance_pleine_statut == True:
                pyxel.rectb(interface_x + 82, interface_y + 114, 45, 13, 8)
            if endurance_inprogress_statut == True:
                pyxel.rectb(interface_x + 82, interface_y + 114, 45, 13, 5)
            if endurance_faible_statut == True:
                pyxel.rectb(interface_x + 82, interface_y + 114, 45, 13, 14)

            ##### ARME #####
            # Affichage de l'interface de l'arme
            if arme_statut == True: # Si l'arme est récupérée:

                # Initialise les variables par défaut de la munition qui sera tirée et affichée
                arme_munition_res_selectionne_x = arme_munition1_res_x
                arme_munition_res_selectionne_y = arme_munition1_res_y

                # Change la munition si elle est utilisée
                if arme_tir_statut == True:
                    
                    # Change la forme/couleur de la munition que le joueur va tirer
                    if arme_munition_count == 2:
                        arme_munition_res_selectionne_x = arme_munition2_res_x
                        arme_munition_res_selectionne_y = arme_munition2_res_y
                    elif arme_munition_count == 3:
                        arme_munition_res_selectionne_x = arme_munition3_res_x
                        arme_munition_res_selectionne_y = arme_munition3_res_y
                    elif arme_munition_count == 4:
                        arme_munition_res_selectionne_x = arme_munition4_res_x
                        arme_munition_res_selectionne_y = arme_munition4_res_y
                    else:
                        arme_munition_res_selectionne_x = arme_munition1_res_x
                        arme_munition_res_selectionne_y = arme_munition1_res_y

                # Interface de l'arme
                pyxel.rectb(interface_x + 46, interface_y + 115, 34, 11, 7)
                # Munitions
                pyxel.text(interface_x + 69, interface_y + 118, str(arme_munition), 7)
                pyxel.blt(interface_x + inventaire_munition_slot_x, interface_y + inventaire_munition_slot_y, 0, arme_munition_res_selectionne_x, arme_munition_res_selectionne_y, arme_munition_size_x, arme_munition_size_y, 0)
                # Chronomètre
                if arme_cooldown >= 450:
                    pyxel.blt(interface_x + 48, interface_y + 117, 0, 48, 16, 7, 7, 0)
                elif arme_cooldown >= 337.5:
                    pyxel.blt(interface_x + 48, interface_y + 117, 0, 56, 16, 7, 7, 0)
                elif arme_cooldown >= 225:
                    pyxel.blt(interface_x + 48, interface_y + 117, 0, 64, 16, 7, 7, 0)
                elif arme_cooldown >= 112.5:
                    pyxel.blt(interface_x + 48, interface_y + 117, 0, 72, 16, 7, 7, 0) 
                elif arme_cooldown >= 0:
                    pyxel.blt(interface_x + 48, interface_y + 117, 0, 80, 16, 7, 7, 0)
                    if arme_munition != 0 and arme_cooldown == 0:
                        pyxel.rectb(interface_x + 45, interface_y + 114, 36, 13, 9)

            ##### AFFICHAGE PAR DIRECTION #####
            if personnage_direction == 1:

                ##### CLEFS #####
                # Initialise de combien les objets doivent être décalés dans cette direction
                x = 8
                y = -1
                # Si une clef est récupérée et sélectionnée elle s'affiche dans la main du personnage sinon elle est à sa position initiale, et si elle est utilisée elle ne s'affiche plus
                # Clef 0
                if clef0_statut == True and clef0_utilise == False: # Si la clef est récupérée et qu'elle n'est pas utilisée
                    if inventaire_objet_selectionne == 4: # Si le joueur sélectionne l'inventaire à l'emplacement 4:
                        pyxel.blt(personnage_x + x, personnage_y + y, 0, clef0_res_x, clef0_res_y, clef0_size_x, clef0_size_y, 0) # Clef 0 affichée dans la main du joueur
                    else:
                        pyxel.blt(1 + slot4_x, slot_y, 0, clef0_res_x, clef0_res_y, clef0_size_x, clef0_size_y, 0) # Clef 0 affichée dans l'inventaire du joueur
                elif clef0_statut == False: # Si la clef n'est pas récupérée:
                    pyxel.blt(clef0_defaut_x, clef0_defaut_y, 0, clef0_res_x, clef0_res_y, clef0_size_x, clef0_size_y, 0) # Clef 0 affichée à son emplacement par défaut

                # Clef 1
                if clef1_statut == True and clef1_utilise == False: # Si la clef est récupérée et qu'elle n'est pas utilisée
                    if inventaire_objet_selectionne == 1: # Si le joueur sélectionne l'inventaire à l'emplacement 1:
                        pyxel.blt(personnage_x + x, personnage_y + y, 0, clef1_res_x, clef1_res_y, -clef1_size_x, -clef1_size_y, 0) # Clef 1 affichée dans la main du joueur
                    else:
                        pyxel.blt(2 + slot1_x, slot_y, 0, clef1_res_x, clef1_res_y, clef1_size_x, clef1_size_y, 0) # Clef 1 affichée dans l'inventaire du joueur
                elif clef1_statut == False: # Si la clef n'est pas récupérée:
                    pyxel.blt(clef1_defaut_x, clef1_defaut_y, 0, clef1_res_x, clef1_res_y, clef1_size_x, clef1_size_y, 0) # Clef 1 affichée à son emplacement par défaut
                
                # Clef 2
                if clef2_statut == True and clef2_utilise == False: # Si la clef est récupérée et qu'elle n'est pas utilisée
                    if inventaire_objet_selectionne == 2: # Si le joueur sélectionne l'inventaire à l'emplacement 2:
                        pyxel.blt(personnage_x + x, personnage_y + y, 0, clef2_res_x, clef2_res_y, -clef2_size_x, -clef2_size_y, 0) # Clef 2 affichée dans la main du joueur
                    else:
                        pyxel.blt(2 + slot2_x, slot_y, 0, clef2_res_x, clef2_res_y, clef2_size_x, clef2_size_y, 0) # Clef 2 affichée dans l'inventaire du joueur
                elif clef2_statut == False: # Si la clef n'est pas récupérée:
                    pyxel.blt(clef2_defaut_x, clef2_defaut_y, 0, clef2_res_x, clef2_res_y, clef2_size_x, clef2_size_y, 0) # Clef 2 affichée à son emplacement par défaut

                # Clef 3
                if clef3_statut == True and clef3_utilise == False: # Si la clef est récupérée et qu'elle n'est pas utilisée
                    if inventaire_objet_selectionne == 3: # Si le joueur sélectionne l'inventaire à l'emplacement 3:
                        pyxel.blt(personnage_x + x, personnage_y + y, 0, clef3_res_x, clef3_res_y, -clef3_size_x, -clef3_size_y, 0) # Clef 3 affichée dans la main du joueur
                    else:
                        pyxel.blt(2 + slot3_x, slot_y, 0, clef3_res_x, clef3_res_y, clef3_size_x, clef3_size_y, 0) # Clef 3 affichée dans l'inventaire du joueur
                elif clef3_statut == False: # Si la clef n'est pas récupérée:
                    pyxel.blt(clef3_defaut_x, clef3_defaut_y, 0, clef3_res_x, clef3_res_y, clef3_size_x, clef3_size_y, 0) # Clef 3 affichée à son emplacement par défaut

                # Clef 4
                if clef4_statut == True and clef4_utilise == False: # Si la clef est récupérée et qu'elle n'est pas utilisée
                    if inventaire_objet_selectionne == 1: # Si le joueur sélectionne l'inventaire à l'emplacement 1:
                        pyxel.blt(personnage_x + x, personnage_y + y, 0, clef4_res_x, clef4_res_y, -clef4_size_x, -clef4_size_y, 0) # Clef 4 affichée dans la main du joueur
                    else:
                        pyxel.blt(2 + slot1_x, slot_y, 0, clef4_res_x, clef4_res_y, clef4_size_x, clef4_size_y, 0) # Clef 4 affichée dans l'inventaire du joueur
                elif clef4_statut == False: # Si la clef n'est pas récupérée:
                    pyxel.blt(clef4_defaut_x, clef4_defaut_y, 0, clef4_res_x, clef4_res_y, clef4_size_x, clef4_size_y, 0) # Clef 4 affichée à son emplacement par défaut

                # Clef 5
                if clef5_statut == True and clef5_utilise == False: # Si la clef est récupérée et qu'elle n'est pas utilisée
                    if inventaire_objet_selectionne == 2: # Si le joueur sélectionne l'inventaire à l'emplacement 2:
                        pyxel.blt(personnage_x + x, personnage_y + y, 0, clef5_res_x, clef5_res_y, clef5_size_x, clef5_size_y, 0) # Clef 5 affichée dans la main du joueur
                    else:
                        pyxel.blt(slot2_x, slot_y, 0, clef5_res_x, clef5_res_y, clef5_size_x, clef5_size_y, 0) # Clef 5 affichée dans l'inventaire du joueur
                elif clef5_statut == False: # Si la clef n'est pas récupérée:
                    pyxel.blt(clef5_defaut_x, clef5_defaut_y, 0, clef5_res_x, clef5_res_y, -clef5_size_x, -clef5_size_y, 0) # Clef 5 affichée à son emplacement par défaut

                # Clef 6
                if clef6_statut == True and clef6_utilise == False: # Si la clef est récupérée et qu'elle n'est pas utilisée
                    if inventaire_objet_selectionne == 3: # Si le joueur sélectionne l'inventaire à l'emplacement 3:
                        pyxel.blt(personnage_x + x, personnage_y + y, 0, clef6_res_x, clef6_res_y, -clef6_size_x, clef6_size_y, 0) # Clef 6 affichée dans la main du joueur
                    else:
                        pyxel.blt(1 + slot3_x, slot_y, 0, clef6_res_x, clef6_res_y, clef6_size_x, clef6_size_y, 0) # Clef 6 affichée dans l'inventaire du joueur
                elif clef6_statut == False: # Si la clef n'est pas récupérée:
                    pyxel.blt(clef6_defaut_x, clef6_defaut_y, 0, clef6_res_x, clef6_res_y, clef6_size_x, clef6_size_y, 0) # Clef 6 affichée à son emplacement par défaut

                ##### ARME #####
                if arme_statut == False: # Si l'arme n'est pas récupérée:
                    pyxel.blt(arme_defaut_x, arme_defaut_y, 0, arme_res_x, arme_res_y, arme_size_x, arme_size_y, 0) # Affiche l'arme à son emplacement initial
                else:
                    if inventaire_objet_selectionne == 5: # Si l'arme est sélectionnée
                        pyxel.blt(personnage_x + x, personnage_y + y, 0, arme_res_x, arme_res_y, arme_size_x, arme_size_y, 0) # Affiche l'arme dans la main du personnage
                    else:
                        pyxel.blt(arme_slot_x, arme_slot_y, 0, arme_res_x, arme_res_y, arme_size_x, arme_size_y, 0) # Affiche l'arme dans la main du personnage
                    ##### ARME -> TIR #####
                    if arme_tir_statut == True:
                        # Tire la munition
                        pyxel.blt(arme_tir_x, arme_tir_y, 0, arme_munition_res_selectionne_x, arme_munition_res_selectionne_y, arme_munition_size_x, arme_munition_size_y, 0)

                ##### PERSONNAGE #####
                pyxel.blt(personnage_x, personnage_y, 0, personnage_selectionne1_res_x, personnage_selectionne1_res_y, personnage_size_x, personnage_size_y, 7)

            elif personnage_direction == 2:
                
                ##### CLEFS #####
                # Initialise de combien les objets doivent être décalés dans cette direction
                x = 8
                y = 5
                # Si une clef est récupérée et sélectionnée elle s'affiche dans la main du personnage sinon elle est à sa position initiale, et si elle est utilisée elle ne s'affiche plus
                # Clef 0
                if clef0_statut == True and clef0_utilise == False: # Si la clef est récupérée et qu'elle n'est pas utilisée
                    if inventaire_objet_selectionne == 4: # Si le joueur sélectionne l'inventaire à l'emplacement 4:
                        pyxel.blt(personnage_x + x, personnage_y + y, 0, clef0_res_x, clef0_res_y, clef0_size_x, clef0_size_y, 0) # Clef 0 affichée dans la main du joueur
                    else:
                        pyxel.blt(1 + slot4_x, slot_y, 0, clef0_res_x, clef0_res_y, clef0_size_x, clef0_size_y, 0) # Clef 0 affichée dans l'inventaire du joueur
                elif clef0_statut == False: # Si la clef n'est pas récupérée:
                    pyxel.blt(clef0_defaut_x, clef0_defaut_y, 0, clef0_res_x, clef0_res_y, clef0_size_x, clef0_size_y, 0) # Clef 0 affichée à son emplacement par défaut
                
                # Clef 1
                if clef1_statut == True and clef1_utilise == False: # Si la clef est récupérée et qu'elle n'est pas utilisée
                    if inventaire_objet_selectionne == 1: # Si le joueur sélectionne l'inventaire à l'emplacement 1:
                        pyxel.blt(personnage_x + x, personnage_y + y, 0, clef1_res_x, clef1_res_y, clef1_size_x, -clef1_size_y, 0) # Clef 1 affichée dans la main du joueur
                    else:
                        pyxel.blt(2 + slot1_x, slot_y, 0, clef1_res_x, clef1_res_y, clef1_size_x, clef1_size_y, 0) # Clef 1 affichée dans l'inventaire du joueur
                elif clef1_statut == False: # Si la clef n'est pas récupérée:
                    pyxel.blt(clef1_defaut_x, clef1_defaut_y, 0, clef1_res_x, clef1_res_y, clef1_size_x, clef1_size_y, 0) # Clef 1 affichée à son emplacement par défaut
                
                # Clef 2
                if clef2_statut == True and clef2_utilise == False: # Si la clef est récupérée et qu'elle n'est pas utilisée
                    if inventaire_objet_selectionne == 2: # Si le joueur sélectionne l'inventaire à l'emplacement 2:
                        pyxel.blt(personnage_x + x, personnage_y + y, 0, clef2_res_x, clef2_res_y, clef2_size_x, -clef2_size_y, 0) # Clef 2 affichée dans la main du joueur
                    else:
                        pyxel.blt(2 + slot2_x, slot_y, 0, clef2_res_x, clef2_res_y, clef2_size_x, clef2_size_y, 0) # Clef 2 affichée dans l'inventaire du joueur
                elif clef2_statut == False: # Si la clef n'est pas récupérée:
                    pyxel.blt(clef2_defaut_x, clef2_defaut_y, 0, clef2_res_x, clef2_res_y, clef2_size_x, clef2_size_y, 0) # Clef 2 affichée à son emplacement par défaut

                # Clef 3
                if clef3_statut == True and clef3_utilise == False: # Si la clef est récupérée et qu'elle n'est pas utilisée
                    if inventaire_objet_selectionne == 3: # Si le joueur sélectionne l'inventaire à l'emplacement 3:
                        pyxel.blt(personnage_x + x, personnage_y + y, 0, clef3_res_x, clef3_res_y, clef3_size_x, clef3_size_y, 0) # Clef 3 affichée dans la main du joueur
                    else:
                        pyxel.blt(2 + slot3_x, slot_y, 0, clef3_res_x, clef3_res_y, clef3_size_x, clef3_size_y, 0) # Clef 3 affichée dans l'inventaire du joueur
                elif clef3_statut == False: # Si la clef n'est pas récupérée:
                    pyxel.blt(clef3_defaut_x, clef3_defaut_y, 0, clef3_res_x, clef3_res_y, clef3_size_x, clef3_size_y, 0) # Clef 3 affichée à son emplacement par défaut

                # Clef 4
                if clef4_statut == True and clef4_utilise == False: # Si la clef est récupérée et qu'elle n'est pas utilisée
                    if inventaire_objet_selectionne == 1: # Si le joueur sélectionne l'inventaire à l'emplacement 1:
                        pyxel.blt(personnage_x + x, personnage_y + y, 0, clef4_res_x, clef4_res_y, clef4_size_x, -clef4_size_y, 0) # Clef 4 affichée dans la main du joueur
                    else:
                        pyxel.blt(2 + slot1_x, slot_y, 0, clef4_res_x, clef4_res_y, clef4_size_x, clef4_size_y, 0) # Clef 4 affichée dans l'inventaire du joueur
                elif clef4_statut == False: # Si la clef n'est pas récupérée:
                    pyxel.blt(clef4_defaut_x, clef4_defaut_y, 0, clef4_res_x, clef4_res_y, clef4_size_x, clef4_size_y, 0) # Clef 4 affichée à son emplacement par défaut

                # Clef 5
                if clef5_statut == True and clef5_utilise == False: # Si la clef est récupérée et qu'elle n'est pas utilisée
                    if inventaire_objet_selectionne == 2: # Si le joueur sélectionne l'inventaire à l'emplacement 2:
                        pyxel.blt(personnage_x + x, personnage_y + y, 0, clef5_res_x, clef5_res_y, clef5_size_x, clef5_size_y, 0) # Clef 5 affichée dans la main du joueur
                    else:
                        pyxel.blt(slot2_x, slot_y, 0, clef5_res_x, clef5_res_y, clef5_size_x, clef5_size_y, 0) # Clef 5 affichée dans l'inventaire du joueur
                elif clef5_statut == False: # Si la clef n'est pas récupérée:
                    pyxel.blt(clef5_defaut_x, clef5_defaut_y, 0, clef5_res_x, clef5_res_y, -clef5_size_x, -clef5_size_y, 0) # Clef 5 affichée à son emplacement par défaut

                # Clef 6
                if clef6_statut == True and clef6_utilise == False: # Si la clef est récupérée et qu'elle n'est pas utilisée
                    if inventaire_objet_selectionne == 3: # Si le joueur sélectionne l'inventaire à l'emplacement 3:
                        pyxel.blt(personnage_x + x, personnage_y + y, 0, clef6_res_x, clef6_res_y, -clef6_size_x, clef6_size_y, 0) # Clef 6 affichée dans la main du joueur
                    else:
                        pyxel.blt(1 + slot3_x, slot_y, 0, clef6_res_x, clef6_res_y, clef6_size_x, clef6_size_y, 0) # Clef 6 affichée dans l'inventaire du joueur
                elif clef6_statut == False: # Si la clef n'est pas récupérée:
                    pyxel.blt(clef6_defaut_x, clef6_defaut_y, 0, clef6_res_x, clef6_res_y, clef6_size_x, clef6_size_y, 0) # Clef 6 affichée à son emplacement par défaut

                ##### ARME #####
                if arme_statut == False: # Si l'arme n'est pas récupérée:
                    pyxel.blt(arme_defaut_x, arme_defaut_y, 0, arme_res_x, arme_res_y, arme_size_x, arme_size_y, 0) # Affiche l'arme à son emplacement initial
                else:
                    if inventaire_objet_selectionne == 5: # Si l'arme est sélectionnée
                        pyxel.blt(personnage_x + x, personnage_y + y, 0, arme_res_x, arme_res_y, arme_size_x, arme_size_y, 0) # Affiche l'arme dans la main du personnage
                    else:
                        pyxel.blt(arme_slot_x, arme_slot_y, 0, arme_res_x, arme_res_y, arme_size_x, arme_size_y, 0) # Affiche l'arme dans la main du personnage
                    ##### ARME -> TIR #####
                    if arme_tir_statut == True:
                        # Tire la munition
                        pyxel.blt(arme_tir_x, arme_tir_y, 0, arme_munition_res_selectionne_x, arme_munition_res_selectionne_y, arme_munition_size_x, arme_munition_size_y, 0)

                ##### PERSONNAGE #####
                pyxel.blt(personnage_x, personnage_y, 0, personnage_selectionne2_res_x, personnage_selectionne2_res_y, personnage_size_x, personnage_size_y, 7)

            elif personnage_direction == 3:
                
                ##### CLEFS #####
                # Initialise de combien les objets doivent être décalés dans cette direction
                x = 0
                y = 7
                # Si une clef est récupérée et sélectionnée elle s'affiche dans la main du personnage sinon elle est à sa position initiale, et si elle est utilisée elle ne s'affiche plus
                # Clef 0
                if clef0_statut == True and clef0_utilise == False: # Si la clef est récupérée et qu'elle n'est pas utilisée
                    if inventaire_objet_selectionne == 4: # Si le joueur sélectionne l'inventaire à l'emplacement 4:
                        pyxel.blt(personnage_x + x, personnage_y + y, 0, clef0_res_x, clef0_res_y, -clef0_size_x, -clef0_size_y, 0) # Clef 0 affichée dans la main du joueur
                    else:
                        pyxel.blt(1 + slot4_x, slot_y, 0, clef0_res_x, clef0_res_y, clef0_size_x, clef0_size_y, 0) # Clef 0 affichée dans l'inventaire du joueur
                elif clef0_statut == False: # Si la clef n'est pas récupérée:
                    pyxel.blt(clef0_defaut_x, clef0_defaut_y, 0, clef0_res_x, clef0_res_y, clef0_size_x, clef0_size_y, 0) # Clef 0 affichée à son emplacement par défaut

                # Clef 1
                if clef1_statut == True and clef1_utilise == False: # Si la clef est récupérée et qu'elle n'est pas utilisée
                    if inventaire_objet_selectionne == 1: # Si le joueur sélectionne l'inventaire à l'emplacement 1:
                        pyxel.blt(personnage_x + x, personnage_y + y, 0, clef1_res_x, clef1_res_y, clef1_size_x, clef1_size_y, 0) # Clef 1 affichée dans la main du joueur
                    else:
                        pyxel.blt(2 + slot1_x, slot_y, 0, clef1_res_x, clef1_res_y, clef1_size_x, clef1_size_y, 0) # Clef 1 affichée dans l'inventaire du joueur
                elif clef1_statut == False: # Si la clef n'est pas récupérée:
                    pyxel.blt(clef1_defaut_x, clef1_defaut_y, 0, clef1_res_x, clef1_res_y, clef1_size_x, clef1_size_y, 0) # Clef 1 affichée à son emplacement par défaut
                
                # Clef 2
                if clef2_statut == True and clef2_utilise == False: # Si la clef est récupérée et qu'elle n'est pas utilisée
                    if inventaire_objet_selectionne == 2: # Si le joueur sélectionne l'inventaire à l'emplacement 2:
                        pyxel.blt(personnage_x + x, personnage_y + y, 0, clef2_res_x, clef2_res_y, clef2_size_x, clef2_size_y, 0) # Clef 2 affichée dans la main du joueur
                    else:
                        pyxel.blt(2 + slot2_x, slot_y, 0, clef2_res_x, clef2_res_y, clef2_size_x, clef2_size_y, 0) # Clef 2 affichée dans l'inventaire du joueur
                elif clef2_statut == False: # Si la clef n'est pas récupérée:
                    pyxel.blt(clef2_defaut_x, clef2_defaut_y, 0, clef2_res_x, clef2_res_y, clef2_size_x, clef2_size_y, 0) # Clef 2 affichée à son emplacement par défaut

                # Clef 3
                if clef3_statut == True and clef3_utilise == False: # Si la clef est récupérée et qu'elle n'est pas utilisée
                    if inventaire_objet_selectionne == 3: # Si le joueur sélectionne l'inventaire à l'emplacement 3:
                        pyxel.blt(personnage_x + x, personnage_y + y, 0, clef3_res_x, clef3_res_y, clef3_size_x, clef3_size_y, 0) # Clef 3 affichée dans la main du joueur
                    else:
                        pyxel.blt(2 + slot3_x, slot_y, 0, clef3_res_x, clef3_res_y, clef3_size_x, clef3_size_y, 0) # Clef 3 affichée dans l'inventaire du joueur
                elif clef3_statut == False: # Si la clef n'est pas récupérée:
                    pyxel.blt(clef3_defaut_x, clef3_defaut_y, 0, clef3_res_x, clef3_res_y, clef3_size_x, clef3_size_y, 0) # Clef 3 affichée à son emplacement par défaut

                # Clef 4
                if clef4_statut == True and clef4_utilise == False: # Si la clef est récupérée et qu'elle n'est pas utilisée
                    if inventaire_objet_selectionne == 1: # Si le joueur sélectionne l'inventaire à l'emplacement 1:
                        pyxel.blt(personnage_x + x, personnage_y + y, 0, clef4_res_x, clef4_res_y, clef4_size_x, clef4_size_y, 0) # Clef 4 affichée dans la main du joueur
                    else:
                        pyxel.blt(2 + slot1_x, slot_y, 0, clef4_res_x, clef4_res_y, clef4_size_x, clef4_size_y, 0) # Clef 4 affichée dans l'inventaire du joueur
                elif clef4_statut == False: # Si la clef n'est pas récupérée:
                    pyxel.blt(clef4_defaut_x, clef4_defaut_y, 0, clef4_res_x, clef4_res_y, clef4_size_x, clef4_size_y, 0) # Clef 4 affichée à son emplacement par défaut

                # Clef 5
                if clef5_statut == True and clef5_utilise == False: # Si la clef est récupérée et qu'elle n'est pas utilisée
                    if inventaire_objet_selectionne == 2: # Si le joueur sélectionne l'inventaire à l'emplacement 2:
                        pyxel.blt(personnage_x + x, personnage_y + y, 0, clef5_res_x, clef5_res_y, -clef5_size_x, -clef5_size_y, 0) # Clef 5 affichée dans la main du joueur
                    else:
                        pyxel.blt(slot2_x, slot_y, 0, clef5_res_x, clef5_res_y, clef5_size_x, clef5_size_y, 0) # Clef 5 affichée dans l'inventaire du joueur
                elif clef5_statut == False: # Si la clef n'est pas récupérée:
                    pyxel.blt(clef5_defaut_x, clef5_defaut_y, 0, clef5_res_x, clef5_res_y, -clef5_size_x, -clef5_size_y, 0) # Clef 5 affichée à son emplacement par défaut

                # Clef 6
                if clef6_statut == True and clef6_utilise == False: # Si la clef est récupérée et qu'elle n'est pas utilisée
                    if inventaire_objet_selectionne == 3: # Si le joueur sélectionne l'inventaire à l'emplacement 3:
                        pyxel.blt(personnage_x + x, personnage_y + y, 0, clef6_res_x, clef6_res_y, -clef6_size_x, -clef6_size_y, 0) # Clef 6 affichée dans la main du joueur
                    else:
                        pyxel.blt(1 + slot3_x, slot_y, 0, clef6_res_x, clef6_res_y, clef6_size_x, clef6_size_y, 0) # Clef 6 affichée dans l'inventaire du joueur
                elif clef6_statut == False: # Si la clef n'est pas récupérée:
                    pyxel.blt(clef6_defaut_x, clef6_defaut_y, 0, clef6_res_x, clef6_res_y, clef6_size_x, clef6_size_y, 0) # Clef 6 affichée à son emplacement par défaut

                ##### ARME #####
                if arme_statut == False: # Si l'arme n'est pas récupérée:
                    pyxel.blt(arme_defaut_x, arme_defaut_y, 0, arme_res_x, arme_res_y, arme_size_x, arme_size_y, 0) # Affiche l'arme à son emplacement initial
                else:
                    if inventaire_objet_selectionne == 5: # Si l'arme est sélectionnée
                        pyxel.blt(personnage_x + x, personnage_y + y, 0, arme_res_x, arme_res_y, -arme_size_x, -arme_size_y, 0) # Affiche l'arme dans la main du personnage
                    else:
                        pyxel.blt(arme_slot_x, arme_slot_y, 0, arme_res_x, arme_res_y, arme_size_x, arme_size_y, 0) # Affiche l'arme dans la main du personnage
                    ##### ARME -> TIR #####
                    if arme_tir_statut == True:
                        # Tire la munition
                        pyxel.blt(arme_tir_x, arme_tir_y, 0, arme_munition_res_selectionne_x, arme_munition_res_selectionne_y, arme_munition_size_x, arme_munition_size_y, 0)

                ##### PERSONNAGE #####
                pyxel.blt(personnage_x, personnage_y, 0, personnage_selectionne1_res_x, personnage_selectionne1_res_y, -personnage_size_x, -personnage_size_y, 7)

            elif personnage_direction == 4:

                ##### CLEFS #####
                # Initialise de combien les objets doivent être décalés dans cette direction
                x = 0
                y = 8
                # Si une clef est récupérée et sélectionnée elle s'affiche dans la main du personnage sinon elle est à sa position initiale, et si elle est utilisée elle ne s'affiche plus
                # Clef 0
                if clef0_statut == True and clef0_utilise == False: # Si la clef est récupérée et qu'elle n'est pas utilisée
                    if inventaire_objet_selectionne == 4: # Si le joueur sélectionne l'inventaire à l'emplacement 4:
                        pyxel.blt(personnage_x + x, personnage_y + y, 0, clef0_res_x, clef0_res_y, -clef0_size_x, -clef0_size_y, 0) # Clef 0 affichée dans la main du joueur
                    else:
                        pyxel.blt(1 + slot4_x, slot_y, 0, clef0_res_x, clef0_res_y, clef0_size_x, clef0_size_y, 0) # Clef 0 affichée dans l'inventaire du joueur
                elif clef0_statut == False: # Si la clef n'est pas récupérée:
                    pyxel.blt(clef0_defaut_x, clef0_defaut_y, 0, clef0_res_x, clef0_res_y, clef0_size_x, clef0_size_y, 0) # Clef 0 affichée à son emplacement par défaut
                
                # Clef 1
                if clef1_statut == True and clef1_utilise == False: # Si la clef est récupérée et qu'elle n'est pas utilisée
                    if inventaire_objet_selectionne == 1: # Si le joueur sélectionne l'inventaire à l'emplacement 1:
                        pyxel.blt(personnage_x + x, personnage_y + y, 0, clef1_res_x, clef1_res_y, clef1_size_x, clef1_size_y, 0) # Clef 1 affichée dans la main du joueur
                    else:
                        pyxel.blt(2 + slot1_x, slot_y, 0, clef1_res_x, clef1_res_y, clef1_size_x, clef1_size_y, 0) # Clef 1 affichée dans l'inventaire du joueur
                elif clef1_statut == False: # Si la clef n'est pas récupérée:
                    pyxel.blt(clef1_defaut_x, clef1_defaut_y, 0, clef1_res_x, clef1_res_y, clef1_size_x, clef1_size_y, 0) # Clef 1 affichée à son emplacement par défaut
                
                # Clef 2
                if clef2_statut == True and clef2_utilise == False: # Si la clef est récupérée et qu'elle n'est pas utilisée
                    if inventaire_objet_selectionne == 2: # Si le joueur sélectionne l'inventaire à l'emplacement 2:
                        pyxel.blt(personnage_x + x, personnage_y + y, 0, clef2_res_x, clef2_res_y, clef2_size_x, clef2_size_y, 0) # Clef 2 affichée dans la main du joueur
                    else:
                        pyxel.blt(2 + slot2_x, slot_y, 0, clef2_res_x, clef2_res_y, clef2_size_x, clef2_size_y, 0) # Clef 2 affichée dans l'inventaire du joueur
                elif clef2_statut == False: # Si la clef n'est pas récupérée:
                    pyxel.blt(clef2_defaut_x, clef2_defaut_y, 0, clef2_res_x, clef2_res_y, clef2_size_x, clef2_size_y, 0) # Clef 2 affichée à son emplacement par défaut

                # Clef 3
                if clef3_statut == True and clef3_utilise == False: # Si la clef est récupérée et qu'elle n'est pas utilisée
                    if inventaire_objet_selectionne == 3: # Si le joueur sélectionne l'inventaire à l'emplacement 3:
                        pyxel.blt(personnage_x + x, personnage_y + y, 0, clef3_res_x, clef3_res_y, clef3_size_x, clef3_size_y, 0) # Clef 3 affichée dans la main du joueur
                    else:
                        pyxel.blt(2 + slot3_x, slot_y, 0, clef3_res_x, clef3_res_y, clef3_size_x, clef3_size_y, 0) # Clef 3 affichée dans l'inventaire du joueur
                elif clef3_statut == False: # Si la clef n'est pas récupérée:
                    pyxel.blt(clef3_defaut_x, clef3_defaut_y, 0, clef3_res_x, clef3_res_y, clef3_size_x, clef3_size_y, 0) # Clef 3 affichée à son emplacement par défaut

                # Clef 4
                if clef4_statut == True and clef4_utilise == False: # Si la clef est récupérée et qu'elle n'est pas utilisée
                    if inventaire_objet_selectionne == 1: # Si le joueur sélectionne l'inventaire à l'emplacement 1:
                        pyxel.blt(personnage_x + x, personnage_y + y, 0, clef4_res_x, clef4_res_y, clef4_size_x, clef4_size_y, 0) # Clef 4 affichée dans la main du joueur
                    else:
                        pyxel.blt(2 + slot1_x, slot_y, 0, clef4_res_x, clef4_res_y, clef4_size_x, clef4_size_y, 0) # Clef 4 affichée dans l'inventaire du joueur
                elif clef4_statut == False: # Si la clef n'est pas récupérée:
                    pyxel.blt(clef4_defaut_x, clef4_defaut_y, 0, clef4_res_x, clef4_res_y, clef4_size_x, clef4_size_y, 0) # Clef 4 affichée à son emplacement par défaut

                # Clef 5
                if clef5_statut == True and clef5_utilise == False: # Si la clef est récupérée et qu'elle n'est pas utilisée
                    if inventaire_objet_selectionne == 2: # Si le joueur sélectionne l'inventaire à l'emplacement 2:
                        pyxel.blt(personnage_x + x, personnage_y + y, 0, clef5_res_x, clef5_res_y, clef5_size_x, -clef5_size_y, 0) # Clef 5 affichée dans la main du joueur
                    else:
                        pyxel.blt(slot2_x, slot_y, 0, clef5_res_x, clef5_res_y, clef5_size_x, clef5_size_y, 0) # Clef 5 affichée dans l'inventaire du joueur
                elif clef5_statut == False: # Si la clef n'est pas récupérée:
                    pyxel.blt(clef5_defaut_x, clef5_defaut_y, 0, clef5_res_x, clef5_res_y, -clef5_size_x, -clef5_size_y, 0) # Clef 5 affichée à son emplacement par défaut

                # Clef 6
                if clef6_statut == True and clef6_utilise == False: # Si la clef est récupérée et qu'elle n'est pas utilisée
                    if inventaire_objet_selectionne == 3: # Si le joueur sélectionne l'inventaire à l'emplacement 3:
                        pyxel.blt(personnage_x + x, personnage_y + y, 0, clef6_res_x, clef6_res_y, -clef6_size_x, -clef6_size_y, 0) # Clef 6 affichée dans la main du joueur
                    else:
                        pyxel.blt(1 + slot3_x, slot_y, 0, clef6_res_x, clef6_res_y, clef6_size_x, clef6_size_y, 0) # Clef 6 affichée dans l'inventaire du joueur
                elif clef6_statut == False: # Si la clef n'est pas récupérée:
                    pyxel.blt(clef6_defaut_x, clef6_defaut_y, 0, clef6_res_x, clef6_res_y, clef6_size_x, clef6_size_y, 0) # Clef 6 affichée à son emplacement par défaut

                ##### ARME #####
                if arme_statut == False: # Si l'arme n'est pas récupérée:
                    pyxel.blt(arme_defaut_x, arme_defaut_y, 0, arme_res_x, arme_res_y, arme_size_x, arme_size_y, 0) # Affiche l'arme à son emplacement initial
                else:
                    if inventaire_objet_selectionne == 5: # Si l'arme est sélectionnée
                        pyxel.blt(personnage_x + x, personnage_y + y, 0, arme_res_x, arme_res_y, -arme_size_x, arme_size_y, 0) # Affiche l'arme dans la main du personnage
                    else:
                        pyxel.blt(arme_slot_x, arme_slot_y, 0, arme_res_x, arme_res_y, arme_size_x, arme_size_y, 0) # Affiche l'arme dans la main du personnage
                    ##### ARME -> TIR #####
                    if arme_tir_statut == True:
                        # Tire la munition
                        pyxel.blt(arme_tir_x, arme_tir_y, 0, arme_munition_res_selectionne_x, arme_munition_res_selectionne_y, arme_munition_size_x, arme_munition_size_y, 0)

                ##### PERSONNAGE #####
                pyxel.blt(personnage_x, personnage_y, 0, personnage_selectionne2_res_x, personnage_selectionne2_res_y, -personnage_size_x, -personnage_size_y, 7)

            else:

                # Dessin du personnage :
                pyxel.blt(personnage_defaut_x, personnage_defaut_y, 0, personnage_selectionne1_res_x, personnage_selectionne1_res_y, personnage_size_x, personnage_size_y, 7) # Personnage
                # Dessin des clefs
                pyxel.blt(clef0_defaut_x, clef0_defaut_y, 0, clef0_res_x, clef0_res_y, clef0_size_x, clef0_size_y, 0) # Clef 0
                pyxel.blt(clef1_defaut_x, clef1_defaut_y, 0, clef1_res_x, clef1_res_y, clef1_size_x, clef1_size_y, 0) # Clef 1
                pyxel.blt(clef2_defaut_x, clef2_defaut_y, 0, clef2_res_x, clef2_res_y, clef2_size_x, clef2_size_y, 0) # Clef 2
                pyxel.blt(clef3_defaut_x, clef3_defaut_y, 0, clef3_res_x, clef3_res_y, clef3_size_x, clef3_size_y, 0) # Clef 3
                pyxel.blt(clef4_defaut_x, clef4_defaut_y, 0, clef4_res_x, clef4_res_y, clef4_size_x, clef4_size_y, 0) # Clef 4
                pyxel.blt(clef5_defaut_x, clef5_defaut_y, 0, clef5_res_x, clef5_res_y, -clef5_size_x, -clef5_size_y, 0) # Clef 5
                pyxel.blt(clef6_defaut_x, clef6_defaut_y, 0, clef6_res_x, clef6_res_y, clef6_size_x, clef6_size_y, 0) # Clef 6
                # Dessin de l'arme
                pyxel.blt(arme_defaut_x, arme_defaut_y, 0, arme_res_x, arme_res_y, arme_size_x, arme_size_y, 0) # Elle a des coordonnées par défaut mais si elle est récupérée elle ne s'affichera plus


            ##### VOISIN #####
            if voisin_direction == 1:
                pyxel.blt(voisin_x, voisin_y, 0, voisin_res1_x, voisin_res1_y, voisin_size_x, voisin_size_y, 7)
            elif voisin_direction == 2:
                pyxel.blt(voisin_x, voisin_y, 0, voisin_res2_x, voisin_res2_y, voisin_size_x, voisin_size_y, 7)
            elif voisin_direction == 3:
                pyxel.blt(voisin_x, voisin_y, 0, voisin_res1_x, voisin_res1_y, -voisin_size_x, -voisin_size_y, 7)
            elif voisin_direction == 4:
                pyxel.blt(voisin_x, voisin_y, 0, voisin_res2_x, voisin_res2_y, -voisin_size_x, -voisin_size_y, 7)
            
            ##### VIES #####
            # Affiche la barre de vie du joueur
            pyxel.rectb(personnage_x - 2, personnage_y - 4, personnage_size_x + 4, 3, 15)
            # Affiche la ou en est la vie du joueur
            if personnage_vies_max == 3:

                if personnage_vies == 3: # Si le nombre de vies restantes est au maximum:
                    pyxel.rect(personnage_x - 1, personnage_y - 3, (personnage_size_x + 2), 1, 11)
                elif personnage_vies == 2: # Si le nombre de vies restantes est à 2:
                    pyxel.rect(personnage_x - 1, personnage_y - 3, (personnage_size_x + 2) // 1.5, 1, 11)
                elif personnage_vies == 1: # Si le nombre de vies restantes est à 1:
                    pyxel.rect(personnage_x - 1, personnage_y - 3, (personnage_size_x + 2) // 3, 1, 11)
                elif personnage_vies == 0: # Si le nombre de vies restantes est nul:
                    pyxel.rect(personnage_x - 1, personnage_y - 3, 0, 0, 11)

            elif personnage_vies_max == 2:

                if personnage_vies == 2: # Si le nombre de vies restantes est au maximum:
                    pyxel.rect(personnage_x - 1, personnage_y - 3, (personnage_size_x + 2), 1, 11)
                elif personnage_vies == 1: # Si le nombre de vies restantes est à 1:
                    pyxel.rect(personnage_x - 1, personnage_y - 3, (personnage_size_x + 2) // 2, 1, 11)
                elif personnage_vies == 0: # Si le nombre de vies restantes est nul:
                    pyxel.rect(personnage_x - 1, personnage_y - 3, 0, 0, 11)

            elif personnage_vies_max == 1:

                if personnage_vies == 1: # Si le nombre de vies restantes est au maximum:
                    pyxel.rect(personnage_x - 1, personnage_y - 3, (personnage_size_x + 2), 1, 11)
                elif personnage_vies == 0: # Si le nombre de vies restantes est nul:
                    pyxel.rect(personnage_x - 1, personnage_y - 3, 0, 0, 11)

            pyxel.text(interface_x + 2, interface_y + 2, "TIMER:" + str(jeu_timer//FPS), 7)

    # =========================================================
    # LANCEMENT DU JEU
    # =========================================================

    # Initialisation des variables à leur valeur par défaut
    TITLE, WIDTH, HEIGHT, FPS, jeu_statut, jeu_perdu, jeu_gagne, jeu_niveau, jeu_page, jeu_timer, gamemod_statut, collisions_statut, endurance_statut, personnage_defaut_x, personnage_defaut_y, personnage_x, personnage_y, personnage_direction, personnage_vitesse, personnage_vies_max, personnage_vies, personnage_endurance, endurance_pleine_statut, endurance_inprogress_statut, endurance_faible_statut, personnage_selectionne, personnage_selectionne1_res_x, personnage_selectionne2_res_x, personnage_selectionne1_res_y, personnage_selectionne2_res_y, personnage_size_x, personnage_size_y, personnage11_res_x, personnage11_res_y, personnage12_res_x, personnage12_res_y, personnage21_res_x, personnage21_res_y, personnage22_res_x, personnage22_res_y, personnage31_res_x, personnage31_res_y, personnage32_res_x, personnage32_res_y, personnage41_res_x, personnage41_res_y, personnage42_res_x, personnage42_res_y, voisin_defaut_x, voisin_defaut_y, voisin_v, voisin_trajectoire, voisin_direction, voisin_x, voisin_y, voisin_res1_x, voisin_res1_y, voisin_res2_x, voisin_res2_y, voisin_size_x, voisin_size_y, voisin_touchee, voisin_endormi_temps, voisin_endormi_max, voisin_trajectoire_pause, voisin_trajectoire_pause_max, voisin_trajectoire_changement_max, inventaire_objet_selectionne, inventaire_objet_selectionne_x, inventaire_objet_selectionne_y, inventaire_munition_slot_x, inventaire_munition_slot_y, marge_interaction, marge_px, marge_py, arme_defaut_x, arme_defaut_y, arme_x, arme_y, arme_size_x, arme_size_y, arme_bar_color, arme_statut, arme_tir_avancement, arme_cooldown, arme_munition, arme_direction, arme_tir_x, arme_tir_y, arme_tir_size_x, arme_tir_size_y, arme_tir_statut, arme_res_x, arme_res_y, arme_munition_count, arme_munition_size_x, arme_munition_size_y, arme_munition1_statut, arme_munition1_defaut_x, arme_munition1_defaut_y, arme_munition1_x, arme_munition1_y, arme_munition1_res_x, arme_munition1_res_y, arme_munition2_statut, arme_munition2_defaut_x, arme_munition2_defaut_y, arme_munition2_x, arme_munition2_y, arme_munition2_res_x, arme_munition2_res_y, arme_munition3_statut, arme_munition3_defaut_x, arme_munition3_defaut_y, arme_munition3_x, arme_munition3_y, arme_munition3_res_x, arme_munition3_res_y, arme_munition4_statut, arme_munition4_defaut_x, arme_munition4_defaut_y, arme_munition4_x, arme_munition4_y, arme_munition4_res_x, arme_munition4_res_y, clef0_defaut_x, clef0_defaut_y, clef0_x, clef0_y, clef0_statut, clef0_size_x, clef0_size_y, clef0_res_x, clef0_res_y, clef0_utilise, clef1_defaut_x, clef1_defaut_y, clef1_x, clef1_y, clef1_statut, clef1_size_x, clef1_size_y, clef1_res_x, clef1_res_y, clef1_utilise, clef2_defaut_x, clef2_defaut_y, clef2_x, clef2_y, clef2_statut, clef2_size_x, clef2_size_y, clef2_res_x, clef2_res_y, clef2_utilise, clef3_defaut_x, clef3_defaut_y, clef3_x, clef3_y, clef3_statut, clef3_size_x, clef3_size_y, clef3_res_x, clef3_res_y, clef3_utilise, clef4_defaut_x, clef4_defaut_y, clef4_x, clef4_y, clef4_statut, clef4_size_x, clef4_size_y, clef4_res_x, clef4_res_y, clef4_utilise, clef5_defaut_x, clef5_defaut_y, clef5_x, clef5_y, clef5_defaut_y, clef5_statut, clef5_size_x, clef5_size_y, clef5_res_x, clef5_res_y, clef5_utilise, clef6_defaut_x, clef6_defaut_y, clef6_x, clef6_y, clef6_statut, clef6_size_x, clef6_size_y, clef6_res_x, clef6_res_y, clef6_utilise, porte0_defaut_x, porte0_defaut_y, porte0_x, porte0_y, porte0_statut, porte0_size_x, porte0_size_y, porte0_res_x, porte0_res_y, porte1_defaut_x, porte1_defaut_y, porte1_x, porte1_y, porte1_statut, porte1_size_x, porte1_size_y, porte1_res_x, porte1_res_y, porte2_defaut_x, porte2_defaut_y, porte2_x, porte2_y, porte2_statut, porte2_size_x, porte2_size_y, porte2_res_x, porte2_res_y, porte3_defaut_x, porte3_defaut_y, porte3_x, porte3_y, porte3_statut, porte3_size_x, porte3_size_y, porte3_res_x, porte3_res_y, porte4_defaut_x, porte4_defaut_y, porte4_x, porte4_y, porte4_statut, porte4_size_x, porte4_size_y, porte4_res_x, porte4_res_y, porte5_defaut_x, porte5_defaut_y, porte5_x, porte5_y, porte5_statut, porte5_size_x, porte5_size_y, porte5_res_x, porte5_res_y, porte6_defaut_x, porte6_defaut_y, porte6_x, porte6_y, porte6_statut, porte6_size_x, porte6_size_y, porte6_res_x, porte6_res_y = reset()
    # Initialisation des valeurs de la feunêtre
    pyxel.init(WIDTH, HEIGHT, title=TITLE, fps=FPS)
    # Charger le fichier des ressources
    pyxel.load("res_final.pyxres")
    # Démarrage du programme
    pyxel.run(update, draw)

else:

    pass