# -*- coding: utf-8 -*-

# Imports

import random
import tkinter as tk
from Vue import Debut_jeu
from Interface_MC import Popularite, Monnaie, Propagation


# Classes

class Controleur:
    
    def __init__(self, Reseau, virus, dico_mesures):
        """
        Initialise le controleur du jeu
        
        Args : 
            Reseau (Reseau) : objet Reseau contenant toutes les villes du jeu et les méthodes pour manipuler le réseau
            virus (Virus) : virus qui a été choisi par le joueur
            dico_mesures (dict) : dictionnaire de l'ensemble des mesures applicables aux villes
        """
        self.Reseau = Reseau
        self.virus = virus
        self.dico_mesures = dico_mesures
        Debut_jeu(self).mainloop()
        self.ville_source = random.choice(list(self.Reseau.villes.values())) #ville source choisie aléatoirement
        self.ville_source.sir["i"] = 1/200
        self.ville_source.sir["s"] -= 1/200
        self.Propagation = Propagation(self, self.Virus, self.ville_source)
        self.Monnaie = Monnaie(self) #initialise la monnaie
        self.Popularite = Popularite(self, 0.1, 0.005) #initialise la popularite
        self.tour = 1
        self.jour = 1
        
        for ville in self.Reseau.villes.values():
            ville.historique = {
                "t": [1.0], # Le jour de départ
                "S": [ville.sir["s"]],
                "I": [ville.sir["i"]],
                "D": [ville.sir["d"]]
            }
    
    
    def lier_monde(self, monde):
        """
        Ajoute le monde du jeu aux attributs du Controleur
        
        Args : 
            monde (Monde) : objet correspondant à la fenêtre principale du jeu
        """
        self.Monde = monde
        self.Monde.texte += f"Un cas de {self.Virus.nom} a été détecté à {self.ville_source.nom}\n\n"

    
    def afficher_villes(self):
        """
        Affiche toutes les villes du jeu dans la fenêtre principale (monde)

        """
        for nom, ville in self.Reseau.villes.items():
            self.Monde.afficher_ville(nom, ville.x, ville.y)


    def fin_de_jeu(self):
        """
        Détermine si le jeu se termine à la fin du tour et si c'est le cas détermine si le joueur a gagné ou perdu. 
        Le joueur perd si plus de 75% de la population mondiale est infectée ou s'il n'a pas réussi à contenir les taux d'infection et de mortalité en dessous de 25 % au bout de 100 jours. 
        Il gagne s'il a réussi à contenir le virus au bout de 100 jours
        
        Returns : 
            str : "perdu", "gagné" ou "continue" 
        """
        res = "continue"
        pop_mondiale = self.Reseau.pop_mondiale_ref
        if 0.75*pop_mondiale <= self.Propagation.pop_infectee or 0.25*pop_mondiale <= self.Propagation.pop_decedee: 
            res = "perdu"
        elif self.Popularite.popularite <= 0 : 
            res = "perdu"
        elif self.dico_mesures["Recherche d'un vaccin"].etape == 4 :
            res = "gagné"
        elif self.jour >= 100 : 
            if 0.25*pop_mondiale <= self.Propagation.pop_infectee : 
                res = "perdu"
            else : 
                res = "gagné"
        return res

