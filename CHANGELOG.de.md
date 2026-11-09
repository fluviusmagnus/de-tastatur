# Versionsverlauf

[中文](CHANGELOG.md) | [English](CHANGELOG.en.md) | **Deutsch**

Dieses Projekt verwendet die Versionsnummernform von
[Semantic Versioning](https://semver.org/lang/de/).
`CFBundleShortVersionString` in `Contents/Info.plist` ist die öffentliche
Versionsnummer.

## [1.2.0] - 2026-11-09

Erste öffentliche Veröffentlichung unter Beibehaltung der bestehenden
Bundle-Version 1.2.0.

### Hinzugefügt

- German E2 (ANSI) und German E1 (ISO) als native macOS-`.bundle`-Eingabequellen.
- QWERTZ-Tastenbelegung, linke und rechte Option-Taste als AltGr sowie erweiterte
  Auswahl mit Option+F.
- Vollständige Tottasten-Zustandsmaschine: Akzente, mehrfache Akzente, IPA,
  griechische Buchstaben, mathematische Zeichen, Brüche, hoch- und tiefgestellte
  Zeichen.
- Offline-Generator und 31 Unit-Tests.
- Nativer macOS-`UCKeyTranslate`-Prüfer und Prüfvektoren.
- Anleitung zur chinesischen Satzzeichenanpassung für Squirrel / Rime.
- Werkzeuge und Aufzeichnungen zur Migration und gezielten Reparatur von
  Eingabequellen.

### Prüfung

- 31 Offline-Tests bestanden.
- E2: 5.024 native Prüfungen bestanden, Hauptsprache `de`.
- E1: 5.026 native Prüfungen bestanden, Hauptsprache `de`.

### Bekannte Einschränkungen

- Keine manuelle Prüfung jeder einzelnen Taste physischer Tastaturen,
  Anwendungstastenkürzel oder des Anmeldefensters / FileVault / der
  Passwortdialoge.
- Der E1-ISO-Pfad wurde über die System-API simuliert, nicht mit einer physischen
  ISO-Tastatur geprüft.
- Nicht auf Intel-Macs oder älteren macOS-Versionen geprüft.
