# MD 接收记录

> 本文件是模板。复制后填写一次实际交接；模板中的 `<待填写>` 不能直接作为交付记录。

## 交接元数据

| 字段 | 实际值 |
| --- | --- |
| pair_id | `<待填写>` |
| 接收方 | `B2 / MDFixer` |
| 交付方 | `A 组检测负责人 / <姓名>` |
| 接收时间 | `<待填写，YYYY-MM-DDThh:mm:ss+08:00>` |
| producer_job_id | `<待填写>` |
| report_type | `ERROR_REPORT` |
| configuration_id | `<待填写或 N/A>` |
| repository.url | `<待填写>` |
| repository.commit | `<待填写，完整 commit>` |

## 报告 Artifact

| 字段 | 实际值 |
| --- | --- |
| artifact URI | `artifact://<pair_id>/<job_id>/<file_name>` |
| 共享目录相对路径 | `artifacts/<pair_id>/<job_id>/<file_name>` |
| sha256 | `<待填写，完整 64 位十六进制值>` |
| 文件是否可读 | `PASS / FAIL` |
| sha256 是否匹配 | `PASS / FAIL` |
| Artifact job 与 producer_job_id 是否一致 | `PASS / FAIL` |

## Finding 清单

| finding_id | type | location | evidence 摘要 | finding commit | 处理结论 |
| --- | --- | --- | --- | --- | --- |
| `<待填写>` | `MISSING / REDUNDANT / 其他` | `<repo-relative-file>:<line>:<column>` | `<待填写>` | `<待填写>` | `修复候选 / 仅记录 / 拒收` |

## 接收校验

- [ ] 报告包含 `schema_version`、`report_type`、`producer_job_id`、`findings`
- [ ] ArtifactRef 的 `uri`、相对路径、`sha256`、`job_id` 齐全
- [ ] 报告文件 SHA-256 与交接值一致
- [ ] repository commit、finding commit 与目标代码 commit 一致
- [ ] 所有 location 都是仓库相对路径，行号/列号合法
- [ ] 每个 finding 都有可复核的 evidence
- [ ] 配置相关信息与 `configuration_id` 一致，或明确为 `N/A`
- [ ] 只将 `MISSING` finding 列入后续 MDFixer 修复候选

## 最终结论

- 接收状态：`PENDING / ACCEPTED / REJECTED`
- 若拒收，原因和补交要求：`<待填写>`
- 若接受，允许进入修复的 finding_id：`<待填写或 N/A>`
- B2 接收人：`<待填写>`
- 备注：`接收通过仅表示报告可消费，不表示修复或重新验证已完成。`

