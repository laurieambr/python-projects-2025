# Mini-Projet Python #3 : Visualisation de performances de stratégie

## Objectif pédagogique

- Apprendre à utiliser `matplotlib` ou `plotly` pour créer des graphiques
- Visualiser les résultats de backtests (stratégie RSI ou autre)
- Rendre les analyses **présentables** (portfolio, SaaS, contenu)

## Étapes du projet

### Bloc 1 – Lecture des données

- Charger le fichier de résultats
- Vérifier que les colonnes importantes sont bien là :
  - Date, Gain/Perte, Capital, Type de trade...

### Bloc 2 – Graphique d’évolution du capital

- Afficher une **courbe de capital** avec `plt.plot()` ou `plotly.line()`
- Ajouter titres, axes, légendes
- Mettre en avant les pics et les drawdowns

### Bloc 3 – Résumé des performances

- Histogramme :
  - Nombre de trades gagnants vs perdants
  - RR moyen par trade
- Pie chart :
  - Pourcentage de réussite
  - Répartition des setups si disponibles

### Bloc 4 – Affichage global

- Créer une fonction `afficher_performance(df)`
- Sauvegarder les graphiques en `.png` (optionnel)
- Ajouter un résumé texte automatique avec :
  - Nombre de trades
  - Winrate
  - Gain total