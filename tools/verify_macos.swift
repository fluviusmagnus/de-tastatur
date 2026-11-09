// Verify an installed layout without enabling or selecting it.
// swift tools/verify_macos.swift dist/native-cases.json [--register /path/to/GermanE2.bundle]
import Carbon
import Foundation

struct TestCase: Decodable {
    let name: String
    let events: [[UInt32]]
    let expected: String
}

struct TestSuite: Decodable {
    let layoutName: String
    let inputSourceID: String
    let language: String
    let keyboardTypes: [UInt32]
    let includeCurrentKeyboard: Bool
    let cases: [TestCase]
}

func fail(_ message: String) -> Never {
    FileHandle.standardError.write(Data(("ERROR: " + message + "\n").utf8))
    exit(1)
}

func property(_ source: TISInputSource, _ key: CFString) -> String? {
    guard let pointer = TISGetInputSourceProperty(source, key) else { return nil }
    return Unmanaged<CFString>.fromOpaque(pointer).takeUnretainedValue() as String
}

let args = Array(CommandLine.arguments.dropFirst())
guard args.count == 1 || (args.count == 3 && args[1] == "--register") else {
    fail("Usage: swift tools/verify_macos.swift dist/native-cases.json [--register installed.bundle]")
}
let suite: TestSuite
do {
    suite = try JSONDecoder().decode(TestSuite.self, from: Data(contentsOf: URL(fileURLWithPath: args[0])))
} catch {
    fail("Cannot read test vectors: \(error)")
}

let original = TISCopyCurrentKeyboardInputSource().takeRetainedValue()
let originalID = property(original, kTISPropertyInputSourceID)
if args.count == 3 {
    let url = URL(fileURLWithPath: args[2]).standardizedFileURL
    let status = TISRegisterInputSource(url as CFURL)
    guard status == noErr else { fail("TISRegisterInputSource failed: \(status)") }
    print("Registered \(url.path) (not enabled or selected)")
}

let sources = TISCreateInputSourceList(nil, true).takeRetainedValue() as! [TISInputSource]
let matches = sources.filter { property($0, kTISPropertyInputSourceID) == suite.inputSourceID }
guard matches.count == 1, let source = matches.first else {
    fail("Expected one installed \(suite.layoutName) source, found \(matches.count). Install/register or log out and retry.")
}
guard property(source, kTISPropertyLocalizedName) == suite.layoutName else {
    fail("Installed layout name does not match test vectors")
}
guard let languagesPointer = TISGetInputSourceProperty(source, kTISPropertyInputSourceLanguages) else {
    fail("Input source does not declare a language")
}
let languages = Unmanaged<CFArray>.fromOpaque(languagesPointer).takeUnretainedValue() as! [String]
guard languages.first == suite.language else {
    fail("Expected primary language \(suite.language), got \(languages)")
}
print("Primary language: \(languages.first ?? "?")")
guard let pointer = TISGetInputSourceProperty(source, kTISPropertyUnicodeKeyLayoutData) else {
    fail("macOS did not compile the layout to Unicode keyboard data")
}
let data = Unmanaged<CFData>.fromOpaque(pointer).takeUnretainedValue()
guard let bytes = CFDataGetBytePtr(data) else { fail("Empty Unicode keyboard data") }
// TIS owns its property storage and can refresh it when registrations change.
// Keep an independent, aligned snapshot for the complete translation run.
let byteCount = CFDataGetLength(data)
let storage = UnsafeMutableRawPointer.allocate(
    byteCount: byteCount, alignment: MemoryLayout<UCKeyboardLayout>.alignment
)
storage.copyMemory(from: bytes, byteCount: byteCount)
defer { storage.deallocate() }
let layout = UnsafeRawPointer(storage).assumingMemoryBound(to: UCKeyboardLayout.self)
let types = Array(Set(suite.keyboardTypes + (suite.includeCurrentKeyboard ? [UInt32(LMGetKbdType())] : []))).sorted()
print("Keyboard types: \(types)")
var failures = 0
var checks = 0
print("Source: \(property(source, kTISPropertyInputSourceID) ?? "?")")
if let enabled = TISGetInputSourceProperty(source, kTISPropertyInputSourceIsEnabled) {
    let value = Unmanaged<CFBoolean>.fromOpaque(enabled).takeUnretainedValue()
    print("Enabled in input menu: \(CFBooleanGetValue(value))")
}
for type in types {
    for test in suite.cases {
        var state: UInt32 = 0
        var actual = ""
        for event in test.events {
            guard event.count == 2, let code = UInt16(exactly: event[0]) else {
                fail("Malformed event in \(test.name)")
            }
            var count = 0
            var output = [UniChar](repeating: 0, count: 256)
            let status = UCKeyTranslate(
                layout, code, UInt16(kUCKeyActionDown), event[1], type, 0,
                &state, output.count, &count, &output
            )
            guard status == noErr else { fail("UCKeyTranslate failed: \(status), \(test.name)") }
            actual += String(utf16CodeUnits: output, count: count)
        }
        checks += 1
        if actual != test.expected {
            failures += 1
            if failures <= 30 {
                print("FAIL type=\(type) \(test.name): expected \(test.expected.debugDescription), got \(actual.debugDescription)")
            }
        }
    }
}
let current = TISCopyCurrentKeyboardInputSource().takeRetainedValue()
guard property(current, kTISPropertyInputSourceID) == originalID else {
    fail("Current input source changed while verifying; this tool did not request a switch")
}
print("\(checks) native checks; \(failures) failures; current input source unchanged")
if failures > 0 { exit(1) }
