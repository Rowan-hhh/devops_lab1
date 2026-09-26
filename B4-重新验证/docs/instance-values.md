# B4 实例值清单

本文件是 B4 真实联调前的填写清单。当前所有值都是“待确认”，不能作为运行证据。双方确认后替换占位内容，并保留确认人和时间。

| 项目 | 实际值 | 确认人/时间 |
| --- | --- | --- |
| `pair_id` | 待确认 | 待确认 |
| REPAIR `job_id` | 待确认 | 待确认 |
| 验证记录 `job_id` | 待确认 | 待确认 |
| repository URL | 待确认 | 待确认 |
| `base_commit` | 待确认 | 待确认 |
| `candidate_commit` | 待确认 | 待确认 |
| `configuration_id` | 待确认 | 待确认 |
| DRAFT `image_ref` | 待确认 | 待确认 |
| Dockerfile Artifact URI | 待确认 | 待确认 |
| 候选 workspace 相对位置 | 待确认 | 待确认 |
| clean command | 待确认 | 待确认 |
| build command | 待确认 | 待确认 |
| test command | 待确认 | 待确认 |
| recheck command | 待确认 | 待确认 |
| recheck report 相对路径 | 待确认 | 待确认 |
| selected `finding_ids` | 待确认 | 待确认 |
| 构建日志 Artifact URI / SHA-256 | 待确认 | 待确认 |
| 测试日志 Artifact URI / SHA-256 | 待确认 | 待确认 |
| 重检报告 Artifact URI / SHA-256 | 待确认 | 待确认 |
| B4 验证报告 Artifact URI / SHA-256 | 待确认 | 待确认 |
| B4 操作人 | 待确认 | 待确认 |
| B2 最终确认人 | 待确认 | 待确认 |
| 最终接受/拒绝决定 | 待确认 | 待确认 |

## 填写规则

- commit 必须是完整 SHA；不能只填写短 SHA。
- 文件产物使用 `artifact://` URI 和仓库共享目录相对映射，不填写本机绝对路径。
- 每个跨组 Artifact 都记录原始字节 SHA-256，并核对其 `commit`、`configuration_id` 和 `producer_job_id`。
- 在 B4+B2 共同确认前，不把 `ACCEPTED` 当作最终 Patch 接受决定。
