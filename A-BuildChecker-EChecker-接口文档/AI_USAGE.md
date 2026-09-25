# AI_USAGE.md — AI 使用记录

本文件记录 AI 在设计过程中的贡献，以及人工采纳、修改和拒绝的理由。

---

## 模板格式

```markdown
### [日期] [任务名称]

**工具/模型**：WorkBuddy (LongCat-2.0) / GPT-4 / ...

**提示摘要**：用户向 AI 提出的问题或指令摘要

**AI 建议**：AI 给出的建议或生成的内容摘要

**人工决策**：
- ✅ 采纳：为什么接受 AI 的建议
- ❌ 修改：做了哪些调整，为什么
- ⛔ 拒绝：为什么不用 AI 的建议

**验证方法**：如何验证决策正确性

**关联文件**：产生的文件或 commit SHA
```

---

## 使用记录

### 2026-09-25 A 组接口文档生成（仓库 devops_lab1）

**工具/模型**：WorkBuddy (LongCat-2.0)

**提示摘要**：用户请求基于 E2 需求和 B 组交接包，在 devops_lab1 仓库中生成 A 组接口文档、JSON 样例、ADR 和 Backlog

**AI 建议**：
- 生成 `README.md`（接口总览）
- 生成 `docs/environment-handoff.md`（环境消费契约）
- 生成 `docs/instance-values.md`（实例值表）
- 生成 8 个 JSON 样例文件
- 生成 `ADR-001-async-job.md`（架构决策记录）
- 生成 `BACKLOG.md`（任务 Backlog）

**人工决策**：
- ✅ 采纳：JSON 样例的结构符合接口文档 v0.2 规范
- ✅ 采纳：pair_id 使用 `pair03`，与 B 组交接包一致
- ❌ 修改：commit SHA 使用示例值，实际运行时替换
- ❌ 修改：`instance-values.md` 中标注"待确认"的项需在课堂练习后更新

**验证方法**：
- 检查 JSON 样例能否通过 v0.2 的 `validate.py` 校验
- 与 B 组交换样例，确认双方理解一致
- 真实运行时替换占位值后再次验证

**关联文件**：
- `A-BuildChecker-EChecker-接口文档/` 目录下所有文件

### 2026-09-25 A 组 E2 样例与交付核验

**工具/模型**：Codex（文档与契约检查辅助工具）

**提示摘要**：根据 E2 任务说明核对 A 组样例、Artifact 交接约定、Backlog 状态和交付记录，并完成可验证的文档补充。

**AI 建议**：
- 补充 FULL_CHECK 与 INCREMENTAL_CHECK 的创建回执样例。
- 将固定预期发现标记为 `INSTRUCTOR_ORACLE`，并声明样例值不是实际运行证据。
- 单独记录 Artifact URI、共享路径映射和接收方校验规则。
- 将配对组未确认事项保留为待办，不填写未经确认的实例值。

**人工决策**：
- ✅ 采纳：按 v0.2 的 `CreateReceipt` 定义补充 A 服务回执样例。
- ✅ 采纳：将 ERROR_REPORT 中的固定预期发现标记为 `INSTRUCTOR_ORACLE`。
- ✅ 采纳：将 Artifact 方案标为待配对 B 组确认的提案。
- ❌ 保留：未确认 `pair_id`、共享目录和访问权限；实例值继续标记为待确认。

**验证方法**：
- 使用 `jsonschema` 4.26.0 的 Draft 2020-12 校验器检查根 Schema 和 A 组有效样例；校验器安装在临时目录，没有加入仓库依赖。
- 检查非法 `job_type` 与缺少 `baseline` 的请求按预期被拒绝。
- 静态核对 FULL_CHECK 计数、报告、Job、Artifact 引用以及 INCREMENTAL_CHECK 的 baseline 版本关系。
- 真实 Artifact 字节和双方共享目录读写在当前阶段不可验证，保持为待确认事项。

**关联文件**：
- `A-BuildChecker-EChecker-接口文档/README.md`
- `A-BuildChecker-EChecker-接口文档/ADR-002-artifact-storage-and-access.md`
- `A-BuildChecker-EChecker-接口文档/BACKLOG.md`
- `A-BuildChecker-EChecker-接口文档/docs/environment-handoff.md`
- `A-BuildChecker-EChecker-接口文档/docs/instance-values.md`
- `A-BuildChecker-EChecker-接口文档/examples/`
- `A-BuildChecker-EChecker-接口文档/E2_COMPLETION.md`
