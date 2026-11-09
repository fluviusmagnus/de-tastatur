#!/usr/bin/env python3
"""Build a macOS ANSI E2 layout from the pinned Windows keyboard tables.

No third-party Python dependencies. This does not install or select an input source.
"""

from collections import deque
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import plistlib
import re
import xml.etree.ElementTree as ET
from xml.sax.saxutils import quoteattr


ROOT = Path(__file__).resolve().parents[1]
NAME = "German E2 (ANSI)"
SOURCE_ID = "local.keyboardlayout.GermanE2.keylayout.GermanE2ANSI"
VARIANTS = {
    "E2": {"name": NAME, "internal": "GermanE2ANSI", "source": SOURCE_ID,
           "id": "-21374", "types": [40]},
    "E1": {"name": "German E1 (ISO)", "internal": "GermanE1ISO",
           "source": "local.keyboardlayout.GermanE1.keylayout.GermanE1ISO", "id": "-21371", "types": [38, 41]},
}
MODIFIERS = [0, 2, 4, 6, 8, 10, 1, 3, 16, 18]

# Physical PC scancodes -> macOS virtual keycodes, not keycap letters.
SC_TO_MAC = {0x29: 50, 0x2B: 42, 0x56: 10, 0x39: 49}
for start, codes in [
    (0x02, [18, 19, 20, 21, 23, 22, 26, 28, 25, 29, 27, 24]),
    (0x10, [12, 13, 14, 15, 17, 16, 32, 34, 31, 35, 33, 30]),
    (0x1E, [0, 1, 2, 3, 5, 4, 38, 40, 37, 41, 39]),
    (0x2C, [6, 7, 8, 9, 11, 45, 46, 43, 47, 44]),
]:
    SC_TO_MAC.update({start + i: code for i, code in enumerate(codes)})

NOOP = ("noop", "")


def state_name(char):
    return "d%04X" % ord(char)


@dataclass
class Reference:
    maps: dict
    transitions: dict
    variant: str = "E2"

    def input_events(self):
        """One physical event for each Windows input character (prefer no modifier)."""
        events = {}
        for index in [0, 1, 4, 5]:
            for code, (kind, char) in sorted(self.maps[index].items()):
                if kind in {"text", "dead"} and char:
                    events.setdefault(char, (code, index))
        return events

    def state_paths(self):
        """Shortest zero-output key sequences reaching every reference dead state."""
        events = self.input_events()
        paths = {}
        for index in [0, 1, 4, 5]:
            for code, (kind, char) in sorted(self.maps[index].items()):
                if kind == "dead":
                    paths.setdefault(char, [(code, index)])
        queue = deque(paths)
        while queue:
            state = queue.popleft()
            for (accent, char), (result, dead) in self.transitions.items():
                if accent == state and dead and char in events and result not in paths:
                    paths[result] = paths[state] + [events[char]]
                    queue.append(result)
        return paths

    def transition_cases(self):
        paths, events = self.state_paths(), self.input_events()
        cases, missing = [], []
        for (accent, char), (result, dead) in sorted(self.transitions.items()):
            label = "%04X+%04X" % (ord(accent), ord(char))
            if accent not in paths or char not in events:
                missing.append(label)
                continue
            cases.append((label, paths[accent] + [events[char]], "" if dead else result, dead))
        return cases, missing

    def terminators(self):
        paths = self.state_paths()
        extra = "\u02df"
        result = {}
        for state, path in paths.items():
            # Prefer the reference's spacing representation, except Extra Selector:
            # its space mapping is a hair space, not a visible accent to flush.
            spacing = self.transitions.get((state, " "))
            if state == extra:
                result[state] = ""
            elif spacing and not spacing[1]:
                result[state] = spacing[0]
            else:
                result[state] = "".join(
                    char for code, index in path
                    for _, char in [self.maps[index][code]] if char != extra
                )
        return result


def load_reference(variant="E2"):
    manifest = ROOT / "references/SHA256SUMS"
    hashes = dict(line.split("  ", 1)[::-1] for line in manifest.read_text().splitlines())
    stem = "kbdgre" + variant[-1]
    names = ["windows/" + stem + "-tables.xml", "windows/" + stem + ".xml"]
    for name in names:
        actual = hashlib.sha256((ROOT / "references" / name).read_bytes()).hexdigest()
        if actual != hashes[name]:
            raise ValueError("Reference checksum mismatch: " + name)
    tables = ET.parse(ROOT / "references" / names[0]).getroot()
    physical = ET.parse(ROOT / "references" / names[1]).getroot()
    vk_tables = {}
    for table in tables.findall(".//VK_TO_WCHAR_TABLE"):
        rows = table.findall("VkToWchars/VK_TO_WCHARS")
        for i, row in enumerate(rows):
            vk = row.get("VirtualKey")
            if vk is None:
                continue
            columns = row.get("Wch").split()
            outputs = []
            for j, hexchar in enumerate(columns):
                value = int(hexchar, 16)
                if value == 0xF000:  # WCH_NONE
                    outputs.append(NOOP)
                elif value == 0xF001:  # WCH_DEAD: the next row supplies accents.
                    accent_row = rows[i + 1]
                    if accent_row.get("VirtualKey") is not None:
                        raise ValueError("Missing dead-key accent row")
                    outputs.append(("dead", chr(int(accent_row.get("Wch").split()[j], 16))))
                elif value == 0xF002:
                    raise ValueError("Unexpected Windows ligature; extend the generator")
                else:
                    outputs.append(("text", chr(value)))
            vk_tables[vk] = outputs

    maps = {index: {} for index in range(10)}
    sc_to_mac = dict(SC_TO_MAC)
    if variant == "E1":
        # Apple ISO keyboards: section (10) is left of 1; grave (50) is
        # the extra key beside left Shift. ANSI places grave (50) left of 1.
        sc_to_mac.update({0x29: 10, 0x56: 50})
    for key in physical.findall("PhysicalKeys/PK"):
        if key.get("SC") is None:
            continue
        scan = int(key.get("SC"), 16)
        if scan not in sc_to_mac:
            continue
        code = sc_to_mac[scan]
        columns = vk_tables[key.get("VK")]
        for index, column in [(0, 0), (1, 1), (4, 4), (5, 5)]:
            maps[index][code] = columns[column] if column < len(columns) else NOOP

    # Native Mac control, navigation, function and keypad keys.
    controls = {
        36: "\r", 48: "\t", 51: "\x08", 53: "\x1b", 117: "\x7f",
        123: "\x1c", 124: "\x1d", 125: "\x1f", 126: "\x1e",
        115: "\x01", 119: "\x04", 116: "\x0b", 121: "\x0c",
        71: "\x1b", 76: "\x03",
    }
    keypad = {
        65: ",", 67: "*", 69: "+", 75: "/", 78: "-", 81: "=",
        82: "0", 83: "1", 84: "2", 85: "3", 86: "4", 87: "5",
        88: "6", 89: "7", 91: "8", 92: "9",
    }
    function_keys = [64, 79, 80, 90, 96, 97, 98, 99, 100, 101, 103,
                     105, 106, 107, 109, 111, 113, 118, 120, 122]
    controls.update({code: "\x10" for code in function_keys})
    for index in [0, 1, 4, 5]:
        maps[index].update({code: ("text", char) for code, char in keypad.items()})
        maps[index].update({code: ("shortcut", char) for code, char in controls.items()})
        maps[index][51] = ("backspace", "\x08")

    # Normal macOS Caps Lock, instead of Windows' all-key Shift Lock semantics.
    for code, token in maps[0].items():
        kind, char = token
        upper = "ẞ" if char == "ß" else char.upper()
        alphabetic = kind == "text" and len(char) == 1 and char.isalpha()
        maps[2][code] = (kind, upper) if alphabetic else token
        maps[3][code] = token if alphabetic else maps[1][code]
        for index, source in [(6, 0), (7, 1)]:
            source_kind, source_char = maps[source][code]
            maps[index][code] = ("shortcut", source_char if source_kind != "noop" else "")
        for index, source in [(8, 0), (9, 1)]:
            source_kind, source_char = maps[source][code]
            if kind == "text" and "a" <= char <= "z":
                source_char = chr(ord(char) - ord("a") + 1)
            elif source_kind == "dead":
                source_char = {"^": "\x1e"}.get(source_char, source_char)
            maps[index][code] = ("shortcut", source_char if source_kind != "noop" else "")

    transitions = {}
    for row in tables.findall(".//DeadKeys/DEADKEY"):
        both = int(row.get("Both"), 16)
        key = (chr(both >> 16), chr(both & 0xFFFF))
        if key in transitions:
            raise ValueError("Duplicate reference transition: " + repr(key))
        transitions[key] = (chr(int(row.get("Composed"), 16)), row.get("Flags") == "DEAD")
    return Reference(maps, transitions, variant)


def make_layout(reference):
    config = VARIANTS[reference.variant]
    root = ET.Element("keyboard", group="126", id=config["id"], name=config["internal"], maxout="8")
    ET.SubElement(root, "layouts")
    ET.SubElement(root.find("layouts"), "layout", first="0", last="255",
                  mapSet="E2", modifiers="modifiers")
    modifiers = ET.SubElement(root, "modifierMap", id="modifiers", defaultIndex="0")
    selectors = [
        "", "anyShift", "caps", "anyShift caps", "anyOption caps?",
        "anyShift anyOption caps?",
        "command anyOption? anyControl? caps?",
        "command anyShift anyOption? anyControl? caps?",
        "anyControl anyOption? caps?", "anyShift anyControl anyOption? caps?",
    ]
    for index, selector in enumerate(selectors):
        select = ET.SubElement(modifiers, "keyMapSelect", mapIndex=str(index))
        ET.SubElement(select, "modifier", keys=selector)
    keymaps = ET.SubElement(root, "keyMapSet", id="E2")
    actions = ET.SubElement(root, "actions")
    terminators = reference.terminators()
    states = sorted(terminators)
    tokens = sorted(
        {token for keymap in reference.maps.values() for token in keymap.values()}
        | {("text", char) for _, char in reference.transitions}
    )
    action_ids = {token: "a%d" % i for i, token in enumerate(tokens)}
    for index, keymap in sorted(reference.maps.items()):
        element = ET.SubElement(keymaps, "keyMap", index=str(index))
        for code, token in sorted(keymap.items()):
            ET.SubElement(element, "key", code=str(code), action=action_ids[token])

    for (kind, char), action_id in action_ids.items():
        action = ET.SubElement(actions, "action", id=action_id)
        for state in [None] + states:
            rule = {"state": "none" if state is None else state_name(state)}
            if kind == "shortcut":
                rule["output"] = char  # Bypass composition and cancel pending state.
            elif kind == "backspace":
                rule["output"] = char if state is None else ""
            elif kind == "noop":
                if state is None:
                    rule["output"] = ""
                else:
                    rule["next"] = state_name(state)
            else:
                transition = reference.transitions.get((state, char))
                if state is not None and transition:
                    result, dead = transition
                    rule["next" if dead else "output"] = state_name(result) if dead else result
                elif kind == "dead":
                    rule["next"] = state_name(char)
                    if state is not None and terminators[state]:
                        rule["output"] = terminators[state]
                else:
                    rule["output"] = (terminators[state] if state is not None else "") + char
            ET.SubElement(action, "when", rule)

    endings = ET.SubElement(root, "terminators")
    for state, text in sorted(terminators.items()):
        ET.SubElement(endings, "when", state=state_name(state), output=text)
    return root


def render_layout(root):
    # Apple's keylayout format uses numeric references for ASCII control outputs.
    # Ordinary XML 1.0 parsers reject these, but macOS keylayout parsers support them.
    def attribute(value):
        quoted = quoteattr(value, {"\t": "&#x0009;", "\n": "&#x000A;", "\r": "&#x000D;"})
        # The macOS layout compiler drops standalone named XML entities in
        # action outputs. Numeric references work, including for &, < and >.
        for named, numeric in [("&amp;", "&#x0026;"), ("&lt;", "&#x003C;"),
                               ("&gt;", "&#x003E;"), ("&quot;", "&#x0022;")]:
            quoted = quoted.replace(named, numeric)
        return re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]",
                      lambda m: "&#x%04X;" % ord(m[0]), quoted)

    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<!DOCTYPE keyboard SYSTEM "file://localhost/System/Library/DTDs/KeyboardLayout.dtd">',
             '<!-- Generated by tools/build_layout.py. Sources and adaptations: README.md. -->']

    def emit(element, depth):
        indent = "  " * depth
        attrs = "".join(" %s=%s" % (key, attribute(value)) for key, value in element.attrib.items())
        if len(element):
            lines.append(indent + "<" + element.tag + attrs + ">")
            for child in element:
                emit(child, depth + 1)
            lines.append(indent + "</" + element.tag + ">")
        else:
            lines.append(indent + "<" + element.tag + attrs + "/>")
    emit(root, 0)
    return "\n".join(lines) + "\n"


def parse_layout(xml):
    """Parse Apple control references through XML-safe placeholders for tests."""
    def replace(match):
        code = int(match[1], 16)
        return chr(0xE000 + code) if code < 32 and code not in [9, 10, 13] else match[0]
    root = ET.fromstring(re.sub(r"&#x([0-9A-Fa-f]+);", replace, xml))
    for element in root.iter():
        for key, value in element.attrib.items():
            element.set(key, "".join(chr(ord(c) - 0xE000) if 0xE000 <= ord(c) < 0xE020 else c
                                     for c in value))
    return root


def make_bundle_info(variant="E2"):
    # Apple's TextInputSources.h requires KLInfo_<keyboard name>, including
    # spaces and punctuation, not the keylayout filename.
    config = VARIANTS[variant]
    return {
        "CFBundleIdentifier": "local.keyboardlayout.German" + variant,
        "CFBundleName": "German" + variant,
        "CFBundlePackageType": "BNDL",
        "CFBundleInfoDictionaryVersion": "6.0",
        "CFBundleDevelopmentRegion": "de",
        "CFBundleShortVersionString": "1.2.0",
        "CFBundleVersion": "3",
        "KLInfo_" + config["internal"]: {
            "TISInputSourceID": config["source"],
            "TISIntendedLanguage": "de",
        },
    }


def build_variant(variant):
    config = VARIANTS[variant]
    reference = load_reference(variant)
    cases, missing = reference.transition_cases()
    # These two records require a character not directly available while a
    # selector is pending. Preserve them as unbound actions, but do not invent
    # an additional E2 key combination to reach them.
    expected_missing = ["02DA+00D7", "02DF+200A"] if variant == "E2" else []
    if missing != expected_missing:
        raise ValueError("Unreachable reference transitions: " + repr(missing))
    root = make_layout(reference)
    out = ROOT / "dist"
    out.mkdir(exist_ok=True)
    layout = out / ("German" + variant + ".keylayout")
    layout.write_text(render_layout(root), encoding="utf-8")
    contents = out / ("German" + variant + ".bundle/Contents")
    resources = contents / "Resources"
    resources.mkdir(parents=True, exist_ok=True)
    (resources / (config["internal"] + ".keylayout")).write_bytes(layout.read_bytes())
    # Retire only the obsolete, known-generated resource from the first E2 bundle.
    legacy = resources / ("German" + variant + ".keylayout")
    if legacy.exists():
        if b"Generated by tools/build_layout.py." not in legacy.read_bytes():
            raise ValueError("Refusing to remove unknown legacy resource: " + str(legacy))
        legacy.unlink()
    (contents / "Info.plist").write_bytes(plistlib.dumps(make_bundle_info(variant)))
    for language in ["de", "en"]:
        localization = resources / (language + ".lproj")
        localization.mkdir(exist_ok=True)
        (localization / "InfoPlist.strings").write_text(
            '"%s" = "%s";\n' % (config["internal"], config["name"]), encoding="utf-16")
    vectors = [
        {"name": name, "events": [[code, MODIFIERS[index]] for code, index in events],
         "expected": expected}
        for name, events, expected, _ in cases
    ]
    # Include each directly mapped event and important Mac-specific behaviours.
    for index, keymap in reference.maps.items():
        for code, (kind, char) in keymap.items():
            vectors.append({"name": "map%d/key%d" % (index, code),
                            "events": [[code, MODIFIERS[index]]],
                            "expected": "" if kind in {"dead", "noop"} else char})
    vectors.extend([
        {"name": "cancel/backspace", "events": [[3, 8], [51, 0], [17, 0]], "expected": "t"},
        {"name": "cancel/escape", "events": [[24, 0], [53, 0], [14, 0]], "expected": "\x1be"},
        {"name": "cancel/command", "events": [[24, 0], [16, 1], [14, 0]], "expected": "ze"},
        {"name": "right-option/ex", "events": [[3, 64], [17, 0]], "expected": "þ"},
        {"name": "right-shift/upper", "events": [[0, 32]], "expected": "A"},
    ])
    vector_file = "native-cases.json" if variant == "E2" else "native-cases-E1.json"
    (out / vector_file).write_text(json.dumps(
        {"layoutName": config["name"], "inputSourceID": config["source"], "language": "de",
         "keyboardTypes": config["types"], "includeCurrentKeyboard": variant == "E2", "cases": vectors},
        ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Built dist/German%s.bundle (German language)" % variant)
    print("%d physically reachable dead-key transitions; %d states; %d native test vectors" %
          (len(cases), len(reference.state_paths()), len(vectors)))
    print("%d additional reference transitions preserved as unbound character actions" % len(missing))


def build():
    for variant in ["E2", "E1"]:
        build_variant(variant)


if __name__ == "__main__":
    build()
