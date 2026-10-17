# Formats des données

Les CSV historiques sont lus avec l'encodage Windows-1252 (`cp1252`), le séparateur `;` et sans ligne d'en-tête.

## Villes du jeu

Nom attendu : `Worldcities - Données Villes 2.csv`. Chaque ligne contient douze colonnes :

1. Nom de la ville.
2. Nom du pays.
3. Population de la ville, entier.
4. Latitude, nombre décimal.
5. Longitude, nombre décimal.
6. PIB du pays, entier.
7. Population du pays, entier.
8. Code pays à deux lettres, non utilisé par le lecteur actuel.
9. Code pays à trois lettres.
10. PUB de la ville, entier utilisé comme ressource économique.
11. Statut de la ville.
12. Poids associé au statut, entier.

Le programme charge les vingt premières villes. La source indiquée par l'équipe pour les villes et leur classement est [World Cities 2024 — Globalization and World Cities Research Network (GaWC)](https://gawc.lboro.ac.uk/gawc-worlds/the-world-according-to-gawc/world-cities-2024/).

## Virus

`Worldcities - Données Virus 3.csv` contient : nom, niveau descriptif, période d'incubation, durée de contagion, mortalité sous la forme `0.50%`, période d'immunité et R0.

Les noms sont utilisés par les boutons de sélection du jeu et doivent rester cohérents avec le CSV.

## Étude de complexité

`Worldcities - Données Villes_2.csv` contient quatre colonnes : nom, latitude, longitude et population. Il sert uniquement à `Calculs_complexite.py` pour l'étude des temps de calcul et n'est pas nécessaire au lancement du jeu.

## Carte

`carte_monde.png` est utilisée comme fond de carte et redimensionnée aux dimensions du canevas. Cette image « libre de droits » provient de [Shutterstock](https://www.shutterstock.com/) et conserve sa licence d'origine ; elle n'entre pas dans le périmètre MIT du code. Voir [les crédits et la licence](credits-et-licence.md).

