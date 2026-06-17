import streamlit as st
import datetime
from dateutil.relativedelta import relativedelta
import time

# Configuration de la page mobile
st.set_page_config(
    page_title="SLINK - RDV Clients",
    page_icon="📅",
    layout="centered"
)

# Application de la palette SLINK
st.markdown("""
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Figtree:wght@400;600;700&display=swap" rel="stylesheet">
    
    <style>
    :root {
        --lobster-pink: #f2545b;
        --cherry-rose: #a93f55;
        --jet-black: #19323c;
        --mint-cream: #f3f7f0;
        --smoky-rose: #8c5e58;
    }
    
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Figtree', sans-serif !important;
        background-color: var(--mint-cream) !important;
        color: var(--jet-black) !important;
    }
    
    h1, h2, h3 { color: var(--jet-black) !important; }
    
    .stTabs [data-baseweb="tab"] {
        color: var(--smoky-rose) !important;
    }
    
    .stTabs [aria-selected="true"] {
        color: var(--lobster-pink) !important;
        border-bottom: 2px solid var(--lobster-pink) !important;
    }
    
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        background-color: var(--lobster-pink) !important;
        color: white !important;
        border: none !important;
        font-weight: 600;
    }
    
    .stButton>button:hover {
        background-color: var(--cherry-rose) !important;
    }
    
    .rdv-card {
        padding: 15px;
        background-color: #FFFFFF;
        border-radius: 10px;
        margin-bottom: 12px;
        border-left: 5px solid var(--lobster-pink);
        box-shadow: 0 2px 5px rgba(25, 50, 60, 0.1);
    }
    </style>
""", unsafe_allow_html=True)

today = datetime.date.today()
if 'rdv_db' not in st.session_state:
    st.session_state.rdv_db = []

st.title("SLINK - RDV Clients")

tab1, tab2, tab3 = st.tabs(["Nouveau RDV", "Agenda", "Historique"])

with tab1:
    client_name = st.text_input("Nom du client")
    col1, col2 = st.columns(2)
    with col1:
        current_date = st.date_input("Date du RDV", today)
    with col2:
        current_time = st.time_input("Heure", datetime.time(10, 0))

    next_date = current_date + relativedelta(months=1)
    st.write(f"Prochain audit suggéré : **{next_date.strftime('%d/%m/%Y')}**")
    final_next_date = st.date_input("Confirmer le prochain RDV", next_date)
    
    meeting_notes = st.text_area("Notes de réunion")
    
    if st.button("Valider et Enregistrer"):
        st.session_state.rdv_db.append({
            "client": client_name,
            "date": current_date,
            "heure": current_time.strftime("%H:%M"),
            "notes": meeting_notes
        })
        st.success("RDV enregistré !")

with tab2:
    st.subheader("Prochains rendez-vous")
    upcoming = sorted([r for r in st.session_state.rdv_db if r["date"] >= today], key=lambda x: x["date"])
    for rdv in upcoming:
        st.markdown(f'<div class="rdv-card"><b>{rdv["client"]}</b><br>{rdv["date"].strftime("%d/%m/%Y")} à {rdv["heure"]}</div>', unsafe_allow_html=True)

with tab3:
    st.subheader("Historique (30 derniers jours)")
    past = sorted([r for r in st.session_state.rdv_db if (today - datetime.timedelta(days=30)) <= r["date"] < today], key=lambda x: x["date"], reverse=True)
    for rdv in past:
        st.markdown(f'<div class="rdv-card"><b>{rdv["client"]}</b><br>Notes: {rdv["notes"]}</div>', unsafe_allow_html=True)
