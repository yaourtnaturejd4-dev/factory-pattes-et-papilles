"""
Script d'analyse de données - Fabrique Pattes & Papilles
Auteur : Agent analyste
Rôle : Calcul des métriques de churn, des signaux précurseurs et génération des graphiques.
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Définition des chemins de données et de sortie
DATA_DIR = "donnees"
ANALYSE_DIR = "chantier/analyse"
os.makedirs(ANALYSE_DIR, exist_ok=True)

# Charte graphique officielle Pattes & Papilles
COLOR_PRIMARY = "#1E4636"      # Vert sapin
COLOR_ACCENT = "#D9734E"       # Terracotta
COLOR_BACKGROUND = "#FBF5EC"   # Crème
COLOR_SECONDARY = "#E8B04B"    # Moutarde
COLOR_MUTED = "#8C9B90"        # Gris vert adouci
COLOR_DARK_TEXT = "#1C2421"    # Texte sombre

# Configuration de base pour matplotlib
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#CCCCCC'
plt.rcParams['axes.linewidth'] = 0.8


def load_datasets():
    """Charge l'ensemble des fichiers de données de la marque."""
    customers_df = pd.read_csv(os.path.join(DATA_DIR, "customers.csv"))
    orders_df = pd.read_csv(os.path.join(DATA_DIR, "orders.csv"))
    products_df = pd.read_csv(os.path.join(DATA_DIR, "products.csv"))
    marketing_df = pd.read_csv(os.path.join(DATA_DIR, "marketing_monthly.csv"))
    support_df = pd.read_csv(os.path.join(DATA_DIR, "abonnes_support.csv"))
    return customers_df, orders_df, products_df, marketing_df, support_df


def prepare_data(customers_df, orders_df):
    """Nettoie et enrichit les données clients et commandes."""
    df_cust = customers_df.copy()
    df_orders = orders_df.copy()

    # Normalisation de l'espèce animale (la valeur 'chat' existe en 5 occurrences)
    df_cust['species_norm'] = df_cust['pet_species'].replace({'chat': 'cat'})

    # Normalisation des canaux d'acquisition
    channel_mapping = {
        'Facebook': 'paid_social',
        'Paid Social': 'paid_social'
    }
    df_cust['channel_norm'] = df_cust['acquisition_channel'].replace(channel_mapping)

    # Conversion des dates
    df_cust['signup_dt'] = pd.to_datetime(df_cust['signup_date'])
    df_cust['last_order_dt'] = pd.to_datetime(df_cust['last_order_date'])
    df_orders['order_dt'] = pd.to_datetime(df_orders['order_date'])

    # Indicateur d'inscription après le 1er mars 2026
    df_cust['signup_post_march'] = df_cust['signup_dt'] >= '2026-03-01'
    df_cust['last_order_post_march'] = df_cust['last_order_dt'] >= '2026-03-01'

    # Identification des départements ruraux en forte tension logistique
    rural_departments = ['22', '29', '35', '56', '2A', '2B', '03', '15', '43', '63', '12', '48', '04', '05', '19', '23', '87']
    df_cust['is_rural'] = df_cust['department'].isin(rural_departments)

    # Identification des acheteurs de croquettes saumon chat (P026 et P027)
    salmon_orders = df_orders[df_orders['product_id'].isin(['P026', 'P027'])]
    salmon_customers = salmon_orders['customer_id'].unique()
    df_cust['bought_salmon_kibble'] = df_cust['customer_id'].isin(salmon_customers)

    salmon_orders_post_may4 = df_orders[(df_orders['product_id'].isin(['P026', 'P027'])) & (df_orders['order_dt'] >= '2026-05-04')]
    salmon_customers_post_may4 = salmon_orders_post_may4['customer_id'].unique()
    df_cust['bought_salmon_post_may4'] = df_cust['customer_id'].isin(salmon_customers_post_may4)

    return df_cust, df_orders


def calculate_metrics(df_cust, df_orders, marketing_df):
    """Calcule l'ensemble des indicateurs quantitatifs clés."""
    metrics = {}

    # 1. Churn global et par formule
    total_customers = len(df_cust)
    churned_customers = int(df_cust['churned'].sum())
    global_churn_rate = churned_customers / total_customers

    subs_df = df_cust[df_cust['plan'] == 'subscription']
    subs_total = len(subs_df)
    subs_churned = int(subs_df['churned'].sum())
    subs_churn_rate = subs_churned / subs_total

    oneoff_df = df_cust[df_cust['plan'] == 'one_off']
    oneoff_total = len(oneoff_df)
    oneoff_churned = int(oneoff_df['churned'].sum())
    oneoff_churn_rate = oneoff_churned / oneoff_total

    metrics['total_customers'] = total_customers
    metrics['churned_customers'] = churned_customers
    metrics['global_churn_rate'] = global_churn_rate
    metrics['subs_total'] = subs_total
    metrics['subs_churned'] = subs_churned
    metrics['subs_churn_rate'] = subs_churn_rate
    metrics['oneoff_total'] = oneoff_total
    metrics['oneoff_churned'] = oneoff_churned
    metrics['oneoff_churn_rate'] = oneoff_churn_rate

    # 2. Churn selon la date d'inscription (avant vs après 1er mars 2026)
    pre_march_cust = df_cust[~df_cust['signup_post_march']]
    post_march_cust = df_cust[df_cust['signup_post_march']]

    metrics['pre_march_total'] = len(pre_march_cust)
    metrics['pre_march_churned'] = int(pre_march_cust['churned'].sum())
    metrics['pre_march_churn_rate'] = pre_march_cust['churned'].mean()

    metrics['post_march_total'] = len(post_march_cust)
    metrics['post_march_churned'] = int(post_march_cust['churned'].sum())
    metrics['post_march_churn_rate'] = post_march_cust['churned'].mean()

    # Churn selon le mois de dernière commande
    df_cust['last_order_month'] = df_cust['last_order_dt'].dt.to_period('M').astype(str)
    last_order_summary = df_cust.groupby('last_order_month')['churned'].agg(
        total='count',
        churned='sum',
        rate='mean'
    ).reset_index()
    metrics['last_order_summary'] = last_order_summary

    # Churn avant et après 1er mars 2026 sur la dernière commande
    pre_march_lo = df_cust[~df_cust['last_order_post_march']]
    post_march_lo = df_cust[df_cust['last_order_post_march']]
    metrics['pre_march_lo_total'] = len(pre_march_lo)
    metrics['pre_march_lo_churned'] = int(pre_march_lo['churned'].sum())
    metrics['pre_march_lo_rate'] = pre_march_lo['churned'].mean()
    metrics['post_march_lo_total'] = len(post_march_lo)
    metrics['post_march_lo_churned'] = int(post_march_lo['churned'].sum())
    metrics['post_march_lo_rate'] = post_march_lo['churned'].mean()

    # 3. Churn par canal d'acquisition (normalisé et brut)
    channel_summary = df_cust.groupby('channel_norm')['churned'].agg(
        total='count',
        churned='sum',
        rate='mean'
    ).reset_index().sort_values('rate', ascending=False)
    metrics['channel_summary'] = channel_summary

    # 4. Churn par espèce
    species_summary = df_cust.groupby('species_norm')['churned'].agg(
        total='count',
        churned='sum',
        rate='mean'
    ).reset_index()
    metrics['species_summary'] = species_summary

    # 5. Churn par niveau de remise de bienvenue
    discount_summary = df_cust.groupby('welcome_discount_pct')['churned'].agg(
        total='count',
        churned='sum',
        rate='mean'
    ).reset_index()
    metrics['discount_summary'] = discount_summary

    # 6. Signaux précurseurs
    # Livraisons sautées (abonnés uniquement)
    skipped_summary = subs_df.groupby('skipped_deliveries_90d')['churned'].agg(
        total='count',
        churned='sum',
        rate='mean'
    ).reset_index()
    metrics['skipped_summary'] = skipped_summary

    # Retards de livraison sur 12 mois
    late_summary = df_cust.groupby('late_deliveries_12m')['churned'].agg(
        total='count',
        churned='sum',
        rate='mean'
    ).reset_index()
    metrics['late_summary'] = late_summary

    # Tickets support sur 12 mois
    tickets_summary = df_cust.groupby('support_tickets_12m')['churned'].agg(
        total='count',
        churned='sum',
        rate='mean'
    ).reset_index()
    metrics['tickets_summary'] = tickets_summary

    # Note du dernier avis
    review_summary = df_cust.dropna(subset=['last_review_score']).groupby('last_review_score')['churned'].agg(
        total='count',
        churned='sum',
        rate='mean'
    ).reset_index()
    metrics['review_summary'] = review_summary

    # 7. Raisons de départ déclarées
    churn_reasons = df_cust[df_cust['churned'] == 1]['churn_reason'].fillna('Non renseigné').value_counts().reset_index()
    churn_reasons.columns = ['reason', 'count']
    churn_reasons['pct_of_churned'] = churn_reasons['count'] / churned_customers
    metrics['churn_reasons'] = churn_reasons

    # 8. Chiffre d'affaires perdu sur les 12 derniers mois (commandes du 2025-07-01 au 2026-06-30)
    orders_12m = df_orders[(df_orders['order_dt'] >= '2025-07-01') & (df_orders['order_dt'] <= '2026-06-30')].copy()
    
    # Table de correspondance client dédoublonnée (évite de dupliquer les lignes de commandes des 15 doublons clients)
    cust_lookup = df_cust[['customer_id', 'churned', 'plan']].drop_duplicates()
    orders_12m_dedup = orders_12m.merge(cust_lookup, on='customer_id', how='left')

    ca_total_12m = orders_12m['line_total_eur'].sum()
    ca_retained_12m = orders_12m_dedup[orders_12m_dedup['churned'] == 0]['line_total_eur'].sum()
    ca_churned_12m = orders_12m_dedup[orders_12m_dedup['churned'] == 1]['line_total_eur'].sum()

    ca_subs_churned_12m = orders_12m_dedup[(orders_12m_dedup['churned'] == 1) & (orders_12m_dedup['plan'] == 'subscription')]['line_total_eur'].sum()
    ca_oneoff_churned_12m = orders_12m_dedup[(orders_12m_dedup['churned'] == 1) & (orders_12m_dedup['plan'] == 'one_off')]['line_total_eur'].sum()

    # Calcul avec doublons de jointure (si fusion directe avec la table brute de 2000 lignes)
    orders_12m_raw_merge = orders_12m.merge(df_cust[['customer_id', 'churned', 'plan']], on='customer_id', how='left')
    ca_churned_12m_raw_merge = orders_12m_raw_merge[orders_12m_raw_merge['churned'] == 1]['line_total_eur'].sum()

    metrics['ca_total_12m'] = ca_total_12m
    metrics['ca_retained_12m'] = ca_retained_12m
    metrics['ca_churned_12m'] = ca_churned_12m
    metrics['ca_subs_churned_12m'] = ca_subs_churned_12m
    metrics['ca_oneoff_churned_12m'] = ca_oneoff_churned_12m
    metrics['ca_churned_12m_raw_merge'] = ca_churned_12m_raw_merge

    # Total dépensé historique dans customers.csv
    total_spent_churned = df_cust[df_cust['churned'] == 1]['total_spent_eur'].sum()
    metrics['total_spent_churned'] = total_spent_churned

    # 9. Crise recette saumon chat
    cats_post_may = df_cust[df_cust['species_norm'] == 'cat']
    cats_salmon = cats_post_may[cats_post_may['bought_salmon_post_may4']]
    cats_other = cats_post_may[~cats_post_may['bought_salmon_post_may4']]

    metrics['cats_salmon_total'] = len(cats_salmon)
    metrics['cats_salmon_churn_rate'] = cats_salmon['churned'].mean()
    metrics['cats_salmon_refused_rate'] = (cats_salmon['churn_reason'] == 'pet_refused_food').mean()

    metrics['cats_other_total'] = len(cats_other)
    metrics['cats_other_churn_rate'] = cats_other['churned'].mean()
    metrics['cats_other_refused_rate'] = (cats_other['churn_reason'] == 'pet_refused_food').mean()

    # 10. Impact rural sur les retards
    rural_stats = df_cust.groupby('is_rural').agg(
        total=('customer_id', 'count'),
        late_mean=('late_deliveries_12m', 'mean'),
        churn_rate=('churned', 'mean')
    ).reset_index()
    metrics['rural_stats'] = rural_stats

    # 11. Coût d'acquisition client (CAC) marketing
    marketing_df['year'] = marketing_df['month'].str[:4]
    mkt_s1_2026 = marketing_df[marketing_df['month'].between('2026-01', '2026-06')]
    cac_s1_2026 = mkt_s1_2026['spend_eur'].sum() / mkt_s1_2026['new_customers'].sum()
    metrics['cac_s1_2026'] = cac_s1_2026

    return metrics


def generate_chart_1_cohorts(df_cust):
    """Graphique 1 : Churn par cohorte d'inscription avant/après le 1er mars 2026."""
    fig, ax = plt.subplots(figsize=(8, 5), facecolor=COLOR_BACKGROUND)
    ax.set_facecolor(COLOR_BACKGROUND)

    periods = ['Avant le 1er mars 2026\n(Prix initial)', 'À partir du 1er mars 2026\n(Hausse tarifaire +5 %)']
    rates_all = [
        df_cust[~df_cust['signup_post_march']]['churned'].mean() * 100,
        df_cust[df_cust['signup_post_march']]['churned'].mean() * 100
    ]
    rates_subs = [
        df_cust[(~df_cust['signup_post_march']) & (df_cust['plan'] == 'subscription')]['churned'].mean() * 100,
        df_cust[(df_cust['signup_post_march']) & (df_cust['plan'] == 'subscription')]['churned'].mean() * 100
    ]

    x = np.arange(len(periods))
    width = 0.35

    rects1 = ax.bar(x - width/2, rates_all, width, label='Ensemble des clients', color=COLOR_PRIMARY)
    rects2 = ax.bar(x + width/2, rates_subs, width, label='Abonnés seuls', color=COLOR_ACCENT)

    ax.set_ylabel('Taux de churn (%)', fontsize=11, color=COLOR_DARK_TEXT, fontweight='bold')
    ax.set_title('Le churn double pour les clients recrutés après la hausse du 1er mars 2026',
                 fontsize=12, fontweight='bold', color=COLOR_PRIMARY, pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels(periods, fontsize=10, color=COLOR_DARK_TEXT)
    ax.set_ylim(0, 65)
    ax.legend(frameon=False, loc='upper left')

    # Ajout des valeurs au-dessus des barres
    for rect in rects1:
        height = rect.get_height()
        ax.annotate(f'{height:.1f} %',
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 4), textcoords="offset points",
                    ha='center', va='bottom', fontsize=10, fontweight='bold', color=COLOR_PRIMARY)

    for rect in rects2:
        height = rect.get_height()
        ax.annotate(f'{height:.1f} %',
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 4), textcoords="offset points",
                    ha='center', va='bottom', fontsize=10, fontweight='bold', color=COLOR_ACCENT)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='y', linestyle='--', alpha=0.3, color='#B0B8B3')

    plt.tight_layout()
    plt.savefig(os.path.join(ANALYSE_DIR, "churn_cohortes_mars_2026.png"), dpi=300)
    plt.close()


def generate_chart_2_channel_discount(df_cust):
    """Graphique 2 : Churn par canal d'acquisition et niveau de remise."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5), facecolor=COLOR_BACKGROUND)
    ax1.set_facecolor(COLOR_BACKGROUND)
    ax2.set_facecolor(COLOR_BACKGROUND)

    # Churn par canal
    ch_data = df_cust.groupby('channel_norm')['churned'].mean().reset_index()
    ch_data['rate_pct'] = ch_data['churned'] * 100
    ch_data = ch_data.sort_values('rate_pct', ascending=True)

    labels = {
        'referral': 'Parrainage',
        'organic_search': 'SEO (Naturel)',
        'direct': 'Accès direct',
        'paid_search': 'Google Ads',
        'paid_social': 'Meta Ads',
        'influencer': 'Influenceurs'
    }
    y_labels = [labels.get(c, c) for c in ch_data['channel_norm']]
    colors1 = [COLOR_ACCENT if c in ['influencer', 'paid_social'] else COLOR_PRIMARY for c in ch_data['channel_norm']]

    bars1 = ax1.barh(y_labels, ch_data['rate_pct'], color=colors1, height=0.6)
    ax1.set_xlabel('Taux de churn (%)', fontsize=10, fontweight='bold', color=COLOR_DARK_TEXT)
    ax1.set_title('Churn par canal d\'acquisition\n(Volatilité maximale des influenceurs)', fontsize=11, fontweight='bold', color=COLOR_PRIMARY)
    ax1.set_xlim(0, 55)

    for bar in bars1:
        w = bar.get_width()
        ax1.annotate(f'{w:.1f} %',
                     xy=(w, bar.get_y() + bar.get_height() / 2),
                     xytext=(5, 0), textcoords="offset points",
                     ha='left', va='center', fontsize=9, fontweight='bold', color=COLOR_DARK_TEXT)

    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.grid(axis='x', linestyle='--', alpha=0.3, color='#B0B8B3')

    # Churn par remise de bienvenue
    disc_data = df_cust.groupby('welcome_discount_pct')['churned'].mean().reset_index()
    disc_data['rate_pct'] = disc_data['churned'] * 100
    disc_labels = [f"Remise {int(r)} %" for r in disc_data['welcome_discount_pct']]
    colors2 = [COLOR_ACCENT if r == 30 else COLOR_PRIMARY for r in disc_data['welcome_discount_pct']]

    bars2 = ax2.bar(disc_labels, disc_data['rate_pct'], color=colors2, width=0.5)
    ax2.set_ylabel('Taux de churn (%)', fontsize=10, fontweight='bold', color=COLOR_DARK_TEXT)
    ax2.set_title('Churn par remise de bienvenue\n(Choc de rétention à -30 %)', fontsize=11, fontweight='bold', color=COLOR_PRIMARY)
    ax2.set_ylim(0, 60)

    for bar in bars2:
        h = bar.get_height()
        ax2.annotate(f'{h:.1f} %',
                     xy=(bar.get_x() + bar.get_width() / 2, h),
                     xytext=(0, 4), textcoords="offset points",
                     ha='center', va='bottom', fontsize=9, fontweight='bold', color=COLOR_DARK_TEXT)

    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.grid(axis='y', linestyle='--', alpha=0.3, color='#B0B8B3')

    fig.suptitle('La remise de 30 % et les influenceurs provoquent une déperdition client critique de près de 50 %',
                 fontsize=12, fontweight='bold', color=COLOR_PRIMARY, y=1.02)

    plt.tight_layout()
    plt.savefig(os.path.join(ANALYSE_DIR, "churn_canal_et_remise.png"), dpi=300, bbox_inches='tight')
    plt.close()


def generate_chart_3_species_salmon(df_cust):
    """Graphique 3 : Churn par espèce et crise de la recette saumon chat."""
    fig, ax = plt.subplots(figsize=(8, 5), facecolor=COLOR_BACKGROUND)
    ax.set_facecolor(COLOR_BACKGROUND)

    categories = [
        'Chiens\n(Toutes recettes)',
        'Chats\n(Autres recettes)',
        'Chats ayant reçu le saumon\naprès le 4 mai 2026'
    ]

    dog_churn = df_cust[df_cust['species_norm'] == 'dog']['churned'].mean() * 100
    cat_other_churn = df_cust[(df_cust['species_norm'] == 'cat') & (~df_cust['bought_salmon_post_may4'])]['churned'].mean() * 100
    cat_salmon_churn = df_cust[(df_cust['species_norm'] == 'cat') & (df_cust['bought_salmon_post_may4'])]['churned'].mean() * 100

    rates = [dog_churn, cat_other_churn, cat_salmon_churn]
    colors = [COLOR_PRIMARY, COLOR_SECONDARY, COLOR_ACCENT]

    bars = ax.bar(categories, rates, color=colors, width=0.55)
    ax.set_ylabel('Taux de churn (%)', fontsize=11, fontweight='bold', color=COLOR_DARK_TEXT)
    ax.set_title('Le changement de recette saumon chat a fait bondir le churn félin à 49,6 %',
                 fontsize=12, fontweight='bold', color=COLOR_PRIMARY, pad=15)
    ax.set_ylim(0, 60)

    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.1f} %',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 4), textcoords="offset points",
                    ha='center', va='bottom', fontsize=10, fontweight='bold', color=COLOR_DARK_TEXT)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='y', linestyle='--', alpha=0.3, color='#B0B8B3')

    plt.tight_layout()
    plt.savefig(os.path.join(ANALYSE_DIR, "churn_espece_et_recette_saumon.png"), dpi=300)
    plt.close()


def generate_chart_4_signals(df_cust):
    """Graphique 4 : Signaux précurseurs (livraisons sautées et notes d'avis)."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5), facecolor=COLOR_BACKGROUND)
    ax1.set_facecolor(COLOR_BACKGROUND)
    ax2.set_facecolor(COLOR_BACKGROUND)

    # Livraisons sautées chez les abonnés
    subs = df_cust[df_cust['plan'] == 'subscription']
    sk_data = subs.groupby('skipped_deliveries_90d')['churned'].agg(rate='mean', count='count').reset_index()
    sk_labels = [f"{int(s)} sautée(s)\n(n={int(c)})" for s, c in zip(sk_data['skipped_deliveries_90d'], sk_data['count'])]
    colors1 = [COLOR_PRIMARY if s == 0 else (COLOR_SECONDARY if s == 1 else COLOR_ACCENT) for s in sk_data['skipped_deliveries_90d']]

    bars1 = ax1.bar(sk_labels, sk_data['rate'] * 100, color=colors1, width=0.5)
    ax1.set_ylabel('Taux de churn des abonnés (%)', fontsize=10, fontweight='bold', color=COLOR_DARK_TEXT)
    ax1.set_title('Abonnés : impact des livraisons sautées\n(Risque multiplié par 2,4 à 2 sauts)', fontsize=11, fontweight='bold', color=COLOR_PRIMARY)
    ax1.set_ylim(0, 45)

    for bar in bars1:
        h = bar.get_height()
        ax1.annotate(f'{h:.1f} %',
                     xy=(bar.get_x() + bar.get_width() / 2, h),
                     xytext=(0, 4), textcoords="offset points",
                     ha='center', va='bottom', fontsize=9, fontweight='bold', color=COLOR_DARK_TEXT)

    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.grid(axis='y', linestyle='--', alpha=0.3, color='#B0B8B3')

    # Notes d'avis
    rev_data = df_cust.dropna(subset=['last_review_score']).groupby('last_review_score')['churned'].agg(rate='mean', count='count').reset_index()
    rev_labels = [f"★ {int(s)}\n(n={int(c)})" for s, c in zip(rev_data['last_review_score'], rev_data['count'])]
    colors2 = [COLOR_ACCENT if s <= 3 else COLOR_PRIMARY for s in rev_data['last_review_score']]

    bars2 = ax2.bar(rev_labels, rev_data['rate'] * 100, color=colors2, width=0.55)
    ax2.set_ylabel('Taux de churn global (%)', fontsize=10, fontweight='bold', color=COLOR_DARK_TEXT)
    ax2.set_title('Tous clients : impact de la note d\'avis\n(Défiance marquée sous 4 étoiles)', fontsize=11, fontweight='bold', color=COLOR_PRIMARY)
    ax2.set_ylim(0, 55)

    for bar in bars2:
        h = bar.get_height()
        ax2.annotate(f'{h:.1f} %',
                     xy=(bar.get_x() + bar.get_width() / 2, h),
                     xytext=(0, 4), textcoords="offset points",
                     ha='center', va='bottom', fontsize=9, fontweight='bold', color=COLOR_DARK_TEXT)

    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.grid(axis='y', linestyle='--', alpha=0.3, color='#B0B8B3')

    fig.suptitle('Sauter deux livraisons ou noter sous 3 étoiles multiplie fortement le risque de départ',
                 fontsize=12, fontweight='bold', color=COLOR_PRIMARY, y=1.02)

    plt.tight_layout()
    plt.savefig(os.path.join(ANALYSE_DIR, "signaux_precurseurs_churn.png"), dpi=300, bbox_inches='tight')
    plt.close()


def generate_chart_5_churn_reasons(df_cust):
    """Graphique 5 : Motifs déclarés de résiliation."""
    fig, ax = plt.subplots(figsize=(9, 5), facecolor=COLOR_BACKGROUND)
    ax.set_facecolor(COLOR_BACKGROUND)

    churned = df_cust[df_cust['churned'] == 1]
    reasons_count = churned['churn_reason'].fillna('Motif non renseigné').value_counts().reset_index()
    reasons_count.columns = ['reason', 'count']

    reason_labels = {
        'price': 'Prix trop élevé (+5 %)',
        'other': 'Autre motif',
        'delivery_issues': 'Retards / Problèmes de livraison',
        'switched_competitor': 'Départ vers un concurrent',
        'pet_refused_food': 'Refus de la nourriture par l\'animal',
        'too_much_stock': 'Trop de stock accumulé',
        'moved_to_vet_diet': 'Passage à un régime vétérinaire',
        'pet_deceased': 'Décès de l\'animal',
        'Motif non renseigné': 'Motif non renseigné'
    }

    reasons_count['clean_label'] = reasons_count['reason'].map(lambda x: reason_labels.get(x, x))
    reasons_count = reasons_count.sort_values('count', ascending=True)

    colors = [COLOR_ACCENT if r in ['price', 'delivery_issues', 'pet_refused_food'] else COLOR_PRIMARY for r in reasons_count['reason']]

    bars = ax.barh(reasons_count['clean_label'], reasons_count['count'], color=colors, height=0.6)
    ax.set_xlabel('Nombre de clients déclarants', fontsize=11, fontweight='bold', color=COLOR_DARK_TEXT)
    ax.set_title('Le prix, la livraison et le refus alimentaire concentrent la majorité des motifs de départ',
                 fontsize=12, fontweight='bold', color=COLOR_PRIMARY, pad=15)
    ax.set_xlim(0, 175)

    for bar in bars:
        w = bar.get_width()
        pct = (w / len(churned)) * 100
        ax.annotate(f'{w} ({pct:.1f} %)',
                    xy=(w, bar.get_y() + bar.get_height() / 2),
                    xytext=(5, 0), textcoords="offset points",
                    ha='left', va='center', fontsize=9, fontweight='bold', color=COLOR_DARK_TEXT)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='x', linestyle='--', alpha=0.3, color='#B0B8B3')

    plt.tight_layout()
    plt.savefig(os.path.join(ANALYSE_DIR, "motifs_depart_declares.png"), dpi=300)
    plt.close()


def generate_chart_6_lost_revenue(metrics):
    """Graphique 6 : Chiffre d'affaires perdu sur 12 mois par formule."""
    fig, ax = plt.subplots(figsize=(8, 5), facecolor=COLOR_BACKGROUND)
    ax.set_facecolor(COLOR_BACKGROUND)

    labels = ['Clients fidèles\n(Consolidé)', 'Clients partis\n(Abonnés)', 'Clients partis\n(Achats ponctuels)']
    amounts = [
        metrics['ca_retained_12m'] / 1000,
        metrics['ca_subs_churned_12m'] / 1000,
        metrics['ca_oneoff_churned_12m'] / 1000
    ]
    colors = [COLOR_PRIMARY, COLOR_ACCENT, COLOR_SECONDARY]

    bars = ax.bar(labels, amounts, color=colors, width=0.5)
    ax.set_ylabel('Chiffre d\'affaires sur 12 mois (k€ TTC)', fontsize=11, fontweight='bold', color=COLOR_DARK_TEXT)
    ax.set_title('153 607 € de CA perdus sur l\'échantillon, portés à 53 % par les abonnés',
                 fontsize=12, fontweight='bold', color=COLOR_PRIMARY, pad=15)
    ax.set_ylim(0, 750)

    for bar in bars:
        h = bar.get_height()
        ax.annotate(f'{h:.1f} k€',
                    xy=(bar.get_x() + bar.get_width() / 2, h),
                    xytext=(0, 4), textcoords="offset points",
                    ha='center', va='bottom', fontsize=10, fontweight='bold', color=COLOR_DARK_TEXT)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='y', linestyle='--', alpha=0.3, color='#B0B8B3')

    plt.tight_layout()
    plt.savefig(os.path.join(ANALYSE_DIR, "perte_chiffre_affaires_12m.png"), dpi=300)
    plt.close()


def main():
    print("Démarrage de l'analyse des données Pattes & Papilles...")
    customers_df, orders_df, products_df, marketing_df, support_df = load_datasets()
    df_cust, df_orders = prepare_data(customers_df, orders_df)
    metrics = calculate_metrics(df_cust, df_orders, marketing_df)

    print("\nGénération des graphiques...")
    generate_chart_1_cohorts(df_cust)
    generate_chart_2_channel_discount(df_cust)
    generate_chart_3_species_salmon(df_cust)
    generate_chart_4_signals(df_cust)
    generate_chart_5_churn_reasons(df_cust)
    generate_chart_6_lost_revenue(metrics)

    print("\nSynthèse des métriques calculées :")
    print(f"- Total clients : {metrics['total_customers']}")
    print(f"- Clients churnés : {metrics['churned_customers']} ({metrics['global_churn_rate']*100:.2f} %)")
    print(f"  * Abonnés churnés : {metrics['subs_churned']} / {metrics['subs_total']} ({metrics['subs_churn_rate']*100:.2f} %)")
    print(f"  * Achats ponctuels churnés : {metrics['oneoff_churned']} / {metrics['oneoff_total']} ({metrics['oneoff_churn_rate']*100:.2f} %)")
    print(f"- Churn selon date d'inscription :")
    print(f"  * Avant 01/03/2026 : {metrics['pre_march_churn_rate']*100:.2f} % ({metrics['pre_march_churned']}/{metrics['pre_march_total']})")
    print(f"  * À partir du 01/03/2026 : {metrics['post_march_churn_rate']*100:.2f} % ({metrics['post_march_churned']}/{metrics['post_march_total']})")
    print(f"- Churn selon date de dernière commande :")
    print(f"  * Avant 01/03/2026 : {metrics['pre_march_lo_rate']*100:.2f} % ({metrics['pre_march_lo_churned']}/{metrics['pre_march_lo_total']})")
    print(f"  * À partir du 01/03/2026 : {metrics['post_march_lo_rate']*100:.2f} % ({metrics['post_march_lo_churned']}/{metrics['post_march_lo_total']})")
    print(f"- CA 12 mois total : {metrics['ca_total_12m']:.2f} €")
    print(f"- CA 12 mois perdu : {metrics['ca_churned_12m']:.2f} € (dont {metrics['ca_subs_churned_12m']:.2f} € abonnés et {metrics['ca_oneoff_churned_12m']:.2f} € ponctuels)")
    print(f"- CA historique perdu (customers.csv) : {metrics['total_spent_churned']:.2f} €")
    print(f"- CAC S1 2026 : {metrics['cac_s1_2026']:.2f} €")
    print("\nAnalyse terminée avec succès.")


if __name__ == '__main__':
    main()
