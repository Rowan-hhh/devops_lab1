# DevOps Lab E2 / E3 成果索引

本仓库用于归档 E2 与 E3 阶段的接口契约、环境交接、检测报告、修复结果及验证证据。

E4 已迁移到 A、B 两组各自的独立仓库，不属于本仓库当前提交内容。

## 快速导航

| 阶段 | 组别 | 主要成果 |
|---|---|---|
| E2 | B组 | 接口契约、DRAFT 环境交接、MDFixer 接收规范、重新验证规范 |
| E2 | A组 | BuildChecker / EChecker 接口样例及检测侧交接材料 |
| E3 | B组 | DRAFT 固定环境、MDFixer Patch、candidate、重新验证证据 |
| E3 | A组 | BuildChecker 测试基线、错误报告、检测复核与最终整理 |

## E2 成果

### B组

| 路径 | 内容 |
|---|---|
| [`接口定义文档_v0.2.md`](接口定义文档_v0.2.md) | B组编写的 A/B 接口定义正文 |
| [`ab-job-contract.schema.json`](ab-job-contract.schema.json) | B组编写的机器可读任务契约 Schema |
| [`接口定义文档.pdf`](接口定义文档.pdf) | 接口定义文档 PDF 版本 |
| [`接口定义文档_v0.2.pdf`](接口定义文档_v0.2.pdf) | v0.2 接口定义文档 PDF 版本 |
| [`A-B_DRAFT环境交接包/`](A-B_DRAFT环境交接包/) | DRAFT 环境向 BuildChecker 交接的契约、结构样例和说明 |
| [`B-MDFixer-MD交接/`](B-MDFixer-MD交接/) | MDFixer 对 MD 报告的接收规范、回执样例和验收说明 |
| [`B-重新验证/`](B-重新验证/) | Patch 重新验证的请求、报告、工具和测试规范 |

其中：

- `B-MDFixer-MD交接/E3/` 属于 E3，不属于 E2。
- `B-重新验证/E3/` 属于 E3，不属于 E2。
- `A-B_DRAFT环境交接包/` 在 E2 契约基础上继续保存了 E3 的实际环境与验证成果。

### A组

| 路径 | 内容 |
|---|---|
| [`A-BuildChecker-EChecker-接口文档/`](A-BuildChecker-EChecker-接口文档/) | BuildChecker / EChecker 请求、回执、错误报告及 Artifact 交接样例 |

## E3 成果

### B组

| 负责人 | 路径 | 内容 |
|---|---|---|
| B1史美一 / B3谢真婷 | [`A-B_DRAFT环境交接包/`](A-B_DRAFT环境交接包/) | DRAFT 固定输入、构建环境、失败样例、参考环境及运行证据 |
| B1史美一 | [`A-B_DRAFT环境交接包/B1-DRAFT环境/`](A-B_DRAFT环境交接包/B1-DRAFT环境/) | Dockerfile、构建日志、参考镜像信息及验收结果 |
| B3谢真婷 | [`A-B_DRAFT环境交接包/fixtures/draft/`](A-B_DRAFT环境交接包/fixtures/draft/) | Tiny Greeting 固定源码、Makefile 和机器可读接口约定 |
| B2易容卉 | [`B-MDFixer-MD交接/E3/`](B-MDFixer-MD交接/E3/) | MDFixer 固定输入、错误报告、参考 Patch、candidate 和联调材料 |
| B4周逸涵 | [`B-重新验证/E3/`](B-重新验证/E3/) | candidate 重跑、Patch 验证、拒绝恢复及最终验证报告 |

### A组

| 路径 | 内容 |
|---|---|
| [`A-BuildChecker-E3测试基线/`](A-BuildChecker-E3测试基线/) | MD/RD 与 C0/C1/C2 测试基线、错误报告、bundle 和交接材料 |
| [`A-检测复核交接/`](A-检测复核交接/) | A组检测复核、Patch 接受记录及最终交付整理 |
| [`docs/E3A组分工.png`](docs/E3A组分工.png) | E3 A组分工说明 |

## 目录边界说明

部分目录同时包含 E2 规范和 E3 实际成果，阅读时按以下边界区分：

| 目录 | E2 部分 | E3 部分 |
|---|---|---|
| `A-B_DRAFT环境交接包/` | 契约说明、实例值表和 JSON 结构样例 | 固定 fixture、B1 构建环境和实际验证证据 |
| `B-MDFixer-MD交接/` | 根目录、`docs/` 和原有接收样例 | `E3/` |
| `B-重新验证/` | 根目录、`docs/`、`examples/`、`tools/` 和 `tests/` | `E3/` |

E2 中的 `.example.json`、占位 commit、示例 SHA-256 和示例路径仅用于说明接口结构，不能作为 E3 已完成真实运行的证据。E3 结果应以对应 E3 目录中的固定输入、实际 commit、Patch、bundle 和验证报告为准。

## 建议阅读顺序

1. 阅读 B组接口定义：[`接口定义文档_v0.2.md`](接口定义文档_v0.2.md)。
2. 查看机器可读契约：[`ab-job-contract.schema.json`](ab-job-contract.schema.json)。
3. 查看 E2 阶段 A、B 两组接口和结构样例。
4. 查看 E3 A组测试基线与错误报告。
5. 查看 E3 B组 DRAFT、MDFixer 和重新验证成果。
6. 最后查看 A组检测复核与最终整理材料。

## E4 独立仓库

E4 不在本仓库中继续开发，A、B 两组分别使用独立仓库：

- A组 BuildChecker：<https://github.com/Avaland-Kong/devops-e4-buildchecker>
- B组 DRAFT：<https://github.com/Rowan-hhh/devops-e4-draft>
