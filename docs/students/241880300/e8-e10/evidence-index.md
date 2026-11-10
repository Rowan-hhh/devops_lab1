# E8—E10 证据索引

实验运行时外层源码 SHA：`c2621b9e7f9d0ba2d0b8ae38112fb4509c0194c2`

所有 `work/` 证据均在本地 worktree 中保留，并由仓库 `.gitignore` 忽略，便于按手册另行归档，不把二进制、缓存和临时样例 Git 历史混入源码提交。

|阶段|OUT|关键证据|
|---|---|---|
|E8 B|`work/e8-B-20261110-241880300`|`fixed-md-report.json`、`candidate.patch`、`patch-plan.json`、`expected-failure.json`、`project/`、`student-source-commit.txt`|
|E9 B|`work/e9-B-20261110-241880300`|`direct-plan.json`/`patch`、`macro-plan.json`/`patch`、`mixed-plan.json`/`patch`、三份独立样例项目、`student-source-commit.txt`|
|E10 B|`work/e10-B-20261110-241880300`|`candidate.patch`、`reject-test/`、`accept/`、`broken.patch`、`reject-patch/`、`recheck-buildchecker/`、`results.csv`、`gate.json`、`personal-unit-tests.log`、`source-before.Makefile`、`student-source-commit.txt`|

## 关键结果

- E8 `fixed-md-report.json`：commit 与样例 HEAD 匹配，发现集合为一项 `MISSING` 和一项 `REDUNDANT`；`expected-failure.json` 为 `STALE_REPORT`。
- E9 三份 plan 分别为 direct/macro/mixed，三种 Patch 均生成于独立样例目录。
- E10 `results.csv`：`test-rejection=True`、`accepted=True`、`patch-rejection=True`；`gate.json` 为 `{"track":"B","passed":true,"rows":3}`。
- E10 `recheck-buildchecker/findings.json`：状态 `SUCCEEDED`，仅保留 `REDUNDANT main.o/unused.h`，无 `MISSING`。

## 远程状态

当前工作区没有 Docker/gh；正确学号分支推送后需补录 Actions URL、远程 headSha、artifact 和 PR 状态。
