import streamlit as st
from menu import menu
st.set_page_config(page_title="EasyPressure", page_icon="🫀", layout="wide")
menu(authenticated=True)


def main():
    # Titel der Einführung
    st.title('Willkommen zur Einführung')

    # Einführungstext
    st.write("""
    Diese Anwendung ermöglicht es Benutzern, ihre Blutdruckwerte und Pulswerte einzugeben und zu verfolgen.
    Sie können die Werte eingeben und die Trends über die Zeit anzeigen lassen.
    
    
Funktionen der Anwendung:

**Eingabe von Blutdruck- und Pulswerten:** Benutzer können ihre Blutdruck- und Pulswerte in die Anwendung eingeben und verwalten.
             
**Verfolgung von Blutdruck- und Pulswerten:** Die Anwendung ermöglicht es Benutzern, ihre eingegebenen Blutdruck- und Pulswerte im Laufe der Zeit zu verfolgen. Sie können Trends erkennen und mögliche Veränderungen im Gesundheitszustand überwachen.
             
**Datenvisualisierung:** Die Anwendung bietet Funktionen zur Visualisierung der eingegebenen Daten, z.B. durch Diagramme oder Grafiken. Dadurch können Benutzer ihre Daten besser verstehen und interpretieren.
             
**Benutzerfreundliche Oberfläche:** Die Anwendung bietet eine benutzerfreundliche Oberfläche, die es Benutzern leicht macht, ihre Daten einzugeben, zu verfolgen und zu analysieren. Streamlit ermöglicht es, interaktive Elemente wie Slider, Dropdown-Menüs und Schaltflächen einzubinden, um die Benutzererfahrung zu verbessern.
    """)


if __name__ == '__main__':
    main()