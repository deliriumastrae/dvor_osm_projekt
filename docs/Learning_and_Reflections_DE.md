
# Lernen und Reflexionen: EasyPressure Projekt

## Projektübersicht
Das EasyPressure-Anwendungsprojekt ist darauf ausgelegt, Blutdruck- und Pulswerte von Benutzern zu überwachen und zu analysieren. Es bietet Funktionen zum Eingeben, Speichern, Verfolgen und Visualisieren von Daten. Das Ziel ist es auch, die Übertragung von Daten an medizinische Fachkräfte zu erleichtern und unterstützt den Export von Daten für die weitere Verwendung. Die Entwicklung ist in Versionen strukturiert, beginnend mit grundlegenden Funktionen in Version 1.0 bis hin zu erweiterten Funktionen in nachfolgenden Releases.

## Schlüsseltechnologien und Abhängigkeiten
- **Streamlit**: Wird verwendet, um die Web-Oberfläche der Anwendung zu erstellen.
- **Pandas** und **Plotly**: Für die Datenverarbeitung und -visualisierung verwendet.
- **bcrypt** und **PyJWT**: Sichern Sicherheit durch Verschlüsselung und Authentifizierung.
- **Python-dotenv**: Verwaltet Umgebungs- und vertrauliche Datenspeicherung.

## Persönliches Lernen und Entwicklung
- Wir habn gelernt, wie man eine benutzerfreundliche Webanwendung entwickelt und wie wichtig es ist, die Bedürfnisse der Endbenutzer bei der Entwicklung von Software zu berücksichtigen.
- Die Bedeutung von Datenvisualisierung und wie sie verwendet wird, um Gesundheitstrends und Muster besser zu verstehen.

## Herausforderungen und Lösungen
- Wir stießen auf Herausforderungen beim Implementieren der Datenbankanbindung. Durch Online-Recherchen, Austausch mit erfahrenen Entwicklern und selbstvertandlich ChatGPT fanden wir effektive Lösungsansätze.
- Sicherheitsbedenken wurden durch das Erlernen und Implementieren von Authentifizierungsprotokollen wie JWT und bcrypt adressiert.

### Probleme und Lösungen
1. **Verlust des Authentifizierungstokens bei Seitenaktualisierung**: In der aktuellen Version des Projekts geht das Authentifizierungstoken bei der Verwendung von `st.sessionstate` verloren. Auf Empfehlung von Dominik haben wir das Projekt auf diese Version zurückgesetzt. Zuvor haben wir das Token mit Hilfe von `CookieController` in Cookies gespeichert. Dabei wurde das Token anscheinend auf dem Streamlit-Server gespeichert, so dass der Benutzer als erfolgreich authentifiziert galt, obwohl er weder Passwort noch Login eingegeben hatte.
2. **Verzögerte Anwendung des benutzerdefinierten Themes**: Manchmal wird mein benutzerdefiniertes Theme nicht sofort angewendet, sondern erst nach der Authentifizierung und einer Seitenaktualisierung. Dieses Problem scheint mit meinem Browser (Chrome) zusammenzuhängen.
3. **Fehlerhafte Speicherung von Diagrammen**: Die Diagramme wurden ohne zusätzliche Verarbeitung nicht korrekt gespeichert. Um dieses Problem zu lösen, mussten wir `kaleido` verwenden.
4. **Anpassung der Schaltfläche, die die Sidebar öffnet und schließt**: Die Anpassung der Schaltfläche mit HTML verursachte ebenfalls Schwierigkeiten. Lokal funktioniert alles wie erwartet, aber in der Cloud kann es zu Instabilitäten kommen.

### Zusätzliche Hinweise der Entwickler
1. **Anpassung des Interfaces für ältere Menschen**: Wir haben das Interface speziell für ältere Benutzer angepasst, indem wir größeren und fetteren Text und umgestaltete Schaltflächen verwendet haben. Diese Änderungen wurden durch HTML implementiert, um die Lesbarkeit und Bedienbarkeit zu verbessern.
2. **Datenversandfunktion**: Die Funktion zum Versenden von Daten wurde so implementiert, dass sie sicher und benutzerfreundlich ist. Alternativ hätten wir Zugriff auf das E-Mail-Konto des Benutzers benötigt, um automatisch Diagramme anhängen zu können, was den Zugang zu persönlichen Passwörtern des Benutzers erfordert hätte.
3. **Anzeigenormwerte**: Die App zeigt keine Normalwerte für Messdaten an, um keine diagnostische Verantwortung zu übernehmen. Die Interpretation der Daten sollte von einem Arzt vorgenommen werden, um die medizinische Genauigkeit und Verantwortlichkeit zu gewährleisten.

## Zukünftige Verbesserungen und Lektionen
- Für zukünftige Versionen könnte man die Interaktionsmöglichkeiten zu erweitern und mehr personalisierte Feedbackoptionen für Benutzer zu integrieren.
- Wir haben die Bedeutung von gründlichem Testen und Feedback-Einholung gelernt, um ein qualitativ hochwertiges Produkt sicherzustellen.

