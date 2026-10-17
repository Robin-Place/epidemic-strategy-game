# -*- coding: utf-8 -*-

# Imports

import math
import numpy as np


# Classes

class Pays:
    
    def __init__(self, nom, population, PIB, ISO):
        """
        Initialise l'objet pays
        
        Args : 
            nom (str) : nom du pays
            population (int) : population du pays
            PIB (int) : PIB du pays
            ISO  (str) : code ISO du pays

        """
        self.nom = nom
        self.population = population
        self.PIB = PIB
        self.code_ISO = ISO



class Ville:
    
    def __init__(self, nom, pays, population, PUB, statut, poids, lat, long):
        """
        Initialise l'objet ville
        
        Args : 
            nom (str) : nom de la ville
            pays (str) : nom du pays
            population (int) : population de la ville
            PUB (int) : PUB de la ville
            statut (str) : catégorie indiquant le niveau d'influence de la ville
            poids (int) : valeur associée au statut de la ville (donc à son influence)
            lat (float) : latitude de la ville
            long (float) : longitude de la ville

        """
        self.nom = nom
        self.pays = pays
        self.pop = population
        self.PUB = PUB
        self.statut = statut
        self.poids = poids
        self.lat = lat
        self.long = long
        self.sir = {"s":1, "e":0, "i":0, "r":0, "d":0}
        self.mesures = []
        

    def get_dico_mesures_ville(self, dico_mesures):
        """
        Initialise le dictionnaire des mesures propre à chaque ville. 

        Args :
            dico_mesures (dict) : dictionnaire d'objets mesure global au jeu
        """
        self.dico_mesures =  dico_mesures
        self.dico_mesures_ville = {}
        # etat entre 0 et 3 : 0 mesure supprimée, 1 mesure non active, 2 mesure passive, 3 mesure active
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
    
    
    def actualiser_delais_mesures(self, nb_jours):
        """
        Diminue le délai des mesures en cours d'activation (état 2).
        Si le délai tombe à 0 ou moins, la mesure passe à l'état 3 (active).
        Diminue aussi la durée d'activation si la mesure est active.
        
        Args : 
            nb_jours (int) : nombre de jours écoulés
        """
        for nom_mesure, donnees in self.dico_mesures_ville.items():
            mesure = donnees["mesure"]
            if donnees["etat"] == 2:  # 2 = Mesure en cours d'activation
                # On diminue le délai restant du nombre de jours passés
                mesure.delai_restant -= nb_jours
                
                # Si le délai est écoulé
                if mesure.delai_restant <= 0:
                    donnees["etat"] = 3  # La mesure devient officiellement active !
                    mesure.duree_activation += mesure.delai_restant # 
                    mesure.delai_restant = 0 # On bloque à 0 pour faire propre
                    if mesure.duree_activation <= 0: # Si la durée d'activation est dépassée
                        donnees["etat"] = 1 #la mesure devient inactive
                        mesure.duree_activation = 0

            elif donnees["etat"] == 3: #3 = mesure active
                mesure.duree_activation -= nb_jours
                if mesure.duree_activation <= 0:
                    donnees["etat"] = 1
                    mesure.duree_activation = 0
    
    
    def get_pub_effectif(self):
        """
        Calcule les revenus journaliers réels en appliquant les mesures (phi)
        ET en retirant de l'économie les personnes malades ou décédées.
        
        Return : 
            (float) PUB effectif de la ville
        """
        mults = self.get_multiplicateurs_mesures()
        
        # Seuls les sains (s), exposés (e), et retirés/guéris (r) peuvent travailler
        # On exclut les infectés (i) et les morts (d)
        ratio_travailleurs = self.sir["s"] + self.sir["e"] + self.sir["r"]

        # Le PUB final dépend des travailleurs et des mesures économiques (phi)
        return self.PUB * ratio_travailleurs * mults["phi"]
    


class Reseau:
    
    def __init__(self, villes, convertisseur):
        """
        Initialise l'objet  Reseau.
        
        Args : 
            villes (dict) : dictionnaire de toutes les villes du jeu (clé : nom de la ville (str) et valeur : objet ville associé)
            convertisseur (ConvertisseurDeCoordonnees) : objet permettant de convertir les coordonnées réelles aux coordonnées sur le canva
        """
        self.villes = villes
        self.conv = convertisseur
        self.pop_mondiale_ref = 0
        i = 0
        for nom, ville in villes.items():
            ville.x, ville.y = self.xy_repere_cartesien(nom)
            ville.Reseau = self
            ville.id_matrice = i
            i += 1
            self.pop_mondiale_ref += ville.pop #permet de calculer la population mondiale de départ
        self.calcul_matrice_adj_2()
    
    
    def effet_mesure(self):
        """
        Applique les effets des mesures de soutien aux villes qui sont situées dans le rayon d'influence des villes dans lesquelles une mesure de soutien est active

        """
        for ville in self.villes.values():
            for nom_mesure, donnees in ville.dico_mesures_ville.items() : 
                if donnees["etat"]==3 and nom_mesure in ["Usines", "Base militaire"] :
                    donnees["mesure"].modif_villes_affectees(nom_mesure)
    
    
    def calcul_min_max_xy(self):
        """
        Calcule les coordonnées cartésiennes minimales et maximales des nœuds dans la structure de graphe.
        
        Return : 
            (tuple) : coordonnées cartésiennes minimales et maximales des nœuds
        """
        x_min = math.inf
        x_max = -math.inf
        y_min = math.inf
        y_max = -math.inf
        
        # Parcours de tous les nœuds du graphe
        for nom, ville in self.villes.items():
            latitude = self.villes[nom].lat
            longitude = self.villes[nom].long
            
            # Conversion des coordonnées géographiques en coordonnées cartésiennes
            x_test, y_test = self.conv.geo_to_canvas(latitude, longitude)
            
            # Mise à jour des valeurs min et max pour les coordonnées x et y
            if x_test < x_min:
                x_min = x_test
            if x_test > x_max:
                x_max = x_test
            if y_test < y_min:
                y_min = y_test
            if y_test > y_max:
                y_max = y_test
                
        return (x_min, x_max, y_min, y_max)
    
    
    def xy_repere_cartesien(self, nom_ville):
        """
        Convertit les coordonnées géographiques d'un nœud en coordonnées cartésiennes.
        
        Return : 
            (tuple) coordonnées cartésiennes du noeud
        """
        if nom_ville not in self.villes:
            raise ValueError("Le nœud spécifié n'existe pas dans le graphe.")

        ville = self.villes[nom_ville]
        x_ville, y_ville = self.conv.geo_to_canvas(ville.lat, ville.long)
        (x_min,x_max,y_min,y_max) = self.calcul_min_max_xy()

        return self.conv.ajuste_to_repere(x_ville, y_ville, x_min, x_max, y_min, y_max)
    
    
    def distance(self, ville1, ville2):
        """
        Calcule la distance entre deux villes 
        
        Args : 
            ville1 (Ville) et ville2 (Ville) : les deux villes dont on souhaite connaître la distance
        
        Return : 
            (float) l distance entre les deux villes
        """
        return ((ville1.x-ville2.x)**2 + (ville1.y-ville2.y)**2)**0.5
    

    def calcul_matrice_adj(self):
        """
        Première version du calcul de la matrice d'adjacence
        """
        liste_villes = list(self.villes.values())
        n = len(liste_villes)
        self.matrice_distances = [[0]*n for i in range(n)]
        for i in range(n):
            for j in range(i, n):
                if i != j:
                    self.matrice_distances[i][j] = self.distance(liste_villes[i], liste_villes[j])
                    self.matrice_distances[j][i] = self.distance(liste_villes[i], liste_villes[j])
    
    
    def calcul_matrice_adj_2(self):
        """
        Deuxième version du calcul de la matrice d'adjacence
        """
        liste_villes = list(self.villes.values())
            
        X = np.array([v.x for v in liste_villes])
        Y = np.array([v.y for v in liste_villes])
        
        dx = X[:, np.newaxis] - X
        dy = Y[:, np.newaxis] - Y
        
        self.matrice_distances = np.sqrt(dx**2 + dy**2)
        masque_zero = (self.matrice_distances == 0)
        self.matrice_distances[masque_zero] = 1.0
        
        attraction = 1.0 / (self.matrice_distances**2)
        np.fill_diagonal(attraction, 0.0)
        somme_lignes = attraction.sum(axis=1, keepdims=True)
        self.matrice_proba_inter = attraction / somme_lignes
    
    
    def PMB(self):
        """
        Calcule le PMB (Produit Mondial Brut) qui est la somme de tous les PUB
        
        Return : 
            (float) PMB
        """
        return sum([ville.get_pub_effectif() for ville in self.villes.values()])
    
    
            
            
class Virus:
    
    def __init__(self, nom, t_incubation, d_contagion, mortalite, p_immunite, R0):
        """
        Initialise l'objet virus
        
        Args : 
            nom (str) : nom du virus
            t_incubation (float) : période d'incubation
            d_contagion (float) : période de contagion
            mortalite (float) : taux de mortalite
            p_immunite (float) : duree de l'immunite 
            R0 (float) : nombre de reproduction de base

        """
        self.nom = nom
        self.alpha = 1/t_incubation
        self.gamma = 1/d_contagion
        self.beta = R0*self.gamma
        self.mu = mortalite
        if p_immunite == 0:
            self.delta = 0 
        else:    
            self.delta = 1/p_immunite



class MesureSanitaireEconomique:
    
    def __init__(self, nom, cout, alpha, beta, gamma, mu, delta, phi, delai, impact_politique):
        """
        Initialise une mesure sanitaire et économique appliquée à une ville spécifique.
        
        Args:
            nom (str): Nom de la mesure (ex: "Port du masque", "Confinement").
            cout (int): Coût financier ou politique de l'action.
            alpha, beta, gamma, mu, delta, phi (float): Coefficients d'impact sur les paramètres du modèle.
            delai (int) : nombre de jours avant que la mesure passe de l'état en cours d'activation à l'état active
            impact_politique (float) : Coût ou bonus politique de la mesure 
        """
        self.nom = nom
        self.cout = cout
        self.cout_init = cout
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.mu = mu
        self.delta = delta
        self.phi = phi
        self.delai = delai
        self.impact_politique = impact_politique # Compris entre 0 et 1
        self.duree_activation = 0
        
        
    def ajouter_ville(self, ville) :
        """
        Associe la mesure à une ville.
        
        Args : 
            ville (Ville) : ville à laquelle on associe la mesure
        """
        self.ville = ville 
        self.villes_affectees = ville
    
    
    def copy(self):
        """
        Réalise une copie de l'objet mesure qui est manipulé
        
        Return : 
            (MesureSanitaireEconomique) copie de la mesure
        """
        return MesureSanitaireEconomique(self.nom, self.cout, self.alpha, self.beta, self.gamma, self.mu, self.delta, self.phi, self.delai, self.impact_politique)



class MesureSoutien(MesureSanitaireEconomique):
    
    def __init__(self, nom, cout, alpha, beta, gamma, mu, delta, phi, rayon, Reseau, delai, impact_politique):
        """
        Initialise une mesure de soutien qui rayonne sur les villes aux alentours.
        
        Args:
            nom (str): Nom de la mesure (ex: "Usines", "Base militaire").
            cout (int): Coût de la mesure.
            ville (Ville): Objet de type Ville où est construite/appliquée la mesure.
            alpha, beta, gamma, mu, delta, phi (float): Coefficients d'impact.
            delai (int) : nombre de jours avant que la mesure passe de l'état en cours d'activation à l'état active
            impact_politique (float) : Coût ou bonus politique de la mesure 
            rayon (int): Distance cartésienne maximale d'impact de la mesure.
            Reseau (Reseau) : objet Reseau du jeu
        """
        super().__init__(nom, cout, alpha, beta, gamma, mu, delta, phi, delai, impact_politique)
        self.rayon = rayon
        self.Reseau = Reseau
        
        
    def ajouter_ville(self, ville):
        """
        Associe la mesure à une ville.
        
        Args : 
            ville (Ville) : ville auquel on associe la mesure
        """
        self.ville = ville


    def get_villes_affectees(self):
        """
        Parcourt toutes les villes du réseau et renvoie la liste de celles qui se trouvent
        à une distance cartésienne strictement inférieure au rayon d'action.
        """
        self.villes_affectees = []
        villes = list(self.ville.Reseau.villes.values()) # Creation d'une liste d'objets ville
        i_ville = villes.index(self.ville)
        
        for i in range(len(villes)):
            if self.ville.Reseau.matrice_distances[i][i_ville] < self.rayon:
                self.villes_affectees.append(villes[i])
        
        self.villes_affectees.remove(self.ville)
        
    
    def modif_villes_affectees(self, nom_mesure):
        """ 
        Modifie les mesures associées à la mesures de soutien dans les villes affectées
        
        Args : 
            nom_mesure (str) : nom de la mesure de soutien 
        """
        self.get_villes_affectees()
        for ville in self.villes_affectees:  
           if self.nom == "Base militaire" :
                ville.dico_mesures_ville["Confinement"]["mesure"].beta *= self.beta
                ville.dico_mesures_ville["Quarantaine"]["mesure"].beta *= self.beta
           if self.nom == "Usines" :
                facteur_cout = 0.7
                ville.dico_mesures_ville["Port du masque"]["mesure"].cout *= facteur_cout
                ville.dico_mesures_ville["Développement hôpitaux"]["mesure"].cout *= facteur_cout
                ville.dico_mesures_ville["Port du masque"]["mesure"].beta *= self.beta
                ville.dico_mesures_ville["Développement hôpitaux"]["mesure"].beta *= self.beta
    
    
    def copy_soutien(self):
        """
        Réalise une copie de l'objet mesure de soutien
        
        Return : 
            (MesureSanitaireEconomique) copie de la mesure
        """
        return MesureSoutien(self.nom, self.cout, self.alpha, self.beta, self.gamma, self.mu, self.delta, self.phi, self.rayon, self.Reseau, self.delai, self.impact_politique)
            


class MesureVaccin(MesureSanitaireEconomique) : 

    def __init__(self, nom, cout, alpha, beta, gamma, mu, delta, phi, delai, impact_politique, variations):
        """
        Initialise la mesure "Recherche d'un vaccin"
        
        Args:
            nom (str): Nom de la mesure (ex: "Usines", "Base militaire").
            cout (int): Coût de la mesure.
            ville (Ville): Objet de type Ville où est construite/appliquée la mesure.
            alpha, beta, gamma, mu, delta, phi (float): Coefficients d'impact.
            delai (int) : nombre de jours avant que la mesure passe de l'état en cours d'activation à l'état active
            impact_politique (float) : Coût ou bonus politique de la mesure 
            variations (tuple de float) : liste de facteurs associés aux différentes étapes de "Recherche d'un vaccin"
            
        """
        super().__init__(nom, cout, alpha, beta, gamma, mu, delta, phi, delai, impact_politique)
        self.etape = 0 # Au debut, la mesure n'est pas mise en place 
        self.gamma_init = gamma
        self.mu_init = mu 
        self.delta_init = delta 
        self.faible, self.moyen_faible, self.moyen = variations
        self.active = 0 # Au debut, la mesure n'est pas en cours d'activation
        self.delai_restant = delai
        

    def activation(self):
        """
        Modifie l'état de MesureVaccin : la mesure est maintenant en cours d'activation
        """
        self.active = 1 # Mesure en cours d'activation
        
        
    def maj_etape(self, nb_jours):
        """
        Met à jour l'etape de la mesure Recherche d'un vaccin en fonction du nombre de jours passés
        
        Args : 
            nb_jours (int) : nombre de jours passés
        """
        if self.active == 1 :
            self.delai_restant -= nb_jours
            
        if self.delai_restant <= 0 :
            self.etape += 1 
            self.delai_restant = self.delai
            self.active = 0
        
        
    def maj_parametres(self, dico_mesures):
        """
        Met à jour les parametres de la recherche de vaccin et de campagne de vaccination en fontion de l'etape
        
        Args : 
            dico_mesures (dict) : dictionnaire de l'ensemble des mesures du jeu {"nom_mesure" : mesure(objet mesure)}
        """
        if self.etape == 1 :
            self.delta = self.delta_init*(1 - self.faible)
            self.mu = self.mu_init*(1 - self.faible)
            self.gamma = self.gamma_init*(1 + self.faible)
            dico_mesures["Campagne de vaccination"].delta = self.delta
            dico_mesures["Campagne de vaccination"].mu = self.mu
            dico_mesures["Campagne de vaccination"].gamma = self.gamma
            
        elif self.etape == 2 :
            self.delta = self.delta_init*(1 - self.moyen_faible)
            self.mu = self.mu_init*(1 - self.moyen_faible)
            self.gamma = self.gamma_init*(1 + self.moyen_faible)
            dico_mesures["Campagne de vaccination"].delta = self.delta
            dico_mesures["Campagne de vaccination"].mu = self.mu
            dico_mesures["Campagne de vaccination"].gamma = self.gamma
            
        elif self.etape == 3 :
            self.delta = self.delta_init*(1 - self.moyen)
            self.mu = self.mu_init*(1 - self.moyen)
            self.gamma = self.gamma_init*(1 + self.moyen)
            dico_mesures["Campagne de vaccination"].delta = self.delta
            dico_mesures["Campagne de vaccination"].mu = self.mu
            dico_mesures["Campagne de vaccination"].gamma = self.gamma
            
        elif self.etape == 4 :
            self.delta = 0
            self.mu = 0
            self.gamma = 1
            dico_mesures["Campagne de vaccination"].delta = self.delta
            dico_mesures["Campagne de vaccination"].mu = self.mu
            dico_mesures["Campagne de vaccination"].gamma = self.gamma
            


class Dico_mesure:

    def __init__(self, Reseau, variations, couts, couts_politiques, facteurs_vaccin, rayon):
        """
        Initialise le dictionnaire d'objets mesure global au jeu

        Args :
        variations (tuple de float) : facteurs de modifications des parametres alpha, beta, gamma, mu, delta, phi
            les facteurs sont compris entre 0 et 1
        couts (tuple d'entiers) : couts monetaires associés aux mesures (faible, faible-moyen, moyen et eleve) 
        couts_politiques (tuple de float) : couts politiques associés aux mesures (faible, moyen, moyen-fort, fort et tres fort) 
            les couts sont compris entre 0 et 1 (la popularite est comprise entre 0 et 1)
        Reseau (Reseau) : reseau du jeu
        facteurs_vaccin (tuple de float): facteurs de modifications des parametres alpha, beta, gamma, mu, delta, phi specialement liés à la mesure recherche de vaccin
            les facteurs sont compris entre 0 et 1
        """
        self.Reseau = Reseau
        
        self.dico_mesures = {}
                                                                            # nom, cout, alpha, beta, gamma, mu, delta, phi, delai, impact_politique
        self.dico_mesures["Port du masque"] = MesureSanitaireEconomique("Port du masque", -couts[0], 1, 1 - variations[0], 1, 1, 1, 1 - variations[0], 0, -couts_politiques[0])
        self.dico_mesures["Développement hôpitaux"] = MesureSanitaireEconomique("Développement hôpitaux", 1 - couts[2], 1, 1, 1 + variations[0], 1 - variations[0], 1 - variations[0], 1, 0, couts_politiques[0])
        self.dico_mesures["Confinement"] = MesureSanitaireEconomique("Confinement", -couts[3], 1, 1 - variations[2], 1, 1, 1 - variations[1], 1 - variations[4], 4, -couts_politiques[3])
        self.dico_mesures["Quarantaine"] = MesureSanitaireEconomique("Quarantaine", -couts[3], 1, 1 - variations[4], 1, 1, 1, 0, 0, -couts_politiques[4])
        self.dico_mesures["Campagne de prévention"] = MesureSanitaireEconomique("Campagne de prévention", -couts[1], 1, 1 - variations[1], 1, 1, 1, 1, 3, couts_politiques[0])
        self.dico_mesures["Boost économique"] = MesureSanitaireEconomique("Boost économique", -couts[2], 1, 1 + variations[2], 1, 1, 1, 1 + variations[4], 0, couts_politiques[2])

        self.dico_mesures["Usines"] = MesureSoutien("Usines", -couts[2], 1, 1 - variations[2], 1, 1, 1, 1 + variations[0] , rayon, Reseau, 4, couts_politiques[2])
        self.dico_mesures["Base militaire"] = MesureSoutien("Base militaire", -couts[3], 1, 1 - variations[0] , 1, 1, 1, 1, rayon, Reseau, 0, - couts_politiques[3])
        
        self.dico_mesures["Recherche d'un vaccin"] = MesureVaccin("Recherche d'un vaccin", -couts[3] , 1, 1, 1, 1, 1, 1 + variations[0], 10, couts_politiques[2] , facteurs_vaccin)
        self.dico_mesures["Campagne de vaccination"] = MesureSanitaireEconomique("Campagne de vaccination", -couts[2], 1, 1, 1, 1, 1, 1 + variations[0] , 0, couts_politiques[0])
    
    
    def init_dico_mesures_ville(self) : 
        """
        Initialise le dictionnaire dico_mesures_ville dans toutes les villes à partir des mesures initialisées dans dico_mesures (dictionnaire de l'ensemble des mesures du jeu)
        """
        for nom_ville, ville in self.Reseau.villes.items() :
            ville.get_dico_mesures_ville(self.dico_mesures)
            ville.dico_mesures = self.dico_mesures
        
        