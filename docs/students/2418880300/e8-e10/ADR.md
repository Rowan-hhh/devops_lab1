# 决策记录

## 背景与约束

B4 要复核候选 Patch，但旧报告、坏 Patch、编译失败或测试失败都不能污染原始源码。E8—E10 手册要求保留候选、验证日志、拒绝原因和源文件保持证据。

## 选择与替代方案

选择“commit 身份检查 + sandbox 验证 + 成功后写回”的流程：`patch()` 先拒绝 `STALE_REPORT`，`validate()` 将候选复制到独立 sandbox，依次检查补丁、构建、测试、头文件变化和重检，全部通过后才写回源 `Makefile`。

替代方案是直接在源目录应用 Patch、失败后恢复。该方案恢复路径容易遗漏生成文件或字节差异，不适合 B4 的复核职责，因此不采用。

## 代价与覆盖范围

教学实现支持 direct/macro/mixed 三种受限声明风格，变量共享范围和复杂 Make 语法仍需扩展分析。验证使用 WSL2 本地 Linux 完成；本机 Docker/gh 不可用，Docker workflow 和远程 Actions 仍是待补的标准环境证据。

## 验证命令与实际证据

- `python3 -m unittest test_profile.StudentE10B -v`：1/1 OK。
- `python3 -m unittest discover -s . -p test_profile.py -v`：8/8 OK。
- E8 `manual-checks.json`：5/5 true。
- E9 `manual-checks.json`：7/7 true。
- E10 `gate.json`：`passed=true`、`rows=3`；BuildChecker 重检状态为 `SUCCEEDED`，无 `MISSING`。
