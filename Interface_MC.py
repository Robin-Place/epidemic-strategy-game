# -*- coding: utf-8 -*-

# Imports

import numpy as np
from random import random
from Vue import formatage


# Classes

class Popularite :
    
    def __init__(self, Controleur, facteur_mesure, facteur_global):
        """
        Initialise la popularite du joueur qui commence avec une popularite de 1 (100%).
        
        Args : 
            Controleur (Controleur) : Controleur du jeu
            facteur_mesure (float) : facteur d'augmentation par mesure (identique pour toutes les mesures)
            facteur_global (float) : facteur d'augmentation global

        """
        self.Controleur = Controleur
        self.popularite = 1.0
        self.facteur_mesure = facteur_mesure # le facteur d'augmentation est le meme pour toutes les mesures
        self.facteur_global = facteur_global
    
    
    def impact_popularite(self):
       """ 
       Determine l'impact de la popularite à chaque tour et sur chaque mesure prise.
       """
       villes = self.Controleur.Reseau.villes #recupere le dictionnaire de villes du jeu
       for ville in villes.values():
           for nom_mesure, donnees in ville.dico_mesures_ville.items(): #parcourt le dico_mesures_ville de chaque ville
               if self.popularite < 0.75 : 
                   if nom_mesure in ["Confinement", "Quarantaine"] : 
                       donnees["mesure"].cout = donnees["mesure"].cout_init*(1+self.facteur_mesure)
               if self.popularite < 0.5 :
                   if nom_mesure in ["Campagne de vaccination", "Campagne de prévention", "Port du masque"]:
                       donnees["mesure"].cout = donnees["mesure"].cout_init*(1+self.facteur_mesure)
               if self.popularite < 0.25 :
                   donnees["mesure"].cout = donnees["mesure"].cout_init*(1+self.facteur_global)
                   
                   # les mesures suivantes deviennent indisponibles
                   ville.dico_mesures_ville["Port du masque"]["etat"] = 0
                   ville.dico_mesures_ville["Quarantaine"]["etat"] = 0
                   
       if self.popularite > 1: #bloque la popularité à 100%
            self.popularité = 1



class Monnaie:
    
    def __init__(self, Controleur):
        """
        Initialise la monnaie du jeu
        
        Args : 
            Controleur (Controleur) : Controleur du jeu
        """
        self.Controleur = Controleur
        self.valeur = 25e12
    
    
    def modif_valeur(self, montant):
        """
        Modifie la valeur de la monnaie disponible en fonction du montant choisi si les fonds du joueur le permettent
        
        Args : 
            montant (float) : valeur à ajouter à la monnaie du joueur(positive ou négative)
        """
        if montant + self.valeur < 0: #vérifie qu'il y a suffisamment de monnaie
            return False
        else:
            self.valeur += montant
            self.Controleur.Monde.label_monnaie.config(text=f"{formatage(self.Controleur.Monnaie.valeur)}")
            return True
        
    

class Propagation:
    
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
        self.pop_infectee = ville_source.pop/500
        self.pop_decedee = 0
        
    
    def propagation(self, nb_jours, version='2'):
        """
        Propage le virus entre les tours
        
        Args : 
            nb_jours (int) : durée de la propagation entre les tours
            version (str) : version du programme à utiliser (par défaut la plus récente)
        """
        for ville in self.Controleur.Reseau.villes.values():
           ville.actualiser_delais_mesures(nb_jours)
           
           if ville not in self.villes_infectees:
                dt = 0.01
                N = int(nb_jours/dt)
                t_global = np.linspace(0, nb_jours, N+1)[1:] + self.Controleur.jour
                ville.historique["t"].extend(t_global)
                ville.historique["S"].extend([ville.sir["s"]] * N)
                ville.historique["I"].extend([ville.sir["i"]] * N)
                ville.historique["D"].extend([ville.sir["d"]] * N)
       
        self.pop_infectee = 0
        self.pop_decedee = 0
       
        # On calcule l'avancée de l'épidémie à l'intérieur des villes infectées
        for ville in self.villes_infectees:
           self.propagation_intra(ville, nb_jours, version)
           self.pop_infectee += ville.sir["i"]*ville.pop
           self.pop_decedee += ville.sir["d"]*ville.pop
           
        # On calcule les voyages du virus entre les villes
        for ville_1 in self.villes_infectees:
           for ville_2 in self.Controleur.Reseau.villes.values():
               if ville_1 != ville_2:    
                   self.propagation_inter(nb_jours, ville_1, ville_2, version)
    
    
    def propagation_inter(self, nb_jours, ville_1, ville_2, version):
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
            self.pop_infectee += probabilite_infection * ville_1.pop
            
            ville_2.sir["i"] += probabilite_infection
            ville_2.sir["s"] -= probabilite_infection
            self.pop_infectee += probabilite_infection * ville_2.pop
            
            if ville_2 not in self.villes_infectees :
                self.villes_infectees.append(ville_2)
                self.Controleur.Monde.texte += f"Des cas de {self.Controleur.Virus.nom} sont également apparus à {ville_2.nom}. {round(500*probabilite_infection, 3)}\n\n"


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
            dotS = - beta_eff * S * I / ville.pop + delta_eff * R
            dotE = beta_eff * S * I / ville.pop - alpha_eff * E
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
                # Utilisation de variables natives --> beaucoup plus efficace
                dotS = - beta_eff * S * I + delta_eff * R
                dotE = beta_eff * S * I - alpha_eff * E
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
        
        t_global = t[:] + self.Controleur.jour
        ville.historique["t"].extend(t_global)
        ville.historique["S"].extend(X[:, 0]) # Colonne 0 = S
        ville.historique["I"].extend(X[:, 2]) # Colonne 2 = I
        ville.historique["D"].extend(X[:, 4]) # Colonne 4 = D
        
        ville.sir["s"] = X[:, 0][-1]
        ville.sir["e"] = X[:, 1][-1]
        ville.sir["i"] = X[:, 2][-1]
        ville.sir["r"] = X[:, 3][-1]
        ville.sir["d"] = X[:, 4][-1]  
        
        
            