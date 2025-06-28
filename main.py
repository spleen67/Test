import streamlit as st

# Configuration de la page
st.set_page_config(
    page_title="Système d'affectation des arbitres",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Page d'accueil avec description
def main():
    st.title("⚽ Système d'affectation des arbitres")
    st.markdown("""
    ## Bienvenue dans la plateforme de gestion des arbitres
        
    **Navigation :**
    - 📊 **Dashboard** : Visualisation des disponibilités des arbitres
    - ⚽ **Rencontres** : Affectation automatique des arbitres aux matches
        
    ### Fonctionnalités principales
    - Consultation des disponibilités en temps réel
    - Proposition d'arbitres selon le niveau de compétition
    - Gestion centralisée des données
    """)
    
    st.image("https://via.placeholder.com/800x400?text=Systeme+Arbitrage", use_column_width=True)
    
    st.markdown("---")
    st.info("ℹ️ Utilisez le menu de gauche pour naviguer entre les différentes pages.")

if __name__ == "__main__":
    main()