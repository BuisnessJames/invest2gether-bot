    # ==============================================================================
    # NEU: SADAQAH JARIYAH & JENSEITS-INVESTMENT (Global Vision)
    # ==============================================================================
    st.markdown("---")
    st.markdown("<h2 style='text-align: center; color: #D4AF37;'>🌱 Das ultimative Investment: Sadaqah Jariyah</h2>", unsafe_allow_html=True)
    
    # Der weise Spruch / Hadith im Zentrum
    html_hadith = """
    <div style='background-color: #1E5631; padding: 20px; border-radius: 10px; text-align: center; color: white;'>
        <h4 style='margin: 0;'>„Der Kluge investiert nicht nur in sein Diesseits, sondern baut Vermögen für sein Jenseits auf.“</h4>
        <p style='font-style: italic; margin-top: 10px; font-size: 0.9em;'>
            Der Prophet Mohammed (s.a.w.) sagte: „Wenn der Mensch stirbt, schneiden sich seine Taten von ihm ab, 
            außer in drei Fällen: Eine fortlaufende Spende (Sadaqah Jariyah), Wissen, von dem Nutzen gezogen wird, 
            oder ein rechtschaffenes Kind, das für ihn betet.“ (Sahih Muslim)
        </p>
    </div>
    """
    st.markdown(html_hadith, unsafe_allow_html=True)
    
    st.markdown("<br><p style='text-align: center;'>Bringen Sie Ihre Rendite aus der digitalen in die reale Welt. Sobald invest2gether offiziell startet, können Sie Ihre monatliche Dividenden-Reinigung oder Zakat per Mausklick direkt in nachhaltige, reale Projekte fließen lassen:</p>", unsafe_allow_html=True)
    
    # 3 Spalten für reale, globale Hilfsprojekte
    proj1, proj2, proj3 = st.columns(3)
    
    with proj1:
        st.markdown("### 💧 1. Nachhaltiger Brunnenbau")
        st.caption("Sichern Sie Dörfern dauerhaften Zugang zu sauberem Trinkwasser. Jedes Mal, wenn ein Mensch oder ein Tier davon trinkt, läuft Ihr Hasanat-Konto im Jenseits vollautomatisch weiter.")
        st.button("Projekt einsehen (Beta)", key="b1", disabled=True)
        
    with proj2:
        st.markdown("### 🧒 2. Waisenkind-Patenschaften")
        st.caption("Übernehmen Sie die Verantwortung für Kleidung, Nahrung und schariakonforme Bildung eines Kindes. Der Prophet (s.a.w.) sagte, dass er und derjenige, der sich einer Waise annimmt, im Paradies so nah wie zwei Finger sein werden.")
        st.button("Projekt einsehen (Beta)", key="b2", disabled=True)
        
    with proj3:
        st.markdown("### 🕌 3. Bau von Bildungsstätten")
        st.caption("Investieren Sie in den Bau von Schulen und Gebetsstätten in Entwicklungsländern. Solange dort gelernt und gebetet wird, erhalten Sie die Belohnung für jede einzelne Niederwerfung.")
        st.button("Projekt einsehen (Beta)", key="b3", disabled=True)
