# B：重新验证

本目录对应流程七“重新验证”。B 在 B2/MDFixer 产出并接受候选 Patch 后，使用同一构建环境和配置执行 rebuild、test、recheck，并把证据交给 B+B2 做最终接受或拒绝决定。

当前仓库是 E2 接口契约仓库，没有真实项目源码、Patch、镜像、Artifact 或运行日志。本目录中的命令、commit、Finding、时间和日志路径均为结构占位值，不代表真实联调已经完成。

## B 的边界

- B2 先确认 A 组 `ERROR_REPORT` 完整、可读、commit 和配置匹配，并接受可处理的 `MISSING` finding。
- 流程发起方负责在 `base_commit` 上应用 Patch 并产生新的完整 `candidate_commit`。
- B 不修改源代码、不执行 `git apply`、不创建 commit，也不自动推送或合并。
- B 只在候选 workspace 中执行 clean（若配置）、build、test 和 recheck。
- 只有构建、测试、重检都成功，且选中的 finding 全部消失，验证记录才是 `ACCEPTED`。否则记录 `REJECTED`，执行失败使用 `REPAIR_3001`。

## 文件索引

| 文件 | 用途 |
| --- | --- |
| [`docs/revalidation.md`](docs/revalidation.md) | 输入、阶段顺序、验收、证据和失败处理规范 |
| [`docs/instance-values.md`](docs/instance-values.md) | 真实联调前由双方填写的实例值清单 |
| [`examples/revalidation-request.example.json`](examples/revalidation-request.example.json) | B 验证请求结构样例 |
| [`examples/revalidation-report-succeeded.example.json`](examples/revalidation-report-succeeded.example.json) | `ACCEPTED` 结构样例 |
| [`examples/revalidation-report-rejected.example.json`](examples/revalidation-report-rejected.example.json) | `REJECTED` 结构样例 |
| [`tools/revalidate.py`](tools/revalidate.py) | Python 标准库验证器和命令行入口 |
| [`tests/test_revalidate.py`](tests/test_revalidate.py) | 本地单元测试和失败路径测试 |
| [`AI_USAGE.md`](AI_USAGE.md) | AI 建议、人工取舍和验证记录 |

## 运行方式

将请求样例复制为真实请求并填写真实值，然后在已应用候选 Patch 的 workspace 中执行：

```text
python B-重新验证/tools/revalidate.py \
  --request B-重新验证/examples/revalidation-request.json \
  --workspace <candidate-workspace> \
  --output <candidate-workspace>/b-verification.json
```

Windows PowerShell 可以使用同样的参数分行方式，或将命令写成一行。程序退出码为：`0` 表示 `ACCEPTED`，`1` 表示候选执行完成但被拒绝，`2` 表示请求、文件或 workspace 配置错误。

## 与现有契约的关系

- 字段语义以仓库根目录 [`接口定义文档_v0.2.md`](../接口定义文档_v0.2.md) 和 [`ab-job-contract.schema.json`](../ab-job-contract.schema.json) 为准。
- B2 的接收前置条件见 [`B-MDFixer-MD交接/docs/md-reception.md`](../B-MDFixer-MD交接/docs/md-reception.md)。
- Artifact URI 和共享路径核验见 [`A-BuildChecker-EChecker-接口文档/ADR-002-artifact-storage-and-access.md`](../A-BuildChecker-EChecker-接口文档/ADR-002-artifact-storage-and-access.md)。
- B 验证记录是对 REPAIR `validation` 的过程性补充，不替代 `RepairSuccessOutput`，不修改根目录 Schema。
