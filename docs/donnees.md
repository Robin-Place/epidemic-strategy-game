# Formats des données

Les CSV historiques sont lus avec l'encodage Windows-1252 (`cp1252`), le séparateur `;` et sans ligne d'en-tête.

## Villes du jeu

Nom attendu : `Worldcities - Données Villes 2.csv` (espace avant `2`). Chaque ligne contient douze colonnes :

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

Le programme charge les vingt premières villes. La date et la source initiale des valeurs économiques restent à documenter.

## Virus

`Worldcities - Données Virus 3.csv` contient : nom, niveau descriptif, période d'incubation, durée de contagion, mortalité sous la forme `0.50%`, période d'immunité et R0.

Les noms sont utilisés par les boutons de sélection du jeu et doivent rester cohérents avec le CSV.

## Étude de complexité

`Worldcities - Données Villes_2.csv` (soulignement avant `2`) contient quatre colonnes : nom, latitude, longitude et population. Il sert à `Calculs_complexite.py` et ne fournit pas les données économiques et nationales du jeu.

## Carte

`carte_monde.png` est utilisée comme fond de carte et redimensionnée aux dimensions du canevas. Son origine et ses conditions de redistribution restent à documenter.

