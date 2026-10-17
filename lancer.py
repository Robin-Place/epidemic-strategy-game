"""Vérifie les ressources attendues avant de lancer le jeu universitaire."""

import argparse
import importlib.util
import os
from pathlib import Path
import runpy


ROOT = Path(__file__).resolve().parent
RESSOURCES = (
    "Worldcities - Données Villes 2.csv",
    "Worldcities - Données Virus 3.csv",
    "carte_monde.png",
)
MODULES = {"numpy": "NumPy", "matplotlib": "Matplotlib", "PIL": "Pillow", "tkinter": "Tkinter"}


def ressources_manquantes(dossier=ROOT):
    return [nom for nom in RESSOURCES if not (Path(dossier) / nom).is_file()]


def main(argv=None):
    parser = argparse.ArgumentParser(description="Jeu de gestion d'une épidémie.")
    parser.add_argument("--check", action="store_true", help="Vérifier les ressources et dépendances sans ouvrir le jeu.")
    args = parser.parse_args(argv)
    manquants = ressources_manquantes()
    modules = [label for nom, label in MODULES.items() if importlib.util.find_spec(nom) is None]
    if manquants or modules:
        if manquants:
            print("Fichiers à ajouter à la racine du dépôt :")
            for nom in manquants:
                print(f"  - {nom}")
        if modules:
            print("Dépendances manquantes : " + ", ".join(modules))
            print("Installer les paquets avec : python -m pip install -r requirements.txt")
            print("Tkinter est un composant de l'installation Python (voir README).")
        return 2
    if args.check:
        print("Ressources et modules présents. Cette vérification ne valide pas une partie complète.")
        return 0
    precedent = Path.cwd()
    try:
        os.chdir(ROOT)
        runpy.run_path(str(ROOT / "Programme_principal.py"), run_name="__main__")
    finally:
        os.chdir(precedent)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
