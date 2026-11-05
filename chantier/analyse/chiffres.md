# Référentiel des chiffres clés du churn

Document établi par l'agent analyste de données le 5 novembre 2026.  
Ce document constitue l'unique source de vérité chiffrée pour les agents stratège, rédacteur, designer et contrôleur.  
Conformément aux règles de l'usine, chaque donnée fait l'objet d'une traçabilité rigoureuse : fichier source, périmètre exact et formule de calcul.

---

## 1. Vue d'ensemble du churn et pertes financières

### 1.1 Taux de churn global et par formule

| Indicateur | Échantillon brut (2 000 lignes) | Base dédoublonnée (1 985 clients) | Fichier source | Méthode et formule de calcul |
|---|---|---|---|---|
| **Taux de churn global** | **32,35 %** (647 / 2 000) | **32,24 %** (640 / 1 985) | `donnees/customers.csv` | `churned.sum() / len(customers)` [Source : `donnees/customers.csv`] |
| **Taux de churn des abonnés** | **15,36 %** (200 / 1 302) | **15,24 %** (197 / 1 293) | `donnees/customers.csv` | Filtre `plan == 'subscription'`, `churned.sum() / count()` [Source : `donnees/customers.csv`] |
| **Taux de churn des achats ponctuels** | **64,04 %** (447 / 698) | **64,02 %** (443 / 692) | `donnees/customers.csv` | Filtre `plan == 'one_off'`, `churned.sum() / count()` [Source : `donnees/customers.csv`] |
| **Part des abonnés dans l'échantillon** | **65,10 %** (1 302 / 2 000) | **65,14 %** (1 293 / 1 985) | `donnees/customers.csv` | `(plan == 'subscription').sum() / len(customers)` [Source : `donnees/customers.csv`] |
| **Part des achats ponctuels** | **34,90 %** (698 / 2 000) | **34,86 %** (692 / 1 985) | `donnees/customers.csv` | `(plan == 'one_off').sum() / len(customers)` [Source : `donnees/customers.csv`] |

> [!NOTE]  
> Le fichier `donnees/customers.csv` comporte 2 000 lignes dont 15 doublons stricts (mêmes identifiants et caractéristiques). Les deux calculs (brut et dédoublonné) sont fournis ci-dessus pour assurer une cohérence arithmétique totale avec les contrôles. L'écart est infime (< 0,15 point).

---

### 1.2 Chiffre d'affaires perdu avec les clients partis

| Indicateur | Valeur calculée | Fichier source | Méthode et formule de calcul |
|---|---|---|---|
| **CA total 12 mois (échantillon)** | **810 532,63 € TTC** | `donnees/orders.csv` | Somme de `line_total_eur` pour les commandes du 01/07/2025 au 30/06/2026 inclus [Source : `donnees/orders.csv`] |
| **CA 12 mois des clients fidèles (churned = 0)** | **656 925,18 € TTC** (81,05 %) | `donnees/orders.csv` & `donnees/customers.csv` | Somme de `line_total_eur` des commandes 12 mois pour `churned == 0` (jointure dédoublonnée) [Source : `donnees/orders.csv`] |
| **CA 12 mois perdu avec les clients partis (churned = 1)** | **153 607,45 € TTC** (18,95 %) | `donnees/orders.csv` & `donnees/customers.csv` | Somme de `line_total_eur` des commandes 12 mois pour `churned == 1` (jointure dédoublonnée) [Source : `donnees/orders.csv`] |
| *-- dont CA perdu sur les abonnés* | **81 820,63 € TTC** (53,27 % du CA perdu) | `donnees/orders.csv` & `donnees/customers.csv` | Commandes 12 mois avec filtre `churned == 1` et `plan == 'subscription'` [Source : `donnees/orders.csv`] |
| *-- dont CA perdu sur les achats ponctuels* | **71 786,82 € TTC** (46,73 % du CA perdu) | `donnees/orders.csv` & `donnees/customers.csv` | Commandes 12 mois avec filtre `churned == 1` et `plan == 'one_off'` [Source : `donnees/orders.csv`] |
| **CA 12 mois perdu si jointure brute non dédoublonnée** | **155 080,48 € TTC** | `donnees/orders.csv` & `donnees/customers.csv` | Jointure directe avec la table `customers.csv` brute (duplication des lignes des 15 clients doublons) [Source : `donnees/orders.csv`] |
| **Total dépensé historique par les clients partis** | **324 108,30 € TTC** | `donnees/customers.csv` | Somme de `total_spent_eur` pour `churned == 1` sur l'ensemble de la vie client [Source : `donnees/customers.csv`] |
| *-- dont total historique abonnés partis* | **220 585,23 € TTC** (68,06 %) | `donnees/customers.csv` | Somme de `total_spent_eur` pour `churned == 1` et `plan == 'subscription'` [Source : `donnees/customers.csv`] |
| *-- dont total historique ponctuels partis* | **103 523,07 € TTC** (31,94 %) | `donnees/customers.csv` | Somme de `total_spent_eur` pour `churned == 1` et `plan == 'one_off'` [Source : `donnees/customers.csv`] |
| **Total dépensé historique par les clients conservés** | **1 710 170,09 € TTC** | `donnees/customers.csv` | Somme de `total_spent_eur` pour `churned == 0` [Source : `donnees/customers.csv`] |
| **Panier moyen historique - Clients conservés** | **68,54 € TTC** | `donnees/customers.csv` | Moyenne de `avg_basket_eur` pour `churned == 0` [Source : `donnees/customers.csv`] |
| **Panier moyen historique - Clients partis** | **64,88 € TTC** | `donnees/customers.csv` | Moyenne de `avg_basket_eur` pour `churned == 1` [Source : `donnees/customers.csv`] |

---

## 2. Analyse temporelle et choc du 1er mars 2026

Le 1er mars 2026, Pattes & Papilles a appliqué une hausse tarifaire de +5 % sur l'ensemble du catalogue, couplée au changement de transporteur le 2 mars 2026.

### 2.1 Churn selon la date d'inscription (Cohortes de recrutement)

| Période de recrutement (`signup_date`) | Nombre total de clients | Clients partis (`churned == 1`) | Taux de churn | Fichier source et formule |
|---|---|---|---|---|
| **Avant le 1er mars 2026** (Prix initial) | 1 633 | 455 | **27,86 %** | `signup_date < '2026-03-01'`, churn moyen [Source : `donnees/customers.csv`] |
| *-- dont abonnés avant le 01/03/2026* | 1 118 | 142 | **12,70 %** | Filtre abonnés `signup_date < '2026-03-01'` [Source : `donnees/customers.csv`] |
| *-- dont achats ponctuels avant le 01/03/2026* | 515 | 313 | **60,78 %** | Filtre ponctuels `signup_date < '2026-03-01'` [Source : `donnees/customers.csv`] |
| **À partir du 1er mars 2026** (Hausse +5 %) | 367 | 192 | **52,32 %** | `signup_date >= '2026-03-01'`, churn moyen [Source : `donnees/customers.csv`] |
| *-- dont abonnés à partir du 01/03/2026* | 184 | 58 | **31,52 %** | Filtre abonnés `signup_date >= '2026-03-01'` [Source : `donnees/customers.csv`] |
| *-- dont achats ponctuels à partir du 01/03/2026* | 183 | 134 | **73,22 %** | Filtre ponctuels `signup_date >= '2026-03-01'` [Source : `donnees/customers.csv`] |

> [!IMPORTANT]  
> Le taux de churn des abonnés a **plus que doublé**, passant de 12,70 % pour les recrues antérieures au 1er mars à **31,52 %** pour celles arrivées après la hausse de prix (+148 % de hausse relative).

---

### 2.2 Churn selon la date de dernière commande (`last_order_date`)

| Mois de dernière commande | Volume clients | Clients partis | Taux de churn | Taux churn Abonnés | Taux churn Ponctuels | Fichier source |
|---|---|---|---|---|---|---|
| **2025-10** | 1 | 1 | **100,00 %** | - (0 client) | 100,00 % (1 / 1) | `donnees/customers.csv` |
| **2025-12** | 8 | 8 | **100,00 %** | - (0 client) | 100,00 % (8 / 8) | `donnees/customers.csv` |
| **2026-01** | 64 | 59 | **92,19 %** | - (0 client) | 92,19 % (59 / 64) | `donnees/customers.csv` |
| **2026-02** | 74 | 62 | **83,78 %** | - (0 client) | 83,78 % (62 / 74) | `donnees/customers.csv` |
| **2026-03** | 88 | 60 | **68,18 %** | - (0 client) | 68,18 % (60 / 88) | `donnees/customers.csv` |
| **2026-04** | 150 | 90 | **60,00 %** | 46,67 % (7 / 15) | 61,48 % (83 / 135) | `donnees/customers.csv` |
| **2026-05** | 427 | 131 | **30,68 %** | 17,14 % (48 / 280) | 56,46 % (83 / 147) | `donnees/customers.csv` |
| **2026-06** | 1 187 | 236 | **19,88 %** | 14,40 % (145 / 1 007) | 50,56 % (91 / 180) | `donnees/customers.csv` |
| **2026-08** | 1 | 0 | **0,00 %** | - (0 client) | 0,00 % (0 / 1) | `donnees/customers.csv` |

**Synthèse avant / après 1er mars 2026 (date de dernière commande) :**
- Dernière commande avant le 01/03/2026 : 147 clients, 130 partis, soit **88,44 % de churn**.
- Dernière commande à partir du 01/03/2026 : 1 853 clients, 517 partis, soit **27,90 % de churn**.
*(Note : La ligne de 2026-08 correspond au client PP-021844 dont la date de dernière commande est saisie au 2026-08-17 dans `customers.csv` contre le 2026-06-17 dans `orders.csv`).*

---

## 3. Canaux d'acquisition et leviers promotionnels

### 3.1 Churn par canal d'acquisition

| Canal d'acquisition | Clients totaux | Part du mix | Clients partis | Taux de churn | Fichier source et calcul |
|---|---|---|---|---|---|
| **Influenceurs (`influencer`)** | 182 | 9,10 % | 83 | **45,60 %** | `donnees/customers.csv` [Source : `donnees/customers.csv`] |
| **Publicité Meta (`paid_social`)** | 646 (brut) / 653 (norm.) | 32,30 % / 32,65 % | 244 / 246 | **37,77 %** (brut) / **37,67 %** (norm.) | `donnees/customers.csv` (inclut 'Facebook' 4 et 'Paid Social' 3) |
| **Google Ads (`paid_search`)** | 374 | 18,70 % | 123 | **32,89 %** | `donnees/customers.csv` [Source : `donnees/customers.csv`] |
| **Accès direct (`direct`)** | 155 | 7,75 % | 45 | **29,03 %** | `donnees/customers.csv` [Source : `donnees/customers.csv`] |
| **Référencement naturel (`organic_search`)** | 321 | 16,05 % | 87 | **27,10 %** | `donnees/customers.csv` [Source : `donnees/customers.csv`] |
| **Parrainage (`referral`)** | 315 | 15,75 % | 63 | **20,00 %** | `donnees/customers.csv` [Source : `donnees/customers.csv`] |

---

### 3.2 Churn par niveau de remise de bienvenue

| Remise de bienvenue (`welcome_discount_pct`) | Clients totaux | Part du mix | Clients partis | Taux de churn | Fichier source et calcul |
|---|---|---|---|---|---|
| **0 %** (Aucune remise) | 620 | 31,00 % | 169 | **27,26 %** | `donnees/customers.csv` [Source : `donnees/customers.csv`] |
| **20 %** (Code BIENVENUE20 ou parrainage) | 907 | 45,35 % | 244 | **26,90 %** | `donnees/customers.csv` [Source : `donnees/customers.csv`] |
| **30 %** (Code BIENVENUE30 ou influenceur) | 473 | 23,65 % | 234 | **49,47 %** | `donnees/customers.csv` [Source : `donnees/customers.csv`] |

> [!WARNING]  
> La remise de 30 % provoque un effet d'aubaine destructeur : le churn bondit à **49,47 %**, soit près du double des clients sans remise (27,26 %) ou avec 20 % (26,90 %).

---

### 3.3 Coût d'acquisition client (CAC) et dépenses marketing

| Canal marketing | Dépenses S1 2026 | Nouveaux clients S1 2026 | CAC S1 2026 | Dépenses 2025 | Nouveaux clients 2025 | CAC 2025 | Source |
|---|---|---|---|---|---|---|---|
| **Paid social** | 134 943 € | 1 543 | **87,45 €** | 258 597 € | 4 023 | 64,28 € | `donnees/marketing_monthly.csv` |
| **Influenceurs** | 44 217 € | 441 | **100,27 €** | 90 286 € | 1 072 | 84,22 € | `donnees/marketing_monthly.csv` |
| **Paid search** | 53 092 € | 735 | **72,23 €** | 91 140 € | 1 657 | 55,00 € | `donnees/marketing_monthly.csv` |
| **Parrainage** | 10 199 € | 331 | **30,81 €** | 27 480 € | 1 037 | 26,50 € | `donnees/marketing_monthly.csv` |
| **Direct** | 0 € | 220 | 0,00 € | 0 € | 0 (intégré) | 0,00 € | `donnees/marketing_monthly.csv` |
| **SEO (Naturel)** | 0 € | 404 | 0,00 € | 0 € | 0 (intégré) | 0,00 € | `donnees/marketing_monthly.csv` |
| **Total entreprise** | **242 451 €** | **3 674** | **65,99 €** | **467 503 €** | **7 789** | **60,02 €** | `donnees/marketing_monthly.csv` |

*(Note : En S1 2026, le CAC moyen atteint exactement 65,99 €, en conformité avec les 66 € mentionnés lors du comité de direction).*

---

## 4. Analyse par espèce et crise de la recette saumon chat

### 4.1 Churn par espèce animale

| Espèce déclarée (`pet_species`) | Effectif brut | Effectif normalisé | Clients partis | Taux de churn | Fichier source et formule |
|---|---|---|---|---|---|
| **Chat (`cat`)** | 830 (brut) | **835** (norm.) | 331 | **39,88 %** (brut) / **39,64 %** (norm.) | `donnees/customers.csv` (normalisation de 5 'chat') [Source : `donnees/customers.csv`] |
| **Chien (`dog`)** | 1 165 | **1 165** | 316 | **27,12 %** | `donnees/customers.csv` [Source : `donnees/customers.csv`] |
| **Écart de churn Chat vs Chien** | - | - | - | **+12,52 points (+46 % relatif)** | Comparaison directe des deux espèces [Source : `donnees/customers.csv`] |

---

### 4.2 Impact spécifique de la modification de recette saumon chat (4 mai 2026)

Le 4 mai 2026, la recette croquettes saumon chat (références P026 1,5 kg et P027 3 kg) a été modifiée par l'ajout de 18 % de poulet déshydraté.

| Segment félin | Effectif total | Clients partis | Taux de churn | Motif `pet_refused_food` | Taux de refus alimentaire | Fichier source et formule |
|---|---|---|---|---|---|---|
| **Acheteurs de croquettes saumon chat après le 4 mai 2026** | 242 | 120 | **49,59 %** | 60 | **24,79 %** (60 / 242) | Jointure `orders.csv` (P026, P027 >= 2026-05-04) et `customers.csv` [Source : `donnees/orders.csv`] |
| **Tous autres propriétaires de chats** | 593 | 211 | **35,58 %** | 5 | **0,84 %** (5 / 593) | Autres chats de la base [Source : `donnees/customers.csv`] |
| **Ensemble des chats** | 835 | 331 | **39,64 %** | 65 | **7,78 %** (65 / 835) | Total chats [Source : `donnees/customers.csv`] |

> [!CAUTION]  
> **60 des 65 cas de refus alimentaire observés chez les chats (92,3 %)** sont directement imputables aux clients ayant commandé les croquettes saumon post-4 mai. Le taux de refus a été multiplié par **29,5** (24,79 % vs 0,84 %).

---

## 5. Signaux précurseurs de départ

### 5.1 Livraisons sautées dans les 90 jours (`skipped_deliveries_90d`, Abonnés)

*Remarque : Cette variable ne s'applique qu'aux 1 302 abonnés (vide pour les achats ponctuels).*

| Livraisons sautées (90j) | Nombre d'abonnés | Abonnés partis | Taux de churn | Risque relatif | Fichier source et calcul |
|---|---|---|---|---|---|
| **0 livraison sautée** | 987 | 136 | **13,78 %** | 1,0× (Référence) | `donnees/customers.csv` [Source : `donnees/customers.csv`] |
| **1 livraison sautée** | 297 | 58 | **19,53 %** | 1,42× | `donnees/customers.csv` [Source : `donnees/customers.csv`] |
| **2 livraisons sautées** | 18 | 6 | **33,33 %** | **2,42×** | `donnees/customers.csv` [Source : `donnees/customers.csv`] |
| **Moyenne abonnés fidèles** | 1 102 | - | **0,239 livraison** | - | Moyenne de la variable pour `churned == 0` |
| **Moyenne abonnés partis** | 200 | - | **0,350 livraison** | **+46,5 %** | Moyenne de la variable pour `churned == 1` |

---

### 5.2 Retards de livraison sur 12 mois (`late_deliveries_12m`) et crise du transporteur

Le 2 mars 2026, le changement de transporteur visait à économiser 0,80 € par colis, mais a entraîné une dégradation de la ponctualité logistique, notamment dans les zones rurales.

| Nombre de colis en retard (12m) | Ensemble des clients | Taux churn global | Abonnés | Taux churn abonnés | Clients déclarant `delivery_issues` | Source |
|---|---|---|---|---|---|---|
| **0 retard** | 1 360 | 35,59 % | 749 | 15,75 % | 39 | `donnees/customers.csv` |
| **1 retard** | 513 | 27,29 % | 426 | 13,85 % | 42 | `donnees/customers.csv` |
| **2 retards** | 100 | 21,00 % | 100 | 21,00 % | 5 | `donnees/customers.csv` |
| **3 retards** | 25 | 8,00 % | 25 | 8,00 % | 1 | `donnees/customers.csv` |
| **4 retards** | 2 | 0,00 % | 2 | 0,00 % | 0 | `donnees/customers.csv` |

**Sur-sinistralité dans les départements ruraux en tension logistique :**  
*(Départements analysés : Bretagne 22, 29, 35, 56 ; Corse 2A, 2B ; Massif Central 03, 15, 43, 63, 12, 48, 19, 23, 87 ; Alpes du Sud 04, 05).*
- Nombre de clients dans ces départements : 249 clients (12,45 % de l'échantillon).
- Retards moyens par client : **0,582 colis/an** en rural vs **0,372** dans les autres départements (**+56,5 % plus fréquents**).
- Taux de churn dans les départements ruraux : **34,54 %** vs **32,04 %**.
- Part des clients citant `delivery_issues` : **5,62 %** (14 / 249) en rural vs **4,17 %** (73 / 1 751) ailleurs.

---

### 5.3 Contacts au service client (`support_tickets_12m`, Abonnés)

| Tickets support (12m) | Abonnés totaux | Abonnés partis | Taux de churn abonnés | Fichier source et formule |
|---|---|---|---|---|
| **0 ticket** | 822 | 119 | **14,48 %** | `donnees/customers.csv` [Source : `donnees/customers.csv`] |
| **1 ticket** | 321 | 50 | **15,58 %** | `donnees/customers.csv` [Source : `donnees/customers.csv`] |
| **2 tickets** | 116 | 22 | **18,97 %** | `donnees/customers.csv` [Source : `donnees/customers.csv`] |
| **3 tickets** | 30 | 6 | **20,00 %** | `donnees/customers.csv` [Source : `donnees/customers.csv`] |
| **4 tickets** | 10 | 2 | **20,00 %** | `donnees/customers.csv` [Source : `donnees/customers.csv`] |
| **5 tickets** | 3 | 1 | **33,33 %** | `donnees/customers.csv` [Source : `donnees/customers.csv`] |
| **Moyenne abonnés fidèles** | 1 102 | - | **0,520 ticket** | Moyenne `support_tickets_12m` pour `churned == 0` |
| **Moyenne abonnés partis** | 200 | - | **0,625 ticket** | **+20,2 %** pour `churned == 1` |

---

### 5.4 Note du dernier avis déposé (`last_review_score`)

*Remarque : 1 115 clients n'ont jamais déposé d'avis (valeur vide).*

| Note déposée | Effectif répondants | Clients partis | Taux de churn | Fichier source et formule |
|---|---|---|---|---|
| **★ 1 / 5** | 8 | 3 | **37,50 %** | `donnees/customers.csv` [Source : `donnees/customers.csv`] |
| **★ 2 / 5** | 50 | 22 | **44,00 %** | `donnees/customers.csv` [Source : `donnees/customers.csv`] |
| **★ 3 / 5** | 192 | 74 | **38,54 %** | `donnees/customers.csv` [Source : `donnees/customers.csv`] |
| **★ 4 / 5** | 326 | 108 | **33,13 %** | `donnees/customers.csv` [Source : `donnees/customers.csv`] |
| **★ 5 / 5** | 309 | 73 | **23,62 %** | `donnees/customers.csv` [Source : `donnees/customers.csv`] |
| **Aucun avis déposé** | 1 115 | 367 | **32,91 %** | `donnees/customers.csv` [Source : `donnees/customers.csv`] |
| **Note moyenne - Fidèles** | 605 avis | - | **4,08 / 5** | Moyenne `last_review_score` pour `churned == 0` |
| **Note moyenne - Partis** | 280 avis | - | **3,81 / 5** | Moyenne `last_review_score` pour `churned == 1` |

---

## 6. Raisons déclarées de résiliation (`churn_reason`)

Sur les 647 clients partis :
- **528 clients ont exprimé un motif explicite** (81,61 % des partants).
- **119 clients n'ont pas renseigné de motif** (18,39 % des partants).

| Rang | Motif de résiliation | Code brut | Nombre de clients | Part des churnés (N=647) | Part des motifs déclarés (N=528) | Répartition Espèce | Fichier source |
|---|---|---|---|---|---|---|---|
| 1 | **Prix trop élevé** | `price` | **146** | **22,57 %** | **27,65 %** | 63 chats, 83 chiens | `donnees/customers.csv` |
| 2 | **Autre motif** | `other` | **94** | **14,53 %** | **17,80 %** | 47 chats, 47 chiens | `donnees/customers.csv` |
| 3 | **Problèmes de livraison** | `delivery_issues` | **87** | **13,45 %** | **16,48 %** | 36 chats, 51 chiens | `donnees/customers.csv` |
| 4 | **Parti chez un concurrent** | `switched_competitor` | **86** | **13,29 %** | **16,29 %** | 38 chats, 48 chiens | `donnees/customers.csv` |
| 5 | **Refus de la nourriture** | `pet_refused_food` | **75** | **11,59 %** | **14,20 %** | **65 chats**, 10 chiens | `donnees/customers.csv` |
| 6 | **Trop de stock à la maison** | `too_much_stock` | **23** | **3,55 %** | **4,36 %** | 16 chats, 7 chiens | `donnees/customers.csv` |
| 7 | **Passage en alimentation vétérinaire** | `moved_to_vet_diet` | **9** | **1,39 %** | **1,70 %** | 0 chat, 9 chiens | `donnees/customers.csv` |
| 8 | **Décès de l'animal** | `pet_deceased` | **8** | **1,24 %** | **1,52 %** | 2 chats, 6 chiens | `donnees/customers.csv` |
| - | **Non renseigné / Vide** | `NaN` | **119** | **18,39 %** | - | 64 chats, 55 chiens | `donnees/customers.csv` |

---

## 7. Sensibilité au prix et revenus du foyer (`household_income_band`)

Validation empirique de l'hypothèse de Nadia Ferrand (départ des foyers modestes suite à la hausse tarifaire de +5 %) :

| Tranche de revenu mensuel net | Effectif total | Clients partis | Taux de churn | Départs pour motif `price` | Part motif `price` sur l'effectif | Source |
|---|---|---|---|---|---|---|
| **Moins de 2 000 €** | 241 | 103 | **42,74 %** | 28 | **11,62 %** (28 / 241) | `donnees/customers.csv` [Source : `donnees/customers.csv`] |
| **2 000 à 3 000 €** | 415 | 121 | **29,16 %** | 27 | **6,51 %** (27 / 415) | `donnees/customers.csv` [Source : `donnees/customers.csv`] |
| **3 000 à 4 500 €** | 465 | 131 | **28,17 %** | 23 | **4,95 %** (23 / 465) | `donnees/customers.csv` [Source : `donnees/customers.csv`] |
| **Plus de 4 500 €** | 284 | 94 | **33,10 %** | 22 | **7,75 %** (22 / 284) | `donnees/customers.csv` [Source : `donnees/customers.csv`] |
| **Non apparié / Inconnu** | 595 | 198 | **33,28 %** | 46 | **7,73 %** (46 / 595) | `donnees/customers.csv` [Source : `donnees/customers.csv`] |

> [!TIP]  
> Le taux de churn des foyers modestes (< 2 000 €/mois) atteint **42,74 %**, soit **+14,57 points** de plus que la classe moyenne (3 000-4 500 €). Le motif de départ `price` y est 2,3 fois plus représenté.

---

## 8. Synthèse pour l'extrapolation globale (Comité de direction)

L'échantillon analysé comprend 2 000 clients représentatifs du portefeuille actif au 30 juin 2026.  
À l'échelle de l'entreprise (18 000 clients actifs à 12 mois, chiffre d'affaires semestriel de 3,1 M€, soit environ 6,2 M€ en rythme annuel) :
- Facteur d'échelle portefeuille : **× 9** (18 000 / 2 000).
- CA perdu sur l'échantillon à 12 mois : **153 607,45 € TTC**.
- **Extrapolation macroéconomique du CA annuel perdu** : environ **1,38 M€ TTC** si les pertes de l'échantillon sont étendues à l'ensemble du parc actif.
