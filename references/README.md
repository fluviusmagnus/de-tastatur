# E1 / E2 布局实现参考

获取日期：2026-11-09。这里只保存参考数据，未安装或修改系统输入源。

## Linux：xkeyboard-config 2.48

来源：X.Org 官方发布包（本次查阅的发布目录中最新版本）。

- 发布目录：https://www.x.org/releases/individual/data/xkeyboard-config/
- 原始包：https://www.x.org/releases/individual/data/xkeyboard-config/xkeyboard-config-2.48.tar.xz
- 上游项目：https://gitlab.freedesktop.org/xkeyboard-config/xkeyboard-config
- 本地文件：`linux/xkeyboard-config-2.48/`

从发布包原样提取：

| 文件 | 用途 |
| --- | --- |
| `symbols/de` | 德语布局源码；E1 在 94–174 行，E2 在 177–193 行 |
| `types/level5` | 八层按键类型及 Shift、LevelThree、LevelFive 的层选择规则 |
| `symbols/level3` | AltGr / 第三层选择键定义 |
| `symbols/level5` | 第五层选择相关定义 |
| `COPYING` | 上游许可说明 |

E2 声明基于 DIN 2137-1:2023-08，继承 `de(e1)`，再覆盖 `<TLDE>`、
`<AE02>`、`<AE03>`、`<AD12>` 和可选 ISO 额外键 `<LSGT>`。
因此不能仅复制 E2 的短小区块，必须同时读取 E1。

E1 的 F 键第三层是 `ISO_Level5_Latch`：AltGr+F 后的下一键选择第五层，
配合 Shift 选择第六层，也就是布局图中的红色字符。

注意：`symbols/de` 定义的是按键到 keysym 的映射，不是全部死键组合表。
Linux 死键通常还依赖 libX11/libxkbcommon 使用的 Compose 数据。
本目录不是可独立安装的完整 XKB 数据集，也不能仅凭这个文件宣称实现了标准的全部组合。

## Windows：German Extended (E2)

- 驱动：`KBDGRE2.DLL`
- KLID：`00030407`
- 本次导出标记的驱动版本：`10.0.29667.1000`
- 查看页面：https://kbdlayout.info/KBDGRE2/

来自第三方网站 kbdlayout.info 对微软驱动表的解析导出，不是微软发布的开放源码，
也没有下载或执行 DLL。文件保留原始字节和版权声明，不应当作可自由再分发的代码。
这些文件不属于本项目 MIT 许可范围，详见 [`../THIRD-PARTY-NOTICES.md`](../THIRD-PARTY-NOTICES.md)。

| 本地文件 | 下载地址 | 用途 |
| --- | --- | --- |
| `windows/kbdgre2-tables.xml` | https://kbdlayout.info/KBDGRE2/download/kbdtables | 低层 KBDTABLES，包括死键和状态表；交叉核验依据 |
| `windows/kbdgre2.xml` | https://kbdlayout.info/KBDGRE2/download/xml | 易处理的按键/修饰键/嵌套死键组合，适合移植参考 |
| `windows/kbdgre2.klc` | https://kbdlayout.info/KBDGRE2/download/klc | 网站生成的 KLC 文本；原始编码为 UTF-16，不保证可无损重新编译 |

下载链接会随网站数据更新；以本地文件、文件头版本和 `SHA256SUMS` 固定本次快照。

`kbdgre2.xml` 中 `With="VK_CONTROL VK_MENU"` 对应 AltGr。
F 键对应的 `DeadKeyTable` 名称为 `EXTRA-WAHLTASTE`，包含红色扩展层。
其他死键表还包含重音、多级选择等组合。移植时应理解嵌套表的状态转换，
不能把内部用作中间状态的 Accent 字符直接当作用户应输入的字符。

## 已核验的交叉结果

- 两套参考都将 W / T / I 的 AltGr 功能定义为 macron / caron / tilde。
- E2 的 AltGr+2 / AltGr+3 为 `<` / `>`。
- Linux 用 `ISO_Level5_Latch`，Windows 用 `EXTRA-WAHLTASTE` 死键实现扩展选择。
- Windows 扩展表：t→þ、T→Þ、2→½、c→¢、C→©、ö→œ、ä→æ。
- 两个 XML 文件均成功解析；KLC 已按 UTF-16 解码并核对驱动名和版本。

建议后续以 Linux 文件核对物理键位与各层字符，以 Windows 内部表和处理版 XML
核对特殊选择及多级死键行为，再逐项对照用户提供的布局图。
实现文件只是参考，不等同于 DIN 标准全文，也未在 Linux/Windows 实机运行验证。

## 新增：Windows E1 独立参考

制作 ISO 备用版本时另行下载，不能直接假定 E1 的死键表与 E2 完全相同：

- 页面：https://kbdlayout.info/KBDGRE1/
- `windows/kbdgre1-tables.xml`：https://kbdlayout.info/KBDGRE1/download/kbdtables
- `windows/kbdgre1.xml`：https://kbdlayout.info/KBDGRE1/download/xml

两者同样是第三方对微软驱动的解析导出，不是开放源码。XML 已成功解析并加入 `SHA256SUMS`。
E1 本次快照含 **1,508** 条死键转换；E2 含 **1,509** 条。
Linux E1 在已有 `symbols/de` 的 `e1` 区块，无需额外下载。
