# Guide du jeu

Ce guide reprend l'ancien README du projet et les règles présentes dans le code. Le joueur cherche à contenir une épidémie dans un réseau de grandes villes, en gérant son budget et sa popularité.

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
- **Boost économique** : modifie le revenu de la ville.
- **Usines** et **base militaire** : appliquent des effets de soutien dans un rayon autour de la ville.

Les mesures combinent coûts, effets sur les paramètres, popularité et délais d'activation. L'ancien README est un document de conception ; les valeurs exactes et certains comportements doivent être vérifiés dans le code et par une partie de démonstration.

## Recherche du vaccin

La recherche est accessible depuis la fenêtre principale. Elle se déroule en quatre étapes. Le code prévoit un délai avant la progression effective et applique les effets de la recherche par l'intermédiaire des paramètres de vaccination.

## Budget et popularité

Le budget comprend un stock disponible et des revenus calculés à partir des villes, de leurs populations encore actives et des mesures appliquées. La popularité est une ressource globale, qui influe sur le coût et la disponibilité de certaines mesures.

Le guide historique décrit plusieurs seuils de popularité. La version du dépôt conserve la logique existante ; une vérification complète des seuils et des actions reste distincte des tests du modèle.

## Fin de partie

Le code déclare une défaite si la population infectée atteint 75 % de la population de référence, si les décès atteignent 25 %, ou si la popularité tombe à zéro. Ces contrôles précèdent les contrôles de victoire.

La recherche vaccinale arrivée à l'étape 4 peut déclencher une victoire. À partir du jour 100, le code vérifie également si la proportion d'infectés reste sous 25 %, sous réserve des conditions de défaite déjà contrôlées.

## Pour comprendre le projet

Voir [la conception et l'optimisation](conception-et-optimisation.md) et le [rapport universitaire original](rapport-projet.pdf).

Ce jeu est un modèle pédagogique. Les paramètres et effets des mesures sont ceux du jeu, sans valeur de prévision épidémiologique.

