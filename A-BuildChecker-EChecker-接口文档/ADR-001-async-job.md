# ADR-001: 采用异步 Job 模型处理耗时构建/检测任务

## 状态

ACCEPTED

## 背景

在 DevOps 教学实验中，构建、全量依赖检测、增量检测、修复验证等任务可能耗时较长，超出单次 HTTP 请求的生命周期。

课程约束（来自 E2 课件）：
- 多个微服务（DRAFT、BuildChecker、EChecker、MDFixer）需跨组协作
- 每个任务可能涉及 Docker 镜像构建、源码编译、依赖分析等耗时操作
- 同一流程中的多个任务需要串联（trace_id）
- 大日志和依赖图不能塞进每个响应

## 决策

采用异步 Job 模型（§1 总体接口风格）：
1. 客户端通过 `POST /v1/{job-type}-jobs` 创建任务，服务端返回 `202 Accepted` 和 `job_id`
2. 客户端通过 `GET /v1/jobs/{job_id}` 轮询任务状态
3. 状态流转：`QUEUED → RUNNING → SUCCEEDED / FAILED / TIMED_OUT / CANCELLED`
4. 同一次完整流程使用相同的 `trace_id` 串联
5. 创建请求携带 `Idempotency-Key` 实现幂等性

端点设计（§1.2）：

| 操作 | 端点 | 实现方 |
|------|------|--------|
| 生成构建环境 | `POST /v1/dockerfile-jobs` | B |
| 全量检测 | `POST /v1/full-check-jobs` | A |
| 增量检测 | `POST /v1/incremental-check-jobs` | A |
| 修复缺失依赖 | `POST /v1/repair-jobs` | B |
| 查询任务 | `GET /v1/jobs/{job_id}` | 接收该任务的服务 |

## 替代方案

| 方案 | 优点 | 后果 |
|------|------|------|
| **同步等待** | 实现简单，一次请求拿到结果 | 客户端与执行耦合，超时不稳定，大日志塞进响应 |
| **异步 Job（已选）** | 解耦客户端与执行，支持长时间任务，进度可查询 | 需要任务存储与查询机制 |

## 后果

- 需要实现任务存储与查询
- 需要设计轮询策略（间隔、超时）
- 使用契约样例验证行为一致性
- 创建请求需携带 `Idempotency-Key` 防止重复创建
- Job 保存元数据，大日志/图/补丁通过 Artifact 引用传递（§4）

## 关联

- Backlog：统一任务模型、产物访问约定
- B 组接口定义：DRAFT 环境交接契约
