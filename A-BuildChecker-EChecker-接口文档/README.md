# A 组接口文档（BuildChecker + EChecker）

本材料是 `A-B_DRAFT环境交接包` 的对等文档，定义 A 组作为环境消费者和检测服务提供者与 B 组之间的接口契约。

本文档严格依据《接口定义文档 v0.2》，所有 JSON 样例使用 `pair03` 作为 pair_id，与 B 组交接包保持一致。

## 角色与职责

| 小组 | 服务 | 职责 | 上游（输入来自） | 下游（输出交给） |
|------|------|------|------------------|------------------|
| **A** | **BuildChecker** | 全量依赖检测，输出 MD/RD 报告 | B 组 DRAFT（环境）+ 仓库源码 | B 组 MDFixer |
| **A** | **EChecker** | 跨提交增量检测，对比基线图 | B 组 DRAFT + BuildChecker 基线图 | B 组 MDFixer |
| B | DRAFT | 生成可构建环境 | 仓库源码 | A 组 BuildChecker / EChecker |
| B | MDFixer | 修复缺失依赖 | A 组 MD 报告 | 重新构建与检测 |

## 接口边界

```
┌─────────────────────────────────────────────────────────────────┐
│                        完整流程                                   │
│                                                                   │
│  仓库 ──→ [DRAFT: B组] ──→ EnvironmentRef ──→ [BuildChecker: A组] │
│                                       │              │            │
│                                       │              ↓            │
│                                       │         MD/RD 报告        │
│                                       │              │            │
│                                       ↓              ↓            │
│                               [EChecker: A组] ←── 基线图          │
│                                       │                           │
│                                       ↓                           │
│                                  增量检测结果                      │
│                                       │                           │
│                                       ↓                           │
│                                  [MDFixer: B组]                   │
└─────────────────────────────────────────────────────────────────┘
```

## 文件索引

| 文件 | 说明 |
|------|------|
| `docs/environment-handoff.md` | A 组消费 DRAFT 环境的契约规则 |
| `docs/instance-values.md` | 双方约定的真实实例值 |
| `examples/full-check-create-request.example.json` | BuildChecker 创建请求（§7.1） |
| `examples/full-check-job-succeeded.example.json` | BuildChecker 成功结果（§7.2） |
| `examples/full-check-job-failed.example.json` | BuildChecker 失败结果 |
| `examples/incremental-check-create-request.example.json` | EChecker 创建请求（§8.1） |
| `examples/incremental-check-job-succeeded.example.json` | EChecker 成功结果（§8.2） |
| `examples/error-report.example.json` | ERROR_REPORT 文件结构（§9） |
| `examples/invalid-request-wrong-job-type.example.json` | 无效请求样例（`job_type` 为 `ABC`，应被拒绝） |
| `ADR-001-async-job.md` | 架构决策记录 |
| `BACKLOG.md` | 任务 Backlog |
| `AI_USAGE.md` | AI 使用记录 |

## 使用边界

- 本文档不修改 B 组定义的接口字段、枚举值、状态流转、错误码或端点
- 如与《接口定义文档 v0.2》存在不一致，以原接口文档为准
- 所有 JSON 样例使用 `pair03` 作为示例 pair_id
