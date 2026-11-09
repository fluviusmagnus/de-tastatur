# macOS 德语 E2 ANSI / E1 ISO 布局规格与进度

> **范围说明：** 本文是项目设计与验收记录。其中“已安装”“已经用户授权”等状态
> 描述的是项目作者本机的验证过程，不代表所有环境都已配置完成；通用安装步骤见
> [`README.md`](README.md)。

## 目标与基准

- 交付原生 `dist/GermanE2.bundle`，名称 `German E2 (ANSI)`；内部包含生成的 keylayout。
- 通过布局包中相应的 `KLInfo_GermanE2ANSI` / `KLInfo_GermanE1ISO` 声明 `TISIntendedLanguage=de`，归入德语，不以裸 keylayout 安装到“其他”类别。显示名称通过 InfoPlist.strings 本地化。
- 同时交付、安装备用 `dist/GermanE1.bundle`，名称 `German E1 (ISO)`，使用独立 Windows E1 参考表。E1 与 E2 使用不同数字布局 ID 和稳定的输入源 ID。
- 物理键位参考 xkeyboard-config 2.48 的 `de(e1)` + `de(e2)`；字符及完整死键状态机移植自已保存的 Windows KBDGRE2 内部表。
- ANSI 键码：Esc 下方为 `^` 死键 / `°`，AltGr 层为 `|`；Option+2/3 为 `<` / `>`。
- 左右 Option 均为 AltGr；Option+F 后松开，再输入目标键选择扩展字符，Shift 选择相应大写或第二字符。
- 保留全部参考死键转换，包括多重重音、音标、希腊字母、数学字符、分数、上下标。

## macOS 适配约定

- Command 保持德语 QWERTZ，不切回美式；Command 和 Control 快捷键不触发死键，并取消尚未完成的组合。
- Caps Lock 使用原生字母大写习惯，不把数字行锁定为符号；Shift+Caps 字母小写。Caps 不改变 Option 层。
- Option+A 按 Windows 实现输入 `☺`，不重映射为表情面板快捷键。
- Shift+Option 仅保留 Windows 表明确指定的字符；不自行用它代替扩展选择。
- Escape 和退格取消未完成的死键；未完成时退格只取消状态，不删除前文。
- 不匹配的普通字符输出可显示的重音前缀及该字符；不把 Windows 内部中间状态代码作为可见字符输出。
- 同时为可选 ISO 额外键提供扩展选择，但以 ANSI 为验收范围；不重映射 Caps Lock、Fn 或系统级按键。
- 安装与分类迁移均经用户授权。旧裸 E2 退役；后续确认新版 E2 已在第三方偏好域持久启用，E1 作为备用未启用。
- 排查旧系统德语时经授权短暂切换 E2，失败事务已回滚并恢复鼠须管；后续定点修改不切换输入法。
- 经备份和授权，仅移除当前用户 `com.apple.HIToolbox/AppleEnabledInputSources` 中旧德语记录。独立进程及磁盘验证通过；注销重登录后的持久效果待用户验收。详见 `INPUT-SOURCE-REPAIR.md`。

## 验收与进度

- [x] 自动生成可重现的 keylayout，引用来源并保留参考文件不变。
- [x] 用独立解释器核对生成 XML 的普通层、Shift、Option、Command、Control、Caps 和取消行为。
- [x] 穷举 1,507 条可由物理按键到达的死键转换；另外两条做字符级测试。
- [x] 提供 macOS `UCKeyTranslate` 原生验证工具；E2 的 5,024 项、E1 的 5,026 项原生检查通过，主语言均为 `de`。
- [x] E1 全部 1,508 条死键转换可由 ISO 键码路径到达，已逐条核对。
- [x] 提供安装、启用、示例、卸载、平台差异及限制文档。

## 已知验证限制

本机没有找到 Apple `klcompiler`。系统 `TISRegisterInputSource` 的公开接口仅支持
Library 下已安装的布局。用户随后明确许可安装并验证；已完成系统实际加载测试，
但尚未人工逐键测试实体键盘及各应用快捷键；E1 使用系统 ISO 类型 38/41 模拟转换，
并非连接实体 ISO 键盘测试。详见 `TESTING.md`。
