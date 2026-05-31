import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime

# ==============================================================================
# WEB-DASHBOARD LAYOUT (Scharia-konformes Branding)
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

# Interaktive Regler für den Kunden
START_KAPITAL = st.sidebar.number_input("Startkapital ($)", min_value=0, max_value=1000000, value=10000, step=1000)
MONATLICHER_SPARPLAN = st.sidebar.number_input("Monatlicher Sparplan ($)", min_value=0, max_value=10000, value=250, step=50)
ORDER_GEBUEHR = st.sidebar.slider("Gebühr pro Umschichtung ($)", min_value=0.0, max_value=20.0, value=4.90, step=0.10)
SMA_FENSTER = st.sidebar.slider("Trend-Filter (Tage des gleitenden Durchschnitts)", min_value=50, max_value=250, value=200, step=10)

# ==============================================================================
# DATA DOWNLOAD & BERECHNUNG (Stabile Halal-Daten via HLAL)
# ==============================================================================
ticker_halal_aktien = "HLAL"  
ticker_gold = "GC=F"         

@st.cache_data(show_spinner="Lade Scharia-konforme Marktdaten herunter...")
def lade_daten():
    daten = yf.download([ticker_halal_aktien, ticker_gold], start="2020-01-01", group_by='ticker')
    aktien_close = daten[ticker_halal_aktien]['Close'].squeeze()
    gold_close = daten[ticker_gold]['Close'].squeeze()
    
    df_raw = pd.DataFrame(index=daten.index)
    df_raw['Aktien'] = aktien_close
    df_raw['Gold'] = gold_close
    return df_raw.ffill().dropna()

df = lade_daten().copy()

# Sicherheitsprüfung
if df.empty:
    st.error("Fehler beim Datenabruf von Yahoo Finance. Bitte lade die Seite neu.")
else:
    # Strategie-Logik
    df['SMA'] = df['Aktien'].rolling(window=SMA_FENSTER).mean()
    df = df.dropna()

    df['Signal'] = 0
    df.loc[df['Aktien'] > df['SMA'], 'Signal'] = 1

    # Backtest-Schleife mit Sparplan-Logik
    kapital_bot = START_KAPITAL
    kapital_bh = START_KAPITAL
    
    anteile_bot = kapital_bot / df['Gold'].iloc
    anteile_bh = kapital_bh / df['Aktien'].iloc
    
    gebuehren_gesamt = 0.0
    position = "Gold"  
    letztes_signal = 0  
    
    verlauf_bot = []
    verlauf_bh = []
    eingezahltes_kapital = START_KAPITAL
    
    letzter_monat = df.index.month

    for i in range(len(df)):
        aktuelles_datum = df.index[i]
        aktueller_monat = aktuelles_datum.month
        kurs_aktien = df['Aktien'].iloc[i]
        kurs_gold = df['Gold'].iloc[i]
        
        if aktueller_monat != letzter_monat:
            eingezahltes_kapital += MONATLICHER_SPARPLAN
            
            if position == "Aktien":
                anteile_bot += MONATLICHER_SPARPLAN / kurs_aktien
            else:
                anteile_bot += MONATLICHER_SPARPLAN / kurs_gold
                
            anteile_bh += MONATLICHER_SPARPLAN / kurs_aktien
            letzter_monat = aktueller_monat
            
        aktuelles_signal = df['Signal'].iloc[i]
        
        if aktuelles_signal != letztes_signal:
            gebuehren_gesamt += ORDER_GEBUEHR
            if aktuelles_signal == 1:
                wert_in_gold = anteile_bot * kurs_gold
                kapital_bot = wert_in_gold - ORDER_GEBUEHR
                anteile_bot = kapital_bot / kurs_aktien
                position = "Aktien"
            else:
                wert_in_aktien = anteile_bot * kurs_aktien
                kapital_bot = wert_in_aktien - ORDER_GEBUEHR
                anteile_bot = kapital_bot / kurs_gold
                anteile_bot = kapital_bot / kurs_gold
                position = "Gold"
            letztes_signal = aktuelles_signal
            
        if position == "Aktien":
            aktueller_wert_bot = anteile_bot * kurs_aktien
        else:
            aktueller_wert_bot = anteile_bot * kurs_gold
            
        aktueller_wert_bh = anteile_bh * kurs_aktien
        
        verlauf_bot.append(aktueller_wert_bot)
        verlauf_bh.append(aktueller_wert_bh)

    df['Bot_Depotwert'] = verlauf_bot
    df['Buy_Hold_Aktien'] = verlauf_bh

    endwert_bot = df['Bot_Depotwert'].iloc[-1]
    endwert_bh = df['Buy_Hold_Aktien'].iloc[-1]
    mehrwert = endwert_bot - endwert_bh

    zakat_betrag = endwert_bot * 0.025
    purification_betrag = endwert_bot * 0.0005  

    # ==============================================================================
    # METRIKEN ANZEIGEN
    # ==============================================================================
    col1, col2, col3 = st.columns(3)
    col1.metric(label="🏆 Endwert invest2gether Halal-Bot", value=f"{endwert_bot:,.2f} $", delta=f"Eingezahlt: {eingezahltes_kapital:,.2f} $")
    col2.metric(label="📉 Endwert Klassischer Halal-Markt", value=f"{endwert_bh:,.2f} $", delta=f"Differenz zum Bot", delta_color="inverse")
    col3.metric(label="💰 Ihr krisengeschützter Mehrwert", value=f"{mehrwert:,.2f} $", delta="Mehrwert durch KI-Umschichtung")

    # ==============================================================================
    # ISLAMISCHE REINIGUNGS-BOXEN
    # ==============================================================================
    st.markdown("### 🕌 Scharia-Konformität & Reinigung")
    zakat_col, purif_col = st.columns(2)
    
    with zakat_col:
        st.success(f"🧮 **Aktuelle Zakat-Schätzung: {zakat_betrag:,.2f} $**")
        st.caption("Entspricht den verpflichtenden 2,5 % Abgabe auf Ihr ruhendes Vermögen. Diese Reinigung sichert den Segen (*Barakah*) Ihres Kapitals.")
        
    with purif_col:
        st.info(f"📌 **Empfohlene Spenden-Reinigung: {purification_betrag:,.2f} $**")
        st.caption("Berechnete 0,05 % Reinigungssumme für unvermeidbare minimale Zinserträge der im Welt-ETF enthaltenen Großkonzerne.")

    # ==============================================================================
    # GRAFIK ANZEIGEN
    # ==============================================================================
    st.subheader("📊 Performance-Vergleich inklusive monatlichem Sparplan")
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(df.index, df['Bot_Depotwert'], label='invest2gether Halal-Bot (Aktien/Gold)', color='#D4AF37', linewidth=2.5)
    ax.plot(df.index, df['Buy_Hold_Aktien'], label='Wahed Halal ETF (Nur Halten)', color='#1E5631', linestyle='--')
    ax.set_ylabel('Depotwert in $')
    ax.grid(True, linestyle=':', alpha=0.6)
    ax.legend(facecolor='#f0f2f6')
    st.pyplot(fig)

    # ==============================================================================
    # INTERAKTIVE WARTELISTE
    # ==============================================================================
    st.markdown("---")
    st.subheader("🚀 Werden Sie Teil der Beta-Phase von invest2gether")
    st.markdown("Haben wir Ihr Interesse geweckt? Tragen Sie sich unverbindlich auf unsere Warteliste ein, um den offiziellen Start nicht zu verpassen.")
    
    csv_datei = "warteliste.csv"
    
    with st.form(key='waitlist_form', clear_on_submit=True):
        col_name, col_email = st.columns(2)
        with col_name:
            kunden_name = st.text_input("Ihr Name")
        with col_email:
            kunden_email = st.text_input("Ihre E-Mail-Adresse")
            
        submit_button = st.form_submit_button(label='Jetzt exklusiven Beta-Zugang sichern ➔')
        
        if submit_button:
            if kunden_name and kunden_email:
                neuer_eintrag = pd.DataFrame([{
                    "Datum": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Name": kunden_name,
                    "Email": kunden_email
                }])
                
                if not os.path.isfile(csv_datei):
                    neuer_eintrag.to_csv(csv_datei, index=False)
                else:
                    neuer_eintrag.to_csv(csv_datei, mode='a', header=False, index=False)
                    
                st.balloons()
                st.success(f"Salam {kunden_name}! Vielen Dank für Ihr Vertrauen. Sie wurden auf der Warteliste eingetragen.")
            else:
                st.warning("Bitte füllen Sie sowohl den Namen als auch die E-Mail-Adresse aus.")

    # ==============================================================================
    # SADAQAH JARIYAH & JENSEITS-INVESTMENT (Gereinigte Einzeiler-Variante)
    # ==============================================================================
    st.markdown("---")
    st.markdown("<h2 style='text-align: center; color: #D4AF37;'>🌱 Das ultimative Investment: Sadaqah Jariyah</h2>", unsafe_allow_html=True)

    # Das grüne Banner komplett als einzeiliger String formatiert, um Fehler zu vermeiden
