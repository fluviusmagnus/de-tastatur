# 第三方材料与许可说明

**中文** | [English](THIRD-PARTY-NOTICES.en.md) | [Deutsch](THIRD-PARTY-NOTICES.de.md)

本仓库的 **源代码、构建脚本、测试及生成的 macOS 布局文件** 采用根目录
[`LICENSE`](LICENSE) 中的 MIT 许可证。

`references/` 目录保存的是布局实现所用的参考材料，**不属于 MIT 许可范围**。
其中部分内容来自第三方，版权归各自权利人所有，这里仅作为技术参考与快照保留。
本项目生成的布局文件是根据公开的键位行为重新实现的结果，不包含第三方源代码、
驱动二进制或运行时组件。

## Linux：xkeyboard-config 2.48

- 上游项目：<https://gitlab.freedesktop.org/xkeyboard-config/xkeyboard-config>
- 发布包：<https://www.x.org/releases/individual/data/xkeyboard-config/xkeyboard-config-2.48.tar.xz>
- 本地位置：`references/linux/xkeyboard-config-2.48/`
- 许可：X11／MIT 风格的宽松许可，完整文本见
  `references/linux/xkeyboard-config-2.48/COPYING`。

使用到的文件：`symbols/de`、`symbols/level3`、`symbols/level5`、
`types/level5`、`COPYING`。

## Windows：German Extended E1 / E2

- 驱动：`KBDGRE1.DLL`（E1）、`KBDGRE2.DLL`（E2）
- KLID：E1 为 `00020407`，E2 为 `00030407`
- 页面：<https://kbdlayout.info/KBDGRE1/>、<https://kbdlayout.info/KBDGRE2/>
- 本地位置：`references/windows/`

这些文件是 **kbdlayout.info 根据微软驱动公开表生成的描述性快照**，不是从
Windows 系统或驱动二进制中提取的代码，也没有下载或执行 DLL。它们用于核对键位、
死键状态机与扩展选择行为，使生成过程可复现。

需要注意：

- 文件保留了原始生成内容及其中包含的版权声明。例如 `kbdgre2.klc` 含
  `© Microsoft Corporation. All rights reserved.`。
- 本项目 **不对这些文件授予任何许可**，也不声称拥有其版权。
- 如果权利人认为这些快照不应被再分发，请通过仓库 Issue 联系，我会移除
  相应文件，并改为在构建时按需下载和校验。
- 这些材料只描述键盘布局行为，不包含微软驱动代码、签名或运行时组件。

下载地址与快照校验值见 [`references/README.md`](references/README.md) 和
[`references/SHA256SUMS`](references/SHA256SUMS)。

## 商标与隶属关系

Apple、macOS、Windows、Microsoft、Rime、鼠须管／Squirrel 等名称和商标归各自
权利人所有。本项目与 Apple、Microsoft、X.Org 或 Rime 项目没有隶属、赞助或
背书关系。

## 免责声明

本项目按“现状”提供，不附带任何明示或默示担保。键盘布局、系统输入源注册和
偏好设置修改可能受 macOS 版本、硬件与应用快捷键影响，使用前请自行评估并备份。
