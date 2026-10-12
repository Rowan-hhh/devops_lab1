# E4 B组最终验收与跨组互检记录

- 统筹与验收人：B4（241880179）
- 整理日期：2026-10-12（Asia/Shanghai）
- B组仓库：`https://github.com/Rowan-hhh/devops-e4-draft.git`
- 验收 SHA：`c7ec20de19d2554f2273d2d76f3739541acedf0c`
- 统一服务器：`47.97.166.140`

## 1. B4 独立重跑

- 独立学号目录：`/root/241880179/draft`
- 成功证据目录：`/root/241880179/draft/work/20261011-221335`
- 系统：Ubuntu 22.04.5 LTS，x86_64
- Docker Server：29.1.3
- Docker Compose：2.40.3
- Buildx：0.30.1
- 镜像：`e4-draft:241880179`
- 镜像 ID：`sha256:8f4440be24c04ded3ee4fa358ff6f22158174f6534e5b282a89f35a29860c5df`

| 验收项 | B4 结果 |
| --- | --- |
| `make doctor` | 通过，`problems: []` |
| 镜像构建 | 通过，架构 `amd64` |
| 单元测试 | `4 passed in 0.01s` |
| 冒烟测试 | `passed: true` |
| 预期失败识别 | `build_exit_code: 1`、`make_not_found: true`，正确捕获 `make: not found` |
| 密钥扫描 | 未发现问题；扫描 23 个文件、Git 历史和镜像 |
| `.env` | 权限 `600`，未被 Git 跟踪 |
| Git 工作区 | 无未提交修改 |
| `make all` | 全流程通过 |

镜像内工具链：

| 工具 | 版本 |
| --- | --- |
| Git | `2.47.3-0+deb13u1` |
| Docker CLI | `28.5.1`（build `e180ab8`） |
| Python | `3.13.14` |
| pytest | `8.4.2` |
| 架构 | `amd64` |

## 2. B3 与 B4 组员重跑比较

| 项目 | B3（241880360） | B4（241880179） | 结论 |
| --- | --- | --- | --- |
| 仓库 | `Rowan-hhh/devops-e4-draft` | 同一仓库 | 一致 |
| SHA | `c7ec20de19d2554f2273d2d76f3739541acedf0c` | 同一 SHA | 一致 |
| 单元测试 | `4 passed` | `4 passed` | 一致 |
| 冒烟测试 | `passed: true` | `passed: true` | 一致 |
| 密钥扫描 | 通过 | 通过 | 一致 |
| 成功证据 | `/root/241880360/draft/work/20261011-133004` | `/root/241880179/draft/work/20261011-221335` | 两份独立证据 |

结论：两名组员在独立学号目录针对同一 SHA 完成 `make all`，可比较结果一致，第④项“组员重跑与最终验收”通过。

## 3. B2 容器与安全验证纳入最终整理

- B2：241880610
- 仓库目录：`/root/E4-draft`
- 证据目录：`/root/E4-draft/work/20261012-014140`
- SHA：`c7ec20de19d2554f2273d2d76f3739541acedf0c`
- 镜像：`e4-draft:241880610`
- 镜像 ID：`sha256:a92c6ab6850b29b4036e25087c3953fc6ba0733bf11e58557cf57aa774757fbb`
- `make all`、4 项单测、冒烟和密钥扫描全部通过。
- `docker.sock` 与 `DOCKER_GID=121` 正常。
- CPU=2、内存=1G、PID=256、`no-new-privileges` 已验证。
- `.env` 权限为 `600` 且未被 Git 跟踪，Git 工作区干净。

结论：B2 的容器运行、安全与资源限制验证已纳入 B组最终整理。

## 4. A组对 B组的跨组验证

A组成员 241880617 已在统一环境中只按 B组 README 对 B组仓库独立执行 `make all`：

- 环境：Ubuntu 22.04.5、x86_64、Docker 29.1.3
- SHA：`c7ec20de19d2554f2273d2d76f3739541acedf0c`
- doctor：通过，`problems: []`
- build：通过
- 工具链：Git 2.47.3、Docker CLI 28.5.1、Python 3.13.14、pytest 8.4.2
- test：`4 passed`
- smoke：`passed: true`
- scan：未发现问题（23 个文件，含 Git 历史和镜像）

结论：A组对 B组仓库的跨组重跑与 B组结果一致，B组仓库具备一键可复现性，无阻塞或密钥泄露。

## 5. B4 任务状态

| 分工 | 状态 |
| --- | --- |
| ④ 独立重跑、结果比较、最终验收 | 已完成 |
| 收集并纳入 B2 安全与容器证据 | 已完成 |
| ⑤ A组重跑 B组仓库 | 已完成，结果一致 |
| ⑤ B组重跑 A组 BuildChecker 仓库 | 已按 README 尝试；确认存在服务器内存差异 |

## 6. B组对 A组的反向互检结果

- A组 BuildChecker 仓库：`https://github.com/Avaland-Kong/devops-e4-buildchecker.git`
- 被测 SHA：`03fa730c30d8599790a1ce635a7f19cecb0dbae3`
- B4 独立目录：`/root/241880179/a-buildchecker-clean`
- 证据目录：`/root/241880179/a-buildchecker-clean/work/20261012-143215`
- B组服务器：`47.97.166.140`，内存 3.5 GiB，无 swap
- `make doctor`：通过，`problems: []`
- `make build`：在镜像内安装 BuildChecker 编译工具链时以退出码 137 结束
- 内核证据：`apt-get` 的匿名 RSS 约 3.3 GB，触发全局 OOM，内核于 2026-10-12 16:27:30 将其终止
- 后续 `test`、`smoke`、`scan`：由于构建未完成而未执行

结论：A组仓库在 A组服务器 `47.97.163.61` 上能够完整通过，但在 B组 3.5 GiB、无 swap 的服务器上首次构建编译工具链时触发 OOM。该差异属于服务器可用内存/交换空间差异，并非 BuildChecker 单元测试或功能逻辑失败。B4 已完成按对方 README 的反向重跑尝试并提供了可复核的差异说明，因此第⑤项双向跨组互检已完成；若课程另行要求必须在 B组服务器全流程通过，应先经教师或服务器负责人批准增加 swap/内存后再重试。
