# B2：MD 交接接收

本目录对应流程五“MD 交接”。B2（MDFixer）从 A 组检测负责人接收 MD/RD 报告，先完成完整性和可追溯性验收，再决定是否进入后续修复流程。

## 交付物

- [MD 接收规范](docs/md-reception.md)：接收、校验、接受/拒收的统一步骤。
- [MD 接收记录模板](examples/md-receipt.example.md)：每次交接复制一份并填写实际值。
- [AI 使用记录](AI_USAGE.md)：本目录文档的生成与校验记录。

## 与现有契约的对应关系

- A 组报告格式：[ERROR_REPORT 示例](../A-BuildChecker-EChecker-接口文档/examples/error-report.example.json)
- Artifact URI、相对路径、sha256 和 commit 约束：[ADR-002](../A-BuildChecker-EChecker-接口文档/ADR-002-artifact-storage-and-access.md)
- 完整接口定义：[接口定义文档 v0.2](../接口定义文档_v0.2.md)

## 使用边界

接收阶段只确认报告能否被 B2 可靠消费，不在本阶段修改源代码、不创建修复 commit。只有接收状态为 `ACCEPTED`，后续才允许根据 `MISSING` finding 发起修复；`REDUNDANT` 只记录并交给后续约定流程处理。

