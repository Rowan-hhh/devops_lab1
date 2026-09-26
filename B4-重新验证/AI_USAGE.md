# AI_USAGE — B4 重新验证材料

## 工具与任务

- 工具/模型：Codex（GPT-5 agent）
- 任务：根据 E2 PPT、流程分工截图、GitHub 仓库现有接口文档和 B2 交接材料，补齐 B4 的重新验证交付物。
- 提示摘要：B4 负责对 B2/MDFixer 候选 Patch 执行 rebuild、test、recheck，并将完成结果推送到仓库。

## AI 建议与人工判断

| AI 建议 | 人工采纳/修改/拒绝 | 理由 |
| --- | --- | --- |
| 新增 B4 目录，提供规范、样例和验证工具 | 采纳 | 现有仓库是接口文档仓库，没有可直接修改的业务源码；需要可追溯的交付材料 |
| 使用 Python 标准库实现本地验证器 | 采纳 | 不增加依赖，便于课堂环境运行和审阅 |
| 工具自动应用 Patch、创建 commit 并推送 | 拒绝 | B4 的职责是重新验证；Patch 应用、提交和最终接受由流程发起方与 B4+B2 协作完成 |
| 在没有真实项目输入时生成成功运行日志 | 拒绝 | 会把结构样例误报成真实证据，违反 E2 可追溯性要求 |
| 使用 `REPAIR_3001` 表示执行后候选无效 | 采纳 | 与接口定义文档 v0.2 的 REPAIR 成功条件和错误模型一致 |

## 关联文件与验证

- 设计：`docs/superpowers/specs/2026-09-26-b4-revalidation-design.md`
- 计划：`docs/superpowers/plans/2026-09-26-b4-revalidation-plan.md`
- 实现：`B4-重新验证/tools/b4_revalidate.py`
- 测试：`B4-重新验证/tests/test_b4_revalidate.py`
- 主要验证命令：`python -m unittest discover -s B4-重新验证/tests -p "test_*.py" -v`
- 说明：本次提交只验证了合成临时 workspace 的工具行为；没有真实源码、Patch、镜像或 Artifact，因此没有声称真实项目 rebuild/test/recheck 成功。
