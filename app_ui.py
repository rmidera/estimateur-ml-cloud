import streamlit as st
import requests

# Configuration de la page
st.set_page_config(
    page_title="Estimateur Immobilier ML",
    page_icon="🏠",
    layout="centered"
)

st.title("🏠 Estimateur de Prix Immobilier")
st.write("Interface connectée à l'API de Machine Learning déployée sur Render.")

# Barre latérale pour la configuration de sécurité
with st.sidebar:
    st.header("⚙️ Configuration API")
    api_url = st.text_input(
        "URL du service",
        value="https://mon-estimateur-ml-v1-0.onrender.com"
    )
    api_key = st.text_input(
        "Clé d'API (X-API-Key)",
        value="SecretML2026!",
        type="password",
        help="Clé secrète requise pour autoriser les requêtes."
    )
    st.info("Statut : Clé injectée dans les en-têtes HTTP de chaque requête.")

# Formulaire principal pour les prédictions
st.subheader("Paramètres du bien")

col1, col2 = st.columns(2)

with col1:
    surface = st.slider("Surface habitable (m²)", min_value=10, max_value=1500, value=80, step=5)

with col2:
    pieces = st.number_input("Nombre de pièces", min_value=1, max_value=50, value=3, step=1)

# Bouton de soumission
if st.button("Estimer le prix", type="primary", use_container_width=True):
    endpoint = f"{api_url.rstrip('/')}/predire"
    headers = {"X-API-Key": api_key}
    params = {"surface_m2": surface, "pieces": pieces}

    with st.spinner("Interrogation du modèle en cours..."):
        try:
            response = requests.get(endpoint, headers=headers, params=params, timeout=20)

            if response.status_code == 200:
                donnees = response.json()
                prix = donnees.get("prix_estime_eur") or donnees.get("prix_estime") or donnees.get("prediction")
                
                st.success("Estimation calculée avec succès !")
                
                # Affichage des métriques clés
                m_col1, m_col2 = st.columns(2)
                if prix is not None:
                    m_col1.metric(label="Prix Estimé", value=f"{float(prix):,.2f} €")
                    prix_m2 = float(prix) / surface
                    m_col2.metric(label="Prix au m²", value=f"{prix_m2:,.2f} €/m²")
                
                with st.expander("Voir la réponse JSON brute"):
                    st.json(donnees)

            elif response.status_code == 401:
                st.error("🔒 Erreur 401 : Clé d'API invalide ou manquante. Vérifiez la clé dans la barre latérale.")
            else:
                st.error(f"Erreur HTTP {response.status_code} : {response.text}")

        except requests.exceptions.RequestException as err:
            st.error(f"Impossible de joindre le serveur distant : {err}")