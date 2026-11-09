# Material und Lizenzierung von Drittanbietern

[中文](THIRD-PARTY-NOTICES.md) | [English](THIRD-PARTY-NOTICES.en.md) | **Deutsch**

Der **Quellcode, die Build-Skripte, die Tests und die generierten
macOS-Layoutdateien** dieses Repositorys stehen unter der MIT-Lizenz in
[`LICENSE`](LICENSE).

`references/` enthält das Referenzmaterial, das zur Implementierung der Layouts
dient, und ist **nicht von MIT abgedeckt**. Ein Teil davon ist Material von
Drittanbietern, dessen Urheberrecht den jeweiligen Inhabern gehört; es wird nur
als technische Referenz und als Snapshot aufbewahrt. Die generierten
Layoutdateien sind eine unabhängige Neuimplementierung auf Grundlage öffentlich
beobachtbaren Tastenverhaltens und enthalten keinen Quellcode, keine
Treiberbinärdateien und keine Laufzeitkomponenten Dritter.

## Linux: xkeyboard-config 2.48

- Upstream-Projekt: <https://gitlab.freedesktop.org/xkeyboard-config/xkeyboard-config>
- Release-Archiv: <https://www.x.org/releases/individual/data/xkeyboard-config/xkeyboard-config-2.48.tar.xz>
- Lokaler Ort: `references/linux/xkeyboard-config-2.48/`
- Lizenz: permissive X11-/MIT-artige Lizenz; der vollständige Text steht in
  `references/linux/xkeyboard-config-2.48/COPYING`.

Verwendete Dateien: `symbols/de`, `symbols/level3`, `symbols/level5`,
`types/level5`, `COPYING`.

## Windows: German Extended E1 / E2

- Treiber: `KBDGRE1.DLL` (E1), `KBDGRE2.DLL` (E2)
- KLID: `00020407` für E1, `00030407` für E2
- Seiten: <https://kbdlayout.info/KBDGRE1/>, <https://kbdlayout.info/KBDGRE2/>
- Lokaler Ort: `references/windows/`

Bei diesen Dateien handelt es sich um **beschreibende Snapshots, die
kbdlayout.info aus den öffentlich dokumentierten Treibertabellen von Microsoft
erzeugt hat**, nicht um aus Windows oder Treiberbinärdateien extrahierten Code.
Es wurde keine DLL heruntergeladen oder ausgeführt. Sie dienen der Prüfung von
Tastenpositionen, Tottasten-Zustandsmaschinen und der erweiterten Auswahl sowie
der Reproduzierbarkeit der Generierung.

Bitte beachten Sie:

- Die Dateien behalten ihren ursprünglichen generierten Inhalt und die darin
  enthaltenen Urheberrechtshinweise. Beispielsweise enthält `kbdgre2.klc`
  `© Microsoft Corporation. All rights reserved.`
- Dieses Projekt **erteilt für diese Dateien keine Lizenz** und erhebt kein
  Urheberrecht an ihnen.
- Wenn Sie Rechteinhaber sind und der Ansicht sind, dass diese Snapshots nicht
  weiterverbreitet werden sollten, öffnen Sie bitte ein Issue. Ich werde die
  betreffenden Dateien entfernen und stattdessen beim Build herunterladen und prüfen.
- Diese Materialien beschreiben ausschließlich Tastaturlayout-Verhalten; sie
  enthalten keinen Microsoft-Treibercode, keine Signaturen und keine
  Laufzeitkomponenten.

Download-Adressen und Prüfsummen der Snapshots stehen in
[`references/README.md`](references/README.md) (derzeit auf Chinesisch) und
[`references/SHA256SUMS`](references/SHA256SUMS).

## Marken und Verbindung zu Unternehmen

Apple, macOS, Windows, Microsoft, Rime, Squirrel und weitere Namen und Marken
gehören ihren jeweiligen Inhabern. Dieses Projekt ist weder mit Apple, Microsoft,
X.Org noch mit dem Rime-Projekt verbunden, gesponsert oder von ihnen unterstützt.

## Haftungsausschluss

Dieses Projekt wird „wie besehen“ ohne ausdrückliche oder stillschweigende
Gewährleistung bereitgestellt. Tastaturlayouts, die Registrierung von
Eingabequellen und Änderungen an Einstellungen können je nach macOS-Version,
Hardware und Anwendungstastenkürzeln unterschiedlich wirken. Prüfen Sie die
Risiken und sichern Sie Ihre Daten vor der Verwendung.
