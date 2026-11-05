# Plan de travail de la mission anti-churn

Ce plan détaille la production des livrables attendus par Nadia Ferrand pour Pattes & Papilles, la répartition des rôles entre les agents de la fabrique et les critères de complétion associés.

## Ordre d'exécution de la fabrique

La chaîne de production suit cinq étapes séquentielles :

1. Analyse de données : extraction des chiffres réels et production des premiers visuels.
2. Stratégie : qualification des segments, définition du plan d'action et cadrage des recommandations individuelles.
3. Production des livrables finaux : rédaction du dossier et des messages, conception de la présentation interactive.
4. Contrôle et relecture : vérification arithmétique et conformité éditoriale bloquantes.
5. Clôture : établissement du bilan et transmission des arbitrages.

## Livrables demandés par le client

### 1. Diagnostic chiffré du churn

- Agent producteur : analyste
- Fichiers attendus :
  - `chantier/analyse/analyse.py`
  - `chantier/analyse/chiffres.md`
  - 4 à 6 graphiques PNG dans `chantier/analyse/`
- Critères de fin :
  - Le script Python s'exécute sans erreur sur les données de `donnees/`.
  - Le taux de churn global et par mois est calculé avant et après le 1er mars 2026.
  - La décomposition du churn couvre le canal d'acquisition, l'espèce, la formule et la remise de bienvenue.
  - Les signaux précurseurs (livraisons sautées, retards, tickets support, notes d'avis) et les motifs déclarés sont isolés.
  - Le chiffre d'affaires perdu sur les douze derniers mois est calculé.
  - Chaque chiffre clé de `chiffres.md` mentionne le fichier source et la formule de calcul exacte.
  - Chaque graphique PNG respecte la palette de la charte (vert sapin `#1E4636`, crème `#FBF5EC`, terracotta `#D9734E`, moutarde `#E8B04B`) et comporte un titre formulant une conclusion explicite.

### 2. Tableau de bord interactif

- Agent producteur : analyste
- Fichier attendu : `chantier/livrables/tableau-de-bord.html`
- Critères de fin :
  - Le fichier est autonome, consultable localement dans un navigateur sans serveur applicatif.
  - L'interface reprend la charte graphique de la marque (polices Fraunces et Inter, palette officielle).
  - Les visualisations (intégrées en base64 ou via Chart.js) sont accompagnées d'un commentaire synthétique expliquant le constat opérationnel.
  - Aucune erreur console ni ressource locale manquante à l'ouverture.

### 3. Recommandations et messages personnalisés pour 20 abonnés à risque

- Agents producteurs :
  - stratège pour le ciblage et la logique d'action
  - rédacteur pour les textes finaux
- Fichiers attendus :
  - `chantier/recommandations.md` (stratège)
  - `chantier/livrables/messages-abonnes.md` (rédacteur)
- Critères de fin :
  - `chantier/recommandations.md` détaille pour chaque profil de `donnees/abonnes_support.csv` le signal détecté, l'action retenue et le produit proposé issu strictement du catalogue d'automne 2026.
  - `chantier/livrables/messages-abonnes.md` contient exactement vingt messages personnalisés.
  - Chaque message nomme l'animal par son prénom, s'adresse au client avec vouvoiement et propose une démarche unique et concrète.
  - Aucune allégation médicale ou curative n'est présente.
  - Aucune remise tarifaire inventée n'est mentionnée.
  - Le style respecte la charte éditoriale et les consignes de rédaction humaine.

### 4. Business case et plan d'action

- Agents producteurs :
  - stratège pour la modélisation économique et le plan d'action
  - rédacteur pour l'intégration dans le document de synthèse
- Fichiers attendus :
  - `chantier/strategie.md` (stratège)
  - `chantier/livrables/dossier.md` (rédacteur)
- Critères de fin :
  - Trois à cinq segments à risque sont quantifiés avec des volumes issus exclusivement de `chiffres.md`.
  - Le plan d'action est découpé par horizon temporel : semaine 1, mois 1, trimestre 1.
  - Le modèle économique présente un scénario prudent et un scénario central.
  - Chaque dépense et chaque gain prévisionnel s'appuie sur une hypothèse explicitée avec son origine.
  - Le dossier complet respecte le plan imposé (constat chiffré, segments, plan d'action, business case, répartition IA/humain, limites et risques).

### 5. Présentation pour le comité de direction

- Agent producteur : designer
- Fichier attendu : `chantier/livrables/presentation.html`
- Critères de fin :
  - Présentation de 8 à 10 diapositives dans un unique fichier HTML navigable au clavier.
  - Respect strict de la charte visuelle (fond crème, typographies Fraunces et Inter).
  - Un message clé par écran formulé dans un titre conclusif.
  - Densité textuelle limitée à 30 mots par diapositive hors graphiques.
  - Intégration d'une diapositive dédiée précisant les apports respectifs de l'IA et les validations humaines requises.

## Étapes de contrôle et de clôture

### Contrôle des chiffres (bloquant)

- Agent responsable : contrôleur des chiffres
- Fichiers attendus :
  - `chantier/controle/controle.py`
  - `chantier/controle.md`
- Critères de fin :
  - Recalcul indépendant de l'ensemble des chiffres cités dans le dossier, la présentation et la stratégie.
  - Tableau comparatif systématique : chiffre cité, chiffre recalculé, écart, fichier source.
  - Mention finale unique `VERDICT : OK` si les écarts sur les chiffres clés sont inférieurs à 2 %, ou `VERDICT : A CORRIGER`.

### Relecture éditoriale (bloquante)

- Agent responsable : relecteur
- Fichier attendu : `chantier/relecture.md`
- Critères de fin :
  - Revue exhaustive de `messages-abonnes.md`, `dossier.md` et `presentation.html`.
  - Relevé précis de toute infraction aux règles dures (santé, remises, fuite de données internes), à la charte et aux consignes de rédaction humaine.
  - Mention finale unique `VERDICT : OK` ou `VERDICT : A CORRIGER`.

### Clôture et synthèse

- Agent responsable : chef de projet
- Fichier attendu : `chantier/bilan.md`
- Critères de fin :
  - Inventaire des livrables finalisés avec leurs chemins d'accès.
  - Relevé des points bloqués ou refusés lors des contrôles.
  - Formulation de trois enseignements pour faire évoluer les règles de l'usine.

## Arbitrages réservés à l'humain

Certains choix dépassent le cadre des données et exigent une décision formelle de Nadia Ferrand et de la direction :

1. Enveloppe budgétaire : quel montant global maximal Pattes & Papilles autorise-t-elle pour déployer le plan d'action anti-churn sur le dernier trimestre 2026 ?
2. Hypothèses économiques : quel taux de rétention cible le comité souhaite-t-il fixer pour le scénario central (ex. 15 % ou 20 % des abonnés en alerte sauvés) ?
3. Politique de compensation : l'entreprise autorise-t-elle des gestes commerciaux ciblés pour les clients victimes de retards de livraison répétés ou de la transition de recette saumon, et sous quelle forme exacte (avoir, sac d'essai gratuit, mois offert) ?
4. Gestion des incidents logistiques : la direction envisage-t-elle une révision contractuelle ou un changement de prestataire logistique suite aux anomalies constatées depuis mars 2026 ?
5. Modalités de contact : les vingt abonnés identifiés doivent-ils recevoir un e-mail direct rédigé au nom du service client ou un appel téléphonique d'un conseiller dédié ?
