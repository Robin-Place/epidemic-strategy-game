# Guide du jeu

Le joueur cherche à contenir une épidémie dans un réseau de grandes villes, en gérant son budget et sa popularité.

## Démarrer et jouer un tour

Après le lancement, choisir un niveau de difficulté puis un virus. La fenêtre principale affiche la carte, le budget, le nombre de jours et les indicateurs d'infection, de mortalité et de popularité.

Survoler une ville permet d'en consulter les informations. La sélectionner ouvre une fenêtre proposant ses mesures disponibles, ses statistiques et des outils pour comprendre la propagation : les coefficients effectifs et les courbes de population vivante, infectée et décédée.

À chaque tour :

1. Choisir les mesures locales et les investissements souhaités dans la limite des ressources disponibles.
2. Consulter les coûts, effets et délais.
3. Cliquer sur **Finir le tour** et choisir le nombre de jours à simuler.
4. Examiner la propagation, les ressources actualisées et le carnet de bord.

## Mesures locales

- **Port du masque** et **campagne de prévention** : agissent sur les paramètres de transmission.
- **Développement hôpitaux** : agit sur les paramètres de guérison et de mortalité.
- **Confinement** et **quarantaine** : réduisent la propagation avec des conséquences économiques et politiques.
- **Boost économique** : augmente le revenu de la ville, mais aussi ses paramètres de transmission ; le bénéfice économique s'accompagne donc d'un risque accru de propagation.
- **Usines** : renforcent les effets du port du masque et du développement des hôpitaux dans les villes situées dans leur rayon d'action, tout en réduisant le coût de ces mesures.
- **Base militaire** : renforce les effets du confinement et de la quarantaine dans les villes situées dans son rayon d'action.

Les mesures combinent coûts, effets sur les paramètres de propagation, popularité et délais d'activation. Consulter les informations d'une mesure avant de l'activer permet d'en évaluer les bénéfices et les contreparties.

## Recherche du vaccin

La recherche est accessible depuis la fenêtre principale et se déroule en quatre étapes, à financer successivement. Chaque étape nécessite un délai avant d'être achevée ; les progrès de la recherche améliorent les effets de la vaccination. Une fois les quatre étapes et leurs délais terminés, la recherche du vaccin permet de remporter la partie, à condition qu'aucune condition de défaite ne soit atteinte.

## Budget et popularité

Le budget comprend un stock disponible et des revenus calculés à partir des villes, de leurs populations encore actives et des mesures appliquées. La popularité est une ressource globale, qui influe sur le coût et la disponibilité de certaines mesures.

Une popularité faible rend certaines mesures plus coûteuses et peut en rendre d'autres indisponibles. Il faut donc surveiller cet indicateur autant que le budget et l'évolution de l'épidémie.

## Fin de partie

La partie est perdue si la population infectée atteint 75 % de la population de référence, si les décès atteignent 25 %, ou si la popularité tombe à zéro.

Deux objectifs permettent de remporter la partie :

- Achever les quatre étapes de recherche du vaccin et leurs délais.
- Atteindre le jour 100 avec moins de 25 % de la population infectée.

Dans les deux cas, les seuils de défaite doivent rester respectés. Si plusieurs seuils sont atteints au même tour, une condition de défaite prend le dessus sur un objectif de victoire.

## Pour comprendre le projet

Voir [la conception et l'optimisation](conception-et-optimisation.md) et le [rapport universitaire original](rapport-projet.pdf).

Ce jeu est un modèle pédagogique. Les paramètres et effets des mesures sont ceux du jeu, sans valeur de prévision épidémiologique.

