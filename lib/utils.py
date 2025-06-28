
# Fichier: utils.py
import streamlit as st
import pandas as pd
import unicodedata
from .constants import SHEETS_CONFIG

def nettoyer_colonnes(df):
    """Normalise les noms de colonnes d'un DataFrame."""
    df.columns = [
        unicodedata.normalize('NFKD', col).encode('ascii', errors='ignore').decode('utf-8').strip().upper()
        for col in df.columns
    ]
    return df

@st.cache_data
def charger_depuis_google_sheets(url):
    """Charge un fichier Excel depuis une URL Google Sheets."""
    return pd.read_excel(url)

@st.cache_data
def get_disponibilites():
    """Charge et prépare les données de disponibilités."""
    df = charger_depuis_google_sheets(SHEETS_CONFIG["disponibilites"])
    df = nettoyer_colonnes(df)
    df['DATE'] = pd.to_datetime(df['DATE'], errors='coerce').dt.date
    df['DISPONIBILITE'] = df['DISPONIBILITE'].astype(str).str.strip().str.upper()
    return df

@st.cache_data
def get_arbitres():
    """Charge et prépare les données des arbitres."""
    df = charger_depuis_google_sheets(SHEETS_CONFIG["arbitres"])
    df = nettoyer_colonnes(df)
    return df

@st.cache_data
def get_rencontres():
    """Charge et prépare les données des rencontres."""
    df = charger_depuis_google_sheets(SHEETS_CONFIG["rencontres"])
    df = nettoyer_colonnes(df)
    
    # Vérifier la présence des colonnes essentielles attendues par l'application
    required_cols = ['DATE', 'COMPETITION NOM', 'EQUIPE DOMICILE', 'EQUIPE VISITEUR', 'RENCONTRE NUMERO']
    missing_cols = [col for col in required_cols if col not in df.columns]
    
    if missing_cols:
        # Si une colonne manque, on lève une erreur très explicite.
        # Cela arrêtera l'application et affichera ce message sur Streamlit Cloud.
        raise ValueError(
            f"COLONNE MANQUANTE: Une ou plusieurs colonnes sont introuvables dans votre Google Sheet 'rencontres'.\n"
            f"Colonnes manquantes (après normalisation): {', '.join(missing_cols)}\n"
            f"Colonnes trouvées (après normalisation): {', '.join(df.columns)}"
        )

    # Si tout va bien, on continue le traitement
    df['DATE'] = pd.to_datetime(df['DATE'], errors='coerce').dt.date
    return df

