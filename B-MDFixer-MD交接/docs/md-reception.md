# MD 交接接收规范（B2）

## 1. 角色和输入

| 项目 | 约定 |
| --- | --- |
| 接收方 | B2 / MDFixer |
| 交付方 | A 组检测负责人 |
| 输入 | `FULL_CHECK` 产出的 MD/RD `ERROR_REPORT` ArtifactRef |
| 交接信息 | MD report、location、evidence、commit |
| 接收记录 | [md-receipt.example.md](../examples/md-receipt.example.md) 的一份实际填写副本 |

报告的字段和 finding 结构以仓库现有的 [ERROR_REPORT 示例](../../A-BuildChecker-EChecker-接口文档/examples/error-report.example.json) 为准，不在本目录重新定义一套接口。

## 2. 接收步骤

### 2.1 定位报告

1. 从 A 组交付的 `error_report` ArtifactRef 读取 `uri`、`sha256`、`job_id`、`producer`、`commit` 和 `configuration_id`。
2. 按契约将 `artifact://{pair_id}/{job_id}/{file_name}` 映射到共享目录中的 `artifacts/{pair_id}/{job_id}/{file_name}`。
3. `file_name` 只能是文件名，不能包含目录分隔符；不得使用绝对路径。

### 2.2 校验交接完整性

以下任意一项失败，接收状态为 `REJECTED`，记录具体原因，不进入修复：

- 报告文件存在且可读；
- 对报告文件原始字节计算出的 SHA-256 与 ArtifactRef 的 `sha256` 完全一致；
- ArtifactRef 的 `job_id` 与报告中的 `producer_job_id` 对得上；
- 报告中的 `repository.commit`、每个 finding 的 `commit` 与交接声明的目标 commit 一致；
- 报告包含 `schema_version`、`report_type=ERROR_REPORT`、`findings`；
- 每个 finding 都包含 `finding_id`、`type`、`target`、`dependency`、`location`、`evidence` 和 `detector`；
- `location.file` 为仓库相对路径，`line` 为正整数；若提供 `column`，也必须为正整数；
- `evidence` 至少能够说明摘要、触发过程、观测到的文件和声明文件；
- 若本次检查依赖配置，`configuration_id` 存在且与交接声明一致。

### 2.3 校验 finding 是否可交给 MDFixer

- `type=MISSING`：可以进入后续修复候选列表；
- `type=REDUNDANT`：在接收记录中保留证据，但不由本次 B2 修复流程自动处理；
- 未知类型：拒收，要求 A 组补充契约或重新生成报告；
- 发现 commit 与当前待修复代码不是同一 commit：拒收，要求重新跑检测或重新交接。

接收通过并不等于修复成功。接收阶段只冻结“B2 将基于哪个报告、哪个 commit、哪个证据开展后续工作”。

## 3. 接受/拒收规则

### ACCEPTED

所有完整性校验通过，报告与目标 commit、配置和 ArtifactRef 一致，且至少有一个可处理的 `MISSING` finding，或者报告虽无 `MISSING` 但内容完整、可追溯。B2 可以继续按接口契约发起 `REPAIR`。

### REJECTED

存在缺文件、sha256 不匹配、commit 不一致、路径非法、location/evidence 不完整、报告格式错误或未知 finding 类型。B2 不修改代码，并在接收记录中写明补交内容。

## 4. 接收记录要求

实际交接时复制模板并填写真实值，至少保留：

- A 组报告 Artifact URI、报告相对路径和 sha256；
- `producer_job_id`、目标 repository URL、目标 commit、`configuration_id`；
- 每个 finding 的 `finding_id`、类型、location 和 evidence 摘要；
- 各项校验结果及失败原因（如有）；
- 最终 `ACCEPTED` 或 `REJECTED`、接收人和时间；
- 若接受，列出允许进入修复的 `MISSING` finding；若拒收，列出要求 A 组重新交付的内容。

模板中的 `<待填写>` 不是有效交接值，提交前必须全部替换或明确填写 `N/A`。

