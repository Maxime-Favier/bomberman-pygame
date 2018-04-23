import pygame
from pygame.locals import *
from datetime import datetime, timedelta

from constant import *
from classes import *

print(cote_fenetre)
pygame.display.init()


fenetre = pygame.display.set_mode((cote_fenetre, cote_fenetre))
pygame.display.set_caption(titre_fenetre)

continuer = 1

while continuer:

    # chargement de l'accueil
    accueil = pygame.image.load(image_accueil).convert()
    fenetre.blit(accueil, (0, 0))

    # rafraichissement
    pygame.display.flip()

    continuer_jeu = 1
    continuer_accueil = 1

    # boucle d'accueil
    while continuer_accueil:

        # limitation de vittesse de la boucle
        pygame.time.Clock().tick(30)

        for event in pygame.event.get():
            # quitter le jeu
            if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
                continuer_accueil = 0
                continuer_jeu = 0
                continuer = 0
                choix = 0
            elif event.type == KEYDOWN and event.key == K_SPACE:
                continuer_accueil = 0
                choix = "n1"

    # Vérification du choix du niveau pour ne pas charger si il quitte ;)
    if choix != 0:
        # chargement du fond
        fond = pygame.image.load(image_fond).convert()

        # generation du niveau à partir d'un fichier
        niveau = Niveau("level.txt")
        niveau.generer()
        niveau.afficher(fenetre)

        # création d'un perso
        perso = Perso(p1_droite, p1_gauche, p1_haut, p1_bas, niveau)
        # création de la bombe
        bombe = Bomb(image_bombe, 10, niveau, perso)
        # création des flammes
        flamme = Flammes(flamme_d, flamme_g, flamme_h, flamme_b)

    # boucle de jeu
    while continuer_jeu:

        # limitation de la vittesse de la boucle
        pygame.time.Clock().tick(30)
        # print(pygame.time.get_ticks())

        for event in pygame.event.get():
            # quitter le jeu
            if event.type == QUIT:
                continuer_jeu = 0
                continuer = 0

            elif event.type == KEYDOWN:
                # retour au menu
                if event.key == K_ESCAPE:
                    continuer_jeu = 0
                if event.key == K_SPACE:
                    bombe.poser(perso.x, perso.y, image_bombe)

                # touches de déplacement
                elif event.key == K_RIGHT:
                    perso.deplacer("droite")
                elif event.key == K_LEFT:
                    perso.deplacer("gauche")
                elif event.key == K_DOWN:
                    perso.deplacer("bas")
                elif event.key == K_UP:
                    perso.deplacer("haut")

        # affichage au nouvelles positions
        fenetre.blit(fond, (0, 0))
        niveau.afficher(fenetre)
        game_over = bombe.exploser()
        fenetre.blit(perso.direction, (perso.x, perso.y))
        fenetre.blit(bombe.bomb, (bombe.x, bombe.y))
        if bombe.explosion == 1:
            fenetre.blit(flamme.fflamme_b,(bombe.x, bombe.y + taille_sprite))
            fenetre.blit(flamme.fflamme_h,(bombe.x, bombe.y - taille_sprite))
            fenetre.blit(flamme.fflamme_g,(bombe.x - taille_sprite, bombe.y))
            fenetre.blit(flamme.fflamme_d,(bombe.x + taille_sprite, bombe.y))
        pygame.display.flip()

        if game_over == 1:
            continuer_jeu = 0







