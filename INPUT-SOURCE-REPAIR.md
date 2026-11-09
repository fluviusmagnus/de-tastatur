# 旧“德语－标准”无法停用：诊断与定点修复

日期：2026-11-09，macOS 27.2 (26B123)。

> **范围说明：** 本文记录项目作者本机的输入源迁移过程，供复现与排障参考。
> 文中 `.backups/` 路径属于本机备份，已被 `.gitignore` 排除，不随仓库发布。
> 不要直接照搬删除输入源；执行前请先备份并确认自己的启用列表。

## 已验证事实

- E2 当前可用，`IsASCIICapable=true`，且为当前键盘布局；日常当前输入法是鼠须管。
- E1/E2 无重复登记，声明的输入源 ID 与系统实际 ID 一致。
- **第三方输入源有单独的持久设置域**：`com.apple.inputsources/AppleEnabledThirdPartyInputSources`。
  E2、鼠须管均正确保存在这里。只看 `com.apple.HIToolbox` 会误判 E2 未保存。
- 系统内置输入源保存在 `com.apple.HIToolbox/AppleEnabledInputSources`。
- 直接调用 `TISDisableInputSource` 停用旧德语返回 0，但重新枚举后它仍启用。
- 临时添加 ABC 后，旧德语可停用；此时停用 ABC 又返回 0 但无效。
- 经用户许可短暂选中 E2 后重试，仍无法停用最后的 ABC。
- 两次事务均回滚：旧德语启用、ABC 不启用、E2 启用，鼠须管恢复。

这些实验确认了本机会保留最后一个内置 ASCII 布局的**外部行为**，并不能证明其内部实现原因。
不需要更改已通过验证的 E2 键位、关闭 SIP 或删除内置布局文件。

## 用户授权的定点修改

用户明确允许：备份后，只移除当前用户保存的旧德语启用记录；保留全部第三方输入源和其他输入法。
不自动注销，不重启，不清理缓存，不修改系统文件。

新增工具：

1. `python3 tools/plan_input_source_retirement.py`：备份两个偏好域，生成 `.backups/retire-standard-*/plan.json`，不修改设置。
2. `swift tools/apply_input_source_plan.swift <plan.json> --check`：检查当前状态和计划范围，不修改设置。
3. 同一命令改用 `--apply`：通过 CFPreferences 只写入 `AppleEnabledInputSources` 这一个键。
4. 同一命令改用 `--restore`：只有设置仍与计划应用后的状态一致时才允许恢复，避免覆盖后续用户修改。

计划只能删除 `German-DIN-2137` / 数字 ID `-18133` 的一个内置键盘记录。
应用前要求 E2 持久启用、运行时启用且支持 ASCII，并作为当前键盘布局；应用时不切换当前输入法。
第三方列表使用整份快照校验，但**从不写入**该域。

## 本次执行结果

实际备份与计划：`.backups/retire-standard-20261109-012208/`。
`--check`、`--apply` 均通过，随后完成独立进程和磁盘读回：

- HIToolbox 全部键与备份对比，只有 `AppleEnabledInputSources` 改变，恰好删除一条旧德语记录。
- `com.apple.inputsources.plist` 与备份字节完全相同，E2 与鼠须管的持久启用设置未变。
- 新进程运行时枚举：旧德语未启用、ABC 未启用、E2 启用、E1 未启用。
- 当前输入法仍是 `im.rime.inputmethod.Squirrel.Hans`，当前键盘布局仍是 E2。
- 未清缓存、未修改系统文件、未自动注销；**注销重登录后的效果仍待用户验收**。

如需恢复本次移除的记录，在项目目录运行：

```sh
swift tools/apply_input_source_plan.swift .backups/retire-standard-20261109-012208/plan.json --restore
```

该命令要求内置启用列表及第三方列表仍与计划对应状态一致；若用户后续调整输入源，工具会拒绝覆盖。
不要直接复制完整备份覆盖现有偏好文件。

## 验收边界

写入成功不等于当前登录会话已修复。必须独立检查磁盘及新进程读回结果，再由用户注销重新登录验证：

- 输入源菜单不再出现“德语－标准”或临时 ABC；
- E2 与鼠须管仍正常，E1 仍可在德语分类添加；
- 偏好设置中的旧记录没有被恢复。

如果设置被立即恢复，停止继续自动修复并报告；不反复覆盖用户偏好或清理缓存。
如果注销后系统仍恢复旧项，应按平台限制／缺陷继续处理，不能声称已解决。
