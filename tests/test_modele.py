"""Tests du modèle sans interface et sans fichiers Worldcities."""

from pathlib import Path
from types import SimpleNamespace
import tempfile
import unittest

import numpy as np
from ConvertisseurDeCoordonnees import ConvertisseurDeCoordonnees
from Modele import Pays, Ville, Reseau, MesureSanitaireEconomique
from Modele import Virus
from Interface_MC import Propagation
from lancer import RESSOURCES, ressources_manquantes


def ville_test(nom="Demo", lat=0, lon=0):
    return Ville(nom, Pays("Fictif", 10000, 100000, "XX"), 1000, 100, "Test", 1, lat, lon)


class TestModele(unittest.TestCase):
    def test_propagation_conserve_la_population(self):
        ville = ville_test()
        ville.dico_mesures_ville = {}
        ville.sir = {"s": .995, "e": 0., "i": .005, "r": 0., "d": 0.}
        ville.historique = {"t": [1.], "S": [.995], "I": [.005], "D": [0.]}
        controleur = SimpleNamespace(jour=1)
        propagation = Propagation(controleur, Virus("Test", 2, 7, .005, 10, 7), ville)
        propagation.propagation_intra(ville, 5, "2")
        self.assertAlmostEqual(sum(ville.sir.values()), 1., places=10)
        self.assertTrue(all(0 <= valeur <= 1 for valeur in ville.sir.values()))
        self.assertEqual(len(ville.historique["t"]), len(ville.historique["I"]))

    def test_ville_sans_virus_ne_cree_pas_dinfection_spontanee(self):
        ville = ville_test()
        ville.dico_mesures_ville = {}
        ville.historique = {"t": [1.], "S": [1.], "I": [0.], "D": [0.]}
        propagation = Propagation(SimpleNamespace(jour=1), Virus("Test", 2, 7, .005, 10, 7), ville)
        propagation.propagation_intra(ville, 5, "2")
        self.assertEqual(ville.sir, {"s": 1., "e": 0., "i": 0., "r": 0., "d": 0.})

    def test_reseau_probabilites_et_population(self):
        villes = {nom: ville_test(nom, lat, lon) for nom, lat, lon in (("A", 10, 20), ("B", 40, 60), ("C", -20, -30))}
        reseau = Reseau(villes, ConvertisseurDeCoordonnees(1000, 500, 50, 30))
        self.assertEqual(reseau.pop_mondiale_ref, 3000)
        self.assertTrue(np.isfinite(reseau.matrice_proba_inter).all())
        np.testing.assert_allclose(reseau.matrice_proba_inter.sum(axis=1), np.ones(3))
        np.testing.assert_allclose(np.diag(reseau.matrice_proba_inter), np.zeros(3))
        self.assertTrue((reseau.matrice_proba_inter >= 0).all())

    def test_revenu_tient_compte_des_malades_et_decedes(self):
        ville = ville_test()
        ville.dico_mesures_ville = {}
        ville.sir = {"s": .3, "e": .1, "i": .2, "r": .1, "d": .3}
        self.assertAlmostEqual(ville.get_pub_effectif(), 50.)

    def test_mesure_activee_apres_delai(self):
        ville = ville_test()
        mesure = MesureSanitaireEconomique("Test", -10, 1, 1, 1, 1, 1, 1, 4, -.1)
        mesure.delai_restant = 4
        mesure.duree_activation = 8
        ville.dico_mesures_ville = {"Test": {"mesure": mesure, "etat": 2}}
        ville.actualiser_delais_mesures(4)
        self.assertEqual(ville.dico_mesures_ville["Test"]["etat"], 3)
        self.assertEqual(mesure.delai_restant, 0)
        ville.actualiser_delais_mesures(8)
        self.assertEqual(ville.dico_mesures_ville["Test"]["etat"], 1)

    def test_delai_depasse_ne_devient_pas_negatif(self):
        ville = ville_test()
        mesure = MesureSanitaireEconomique("Test", -10, 1, 1, 1, 1, 1, 1, 3, -.1)
        mesure.delai_restant = 3
        mesure.duree_activation = 4
        ville.dico_mesures_ville = {"Test": {"mesure": mesure, "etat": 2}}
        ville.actualiser_delais_mesures(10)
        self.assertEqual(mesure.delai_restant, 0)
        self.assertEqual(mesure.duree_activation, 0)
        self.assertEqual(ville.dico_mesures_ville["Test"]["etat"], 1)

    def test_ressources_manquantes_sont_identifiees(self):
        with tempfile.TemporaryDirectory() as dossier:
            self.assertEqual(ressources_manquantes(dossier), list(RESSOURCES))
            for nom in RESSOURCES:
                (Path(dossier) / nom).touch()
            self.assertEqual(ressources_manquantes(dossier), [])


if __name__ == "__main__":
    unittest.main()
