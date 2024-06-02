# Produkt Roadmap für Blutdruck- und Pulswerte-Anwendung

# EasyPressure

## Version Demo (23.05.24) - Grundlegende Funktionalität

### Funktionen:
- **Eingabe von Blutdruck- und Pulswerten**
  - Benutzer können ihre Blutdruck- und Pulswerte in die Anwendung eingeben und speichern.
- **Verfolgung von Blutdruck- und Pulswerten**
  - Benutzer können ihre eingegebenen Blutdruck- und Pulswerte im Laufe der Zeit verfolgen und Trends erkennen.
- **Datenvisualisierung**
  - Implementierung grundlegender Diagramme und Grafiken zur Visualisierung der eingegebenen Daten.
- **Benutzerfreundliche Oberfläche**
  - Integration von interaktiven Elementen wie Slider, Dropdown-Menüs und Schaltflächen für eine verbesserte Benutzererfahrung.

### Meilensteine:
- Design und Entwicklung der Benutzeroberfläche 
- Implementierung der Datenbankstruktur für die Speicherung von Blutdruck- und Pulswerten
- Entwicklung der Funktionen für die Eingabe und Verfolgung von Blutdruck- und Pulswerten
- Integration von Datenvisualisierungen zur besseren Interpretation der Daten 
- Testphase und Fehlerbehebung 

## Version Fertig(03.06.24) - Erweiterte Funktionen 

### Funktionen:
- **Benutzerprofile**
  - Möglichkeit für Benutzer, persönliche Profile anzulegen und ihre gespeicherten Daten zu verwalten.
- **Export von Daten**
  - Option zum Exportieren der gespeicherten Daten für die Verwendung in anderen Anwendungen oder für den Austausch mit medizinischen Fachkräften.
- **Anpassbare Datenvisualisierungen**
  - Erweiterte Optionen zur Anpassung und Konfiguration von Diagrammen und Grafiken.

### Meilensteine:
- Entwicklung von Benutzerprofilen und Profilverwaltungsfunktionen  
- Hinzufügen von Exportfunktionen für Daten 
- Verbesserung der Anpassungsmöglichkeiten für Datenvisualisierungen 
- Integration von Feedbackmechanismen für Benutzer 


Diese Roadmap bietet einen Überblick über die geplanten Entwicklungsphasen und Funktionserweiterungen für die Blutdruck- und Pulswerte-Anwendung. Sie wird regelmäßig aktualisiert.

### Analyse der Projektdateien

#### Datei `requirements.txt`
Enthält Abhängigkeiten für das Projekt:
- **streamlit** - Zur Erstellung von Webanwendungen.
- **PyGithub==1.55** - Für die Interaktion mit der GitHub API.
- **bcrypt** - Zum Hashen von Passwörtern.
- **PyJWT>=2.0.0** und **python-jose>=3.3.0** - Für die Arbeit mit JWT.
- **pandas** - Zur Datenanalyse.
- **python-dotenv** - Zum Laden von Umgebungsvariablen.
- **plotly==5.5.0** und **kaleido==0.2.1** - Zur Visualisierung von Daten und zum Export von Grafiken.
- **streamlit_cookies_controller** - Zur Verwaltung von Cookies in Streamlit.
- **reportlab** und **Pillow** - Zur Arbeit mit PDF und Bildern.

#### Datei `menu.py`
Verwaltet das Seitenmenü der Webanwendung:
- **sidebar_button()**: Fügt eine Schaltfläche zur Seitenleiste hinzu, die FontAwesome und CSS für einen einheitlichen Stil verwendet.
- **authenticated_menu()**: Zeigt ein Menü für authentifizierte Benutzer mit verschiedenen Links und einer Abmeldefunktion.
- **unauthenticated_menu()**: Leitet nicht authentifizierte Benutzer zur Anmeldeseite weiter.
- **menu(authenticated)**: Bestimmt, welches Menü angezeigt wird, je nach Authentifizierungsstatus.

#### Datei `app.py`
Hauptausführbare Datei der Webanwendung:
- **Seiteneinrichtung**: Legt den Titel und das Icon der Seite fest.
- **Authentifizierungslogik**: Zeigt Optionen für Anmeldung und Registrierung an und aktiviert entsprechende Funktionen.
- **Integration mit .env**: Lädt Umgebungsvariablen, um die Sicherheit zu erhöhen.

#### Datei `archiv.py`
Verwaltet die Archivierung von Benutzerdaten:
- **Datenaktualisierung**: Benutzer können Daten direkt im Archiv ändern.
- **Datendarstellung**: Dynamische Erstellung von Benutzeroberflächenelementen für jede Aufzeichnung.

#### Datei `create_diagram.py`
Erstellt Diagramme basierend auf Benutzerdaten:
- **Diagrammerstellung**: Visualisiert Veränderungen im Gesundheitszustand.
- **Export in PDF**: Vereinfacht das Speichern und Teilen von Analyseergebnissen.

#### Datei `data_entry.py`
Verwaltet die Dateneingabe des Benutzers:
- **Universelle Dateneingabe**: Auswahl zwischen Schieberegler und numerischer Eingabe.
- **Datenbeschaffungslogik**: Speichert Daten unmittelbar nach der Eingabe.

#### Datei `important_variables.py`
Enthält wichtige Variablen und Einstellungen:
- **GITHUB_TOKEN, JWT_KEY**: Tokens für Authentifizierung und Arbeit mit GitHub und JWT.
- **REPO_NAME, VALUE_FILE, LOGIN_FILE, VALUE_COLUMNS, LOGIN_COLUMNS**: Konstanten für Repository- und Dateinamen sowie Datenstrukturen.

#### Datei `auth_utilities.py`
Funktionen für die Benutzerauthentifizierung:
- **generateAuthToken(username)**: Erstellt ein Token für authentifizierte Benutzer.
- **decode_auth_token(token)**: Dekodiert und gibt Informationen aus dem Token zurück.
- **get_auth_token()**: Gibt das aktuelle Authentifizierungstoken aus der Sitzung zurück.

#### Datei `data_repo_utilities.py`
Funktionen für die Arbeit mit Benutzerdaten über die GitHub API:
- **get_user_data(username, repo_name, file_name, columns)**: Ruft Benutzerdaten von GitHub ab.
- **update_user_data(username, repo_name, file_name, columns, new_data)**: Aktualisiert Benutzerdaten auf GitHub.
- **update_value_data(...) und add_user_to_github(...)**: Zusätzliche Funktionen zur Aktualisierung von Wertdaten und zum Hinzufügen neuer Benutzer.

#### Datei `log_reg.py`
Verarbeitet Login- und Registrierungsprozesse:
- **login()**: Authentifiziert den Benutzer und richtet die Sitzung ein.
- **register()**: Registriert einen neuen Benutzer mit Datenvalidierung.
- **authenticate(username, password)**: Überprüft Benutzernamen und Passwort.