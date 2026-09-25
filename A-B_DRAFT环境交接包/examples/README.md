# JSON 结构样例说明

本材料依据《接口定义文档 v0.2》，不替代原接口文档。

本目录中的 JSON 只展示环境交接所需的既有结构，不重新设计 Job、Artifact、错误码、端点或字段语义。如果样例与原接口文档不一致，以原接口文档为准。

## 占位值

- `https://example.com/pair03/demo-project.git` 是示例仓库 URL。
- `0123456789abcdef0123456789abcdef01234567` 是示例完整 commit。
- `pair03` 是示例 `pair_id`。
- `job-draft-example`、`job-full-example` 和 `trace-pair03-example` 是示例编号。
- 重复字符组成的 64 位 `sha256` 和镜像 digest 是示例值。
- JSON 中的时间均为示例时间。
- `make`、`make test`、`make clean` 和 `cc-MODE0` 是结构占位值。

这些值不表示真实仓库、Dockerfile、镜像、构建、测试、日志或 BuildChecker 运行已经存在。真实值及其状态见 `../docs/instance-values.md`，未确定内容均标记为“待确认”。

JSON 中不使用字符串“待确认”替代 URI、commit、digest、时间、数字或枚举，因为这会使结构样例失去对应字段的格式意义。

错误 Job 样例中的 `error.details.log_uri` 仅用于展示可选的错误详情结构，不表示 v0.2 要求每一种 DRAFT 错误都必须提供该字段，也不表示对应日志已经生成。

## 文件说明

- `draft-create-request.example.json`：DRAFT 创建请求。
- `draft-create-receipt.example.json`：DRAFT 创建回执。
- `draft-job-succeeded.example.json`：DRAFT 成功 Job 的结构，不是实际成功记录。
- `draft-job-failed-env-3002.example.json`：镜像构建失败 Job。
- `draft-job-failed-draft-3001.example.json`：达到最大迭代次数仍未通过测试的 Job。
- `draft-job-timed-out-exec-4002.example.json`：DRAFT 超时 Job。
- `full-check-create-request.example.json`：FULL_CHECK 引用 DRAFT 环境的创建请求。

本目录不包含这些 URI 所指向的 Dockerfile、镜像或日志文件。
