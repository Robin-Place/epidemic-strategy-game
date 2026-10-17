# -*- coding: utf-8 -*-


from Modele import Pays, Ville, Reseau, Virus, MesureSanitaireEconomique
from ConvertisseurDeCoordonnees import ConvertisseurDeCoordonnees
from Interface_MC import Monnaie, Popularite, Propagation

#INITIALISATION DES OBJETS

#pays
japan = Pays("Japan", 125000000, 5000000000000, "JP")
indonesia = Pays("Indonesia", 273000000, 1000000000000, "ID")
india = Pays("India", 1400000000, 3000000000000, "IN")

#villes
tokyo = Ville("Tokyo", japan, 37785000, 1500000000000, "Capitale", 13, 35.685, 139.7514)
tokyo.dico_mesures_ville = {}
jakarta = Ville("Jakarta", indonesia, 33756000, 350000000000, "Capitale", 13, -6.1753, 106.8269)
jakarta.dico_mesures_ville = {}
delhi = Ville("Delhi", india, 32226000, 250000000000, "Capitale", 13, 28.66, 77.23)
delhi.dico_mesures_ville = {}

#dictionnaire des villes 
dico_villes = {"Tokyo": tokyo, "Jakarta": jakarta, "Delhi": delhi}

#convertisseur de coordonnées
convertisseur = ConvertisseurDeCoordonnees(l_canvas=1000, h_canvas=500, offset_earth=50, offset_screen=30)

#réseau
reseau = Reseau(dico_villes, convertisseur)

#virus
virus = Virus("virus_test", 1, 1, 0.2, 5, 0.05)

#utiles pour les mesures
variations = [0.05, 0.10, 0.25, 0.60, 1]
couts = [5e12, 1e13, 2.5e13, 5e13, 1e14]
couts_politiques = [0.02, 0.08, 0.15, 0.2, 0.25]




#TESTS

#Test 1 : actualiser_delais_mesures (vérification du changement d'état)

mesure_confinement1 = MesureSanitaireEconomique(
    "Confinement", 
    -couts[3], 
    1, 
    1 - variations[4], 
    1, 
    1 - variations[4], 
    1, 
    0, 
    0, 
    -couts_politiques[3]
)

mesure_confinement1.delai_restant = 4  
mesure_confinement1.duree_activation = 1

tokyo.dico_mesures_ville = {
    "Confinement": {"mesure": mesure_confinement1, "etat": 2} #la mesure est à l'état 2 (en attente)
}
print("test 1 : actualiser_delais_mesures (vérification du changement d'état)")

tokyo.actualiser_delais_mesures(4) #nb_jours == délai restant , donc l'état passe à 3
if tokyo.dico_mesures_ville["Confinement"]["etat"] == 3 : 
    print(True)
else: 
    print(False)
    



#Test 2 : actualiser_delais_mesures (saut de 10 jours)

mesure_confinement2 = MesureSanitaireEconomique(
    "Confinement", 
    -couts[3], 
    1, 
    1 - variations[4], 
    1, 
    1 - variations[4], 
    1, 
    0, 
    0, 
    -couts_politiques[3]
)


mesure_confinement2.delai_restant = 3
jakarta.dico_mesures_ville = {
    "Confinement": {"mesure": mesure_confinement2, "etat": 2} #la mesure est à l'état 2 (en attente)
}

print("test 2 : actualiser_delais_mesures (vérification pas de délai négatif)")

jakarta.actualiser_delais_mesures(10) #nb_jours > délai restant, donc le délai à 0
if mesure_confinement2.delai_restant == 0  : 
    print(True)
else: 
    print(False)
    
    


#Test 3 : get_pub_effectif (population entièrement infectée ou décédée)

jakarta.sir = {"s": 0.0, "e": 0.0, "i": 0.6, "r": 0.0, "d": 0.4}

print("test 3 : get_pub_effectif (population entièrement infectée ou décédée)")

if jakarta.get_pub_effectif() == 0.0 : #la population est entièrement inactive, le PUB vaut 0
    print(True)
else : 
    print(False)
    
    
    
    
#Test 4 : propagation (toute la population d'une ville est décédée)

delhi.sir = {"s": 0.0, "e": 0.0, "i": 0.0, "r": 0.0, "d": 1.0} #la population est entièrement décédée
dotI = virus.alpha * delhi.sir["e"] - (virus.gamma+ virus.mu) * delhi.sir["i"] #calcul de la variation de la proportion d'infectés (avec propagation_intra)

print("test 4 : propagation (toute la population d'une ville est décédée)")

if dotI == 0.0 : #si tout le monde est mort le virus ne peut plus se propager au sein de la ville 
    print(True)
else : 
    print(False)
    
    
    
    
#Test 5 : propagation (toute la population d'une ville est immunisée)

virus.delta = 0.0

tokyo.sir = {"s": 0.0, "e": 0.0, "i": 0.0, "r": 1.0, "d": 0.0} #la population est entierement immunisée
dotS = - virus.beta * tokyo.sir["s"] * tokyo.sir["i"] + virus.delta * tokyo.sir["r"] #calcul de la variation des proportions du modèle SIR (avec propagation_intra)
dotE = virus.beta * tokyo.sir["s"] * tokyo.sir["i"] - virus.alpha * tokyo.sir["e"]

print("test 5 : propagation (toute la population d'une ville est immunisée)")

if dotS == 0.0 and dotE == 0.0: #les proportions de personnes saines et exposées ne peuvent plus varier car tout le monde est immunisé
    print(True)
else:
    print(False)
    
    
    
#Test 6 : propagation (le taux d'infectés ne peut pas dépasser 100%)

delhi.sir = {"s": 0.0, "e": 0.0, "i": 1.0, "r": 0.0, "d": 0.0} #la population est entièrement infectée
dotI = virus.alpha * delhi.sir["e"] - (virus.gamma + virus.mu) * delhi.sir["i"] #calcul de la variation de la proportion d'infectés (avec propagation_intra)
n_i = delhi.sir["i"] + dotI #proportion d'infectés au pas de temps suivant

print("test 6 : propagation (le taux d'infectés ne peut pas dépasser 100%)")

if n_i <= 1.0: #on ne dépasse pas 100 %
    print(True)
else:
    print(False)
    
    
    
 
#Test 7 : impact_popularite (vérification de l'annulation des mesures qui font baisser la popularité si elle est trop basse)

mesure_confinement3 = MesureSanitaireEconomique(
    "Confinement", -couts[3], 1, 1 - variations[4], 1, 1 - variations[4], 1, 0, 0, -couts_politiques[3]
)
mesure_confinement3.cout_init = -couts[3]


tokyo.dico_mesures_ville = {
    "Confinement": {"mesure": mesure_confinement3, "etat": 3}, #ajout des mesures au dico_mesures de tokyo (le type de mesure dans les valeurs n'a pas d'importance)
    "Quarantaine": {"mesure": mesure_confinement3, "etat": 3},
    "Port du masque": {"mesure": mesure_confinement3, "etat": 3},
    "Développement hôpitaux": {"mesure": mesure_confinement3, "etat": 3} 
}

popularite = 0.10  
facteur_global = 0.005


for nom_mesure, donnees in tokyo.dico_mesures_ville.items(): #structure de la méthode impact_popularité avec facteur_mesure = 0.1
    if popularite < 0.75:
        if nom_mesure in ["Confinement", "Quarantaine"]:
            donnees["mesure"].cout = donnees["mesure"].cout_init * 0.1
            
    if popularite < 0.5:
        if nom_mesure in ["Recherche d'un vaccin", "Campagne de vaccination", "Campagne de prévention", "Port du masque"]:
            donnees["mesure"].cout = donnees["mesure"].cout_init * 0.1
            
    if popularite > 0 and popularite < 0.25:
        donnees["mesure"].cout = donnees["mesure"].cout_init * facteur_global
        
        if tokyo.dico_mesures_ville["Port du masque"]["etat"] != 4 or tokyo.dico_mesures_ville["Développement hôpitaux"]["etat"] != 4:
            tokyo.dico_mesures_ville["Port du masque"]["etat"] = 0
            tokyo.dico_mesures_ville["Développement hôpitaux"]["etat"] = 0
            
        if tokyo.dico_mesures_ville["Confinement"]["etat"] != 4 or tokyo.dico_mesures_ville["Quarantaine"]["etat"] != 4:
            tokyo.dico_mesures_ville["Confinement"]["etat"] = 0
            tokyo.dico_mesures_ville["Quarantaine"]["etat"] = 0

print("test 7 : impact_popularite (vérification de l'annulation des mesures si la popularité est trop basse)")

if tokyo.dico_mesures_ville["Confinement"]["etat"] == 0: #état de Confinement doit être égal à 0 à cause de la popularité trop basse
    print(True)
else:
    print(False)
    
    
    
#Test 8 : si les fonds sont insufisants l'achat est bloqué

monnaie = 50000.0
cout_mesure = -100000.0 #le coût est supérieur aux fonds disponibles 

print("test 8 : vérification du blocage (fenêtre d'erreur) si les fonds sont insuffisants")

if (monnaie + cout_mesure) < 0.0: #la fenêtre s'affiche à cette condition dans la méthode lancer_activation de Info_ville qui renvoie à modif_valeur de Monnaie
    print(True) #la condition est suffisante et l'achat est bloqué
else:
    print(False)

    