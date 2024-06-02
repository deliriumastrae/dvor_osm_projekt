import streamlit as st
from menu import menu
st.set_page_config(page_title="EasyPressure", page_icon="🫀",layout="wide")
menu(authenticated=True)

def main():
    st.title("Willkommen zur Einführung in EasyPressure ")

    st.write("""
    Diese Application wurde speziell entwickelt, um Benutzern das Eingeben, Verwalten und Überwachen ihrer Blutdruck- und Pulswerte zu erleichtern. Mit EasyPressure können Sie nicht nur Ihre Gesundheitsdaten effektiv verfolgen, sondern diese auch direkt an Ihren Arzt weiterleiten, was eine nahtlose Kommunikation und bessere medizinische Betreuung ermöglicht.
    """)

    st.header("Funktionen der Anwendung:")

    st.markdown("""
    - **Eingabe von Blutdruck- und Pulswerten**: Geben Sie Ihre Werte sicher und einfach ein und speichern Sie diese in Ihrem Benutzerprofil. Diese Daten helfen Ihnen, ein persönliches Gesundheitsregister zu führen.
    - **Verfolgung von Blutdruck- und Pulswerten**: Überwachen Sie Ihre Werte über die Zeit, um Trends und signifikante Änderungen in Ihrem Gesundheitszustand zu erkennen. Diese Funktion ist besonders wertvoll, um präventive Maßnahmen zu ergreifen oder die Wirksamkeit von medizinischen Behandlungen zu beurteilen.
    - **Datenvisualisierung**: Nutzen Sie fortschrittliche Diagramme und Grafiken, um Ihre Blutdruck- und Pulswerte anschaulich darzustellen. Unsere visuellen Tools sind darauf ausgerichtet, Ihnen ein klares Bild Ihrer Gesundheitsentwicklung zu vermitteln.
    - **Benutzerfreundliche Oberfläche**: Die Anwendung zeichnet sich durch eine intuitive und leicht zugängliche Benutzeroberfläche aus. Dank der Verwendung von Streamlit integrieren wir interaktive Elemente wie Slider, Dropdown-Menüs und Schaltflächen, die die Benutzererfahrung signifikant verbessern.
    - **Sichere Datenübermittlung an Ärzte**: Mit nur wenigen Klicks können Sie Ihre Gesundheitsdaten sicher an Ihren Arzt übermitteln. Diese Funktion fördert eine effektive Kommunikation zwischen Ihnen und Ihrem medizinischen Betreuer und unterstützt eine datenbasierte Diagnostik und Behandlung.
    """)

    st.info("Durch die Nutzung von EasyPressure können Sie aktiv an der Überwachung und Verbesserung Ihrer Gesundheit mitwirken, während Sie gleichzeitig von einer Technologie profitieren, die Sicherheit, Benutzerfreundlichkeit und Effizienz in den Vordergrund stellt.")
if __name__ == '__main__':
    main()