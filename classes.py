import pygame
from pygame.locals import *
from constant import *
from datetime import datetime, timedelta


class Niveau:
    def __init__(self, fichier):
        self.fichier = fichier
        self.structure = [[]]

    def generer(self):
        with open(self.fichier, "r") as fichier:
            structure_niveau = []
            for ligne in fichier:
                ligne_niveau = []
                for sprite in ligne:
                    if sprite != "\n":
                        ligne_niveau.append(sprite)
                structure_niveau.append(ligne_niveau)
            self.structure = structure_niveau

    def afficher(self, fenetre):
        brick = pygame.image.load(image_brick)
        pillar = pygame.image.load(image_pillier)
        sol = pygame.image.load(image_sol)

        num_ligne = 0
        for ligne in self.structure:
            num_case = 0
            for sprite in ligne:
                x = num_case * taille_sprite
                y = num_ligne * taille_sprite

                if sprite == "p":
                    fenetre.blit(pillar, (x, y))
                elif sprite == "s":
                    fenetre.blit(sol, (x, y))
                elif sprite == "b":
                    fenetre.blit(brick, (x, y))
                num_case += 1
            num_ligne += 1

    def detruire(self,case_x, case_y):
        self.structure[int(case_x)][int(case_y)] = "s"



class Perso:
    """Classe permettant de créer un personage"""

    def __init__(self, droite, gauche, haut, bas, niveau):
        # initialisation des images et gestion de la transparance
        self.droite = pygame.image.load(droite).convert()
        self.droite.set_colorkey((255, 255, 255))
        self.gauche = pygame.image.load(gauche).convert()
        self.gauche.set_colorkey((255, 255, 255))
        self.haut = pygame.image.load(haut).convert()
        self.haut.set_colorkey((255, 255, 255))
        self.bas = pygame.image.load(bas).convert()
        self.bas.set_colorkey((255, 255, 255))

        self.case_x = 1
        self.case_y = 1
        self.x = 40
        self.y = 40

        self.direction = self.droite
        self.niveau = niveau

    def deplacer(self, direction):
        """Methode de déplacement du personnage"""

        if direction == "droite":
            # dépassement de l'écran ?
            if self.case_x < (nombre_sprite_cote - 1):
                # destination le sol ?
                if self.niveau.structure[self.case_y][self.case_x + 1] == "s":
                    # déplacement d"une case
                    self.case_x += 1
                    # calcul de la position en px
                    self.x = self.case_x * taille_sprite
            # image dans la bonne direction
            self.direction = self.droite

        if direction == "gauche":
            if self.case_x > 0:
                if self.niveau.structure[self.case_y][self.case_x - 1] == "s":
                    self.case_x -= 1
                    self.x = self.case_x * taille_sprite
            self.direction = self.gauche

        if direction == "haut":
            if self.case_y > 0:
                if self.niveau.structure[self.case_y - 1][self.case_x] == "s":
                    self.case_y -= 1
                    self.y = self.case_y * taille_sprite
            self.direction = self.haut

        if direction == "bas":
            if self.case_y < (nombre_sprite_cote - 1):
                if self.niveau.structure[self.case_y + 1][self.case_x] == "s":
                    self.case_y += 1
                    self.y = self.case_y * taille_sprite
            self.direction = self.bas


class Bomb:
    """Classe controllant la bombe"""
    def __init__(self, bomb, time, niveau, perso):
        # chargement des sprites
        self.bomb = pygame.image.load(bomb).convert()
        self.time = time
        # place la bombe a une position non visible par default
        self.x = 640
        self.y = 640
        self.case_x = 255
        self.case_y = 255
        self._time_created = datetime.now()
        # déclaration des variables de la classe
        self.niveau = niveau
        self.perso = perso
        self.explosion = 0


    def poser(self, x, y, bomb):
        """pose et arme la bombe"""
        self.bomb = pygame.image.load(bomb).convert()
        self.bomb.set_colorkey((255, 255, 255))
        self.x = x
        self.y = y
        self.case_x = int(x / taille_sprite)
        self.case_y = int(y / taille_sprite)
        self._time_created = datetime.now()
        self.explosion = 0

    def exploser(self):
        """Explosion de la bombe"""

        if timedelta(seconds=3) <= datetime.now() - self._time_created:
            self.bomb = pygame.image.load(image_explosion).convert()
            self.bomb.set_colorkey((255, 255, 255))
            self.explosion = 1

            # try / except vrmt hard codé à supprimer
            try:
                # destruction des briques de tous les cotes
                if self.niveau.structure[self.case_y][self.case_x + 1] == "b":
                    self.niveau.detruire(self.case_y, self.case_x + 1)

                if self.niveau.structure[self.case_y][self.case_x - 1] == "b":
                    self.niveau.detruire(self.case_y, self.case_x - 1)

                if self.niveau.structure[self.case_y - 1][self.case_x] == "b":
                    self.niveau.detruire(self.case_y - 1, self.case_x)

                if self.niveau.structure[self.case_y + 1][self.case_x] == "b":
                    self.niveau.detruire(self.case_y + 1, self.case_x)

                # conditions de victoire
                if self.case_x -1 <= self.perso.case_x <= self.case_x +1:
                    if self.case_y -1 <= self.perso.case_y <= self.case_y +1:
                        return 1

            except IndexError:
                pass

        if timedelta(milliseconds=3500) <= datetime.now() - self._time_created:
            # place la bombe a une position non visible
            self.x = 640
            self.y = 640
            self.case_x = 255
            self.case_y = 255
            self.explosion = 0


class Flammes:
    def __init__(self,fflamme_d, fflamme_g, fflamme_h, fflamme_b):
        # chargement des sprites de flammes
        self.fflamme_d = pygame.image.load(fflamme_d).convert()
        self.fflamme_d.set_colorkey((255, 255, 255))
        self.fflamme_g = pygame.image.load(fflamme_g).convert()
        self.fflamme_g.set_colorkey((255, 255, 255))
        self.fflamme_h = pygame.image.load(fflamme_h).convert()
        self.fflamme_h.set_colorkey((255, 255, 255))
        self.fflamme_b = pygame.image.load(fflamme_b).convert()
        self.fflamme_b.set_colorkey((255, 255, 255))




