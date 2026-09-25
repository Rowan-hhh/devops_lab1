# A/B 联调实例值（A 组视角）

本文件记录 A/B 双方约定的真实运行配置。严格依据《接口定义文档 v0.2》。所有"待确认"项需在课堂练习中与 B 组确认后填写。

## 1. 小组编号

| 项目 | 值 | 状态 |
|------|-----|------|
| pair_id | `pair03` | 已确认（与 B 组交接包一致） |
| trace_id 前缀 | `trace-pair03` | 已确认 |

## 2. 源码版本

| 项目 | 值 | 状态 |
|------|-----|------|
| `repository.url` | 待确认 | 待确认 |
| `repository.commit` | 待确认 | 必须为完整 commit SHA |
| `repository.project_root` | `.`（根目录） | 已确认 |
| A/B 均能取得同一 commit | 待确认 | 待确认 |

## 3. 构建配置

| 项目 | 值 | 状态 |
|------|-----|------|
| `configuration_id` | `cc-MODE0` | 已确认（v0.2 参考值） |
| DRAFT `build_command` | 待确认 | 由 B 组决定 |
| DRAFT `test_command` | 待确认 | 由 B 组决定 |
| FULL_CHECK `clean_command` | 待确认 | 待确认 |
| FULL_CHECK `build_command` | 待确认 | 待确认 |

## 4. 服务参数

| 项目 | 值 | 状态 |
|------|-----|------|
| DRAFT 服务 base URL | 待确认 | 待确认 |
| FULL_CHECK 服务 base URL | 待确认 | 待确认 |
| HTTP 鉴权方式 | 待确认 | 待确认 |
| `max_iterations` | 5（v0.2 参考值） | 待确认 |
| `timeout_seconds` | 600（v0.2 参考值） | 待确认 |

## 5. Artifact 共享

| 项目 | 值 | 状态 |
|------|-----|------|
| 共享仓库或目录 | 待确认 | 待确认 |
| `sha256` 计算方法 | `sha256sum file \| awk '{print $1}'` | 已确认 |

## 6. 当前产物和证据

| 项目 | 状态 |
|------|------|
| 真实 DRAFT 环境交付 | 待确认 |
| 真实 FULL_CHECK 运行 | 待确认 |
| 真实 ERROR_REPORT 产出 | 待确认 |
| 真实增量检测运行 | 待确认 |
