# MCTS et classe `Vertex`

Cette page décrit l’algorithme Monte-Carlo Tree Search (MCTS) du projet, ainsi que la classe `Vertex` qui représente les nœuds de son arbre de recherche.

## MCTS

Le MCTS estime la qualité des coups en répétant des simulations à partir de la position courante. Il ne parcourt donc pas systématiquement toutes les parties possibles.

Dans ManicMinelayers, un coup déplace un joueur vers une case vide selon l’un des huit déplacements en « L » du cavalier. La case quittée devient marquée et ne peut plus être occupée. Une partie se termine lorsqu’un joueur ne peut plus bouger; si les deux joueurs sont bloqués, le résultat est nul.

### Paramètres

```python
MCTS(
    game,
    iterations=200,
    exploration_weight=math.sqrt(2.0),
    rollout_depth=20,
)
```

| Paramètre | Valeur par défaut | Rôle |
|---|---:|---|
| `game` | — | Instance de `ManicMineLayers` utilisée pour obtenir l’état de départ. |
| `iterations` | `200` | Nombre de simulations effectuées pour choisir un coup. |
| `exploration_weight` | `sqrt(2)` | Poids du terme d’exploration dans le score UCB1. Une valeur élevée favorise davantage les coups peu explorés. |
| `rollout_depth` | `20` | Nombre maximal de coups joués au hasard lors d’une simulation. |

Le point d’entrée pour choisir un coup est :

```python
get_move(
    from_position: tuple[int, int],
    other_player_position: tuple[int, int],
) -> tuple[int, int] | None
```

La position de départ sert à identifier le joueur racine dans la copie de la partie. Le joueur adverse et les coups légaux sont ensuite déterminés à partir de l’état du jeu copié. La méthode renvoie la destination choisie, ou `None` si aucun coup n’est disponible. Elle ne modifie pas la partie originale.

Exemple d’utilisation avec les paramètres par défaut :

```python
algorithm = MCTS(game)
move = algorithm.get_move(player.position, opponent.position)
```

Il est aussi possible de remplacer les paramètres, par exemple :

```python
algorithm = MCTS(
    game,
    iterations=500,
    exploration_weight=1.4,
    rollout_depth=30,
)
```

Le CLI instancie actuellement `MCTS(game)` sans exposer ces paramètres. La commande de jeu existante permet de sélectionner MCTS comme joueur :

```sh
make play mcts stupidbot
```

### Étapes de la recherche

Pour chaque itération, l’algorithme :

1. **Sélectionne** des enfants déjà explorés tant que le nœud n’a plus de coups non essayés et n’est pas terminal.
2. **Développe** un coup non essayé en créant un nouvel état et un enfant dans l’arbre.
3. **Simule** une partie depuis ce nœud, en choisissant les coups au hasard jusqu’à la fin de partie ou jusqu’à `rollout_depth`.
4. **Rétropropage** le résultat vers le nœud racine et ses ancêtres.

La sélection utilise le score UCB1 :

```text
moyenne_des_récompenses + exploration_weight * sqrt(log(visites_parent) / visites_enfant)
```

Un enfant jamais visité reçoit temporairement un score infini afin d’être exploré. À la fin des itérations, le coup renvoyé est celui de l’enfant racine ayant le plus grand nombre de visites.

### Récompenses et limites actuelles

Les récompenses sont évaluées du point de vue du joueur racine : victoire `1.0`, défaite `0.0`, match nul `0.5`. Cette même récompense est ajoutée aux visites de chaque nœud du chemin de rétropropagation.

Une simulation encore en cours lorsqu’elle atteint la profondeur maximale reçoit également `0.5` : ce score neutre ne signifie pas nécessairement que la position est réellement un match nul.

**Limite d’implémentation à connaître :** pendant les simulations aléatoires, le joueur local change après chaque coup, mais `current_player` dans l’état simulé n’est pas synchronisé. Or `set_game_state()` consulte ce champ. Le statut calculé en cours de simulation, et donc certaines récompenses, peut alors être incorrect. Dans l’expansion de l’arbre, le statut est calculé avant le changement de `current_player`, tandis que l’évaluation du résultat intervient ensuite; l’interprétation du cas `CURRENT_WIN` peut aussi être incohérente. Ces points sont à corriger dans l’algorithme avant de se fier aux résultats comme à une évaluation exacte.

## Classe `Vertex`

Un `Vertex` est un nœud de l’arbre MCTS. Il conserve l’état de jeu représenté, son lien vers le parent, les enfants et les statistiques de recherche.

| Attribut | Description |
|---|---|
| `state` | État du jeu associé au nœud. |
| `parent` | Nœud parent, ou `None` pour la racine. |
| `move` | Coup ayant mené à ce nœud, ou `None` pour la racine. |
| `children` | Liste des nœuds enfants déjà développés. |
| `untried_moves` | Coups légaux du joueur courant qui n’ont pas encore été développés. |
| `visits` | Nombre de simulations rétropropagées à travers ce nœud. |
| `total_reward` | Somme des récompenses rétropropagées à travers ce nœud. |

À sa création, `Vertex` calcule `untried_moves` à partir du joueur courant et de sa position. Si l’état, le joueur courant ou la méthode `possible_moves` manque, cette liste est vide. La propriété `is_terminal` indique si l’état de jeu diffère de `GameState.ONGOING`. La méthode `add_child(child)` ajoute un enfant, et `repr(vertex)` fournit un résumé de ses statistiques.

La classe se trouve dans [`src/classes/vertex.py`](../src/classes/vertex.py); l’algorithme est dans [`src/classes/algorithms/mcts.py`](../src/classes/algorithms/mcts.py).
