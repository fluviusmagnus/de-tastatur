# Changelog

[中文](CHANGELOG.md) | **English** | [Deutsch](CHANGELOG.de.md)

This project follows the version-number format of
[Semantic Versioning](https://semver.org/). `CFBundleShortVersionString` in
`Contents/Info.plist` is the public version number.

## [1.2.0] - 2026-11-09

First public release, retaining the existing bundle version 1.2.0.

### Added

- German E2 (ANSI) and German E1 (ISO) native macOS `.bundle` input sources.
- QWERTZ key positions, both Option keys as AltGr, and Option+F extended selection.
- Complete dead-key state machine: accents, multiple accents, IPA, Greek letters,
  mathematical symbols, fractions, superscripts and subscripts.
- Offline generator and 31 unit tests.
- Native macOS `UCKeyTranslate` verifier and verification vectors.
- Chinese punctuation adaptation notes for Squirrel / Rime.
- Input-source migration and targeted-repair tools and records.

### Verification

- 31 offline tests passed.
- E2: 5,024 native checks passed, primary language `de`.
- E1: 5,026 native checks passed, primary language `de`.

### Known limitations

- No key-by-key manual testing of physical keyboards, application shortcuts, or
  the login window / FileVault / password dialogs.
- The E1 ISO path is simulated through the system API, not tested with a physical
  ISO keyboard.
- Not verified on Intel Macs or older macOS versions.
