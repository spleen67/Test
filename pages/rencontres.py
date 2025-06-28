import streamlit as st
import pandas as pd


from lib.constants import CATEGORIE_NIVEAU, NIVEAU_COMPETITIONS
from lib.utils import get_rencontres, get_arbitres, get_disponibilites

# Configuration de la page
st.set_page_config(page_title="Affectation des arbitres", layout="wide")
st.title("Affectation automatique des arbitres aux rencontres")

@st.cache_data
def charger_donnees_fusionnees():
    """Charge et fusionne toutes les données nécessaires."""
    rencontres = get_rencontres()
    arbitres = get_arbitres()
    disponibilites = get_disponibilites()
    
    # Ne garder que les arbitres disponibles
    dispo_oui = disponibilites[disponibilites['DISPONIBILITE'] == "OUI"]
    
    # Fusionner les disponibilités avec les détails des arbitres
    arbitres_disponibles = pd.merge(
        dispo_oui,
        arbitres, 
        left_on='NO LICENCE', 
        right_on='NUMERO AFFILIATION', 
        how='left'
    )
    
    # Ajouter le niveau numérique à chaque arbitre
    arbitres_disponibles['CATEGORIE'] = arbitres_disponibles['CATEGORIE'].str.upper()
    arbitres_disponibles['NIVEAU'] = arbitres_disponibles['CATEGORIE'].map(CATEGORIE_NIVEAU)
    
    return rencontres, arbitres_disponibles

def filtrer_arbitres_eligibles(rencontre, arbitres_disponibles):
    """Filtre les arbitres éligibles pour une rencontre donnée."""
    # Récupérer la date et le niveau de la rencontre
    date_rencontre = rencontre.iloc[0]['DATE']
    competition = rencontre.iloc[0]['COMPETITION NOM'].strip().upper()
    niveau_min, niveau_max = NIVEAU_COMPETITIONS.get(competition, (None, None))
    
    if niveau_min is None:
        st.error(f"Niveau de compétition non défini pour : {competition}")
        return pd.DataFrame()
        
    # 1. Filtrer les arbitres disponibles à la bonne date
    arbitres_dispo_date = arbitres_disponibles[arbitres_disponibles['DATE'] == date_rencontre]
    
    # 2. Filtrer par niveau de compétence
    arbitres_eligibles = arbitres_dispo_date[
        arbitres_dispo_date['NIVEAU'].apply(lambda x: niveau_min <= x <= niveau_max if pd.notna(x) else False)
    ]
    
    return arbitres_eligibles

# --- Interface Utilisateur ---

# Chargement des données
rencontres, arbitres_disponibles = charger_donnees_fusionnees()

st.subheader("Sélectionnez une rencontre")

# Amélioration de la sélection de la rencontre
if rencontres.empty:
    st.warning("Aucune rencontre à afficher. Vérifiez la source de données.")
    st.stop()

# Créer une colonne textuelle pour l'affichage dans le selectbox
rencontres['display'] = rencontres['EQUIPE DOMICILE'] + " vs " + rencontres['EQUIPE VISITEUR'] + " (" + rencontres['DATE'].astype(str) + ")"
rencontre_display = st.selectbox("Choisissez une rencontre :", rencontres['display'])

if rencontre_display:
    # Retrouver la rencontre sélectionnée
    rencontre_selectionnee = rencontres[rencontres['display'] == rencontre_display]
    
    st.write("**Détails de la rencontre :**")
    st.table(rencontre_selectionnee[['DATE', 'COMPETITION NOM', 'EQUIPE DOMICILE', 'EQUIPE VISITEUR']])
    
    # Filtrer et afficher les arbitres
    arbitres_eligibles = filtrer_arbitres_eligibles(rencontre_selectionnee, arbitres_disponibles)
    
    st.subheader("Arbitres proposés")
    if not arbitres_eligibles.empty:
        st.dataframe(
            arbitres_eligibles[['NOM', 'PRENOM', 'NO LICENCE', 'CATEGORIE', 'NIVEAU']],
            column_config={
                "NOM": "Nom",
                "PRENOM": "Prénom",
                "NO LICENCE": "N° Licence",
                "CATEGORIE": "Catégorie",
                "NIVEAU": "Niveau"
            },
            use_container_width=True,
            hide_index=True
        )
    else:
        st.warning("Aucun arbitre disponible et compatible avec le niveau requis pour cette date.")
