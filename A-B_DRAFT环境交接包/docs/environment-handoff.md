# DRAFT–BuildChecker 环境交接说明

本材料依据《接口定义文档 v0.2》，不替代原接口文档。

本文只说明 DRAFT 环境交接给 BuildChecker 时需要使用的既有接口内容。它不重新定义 Job、Artifact、错误码、端点或字段语义。如有冲突，以《接口定义文档 v0.2》为准。

## 1. 交接范围

DRAFT 是完整流程中的环境生成任务。流程发起方先创建 DRAFT Job，查询到成功结果后，再把其中的 Dockerfile `ArtifactRef` 和镜像引用组成 `EnvironmentRef`，用于创建 FULL_CHECK Job。

本次真实仓库、命令、运行平台、镜像和 Artifact 访问方式见 [`instance-values.md`](instance-values.md)；尚未确定的项目均为“待确认”。

对应原文：§1.3、§5.3、§6、§7.1。

## 2. DRAFT 创建请求

- 使用 `POST /v1/dockerfile-jobs`。
- `schema_version` 为 `2.0`。
- `job_type` 为 `DRAFT`，并且必须与端点一致。
- 创建请求必须携带 `Idempotency-Key`。
- `trace_id` 由流程发起方提供，并在同一次完整流程中保持不变。
- `input.repository` 使用 `url`、完整 `commit` 和 `project_root`。
- DRAFT 的 `input.build` 使用 `build_command` 和 `test_command`。
- DRAFT 的 `input.build` 不出现 `configuration_id` 和 `clean_command`。
- `input.limits` 使用 `max_iterations` 和 `timeout_seconds`。

对应原文：§1.1、§1.2、§5.1、§5.2、§6.1。

## 3. 创建回执与 Job 查询

- 创建请求成功受理时返回 `202 Accepted` 和 `CreateReceipt`。
- 创建回执的 `status` 必须是 `QUEUED`，并且不包含 `input`、`output` 或 `error`。
- 后续使用 `GET /v1/jobs/{job_id}` 查询完整 Job。
- 查询结果中的 `input` 原样保留创建请求内容。
- `QUEUED` 或 `RUNNING` 时，`output` 和 `error` 都为 `null`。
- `SUCCEEDED` 时，`output` 为对象，`error` 为 `null`。
- `FAILED`、`TIMED_OUT` 或 `CANCELLED` 时，`output` 为 `null`，`error` 为对象。
- `execution` 时间使用 UTC、RFC 3339，并以 `Z` 结尾；尚未发生的时间为 `null`。

对应原文：§2、§3。

## 4. DRAFT 成功与失败

DRAFT 只有在以下条件全部满足时才能为 `SUCCEEDED`：

- 已产出 Dockerfile；
- 已产出镜像；
- `build_result.exit_code` 为 `0`；
- `test_result.exit_code` 为 `0`。

失败和超时沿用原错误模型：

| 条件 | 状态 | 错误码 | 输出要求 |
| --- | --- | --- | --- |
| 镜像构建失败 | `FAILED` | `ENV_3002` | `output` 为 `null`，不得交付 `image` |
| 达到 `max_iterations` 仍未通过测试 | `FAILED` | `DRAFT_3001` | `output` 为 `null`，不得交付 `image` |
| 超过时间限制 | `TIMED_OUT` | `EXEC_4002` | `output` 为 `null` |

对应原文：§2.4、§6.2、§11.1。

## 5. 成功输出与 EnvironmentRef

DRAFT 成功输出包含：

- `dockerfile`
- `image`
- `iteration_logs`
- `build_result`
- `test_result`

FULL_CHECK 的 `environment` 使用 §5.3 定义的 `EnvironmentRef`：

- `environment.dockerfile` 使用 DRAFT 成功输出中的完整 `dockerfile` ArtifactRef；
- `environment.image_ref` 等于 DRAFT 成功输出中的 `image.uri`；
- 不使用单独的 `dockerfile_uri`；
- `dockerfile.producer_job_id` 必须与产出对应镜像的 DRAFT 相同。

对应原文：§5.3、§6.2、§7.1。

## 6. Dockerfile 与镜像

Dockerfile ArtifactRef 使用既有字段：

- `artifact_id`
- `type: "DOCKERFILE"`
- `uri`
- `media_type`
- `producer_job_id`
- `commit`
- `sha256`

镜像使用 `CONTAINER_IMAGE` ArtifactRef。其 `uri` 也是下游使用的 `image_ref`，格式为：

```text
{name}@sha256:{digest}
```

`CONTAINER_IMAGE.sha256` 必须等于 `uri` 中 `@sha256:` 后面的 digest。Dockerfile 和镜像均未变化时，后续检测可以继续使用同一次 DRAFT 的 `EnvironmentRef`。Makefile 补丁不会自动改变 `image_ref`。

对应原文：§4.1、§4.2、§5.3、§6.2。

## 7. Artifact URI 与共享路径

文件产物 URI 固定为：

```text
artifact://{pair_id}/{job_id}/{file_name}
```

联调时映射到仓库内共享路径：

```text
artifacts/{pair_id}/{job_id}/{file_name}
```

必须满足：

- `pair_id` 匹配 `[a-z0-9]+(-[a-z0-9]+)*`；
- URI 中的 `job_id` 等于 `producer_job_id`；
- `file_name` 只含字母、数字、点、下划线和短横线，不含路径分隔符；
- 下游能够读取映射后的文件；
- 不使用本机绝对路径进行交接。

对应原文：§4.3。

## 8. FULL_CHECK 引用方式

FULL_CHECK 使用 `POST /v1/full-check-jobs`。请求中：

- `input.repository` 指定当前待检测源码；
- `input.environment` 使用 DRAFT 输出形成的 `EnvironmentRef`；
- `input.build` 使用 `configuration_id`、`clean_command` 和 `build_command`；
- FULL_CHECK 的 `input.build` 不出现 `test_command`。

`configuration_id` 是 FULL_CHECK 的必填字段，不应增加到 DRAFT 请求中。

对应原文：§5.2、§5.3、§7.1。

## 9. 交接一致性检查

- 所有跨组传递的 ArtifactRef 都带 `sha256`。
- 依赖源码的产物带完整 `commit`。
- 依赖构建配置的产物带 `configuration_id`。
- 文件产物的实际字节与其 `sha256` 一致。
- `CONTAINER_IMAGE.sha256` 与镜像 URI 中的 digest 一致。
- Dockerfile URI 中的 `job_id` 与 `producer_job_id` 一致。
- Dockerfile 与对应镜像来自同一个 DRAFT Job。
- FULL_CHECK 的 `environment.image_ref` 与 DRAFT 的 `image.uri` 完全一致。
- 下游读取 Artifact 时核对 `sha256`、适用的 `commit` 和 `configuration_id`。

对应原文：§4.1、§4.3、§5.3、§13 T09。

## 10. 当前证据状态

本目录中的 JSON 均为结构样例。目前没有随本包交付真实 Dockerfile、镜像、构建日志、测试日志、Artifact 文件或联调结果。上述真实内容的状态均为“待确认”。

