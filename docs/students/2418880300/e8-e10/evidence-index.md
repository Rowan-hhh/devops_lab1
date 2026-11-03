# E8—E10 证据索引

实验运行时外层源码 SHA：`7d2c8414d4c40b63f94ae5b74929315d45df80ce`

所有 `work/` 证据均在本地 worktree 中保留，并由仓库 `.gitignore` 忽略，便于按手册另行归档，不把二进制、缓存和临时样例 Git 历史混入源码提交。

|阶段|OUT|关键证据|
|---|---|---|
|E8 B|`work/e8-B-20261104`|`fixed-md-report.json`、`candidate.patch`、`patch-plan.json`、`expected-failure.json`、`manual-checks.json`、`project/`、`结论.txt`、`*-command.txt`、`*-run.log`|
|E9 B|`work/e9-B-20261104`|`direct-input.json`/`patch`/`plan`、`macro-input.json`/`patch`/`plan`、`mixed-input.json`/`patch`/`plan`、`apply-demo/`、`manual-checks.json`、`结论.txt`、`*-command.txt`、`*-run.log`|
|E10 B|`work/e10-B-20261104`|`fixed-md-report.json`、`candidate.patch`、`source-before.Makefile`、`reject-test/`、`accept/`、`broken.patch`、`reject-patch/`、`recheck-buildchecker/`、`results.csv`、`gate.json`、`*-command.txt`、`*-run.log`|

## 关键结果

- E8 `manual-checks.json`：commit 匹配、发现集合、Patch 可应用、旧报告拒绝、源字节保持均为 true。
- E9 `manual-checks.json`：direct/macro/mixed 三种 style、源项目干净、macro 副本应用均为 true。
- E10 `results.csv`：`test-rejection=True`、`accepted=True`、`patch-rejection=True`；`gate.json` 为 `{"track":"B","passed":true,"rows":3}`。
- E10 `recheck-buildchecker/findings.json`：状态 `SUCCEEDED`，仅保留 `REDUNDANT main.o/unused.h`，无 `MISSING`。

## 远程状态

当前工作区没有 Docker/gh，未生成 Actions URL、远程 headSha、artifact 或 PR；这些不是本地证据的替代品，需在分支推送后补录。
