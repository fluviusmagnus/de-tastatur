# 变更记录

**中文** | [English](CHANGELOG.en.md) | [Deutsch](CHANGELOG.de.md)

本项目遵循 [Semantic Versioning](https://semver.org/lang/zh-CN/) 的版本号形式；
`Contents/Info.plist` 中的 `CFBundleShortVersionString` 为对外版本号。

## [1.2.0] - 2026-11-09

首个公开发布版本，沿用现有 bundle 版本号 1.2.0。

### 新增

- German E2 (ANSI) 与 German E1 (ISO) 两个原生 macOS `.bundle` 输入源。
- QWERTZ 键位、左右 Option 作为 AltGr、Option+F 扩展选择。
- 完整死键状态机：重音、多重重音、音标、希腊字母、数学符号、分数、上下标。
- 离线生成器与 31 项单元测试。
- macOS `UCKeyTranslate` 原生验证工具与验证向量。
- 鼠须管 / Rime 中文标点适配说明。
- 输入源迁移与定点修复工具及记录。

### 验证

- 离线测试 31 项全部通过。
- E2：5,024 项原生检查通过，主语言 `de`。
- E1：5,026 项原生检查通过，主语言 `de`。

### 已知限制

- 未逐键人工测试实体键盘、各应用快捷键、登录窗口 / FileVault / 密码对话框。
- E1 的 ISO 路径为系统 API 模拟，未连接实体 ISO 键盘。
- 未在 Intel Mac 或较旧 macOS 上验证。
