# 验证记录

> **范围说明：** 本文是 2026-11-09 在项目作者本机上的点时间验证记录，不是对
> 所有 macOS 版本、硬件和应用的通用保证。复现方式见 [`README.md`](README.md)。

日期：2026-11-09。环境：macOS 27.2，build 26B123；当前硬件键盘类型由 `LMGetKbdType()` 返回 91。

## 离线测试

命令：`python3 -m unittest discover -s tests -v`

最终结果：**31 个测试全部通过**（23 个布局测试、8 个定点修改保护测试）。生成结果可重现，两个 Library 安装包与成品完全一致，
10 个参考文件的 SHA-256 均通过核对（原有 8 个文件未改变，新增 2 个 E1 文件）。

覆盖内容：

- 生成 XML 的独立解释器：普通层、Shift、Option、Caps、Command、Control、取消及回退行为。
- E2 参考表全部 **1,509** 条转换，按字符级动作逐条核对；其中 **1,507** 条可用按键路径到达。
- E1 使用独立参考表，全部 **1,508** 条转换可用 ISO 键码路径到达，逐条核对完整输入序列。
- 两版各有 **92** 个可到达死键状态，包括中间状态。
- Linux `de(e1)` / `de(e2)` 的 ISO / ANSI 普通层、Shift、AltGr 及扩展字符层交叉核对。
- XML 动作／状态引用、重复键码、输出长度、特殊字符转义回归检查。

### E2 的两条不能直接由物理键到达的参考记录

- `02DA+00D7`：ring 选择之后输入 `×`。
- `02DF+200A`：扩展选择之后输入 hair space。

`×` 和 hair space 本身需要通过选择序列产生，不能在已有待定状态中直接从 E2
物理按键输入。生成文件保留相应字符动作，并做字符级测试，但未发明额外快捷键来暴露它们。

## macOS 原生验证

经用户明确许可，仅安装至当前用户 Library 目录，再调用 `TISRegisterInputSource`。
验证工具不启用或选择输入源；验证前后当前输入源相同。

命令：

```sh
swift tools/verify_macos.swift dist/native-cases.json --register "$HOME/Library/Keyboard Layouts/GermanE2.bundle"
swift tools/verify_macos.swift dist/native-cases-E1.json --register "$HOME/Library/Keyboard Layouts/GermanE1.bundle"
```

系统加载并确认两版的主语言均为 **`de`**，因此按德语分类，不再使用无主语言的裸布局登记。

| 布局 | 输入源 ID | 向量数 | 键盘类型 | 原生检查 |
| --- | --- | --- | --- | --- |
| E2 ANSI | `local.keyboardlayout.GermanE2.keylayout.GermanE2ANSI` | 2,512 | 40、91 | 5,024 项，0 失败 |
| E1 ISO | `local.keyboardlayout.GermanE1.keylayout.GermanE1ISO` | 2,513 | 38、41 | 5,026 项，0 失败 |

38 / 41 是 SDK 定义的便携 USB ISO / 第三方 ISO 类型；是系统 API 模拟测试，不是实体 ISO 键盘测试。

布局包内部 keylayout 的 SHA-256：

- E2：`fc9b6118ac16bae04793b61448c087ccb6341572a10eefffd32fa4a90eae2656`
- E1：`fda1c1a5af1a06561b9c7465311ba81c79cd935e1f00372661233f8f98819c46`

原先 `org.unknown.keylayout.GermanE2ANSI` 已停用并从可枚举输入源中消失，裸文件移至项目 `.backups/`。
迁移时曾认为 E2 未持久保存；后续排查已纠正：第三方启用列表在独立的 `com.apple.inputsources` 域，E2 已正确保存。
排查期间经授权短暂选中 E2 的事务失败，已回滚并恢复鼠须管；原生转换验证工具本身从不选择输入源。

## 旧系统德语的定点修改验证

- 备份及计划：`.backups/retire-standard-20261109-012208/`。
- Swift 工具 `--check` 和 `--apply` 均运行通过。
- 独立 Swift 进程通过 CFPreferences 读回计划应用后的列表及未变的第三方列表。
- Python 对比完整备份与磁盘文件：HIToolbox 仅 `AppleEnabledInputSources` 改变，恰好删除旧德语一条；第三方文件字节完全未变。
- 新枚举确认旧德语与 ABC 均未启用，E2 启用、E1 未启用；当前鼠须管，当前键盘布局仍为 E2。
- 尚未注销重登录，不能据此宣称最终持久修复。流程与受保护回滚命令见 `INPUT-SOURCE-REPAIR.md`。

迁移期间还出现过一次 E1 `UCKeyTranslate` 的输出缓冲区错误；重新注册后复测通过。
验证工具增加了独立键盘数据快照，但未证明缓存错误的根因；建议注销重登后再使用，
以刷新迁移期间的旧登记。不要将一次成功解释为所有运行环境均已人工验证。

除了全部可到达的死键转换，还包括直接按键映射、右 Option、右 Shift、取消和快捷键行为。

首次原生测试发现 12 个失败（两个键盘类型各 6 个）：Apple 编译器在动作输出中
丢弃了使用 XML 命名实体的 `&`、`<`、`>`。改为数值引用后完整复测通过，
并增加离线回归测试。不能仅以普通 XML 解析成功代替原生加载验证。

## 尚未人工验证

- 逐键按压实体键盘并核对印字位置。
- 各个编辑器、终端、浏览器及其自定义快捷键。
- 登录窗口、FileVault、密码对话框（不保证当前用户自定义布局可用）。
- ISO / JIS 实体硬件与外接数字键盘；本机 ANSI 已进行 API 验证，ISO 仅模拟验证。
