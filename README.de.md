# German E1 / E2 für macOS

[中文](README.md) | [English](README.en.md) | **Deutsch**

Zwei native macOS-Tastaturlayouts: **German E2 (ANSI)** und das alternative
**German E1 (ISO)**, beide als Eingabequellen unter **Deutsch** einsortiert.
Die Tastenpositionen folgen `de(e1)` / `de(e2)` aus Linux `xkeyboard-config`
2.48; Zeichen, Tottasten und die Zustandsmaschine für die erweiterte Auswahl
stammen aus den öffentlichen Layouttabellen von Windows `KBDGRE1.DLL` /
`KBDGRE2.DLL`.

Karabiner, ein Hintergrunddienst, eine Bedienungshilfen-Berechtigung oder eine
Laufzeitumgebung von Drittanbietern sind nicht erforderlich.

## Funktionen

- **Native Layout-Bundles**: Standard-`.bundle`-Eingabequellen mit
  `TISIntendedLanguage=de`, daher listet macOS sie unter Deutsch.
- **QWERTZ**: An der Position der US-Taste Y wird `z` eingegeben, an der Position
  der US-Taste Z `y`.
- **Beide Option-Tasten wirken als AltGr**; keine Emulation mit Control+Option.
- **Vollständige Tottastentabellen**: Akzente, mehrfache Akzente, IPA,
  griechische Buchstaben, mathematische Zeichen, Brüche, hoch- und tiefgestellte Zeichen.
- **Erweiterte Auswahl**: Option+F drücken, beide Tasten loslassen, dann die
  Ziel-Taste drücken. Für Großbuchstaben oder Zweitbelegungen zusätzlich Shift
  an der Ziel-Taste.
- **E2 ANSI** ist das Hauptlayout; **E1 ISO** ist für ISO-Tastaturen mit der
  zusätzlichen Taste.
- Reproduzierbare Generierung, Offline-Tests und ein nativer
  `UCKeyTranslate`-Prüfer für macOS.

## Unterstützter Bereich

Geprüfte Umgebung:

| Punkt | Wert |
| --- | --- |
| macOS | 27.2 (Build 26B123) |
| Hardware | Apple Silicon, `LMGetKbdType()` liefert 91 |
| Tastatur | Physische ANSI-Tastatur |
| Bundle-Version | 1.2.0 (siehe `Contents/Info.plist`) |

Noch nicht manuell geprüft: Intel-Macs, ältere macOS-Versionen, physische
ISO-/JIS-Tastaturen, externe Ziffernblöcke, Anmeldefenster / FileVault /
Passwortdialoge sowie anwendungsspezifische Tastenkürzel. Die E1-ISO-Prüfung
verwendet die System-API mit simulierten Tastaturtypen, keine physische
ISO-Tastatur. Siehe [`TESTING.md`](TESTING.md) (derzeit auf Chinesisch).

## Installation

### Variante 1: fertige Bundles verwenden

```sh
mkdir -p "$HOME/Library/Keyboard Layouts"
cp -R dist/GermanE2.bundle "$HOME/Library/Keyboard Layouts/"
cp -R dist/GermanE1.bundle "$HOME/Library/Keyboard Layouts/"   # nur bei Bedarf für die ISO-Ausweichversion
```

`dist/*.keylayout` sind Zwischendateien des Builds. **Installieren Sie das
gesamte `.bundle`, nicht die einzelnen Dateien.** Existiert am Zielort bereits
eine Datei mit demselben Namen, prüfen und sichern Sie sie zuerst, damit Sie
kein anderes benutzerdefiniertes Layout überschreiben.

### Variante 2: aus dem Quellcode bauen

Erfordert Python 3.9+; für die native Prüfung zusätzlich die Swift Command Line
Tools von macOS.

```sh
python3 tools/build_layout.py
python3 -m unittest discover -s tests -v
```

Der Build schreibt nur Dateien unter `dist/`; er installiert, registriert oder
wählt keine Eingabequelle aus. Kopieren Sie das Ergebnis anschließend wie in
Variante 1.

Damit macOS ein neu installiertes Layout sofort erkennt, registrieren Sie es
ausdrücklich (dies aktiviert oder wählt es nicht aus):

```sh
swift tools/verify_macos.swift dist/native-cases.json \
  --register "$HOME/Library/Keyboard Layouts/GermanE2.bundle"
swift tools/verify_macos.swift dist/native-cases-E1.json \
  --register "$HOME/Library/Keyboard Layouts/GermanE1.bundle"
```

## Aktivieren

1. **Systemeinstellungen → Tastatur → Texteingabe → Bearbeiten** öffnen.
2. Auf **＋ → Deutsch** klicken und **German E2 (ANSI)** oder
   **German E1 (ISO)** suchen.
3. Nach dem Hinzufügen über das Eingabemenü in der Menüleiste zum Layout wechseln.
4. Erscheint es noch nicht in der Liste, melden Sie sich ab und wieder an;
   starten Sie bei Bedarf neu.

Löschen Sie keine integrierten Layoutdateien. Ein benutzerdefiniertes Layout des
aktuellen Benutzers funktioniert nicht garantiert bei der FileVault-Entsperrung,
im Anmeldefenster oder in allen Passwortdialogen.

## Verwendung

### Auswahl zwischen E2 und E1

Auf ANSI-Hardware verwenden Sie **E2**. **E1** ist für ISO-Tastaturen gedacht:
Die linke Shift-Taste ist kürzer, daneben befindet sich eine zusätzliche
Zeichentaste.

| Position / Funktion | E2 ANSI | E1 ISO |
| --- | --- | --- |
| Zusätzliche Taste neben linker Shift | Nicht erforderlich; falls vorhanden, dient sie der erweiterten Auswahl | `<` / Shift `>` / Option &#124; |
| Option-Ebene der Taste unter Esc | &#124; | `×` |
| Option+2 / Option+3 | `<` / `>` | `²` / `³` |
| Nach erweiterter Auswahl `+` drücken | `×` | `±` |

Beide verwenden Option+F, loslassen, dann die Ziel-Taste, um erweiterte Zeichen
auszuwählen. Die physischen Tastenpositionen und Beispiele unten beschreiben
vor allem **E2 ANSI**.

### Grundregeln

- Buchstaben sind **QWERTZ**: An der Position der US-Taste Y wird `z` eingegeben,
  an der Position der US-Taste Z `y`.
- **Beide Option-Tasten sind AltGr**; AltGr wird nicht mit Control+Option emuliert.
- **Erweiterte Auswahl: Option+F drücken, beide Tasten loslassen, dann die
  Ziel-Taste drücken.**
- Für Großbuchstaben oder Zweitbelegungen der roten Ebene fügen Sie Shift beim
  Schritt der Ziel-Taste hinzu; halten Sie Option nicht durchgehend gedrückt.
- Akzent-Tottasten: Zuerst den Akzent eingeben, dann den Buchstaben. Escape oder
  Rücktaste bricht eine unvollständige Eingabe ab.

### ANSI-Tastenpositionen

„US-Taste“ dient nur zur Lokalisierung der physischen Taste; Ihre Tastenkappen
müssen diese Zeichen nicht tragen.

| Physische US-Tastenposition | E2 normal | Shift | Option |
| --- | --- | --- | --- |
| Backtick-Taste unter Esc | `^` Tottaste | `°` | &#124; |
| `-`-Taste | `ß` | `?` | `\` |
| `=`-Taste | Akut-Tottaste | Grave-Tottaste | Punkt-oben-Tottaste |
| `[`-Taste | `ü` | `Ü` | Horn / griechische Buchstaben |
| `]`-Taste | `+` | `*` | `~` |
| `;`-Taste | `ö` | `Ö` | Punkt-unten-Tottaste |
| Taste für einfaches Anführungszeichen | `ä` | `Ä` | Makron-Auswahl |
| Backslash-Taste | `#` | `'` | `−` |
| `/`-Taste | `-` | `_` | weiches Trennzeichen |

### Häufige Zeichen

Die folgenden Ziffern- und Buchstabenpositionen sind auf US- und E2-Tastaturen
gleich (Q/W/E/R/T/F/I usw.):

| Eingabe | Ausgabe |
| --- | --- |
| Option+Q / E | `@` / `€` |
| Option+2 / 3 | `<` / `>` |
| Option+7 / 8 / 9 / 0 | `{` / `[` / `]` / `}` |
| Option+W, loslassen, dann A | `ā` |
| Option+T, loslassen, dann A | `ǎ` |
| Option+I, loslassen, dann A | `ã` |
| Option+F, loslassen, dann T | `þ` |
| Option+F, loslassen, dann Shift+T | `Þ` |
| Option+F, loslassen, dann 2 | `½` |
| Option+F, loslassen, dann Shift+C | `©` |
| Option+F, loslassen, dann US-`;` | `œ` |
| Option+R, loslassen, E drücken, dann 5 | `ɛ` |
| Option+US-`[`, loslassen, dann A | `α` |
| Option+T, loslassen, dann 1 | `₁` |
| `^`-Tottaste unter Esc, loslassen, dann 2 | `²` |

Beispiel für mehrere Akzente: Option+US-`[` (Horn), loslassen; Option+US-`;`
(Punkt unten), loslassen; U drücken, ergibt `ự`. Die Reihenfolge der beiden
Akzente ist austauschbar.

## macOS-Anpassungen und Grenzen

- **Command behält die deutsche Position**: An der Position der US-Taste Y liegt
  ⌘Z, üblicherweise Rückgängig; es wird nicht auf US-QWERTY zurückgeschaltet.
- Command-/Control-Tastenkürzel umgehen Tottasten und brechen eine unvollständige
  Eingabe ab. Control+A…Z werden gemäß den deutschen Buchstaben auf Steuerzeichen
  abgebildet.
- Caps Lock folgt dem macOS-Verhalten für Großbuchstaben; die Ziffernreihe wird
  nicht auf Symbole gesperrt. Shift+Caps erzeugt Kleinbuchstaben. Caps ändert die
  Option-Ebene nicht.
- Option+A gibt `☺` aus, gemäß der unter Windows zulässigen Implementierung; die
  Emoji-Auswahl wird nicht geöffnet.
- Shift+Option entspricht nicht der roten erweiterten Ebene; nur Ausgaben, die in
  der Windows-Referenztabelle ausdrücklich angegeben sind, bleiben erhalten,
  z. B. Shift+Option+ß ergibt `ẞ`.
- Nicht passende Akzentkombinationen behalten ein sichtbares Akzentpräfix;
  interne Zwischenzustandscodes von Windows werden nie als fremde Zeichen ausgegeben.
- Escape und Rücktaste brechen eine unvollständige Tottaste ab; im unvollständigen
  Zustand löscht die Rücktaste nur den Zustand und keinen vorhergehenden Text.
- Das Dezimaltrennzeichen des Ziffernblocks ist das deutsche Komma. Trifft E2 auf
  die optionale zusätzliche ISO-Taste, kann diese der erweiterten Auswahl dienen;
  auf E1 gibt diese Taste `< > |` aus.
- Die native API-Prüfung ersetzt keine manuellen Tests in jeder Anwendung.
  Anwendungsspezifische Tastenkürzel und das Option-Verhalten im Terminal können
  das Systemlayout weiterhin überlagern.
- Referenzimplementierungen und Benutzer-Layoutdiagramme sind nicht der
  vollständige DIN-Standard; eine Standardzertifizierung wird nicht beansprucht.

## Repository-Struktur

```text
.
├── README.md                 # Chinesisch (Standard)
├── README.en.md              # Englisch
├── README.de.md              # Deutsch
├── LICENSE                   # MIT (Projektcode und generierte Layoutdateien)
├── THIRD-PARTY-NOTICES.md    # Quellen und Lizenzgrenzen (Chinesisch)
├── THIRD-PARTY-NOTICES.en.md # Englisch
├── THIRD-PARTY-NOTICES.de.md # Deutsch
├── CHANGELOG.md              # Versionsverlauf (Chinesisch)
├── CHANGELOG.en.md           # Englisch
├── CHANGELOG.de.md           # Deutsch
├── SPEC.md                   # Ziele, Einschränkungen, Abnahmekriterien
├── TESTING.md                # Test- und native Prüfaufzeichnung
├── INPUT-SOURCE-REPAIR.md    # Eingabequellen-Migration (Rechner des Autors)
├── RIME-E2.md                # Chinesische Satzzeichenanpassung für Squirrel / Rime
├── dist/                     # Generierte Ergebnisse und native Testvektoren
│   ├── GermanE1.bundle
│   ├── GermanE2.bundle
│   ├── *.keylayout           # Zwischendateien; nicht separat installieren
│   └── native-cases*.json    # Native Prüffälle
├── references/               # Fixierte Referenz-Snapshots von Drittanbietern
├── tools/                    # Werkzeuge für Generierung, Prüfung und Eingabepläne
└── tests/                    # Offline-Unit-Tests
```

## Bauen und prüfen

```sh
python3 tools/build_layout.py
python3 -m unittest discover -s tests -v
swift tools/verify_macos.swift dist/native-cases.json
swift tools/verify_macos.swift dist/native-cases-E1.json
```

- Offline-Tests: 31 Tests für das generierte XML, die Ebenen normal/Shift/Option/
  Command/Control/Caps, Abbruch und Rückfall, alle E1/E2-Referenzübergänge der
  Tottasten sowie die Prüfsummen der Referenz-Snapshots.
- Native Prüfung: 5.024 Prüfungen für E2 und 5.026 für E1, jeweils mit
  Hauptsprache `de`; das Layout muss bereits installiert und vom System erkannt sein.
- Der Generator installiert, registriert oder wählt keine Eingabequelle aus;
  `--register` registriert nur, ohne sie zu aktivieren oder auszuwählen.
- Nach dem Neugenerieren der Dateien aktualisieren Sie die Kopie in
  `~/Library/Keyboard Layouts`, registrieren Sie erneut oder melden Sie sich ab
  und wieder an; sonst verwendet macOS möglicherweise weiterhin die alte Version.

Die vollständige Aufzeichnung finden Sie in [`TESTING.md`](TESTING.md) (derzeit
auf Chinesisch). `.backups/` ist das lokale Sicherungsverzeichnis des Autors,
über `.gitignore` ausgeschlossen und **wird nicht veröffentlicht**; Pfade in der
Dokumentation dienen nur der Reproduktion.

## Deinstallieren

Zuerst zu einem Systemlayout wie ABC wechseln, die Eingabequelle in den
Systemeinstellungen entfernen und dann das entsprechende
`~/Library/Keyboard Layouts/GermanE2.bundle` oder `GermanE1.bundle` löschen.
Melden Sie sich bei Bedarf ab und wieder an. Das Löschen des Projektverzeichnisses
deinstalliert die Kopie in `Library` nicht.

## Dokumentation

- [SPEC.md](SPEC.md): Spezifikation, macOS-Anpassungsregeln und Abnahmekriterien
  (Chinesisch).
- [TESTING.md](TESTING.md): Offline-Tests, native Prüfung und bekannte Grenzen
  (Chinesisch).
- [INPUT-SOURCE-REPAIR.md](INPUT-SOURCE-REPAIR.md): Diagnose und gezielte
  Reparatur der alten Eingabequelle „Deutsch – Standard“ (Chinesisch).
- [RIME-E2.md](RIME-E2.md): Chinesische Satzzeichenanpassung für Squirrel / Rime
  unter E2 (Chinesisch).
- [references/README.md](references/README.md): Quellen, Versionen und Prüfsummen
  (Chinesisch).
- [THIRD-PARTY-NOTICES.md](THIRD-PARTY-NOTICES.md): Material und Lizenzierung von
  Drittanbietern (Chinesisch; auch [Englisch](THIRD-PARTY-NOTICES.en.md) und
  [Deutsch](THIRD-PARTY-NOTICES.de.md)).
- [CHANGELOG.md](CHANGELOG.md): Versionsverlauf (Chinesisch; auch
  [Englisch](CHANGELOG.en.md) und [Deutsch](CHANGELOG.de.md)).

## Lizenz

Quellcode, Build-Skripte, Tests und generierte Layoutdateien des Projekts stehen
unter der [MIT-Lizenz](LICENSE). Material von Drittanbietern unter `references/`
ist nicht von MIT abgedeckt; siehe [THIRD-PARTY-NOTICES.de.md](THIRD-PARTY-NOTICES.de.md).

Apple, macOS, Windows, Microsoft, Rime und weitere Namen und Marken gehören ihren
jeweiligen Inhabern. Dieses Projekt ist mit ihnen weder verbunden noch von ihnen
unterstützt.
