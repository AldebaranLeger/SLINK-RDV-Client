import streamlit as st
import datetime
from dateutil.relativedelta import relativedelta
import time

# Configuration de la page mobile
st.set_page_config(
    page_title="SLINK - RDV Clients",
    page_icon="📅",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Chargement de la police Figtree et thèmatique Blanc Joyeux
st.markdown("""
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Figtree:wght@400;600;700&display=swap" rel="stylesheet">
    
    <style>
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        font-family: 'Figtree', sans-serif !important;
        background-color: #FFFFFF !important;
    }
    .stTabs [data-baseweb="tab"] {
        font-family: 'Figtree', sans-serif !important;
        font-weight: 600;
    }
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        background: linear-gradient(135deg, #4F46E5, #6366F1);
        color: white;
        border: none;
        font-weight: 600;
        padding: 10px;
    }
    .success-box {
        padding: 12px;
        background-color: #F0FDF4;
        color: #166534;
        border-radius: 12px;
        margin-bottom: 15px;
        border-left: 4px solid #16A34A;
    }
    .rdv-card {
        padding: 15px;
        background-color: #F9FAFB;
        border-radius: 12px;
        margin-bottom: 12px;
        border: 1px solid #F3F4F6;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }
    </style>
""", unsafe_allow_html=True)

# Initialisation de la base de données temporaire (Session State)
today = datetime.date.today()
if 'rdv_db' not in st.session_state:
    st.session_state.rdv_db = [
        {"client": "Société Alpha", "date": today - datetime.timedelta(days=15), "heure": "14:00", "notes": "Audit mensuel OK. Client très satisfait.", "cr": "R.A.S"},
        {"client": "Garage Dupuis", "date": today - datetime.timedelta(days=2), "heure": "10:30", "notes": "Besoin d'optimiser le CRM le mois prochain.", "cr": "Aide CRM requise"},
        {"client": "Cabinet Loire", "date": today + datetime.timedelta(days=5), "heure": "09:00", "notes": "Préparation bilan trimestriel.", "cr": ""},
        {"client": "Tech Vision", "date": today + datetime.timedelta(days=12), "heure": "16:00", "notes": "Point de situation régulier.", "cr": ""}
    ]

st.title("📱 SLINK - RDV Clients")

# Organisation en Onglets pour l'ergonomie mobile
tab1, tab2, tab3 = st.tabs(["➕ Nouveau RDV", "📅 Agenda", "📜 Historique (M-1)"])

# ONGLET 1 : CRÉATION ET ENREGISTREMENT DE RDV
with tab1:
    st.write("### 👥 Informations Client")
    client_name = st.text_input("Nom du client", placeholder="Ex: Jean Dupont")

    st.write("### 📅 Planification")
    col1, col2 = st.columns(2)
    with col1:
        current_date = st.date_input("Date du RDV Actuel", today)
    with col2:
        current_time = st.time_input("Heure du RDV", datetime.time(10, 0))

    # Calcul J+1 mois exact
    next_suggested_date = current_date + relativedelta(months=1)

    st.markdown(f"""
    <div class="success-box">
        💡 <b>Suggestion SLINK :</b> Prochain RDV d'audit conseillé le <b>{next_suggested_date.strftime('%d/%m/%Y')}</b>.
    </div>
    """, unsafe_allow_html=True)

    final_next_date = st.date_input("Confirmer la date du prochain RDV", next_suggested_date)

    st.write("### 📝 Déroulement de la Réunion")
    meeting_notes = st.text_area("Notes de réunion", placeholder="Points clés abordés...")

    st.write("🎙️ **Enregistrement**")
    if 'recording' not in st.session_state:
        st.session_state.recording = False

    if not st.session_state.recording:
        if st.button("🔴 Lancer l'enregistrement", key="record_btn"):
            st.session_state.recording = True
            st.rerun()
    else:
        st.success("🎤 Enregistrement en cours...")
        if st.button("⏹️ Arrêter et sauvegarder", key="stop_btn"):
            st.session_state.recording = False
            st.rerun()

    if st.button("✨ Valider & Générer le Compte-Rendu"):
        if not client_name:
            st.warning("⚠️ Entrez le nom du client.")
        else:
            with st.spinner("Analyse en cours..."):
                time.sleep(1.5)
                
                # Génération du texte du compte-rendu
                summary_text = f"CR Simplifié - {client_name}\nDate: {current_date.strftime('%d/%m/%Y')}\nNotes: {meeting_notes}\nProchain RDV validé pour le: {final_next_date.strftime('%d/%m/%Y')}"
                
                # Sauvegarde automatique dans la liste
                st.session_state.rdv_db.append({
                    "client": client_name,
                    "date": current_date,
                    "heure": current_time.strftime("%H:%M"),
                    "notes": meeting_notes,
                    "cr": summary_text
                })
                
                # Affichage immédiat du résultat
                st.success("RDV enregistré et ajouté à l'agenda !")
                st.markdown("#### 📋 Compte-Rendu Succinct")
                st.info(summary_text)

# ONGLET 2 : VUE AGENDA (RDV Futurs)
with tab2:
    st.write("### 📆 Prochains Rendez-vous")
    # Filtrer les rendez-vous à partir d'aujourd'hui inclus, triés par ordre chronologique
    upcoming_rdvs = [r for r in st.session_state.rdv_db if r["date"] >= today]
    upcoming_rdvs = sorted(upcoming_rdvs, key=lambda x: x["date"])
    
    if not upcoming_rdvs:
        st.write("Aucun rendez-vous de planifié.")
    else:
        for rdv in upcoming_rdvs:
            st.markdown(f"""
            <div class="rdv-card">
                <span style="color:#4F46E5; font-weight:700;">{rdv['date'].strftime('%d/%m/%Y')} à {rdv['heure']}</span><br>
                <b>Client :</b> {rdv['client']}<br>
                <small style="color:#6B7280;">Note : {rdv['notes'] if rdv['notes'] else 'Aucune note'}</small>
            </div>
            """, unsafe_allow_html=True)

# ONGLET 3 : HISTORIQUE (Réunions enregistrées sur le dernier mois)
with tab3:
    st.write("### 📜 Réunions du dernier mois")
    one_month_ago = today - datetime.timedelta(days=30)
    
    # Filtrer les réunions passées dans l'intervalle [J-30, Hier]
    past_rdvs = [r for r in st.session_state.rdv_db if one_month_ago <= r["date"] < today]
    past_rdvs = sorted(past_rdvs, key=lambda x: x["date"], reverse=True)
    
    if not past_rdvs:
        st.write("Aucun historique trouvé pour les 30 derniers jours.")
    else:
        for rdv in past_rdvs:
            st.markdown(f"""
            <div class="rdv-card" style="border-left: 4px solid #9CA3AF;">
                <span style="color:#374151; font-weight:700;">{rdv['date'].strftime('%d/%m/%Y')}</span> - <b>{rdv['client']}</b><br>
                <small style="color:#4B5563;"><b>Notes :</b> {rdv['notes']}</small>
            </div>
            """, unsafe_allow_html=True)
            
            # Bouton d'export individuel si un CR existe
            if rdv["cr"]:
                st.download_button(
                    label=f"📥 Télécharger CR {rdv['client']}",
                    data=rdv["cr"],
                    file_name=f"CR_{rdv['client']}.txt",
                    mime="text/plain",
                    key=f"dl_{rdv['client']}_{rdv['date']}"
                )
