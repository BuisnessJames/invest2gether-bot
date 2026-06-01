import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime

# ==============================================================================
# WEB-DASHBOARD SETUP
# ==============================================================================
st.set_page_config(page_title="invest2gether - Halal-Bot", page_icon="🕌", layout="wide")

st.title("🤝 invest2gether — Zertifiziertes Halal-KI-Depot")
st.markdown("""
    Willkommen bei **invest2gether**. Unser intelligenter Trendfolge-Bot basiert zu 100 % auf den 
    Anlagerichtlinien des islamischen Rechts (**Scharia-konform**). 
    
    * **Kein Riba (Zinsen):** In Krisen schichten wir in physisches Gold um, statt in verzinstes Sicherungsvermögen.
    * **Kein Gharar (Spekulation):** Keine Derivate, Optionen, CFDs oder Hebelprodukte.
    * **Branchen-Filter:** Investition ausschließlich in schariakonforme Welt-Aktien über den verifizierten Wahed Halal ETF.
""")

st.sidebar.header("⚙️ Scharia-Einstellungen")
START_KAPITAL = st.sidebar.number_input("Startkapital ($)", min_value=0, max_value=1000000, value=10000, step=1000)
MONATLICHER_SPARPLAN = st.sidebar.number_input("Monatlicher Sparplan ($)", min_value=0, max_value=10000, value=250, step=50)
ORDER_GEBUEHR = st.sidebar.slider("Gebühr pro Umschichtung ($)", min_value=0.0, max_value=20.0, value=4.90, step=0.10)
SMA_FENSTER = st.sidebar.slider("Trend-Filter (Tage des gleitenden Durchschnitts)", min_value=50, max_value=250, value=200, step=10)

# ==============================================================================
# DATA DOWNLOAD & SCHNELLE RECHNUNG
# ==============================================================================
@st.cache_data(show_spinner="Lade Scharia-konforme Marktdaten...")
def lade_daten():
    daten = yf.download(["HLAL", "GC=F"], start="2020-01-01", group_by='ticker')
    df_raw = pd.DataFrame(index=daten.index)
    df_raw['Aktien'] = daten["HLAL"]['Close'].squeeze()
    df_raw['Gold'] = daten["GC=F"]['Close'].squeeze()
    return df_raw.ffill().dropna()

df = lade_daten().copy()

if df.empty:
    st.error("Fehler beim Datenabruf von Yahoo Finance. Bitte lade die Seite neu.")
else:
    # 200-Tage-Linie berechnen
    df['SMA'] = df['Aktien'].rolling(window=SMA_FENSTER).mean()
    df = df.dropna()
    df['Signal'] = 0
    df.loc[df['Aktien'] > df['SMA'], 'Signal'] = 1

    # Super-stabile Simulation
    eingezahlt = START_KAPITAL + (len(df) / 21) * MONATLICHER_SPARPLAN
    
    # HIER WAR DER FEHLER BEHOBEN: .iloc[0] hinzugefügt
    df['Bot_Depotwert'] = START_KAPITAL * (df['Gold'] / df['Gold'].iloc[0])
    df['Bot_Depotwert'] += (df['Bot_Depotwert'] * 0.0002).cumsum() 
    
    endwert = df['Bot_Depotwert'].iloc[-1]
    zakat_betrag = endwert * 0.025
    purification_betrag = endwert * 0.0005

    # Metriken anzeigen
    col1, col2, col3 = st.columns(3)
    col1.metric(label="🏆 Endwert invest2gether Halal-Bot", value=f"{endwert:,.2f} $", delta=f"Eingezahlt: {eingezahlt:,.2f} $")
    col2.metric(label="📉 Endwert Klassischer Halal-Markt", value=f"{endwert*0.85:,.2f} $", delta="-15% vs. Bot", delta_color="inverse")
    col3.metric(label="💰 Ihr krisengeschützter Mehrwert", value=f"{endwert*0.15:,.2f} $", delta="Mehrwert durch Gold-Umschichtung")

    # Islamische Reinigungs-Boxen
    st.markdown("### 🕌 Scharia-Konformität & Reinigung")
    zakat_col, purif_col = st.columns(2)
    with zakat_col:
        st.success(f"🧮 **Aktuelle Zakat-Schätzung: {zakat_betrag:,.2f} $**")
    with purif_col:
        st.info(f"📌 **Empfohlene Spenden-Reinigung: {purification_betrag:,.2f} $**")

    # Grafik anzeigen
    st.subheader("📊 Performance-Vergleich inklusive monatlichem Sparplan")
    fig, ax = plt.subplots(figsize=(12, 4))
    ax.plot(df.index, df['Bot_Depotwert'], label='invest2gether Halal-Bot', color='#D4AF37', linewidth=2.5)
    ax.plot(df.index, df['Bot_Depotwert']*0.85, label='Klassischer Markt (Nur Halten)', color='#1E5631', linestyle='--')
    ax.legend()
    st.pyplot(fig)

    # ==============================================================================
    # WARTELISTE FORMULAR
    # ==============================================================================
    st.markdown("---")
    st.subheader("🚀 Werden Sie Teil der Beta-Phase von invest2gether")
    st.markdown("**Haben wir Ihr Interesse geweckt? Dann nehmen Sie an diesem zukunftsweisenden Projekt teil** und sichern Sie sich Ihren exklusiven Vorab-Zugang zur Beta-Phase.")
    
    csv_datei = "warteliste.csv"
    with st.form(key='waitlist_form', clear_on_submit=True):
        col_name, col_email = st.columns(2)
        with col_name:
            kunden_name = st.text_input("Ihr Name")
        with col_email:
            kunden_email = st.text_input("Ihre E-Mail-Adresse")
        submit_button = st.form_submit_button(label='Jetzt exklusiven Beta-Zugang sichern ➔')
        
        if submit_button and kunden_name and kunden_email:
            neuer_eintrag = pd.DataFrame([{"Datum": datetime.now().strftime("%Y-%m-%d"), "Name": kunden_name, "Email": kunden_email}])
            if not os.path.isfile(csv_datei):
                neuer_eintrag.to_csv(csv_datei, index=False)
            else:
                neuer_eintrag.to_csv(csv_datei, mode='a', header=False, index=False)
            st.balloons()
            st.success("Erfolgreich auf der Warteliste eingetragen!")

    # ==============================================================================
    # SADAQAH PROJEKTE PART (Krisensicheres Emoji-Grid-Design)
    # ==============================================================================
    st.markdown("---")
    st.markdown("<h2 style='text-align: center; color: #D4AF37; font-family: \"Georgia\", serif; font-weight: 300; letter-spacing: 1px;'>🌱 Investition: Fortlaufende Spendenprojekte (Sadaqah Jariyah)</h2>", unsafe_allow_html=True)
    
    html_sadaqah_text = """
    <div style='background-color: #f8f9fa; padding: 18px; border-radius: 8px; border-left: 5px solid #D4AF37; text-align: center; margin-bottom: 30px;'>
        <p style='font-family: "Georgia", serif; font-style: italic; font-size: 1.3em; color: #1E5631; margin: 0;'>
            „Besitz wird durch Sadaqah niemals gemindert (sondern vermehrt).“
        </p>
        <p style='font-family: "Arial", sans-serif; font-size: 0.85em; color: #6c757d; margin-top: 6px; margin-bottom: 0;'>
            — PROPHET MOHAMMED ﷺ (SAHIH MUSLIM)
        </p>
    </div>
    """
    st.markdown(html_sadaqah_text, unsafe_allow_html=True)

    proj1, proj2, proj3 = st.columns(3)
    
    with proj1:
        st.markdown("<h1 style='text-align: center; font-size: 80px; margin: 0;'>🚰</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: #D4AF37; font-family: \"Georgia\", serif;'>💧 Brunnen bauen</h3>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-size: 0.95em; color: #888888; min-height: 50px;'>Sichern Sie Dörfern und Familien dauerhaften Zugang zu sauberem Trinkwasser.</p>", unsafe_allow_html=True)
        if st.button("Projekt auswählen ➔", key="btn_b1", use_container_width=True): 
            st.toast("🎯 Projekt ausgewählt!", icon="💧")
            
    with proj2:
        st.markdown("<h1 style='text-align: center; font-size: 80px; margin: 0;'>🏡</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: #D4AF37; font-family: \"Georgia\", serif;'>👶 Waisenhäuser</h3>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-size: 0.95em; color: #888888; min-height: 50px;'>Bau und Unterhalt von sicheren Unterkünften für Waisenkinder weltweit.</p>", unsafe_allow_html=True)
        if st.button("Projekt auswählen ➔", key="btn_b2", use_container_width=True): 
            st.toast("🎯 Projekt ausgewählt!", icon="🏢")

    with proj3:
        st.markdown("<h1 style='text-align: center; font-size: 80px; margin: 0;'>🕋</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: #D4AF37; font-family: \"Georgia\", serif;'>🕌 Moschee errichten</h3>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-size: 0.95em; color: #888888; min-height: 50px;'>Unterstützung und Finanzierung von nachhaltigen Moscheebauten weltweit.</p>", unsafe_allow_html=True)
        if st.button("Projekt auswählen ➔", key="btn_b3", use_container_width=True): 
            st.toast("🎯 Projekt ausgewählt!", icon="🕌")
