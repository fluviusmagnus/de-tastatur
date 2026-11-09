"""Generated macOS layout behaviour, checked against the saved Windows tables."""

import unittest
import re

from tools.build_layout import NAME, ROOT, VARIANTS, load_reference, make_bundle_info, make_layout, parse_layout, render_layout


class LayoutInterpreter:
    """Small independent interpreter for the emitted key/action subset."""

    def __init__(self, xml):
        root = parse_layout(xml)
        self.maps = {
            int(m.get("index")): {int(k.get("code")): k.attrib for k in m}
            for m in root.findall("keyMapSet/keyMap")
        }
        self.actions = {
            a.get("id"): {w.get("state"): w.attrib for w in a}
            for a in root.findall("actions/action")
        }
        self.state = "none"

    def press(self, code, index=0):
        key = self.maps[index][code]
        if "action" in key:
            rule = self.actions[key["action"]][self.state]
        else:
            rule = key
        self.state = rule.get("next", "none")
        return rule.get("output", "")

    def sequence(self, events):
        return "".join(self.press(code, index) for code, index in events)


class LayoutTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.reference = load_reference()
        cls.root = make_layout(cls.reference)
        cls.xml = render_layout(cls.root)

    def setUp(self):
        self.keyboard = LayoutInterpreter(self.xml)

    def test_reference_is_pinned_and_complete(self):
        self.assertEqual(len(self.reference.transitions), 1509)

    def test_bundle_declares_german_language(self):
        info = make_bundle_info()
        self.assertIn(".keyboardlayout.", info["CFBundleIdentifier"])
        self.assertEqual(info["CFBundlePackageType"], "BNDL")
        self.assertEqual(info["CFBundleDevelopmentRegion"], "de")
        layout = info["KLInfo_" + VARIANTS["E2"]["internal"]]
        self.assertEqual(layout["TISIntendedLanguage"], "de")
        self.assertEqual(layout["TISInputSourceID"], "local.keyboardlayout.GermanE2.keylayout.GermanE2ANSI")

    def test_e1_iso_positions_and_german_bundle(self):
        reference = load_reference("E1")
        keyboard = LayoutInterpreter(render_layout(make_layout(reference)))
        self.assertEqual(len(reference.transitions), 1508)
        self.assertEqual(keyboard.press(10, 1), "°")
        self.assertEqual(keyboard.press(10, 4), "×")
        self.assertEqual(keyboard.press(50), "<")
        self.assertEqual(keyboard.press(50, 1), ">")
        self.assertEqual(keyboard.press(50, 4), "|")
        self.assertEqual(keyboard.press(19, 4), "²")
        self.assertEqual(keyboard.press(20, 4), "³")
        self.assertEqual(keyboard.sequence([(3, 4), (30, 0)]), "±")
        self.assertEqual(keyboard.sequence([(3, 4), (50, 0)]), "≤")
        info = make_bundle_info("E1")
        metadata = info["KLInfo_" + VARIANTS["E1"]["internal"]]
        self.assertEqual(metadata["TISIntendedLanguage"], "de")
        self.assertEqual(metadata["TISInputSourceID"], "local.keyboardlayout.GermanE1.keylayout.GermanE1ISO")

    def test_all_e1_physically_reachable_transitions(self):
        reference = load_reference("E1")
        cases, missing = reference.transition_cases()
        self.assertEqual(missing, [])
        self.assertEqual(len(cases), 1508)
        keyboard = LayoutInterpreter(render_layout(make_layout(reference)))
        for name, events, expected, pending in cases:
            with self.subTest(transition=name):
                keyboard.state = "none"
                self.assertEqual(keyboard.sequence(events), expected)
                self.assertEqual(keyboard.state != "none", pending)

    def test_linux_ansi_layers_agree_with_windows(self):
        self.check_linux_layers("E2")

    def test_linux_iso_layers_agree_with_windows(self):
        self.check_linux_layers("E1")

    def check_linux_layers(self, variant):
        reference = load_reference(variant)
        keyboard = LayoutInterpreter(render_layout(make_layout(reference)))
        source = (ROOT / "references/linux/xkeyboard-config-2.48/symbols/de").read_text()
        definitions = {}
        for part in (["e1", "e2"] if variant == "E2" else ["e1"]):
            body = re.search(r'^xkb_symbols "' + part + r'" \{(.*?)^\s*\};',
                             source, re.M | re.S)[1]
            for match in re.finditer(r'key\s+<([^>]+)>\s*\{\[([^\]]+)\]', body):
                definitions[match[1]] = [s.strip() for s in match[2].split(",")]
        codes = {"TLDE": 50, "BKSL": 42, "SPCE": 49}
        if variant == "E1":
            codes.update({"TLDE": 10, "LSGT": 50})
        for row, keys in [
            ("AE", [18, 19, 20, 21, 23, 22, 26, 28, 25, 29, 27, 24]),
            ("AD", [12, 13, 14, 15, 17, 16, 32, 34, 31, 35, 33, 30]),
            ("AC", [0, 1, 2, 3, 5, 4, 38, 40, 37, 41, 39]),
            ("AB", [6, 7, 8, 9, 11, 45, 46, 43, 47, 44]),
        ]:
            codes.update({"%s%02d" % (row, i + 1): code for i, code in enumerate(keys)})
        symbols = dict(zip(
            "degree exclam rightsinglequotemark quotedbl section dollar emdash percent "
            "exclamdown ampersand questiondown slash braceleft parenleft bracketleft "
            "parenright bracketright equal braceright ssharp question backslash sterling "
            "EuroSign at masculine ordfeminine schwa SCHWA trademark registered thorn THORN "
            "ezh EZH downarrow uparrow idotless oslash Oslash rightarrow leftarrow "
            "udiaeresis Udiaeresis plus asterisk asciitilde plusminus seconds minutes "
            "lstroke Lstroke odiaeresis Odiaeresis oe OE adiaeresis Adiaeresis ae AE "
            "numbersign apostrophe less greater bar guillemotright guillemotleft "
            "doublelowquotemark singlelowquotemark leftdoublequotemark leftsinglequotemark "
            "rightdoublequotemark endash eng ENG mu comma semicolon period colon "
            "periodcentered minus underscore hyphen space nobreakspace onequarter onehalf "
            "threequarters brokenbar paragraph currency permille copyright cent division notsign".split(),
            list("°!’\"§$—%¡&¿/{([)]=}ß?\\£€@ºªəƏ™®þÞʒƷ↓↑ıøØ→←üÜ+*~±″′łŁöÖœŒäÄæÆ#'<>|»«„‚“‘”–ŋŊµ,;.:·-_\u00ad \u00a0¼½¾¦¶¤‰©¢÷¬")
        ))
        accents = dict(zip(
            "dead_circumflex dead_acute dead_grave dead_abovedot dead_macron dead_doubleacute "
            "dead_caron dead_diaeresis dead_breve dead_tilde dead_abovering dead_hook dead_horn "
            "dead_belowmacron dead_cedilla dead_belowcomma dead_ogonek dead_belowdot "
            "dead_stroke ISO_Level5_Latch".split(),
            list("^´`˙¯˝ˇ¨˘˜˚ˀʼˍ¸ˏ˛ˌ˗˟")
        ))
        symbols.update({"notequal": "≠", "multiply": "×", "eth": "ð", "ETH": "Ð", "ellipsis": "…"})
        symbols.update({"lessthanequal": "≤", "greaterthanequal": "≥"})
        symbols.update({"twosuperior": "²", "threesuperior": "³"})

        def decode(symbol):
            if len(symbol) == 1:
                return symbol
            if re.fullmatch(r"U[0-9A-Fa-f]{4,8}", symbol):
                return chr(int(symbol[1:], 16))
            return symbols[symbol]

        checked = 0
        for position, code in codes.items():
            columns = definitions[position]
            for column, index in [(0, 0), (1, 1), (2, 4), (4, 0), (5, 1)]:
                symbol = columns[column]
                if symbol in {"any", "Multi_key"}:
                    continue  # Linux Compose vs Windows smiley is a documented choice.
                with self.subTest(position=position, column=column):
                    if column < 3:
                        expected = ("dead", accents[symbol]) if symbol in accents else ("text", decode(symbol))
                        self.assertEqual(reference.maps[index][code], expected)
                    else:
                        keyboard.state = "none"
                        self.assertEqual(keyboard.sequence([(3, 4), (code, index)]), decode(symbol))
                checked += 1
        self.assertGreater(checked, 220)

    def test_special_xml_characters_use_numeric_references(self):
        # Regression: macOS successfully loaded named-entity outputs but dropped
        # &, < and > when typing, unlike the independent XML interpreter.
        for entity in ["&amp;", "&lt;", "&gt;"]:
            self.assertNotIn(entity, self.xml)
        for entity in ["&#x0026;", "&#x003C;", "&#x003E;"]:
            self.assertIn(entity, self.xml)

    def test_output_length_limit(self):
        for element in self.root.iter():
            self.assertLessEqual(len(element.get("output", "").encode("utf-16-le")) // 2,
                                 int(self.root.get("maxout")))

    def test_basic_ansi_positions(self):
        self.assertEqual(self.keyboard.press(16), "z")
        self.assertEqual(self.keyboard.press(6), "y")
        self.assertEqual(self.keyboard.press(50, 1), "°")
        self.assertEqual(self.keyboard.press(50, 4), "|")
        self.assertEqual(self.keyboard.press(19, 4), "<")
        self.assertEqual(self.keyboard.press(20, 4), ">")

    def test_extended_selector(self):
        for code, index, expected in [
            (17, 0, "þ"), (17, 1, "Þ"), (19, 0, "½"),
            (8, 0, "¢"), (8, 1, "©"), (41, 0, "œ"), (39, 0, "æ"),
        ]:
            with self.subTest(code=code, index=index):
                self.assertEqual(self.keyboard.press(3, 4), "")
                self.assertEqual(self.keyboard.press(code, index), expected)
                self.assertEqual(self.keyboard.state, "none")

    def test_accent_positions(self):
        for key, expected in [(13, "ā"), (17, "ǎ"), (34, "ã")]:
            self.assertEqual(self.keyboard.sequence([(key, 4), (0, 0)]), expected)

    def test_special_selectors(self):
        for prefix, code, expected in [
            (17, 18, "₁"), (33, 0, "α"),
            (33, 18, "⅛"), (32, 18, "⅓"), (31, 18, "①"),
        ]:
            with self.subTest(prefix=prefix):
                self.assertEqual(
                    self.keyboard.sequence([(prefix, 4), (code, 0)]), expected
                )

    def test_ipa_uses_three_steps(self):
        self.assertEqual(self.keyboard.sequence([(15, 4), (14, 0), (23, 0)]), "ɛ")

    def test_chained_vietnamese_diacritics(self):
        for events in [
            [(33, 4), (41, 4), (32, 0)],
            [(41, 4), (33, 4), (32, 0)],
        ]:
            self.assertEqual(self.keyboard.sequence(events), "ự")

    def test_superscripts(self):
        self.assertEqual(self.keyboard.sequence([(50, 0), (19, 0)]), "²")

    def test_pending_state_cancellation(self):
        self.keyboard.press(3, 4)
        self.assertEqual(self.keyboard.press(51), "")
        self.assertEqual(self.keyboard.press(17), "t")
        self.keyboard.press(24)
        self.assertEqual(self.keyboard.press(53), "\x1b")
        self.assertEqual(self.keyboard.press(14), "e")

    def test_command_uses_german_positions_and_cancels_dead_state(self):
        self.keyboard.press(24)
        self.assertEqual(self.keyboard.press(16, 6), "z")
        self.assertEqual(self.keyboard.press(6, 6), "y")
        self.assertEqual(self.keyboard.press(14), "e")

    def test_control_shortcuts(self):
        self.assertEqual(self.keyboard.press(16, 8), "\x1a")
        self.assertEqual(self.keyboard.press(6, 8), "\x19")
        self.assertEqual(self.keyboard.press(0, 8), "\x01")

    def test_native_caps_lock(self):
        self.assertEqual(self.keyboard.press(0, 2), "A")
        self.assertEqual(self.keyboard.press(0, 3), "a")
        self.assertEqual(self.keyboard.press(18, 2), "1")
        self.assertEqual(self.keyboard.press(18, 3), "!")

    def test_no_internal_state_characters_leak_on_fallback(self):
        # Circumflex + acute creates a Windows-internal intermediate state U+0531.
        self.assertEqual(self.keyboard.sequence([(50, 0), (24, 0)]), "")
        result = self.keyboard.press(18)
        self.assertNotIn("Ա", result)
        self.assertTrue(result.endswith("1"))

    def test_every_reference_transition(self):
        # Prefix paths and expected results come directly from the Windows graph,
        # not from evaluating the generated XML.
        cases, missing = self.reference.transition_cases()
        self.assertEqual(missing, ["02DA+00D7", "02DF+200A"])
        self.assertEqual(len(cases), 1507)
        for name, events, expected, pending in cases:
            with self.subTest(transition=name):
                keyboard = self.keyboard
                keyboard.state = "none"
                self.assertEqual(keyboard.sequence(events), expected)
                self.assertEqual(keyboard.state != "none", pending)

    def test_all_1509_reference_records_at_character_level(self):
        for (state, char), (result, dead) in self.reference.transitions.items():
            with self.subTest(state=state, char=char):
                # All incoming characters have an action, including the two
                # unbound inputs that cannot be produced by a physical E2 key.
                candidates = [
                    rules for rules in self.keyboard.actions.values()
                    if rules["none"].get("output") == char and "next" not in rules["none"]
                ]
                expected = {"state": "d%04X" % ord(state)}
                expected["next" if dead else "output"] = "d%04X" % ord(result) if dead else result
                self.assertTrue(any(rules[expected["state"]] == expected for rules in candidates))

    def test_structure_has_no_duplicate_keys_or_undefined_references(self):
        root = parse_layout(self.xml)
        actions = root.findall("actions/action")
        action_ids = {a.get("id") for a in actions}
        self.assertEqual(len(action_ids), len(actions))
        states = {"none"} | {w.get("state") for a in actions for w in a}
        terminators = {w.get("state") for w in root.findall("terminators/when")}
        self.assertEqual(states - {"none"}, terminators)
        for keymap in root.findall("keyMapSet/keyMap"):
            codes = [k.get("code") for k in keymap]
            self.assertEqual(len(codes), len(set(codes)))
            for key in keymap:
                if key.get("action"):
                    self.assertIn(key.get("action"), action_ids)
        for action in actions:
            self.assertEqual({w.get("state") for w in action}, states)
            self.assertEqual(len(action), len(states))
            for when in action:
                if when.get("next"):
                    self.assertIn(when.get("next"), states)


if __name__ == "__main__":
    unittest.main()
