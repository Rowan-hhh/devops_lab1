# A 组环境消费接口契约

本材料定义 A 组消费 B 组 DRAFT 环境的方式，以及 A 组向 B 组 MDFixer 交付 MD/RD 报告的方式。

严格依据《接口定义文档 v0.2》§7（FULL_CHECK 接口）和 §8（INCREMENTAL_CHECK 接口）。

## 1. 环境消费：BuildChecker 接收 DRAFT 输出

### 1.1 EnvironmentRef 结构

BuildChecker 的 `input.environment` 使用 DRAFT 成功输出的 `EnvironmentRef`：

```json
{
  "dockerfile": {
    "artifact_id": "dockerfile-001",
    "type": "DOCKERFILE",
    "uri": "artifact://pair03/job-draft-001/Dockerfile",
    "media_type": "text/plain",
    "producer_job_id": "job-draft-001",
    "commit": "0123456789abcdef0123456789abcdef01234567",
    "sha256": "1111111111111111111111111111111111111111111111111111111111111111"
  },
  "image_ref": "pair03/demo-project@sha256:2222222222222222222222222222222222222222222222222222222222222222"
}
```

### 1.2 一致性检查

接收 DRAFT 输出时，BuildChecker 必须验证（§5.3）：

| 检查项 | 规则 |
|--------|------|
| Dockerfile 与镜像同源 | `dockerfile.producer_job_id` == `image.producer_job_id` |
| 镜像 URI 一致 | `input.environment.image_ref` == `output.image.uri` |
| commit 一致 | Dockerfile 和镜像的 `commit` 相同 |
| sha256 可验证 | `sha256` 与 Artifact 实际字节匹配 |
| 来自同一 DRAFT | Dockerfile 和镜像的 `producer_job_id` 相同 |

### 1.3 Artifact URI 解析（§4.3）

- 格式：`artifact://{pair_id}/{job_id}/{file_name}`
- 本地映射：`artifacts/{pair_id}/{job_id}/{file_name}`
- 解析流程：提取 `pair_id` + `job_id` + `file_name` → 拼接本地路径 → 下载并验证 sha256

## 2. MD/RD 报告：BuildChecker 输出给 MDFixer

### 2.1 输出结构（§7.2）

BuildChecker 成功时，`output` 包含：

```json
{
  "actual_graph": {
    "artifact_id": "actual-graph-001",
    "type": "ACTUAL_GRAPH",
    "uri": "artifact://pair03/job-full-001/actual.json",
    "media_type": "application/json",
    "producer_job_id": "job-full-001",
    "commit": "0123456789abcdef0123456789abcdef01234567",
    "configuration_id": "cc-MODE0",
    "sha256": "4444444444444444444444444444444444444444444444444444444444444444"
  },
  "declared_graph": {
    "artifact_id": "declared-graph-001",
    "type": "DECLARED_GRAPH",
    "uri": "artifact://pair03/job-full-001/declared.json",
    "media_type": "application/json",
    "producer_job_id": "job-full-001",
    "commit": "0123456789abcdef0123456789abcdef01234567",
    "configuration_id": "cc-MODE0",
    "sha256": "5555555555555555555555555555555555555555555555555555555555555555"
  },
  "error_report": {
    "artifact_id": "error-report-001",
    "type": "ERROR_REPORT",
    "uri": "artifact://pair03/job-full-001/error-report.json",
    "media_type": "application/json",
    "producer_job_id": "job-full-001",
    "commit": "0123456789abcdef0123456789abcdef01234567",
    "configuration_id": "cc-MODE0",
    "sha256": "6666666666666666666666666666666666666666666666666666666666666666"
  },
  "summary": {
    "missing_count": 1,
    "redundant_count": 0
  }
}
```

### 2.2 ERROR_REPORT 文件结构（§9）

```json
{
  "schema_version": "2.0",
  "report_type": "ERROR_REPORT",
  "producer_job_id": "job-full-001",
  "repository": {
    "url": "https://example.com/pair03/demo-project.git",
    "commit": "0123456789abcdef0123456789abcdef01234567"
  },
  "configuration_id": "cc-MODE0",
  "findings": [
    {
      "finding_id": "finding-md-001",
      "type": "MISSING",
      "target": "main.o",
      "dependency": "config.h",
      "commit": "0123456789abcdef0123456789abcdef01234567",
      "location": {
        "file": "Makefile",
        "line": 12,
        "column": 1
      },
      "evidence": {
        "summary": "main.o uses config.h but the dependency is not declared",
        "process": "cc -c main.c -o main.o",
        "observed_file": "config.h",
        "declaration_file": "Makefile"
      },
      "detector": "BUILD_CHECKER"
    }
  ]
}
```

## 3. 增量检测：EChecker 接口

### 3.1 输入（§8.1）

```json
{
  "schema_version": "2.0",
  "trace_id": "trace-pair03-001",
  "job_type": "INCREMENTAL_CHECK",
  "input": {
    "base_commit": "0123456789abcdef0123456789abcdef01234567",
    "repository": {
      "url": "https://example.com/pair03/demo-project.git",
      "commit": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
      "project_root": "."
    },
    "environment": {
      "dockerfile": { /* DRAFT 产出的 Dockerfile ArtifactRef */ },
      "image_ref": "pair03/demo-project@sha256:2222222222222222222222222222222222222222222222222222222222222222"
    },
    "build": {
      "configuration_id": "cc-MODE0",
      "clean_command": "make clean",
      "build_command": "make"
    },
    "baseline": {
      "actual_graph_uri": "artifact://pair03/job-full-001/actual.json",
      "declared_graph_uri": "artifact://pair03/job-full-001/declared.json",
      "commit": "0123456789abcdef0123456789abcdef01234567",
      "configuration_id": "cc-MODE0"
    }
  }
}
```

### 3.2 成功输出（§8.2）

```json
{
  "current_error_report": { /* ERROR_REPORT ArtifactRef */ },
  "finding_changes": {
    "introduced": [],
    "resolved": ["finding-md-001"],
    "unchanged": []
  },
  "updated_actual_graph": { /* ACTUAL_GRAPH ArtifactRef */ },
  "updated_declared_graph": { /* DECLARED_GRAPH ArtifactRef */ }
}
```

## 4. 错误处理（§11）

### 4.1 系统错误（写入 job.error）

| 错误码 | 触发条件 | A 组响应 |
|--------|----------|----------|
| `ENV_3002` | 镜像构建失败（来自 DRAFT） | 通知 B 组重新运行 DRAFT |
| `EXEC_4002` | 任务超时 | 检查 `timeout_seconds` 设置 |
| `ANALYSIS_5001` | 分析器失败 | 检查输入格式和环境 |

### 4.2 请求拒绝（HTTP 4xx，不生成 job_id）

| HTTP 状态 | 错误码 | 触发条件 |
|-----------|--------|----------|
| 422 | `VALIDATION_1001` | `job_type` 与端点不一致 |
| 422 | `BASELINE_2001` | 增量检测缺少 baseline |
| 422 | `BASELINE_2002` | baseline 提交或配置不匹配 |
| 409 | `VERSION_2001` | 报告 commit 与源码 commit 不一致 |

## 5. Artifact 传递规则（§4.1）

| 规则 | 说明 |
|------|------|
| 带 sha256 | 所有跨组 Artifact 必须带 sha256 |
| 带 commit | 源码相关 Artifact 带完整 commit |
| 带 configuration_id | 构建配置相关 Artifact 带 configuration_id |
| 无绝对路径 | 本机绝对路径不用于跨组交接 |
| 核对完整性 | 下游必须核对 sha256 与实际文件一致 |
