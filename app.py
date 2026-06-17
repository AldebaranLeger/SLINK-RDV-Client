import streamlit as st
import datetime
from dateutil.relativedelta import relativedelta
import time

# Configuration de la page pour mobile
st.set_page_config(
    page_title="SLINK - RDV Clients",
    page_icon="📅",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Style CSS pour une ambiance "App Mobile" moderne
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 10px; background-color: #007bff; color: white; }
    .stTextInput>div>div>input { border-radius: 8px; }
    .success-box { padding: 10px; background-color: #d4edda; color: #155724; border-radius: 8px; margin-bottom: 15px; }
    </style>
""", unsafe_allow_html=True)

st.title("📱 SLINK - RDV Clients")
st.subheader("Fidélisation & Audits Mensuels")

---

# 1. IDENTIFICATION CLIENT
st.write("### 👥 Informations Client")
client_name = st.text_input("Nom du client", placeholder="Ex: Jean Dupont")

# 2. GESTION DU RDV ACTUEL & SUGGESTION AUTOMATIQUE
st.write("### 📅 Planification")
col1, col2 = st.columns(2)

with col1:
    current_date = st.date_input("Date du RDV Actuel", datetime.date.today())
with col2:
    current_time = st.time_input("Heure du RDV", datetime.time(10, 0))

# Logique de suggestion : Mois actuel + 1 mois exact pour l'audit de fidélisation
next_suggested_date = current_date + relativedelta(months=1)

st.markdown(f"""
<div class="success-box">
    💡 <b>Suggestion SLINK :</b> Prochain RDV d'audit conseillé le <b>{next_suggested_date.strftime('%d/%m/%Y')}</b> (J+1 mois).
</div>
""", unsafe_allow_html=True)

final_next_date = st.date_input("Confirmer la date du prochain RDV", next_suggested_date)

---

# 3. NOTES ET ENREGISTREMENT AUDIO
st.write("### 📝 Déroulement de la Réunion")
meeting_notes = st.text_area("Notes rapides prises à la volée", placeholder="Points clés abordés...")

# Module Audio (Simulation de l'enregistrement natif smartphone)
st.write("🎙️ **Enregistrement de l'audit**")
audio_placeholder = st.empty()

if 'recording' not in st.session_state:
    st.session_state.recording = False

if not st.session_state.recording:
    if st.button("🔴 Lancer l'enregistrement"):
        st.session_state.recording = True
        st.rerun()
else:
    st.success("🎤 Enregistrement en cours... SLINK écoute votre client.")
    if st.button("⏹️ Arrêter et sauvegarder"):
        st.session_state.recording = False
        st.session_state.audio_ready = True
        st.rerun()

---

# 4. COMPTE-RENDU AUTOMATIQUE (IA)
st.write("### 🤖 Intelligence Artificielle SLINK")

if st.button("✨ Générer le Compte-Rendu Succinct"):
    if not client_name:
        st.warning("⚠️ Veuillez entrer le nom du client avant de générer le rapport.")
    else:
        with st.spinner("Analyse de l'audio et des notes en cours..."):
            time.sleep(2) # Simulation du temps de traitement de l'API
            
            # Structure du compte-rendu succinct demandé
            st.markdown("### 📋 Compte-Rendu de Réunion")
            st.info(f"**Client :** {client_name} | **Date :** {current_date.strftime('%d/%m/%Y')}")
            
            # Remplacement par l'appel API Whisper/GPT en production
            summary_template = f"""
            **1. Résumé des échanges :**
            * Le client est globalement satisfait des performances de l'audit du mois passé ({current_date.strftime('%B')}).
            * Points bloquants relevés : {meeting_notes if meeting_notes else 'Aucun point bloquant saisi.'}
            
            **2. Plan d'action & Fidélisation :**
            * [ ] Validation des livrables de ce mois-ci.
            * [ ] Préparation des indicateurs pour le prochain audit.
            
            **3. Prochaine échéance :**
            * RDV validé pour le **{final_next_date.strftime('%d/%m/%Y')}** afin d'analyser les résultats du cycle actuel.
            """
            st.write(summary_template)
            
            # Option de sauvegarde
            st.download_button(
                label="📥 Télécharger le compte-rendu (TXT)",
                data=summary_template,
                file_name=f"CR_{client_name}_{current_date}.txt",
                mime="text/plain"
            )