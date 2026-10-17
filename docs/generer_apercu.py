"""Trace un scénario d'une ville avec le modèle du jeu, sans interface."""

from pathlib import Path
import sys
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from Programme_principal import lire_donnees_villes, lire_donnees_virus
from Interface_MC import Propagation


def main():
    _, villes = lire_donnees_villes(ROOT / "Worldcities - Données Villes 2.csv", nb_villes=20)
    ville = next(iter(villes.values()))
    virus = lire_donnees_virus(ROOT / "Worldcities - Données Virus 3.csv")["Grippe Saisonnière"]
    ville.dico_mesures_ville = {}
    ville.sir = {"s": .995, "e": 0., "i": .005, "r": 0., "d": 0.}
    ville.historique = {"t": [1.], "S": [.995], "I": [.005], "D": [0.]}
    propagation = Propagation(SimpleNamespace(jour=1), virus, ville)
    propagation.propagation_intra(ville, 100, "2")
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.subplots_adjust(left=.11, right=.97, bottom=.25, top=.78)
    fig.suptitle("Contenir une épidémie : le modèle en action", x=.08, ha="left", fontsize=20, fontweight="bold")
    ax.set_title(f"{ville.nom} · scénario sans intervention · paramètres de la grippe du jeu", loc="left", fontsize=11, pad=18)
    jours = np.asarray(ville.historique["t"]) - 1
    ax.plot(jours, np.asarray(ville.historique["I"]) * 100, color="#196e71", linewidth=2.8, label="Population infectée")
    ax.plot(jours, np.asarray(ville.historique["D"]) * 100, color="#656a73", linewidth=2.4, linestyle="--", label="Population décédée")
    ax.set(xlabel="Temps écoulé (jours)", ylabel="Part de la population de la ville (%)", xlim=(0, 100), ylim=(0, 100))
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", color="#e1e6e6", linewidth=.7)
    ax.legend(loc="upper right", frameon=False)
    fig.text(.08, .035, "Calcul avec Interface_MC.Propagation.propagation_intra, version 2 (SEIRD / Euler).\nUne seule ville, aucune propagation interville, aucune mesure ; 0,5 % d'infectés au départ.\nScénario pédagogique sur 100 jours. Illustration calculée, sans valeur de prévision épidémiologique.", fontsize=8, color="#5b6667")
    cible = ROOT / "docs" / "apercu-propagation.png"
    fig.savefig(cible, dpi=160, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(cible)


if __name__ == "__main__":
    main()
