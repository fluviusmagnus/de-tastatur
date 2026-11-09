// A guarded, one-key CFPreferences update; never rewrites an entire plist.
// Usage: swift tools/apply_input_source_plan.swift plan.json --check|--apply|--restore
import Carbon
import Foundation

func fail(_ message: String) -> Never {
    FileHandle.standardError.write(Data(("ERROR: " + message + "\n").utf8))
    exit(1)
}
func same(_ left: [[String: Any]], _ right: [[String: Any]]) -> Bool {
    NSArray(array: left).isEqual(NSArray(array: right))
}
func read(_ domain: String, _ key: String) -> [[String: Any]] {
    guard let value = CFPreferencesCopyValue(key as CFString, domain as CFString,
                                            kCFPreferencesCurrentUser, kCFPreferencesAnyHost),
          let array = value as? [[String: Any]] else { fail("Missing preference array: \(domain)/\(key)") }
    return array
}
func write(_ domain: String, _ key: String, _ value: [[String: Any]]) -> Bool {
    CFPreferencesSetValue(key as CFString, value as CFArray, domain as CFString,
                          kCFPreferencesCurrentUser, kCFPreferencesAnyHost)
    return CFPreferencesSynchronize(domain as CFString, kCFPreferencesCurrentUser, kCFPreferencesAnyHost)
}
func sourceID(_ source: TISInputSource) -> String {
    guard let pointer = TISGetInputSourceProperty(source, kTISPropertyInputSourceID) else { return "?" }
    return Unmanaged<CFString>.fromOpaque(pointer).takeUnretainedValue() as String
}
func flag(_ source: TISInputSource, _ key: CFString) -> Bool {
    guard let pointer = TISGetInputSourceProperty(source, key) else { return false }
    return CFBooleanGetValue(Unmanaged<CFBoolean>.fromOpaque(pointer).takeUnretainedValue())
}

let args = Array(CommandLine.arguments.dropFirst())
guard args.count == 2, ["--check", "--apply", "--restore"].contains(args[1]) else {
    fail("Usage: swift tools/apply_input_source_plan.swift plan.json --check|--apply|--restore")
}
let plan: [String: Any]
do {
    let data = try Data(contentsOf: URL(fileURLWithPath: args[0]))
    guard let decoded = try JSONSerialization.jsonObject(with: data) as? [String: Any] else {
        fail("Plan must be a JSON dictionary")
    }
    plan = decoded
} catch { fail("Cannot read plan: \(error)") }

guard plan["domain"] as? String == "com.apple.HIToolbox",
      plan["key"] as? String == "AppleEnabledInputSources",
      let before = plan["before"] as? [[String: Any]],
      let after = plan["after"] as? [[String: Any]],
      let thirdBefore = plan["thirdPartyBefore"] as? [[String: Any]],
      let replacementID = plan["replacementID"] as? String,
      replacementID == "local.keyboardlayout.GermanE2.keylayout.GermanE2ANSI" else {
    fail("Unexpected plan scope")
}
let expectedAfter = before.filter {
    !(($0["InputSourceKind"] as? String) == "Keyboard Layout"
      && ($0["KeyboardLayout Name"] as? String) == "German-DIN-2137"
      && ($0["KeyboardLayout ID"] as? NSNumber)?.intValue == -18133)
}
guard same(expectedAfter, after), before.count - after.count <= 1 else {
    fail("Plan changes more than the single targeted German record")
}
guard thirdBefore.contains(where: {
    ($0["InputSourceKind"] as? String) == "Keyboard Layout"
    && ($0["KeyboardLayout Name"] as? String) == "GermanE2ANSI"
    && ($0["KeyboardLayout ID"] as? NSNumber)?.intValue == -21374
}) else { fail("Plan has no persisted E2 replacement") }

let domain = "com.apple.HIToolbox", key = "AppleEnabledInputSources"
let expected = args[1] == "--restore" ? after : before
let desired = args[1] == "--restore" ? before : after
guard same(read(domain, key), expected) else { fail("Input-source settings changed since the plan was made; refusing to overwrite") }
guard same(read("com.apple.inputsources", "AppleEnabledThirdPartyInputSources"), thirdBefore) else {
    fail("Third-party settings changed; refusing to apply stale plan")
}
let original = sourceID(TISCopyCurrentKeyboardInputSource().takeRetainedValue())
if args[1] != "--restore" {
    let sources = TISCreateInputSourceList(nil, true).takeRetainedValue() as! [TISInputSource]
    let matches = sources.filter { sourceID($0) == replacementID }
    guard matches.count == 1, let e2 = matches.first,
          flag(e2, kTISPropertyInputSourceIsEnabled), flag(e2, kTISPropertyInputSourceIsASCIICapable),
          sourceID(TISCopyCurrentKeyboardLayoutInputSource().takeRetainedValue()) == replacementID else {
        fail("E2 is not the enabled, ASCII-capable current keyboard layout")
    }
}
if args[1] == "--check" {
    print("CHECK PASSED: one-key plan, settings unchanged, E2 enabled and ASCII-capable. No settings written.")
    exit(0)
}
guard write(domain, key, desired), same(read(domain, key), desired) else {
    let restored = write(domain, key, expected)
    fail("Write/readback failed; restoration requested: \(restored)")
}
guard same(read("com.apple.inputsources", "AppleEnabledThirdPartyInputSources"), thirdBefore),
      sourceID(TISCopyCurrentKeyboardInputSource().takeRetainedValue()) == original else {
    let restored = write(domain, key, expected)
    fail("Unrelated settings or current input source changed; restoration requested: \(restored)")
}
print("\(args[1]) persisted and verified: only \(domain)/\(key) changed.")
print("Third-party sources and current input method unchanged. No logout, restart or cache deletion performed.")
print("The live picker may retain its old state until you log out and back in; this tool does not claim it is fixed yet.")
