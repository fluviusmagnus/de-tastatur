#!/usr/bin/env python3
"""Back up and plan a one-key preference change. This does not apply it."""

import copy
from datetime import datetime
import json
from pathlib import Path
import plistlib
import shutil


def make_plan(builtin, thirdparty):
    before = builtin.get("AppleEnabledInputSources")
    third = thirdparty.get("AppleEnabledThirdPartyInputSources")
    if not isinstance(before, list) or not isinstance(third, list):
        raise ValueError("Missing enabled input-source preference arrays")
    e2 = {"InputSourceKind": "Keyboard Layout", "KeyboardLayout Name": "GermanE2ANSI",
          "KeyboardLayout ID": -21374}
    if not any(all(record.get(key) == value for key, value in e2.items()) for record in third):
        raise ValueError("The verified E2 layout is not persistently enabled in com.apple.inputsources")
    after = []
    for record in before:
        if (record.get("InputSourceKind") == "Keyboard Layout"
                and record.get("KeyboardLayout Name") == "German-DIN-2137"):
            if record.get("KeyboardLayout ID") != -18133:
                raise ValueError("Unexpected numeric ID for the built-in German layout")
        else:
            after.append(record)
    return copy.deepcopy({
        "domain": "com.apple.HIToolbox", "key": "AppleEnabledInputSources",
        "before": before, "after": after, "thirdPartyBefore": third,
        "replacementID": "local.keyboardlayout.GermanE2.keylayout.GermanE2ANSI",
    })


def main():
    root = Path(__file__).resolve().parents[1]
    preferences = Path.home() / "Library/Preferences"
    builtin = preferences / "com.apple.HIToolbox.plist"
    thirdparty = preferences / "com.apple.inputsources.plist"
    plan = make_plan(plistlib.loads(builtin.read_bytes()), plistlib.loads(thirdparty.read_bytes()))
    backup = root / ".backups" / ("retire-standard-" + datetime.now().strftime("%Y%m%d-%H%M%S"))
    backup.mkdir(mode=0o700, parents=True, exist_ok=False)
    for source in [builtin, thirdparty]:
        target = backup / source.name
        shutil.copy2(source, target)
        target.chmod(0o600)
    output = backup / "plan.json"
    output.write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n")
    output.chmod(0o600)
    print("Backed up both preference domains. No settings changed.")
    print("Plan:", output.relative_to(root))
    print("Records to remove:", len(plan["before"]) - len(plan["after"]))


if __name__ == "__main__":
    main()
