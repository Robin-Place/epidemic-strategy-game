# -*- coding: utf-8 -*-

# Imports 

import csv
import math
from pathlib import Path
from Modele import Pays, Ville, Reseau, Virus, Dico_mesure
from ConvertisseurDeCoordonnees import ConvertisseurDeCoordonnees


# Fonctions

def lire_donnees_villes(donnees_villes, nb_villes=math.inf):
    pays = {}
    villes = {}
    with open(donnees_villes, newline='', encoding='cp1252') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        i = 1
        for ligne in reader:
            if ligne[1] not in pays:
                pays[ligne[1]] = Pays(ligne[1], int(ligne[6]), int(ligne[5]), ligne[8])
            villes[ligne[0]] = Ville(ligne[0], pays[ligne[1]], int(ligne[2]), int(ligne[9]), ligne[10], int(ligne[11]), float(ligne[3]), float(ligne[4]))
            if i >= nb_villes:
                break
            i += 1
    if i < nb_villes:
        print(f"Nombre de villes insuffisant : {i} villes trouvées")
    return pays, villes


def lire_donnees_virus(donnees_virus):
    virus = {}
    with open(donnees_virus, newline='', encoding='cp1252') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        for ligne in reader:
            virus[ligne[0]] = Virus(ligne[0], int(ligne[2]), int(ligne[3]), float(ligne[4][:-1])/100, int(ligne[5]), float(ligne[6]))
    return virus


# Programme principal

def main():
    # Les lecteurs de données restent importables sans ouvrir de fenêtre.
    from Controleur import Controleur
    from Vue import Monde

    racine = Path(__file__).resolve().parent
    fichier_villes = racine / "Worldcities - Données Villes 2.csv"
    fichier_virus = racine / "Worldcities - Données Virus 3.csv"
    l_canvas, h_canvas, offset_earth, offset_screen, h_menu = 1000, 500, 50, 30, 50
    variations, couts, couts_politiques, facteurs_vaccin = [0.05, 0.10, 0.25, 0.60, 1], [5e12, 1e13, 2.5e13, 5e13, 1e14], [0.02, 0.08, 0.15, 0.2, 0.25], [0.05, 0.10, 0.30]
    rayon_action_mesures_soutien = 100
    pays, villes = lire_donnees_villes(fichier_villes, nb_villes=20)
    virus = lire_donnees_virus(fichier_virus)
    conv = ConvertisseurDeCoordonnees(l_canvas, h_canvas, offset_earth, offset_screen)
    reseau = Reseau(villes, conv)
    mesures = Dico_mesure(reseau, variations, couts, couts_politiques, facteurs_vaccin, rayon_action_mesures_soutien)
    mesures.init_dico_mesures_ville()
    controleur = Controleur(reseau, virus, mesures.dico_mesures)
    monde = Monde(controleur, l_canvas, h_canvas, h_menu, rayon_action_mesures_soutien)
    controleur.afficher_villes()
    monde.mainloop()


if __name__ == "__main__":
    main()




