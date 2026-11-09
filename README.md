# German E1 / E2 for macOS

**中文** | [English](README.en.md) | [Deutsch](README.de.md)

两个原生 macOS 键盘布局：**German E2 (ANSI)** 和备用 **German E1 (ISO)**，均归入
**德语** 输入源。键位参考 Linux `xkeyboard-config` 2.48 的 `de(e1)` / `de(e2)`，
字符、死键和扩展选择状态机移植自 Windows `KBDGRE1.DLL` / `KBDGRE2.DLL` 的公开布局表。

不依赖 Karabiner、后台服务、辅助功能权限或第三方运行时。

> **English summary:** Native macOS keyboard layouts for German DIN 2137 E1 (ISO)
> and E2 (ANSI), implemented as `.bundle` input sources. QWERTZ, AltGr on both
> Option keys, full dead-key state machines, and Option+F extended selection.
> No background services or accessibility permissions required.

## 特性

- **原生布局包**：标准 `.bundle`，声明 `TISIntendedLanguage=de`，在系统中归入“德语”。
- **QWERTZ**：美式键帽 Y 位置输入 `z`，Z 位置输入 `y`。
- **左右 Option 均为 AltGr**，不使用 Control+Option 模拟。
- **完整死键表**：重音、多重重音、音标、希腊字母、数学符号、分数、上下标等。
- **扩展选择**：按 Option+F，松开，再按目标键；Shift 选择对应大写或第二字符。
- **E2 ANSI** 为主布局；**E1 ISO** 用于带额外键的 ISO 键盘。
- 生成过程可复现，附离线测试与 macOS `UCKeyTranslate` 原生验证工具。

## 支持范围

当前已验证环境：

| 项目 | 值 |
| --- | --- |
| macOS | 27.2（build 26B123） |
| 硬件 | Apple Silicon，`LMGetKbdType()` 返回 91 |
| 键盘 | ANSI 实体键盘 |
| bundle 版本 | 1.2.0（见 `Contents/Info.plist`） |

尚未人工验证：Intel Mac、较旧 macOS、实体 ISO／JIS 键盘、外接数字键盘、
登录窗口／FileVault／密码对话框，以及各应用的自定义快捷键。E1 的 ISO 验证为
系统 API 模拟，不是实体 ISO 键盘测试。详见 [`TESTING.md`](TESTING.md)。

## 安装

### 方式一：使用仓库中的成品

```sh
mkdir -p "$HOME/Library/Keyboard Layouts"
cp -R dist/GermanE2.bundle "$HOME/Library/Keyboard Layouts/"
cp -R dist/GermanE1.bundle "$HOME/Library/Keyboard Layouts/"   # 需要 ISO 备用版时
```

`dist/*.keylayout` 是构建中间文件，**请安装整个 `.bundle`，不要单独安装这些文件**。
若目标位置已有同名文件，请先核对并备份，避免覆盖其他自定义布局。

### 方式二：从源码构建

需要 Python 3.9+；原生验证还需要 macOS 的 Swift Command Line Tools。

```sh
python3 tools/build_layout.py
python3 -m unittest discover -s tests -v
```

构建只生成 `dist/` 下的文件，不会安装、注册或切换输入源。生成后可再按方式一复制。

如需让系统立即发现新安装的布局，可显式注册（不会启用或切换输入源）：

```sh
swift tools/verify_macos.swift dist/native-cases.json \
  --register "$HOME/Library/Keyboard Layouts/GermanE2.bundle"
swift tools/verify_macos.swift dist/native-cases-E1.json \
  --register "$HOME/Library/Keyboard Layouts/GermanE1.bundle"
```

## 启用

1. 打开 **系统设置 → 键盘 → 文本输入 → 编辑**。
2. 点 **＋ → 德语**，查找 **German E2 (ANSI)** 或 **German E1 (ISO)**。
3. 添加后，通过菜单栏输入法菜单切换到该布局。
4. 如果暂未出现在添加列表中，注销并重新登录后再找；必要时重启。

不要在系统设置中删除内置布局文件。当前用户的自定义布局不保证能用于
FileVault 开机解锁、登录窗口或所有密码对话框。

## 使用方式

### E2 与 E1 的选择

ANSI 硬件使用 **E2**。**E1** 留作连接 ISO 键盘时使用；ISO 的左 Shift 较短，
旁边有额外字符键。

| 位置／功能 | E2 ANSI | E1 ISO |
| --- | --- | --- |
| 左 Shift 旁的额外键 | 不需要；若有则作扩展选择 | `<` / Shift `>` / Option &#124; |
| Esc 下方重音键的 Option 层 | &#124; | `×` |
| Option+2 / Option+3 | `<` / `>` | `²` / `³` |
| 扩展选择后按 `+` | `×` | `±` |

两者均按 Option+F、松开后选择扩展字符。下面的物理键位与示例主要按 **E2 ANSI** 描述。

### 基本规则

- 字母为 **QWERTZ**：美式键帽 Y 的位置输入 `z`，美式键帽 Z 的位置输入 `y`。
- **左右 Option 都是 AltGr**，不使用 Control+Option 模拟 AltGr。
- **扩展选择：按 Option+F，松开两个键，再按目标键。**
- 红色层中的大写或第二字符：在目标键那一步加 Shift，不是一直按着 Option。
- 重音死键：先输入重音，再输入字母。Escape 或退格可取消未完成的组合。

### ANSI 键位

这里的“美式键帽”仅用于定位物理按键，不要求键帽实际印有这些字符。

| 美式物理键位置 | E2 普通输出 | Shift 输出 | Option 输出 |
| --- | --- | --- | --- |
| Esc 下方的反引号键 | `^` 死键 | `°` | &#124; |
| `-` 键 | `ß` | `?` | `\` |
| `=` 键 | acute 死键 | grave 死键 | 上点死键 |
| `[` 键 | `ü` | `Ü` | horn／希腊字母选择 |
| `]` 键 | `+` | `*` | `~` |
| `;` 键 | `ö` | `Ö` | 下点死键 |
| 单引号键 | `ä` | `Ä` | 横划选择 |
| 反斜线键 | `#` | `'` | `−` |
| `/` 键 | `-` | `_` | 软连字符 |

### 常用字符

以下数字和 Q/W/E/R/T/F/I 等字母位置在美式与 E2 键盘上相同：

| 操作 | 输出 |
| --- | --- |
| Option+Q / E | `@` / `€` |
| Option+2 / 3 | `<` / `>` |
| Option+7 / 8 / 9 / 0 | `{` / `[` / `]` / `}` |
| Option+W，松开，再按 A | `ā` |
| Option+T，松开，再按 A | `ǎ` |
| Option+I，松开，再按 A | `ã` |
| Option+F，松开，再按 T | `þ` |
| Option+F，松开，再按 Shift+T | `Þ` |
| Option+F，松开，再按 2 | `½` |
| Option+F，松开，再按 Shift+C | `©` |
| Option+F，松开，再按美式 `;` 键 | `œ` |
| Option+R，松开，按 E，再按 5 | `ɛ` |
| Option+美式 `[` 键，松开，再按 A | `α` |
| Option+T，松开，再按 1 | `₁` |
| Esc 下方的 `^` 死键，松开，再按 2 | `²` |

多重重音示例：Option+美式 `[`（horn），松开；Option+美式 `;`（下点），松开；
按 U，得到 `ự`。这两个重音的顺序也可交换。

## macOS 适配与边界

- **Command 保持德语位置**：美式 Y 键的位置是 ⌘Z，通常用于撤销；不会切回美式 QWERTY。
- Command / Control 快捷键绕过死键，并取消未完成的组合。Control+A…Z 按德语字母映射到控制字符。
- Caps Lock 采用 Mac 的字母大写习惯，不把数字行锁成符号；Shift+Caps 为小写。Caps 不改变 Option 层。
- Option+A 输入 `☺`，采用 Windows 的允许实现，不自动打开表情面板。
- Shift+Option 不等于红色扩展层；仅保留 Windows 参考表明确指定的输出，例如 Shift+Option+ß 为 `ẞ`。
- 不匹配的重音组合保留可见前缀；不将 Windows 的内部中间状态码输出成无关字符。
- Escape 和退格取消未完成的死键；未完成时退格只取消状态，不删除前文。
- 数字小键盘小数点采用德语逗号。E2 若遇到 ISO 额外键可用它作扩展选择；E1 则在该键输入 `< > |`。
- 原生 API 验证不等于所有应用的人工测试；应用自定义快捷键、终端 Option 行为等仍可能覆盖系统布局。
- 参考实现和用户布局图并不等于 DIN 标准全文；不宣称通过标准认证。

## 仓库结构

```text
.
├── README.md                 # 本文件（中文）
├── README.en.md              # English
├── README.de.md              # Deutsch
├── LICENSE                   # MIT（适用于本项目代码与生成的布局文件）
├── THIRD-PARTY-NOTICES.md    # references/ 的来源、版权与许可边界（中文）
├── THIRD-PARTY-NOTICES.en.md # English
├── THIRD-PARTY-NOTICES.de.md # Deutsch
├── CHANGELOG.md              # 版本记录（中文）
├── CHANGELOG.en.md           # English
├── CHANGELOG.de.md           # Deutsch
├── SPEC.md                   # 目标、约束、验收标准
├── TESTING.md                # 测试与原生验证记录
├── INPUT-SOURCE-REPAIR.md    # 输入源迁移排障记录（作者本机）
├── RIME-E2.md                # 鼠须管 / Rime 中文标点适配
├── dist/                     # 生成成品与原生验证向量
│   ├── GermanE1.bundle
│   ├── GermanE2.bundle
│   ├── *.keylayout           # 构建中间文件，勿单独安装
│   └── native-cases*.json    # 原生验证用例
├── references/               # 固定版本的第三方参考快照
├── tools/                    # 生成、验证、输入源计划工具
└── tests/                    # 离线单元测试
```

## 构建与验证

```sh
python3 tools/build_layout.py
python3 -m unittest discover -s tests -v
swift tools/verify_macos.swift dist/native-cases.json
swift tools/verify_macos.swift dist/native-cases-E1.json
```

- 离线测试：31 项，覆盖生成 XML、普通层／Shift／Option／Command／Control／Caps、
  取消与回退、E1/E2 全部参考死键转换、参考快照校验和。
- 原生验证：E2 5,024 项、E1 5,026 项，主语言均为 `de`；需要布局已安装并已被系统发现。
- 生成器不安装、不注册、不切换输入源；`--register` 只注册，不启用或切换。
- 更新生成文件后，须另外更新 Library 中的安装副本再注册／重新登录，否则系统可能仍使用旧版本。

完整记录见 [`TESTING.md`](TESTING.md)。`.backups/` 是作者本机的备份目录，
已被 `.gitignore` 排除，**不随仓库发布**；相关文档中的路径仅作复现参考。

## 卸载

先切回 ABC 等系统布局，在系统设置中移除相应输入源，然后删除对应的
`~/Library/Keyboard Layouts/GermanE2.bundle` 或 `GermanE1.bundle`。必要时注销重新登录。
删除项目目录不会自动卸载 Library 中的副本。

## 文档

- [README.en.md](README.en.md) / [README.de.md](README.de.md)：英文／德文版说明。
- [SPEC.md](SPEC.md)：规格、macOS 适配约定与验收标准。
- [TESTING.md](TESTING.md)：离线测试、原生验证、已知限制。
- [INPUT-SOURCE-REPAIR.md](INPUT-SOURCE-REPAIR.md)：旧“德语－标准”输入源的诊断与定点修复记录。
- [RIME-E2.md](RIME-E2.md)：鼠须管 / Rime 的 E2 中文标点适配。
- [references/README.md](references/README.md)：参考来源、版本与校验方式。
- [THIRD-PARTY-NOTICES.md](THIRD-PARTY-NOTICES.md)：第三方材料与许可说明（另有
  [English](THIRD-PARTY-NOTICES.en.md) / [Deutsch](THIRD-PARTY-NOTICES.de.md)）。
- [CHANGELOG.md](CHANGELOG.md)：版本变更记录（另有
  [English](CHANGELOG.en.md) / [Deutsch](CHANGELOG.de.md)）。

## 许可

本项目源代码、构建脚本、测试及生成的布局文件采用 [MIT 许可证](LICENSE)。
`references/` 下的第三方参考材料不适用 MIT，详情见
[THIRD-PARTY-NOTICES.md](THIRD-PARTY-NOTICES.md)。

Apple、macOS、Windows、Microsoft、Rime 等名称与商标归各自权利人所有，
本项目与它们没有隶属或背书关系。
