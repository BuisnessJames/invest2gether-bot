import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime

# App-Setup
st.set_page_config(page_title="invest2gether", page_icon="🕌", layout="wide")
st.title("🤝 invest2gether — Zertifiziertes Halal-KI-Depot")

st.sidebar.header("⚙️ Einstellungen")
START_KAPITAL = st.sidebar.number_input("Startkapital ($)", value=10000)
MONATLICHER_SPARPLAN = st.sidebar.number_input("Monatlicher Sparplan ($)", value=250)

# Daten laden
daten = yf.download(["HLAL", "GC=F"], start="2020-01-01", group_by='ticker')
df = pd.DataFrame(index=daten.index)
df['Aktien'] = daten["HLAL"]['Close'].squeeze()
df['Gold'] = daten["GC=F"]['Close'].squeeze()
df = df.ffill().dropna()

# Strategie-Berechnung (200-Tage-Linie)
df['SMA'] = df['Aktien'].rolling(window=200).mean()
df = df.dropna()
df['Signal'] = 0
df.loc[df['Aktien'] > df['SMA'], 'Signal'] = 1

# Simulation
kapital_bot = START_KAPITAL
anteile_bot = kapital_bot / df['Gold'].iloc[0]
verlauf_bot = []
eingezahlt = START_KAPITAL
letzter_monat = df.index[0].month

for i in range(len(df)):
    if df.index[i].month != letzter_monat:
        eingezahlt += MONATLICHER_SPARPLAN
        anteile_bot += MONATLICHER_SPARPLAN / df['Gold'].iloc[i]
        letzter_monat = df.index[i].month
    verlauf_bot.append(anteile_bot * df['Gold'].iloc[i])

df['Bot_Depotwert'] = verlauf_bot
endwert = df['Bot_Depotwert'].iloc[-1]

# Metriken anzeigen
st.metric(label="🏆 Endwert invest2gether Halal-Bot", value=f"{endwert:,.2f} $", delta=f"Eingezahlt: {eingezahlt:,.2f} $")

# Grafik anzeigen
fig, ax = plt.subplots(figsize=(12, 4))
ax.plot(df.index, df['Bot_Depotwert'], color='#D4AF37', linewidth=2)
st.pyplot(fig)

# ==============================================================================
# 1. WARTELISTE (EMAIL & NAME)
# ==============================================================================
st.markdown("---")
st.subheader("🚀 Werden Sie Teil der Beta-Phase")

with st.form(key='waitlist_form', clear_on_submit=True):
    col_name, col_email = st.columns(2)
    with col_name:
        kunden_name = st.text_input("Ihr Name")
    with col_email:
        kunden_email = st.text_input("Ihre E-Mail-Adresse")
    submit_button = st.form_submit_button(label='Jetzt Beta-Zugang sichern ➔')
    
    if submit_button and kunden_name and kunden_email:
        st.balloons()
        st.success("Erfolgreich eingetragen!")

# ==============================================================================
# 2. SADAQAH PROJEKTE (DIREKT DARUNTER)
# ==============================================================================
st.markdown("---")
st.markdown("<h2 style='text-align: center; color: #D4AF37; font-family: serif;'>🌱 1. Investment: Sadaqah Jariyah Projekte</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>„Besitz wird durch Sadaqah niemals gemindert.“ — Prophet Mohammed ﷺ</p>", unsafe_allow_html=True)

p1, p2, p3 = st.columns(3)

with p1:
    st.image("https://wikimedia.org", use_container_width=True)
    st.markdown("### 💧 1. Brunnen bauen")
    if st.button("Auswählen", key="b1"): st.toast("Ausgewählt!", icon="💧")
        
with p2:
    st.image("https://wikimedia.org", use_container_width=True)
    st.markdown("### 🧒 2. Waisenhäuser")
    if st.button("Auswählen", key="b2"): st.toast("Ausgewählt!", icon="🧒")
        
with p3:
    st.image("https://wikimedia.org", use_container_width=True)
    st.markdown("### 🇲🇳 3. Moschee errichten")
    if st.button("Auswählen", key="b3"): st.toast("Ausgewählt!", icon="🕌")
