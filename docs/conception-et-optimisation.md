# Conception et optimisation

Le [rapport universitaire](rapport-projet.pdf) documente l'évolution de l'architecture du jeu et l'étude des coûts de calcul. Il complète le code par des diagrammes et des observations expérimentales.

## Faire évoluer le découpage

Le découpage final spécialise les responsabilités :

- Les villes conservent leurs données, leurs historiques et leurs mesures locales.
- Le réseau prépare les matrices de distances et de poids de connexion.
- Les mesures sanitaires, de soutien et de vaccination sont représentées par des classes spécialisées avec héritage.
- La propagation, la monnaie et la popularité sont déléguées à des objets dédiés.
- L'interface comprend le choix de difficulté et de virus, les informations sur les villes, la recherche vaccinale, la fin de tour, la fin de partie et le carnet de bord.

Le rapport compare les schémas initial et final. Le code suit cette organisation inspirée de MVC, tout en conservant certaines dépendances entre modèle et affichage.

## Éviter les recherches répétées dans les listes

La première version de la propagation retrouve les positions des villes avec `list.index`. La seconde attribue à chaque ville un `id_matrice` utilisé pour accéder directement aux coefficients pré-calculés.

Le rapport analyse ainsi le coût du parcours entre villes comme passant de `O(I × V²)` à `O(I × V)`, avec `I` villes infectées et `V` villes au total, pour la partie liée aux recherches d'indices. C'est un exemple concret du rôle des structures de données dans les performances.

Cette analyse doit être lue dans le périmètre décrit par le rapport : d'autres opérations restent présentes dans le code complet, notamment les tests d'appartenance à la liste des villes infectées et la gestion des historiques. Elle ne suffit pas à garantir le coût total de tous les chemins d'exécution.

## Compromis dans l'intégration numérique

Le modèle intra-ville utilise Euler explicite. La seconde version remplace des créations répétées de petits tableaux par des variables scalaires et borne les compartiments entre 0 et 1.

Ce bornage limite certaines valeurs aberrantes, avec un coût supplémentaire. Il ne constitue pas une preuve générale de stabilité numérique ni de conservation de la population pour tous les paramètres.

## Ce que montrent les mesures du rapport

L'étude compare les deux versions selon le nombre de villes, la durée simulée et le type de virus, avec des classes simplifiées pour isoler les calculs.

- Sur l'axe de la durée, le rapport observe des temps approximativement linéaires et une version 2 environ 20 % plus lente.
- Sur l'essai par type de virus, pour 100 villes et 1 000 jours, il rapporte une version 1 environ 30 % plus lente que la version 2.
- Le rapport souligne aussi que les très grands réseaux peuvent produire des comportements incohérents ou des probabilités inter-villes devenues négligeables.

Ces pourcentages décrivent les mesures du rapport, pas des essais reproduits lors de la préparation de ce dépôt. Le matériel et le protocole ne permettent pas d'en faire une promesse de performance généralisable.

## Vérifications de la version du dépôt

Les tests ajoutés contrôlent des comportements du modèle : délais des mesures, revenu, probabilités du réseau, propagation et lecture des CSV. Une simulation sans interface a également été effectuée sur 20 villes pendant deux tours de cinq jours.

Ces vérifications ne valident pas une partie complète, toutes les interactions de l'interface ou le modèle sur de très grands réseaux.

## Sources du projet

Cette présentation s'appuie sur le rapport de six pages et l'ancien README fournis par Robin PLACE, ainsi que sur les fichiers Python du dépôt. Les commandes génériques GitLab présentes à la fin de l'ancien README n'ont pas été reprises : elles ne décrivaient pas le fonctionnement du jeu.

