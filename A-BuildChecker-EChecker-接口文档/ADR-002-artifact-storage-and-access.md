# ADR-002: 统一 Artifact URI 与共享目录读取方式

## 状态

PROPOSED（A 组方案，待配对 B 组确认共享位置和读取权限）

## 背景

BuildChecker 和 EChecker 接收 DRAFT 环境及基线图，也向 MDFixer 交付依赖图和 ERROR_REPORT。Job JSON 只传递 Artifact 元数据，大文件通过 URI 引用。接收方需要按双方可理解的规则定位文件并校验内容。

《接口定义文档 v0.2》§4.3 已定义逻辑 URI 和仓库内相对路径映射。实际共享仓库、目录权限、同步方式和文件保留策略仍未确认。

## 决策

A 组采用以下契约级访问规则，并提交配对 B 组确认：

1. 文件 Artifact URI 使用 `artifact://{pair_id}/{job_id}/{file_name}`。
2. 联调仓库中的相对文件路径使用 `artifacts/{pair_id}/{job_id}/{file_name}`。接收方将 URI 的三段路径映射为该相对路径，并从双方约定的共享仓库副本读取文件。
3. `pair_id`、`job_id` 和 `file_name` 必须符合 v0.2 约束。`file_name` 不包含目录分隔符，路径解析不得越出 `artifacts/` 根目录。
4. 接收方读取文件字节后计算 SHA-256，并与 ArtifactRef 的 `sha256` 比较；同时核对 URI 中的 `job_id` 与 `producer_job_id`，并核对适用的 `commit` 和 `configuration_id`。
5. 跨组交接使用逻辑 URI 和仓库内相对路径，不使用某台机器的绝对路径。
6. 实际共享仓库或目录、读写权限、同步时机及保留期限由配对双方确认后记录在 `docs/instance-values.md`。这些运行实例值不改变逻辑 URI 格式。

## 替代方案

| 方案 | 优点 | 后果 |
|------|------|------|
| 在 Job JSON 中内嵌图、日志或报告 | 消费端不需要额外查找文件 | 大文件扩大 HTTP 请求和响应，违背 v0.2 的 Artifact 引用约定 |
| 在 ArtifactRef 中放置本机绝对路径 | 本机读取直接 | 跨机器不可移植，不能作为组间接口 |
| 使用双方确认的共享仓库相对路径映射 | 与 v0.2 URI 规则一致，可按摘要核对文件 | 双方仍需确认共享位置、权限和同步方式 |

## 后果

- 生产方需要将文件放入双方确认的共享位置，并提供准确的 ArtifactRef 元数据。
- 消费方需要解析 URI、读取实际字节、核对 SHA-256 及适用的版本元数据。
- 固定重复字符组成的示例摘要不能作为真实文件完整性证明。
- 在 B 组确认共享位置和权限前，本 ADR 仍为提案，不能声称已完成真实跨组读取验证。

## 关联

- 契约：`接口定义文档_v0.2.md` §4.1、§4.3、§13 T09
- A 组交接规则：`docs/environment-handoff.md`
- 运行实例值：`docs/instance-values.md`
- 异步任务决策：`ADR-001-async-job.md`
