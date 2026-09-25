# Backlog — DevOps 教学实验

## 使用说明

- 每项任务有负责人、产物和验收条件
- 状态：`TODO` / `IN_PROGRESS` / `DONE` / `BLOCKED`
- 优先级：P0（必须）/ P1（重要）/ P2（可选）

---

## E2 任务（接口契约）

| ID | 任务 | 责任方 | 产物 | 验收条件 | 状态 |
|----|------|--------|------|----------|------|
| E2-01 | 统一任务模型（四类 Job） | A+B 共同 | `task.schema.json` | 四类对象可表达 | TODO |
| E2-02 | BuildChecker 接口定义 | A 组 | FULL_CHECK 请求/响应样例 | 包含 environment + MD/RD 输出 | DONE |
| E2-03 | EChecker 接口定义 | A 组 | INCREMENTAL_CHECK 请求/响应样例 | 基线图引用正确 | DONE |
| E2-04 | ERROR_REPORT 格式定义 | A 组 | MISSING/RD 发现样例 | 包含 finding_id + evidence | DONE |
| E2-05 | 产物访问约定 | A+B 共同 | ADR + 契约样例 | 说明下游读取方式 | TODO |
| E2-06 | Artifact 共享机制 | A+B 共同 | 共享目录 + sha256 规范 | 双方可读写 | TODO |
| E2-07 | 与 B 组三轮配对练习 | A+B 共同 | 双方签字的接口样例 | 课堂完成 | DONE |
| E2-08 | ADR 记录 | A+B 各自 | ADR 文档 | 记录异步 Job 决策 | DONE |
| E2-09 | 个人贡献记录 | 各自 | Git 提交 + Issue/PR | 可追溯 | TODO |

---

## E3 任务（并行测试基线）

| ID | 任务 | 责任方 | 产物 | 验收条件 | 状态 |
|----|------|--------|------|----------|------|
| E3-01 | MD/RD 项目准备 | A 组 | 可运行的 BuildChecker 项目 | 支持 C0/C1/C2 基线 | TODO |
| E3-02 | C0/C1/C2 提交版本 | A+B 各自 | 三个连续 commit | 增量变化可追溯 | TODO |
| E3-03 | 基线依赖图 | A 组 | C0 的 actual.json | EChecker 可消费 | TODO |
| E3-04 | 增量检测基线 | A 组 | C1 对比 C0 的结果 | 新增/消除可识别 | TODO |
| E3-05 | 并行测试执行 | A 组 | 测试报告 | 全量+增量均通过 | TODO |

---

## 已完成

（暂无）
