# B 重新验证交付设计

## 背景与目标

B 负责在 B2/MDFixer 产生候选 Patch 后，按同一构建环境和配置重新验证候选修改。当前仓库已经包含 E2 v0.2 接口契约、A 组检测材料和 B2 的 MD 接收规范，但没有可运行的源码项目、真实 Patch、镜像或日志。因此本次交付提供可审计的 B 规范、样例、验证记录模板和一个本地验证工具，不伪造真实 rebuild、test 或 recheck 结果。

成功判据与现有接口契约保持一致：候选修改必须完成构建和测试，并且重检报告中不再包含本次选择的 `MISSING` finding。任一阶段失败时，验证结果为拒绝，使用契约规定的 `REPAIR_3001`，且不得把失败候选标为成功。

## 范围与非目标

范围：

- 读取 B2 已接受的修复上下文：修复前 `base_commit`、候选提交、选中的 `finding_ids`、`configuration_id`、构建/测试/重检命令和重检报告路径。
- 按顺序执行 clean（若提供）、build、test、recheck，并保存每个阶段的退出码、耗时、日志相对路径和失败原因。
- 校验重检报告为 JSON，确认选中的 finding ID 已全部消失。
- 生成 `ACCEPTED` 或 `REJECTED` 的 B 验证记录；记录可供 B+B2 最终接受或拒绝 Patch。
- 提供成功、失败和待填写的文档样例，并说明真实 Artifact 的 `artifact://` 映射、SHA-256、commit 和配置核验。

非目标：

- 不实现 DRAFT、BuildChecker、EChecker 或 MDFixer 服务。
- 不修改源代码、不自动创建修复 commit、不替代流程发起方执行 `git apply`。
- 不把示例 commit、摘要、日志、镜像或报告声明为真实运行结果。
- 不重新定义 `RepairCreateRequest`、`RepairSuccessOutput`、`ArtifactRef` 或错误码。

## 交付结构

新增 `B-重新验证/`：

- `README.md`：B 角色边界、运行入口、接受/拒绝规则和契约链接。
- `docs/revalidation.md`：逐阶段验证规范、输入输出字段、证据保存和人工复核要求。
- `docs/instance-values.md`：真实联调前需要双方填写的仓库、commit、配置、命令和 Artifact 值；默认全部标记为待确认。
- `examples/revalidation-request.example.json`：只描述结构的请求样例。
- `examples/revalidation-report-succeeded.example.json`：结构成功样例，明确为占位证据。
- `examples/revalidation-report-rejected.example.json`：重检仍含选中 finding 时的失败样例。
- `tools/revalidate.py`：标准库实现的本地验证器。
- `tests/test_revalidate.py`：`unittest` 测试，覆盖成功路径、构建失败、测试失败、重检残留 finding、非法报告和命令超时。
- `AI_USAGE.md`：记录本次材料中 AI 建议、人工取舍和验证命令。

## 工具接口与数据流

命令入口：

```text
python B-重新验证/tools/revalidate.py \
  --request B-重新验证/examples/revalidation-request.json \
  --workspace <candidate-workspace> \
  --output <verification-report.json>
```

请求 JSON 使用以下字段：

- `schema_version` 固定为 `2.0`。
- `base_commit` 为 Patch 针对的修复前完整 SHA。
- `candidate_commit` 为流程发起方应用 Patch 后的完整 SHA；工具只记录和校验格式，不创建 commit。
- `finding_ids` 为本次 Patch 选择的 `MISSING` finding ID 列表，不能为空。
- `configuration_id` 必须与 A 组报告和 REPAIR 请求一致。
- `commands.clean` 可选；`commands.build`、`commands.test`、`commands.recheck` 必填。命令以字符串保存，供本地 shell 执行并原样记录。
- `recheck_report` 为候选 workspace 内的仓库相对 JSON 路径；重检命令必须产生该文件。
- `timeout_seconds` 为单个阶段的超时上限。

数据流：

```text
B2 accepted receipt
        │
        ▼
request validation ── invalid ──► REJECTED / validation error
        │
        ▼
clean → build → test → recheck report
        │       │       │          │
        │       │       │          └─ selected finding remains? reject
        │       │       └──────────── exit != 0? reject
        │       └──────────────────── exit != 0? reject
        └──────────────────────────── command error/timeout? reject
                                      │
                                      ▼
                         verification report + evidence logs
```

工具以子进程的退出码作为 build/test/recheck 的执行判据，以重检 JSON 中的 `findings[].finding_id` 作为 finding 消失判据。它不会猜测“命令输出看起来像成功”，也不会在输入缺失时生成 `ACCEPTED`。

## 输出与证据

验证记录包含：

- `verification_status`: `ACCEPTED` 或 `REJECTED`。
- `base_commit`、`candidate_commit`、`configuration_id` 和 `finding_ids`。
- `validation.clean`、`validation.build`、`validation.test`、`validation.recheck`，每项含 `success`、`exit_code`、`duration_ms`、日志相对路径；未执行阶段明确记录原因。
- `remaining_selected_findings`：重检报告中仍存在的选中 finding ID。
- 成功时 `error` 为 `null`；构建、测试、重检失败或 selected finding 残留时，`error.code` 为 `REPAIR_3001`。
- `generated_at` 使用 UTC RFC 3339。

工具生成的日志和报告必须位于候选 workspace 或其指定的证据目录中，并使用仓库相对路径。跨组交接时，再按主契约将文件映射为 `artifact://{pair_id}/{job_id}/{file_name}`，由接收方核对原始字节 SHA-256、适用 commit 和 `configuration_id`。

成功的 B 记录只能证明当前候选通过了 rebuild、test、recheck。最终是否接受 Patch 仍由 B+B2 按记录共同确认；工具不会自动推送、合并或创建新 commit。

## 错误处理

- 请求 JSON 无法解析、缺字段、空 finding 列表、SHA 格式错误或命令配置非法：在执行前拒绝，并返回可定位的校验错误；不生成成功记录。
- clean/build/test/recheck 返回非零退出码：记录阶段日志和退出码，验证状态为 `REJECTED`，错误码为 `REPAIR_3001`。
- 阶段超时或进程无法启动：终止该阶段进程（在平台允许时），记录超时或启动错误，验证状态为 `REJECTED`，错误码为 `REPAIR_3001`。
- 重检报告不存在、无法解析、结构不完整或 `findings` 不是数组：拒绝候选并记录报告错误。
- 重检报告仍包含任意选中的 `finding_id`：拒绝候选，列出残留 ID；不把 Patch 放入成功输出。

## 测试与验收

测试使用 Python 标准库 `unittest`，不新增运行时依赖。测试通过临时目录和可移植的 Python 子进程模拟 build/test/recheck，验证：

1. clean/build/test/recheck 全部退出 0 且选中 finding 消失时生成 `ACCEPTED`。
2. build 或 test 返回非零时生成 `REJECTED`，并停止后续阶段。
3. recheck 返回 0 但仍含选中 finding 时生成 `REJECTED` 和 `REPAIR_3001`。
4. 重检报告 JSON 无法解析或结构错误时拒绝。
5. 阶段超时后生成拒绝记录且保留超时证据。
6. 输出日志路径为相对路径，成功记录不携带本机绝对路径作为交接字段。

文档验收还包括：所有示例明确声明占位值；成功样例的 `remaining_selected_findings` 为空；失败样例的 `output`/成功状态不被误用；README、B2 记录和 v0.2 契约之间的字段语义一致。

## 兼容性与风险

- 工具只消费 B 自己定义的验证请求，不改变仓库根目录 Schema；契约字段仍以 `接口定义文档_v0.2.md` 和 `ab-job-contract.schema.json` 为准。
- 命令字符串需依赖调用方环境；真实联调前必须在 `instance-values.md` 记录平台、工作目录和命令，并由双方确认。
- Windows 与 POSIX shell 的命令语法可能不同；样例只表达结构，真实命令必须按执行平台填写。
- 工具不具备容器隔离能力，不能代替安全的构建沙箱；生产或公共环境应在受控 runner 中执行。
