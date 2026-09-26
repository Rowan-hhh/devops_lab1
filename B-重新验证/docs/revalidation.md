# B 重新验证规范

## 1. 目的与前置条件

B 接收 B2 已接受的修复上下文，并确认候选 Patch 在约定环境下真正生效。进入 B 前必须具备：

1. A 组 `ERROR_REPORT` 的目标 commit、`configuration_id` 和选中的 `MISSING` finding。
2. B2 接收记录及允许进入修复的 `finding_ids`。
3. 流程发起方在 `base_commit` 上应用候选 Patch 后产生的 `candidate_commit`。
4. 与 DRAFT/FULL_CHECK 相同的 `EnvironmentRef`、构建配置和可执行命令。

B 工具不应用 Patch，也不替 B2 判断报告是否完整。它验证的是已经准备好的 candidate workspace。

## 2. 请求字段

验证器消费一个补充请求，字段如下：

| 字段 | 必填 | 约束 |
| --- | --- | --- |
| `schema_version` | 是 | 固定为 `2.0` |
| `base_commit` | 是 | Patch 针对的 40 位小写完整 SHA |
| `candidate_commit` | 是 | 应用 Patch 后的 40 位小写完整 SHA |
| `configuration_id` | 是 | 必须与 A 组报告、REPAIR 请求和环境一致 |
| `finding_ids` | 是 | 非空、唯一，只能列出本次选择的 `MISSING` finding |
| `commands.clean` | 否 | 清理命令；为空时记录为跳过 |
| `commands.build` | 是 | 构建命令 |
| `commands.test` | 是 | 测试命令 |
| `commands.recheck` | 是 | 重新检测命令，必须生成 `recheck_report` |
| `recheck_report` | 是 | candidate workspace 内的相对 JSON 路径，不得包含 `..` 或绝对路径 |
| `timeout_seconds` | 是 | 每个阶段的正数超时上限 |

真实 REPAIR 请求仍须满足主契约中 `clean_command`、`build_command`、`test_command` 和 `configuration_id` 的要求；本请求只是 B 执行记录的本地入口。

## 3. 阶段顺序

验证器严格按以下顺序执行，并在第一个失败阶段停止：

| 阶段 | 通过条件 | 失败结果 |
| --- | --- | --- |
| clean | 配置为空，或命令退出码为 0 | 停止并拒绝 |
| build | 命令退出码为 0 | 停止并拒绝 |
| test | 命令退出码为 0 | 停止并拒绝 |
| recheck | 命令退出码为 0，且报告可解析 | 检查 Finding 后决定 |

每个阶段的 stdout/stderr 写入 `b-evidence/<stage>.log`。报告记录退出码、耗时、相对日志路径；未执行阶段记录 `skipped` 和原因。超时阶段记录 `timed_out`，其后的阶段不执行。

## 4. 重检判定

重检报告必须是 JSON 对象，并包含数组 `findings`。每条 Finding 至少需要字符串 `finding_id`。验证器只将报告中仍出现的选中 ID 放入 `remaining_selected_findings`：

- `remaining_selected_findings` 为空，且 build/test/recheck 均通过：`verification_status=ACCEPTED`。
- 任意选中 ID 仍存在：`verification_status=REJECTED`，错误码 `REPAIR_3001`。
- 报告不存在、JSON 无法解析或结构不完整：`verification_status=REJECTED`，错误码 `REPAIR_3001`。

报告中出现未被本次 Patch 选择的其他 Finding，不会单独导致本次候选被拒绝，但 B+B2 应在最终确认时记录是否需要另行处理。

## 5. 输出记录

输出 JSON 至少包含：

```json
{
  "schema_version": "2.0",
  "verification_status": "ACCEPTED",
  "base_commit": "<40 位完整 SHA>",
  "candidate_commit": "<40 位完整 SHA>",
  "configuration_id": "<配置编号>",
  "finding_ids": ["<选中的 finding>"] ,
  "validation": {
    "build": {"success": true, "exit_code": 0, "duration_ms": 123, "log_path": "b-evidence/build.log"},
    "test": {"success": true, "exit_code": 0, "duration_ms": 123, "log_path": "b-evidence/test.log"},
    "recheck": {"success": true, "exit_code": 0, "duration_ms": 123, "log_path": "b-evidence/recheck.log"}
  },
  "remaining_selected_findings": [],
  "error": null,
  "generated_at": "<UTC RFC 3339 时间>"
}
```

失败执行使用 `verification_status=REJECTED`、`error.code=REPAIR_3001` 和阶段信息；请求本身不合法时使用 `VALIDATION_1001`，不启动任何命令。

## 6. Artifact 与最终确认

日志、重检报告和验证记录必须先保存在共享目录中的相对路径。跨组交接时按主契约映射：

```text
artifact://{pair_id}/{job_id}/{file_name}
    ↕
artifacts/{pair_id}/{job_id}/{file_name}
```

接收方需要核对原始字节 SHA-256、适用 commit、`configuration_id`、`producer_job_id` 和文件可读性。禁止用本机绝对路径作为交接地址。

B 的 `ACCEPTED` 只证明当前候选完成 rebuild、test、recheck 且选中 Finding 消失。B 与 B2 仍需共同确认接受或拒绝 Patch；接受后由流程发起方决定如何提交和推送。

## 7. 当前证据限制

本仓库没有真实 candidate workspace、Patch、镜像或 recheck report。因此本目录的样例和本次提交不能证明真实项目已经构建、测试或重检成功。真实联调前必须填写 [`instance-values.md`](instance-values.md)，并把实际日志和 Artifact 引用附上。
