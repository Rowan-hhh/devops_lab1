# DRAFT–BuildChecker 环境交接包

本材料依据《接口定义文档 v0.2》，不替代原接口文档。

本目录用于帮助 A/B 双方按既有接口契约完成 DRAFT 环境到 BuildChecker 的交接。它只提取环境交接所需的规则、待确认的实例值和 JSON 结构样例，不重新设计 Job、Artifact、错误码、端点或字段语义。

如本材料与《接口定义文档 v0.2》存在不一致，以原接口文档为准。接口基线见 [`../接口定义文档_v0.2.md`](../接口定义文档_v0.2.md)。

## 当前状态

本包不表示真实联调已经完成。当前真实状态如下：

| 项目 | 状态 |
| --- | --- |
| 真实仓库、commit 与项目目录 | 待确认 |
| 真实构建与测试命令 | 待确认 |
| 真实 Dockerfile | 待确认 |
| 真实镜像及 digest | 待确认 |
| 真实构建结果 | 待确认 |
| 真实测试结果 | 待确认 |
| Artifact 共享位置和访问权限 | 待确认 |
| A/B 首次环境交付与试跑结果 | 待确认 |

本目录没有生成或附带真实 Dockerfile、镜像、日志、Artifact 或测试结果。

## 文件索引

- [`docs/environment-handoff.md`](docs/environment-handoff.md)：环境交接所需的契约规则及核对点。
- [`docs/instance-values.md`](docs/instance-values.md)：真实联调参数表；未确定内容统一标记为“待确认”。
- [`examples/README.md`](examples/README.md)：JSON 示例的占位值和使用限制。
- `examples/*.example.json`：DRAFT 请求、回执、Job 结果及 FULL_CHECK 请求的结构样例。

建议先阅读本文件，再阅读环境交接说明和实例值表，最后查看 JSON 结构样例。

## 示例值声明

所有 `.example.json` 文件仅用于说明 v0.2 的既有结构。JSON 中的仓库 URL、commit、`sha256` 和镜像 digest 都是结构占位值：

- `example.com` 是示例域名；
- `0123456789abcdef0123456789abcdef01234567` 是示例完整 commit；
- 重复字符组成的 64 位 `sha256` 和镜像 digest 是示例值；
- `pair03`、示例 `job_id`、`trace_id` 和时间均为结构占位值；
- `make`、`make test`、`make clean` 和 `cc-MODE0` 是结构占位值，并不表示双方已经选定这些命令或配置。

结构样例不能作为真实运行证据。实际值及确认状态只在 `docs/instance-values.md` 中记录。

## 使用边界

- 不在本包中修改接口字段、枚举值、状态流转、错误码或端点。
- 不把运行配置新增为接口字段。
- 不使用 `.example.json` 声称服务已经受理、构建、测试、发布镜像或完成检测。
- 真实文件产物必须按 v0.2 的 `artifact://` 规则交接，并由接收方核对其内容和元数据。
