# Jeu de stratégie : contenir une épidémie

**Limiter la propagation d'un virus entre des villes en arbitrant entre mesures sanitaires, budget et popularité.**

Projet informatique collectif réalisé à l'INSA Lyon, en équipe de cinq étudiants. Le jeu associe un modèle de propagation à une interface graphique au tour par tour.

**Python · Tkinter · NumPy · Matplotlib · Pillow · programmation orientée objet · MVC**

## Principe du jeu

Une épidémie apparaît dans une ville et menace de se propager à l'ensemble du réseau mondial.
Le joueur organise la réponse en choisissant les mesures sanitaires et économiques à appliquer dans chaque ville.
À chaque tour, il décide du nombre de jours écoulés et doit arbitrer entre limitation des contaminations, coût des interventions et maintien de la popularité.
Les investissements locaux peuvent renforcer les mesures dans les villes voisines, tandis que la recherche fait progresser le développement d'un vaccin.
Deux voies permettent de gagner : contenir l'épidémie pendant 100 jours ou achever les quatre étapes de la recherche vaccinale et leurs délais, tout en préservant la population et la popularité.

- Carte interactive et informations sur les villes.
- Modèle à compartiments **SEIRD** : sains, exposés, infectés, rétablis et décédés.
- Propagation au sein des villes et entre les villes du réseau.
- Mesures sanitaires et économiques avec coûts et délais d'activation.
- Suivi du budget, de la popularité, des populations touchées et de la recherche vaccinale.
- Outils d'analyse par ville : coefficients effectifs des mesures, courbes de propagation et carnet de bord.

Voir [le guide du jeu](docs/guide-du-jeu.md) pour le déroulement d'une partie et les conditions de victoire.

## Conception et optimisation

Le projet comprend une évolution du découpage MVC, une hiérarchie de mesures et une étude de complexité de la propagation. La seconde version remplace les recherches répétées de positions dans les listes par des indices de matrice pré-calculés.

Le rapport compare les versions selon le nombre de villes, la durée simulée et les virus. Il met en évidence des compromis entre coût de calcul et précautions numériques, ainsi que des limites sur les grands réseaux.

Voir [la conception et l'optimisation](docs/conception-et-optimisation.md) et [le rapport universitaire original](docs/rapport-projet.pdf).

## Contribution et équipe

**Robin PLACE : contribution transversale au développement de l'application**, dans le cadre du travail collectif de l'équipe.

Le projet a été réalisé avec **Seymour LOI, Juliette Herr-Peyrot, Emilie LESOMMERE et Mai-Linh Duong**.

## Installation et lancement

Environnement de référence : **Python 3.12**, avec Tkinter. Les versions utilisées pour la vérification sont fixées dans `requirements.txt`.

```sh
git clone https://github.com/Robin-Place/epidemic-strategy-game.git
cd epidemic-strategy-game
python -m venv .venv
```

Activer l'environnement avec `.venv\Scripts\Activate.ps1` sous PowerShell, ou `source .venv/bin/activate` sous Linux/macOS, puis :

```sh
python -m pip install -r requirements.txt
python lancer.py
```

Les données nécessaires au jeu et le fond de carte sont fournis à la racine du dépôt. Voir [les formats et les sources des données](docs/donnees.md).

Si Tkinter manque, vérifier son installation avec `python -m tkinter`. Il est fourni par l'installateur officiel Python pour Windows et peut nécessiter le paquet système `python3-tk` sous Linux.

## Organisation du code

- `Modele.py` : pays, villes, réseau, virus et mesures.
- `Vue.py` : carte, fenêtres et graphiques.
- `Controleur.py` : initialisation et règles de fin de partie.
- `Interface_MC.py` : propagation, monnaie et popularité.
- `Programme_principal.py` : lecture des données et assemblage.
- `ConvertisseurDeCoordonnees.py` : conversion des coordonnées géographiques.
- `Calculs_complexite.py` : script expérimental d'étude des temps de calcul.
- `tests/` : tests automatisés du modèle.

Le découpage suit une organisation inspirée de MVC. Certaines dépendances entre logique et affichage demeurent.

## Vérifications et limites

```sh
python -m unittest discover -s tests -v
```

Les tests contrôlent les probabilités de connexion, les délais des mesures et l'effet des populations malades et décédées sur le revenu. Les données originales ne sont pas nécessaires à ces tests.

Le rapport conserve les mesures expérimentales du projet ; elles n'ont pas été reproduites lors de la préparation de cette version.

Ce jeu utilise un modèle pédagogique et des paramètres de jeu. Il ne constitue pas un outil de prévision épidémiologique. Les prolongements possibles sont la séparation plus complète entre modèle et interface, des scénarios reproductibles avec graine aléatoire et des tests couvrant des parties entières.

## Crédits et licence

Les auteurs du projet sont les cinq membres de l'équipe cités plus haut. Merci à **Carole FRINDEL**, enseignante à l'INSA Lyon, pour son aide dans l'organisation du projet.

Le code est disponible sous [licence MIT](LICENSE). Les ressources externes conservent leurs conditions d'utilisation propres. Voir [les crédits et la licence](docs/credits-et-licence.md).
