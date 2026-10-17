"""Vérification des lecteurs avec des lignes représentatives des formats CSV."""

from pathlib import Path
import tempfile
import unittest

from Programme_principal import lire_donnees_villes, lire_donnees_virus


class TestDonnees(unittest.TestCase):
    def test_ordre_des_colonnes_population_et_pib(self):
        with tempfile.TemporaryDirectory() as dossier:
            p = Path(dossier) / "villes.csv"
            p.write_text("Ville Démo;Pays;1000;10.5;-20.5;5000000000;250000;XX;XXX;12345;Alpha;20\n", encoding="cp1252")
            pays, villes = lire_donnees_villes(p, nb_villes=1)
            self.assertEqual(pays["Pays"].population, 250000)
            self.assertEqual(pays["Pays"].PIB, 5000000000)
            self.assertEqual(villes["Ville Démo"].PUB, 12345)
            self.assertEqual(villes["Ville Démo"].lat, 10.5)

    def test_parametres_virus_et_pourcentage(self):
        with tempfile.TemporaryDirectory() as dossier:
            p = Path(dossier) / "virus.csv"
            p.write_text("Virus Démo;Facile;2;7;0.50%;10;7\n", encoding="cp1252")
            virus = lire_donnees_virus(p)["Virus Démo"]
            self.assertAlmostEqual(virus.alpha, .5)
            self.assertAlmostEqual(virus.mu, .005)
            self.assertAlmostEqual(virus.beta, 1.)


if __name__ == "__main__":
    unittest.main()
