# A/B 联调实例值

本文件记录 A/B 双方约定的真实运行配置。严格依据《接口定义文档 v0.2》。

**标记说明**：
- ✅ 已确认：双方已对齐
- 🔴 B 组提供：必须由 B 组同学填写
- 🟡 A 组可提供：A 组同学可自行决定

## 1. 小组编号

| 项目 | 值 | 状态 |
|------|-----|------|
| pair_id | `pair03` | ✅ 已确认（与 B 组交接包一致） |
| trace_id 前缀 | `trace-pair03` | ✅ 已确认 |

## 2. 源码版本

| 项目 | 值 | 状态 |
|------|-----|------|
| `repository.url` | 🔴 B 组提供 | 待 B 组提供仓库 URL |
| `repository.commit` | 🔴 B 组提供 | 待 B 组提供完整 commit SHA |
| `repository.project_root` | `.`（根目录） | ✅ 已确认 |
| A/B 均能取得同一 commit | 🔴 B 组确认 | 待 B 组确认仓库访问方式 |

## 3. 构建配置

| 项目 | 值 | 状态 |
|------|-----|------|
| `configuration_id` | `cc-MODE0` | ✅ 已确认（v0.2 参考值） |
| DRAFT `build_command` | 🔴 B 组提供 | 待 B 组提供 |
| DRAFT `test_command` | 🔴 B 组提供 | 待 B 组提供 |
| FULL_CHECK `clean_command` | `make clean` | 🟡 A 组提议，待 B 组确认 |
| FULL_CHECK `build_command` | `make` | 🟡 A 组提议，待 B 组确认 |

## 4. 服务参数

| 项目 | 值 | 状态 |
|------|-----|------|
| DRAFT 服务 base URL | 🔴 B 组提供 | 待 B 组提供 |
| FULL_CHECK 服务 base URL | 🟡 A 组提供 | A 组部署后填写 |
| HTTP 鉴权方式 | 无（本地联调） | 🟡 A 组提议 |
| `max_iterations` | 5 | ✅ 已确认（v0.2 默认值） |
| `timeout_seconds` | 600 | ✅ 已确认（v0.2 默认值） |
| Job 查询间隔 | 5 秒 | 🟡 A 组提议 |

## 5. Artifact 共享

| 项目 | 值 | 状态 |
|------|-----|------|
| 共享方式 | 仓库内 `artifacts/` 目录，git push/pull 同步 | 🟡 A 组提议，待 B 组确认 |
| `sha256` 计算方法 | `sha256sum file \| awk '{print $1}'` | ✅ 已确认 |

## 6. 当前产物和证据

| 项目 | 状态 |
|------|------|
| 真实 DRAFT 环境交付 | 待 B 组交付 |
| 真实 FULL_CHECK 运行 | 待 A 组部署后验证 |
| 真实 ERROR_REPORT 产出 | 待 A 组部署后验证 |
| 真实增量检测运行 | 待 A 组部署后验证 |
