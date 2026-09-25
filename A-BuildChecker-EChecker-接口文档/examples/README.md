# A 组 JSON 样例

本目录中的 JSON 展示《接口定义文档 v0.2》的请求、创建回执、查询结果、拒绝输入和 Artifact 引用结构。它们不表示 A 组服务已经部署或运行。

## 占位值与发现来源

- `pair03`、仓库 URL、commit、Job 编号、时间、命令和摘要值均为结构占位值。
- `error-report.example.json` 是固定预期发现样例。MISSING 和 REDUNDANT 均使用 `INSTRUCTOR_ORACLE`，不表示检测器实际产出了该报告。
- `full-check-job-succeeded.example.json` 的计数与该报告中的 Finding 数量对应。报告 ArtifactRef 与 Job 的 `producer_job_id`、commit 和 `configuration_id` 一致。
- 同一任务的创建回执和成功查询结果使用相同的 `job_id` 与 `trace_id`。回执只包含创建回执允许的公共字段，不包含 `input`、`output` 或 `error`。
- 示例 `sha256` 和镜像 digest 不对应真实文件或镜像字节，不能用于实际完整性核验。

## 文件对应关系

- `full-check-create-request.example.json`、`full-check-create-receipt.example.json` 和 `full-check-job-succeeded.example.json` 展示 FULL_CHECK 生命周期。
- `full-check-job-failed.example.json` 展示分析器执行失败。
- `error-report.example.json` 展示一条 MISSING 和一条 REDUNDANT Finding。
- `incremental-check-create-request.example.json`、`incremental-check-create-receipt.example.json` 和 `incremental-check-job-succeeded.example.json` 展示 INCREMENTAL_CHECK 生命周期。
- `invalid-request-wrong-job-type.example.json` 展示端点任务类型不匹配的拒绝输入。

样例对照的 Schema 定义位于仓库根目录 `ab-job-contract.schema.json`。跨字段关系和 Artifact 字节校验还需按契约执行接收方检查。
