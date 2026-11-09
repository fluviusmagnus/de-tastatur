import copy
import unittest

from tools.plan_input_source_retirement import make_plan


def keyboard(name, numeric_id):
    return {"InputSourceKind": "Keyboard Layout", "KeyboardLayout Name": name,
            "KeyboardLayout ID": numeric_id}


class InputSourceRetirementTests(unittest.TestCase):
    def setUp(self):
        self.old = keyboard("German-DIN-2137", -18133)
        self.e2 = keyboard("GermanE2ANSI", -21374)
        self.chinese = {"InputSourceKind": "Input Mode", "Bundle ID": "com.apple.inputmethod.SCIM",
                        "Input Mode": "com.apple.inputmethod.SCIM.Shuangpin"}
        self.rime = {"InputSourceKind": "Input Mode", "Bundle ID": "im.rime.inputmethod.Squirrel",
                     "Input Mode": "im.rime.inputmethod.Squirrel.Hans"}
        self.builtin = {"AppleEnabledInputSources": [self.chinese, self.old],
                        "AppleSelectedInputSources": [self.rime],
                        "AppleCurrentKeyboardLayoutInputSourceID": "keep-selected-source",
                        "AppleInputSourceHistory": [self.old, self.e2]}
        self.thirdparty = {"AppleEnabledThirdPartyInputSources": [self.e2, self.rime]}

    def test_removes_only_exact_builtin_record(self):
        plan = make_plan(self.builtin, self.thirdparty)
        self.assertEqual(plan["before"], [self.chinese, self.old])
        self.assertEqual(plan["after"], [self.chinese])
        self.assertEqual(plan["domain"], "com.apple.HIToolbox")
        self.assertEqual(plan["key"], "AppleEnabledInputSources")

    def test_preserves_other_keyboard_layouts(self):
        abc = keyboard("ABC", 252)
        self.builtin["AppleEnabledInputSources"].append(abc)
        plan = make_plan(self.builtin, self.thirdparty)
        self.assertEqual(plan["after"], [self.chinese, abc])

    def test_requires_persisted_e2_in_thirdparty_domain(self):
        with self.assertRaises(ValueError):
            make_plan(self.builtin, {"AppleEnabledThirdPartyInputSources": [self.rime]})

    def test_rejects_wrong_e2_numeric_id(self):
        self.e2["KeyboardLayout ID"] = -9999
        with self.assertRaises(ValueError):
            make_plan(self.builtin, self.thirdparty)

    def test_rejects_unexpected_old_numeric_id(self):
        self.old["KeyboardLayout ID"] = -9999
        with self.assertRaises(ValueError):
            make_plan(self.builtin, self.thirdparty)

    def test_missing_old_record_is_idempotent(self):
        self.builtin["AppleEnabledInputSources"] = [self.chinese]
        plan = make_plan(self.builtin, self.thirdparty)
        self.assertEqual(plan["before"], plan["after"])

    def test_does_not_mutate_settings_or_history(self):
        before = copy.deepcopy((self.builtin, self.thirdparty))
        plan = make_plan(self.builtin, self.thirdparty)
        plan["before"].clear()
        self.assertEqual((self.builtin, self.thirdparty), before)

    def test_thirdparty_snapshot_preserves_all_entries(self):
        plan = make_plan(self.builtin, self.thirdparty)
        self.assertEqual(plan["thirdPartyBefore"], [self.e2, self.rime])


if __name__ == "__main__":
    unittest.main()
