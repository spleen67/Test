import streamlit as st
import pandas as pd


from lib.utils import get_disponibilites, get_arbitres

# Configuration de la page
st.set_page_config(page_title="Disponibilités des arbitres", layout="wide")
st.title("Tableau de bord des disponibilités des arbitres")

# Chargement des données via les fonctions utilitaires
df_dispo_raw = get_disponibilites()
df_arbitres_raw = get_arbitres()

# Préparation des données pour l'affichage et la fusion
# On garde uniquement les colonnes utiles des arbitres pour la fusion
df_arbitres = df_arbitres_raw[['NUMERO AFFILIATION', 'CATEGORIE_x', 'CODE CLUB']].copy()

# On transforme la disponibilité en icônes pour l'affichage
df_dispo = df_dispo_raw.copy()
df_dispo['DISPONIBILITE'] = df_dispo['DISPONIBILITE'].apply(lambda x: "✅" if x == "OUI" else "☑️")

# Fusion des données
if 'NO LICENCE' in df_dispo.columns:
    df = pd.merge(df_dispo, df_arbitres, left_on='NO LICENCE', right_on='NUMERO AFFILIATION', how='left')
else:
    st.error("La colonne 'NO LICENCE' est introuvable dans le fichier de disponibilités.")
    st.stop()

# Vérification des colonnes nécessaires
# Note: 'CATEGORIE_y' devient 'CATEGORIE' car on a évité la collision de colonnes
colonnes_requises = ['NOM', 'PRENOM', 'CATEGORIE_x', 'CODE CLUB', 'DATE', 'DISPONIBILITE']
colonnes_manquantes = [col for col in colonnes_requises if col not in df.columns]

if colonnes_manquantes:
    st.error(f"Colonnes manquantes pour le tableau : {', '.join(colonnes_manquantes)}")
    st.write("Colonnes disponibles :", df.columns.tolist())
    st.stop()

# Création du tableau pivoté
pivot = df.pivot_table(
    index=['NOM', 'PRENOM', 'CATEGORIE_x', 'CODE CLUB'],
    columns='DATE',
    values='DISPONIBILITE',
    aggfunc='first',
    fill_value='☑️'
)

# Formatage des dates en colonnes (format FR)
pivot.columns = [pd.to_datetime(date).strftime('%d/%m/%Y') for date in pivot.columns]
pivot.reset_index(inplace=True)

# Affichage du tableau
st.dataframe(pivot, use_container_width=True)
