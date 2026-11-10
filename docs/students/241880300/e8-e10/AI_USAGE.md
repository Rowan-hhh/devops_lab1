# AI使用记录

工具/模型/日期：Codex（GPT-5）/ 2026-11-04。

输入上下文与问题：用户给出 E8 B4 分工截图、E8—E10 个人分支要求、正确学号 `241880300` 和课程分发包。任务是按 B 组手册完成个人实验、保留证据并提交个人贡献。

模型建议：先读取压缩包手册和仓库现状；使用 `student/241880300/e8-e10` 隔离分支；只导入 `03_实验包` 的运行代码；新增 E10 B 编译失败回滚测试；本机没有 Docker/gh 时用 WSL2 的 gcc、Make、strace 运行核心实验，并把 Docker workflow 留给 Actions。

采纳/拒绝及理由：采纳了上述分支、目录和测试方案，因为它们与手册的个人分支和 B4 职责一致。拒绝把整套授课材料嵌入仓库，也没有把本地 WSL 结果冒充 GitHub Actions 结果。

人工修改：人工选择 B4 测试输入和独立预期，导入课程运行文件，新增 `StudentE10B`，填写报告/ADR/证据索引，并检查 E8/E9 手动断言和 E10 三种验证结果。

实际验证命令/输入/结果：

- `python3 -m unittest discover -s labs/e8e10 -p test_profile.py -v`：8/8 OK，包含 B4 编译失败回滚测试。
- `python3 labs/e8e10/lab.py e8 --track B --out work/e8-B-20261110-241880300`：完成。
- `python3 labs/e8e10/lab.py e9 --track B --out work/e9-B-20261110-241880300`：完成。
- `PYTHONPATH=labs/e8e10/environment/services/buildchecker python3 labs/e8e10/lab.py e10 --track B --out work/e10-B-20261110-241880300`：`gate.json passed=true`。

未使用模型生成实验结果；所有报告中的结果来自本次 WSL 实际运行文件。未记录或提交任何 GitHub 凭据、密码、token 或设备验证码。
