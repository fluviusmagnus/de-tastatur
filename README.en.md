# German E1 / E2 for macOS

[中文](README.md) | **English** | [Deutsch](README.de.md)

Two native macOS keyboard layouts: **German E2 (ANSI)** and the alternative
**German E1 (ISO)**, both filed under **German** input sources. Key positions
follow `de(e1)` / `de(e2)` from Linux `xkeyboard-config` 2.48; characters, dead
keys and the extended-selection state machine are ported from the public layout
tables of Windows `KBDGRE1.DLL` / `KBDGRE2.DLL`.

No Karabiner, background service, accessibility permission or third-party
runtime is required.

## Features

- **Native layout bundles**: standard `.bundle` input sources declaring
  `TISIntendedLanguage=de`, so macOS lists them under German.
- **QWERTZ**: the US-keycap Y position types `z`, the US-keycap Z position types `y`.
- **Both Option keys act as AltGr**; no Control+Option emulation.
- **Complete dead-key tables**: accents, multiple accents, IPA, Greek letters,
  mathematical symbols, fractions, superscripts and subscripts.
- **Extended selection**: press Option+F, release both keys, then press the
  target key. Add Shift at the target-key step for uppercase or secondary characters.
- **E2 ANSI** is the primary layout; **E1 ISO** is for ISO keyboards with the extra key.
- Reproducible generation, offline tests, and a native macOS `UCKeyTranslate` verifier.

## Support scope

Verified environment:

| Item | Value |
| --- | --- |
| macOS | 27.2 (build 26B123) |
| Hardware | Apple Silicon, `LMGetKbdType()` returns 91 |
| Keyboard | Physical ANSI keyboard |
| Bundle version | 1.2.0 (see `Contents/Info.plist`) |

Not yet manually verified: Intel Macs, older macOS versions, physical ISO/JIS
keyboards, external numeric keypads, the login window / FileVault / password
dialogs, and application-specific shortcuts. E1 ISO verification uses the system
API with simulated keyboard types, not a physical ISO keyboard. See
[`TESTING.md`](TESTING.md) (currently in Chinese).

## Installation

### Option 1: use the prebuilt bundles

```sh
mkdir -p "$HOME/Library/Keyboard Layouts"
cp -R dist/GermanE2.bundle "$HOME/Library/Keyboard Layouts/"
cp -R dist/GermanE1.bundle "$HOME/Library/Keyboard Layouts/"   # only if you need the ISO fallback
```

`dist/*.keylayout` are build intermediates. **Install the whole `.bundle`, not
those files individually.** If a file with the same name already exists, check
and back it up first so you do not overwrite another custom layout.

### Option 2: build from source

Requires Python 3.9+; native verification additionally requires the macOS Swift
Command Line Tools.

```sh
python3 tools/build_layout.py
python3 -m unittest discover -s tests -v
```

The build only writes files under `dist/`; it does not install, register or
select an input source. Copy the result as described in Option 1.

To make macOS notice a newly installed layout immediately, register it
explicitly (this does not enable or select it):

```sh
swift tools/verify_macos.swift dist/native-cases.json \
  --register "$HOME/Library/Keyboard Layouts/GermanE2.bundle"
swift tools/verify_macos.swift dist/native-cases-E1.json \
  --register "$HOME/Library/Keyboard Layouts/GermanE1.bundle"
```

## Enabling

1. Open **System Settings → Keyboard → Text Input → Edit**.
2. Click **＋ → German** and find **German E2 (ANSI)** or **German E1 (ISO)**.
3. After adding it, switch to the layout from the input menu in the menu bar.
4. If it does not appear in the list yet, log out and back in, then look again;
   restart if necessary.

Do not delete the built-in layout files. A custom layout for the current user is
not guaranteed to work at FileVault unlock, in the login window, or in every
password dialog.

## Usage

### Choosing E2 or E1

Use **E2** on ANSI hardware. **E1** is intended for ISO keyboards: the left
Shift key is shorter and there is an extra character key next to it.

| Position / function | E2 ANSI | E1 ISO |
| --- | --- | --- |
| Extra key next to left Shift | Not needed; if present, it acts as extended selection | `<` / Shift `>` / Option &#124; |
| Option layer of the key below Esc | &#124; | `×` |
| Option+2 / Option+3 | `<` / `>` | `²` / `³` |
| Press `+` after extended selection | `×` | `±` |

Both use Option+F, release, then the target key to select extended characters.
The physical key positions and examples below describe **E2 ANSI** primarily.

### Basic rules

- Letters are **QWERTZ**: the US-keycap Y position types `z`, the US-keycap Z
  position types `y`.
- **Both Option keys are AltGr**; AltGr is not emulated with Control+Option.
- **Extended selection: press Option+F, release both keys, then press the target key.**
- For uppercase or secondary characters in the red layer, add Shift at the
  target-key step; do not hold Option throughout.
- Accent dead keys: type the accent first, then the letter. Escape or Backspace
  cancels an unfinished composition.

### ANSI key positions

"US keycap" is used only to locate a physical key; your keycaps do not need to
show these characters.

| Physical US key position | E2 normal output | Shift output | Option output |
| --- | --- | --- | --- |
| Backtick key below Esc | `^` dead key | `°` | &#124; |
| `-` key | `ß` | `?` | `\` |
| `=` key | acute dead key | grave dead key | dot-above dead key |
| `[` key | `ü` | `Ü` | horn / Greek letter selection |
| `]` key | `+` | `*` | `~` |
| `;` key | `ö` | `Ö` | dot-below dead key |
| Single-quote key | `ä` | `Ä` | macron selection |
| Backslash key | `#` | `'` | `−` |
| `/` key | `-` | `_` | soft hyphen |

### Common characters

The following number and letter positions are the same on US and E2 keyboards
(Q/W/E/R/T/F/I, etc.):

| Input | Output |
| --- | --- |
| Option+Q / E | `@` / `€` |
| Option+2 / 3 | `<` / `>` |
| Option+7 / 8 / 9 / 0 | `{` / `[` / `]` / `}` |
| Option+W, release, then A | `ā` |
| Option+T, release, then A | `ǎ` |
| Option+I, release, then A | `ã` |
| Option+F, release, then T | `þ` |
| Option+F, release, then Shift+T | `Þ` |
| Option+F, release, then 2 | `½` |
| Option+F, release, then Shift+C | `©` |
| Option+F, release, then US `;` | `œ` |
| Option+R, release, press E, then 5 | `ɛ` |
| Option+US `[`, release, then A | `α` |
| Option+T, release, then 1 | `₁` |
| `^` dead key below Esc, release, then 2 | `²` |

Multiple accents example: Option+US `[` (horn), release; Option+US `;`
(dot below), release; press U to get `ự`. The two accents may be entered in
either order.

## macOS adaptations and limits

- **Command keeps the German position**: the US Y key position is ⌘Z, normally
  Undo; it does not switch back to US QWERTY.
- Command / Control shortcuts bypass dead keys and cancel an unfinished
  composition. Control+A…Z map to control characters according to the German letters.
- Caps Lock follows the macOS letter-capitalisation behaviour; it does not lock
  the number row to symbols. Shift+Caps produces lowercase. Caps does not change
  the Option layer.
- Option+A types `☺`, following the Windows-permitted implementation; it does not
  open the emoji picker.
- Shift+Option is not the red extended layer; only outputs explicitly specified
  by the Windows reference table are kept, e.g. Shift+Option+ß is `ẞ`.
- Unmatched accent combinations keep a visible accent prefix; internal Windows
  intermediate state codes are never shown as unrelated characters.
- Escape and Backspace cancel an unfinished dead key; when unfinished, Backspace
  only cancels the state and does not delete preceding text.
- The numeric keypad decimal separator is the German comma. If E2 encounters the
  optional ISO extra key, it can act as extended selection; on E1 that key types `< > |`.
- Native API verification is not the same as manual testing in every app.
  Application shortcuts and terminal Option behaviour can still override the
  system layout.
- Reference implementations and user layout diagrams are not the full DIN
  standard; no standard certification is claimed.

## Repository layout

```text
.
├── README.md                 # Chinese (default)
├── README.en.md              # English
├── README.de.md              # German
├── LICENSE                   # MIT (project code and generated layout files)
├── THIRD-PARTY-NOTICES.md    # sources, copyright and license boundaries (Chinese)
├── THIRD-PARTY-NOTICES.en.md # English
├── THIRD-PARTY-NOTICES.de.md # German
├── CHANGELOG.md              # version history (Chinese)
├── CHANGELOG.en.md           # English
├── CHANGELOG.de.md           # German
├── SPEC.md                   # goals, constraints, acceptance criteria
├── TESTING.md                # test and native verification record
├── INPUT-SOURCE-REPAIR.md    # input-source migration notes (author's machine)
├── RIME-E2.md                # Squirrel / Rime Chinese punctuation adaptation
├── dist/                     # generated outputs and native test vectors
│   ├── GermanE1.bundle
│   ├── GermanE2.bundle
│   ├── *.keylayout           # build intermediates; do not install separately
│   └── native-cases*.json    # native verification cases
├── references/               # pinned third-party reference snapshots
├── tools/                    # generation, verification and input-source plan tools
└── tests/                    # offline unit tests
```

## Build and verification

```sh
python3 tools/build_layout.py
python3 -m unittest discover -s tests -v
swift tools/verify_macos.swift dist/native-cases.json
swift tools/verify_macos.swift dist/native-cases-E1.json
```

- Offline tests: 31 tests covering the generated XML, normal/Shift/Option/
  Command/Control/Caps layers, cancellation and fallback, all E1/E2 reference
  dead-key transitions, and reference snapshot checksums.
- Native verification: 5,024 checks for E2 and 5,026 for E1, both with primary
  language `de`; the layout must already be installed and discovered by the system.
- The generator does not install, register or select an input source;
  `--register` only registers, without enabling or selecting it.
- After regenerating files, update the copy in `~/Library/Keyboard Layouts`,
  register again or log out and back in; otherwise macOS may keep using the old version.

See [`TESTING.md`](TESTING.md) for the full record (currently in Chinese).
`.backups/` is the author's local backup directory, excluded via `.gitignore`
and **not published**; paths in the documentation are for reproduction only.

## Uninstall

Switch back to a system layout such as ABC first, remove the input source in
System Settings, then delete the corresponding
`~/Library/Keyboard Layouts/GermanE2.bundle` or `GermanE1.bundle`. Log out and
back in if necessary. Deleting the project directory does not uninstall the copy
in `Library`.

## Documentation

- [SPEC.md](SPEC.md): specification, macOS adaptation rules and acceptance criteria (Chinese).
- [TESTING.md](TESTING.md): offline tests, native verification and known limits (Chinese).
- [INPUT-SOURCE-REPAIR.md](INPUT-SOURCE-REPAIR.md): diagnosis and targeted repair of the old "German – Standard" input source (Chinese).
- [RIME-E2.md](RIME-E2.md): E2 Chinese punctuation adaptation for Squirrel / Rime (Chinese).
- [references/README.md](references/README.md): sources, versions and checksums (Chinese).
- [THIRD-PARTY-NOTICES.md](THIRD-PARTY-NOTICES.md): third-party material and licensing (Chinese;
  also available in [English](THIRD-PARTY-NOTICES.en.md) and [German](THIRD-PARTY-NOTICES.de.md)).
- [CHANGELOG.md](CHANGELOG.md): version history (Chinese;
  also available in [English](CHANGELOG.en.md) and [German](CHANGELOG.de.md)).

## License

The project source code, build scripts, tests and generated layout files are
released under the [MIT License](LICENSE). Third-party reference material under
`references/` is not covered by MIT; see
[THIRD-PARTY-NOTICES.en.md](THIRD-PARTY-NOTICES.en.md).

Apple, macOS, Windows, Microsoft, Rime and other names and trademarks belong to
their respective owners. This project is not affiliated with or endorsed by them.
