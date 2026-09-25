# A 组 E2 完成情况

## 范围

E2 交付接口契约、机器可读 Schema、结构样例和设计记录。E2 不部署 API，不实现 BuildChecker 或 EChecker，也不声称真实项目已经构建或检测。

## A 组交付状态

| 内容 | 状态 | 产物或说明 |
|------|------|------------|
| FULL_CHECK 创建请求、202 回执和查询结果 | DONE | `examples/full-check-create-request.example.json`、`examples/full-check-create-receipt.example.json`、`examples/full-check-job-succeeded.example.json` |
| FULL_CHECK 执行失败样例 | DONE | `examples/full-check-job-failed.example.json` 使用 `ANALYSIS_5001`，`output` 为 `null` |
| MISSING 与 REDUNDANT 发现 | DONE | `examples/error-report.example.json` 包含位置和 evidence；固定预期发现使用 `INSTRUCTOR_ORACLE` |
| INCREMENTAL_CHECK 请求、202 回执和查询结果 | DONE | `examples/incremental-check-create-request.example.json`、`examples/incremental-check-create-receipt.example.json`、`examples/incremental-check-job-succeeded.example.json` |
| 产物交接规则 | IN_PROGRESS | `ADR-002-artifact-storage-and-access.md` 已记录 A 组方案，等待配对 B 组确认 |
| 双方共享目录和访问权限 | BLOCKED | 共享位置、读写权限及同步方式尚未由配对双方确认 |
| 三轮配对练习记录 | BLOCKED | 当前仓库没有双方确认的三轮记录 |
| 配对组实例值 | BLOCKED | `pair03` 和其他实例字段仍为占位值 |

## 校验结果

- 根目录 `ab-job-contract.schema.json` 通过 JSON Schema Draft 2020-12 Schema 自检。
- 使用 `jsonschema` 4.26.0 和 Draft 2020-12 校验器核对 A 组 9 个 JSON 样例：8 个有效样例通过对应 `$defs`，`invalid-request-wrong-job-type.example.json` 按预期被拒绝。校验器安装在临时目录，没有加入仓库依赖。
- 删除 INCREMENTAL_CHECK 请求的 `baseline` 后，Schema 按预期拒绝该请求。
- INCREMENTAL_CHECK 样例满足 `baseline.commit == base_commit` 且 `repository.commit != base_commit`。
- FULL_CHECK 成功 Job、ERROR_REPORT 和 ArtifactRef 的 producer Job、commit、configuration ID、URI 及 MD/RD 计数相互一致。
- 两个 A 服务创建回执与对应查询 Job 的 `job_id`、`trace_id`、`job_type` 和 `created_at` 一致。
- 基线 commit 不匹配属于接收方跨字段检查，不由当前 Schema 自动比较。当前请求样例的匹配关系已静态核对；API 尚未实现，因此未执行 HTTP 422 运行测试。
- 示例 SHA-256、仓库、commit 和镜像 digest 均为占位值。仓库没有对应的真实 Artifact 字节，未执行真实字节摘要校验。
- `git diff --check` 在各次本地提交前通过。

## 下一步

1. 与同号 B 组确认真实配对编号和 `pair_id`，并确认 ADR-002 的 Artifact 访问方案。
2. 确认共享仓库或目录、读写权限、文件同步方式和保留约定，再更新 `docs/instance-values.md`。
3. 完成并记录三轮配对练习及双方对失败输入和交接样例的确认。
4. 收到 E3 项目资料后，再登记真实仓库、commit、构建命令和 Artifact 实例值，并按 E3 要求准备测试基线。
5. 本轮 Git 提交保留在本地仓库；未执行 push。

本地提交者、提交 SHA 和提交说明以仓库 Git 历史为准。当前文档记录的是 A 组状态，不代表配对 B 组已验收。
