# -*- coding: utf-8 -*-

# Imports
import csv
import math
import numpy as np
import matplotlib.pyplot as plt
from time import time, sleep
from random import random, choice
from Modele import Reseau, Virus, Dico_mesure
from ConvertisseurDeCoordonnees import ConvertisseurDeCoordonnees


# Fonctions

def lire_donnees_villes(donnees_villes, nb_villes=math.inf):
    """ 
    Effetue la lecture du fichier csv contenant les données sur les villes
    
    Args : 
        donnees_villes (str) : nom du fichier contenant les données
        nb_villes (int) : nombre de villes dont on veut extraire les données (par défaut la totalité)
        
    Return : 
        (dict) dictionnaire qui associe au nom de chaque ville l'objet Ville associé
    """
    villes = {}
    with open(donnees_villes, newline='', encoding='cp1252') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        i = 1
        for ligne in reader:
            villes[ligne[0]] = Ville_2(ligne[0], float(ligne[1]), float(ligne[2]), int(ligne[3]))
            if i >= nb_villes:
                break
            i += 1
    if i < nb_villes:
        print(f"Nombre de villes insuffisant : {i} villes trouvées")
    return villes


def lire_donnees_virus(donnees_virus):
    """ 
    Effetue la lecture du fichier csv contenant les données sur les virus
    
    Args : 
        donnees_virus (str) : nom du fichier contenant les données
        
    Return : 
        (dict) dictionnaire qui associe au nom de chaque virus l'objet Virus associé
    """
    virus = {}
    with open(donnees_virus, newline='', encoding='cp1252') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        for ligne in reader:
            virus[ligne[0]] = Virus(ligne[0], int(ligne[2]), int(ligne[3]), float(ligne[4][:-1])/100, int(ligne[5]), float(ligne[6]))
    return virus


# Classes modifiées

class Ville_2:
    
    def __init__(self, nom, lat, long, population):
        """
        Initialise l'objet ville
        
        Args : 
            nom (str) : nom de la ville
            lat (float) : latitude de la ville
            long (float) : longitude de la ville
            population (int) : population de la ville
        """
        self.nom = nom
        self.lat = lat
        self.long = long
        self.pop = population
        self.sir = {"s":1, "e":0, "i":0, "r":0, "d":0}
    
    
    def get_dico_mesures_ville(self, dico_mesures):
        """
        Initialise le dictionnaire des mesures propre à chaque ville. 

        Args :
            dico_mesures (dict) : dictionnaire d'objets mesure global au jeu
        """
        self.dico_mesures =  dico_mesures
        self.dico_mesures_ville = {}
        # etat entre 0 et 4 : 0 mesure supprimée, 1 mesure non active, 2 mesure passive, 3 mesure active, 4 mesure de soutien active
        self.dico_mesures_ville["Port du masque"] = {"mesure" : dico_mesures["Port du masque"].copy(), "etat" : 1}
        self.dico_mesures_ville["Développement hôpitaux"] = {"mesure" : dico_mesures["Développement hôpitaux"].copy(), "etat" : 1}
        self.dico_mesures_ville["Confinement"] = {"mesure" : dico_mesures["Confinement"].copy(), "etat" : 1}
        self.dico_mesures_ville["Quarantaine"] = {"mesure" : dico_mesures["Quarantaine"].copy(), "etat" : 1}
        self.dico_mesures_ville["Campagne de prévention"] = {"mesure" : dico_mesures["Campagne de prévention"].copy(), "etat" : 1}
        self.dico_mesures_ville["Boost économique"] = {"mesure" : dico_mesures["Boost économique"].copy(), "etat" : 1}
        self.dico_mesures_ville["Usines"] = {"mesure" : dico_mesures["Usines"].copy_soutien(), "etat" : 1}
        self.dico_mesures_ville["Base militaire"] = {"mesure" : dico_mesures["Base militaire"].copy_soutien(), "etat" : 1}
        
        for val in self.dico_mesures_ville.values() :
            val["mesure"].ajouter_ville(self)
    

    def get_multiplicateurs_mesures(self):
        """
        Calcule et renvoie le produit des coefficients de toutes les mesures ACTIVES (état 3) dans la ville.
        
        Return : 
            mult (dict) : dico des multitplicateurs à associer aux mesures
        """
        mult = {"alpha": 1.0, "beta": 1.0, "gamma": 1.0, "mu": 1.0, "delta": 1.0, "phi": 1.0}
        for nom_mesure, donnees in self.dico_mesures_ville.items():
            if donnees["etat"] == 3: # On ne prend en compte que l'état 3 (mesure active)
                mesure = donnees["mesure"]
                mult["alpha"] *= mesure.alpha*self.dico_mesures["Campagne de vaccination"].alpha
                mult["beta"] *= mesure.beta*self.dico_mesures["Campagne de vaccination"].beta
                mult["gamma"] *= mesure.gamma*self.dico_mesures["Campagne de vaccination"].gamma
                mult["mu"] *= mesure.mu*self.dico_mesures["Campagne de vaccination"].mu
                mult["delta"] *= mesure.delta*self.dico_mesures["Campagne de vaccination"].delta
                mult["phi"] *= mesure.phi*self.dico_mesures["Campagne de vaccination"].phi
        return mult        


class Controleur_2:
    
    def __init__(self, Reseau, virus, niveau):
        """
        Initialise le controleur du jeu
        
        Args : 
            Reseau (Reseau) : objet Reseau contenant toutes les villes du jeu et les méthodes pour manipuler le réseau
            virus (Virus) : virus qui a été choisi par le joueur
            niveau (int) : niveau du virus
        """
        self.Reseau = Reseau
        self.Virus = virus
        self.niveau = niveau
        self.ville_source = choice(list(Reseau.villes.values()))
        self.ville_source.sir["i"] = 1/200
        self.ville_source.sir["s"] -= 1/200
        self.Propagation = Propagation_2(self, self.Virus, self.ville_source)
        
        for ville in Reseau.villes.values():
            ville.historique = {
                "t": [1.0], # Le jour de départ
                "S": [ville.sir["s"] * ville.pop],
                "I": [ville.sir["i"] * ville.pop],
                "D": [ville.sir["d"] * ville.pop]
            }


class Propagation_2:
    
    def __init__(self, Controleur, virus, ville_source):
        """
        Initialise l'objet Propagation
        
        Args : 
            Controleur (Controleur) : Controleur du jeu
            virus (Virus) : Virus à propager
            ville_source (Ville) : Ville choisie aléatoirement dont la propagation est issue
        """
        self.Controleur = Controleur
        self.virus = virus
        self.villes_infectees = [ville_source]
        
    
    def propagation(self, nb_jours, version):
       """
       Propage le virus entre les tours
       
       Args : 
           nb_jours (int) : durée de la propagation entre les tours
           version (str) : version du programme à utiliser (par défaut la plus récente)
       """
       # On calcule l'avancée de l'épidémie à l'intérieur des villes infectées
       for ville in self.villes_infectees:
           self.propagation_intra(ville, nb_jours, version)
           
       # On calcule les voyages du virus entre les villes
       for ville_1 in self.villes_infectees:
           for ville_2 in self.Controleur.Reseau.villes.values():
               if ville_1 != ville_2:    
                   self.propagation_inter(ville_1, ville_2, version)
    
    
    def propagation_inter(self, ville_1, ville_2, version):
        """
        Propagae la maladie entre deux villes
        
        Args : 
            nb_jours (int) : durée de la propagation entre les tours
            ville_1 (Ville) : ville dont est issue la propagation
            ville_2 (Ville) : ville dans laquelle peut arriver la propagation
            version (str) : version du programme à utiliser
        """
        if version == '1':
            # Ancienne version basée sur la distance --> inadaptée aux tests avec beaucoup de villes
            villes = list(self.Controleur.Reseau.villes.values())
            i_ville_1 = villes.index(ville_1)
            i_ville_2 = villes.index(ville_2)
            distance = self.Controleur.Reseau.matrice_distances[i_ville_1][i_ville_2]        
            pression = ville_1.sir["i"]
            k = 25 # Facteur d'équilibrage
            probabilite_infection = k * pression / (distance**2)
        elif version == '2':
            # Contournement des .index --> beaucoup plus efficace
            # Utilisation de poids_connexion = 1/distance**2 --> adapté aux tests avec un nombre de villes variables
            poids_connexion = self.Controleur.Reseau.matrice_proba_inter[ville_1.id_matrice][ville_2.id_matrice]
            pression = ville_1.sir["i"]
            k = 25 # Facteur d'équilibrage
            probabilite_infection = k * pression * poids_connexion
        
        if 5 * random() < probabilite_infection * self.Controleur.niveau:
            if version == '1':
                # Aucun vérification 
                probabilite_infection /= 500
            elif version == '2':    
                # Majoration de l'infection
                probabilite_infection = min(probabilite_infection/500, ville_1.sir["s"], ville_2.sir["s"])
            ville_1.sir["i"] += probabilite_infection
            ville_1.sir["s"] -= probabilite_infection
            
            ville_2.sir["i"] += probabilite_infection
            ville_2.sir["s"] -= probabilite_infection
            
            if ville_2 not in self.villes_infectees :
                self.villes_infectees.append(ville_2)


    def propagation_intra(self, ville, nb_jours, version):
        """
        Propagae la maladie au sein d'une ville
        
        Args : 
            ville (Ville) : ville dans laquelle la propagation a lieu
            nb_jours (int) : durée de la propagation entre les tours
            version (str) : version du programme à utiliser
        """
        dt = 0.01
        N = int(nb_jours/dt) # Nombre de pas de temps
        t = np.linspace(0, nb_jours, N+1)
        X0 = np.array([ville.sir["s"], ville.sir["e"], ville.sir["i"], ville.sir["r"], ville.sir["d"]])
        
        
        def derivative(X, t):
            """
            Met en place le système différentiel de la propagation pour le modèle SEIRD
            
            Args : 
                X (array) : vecteur des valeurs initiales du dico sir de la ville
                t (array) : vecteur du temps
            
            Return: 
                (array) valeur des corrections à apporter au vecteur initial
            """
            S, E, I, R, D = X
            dotS = - beta_eff * S * I + delta_eff * R
            dotE = beta_eff * S * I - alpha_eff * E
            dotI = alpha_eff * E - (gamma_eff + mu_eff) * I
            dotR = gamma_eff * I - delta_eff * R
            dotD = mu_eff * I
            return np.array([dotS, dotE, dotI, dotR, dotD])
        
        
        def Euler(func, X0, t):
            """
            Schéma de résolution du système d'équations différentielles
            
            Args : 
                func (fonction) : fonction renvoyant la valeur des corrections à apporter au vecteur initial
                X0 (array) : vecteur des valeurs initiales du dico sir de la ville
                t (array) : vecteur du temps
            
            Return: 
                (array) valeur du nouveau vecteur des valeurs du dico sir de la ville
            """
            dt = t[1] - t[0]
            N = len(t)
            X  = np.zeros([N, X0.shape[0]])
            X[0] = X0
            for i in range(N-1):
                X[i+1] = X[i] + func(X[i], t[i]) * dt
            return X
        
        
        def Euler_2(X0, t):
            """
            Schéma de résolution du système d'équations différentielles augmenté de bornes pour les valeurs du dico et utilisant des variables natives
            
            Args : 
                X0 (array) : vecteur des valeurs initiales du dico sir de la ville
                t (array) : vecteur du temps
            
            Return: 
                (array) valeur du nouveau vecteur des valeurs du dico sir de la ville
            """
            dt = t[1] - t[0]
            N = len(t)
            X = np.zeros([N, 5])
            X[0] = X0
            S, E, I, R, D = X0
            
            for i in range(N-1):
                dotS = - beta_eff * S * I / ville.pop + delta_eff * R
                dotE = beta_eff * S * I / ville.pop - alpha_eff * E
                dotI = alpha_eff * E - (gamma_eff + mu_eff) * I
                dotR = gamma_eff * I - delta_eff * R
                dotD = mu_eff * I
                
                S += dotS * dt
                E += dotE * dt
                I += dotI * dt
                R += dotR * dt
                D += dotD * dt
                
                S = max(0.0, min(1.0, S))
                E = max(0.0, min(1.0, E))
                I = max(0.0, min(1.0, I))
                R = max(0.0, min(1.0, R))
                D = max(0.0, min(1.0, D))
                
                X[i+1] = [S, E, I, R, D]

            return X
        
        
        mults = ville.get_multiplicateurs_mesures()
        alpha_eff = (self.virus.alpha * mults["alpha"])
        beta_eff  = (self.virus.beta * mults["beta"])
        gamma_eff = (self.virus.gamma * mults["gamma"])
        delta_eff = (self.virus.delta * mults["delta"])
        mu_eff    = (self.virus.mu * mults["mu"])
        
        if version == '1':
            # Création de tableaux Numpy a chaque itération
            # Aucune vérification sur la cohérence des résultats
            X = Euler(derivative, X0, t)
        
        elif version == '2':
            # Utilisation de variables natives --> gain d'efficacité
            # Valeurs bornées pour les proportion pour éviter la divergence du schéma d'Euler sans diminuer le pas de temps
            X = Euler_2(X0, t)
        
        ville.sir["s"] = X[:, 0][-1]
        ville.sir["e"] = X[:, 1][-1]
        ville.sir["i"] = X[:, 2][-1]
        ville.sir["r"] = X[:, 3][-1]
        ville.sir["d"] = X[:, 4][-1]      


# Paramètres
fichier_villes = "Worldcities - Données Villes_2.csv"
fichier_virus = "Worldcities - Données Virus 3.csv"

l_canvas, h_canvas, offset_earth, offset_screen, h_menu = 1000, 500, 50, 300, 50
variations, couts, couts_politiques, facteurs_vaccin = [0.05, 0.10, 0.25, 0.60, 1], [5e12, 1e13, 2.5e13, 5e13, 1e14], [0.02, 0.08, 0.15, 0.2, 0.25], [0.05, 0.10, 0.30]
rayon_action_mesures_soutien = 100

virus = list(lire_donnees_virus(fichier_virus).values())

version = '2'
nb_villes = [10, 100, 1000, 2500, 5000, 7500, 10000]
nb_jours = [10, 100, 1000, 2500, 5000, 10000, 25000, 50000, 100000]
liste_virus = [(virus[i], i%2) for i in range(8)]
temps_exe_1 = []
temps_exe_2 = []
temps_exe_3 = []
variables = ["villes"] # "villes", "jours", "virus"



# Calculs
if "villes" in variables:
    Conv = ConvertisseurDeCoordonnees(l_canvas, h_canvas, offset_earth, offset_screen)
    for n in nb_villes:
        t0 = time()
        villes = lire_donnees_villes(fichier_villes, nb_villes=n)
        reseau = Reseau(villes, Conv)
        Dico_mesures = Dico_mesure(reseau, variations, couts, couts_politiques, facteurs_vaccin, rayon_action_mesures_soutien)
        Dico_mesures.init_dico_mesures_ville()
        Controleur = Controleur_2(reseau, virus[7], 4)
        t1 = time()
        for i in range(10):
            Controleur.Propagation.propagation(10, version)
        t2 = time()
        temps_exe_1.append(t2-t1)
        print(f"{n} villes --> {t2-t1} s ({t1-t0} s)")


if "jours" in variables:
    villes = lire_donnees_villes(fichier_villes, nb_villes=100)
    Conv = ConvertisseurDeCoordonnees(l_canvas, h_canvas, offset_earth, offset_screen)
    for n in nb_jours:
        t0 = time()
        reseau = Reseau(villes, Conv)
        Dico_mesures = Dico_mesure(reseau, variations, couts, couts_politiques, facteurs_vaccin, rayon_action_mesures_soutien)
        Dico_mesures.init_dico_mesures_ville()
        Controleur = Controleur_2(reseau, virus[0], 1)
        t1 = time()
        Controleur.Propagation.propagation(n, version)
        t2 = time()
        temps_exe_2.append(t2-t1)
        print(f"{n} jours --> {t2-t1} s ({t1-t0} s)")
    

if "virus" in variables:
    villes = lire_donnees_villes(fichier_villes, nb_villes=100)
    Conv = ConvertisseurDeCoordonnees(l_canvas, h_canvas, offset_earth, offset_screen)
    for v in liste_virus:
        t0 = time()
        reseau = Reseau(villes, Conv)
        Dico_mesures = Dico_mesure(reseau, variations, couts, couts_politiques, facteurs_vaccin, rayon_action_mesures_soutien)
        Dico_mesures.init_dico_mesures_ville()
        Controleur = Controleur_2(reseau, v[0], v[1])
        t1 = time()
        Controleur.Propagation.propagation(1000, version)
        t2 = time()
        temps_exe_3.append(t2-t1)
        print(f"{v[0].nom} --> {t2-t1} s ({t1-t0} s)")


# Affichage
print(temps_exe_1, temps_exe_2, temps_exe_3)

figure = plt.figure(figsize = (16, len(variables)*10))

if "villes" in variables:
    ax = figure.add_subplot(len(variables), 1, variables.index("villes")+1)
    ax.plot(nb_villes, temps_exe_1)
    ax.set_title(f"Evolution du temps d'exécution en fonction du nombre de villes - Version {version}")
    ax.set_xlabel("Nombre de villes du réseau")
    ax.set_ylabel("Temps d'exécution (s)")
    ax.set_xlim([min(nb_villes), max(nb_villes)])
    ax.set_ylim([0, 1.1*max(temps_exe_1)])
    # [0.01698136329650879, 0.016004323959350586, 0.01799941062927246, 0.03000020980834961, 0.12951421737670898, 0.040285348892211914, 0.04406237602233887, 0.05264163017272949, 0.08508872985839844]

if "jours" in variables:
    ax = figure.add_subplot(len(variables), 1, variables.index("jours")+1)
    ax.plot(nb_jours, temps_exe_2)
    ax.set_title(f"Evolution du temps d'exécution en fonction du nombre de jours - Version {version}")
    ax.set_xlabel("Durée de la propagation (jours)")
    ax.set_ylabel("Temps d'exécution (s)")
    ax.set_xlim([min(nb_jours), max(nb_jours)])
    ax.set_ylim([0, 1.1*max(temps_exe_2)])
    # [0.003998994827270508, 0.04080557823181152, 0.4331035614013672, 1.0717427730560303, 2.3400871753692627, 6.0427398681640625, 14.729548931121826, 29.931869983673096, 61.7673077583313]

if "virus" in variables:
    ax = figure.add_subplot(len(variables), 1, variables.index("virus")+1)
    ax.plot([v.nom for v in virus], temps_exe_3)
    ax.set_title(f"Evolution du temps d'exécution en fonction du virus - Version {version}")
    ax.set_xlabel("Virus")
    ax.set_ylabel("Temps d'exécution (s)")
    ax.set_xlim([0, 7])
    ax.set_ylim([0, 1.1*max(temps_exe_3)])

plt.show()

